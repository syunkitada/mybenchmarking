"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def tmp_systems_dir(tmp_path):
    """Create temporary systems directory."""
    systems_dir = tmp_path / "systems"
    systems_dir.mkdir()
    return systems_dir


@pytest.fixture
def tmp_results_dir(tmp_path):
    """Create temporary results directory structure."""
    results_dir = tmp_path / "results"
    for category in ["cpu", "memory", "disk", "network"]:
        (results_dir / category).mkdir(parents=True)
    return results_dir
