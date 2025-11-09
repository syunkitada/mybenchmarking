"""Tests for storage integrity and JSON operations."""

import pytest
import json
from pathlib import Path
from datetime import date, datetime
from mybench.storage.base import (
    atomic_save_json,
    load_and_validate_json,
    save_model_to_json,
)
from mybench.storage.profiles import (
    save_system_profile,
    load_system_profile,
    list_system_profiles,
    profile_exists,
)
from mybench.storage.results import (
    save_benchmark_result,
    load_benchmark_result,
    list_benchmark_results,
    get_result_by_id,
)
from mybench.models.system import (
    SystemProfile,
    CPUSpec,
    MemorySpec,
    DiskSpec,
    NetworkSpec,
    HardwareSpecs,
)
from mybench.models.result import BenchmarkResult
from mybench.models.config import (
    SystemConfiguration,
    KernelConfig,
)


def test_atomic_save_json(tmp_path):
    """Test atomic JSON save creates valid file."""
    filepath = tmp_path / "test.json"
    data = {"key": "value", "number": 42}

    atomic_save_json(filepath, data)

    assert filepath.exists()
    with open(filepath, "r") as f:
        loaded = json.load(f)
    assert loaded == data


def test_atomic_save_json_creates_directory(tmp_path):
    """Test atomic save creates parent directories."""
    filepath = tmp_path / "subdir" / "test.json"
    data = {"test": True}

    atomic_save_json(filepath, data)

    assert filepath.exists()


def test_load_and_validate_json_success(tmp_path):
    """Test loading and validating valid JSON."""
    filepath = tmp_path / "profile.json"

    profile_data = {
        "profile_id": "test",
        "profile_name": "Test",
        "type": "physical",
        "created": "2025-11-09",
        "hardware": {
            "cpu": {"model": "Intel", "cores": 4, "threads": 4},
            "memory": {"total_gb": 16},
            "disk": {"type": "SSD", "capacity_gb": 500},
            "network": {},
        },
    }

    with open(filepath, "w") as f:
        json.dump(profile_data, f)

    profile = load_and_validate_json(filepath, SystemProfile)
    assert profile.profile_id == "test"
    assert profile.hardware.cpu.cores == 4


def test_load_and_validate_json_validation_error(tmp_path):
    """Test that invalid data raises validation error."""
    filepath = tmp_path / "invalid.json"

    # Missing required fields
    invalid_data = {"profile_id": "test"}

    with open(filepath, "w") as f:
        json.dump(invalid_data, f)

    with pytest.raises(Exception):  # Pydantic ValidationError
        load_and_validate_json(filepath, SystemProfile)


def test_save_model_to_json(tmp_path):
    """Test saving Pydantic model to JSON."""
    filepath = tmp_path / "profile.json"

    profile = SystemProfile(
        profile_id="test",
        profile_name="Test System",
        type="physical",
        created=date(2025, 11, 9),
        hardware=HardwareSpecs(
            cpu=CPUSpec(model="Intel", cores=4, threads=4),
            memory=MemorySpec(total_gb=16),
            disk=DiskSpec(type="SSD", capacity_gb=500),
            network=NetworkSpec(),
        ),
    )

    save_model_to_json(filepath, profile)

    assert filepath.exists()

    # Verify can be loaded back
    loaded = load_and_validate_json(filepath, SystemProfile)
    assert loaded.profile_id == profile.profile_id
    assert loaded.hardware.cpu.cores == 4


def test_json_is_pretty_printed(tmp_path):
    """Test that saved JSON is human-readable (pretty-printed)."""
    filepath = tmp_path / "test.json"
    data = {"key": "value", "nested": {"a": 1, "b": 2}}

    atomic_save_json(filepath, data)

    with open(filepath, "r") as f:
        content = f.read()

    # Check for indentation (pretty-print)
    assert '  "key"' in content or "  " in content
    # Check for trailing newline
    assert content.endswith("\n")


def test_benchmark_result_save_load_integrity(tmp_path):
    """Test benchmark result maintains data integrity through save/load."""
    filepath = tmp_path / "result.json"

    result = BenchmarkResult(
        timestamp=datetime(2025, 11, 9, 14, 30, 22),
        category="cpu",
        tool="sysbench",
        label="baseline",
        system_profile_id="test-desktop",
        configuration=SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(version="5.15.0", cpu_governor="performance"),
        ),
        benchmark_parameters={"threads": 8, "time": 60},
        results={"events_per_second": 12543.67, "total_time": 60.0001},
    )

    save_model_to_json(filepath, result)
    loaded = load_and_validate_json(filepath, BenchmarkResult)

    # Verify data integrity
    assert loaded.tool == result.tool
    assert loaded.category == result.category
    assert loaded.system_profile_id == result.system_profile_id
    assert loaded.results["events_per_second"] == 12543.67
    assert loaded.configuration.kernel.cpu_governor == "performance"


