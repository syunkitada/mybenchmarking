"""CLI command for listing benchmark results."""

import click
import json
import csv
import sys

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
@click.option(
    "--export",
    type=click.Choice(["json", "csv"]),
    help="Export results to JSON or CSV format",
)
@click.pass_context
def list_cmd(ctx, category, system_profile_id, label, export):
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

        # Export to requested format
        if export == "json":
            _export_json(results)
        elif export == "csv":
            _export_csv(results)
        else:
            # Default table view
            table = format_benchmark_results_table(results)
            console.print(table)
            console.print(f"\n[dim]Total: {len(results)} results[/]")
    except Exception as e:
        print_error(f"Failed to list results: {e}")
        ctx.exit(1)


def _export_json(results):
    """Export results to JSON format."""
    output = []
    for result in results:
        output.append(result.model_dump(mode="json"))

    json.dump(output, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")


def _export_csv(results):
    """Export results to CSV format."""
    if not results:
        return

    # Extract fields from first result
    fieldnames = [
        "timestamp",
        "category",
        "tool",
        "system_profile_id",
        "label",
    ]

    # Add result metrics as separate columns
    if results[0].results:
        for key in results[0].results.keys():
            fieldnames.append(f"result_{key}")

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    for result in results:
        row = {
            "timestamp": result.timestamp.isoformat(),
            "category": result.category,
            "tool": result.tool,
            "system_profile_id": result.system_profile_id,
            "label": result.label or "",
        }

        # Add result metrics
        for key, value in result.results.items():
            row[f"result_{key}"] = value

        writer.writerow(row)
