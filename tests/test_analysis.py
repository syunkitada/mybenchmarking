"""Tests for benchmark analysis and comparison functions."""

import pytest
from datetime import datetime
from mybench.analysis.compare import (
    calculate_delta,
    compare_results,
    detect_config_changes,
    generate_trend_data,
)
from mybench.models.result import BenchmarkResult
from mybench.models.config import SystemConfiguration, KernelConfig


class TestCalculateDelta:
    """Tests for calculate_delta function (T058)."""

    def test_positive_change(self):
        """Test delta calculation with positive change."""
        result = calculate_delta(100.0, 150.0)
        assert result["value1"] == 100.0
        assert result["value2"] == 150.0
        assert result["delta"] == 50.0
        assert result["percent_change"] == 50.0

    def test_negative_change(self):
        """Test delta calculation with negative change."""
        result = calculate_delta(200.0, 150.0)
        assert result["value1"] == 200.0
        assert result["value2"] == 150.0
        assert result["delta"] == -50.0
        assert result["percent_change"] == -25.0

    def test_no_change(self):
        """Test delta calculation with no change."""
        result = calculate_delta(100.0, 100.0)
        assert result["value1"] == 100.0
        assert result["value2"] == 100.0
        assert result["delta"] == 0.0
        assert result["percent_change"] == 0.0

    def test_zero_baseline(self):
        """Test delta calculation with zero baseline."""
        result = calculate_delta(0.0, 50.0)
        assert result["value1"] == 0.0
        assert result["value2"] == 50.0
        assert result["delta"] == 50.0
        assert result["percent_change"] == float("inf")

    def test_accuracy_within_threshold(self):
        """Test calculation accuracy is within <1% error (T058 requirement)."""
        # Test with known values
        result = calculate_delta(1000.0, 1234.5)
        expected_percent = 23.45
        actual_percent = result["percent_change"]
        error = abs(expected_percent - actual_percent) / expected_percent * 100
        assert error < 1.0, f"Error {error}% exceeds 1% threshold"

    def test_small_values_accuracy(self):
        """Test accuracy with small decimal values."""
        result = calculate_delta(0.123, 0.456)
        expected_delta = 0.333
        actual_delta = result["delta"]
        error = abs(expected_delta - actual_delta) / expected_delta * 100
        assert error < 1.0, f"Error {error}% exceeds 1% threshold"

    def test_large_values_accuracy(self):
        """Test accuracy with large values."""
        result = calculate_delta(1000000.0, 1500000.0)
        assert result["percent_change"] == 50.0
        assert result["delta"] == 500000.0