def test_save_and_load_system_profile(tmp_path):
    """Test saving and loading system profiles."""
    systems_dir = tmp_path / "systems"

    profile = SystemProfile(
        profile_id="test-desktop",
        profile_name="Test Desktop",
        type="physical",
        created=date(2025, 11, 9),
        hardware=HardwareSpecs(
            cpu=CPUSpec(model="Intel i7", cores=8, threads=8),
            memory=MemorySpec(total_gb=32),
            disk=DiskSpec(type="NVMe SSD", capacity_gb=1000),
            network=NetworkSpec(),
        ),
    )

    # Save
    filepath = save_system_profile(profile, systems_dir)
    assert filepath.exists()
    assert filepath.name == "test-desktop.json"

    # Load
    loaded = load_system_profile("test-desktop", systems_dir)
    assert loaded.profile_id == "test-desktop"
    assert loaded.hardware.cpu.cores == 8


def test_profile_exists(tmp_path):
    """Test profile existence check."""
    systems_dir = tmp_path / "systems"

    assert not profile_exists("nonexistent", systems_dir)

    profile = SystemProfile(
        profile_id="exists",
        profile_name="Exists",
        type="physical",
        created=date.today(),
        hardware=HardwareSpecs(
            cpu=CPUSpec(model="CPU", cores=4, threads=4),
            memory=MemorySpec(total_gb=16),
            disk=DiskSpec(type="SSD", capacity_gb=500),
            network=NetworkSpec(),
        ),
    )
    save_system_profile(profile, systems_dir)

    assert profile_exists("exists", systems_dir)


def test_list_system_profiles(tmp_path):
    """Test listing system profiles."""
    systems_dir = tmp_path / "systems"

    # Create multiple profiles
    for i in range(3):
        profile = SystemProfile(
            profile_id=f"system-{i}",
            profile_name=f"System {i}",
            type="physical",
            created=date.today(),
            hardware=HardwareSpecs(
                cpu=CPUSpec(model="CPU", cores=4, threads=4),
                memory=MemorySpec(total_gb=16),
                disk=DiskSpec(type="SSD", capacity_gb=500),
                network=NetworkSpec(),
            ),
        )
        save_system_profile(profile, systems_dir)

    profiles = list_system_profiles(systems_dir)
    assert len(profiles) == 3
    assert all(isinstance(p, SystemProfile) for p in profiles)


def test_save_and_load_benchmark_result(tmp_path):
    """Test saving and loading benchmark results."""
    results_dir = tmp_path / "results"

    result = BenchmarkResult(
        timestamp=datetime(2025, 11, 9, 14, 30, 22),
        category="cpu",
        tool="sysbench",
        system_profile_id="test-system",
        configuration=SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(version="5.15.0"),
        ),
        benchmark_parameters={"threads": 8},
        results={"score": 1000.5},
    )

    # Save
    filepath = save_benchmark_result(result, results_dir)
    assert filepath.exists()
    assert "2025-11-09_143022_sysbench.json" == filepath.name

    # Load
    loaded = load_benchmark_result(filepath)
    assert loaded.tool == "sysbench"
    assert loaded.results["score"] == 1000.5


def test_list_benchmark_results_with_filters(tmp_path):
    """Test listing benchmark results with filters."""
    results_dir = tmp_path / "results"

    # Create multiple results
    for i in range(3):
        result = BenchmarkResult(
            timestamp=datetime(2025, 11, 9, 14, i, 0),
            category="cpu",
            tool=f"tool-{i}",
            system_profile_id="system-1" if i < 2 else "system-2",
            label="test" if i == 0 else None,
            configuration=SystemConfiguration(
                os="Ubuntu",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={},
            results={"value": i},
        )
        save_benchmark_result(result, results_dir)

    # List all
    all_results = list_benchmark_results(results_dir)
    assert len(all_results) == 3

    # Filter by system
    system1_results = list_benchmark_results(results_dir, system_profile_id="system-1")
    assert len(system1_results) == 2

    # Filter by label
    labeled_results = list_benchmark_results(results_dir, label="test")
    assert len(labeled_results) == 1


def test_get_result_by_id(tmp_path):
    """Test getting a specific result by ID."""
    results_dir = tmp_path / "results"

    result = BenchmarkResult(
        timestamp=datetime(2025, 11, 9, 14, 30, 22),
        category="cpu",
        tool="sysbench",
        system_profile_id="test",
        configuration=SystemConfiguration(
            os="Ubuntu",
            kernel=KernelConfig(version="5.15.0"),
        ),
        benchmark_parameters={},
        results={"score": 100},
    )
    save_benchmark_result(result, results_dir)

    # Get by ID
    loaded = get_result_by_id("2025-11-09_143022_sysbench", results_dir)
    assert loaded is not None
    assert loaded.tool == "sysbench"

    # Non-existent ID
    not_found = get_result_by_id("nonexistent", results_dir)
    assert not_found is None
