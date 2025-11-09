"""Benchmark result data models."""

from typing import Any, Dict, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .config import SystemConfiguration


class BenchmarkResult(BaseModel):
    """Benchmark result file structure."""

    schema_version: str = Field(
        default="1.0", description="Schema version for compatibility"
    )
    timestamp: datetime = Field(description="Benchmark execution timestamp")
    category: Literal["cpu", "memory", "disk", "network"] = Field(
        description="Benchmark category"
    )
    tool: str = Field(description="Benchmark tool name")
    label: Optional[str] = Field(None, description="Optional label for this result")
    system_profile_id: str = Field(description="Reference to system profile")
    configuration: SystemConfiguration = Field(
        description="System configuration at benchmark time"
    )
    benchmark_parameters: Dict[str, Any] = Field(
        description="Parameters used for the benchmark"
    )
    results: Dict[str, Any] = Field(description="Benchmark results and metrics")
    raw_output: Optional[str] = Field(None, description="Raw benchmark output")