class TestCompareResults:
    """Tests for compare_results function (T059)."""

    def test_compare_same_tool_same_metrics(self):
        """Test comparing results from the same tool with same metrics."""
        result1 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 10, 0, 0),
            category="cpu",
            tool="sysbench",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"threads": 8, "time": 60},
            results={"events_per_second": 10000.0, "total_events": 600000},
        )

        result2 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 11, 0, 0),
            category="cpu",
            tool="sysbench",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"threads": 8, "time": 60},
            results={"events_per_second": 12000.0, "total_events": 720000},
        )

        deltas = compare_results(result1, result2)

        assert "events_per_second" in deltas
        assert deltas["events_per_second"]["delta"] == 2000.0
        assert deltas["events_per_second"]["percent_change"] == 20.0

        assert "total_events" in deltas
        assert deltas["total_events"]["delta"] == 120000
        assert deltas["total_events"]["percent_change"] == 20.0

    def test_compare_different_metrics(self):
        """Test comparing results with different metric types (T059)."""
        result1 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 10, 0, 0),
            category="disk",
            tool="fio",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"bs": "4k", "iodepth": 32, "rw": "randread"},
            results={
                "read_iops": 50000.0,
                "read_bw_kb": 200000.0,
                "lat_avg_us": 640.0,
                "lat_99th_us": 1200.0,
            },
        )

        result2 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 11, 0, 0),
            category="disk",
            tool="fio",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"bs": "4k", "iodepth": 32, "rw": "randread"},
            results={
                "read_iops": 60000.0,
                "read_bw_kb": 240000.0,
                "lat_avg_us": 530.0,
                "lat_99th_us": 1000.0,
            },
        )

        deltas = compare_results(result1, result2)

        # Check IOPS improvement
        assert deltas["read_iops"]["percent_change"] == 20.0

        # Check bandwidth improvement
        assert deltas["read_bw_kb"]["percent_change"] == 20.0

        # Check latency improvement (lower is better, so negative change)
        assert deltas["lat_avg_us"]["percent_change"] < 0
        assert deltas["lat_99th_us"]["percent_change"] < 0

    def test_compare_non_numeric_values(self):
        """Test that non-numeric values are handled gracefully."""
        result1 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 10, 0, 0),
            category="cpu",
            tool="sysbench",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"threads": 8},
            results={"events_per_second": 10000.0, "status": "completed"},
        )

        result2 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 11, 0, 0),
            category="cpu",
            tool="sysbench",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"threads": 8},
            results={"events_per_second": 12000.0, "status": "completed"},
        )

        deltas = compare_results(result1, result2)

        assert "status" in deltas
        assert deltas["status"]["delta"] == "N/A"
        assert deltas["status"]["percent_change"] == "N/A"

    def test_compare_different_tools_raises_error(self):
        """Test that comparing different tools raises ValueError."""
        result1 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 10, 0, 0),
            category="cpu",
            tool="sysbench",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"threads": 8},
            results={"events_per_second": 10000.0},
        )

        result2 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 11, 0, 0),
            category="cpu",
            tool="stress-ng",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"cpu": 8},
            results={"bogo_ops": 50000.0},
        )

        with pytest.raises(ValueError, match="Cannot compare different tools"):
            compare_results(result1, result2)

    def test_compare_different_categories_raises_error(self):
        """Test that comparing different categories raises ValueError."""
        result1 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 10, 0, 0),
            category="cpu",
            tool="sysbench",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"threads": 8},
            results={"events_per_second": 10000.0},
        )

        result2 = BenchmarkResult(
            schema_version="1.0",
            timestamp=datetime(2025, 11, 9, 11, 0, 0),
            category="memory",
            tool="sysbench",
            system_profile_id="test-system",
            configuration=SystemConfiguration(
                os="Ubuntu 22.04",
                kernel=KernelConfig(version="5.15.0"),
            ),
            benchmark_parameters={"threads": 8},
            results={"throughput_mib": 5000.0},
        )

        with pytest.raises(ValueError, match="Cannot compare different categories"):
            compare_results(result1, result2)


class TestDetectConfigChanges:
    """Tests for detect_config_changes function (T060)."""

    def test_kernel_parameter_changes(self):
        """Test kernel parameter differences detection (T060)."""
        config1 = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(
                version="5.15.0",
                cpu_governor="performance",
                parameters={
                    "transparent_hugepage": "always",
                    "numa_balancing": "1",
                },
            ),
        )

        config2 = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(
                version="5.15.0",
                cpu_governor="performance",
                parameters={
                    "transparent_hugepage": "madvise",
                    "numa_balancing": "1",
                },
            ),
        )

        changes = detect_config_changes(config1, config2)

        assert "param_transparent_hugepage" in changes["kernel"]
        thp_change = changes["kernel"]["param_transparent_hugepage"]
        assert thp_change["old"] == "always"
        assert thp_change["new"] == "madvise"

    def test_kernel_version_change(self):
        """Test detection of kernel version change."""
        config1 = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(version="5.15.0"),
        )

        config2 = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(version="6.2.0"),
        )

        changes = detect_config_changes(config1, config2)

        assert changes["kernel"]["version"]["old"] == "5.15.0"
        assert changes["kernel"]["version"]["new"] == "6.2.0"

    def test_cpu_governor_change(self):
        """Test detection of CPU governor change."""
        config1 = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(version="5.15.0", cpu_governor="powersave"),
        )

        config2 = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(version="5.15.0", cpu_governor="performance"),
        )

        changes = detect_config_changes(config1, config2)

        assert changes["kernel"]["cpu_governor"]["old"] == "powersave"
        assert changes["kernel"]["cpu_governor"]["new"] == "performance"

    def test_os_change(self):
        """Test detection of OS change."""
        config1 = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(version="5.15.0"),
        )

        config2 = SystemConfiguration(
            os="Ubuntu 24.04",
            kernel=KernelConfig(version="6.8.0"),
        )

        changes = detect_config_changes(config1, config2)

        assert changes["os"] is not None
        assert changes["os"]["old"] == "Ubuntu 22.04"
        assert changes["os"]["new"] == "Ubuntu 24.04"

    def test_environment_variable_changes(self):
        """Test detection of environment variable changes."""
        config1 = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(version="5.15.0"),
            environment={"OMP_NUM_THREADS": "8", "GOMP_CPU_AFFINITY": "0-7"},
        )

        config2 = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(version="5.15.0"),
            environment={"OMP_NUM_THREADS": "16", "GOMP_CPU_AFFINITY": "0-15"},
        )

        changes = detect_config_changes(config1, config2)

        assert "OMP_NUM_THREADS" in changes["environment"]
        assert changes["environment"]["OMP_NUM_THREADS"]["old"] == "8"
        assert changes["environment"]["OMP_NUM_THREADS"]["new"] == "16"

    def test_no_changes(self):
        """Test that identical configurations show no changes."""
        config = SystemConfiguration(
            os="Ubuntu 22.04",
            kernel=KernelConfig(
                version="5.15.0",
                cpu_governor="performance",
                parameters={"transparent_hugepage": "always"},
            ),
        )

        changes = detect_config_changes(config, config)

        assert changes["os"] is None
        assert len(changes["kernel"]) == 0
        assert len(changes["software"]) == 0
        assert len(changes["environment"]) == 0


