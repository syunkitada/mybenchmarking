"""CLI commands for comparing benchmark results."""

import click
from rich.table import Table

from ..storage.results import get_result_by_id, list_benchmark_results
from ..analysis.compare import (
    compare_results,
    detect_config_changes,
    generate_trend_data,
)
from ..utils.format import (
    format_comparison_table,
    print_error,
    print_warning,
    console,
)


@click.group(name="compare")
def compare():
    """Compare benchmark results."""
    pass


@compare.command(name="diff")
@click.argument("result_id1")
@click.argument("result_id2")
@click.option(
    "--show-config",
    is_flag=True,
    help="Show configuration changes",
)
@click.pass_context
def compare_diff(ctx, result_id1, result_id2, show_config):
    """Compare two benchmark results.

    RESULT_ID1 and RESULT_ID2 should be in the format: YYYY-MM-DD_HHMMSS_tool
    """
    results_dir = ctx.obj["RESULTS_PATH"]

    try:
        # Load both results
        result1 = get_result_by_id(result_id1, results_dir)
        result2 = get_result_by_id(result_id2, results_dir)

        if result1 is None:
            print_error(f"Result '{result_id1}' not found")
            ctx.exit(1)

        if result2 is None:
            print_error(f"Result '{result_id2}' not found")
            ctx.exit(1)

        # Compare results
        deltas = compare_results(result1, result2)

        # Display comparison
        table = format_comparison_table(result1, result2, deltas)
        console.print(table)

        # Show configuration changes if requested
        if show_config:
            console.print("\n[bold cyan]Configuration Changes:[/]\n")
            changes = detect_config_changes(
                result1.configuration, result2.configuration
            )

            # Display changes
            has_changes = False
            if changes["os"]:
                console.print(
                    f"[yellow]OS:[/] {changes['os']['old']} → {changes['os']['new']}"  # noqa: E501
                )
                has_changes = True

            if changes["kernel"]:
                console.print("\n[yellow]Kernel:[/]")
                for key, change in changes["kernel"].items():
                    console.print(
                        f"  {key}: {change['old']} → {change['new']}"
                    )  # noqa: E501
                has_changes = True

            if changes["software"]:
                console.print("\n[yellow]Software:[/]")
                for key, change in changes["software"].items():
                    console.print(
                        f"  {key}: {change['old']} → {change['new']}"
                    )  # noqa: E501
                has_changes = True

            if changes["environment"]:
                console.print("\n[yellow]Environment:[/]")
                for key, change in changes["environment"].items():
                    console.print(
                        f"  {key}: {change['old']} → {change['new']}"
                    )  # noqa: E501
                has_changes = True

            if not has_changes:
                console.print("[dim]No configuration changes detected[/]")

    except ValueError as e:
        print_error(str(e))
        ctx.exit(1)
    except Exception as e:
        print_error(f"Failed to compare results: {e}")
        ctx.exit(1)


@compare.command(name="trend")
@click.option("--system", "system_profile_id", required=True, help="System profile ID")
@click.option(
    "--category",
    type=click.Choice(["cpu", "memory", "disk", "network"]),
    help="Filter by category",
)
@click.option("--tool", help="Filter by tool name")
@click.option("--metric", help="Show trend for specific metric")
@click.pass_context
def compare_trend(ctx, system_profile_id, category, tool, metric):
    """Show performance trends over time for a system."""
    results_dir = ctx.obj["RESULTS_PATH"]

    try:
        # Load all results for the system
        results = list_benchmark_results(
            results_dir,
            category=category,
            system_profile_id=system_profile_id,
        )

        if not results:
            print_warning(
                f"No results found for system '{system_profile_id}'"
            )  # noqa: E501
            ctx.exit(0)

        # Filter by tool if specified
        if tool:
            results = [r for r in results if r.tool == tool]
            if not results:
                print_warning(f"No results found for tool '{tool}'")
                ctx.exit(0)

        # Sort by timestamp
        results.sort(key=lambda r: r.timestamp)

        # Generate trend data
        trends = generate_trend_data(results)

        if not trends:
            print_warning("No trend data available")
            ctx.exit(0)

        # Display trends
        if metric:
            # Show specific metric
            if metric not in trends:
                print_error(f"Metric '{metric}' not found in results")
                console.print(f"[dim]Available metrics: {', '.join(trends.keys())}[/]")
                ctx.exit(1)

            table = Table(title=f"Trend: {metric}")
            table.add_column("Timestamp", style="cyan")
            table.add_column("Value", style="green")
            table.add_column("Label", style="yellow")

            for data_point in trends[metric]:
                value = data_point["value"]
                value_str = (
                    f"{value:.4f}" if isinstance(value, float) else str(value)
                )  # noqa: E501
                table.add_row(
                    data_point["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    value_str,
                    data_point.get("label") or "-",
                )

            console.print(table)
        else:
            # Show all metrics summary
            console.print(f"[bold cyan]Trend Summary for {system_profile_id}[/]\n")
            console.print(f"Total results: {len(results)}")
            console.print(
                f"Date range: {results[0].timestamp.date()} to {results[-1].timestamp.date()}"
            )  # noqa: E501
            console.print(f"\nAvailable metrics ({len(trends)}):")
            for metric_name in sorted(trends.keys()):
                data_points = len(trends[metric_name])
                console.print(
                    f"  • {metric_name} ({data_points} data points)"
                )  # noqa: E501

            console.print(
                "\n[dim]Tip: Use --metric <name> to see detailed trend for a specific metric[/]"  # noqa: E501
            )

    except Exception as e:
        print_error(f"Failed to generate trends: {e}")
        ctx.exit(1)
