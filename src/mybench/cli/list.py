"""CLI command for listing benchmark results."""

import click

from ..storage.results import list_benchmark_results
from ..utils.format import (
    format_benchmark_results_table,
    print_error,
    console,
)


@click.command(name="list")
@click.option(
    "--category",
    type=click.Choice(["cpu", "memory", "disk", "network"]),
    help="Filter by category",
)
@click.option(
    "--system", "system_profile_id", help="Filter by system profile ID"
)  # noqa: E501
@click.option("--label", help="Filter by label")
@click.pass_context
def list_cmd(ctx, category, system_profile_id, label):
    """List benchmark results with optional filters."""
    results_dir = ctx.obj["RESULTS_PATH"]

    try:
        results = list_benchmark_results(
            results_dir,
            category=category,
            system_profile_id=system_profile_id,
            label=label,
        )

        if not results:
            console.print("[yellow]No benchmark results found[/]")
            return

        table = format_benchmark_results_table(results)
        console.print(table)
        console.print(f"\n[dim]Total: {len(results)} results[/]")
    except Exception as e:
        print_error(f"Failed to list results: {e}")
        ctx.exit(1)