class TestGenerateTrendData:
    """Tests for generate_trend_data function."""

    def test_trend_data_with_multiple_results(self):
        """Test generating trend data from multiple results."""
        results = [
            BenchmarkResult(
                schema_version="1.0",
                timestamp=datetime(2025, 11, 9, 10, 0, 0),
                category="cpu",
                tool="sysbench",
                system_profile_id="test-system",
                label="baseline",
                configuration=SystemConfiguration(
                    os="Ubuntu 22.04",
                    kernel=KernelConfig(version="5.15.0"),
                ),
                benchmark_parameters={"threads": 8},
                results={"events_per_second": 10000.0},
            ),
            BenchmarkResult(
                schema_version="1.0",
                timestamp=datetime(2025, 11, 9, 11, 0, 0),
                category="cpu",
                tool="sysbench",
                system_profile_id="test-system",
                label="after-tuning",
                configuration=SystemConfiguration(
                    os="Ubuntu 22.04",
                    kernel=KernelConfig(version="5.15.0"),
                ),
                benchmark_parameters={"threads": 8},
                results={"events_per_second": 11000.0},
            ),
            BenchmarkResult(
                schema_version="1.0",
                timestamp=datetime(2025, 11, 9, 12, 0, 0),
                category="cpu",
                tool="sysbench",
                system_profile_id="test-system",
                label="optimized",
                configuration=SystemConfiguration(
                    os="Ubuntu 22.04",
                    kernel=KernelConfig(version="5.15.0"),
                ),
                benchmark_parameters={"threads": 8},
                results={"events_per_second": 12000.0},
            ),
        ]

        trends = generate_trend_data(results)

        assert "events_per_second" in trends
        assert len(trends["events_per_second"]) == 3
        assert trends["events_per_second"][0]["value"] == 10000.0
        assert trends["events_per_second"][1]["value"] == 11000.0
        assert trends["events_per_second"][2]["value"] == 12000.0

    def test_trend_data_with_empty_results(self):
        """Test generating trend data with empty list."""
        trends = generate_trend_data([])
        assert trends == {}

    def test_trend_data_with_missing_metrics(self):
        """Test trend data handles missing metrics gracefully."""
        results = [
            BenchmarkResult(
                schema_version="1.0",
                timestamp=datetime(2025, 11, 9, 10, 0, 0),
                category="cpu",
                tool="sysbench",
                system_profile_id="test-system",
                configuration=SystemConfiguration(
                    os="Ubuntu 22.04",
                    kernel=KernelConfig(version="5.15.0"),
                ),
                benchmark_parameters={"threads": 8},
                results={"events_per_second": 10000.0, "total_events": 600000},
            ),
            BenchmarkResult(
                schema_version="1.0",
                timestamp=datetime(2025, 11, 9, 11, 0, 0),
                category="cpu",
                tool="sysbench",
                system_profile_id="test-system",
                configuration=SystemConfiguration(
                    os="Ubuntu 22.04",
                    kernel=KernelConfig(version="5.15.0"),
                ),
                benchmark_parameters={"threads": 8},
                results={"events_per_second": 11000.0},  # total_events missing
            ),
        ]

        trends = generate_trend_data(results)

        assert len(trends["events_per_second"]) == 2
        assert len(trends["total_events"]) == 1  # Only first result has it
