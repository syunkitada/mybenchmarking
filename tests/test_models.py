"""Tests for Pydantic model validation."""

import pytest
from datetime import date, datetime
from mybench.models import (
    SystemProfile,
    CPUSpec,
    MemorySpec,
    DiskSpec,
    NetworkSpec,
    HardwareSpecs,
    SystemConfiguration,
    KernelConfig,
    BenchmarkResult,
)


def test_system_profile_physical_valid():
    """Test valid physical system profile."""
    profile = SystemProfile(
        profile_id="test-desktop",
        profile_name="Test Desktop",
        type="physical",
        created=date(2025, 11, 9),
        hardware=HardwareSpecs(
            cpu=CPUSpec(model="Intel Core i7", cores=8, threads=16),
            memory=MemorySpec(total_gb=32),
            disk=DiskSpec(type="NVMe SSD", capacity_gb=1000),
            network=NetworkSpec(),
        ),
    )
    assert profile.profile_id == "test-desktop"
    assert profile.type == "physical"


def test_system_profile_invalid_cores():
    """Test that invalid core count raises validation error."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        SystemProfile(
            profile_id="test",
            profile_name="Test",
            type="physical",
            created=date(2025, 11, 9),
            hardware=HardwareSpecs(
                cpu=CPUSpec(model="Intel", cores=0, threads=1),  # Invalid: must be > 0
                memory=MemorySpec(total_gb=8),
                disk=DiskSpec(type="SSD", capacity_gb=100),
                network=NetworkSpec(),
            ),
        )


def test_benchmark_result_valid():
    """Test valid benchmark result."""
    result = BenchmarkResult(
        timestamp=datetime(2025, 11, 9, 14, 30, 22),
        category="cpu",
        tool="sysbench",
        system_profile_id="test-desktop",
        configuration=SystemConfiguration(
            os="Ubuntu 22.04", kernel=KernelConfig(version="5.15.0")
        ),
        benchmark_parameters={"threads": 8},
        results={"events_per_second": 12543.67},
    )
    assert result.category == "cpu"
    assert result.schema_version == "1.0"


def test_benchmark_result_invalid_category():
    """Test that invalid category raises validation error."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        BenchmarkResult(
            timestamp=datetime.now(),
            category="invalid",  # Not in Literal options
            tool="test",
            system_profile_id="test",
            configuration=SystemConfiguration(
                os="Linux", kernel=KernelConfig(version="5.0")
            ),
            benchmark_parameters={},
            results={},
        )


def test_system_configuration_valid():
    """Test valid system configuration."""
    config = SystemConfiguration(
        os="Ubuntu 22.04",
        kernel=KernelConfig(
            version="5.15.0",
            parameters={"intel_pstate": "active"},
            cpu_governor="performance",
        ),
    )
    assert config.os == "Ubuntu 22.04"
    assert config.kernel.cpu_governor == "performance"
