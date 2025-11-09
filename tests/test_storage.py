"""Tests for storage integrity and JSON operations."""

import pytest
import json
from pathlib import Path
from datetime import date, datetime
from mybench.storage import (
    atomic_save_json,
    load_and_validate_json,
    save_model_to_json,
)
from mybench.models import (
    SystemProfile,
    CPUSpec,
    MemorySpec,
    DiskSpec,
    NetworkSpec,
    HardwareSpecs,
    BenchmarkResult,
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
