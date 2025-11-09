"""Rich formatting utilities for CLI output."""

from typing import Any, Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
import json

from ..models.system import SystemProfile
from ..models.result import BenchmarkResult

console = Console()


def format_system_profiles_table(profiles: List[SystemProfile]) -> Table:
    """Format system profiles as a Rich table."""
    table = Table(title="System Profiles", show_header=True)
    table.add_column("Profile ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Type", style="yellow")
    table.add_column("CPU", style="white")
    table.add_column("Memory", style="white")
    table.add_column("Created", style="dim")

    for profile in profiles:
        # Extract CPU info based on type
        if hasattr(profile.hardware.cpu, "model"):
            cpu_info = f"{profile.hardware.cpu.model} ({profile.hardware.cpu.cores}c)"  # noqa: E501
        else:
            cpu_info = f"{profile.hardware.cpu.vcpus} vCPUs"

        memory_info = f"{profile.hardware.memory.total_gb}GB"

        table.add_row(
            profile.profile_id,
            profile.profile_name,
            profile.type,
            cpu_info,
            memory_info,
            str(profile.created),
        )

    return table


def format_system_profile_detail(profile: SystemProfile) -> None:
    """Display detailed system profile information."""
    # Convert to dict and pretty print
    data = profile.model_dump(exclude_none=True)
    json_str = json.dumps(data, indent=2, default=str)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)

    console.print(
        Panel(
            syntax,
            title=f"[bold cyan]System Profile: {profile.profile_name}[/]",
            border_style="cyan",
        )
    )


def format_benchmark_results_table(results: List[BenchmarkResult]) -> Table:
    """Format benchmark results as a Rich table."""
    table = Table(title="Benchmark Results", show_header=True)
    table.add_column("Timestamp", style="cyan")
    table.add_column("Category", style="yellow")
    table.add_column("Tool", style="green")
    table.add_column("System", style="white")
    table.add_column("Label", style="magenta")
    table.add_column("Key Metrics", style="white")

    for result in results:
        # Extract key metrics (first few items)
        metrics = []
        for key, value in list(result.results.items())[:3]:
            if isinstance(value, float):
                metrics.append(f"{key}: {value:.2f}")
            else:
                metrics.append(f"{key}: {value}")
        metrics_str = ", ".join(metrics)

        table.add_row(
            result.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            result.category,
            result.tool,
            result.system_profile_id,
            result.label or "-",
            metrics_str,
        )

    return table


def format_benchmark_result_detail(result: BenchmarkResult) -> None:
    """Display detailed benchmark result information."""
    # Convert to dict and pretty print
    data = result.model_dump(exclude_none=True)
    json_str = json.dumps(data, indent=2, default=str)
    syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)

    result_id = result.timestamp.strftime("%Y-%m-%d_%H%M%S")
    console.print(
        Panel(
            syntax,
            title=f"[bold cyan]Benchmark Result: {result_id}_{result.tool}[/]",  # noqa: E501
            border_style="cyan",
        )
    )


def format_comparison_table(
    result1: BenchmarkResult,
    result2: BenchmarkResult,
    deltas: Dict[str, Dict[str, Any]],
) -> Table:
    """Format comparison results as a Rich table."""
    table = Table(title="Benchmark Comparison", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Result 1", style="white")
    table.add_column("Result 2", style="white")
    table.add_column("Delta", style="yellow")
    table.add_column("Change %", style="green")

    for metric, delta_info in deltas.items():
        value1 = delta_info.get("value1", "N/A")
        value2 = delta_info.get("value2", "N/A")
        delta = delta_info.get("delta", "N/A")
        percent = delta_info.get("percent_change", "N/A")

        # Format values
        if isinstance(value1, float):
            value1_str = f"{value1:.4f}"
        else:
            value1_str = str(value1)

        if isinstance(value2, float):
            value2_str = f"{value2:.4f}"
        else:
            value2_str = str(value2)

        if isinstance(delta, float):
            delta_str = f"{delta:+.4f}"
        else:
            delta_str = str(delta)

        if isinstance(percent, float):
            # Color code: green for improvement, red for regression
            if percent > 0:
                percent_str = f"[green]+{percent:.2f}%[/]"
            elif percent < 0:
                percent_str = f"[red]{percent:.2f}%[/]"
            else:
                percent_str = "0.00%"
        else:
            percent_str = str(percent)

        table.add_row(metric, value1_str, value2_str, delta_str, percent_str)

    return table


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green]✓[/] {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[red]✗[/] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[yellow]⚠[/] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[blue]ℹ[/] {message}")
