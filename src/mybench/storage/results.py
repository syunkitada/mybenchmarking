"""Benchmark result storage operations."""

from pathlib import Path
from typing import List, Literal, Optional

from ..models.result import BenchmarkResult
from .base import load_and_validate_json, save_model_to_json


def save_benchmark_result(
    result: BenchmarkResult, results_dir: Path, category: Optional[str] = None
) -> Path:
    """
    Save a benchmark result to JSON file with timestamp filename.

    Args:
        result: BenchmarkResult to save
        results_dir: Base results directory
        category: Optional category override (uses result.category if not
            provided)

    Returns:
        Path to saved result file

    Raises:
        IOError: If file cannot be written
    """
    cat = category or result.category
    category_dir = results_dir / cat
    category_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename: YYYY-MM-DD_HHMMSS_tool.json
    timestamp = result.timestamp.strftime("%Y-%m-%d_%H%M%S")
    filename = f"{timestamp}_{result.tool}.json"
    filepath = category_dir / filename

    save_model_to_json(filepath, result)
    return filepath


def load_benchmark_result(filepath: Path) -> BenchmarkResult:
    """
    Load a benchmark result from JSON file.

    Args:
        filepath: Path to result file

    Returns:
        Loaded BenchmarkResult

    Raises:
        FileNotFoundError: If result file doesn't exist
        ValidationError: If JSON doesn't match schema
    """
    return load_and_validate_json(filepath, BenchmarkResult)


def list_benchmark_results(
    results_dir: Path,
    category: Optional[Literal["cpu", "memory", "disk", "network"]] = None,
    system_profile_id: Optional[str] = None,
    label: Optional[str] = None,
) -> List[BenchmarkResult]:
    """
    List benchmark results with optional filters.

    Args:
        results_dir: Base results directory
        category: Filter by category (cpu, memory, disk, network)
        system_profile_id: Filter by system profile ID
        label: Filter by label

    Returns:
        List of BenchmarkResult objects, sorted by timestamp (newest first)

    Raises:
        ValidationError: If any JSON file is invalid
    """
    if not results_dir.exists():
        return []

    results = []

    # Determine which directories to scan
    if category:
        search_dirs = [results_dir / category]
    else:
        search_dirs = [
            results_dir / cat for cat in ["cpu", "memory", "disk", "network"]
        ]

    # Load results from all applicable directories
    for cat_dir in search_dirs:
        if not cat_dir.exists():
            continue

        for filepath in cat_dir.glob("*.json"):
            try:
                result = load_and_validate_json(filepath, BenchmarkResult)

                # Apply filters
                if system_profile_id and (
                    result.system_profile_id != system_profile_id
                ):
                    continue
                if label and result.label != label:
                    continue

                results.append(result)
            except Exception as e:
                # Log error but continue processing other files
                print(f"Warning: Failed to load {filepath}: {e}")

    # Sort by timestamp, newest first
    results.sort(key=lambda r: r.timestamp, reverse=True)
    return results


def get_result_by_id(result_id: str, results_dir: Path) -> Optional[BenchmarkResult]:
    """
    Find and load a result by its ID (timestamp_tool pattern).

    Args:
        result_id: Result identifier (e.g., "2025-11-09_143022_sysbench")
        results_dir: Base results directory

    Returns:
        BenchmarkResult if found, None otherwise
    """
    # Search all category directories
    for cat in ["cpu", "memory", "disk", "network"]:
        cat_dir = results_dir / cat
        if not cat_dir.exists():
            continue

        filepath = cat_dir / f"{result_id}.json"
        if filepath.exists():
            try:
                return load_and_validate_json(filepath, BenchmarkResult)
            except Exception as e:
                print(f"Warning: Failed to load {filepath}: {e}")
                return None

    return None
