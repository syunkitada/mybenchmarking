"""Benchmark comparison and analysis functions."""

from typing import Any, Dict, List
from ..models.result import BenchmarkResult
from ..models.config import SystemConfiguration


def calculate_delta(value1: float, value2: float) -> Dict[str, Any]:
    """
    Calculate delta and percentage change between two values.

    Args:
        value1: First value (baseline)
        value2: Second value (comparison)

    Returns:
        Dict with delta, percent_change, value1, value2
    """
    delta = value2 - value1
    if value1 != 0:
        percent_change = (delta / value1) * 100
    else:
        percent_change = float("inf") if delta > 0 else float("-inf")

    return {
        "value1": value1,
        "value2": value2,
        "delta": delta,
        "percent_change": percent_change,
    }


def compare_results(
    result1: BenchmarkResult, result2: BenchmarkResult
) -> Dict[str, Dict[str, Any]]:
    """
    Compare two benchmark results and calculate deltas for all metrics.

    Args:
        result1: First benchmark result (baseline)
        result2: Second benchmark result (comparison)

    Returns:
        Dict mapping metric names to delta information

    Raises:
        ValueError: If results are from different tools or categories
    """
    if result1.tool != result2.tool:
        raise ValueError(
            f"Cannot compare different tools: {result1.tool} vs {result2.tool}"  # noqa: E501
        )

    if result1.category != result2.category:
        raise ValueError(
            f"Cannot compare different categories: "
            f"{result1.category} vs {result2.category}"
        )

    deltas = {}

    # Get all metrics from both results
    all_metrics = set(result1.results.keys()) | set(result2.results.keys())

    for metric in all_metrics:
        value1 = result1.results.get(metric)
        value2 = result2.results.get(metric)

        # Only compare numeric values
        if isinstance(value1, (int, float)) and isinstance(
            value2, (int, float)
        ):  # noqa: E501
            deltas[metric] = calculate_delta(value1, value2)
        else:
            # Store non-numeric values for reference
            deltas[metric] = {
                "value1": value1,
                "value2": value2,
                "delta": "N/A",
                "percent_change": "N/A",
            }

    return deltas


def detect_config_changes(
    config1: SystemConfiguration, config2: SystemConfiguration
) -> Dict[str, Any]:
    """
    Detect configuration changes between two system configurations.

    Args:
        config1: First system configuration
        config2: Second system configuration

    Returns:
        Dict with categorized configuration changes
    """
    changes = {
        "os": None,
        "kernel": {},
        "software": {},
        "environment": {},
    }

    # Check OS change
    if config1.os != config2.os:
        changes["os"] = {"old": config1.os, "new": config2.os}

    # Check kernel changes
    if config1.kernel.version != config2.kernel.version:
        changes["kernel"]["version"] = {
            "old": config1.kernel.version,
            "new": config2.kernel.version,
        }

    if config1.kernel.cpu_governor != config2.kernel.cpu_governor:
        changes["kernel"]["cpu_governor"] = {
            "old": config1.kernel.cpu_governor,
            "new": config2.kernel.cpu_governor,
        }

    # Check kernel parameters
    params1 = config1.kernel.parameters or {}
    params2 = config2.kernel.parameters or {}
    all_params = set(params1.keys()) | set(params2.keys())
    for param in all_params:
        val1 = params1.get(param)
        val2 = params2.get(param)
        if val1 != val2:
            changes["kernel"][f"param_{param}"] = {"old": val1, "new": val2}

    # Check software version changes
    sw1_dict = config1.software.model_dump() if config1.software else {}
    sw2_dict = config2.software.model_dump() if config2.software else {}
    all_sw = set(sw1_dict.keys()) | set(sw2_dict.keys())
    for sw in all_sw:
        val1 = sw1_dict.get(sw)
        val2 = sw2_dict.get(sw)
        if val1 != val2:
            changes["software"][sw] = {"old": val1, "new": val2}

    # Check environment variable changes
    env1 = config1.environment or {}
    env2 = config2.environment or {}
    all_env = set(env1.keys()) | set(env2.keys())
    for env_var in all_env:
        val1 = env1.get(env_var)
        val2 = env2.get(env_var)
        if val1 != val2:
            changes["environment"][env_var] = {"old": val1, "new": val2}

    return changes


def generate_trend_data(
    results: List[BenchmarkResult],
) -> Dict[str, List[Any]]:  # noqa: E501
    """
    Generate time-series trend data from multiple results.

    Args:
        results: List of benchmark results, should be sorted by timestamp

    Returns:
        Dict mapping metric names to lists of (timestamp, value) tuples
    """
    if not results:
        return {}

    trends = {}

    # Collect all unique metrics
    all_metrics = set()
    for result in results:
        all_metrics.update(result.results.keys())

    # Build time series for each metric
    for metric in all_metrics:
        trend_data = []
        for result in results:
            value = result.results.get(metric)
            if value is not None:
                trend_data.append(
                    {
                        "timestamp": result.timestamp,
                        "value": value,
                        "label": result.label,
                    }
                )
        trends[metric] = trend_data

    return trends
