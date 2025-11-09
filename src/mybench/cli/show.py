"""CLI command for showing benchmark result details."""

import click

from ..storage.results import get_result_by_id
from ..utils.format import (
    format_benchmark_result_detail,
    print_error,
)


@click.command(name="show")
@click.argument("result_id")
@click.pass_context
def show_cmd(ctx, result_id):
    """Show detailed information about a benchmark result.

    RESULT_ID should be in the format: YYYY-MM-DD_HHMMSS_tool
    (e.g., 2025-11-09_143022_sysbench)
    """
    results_dir = ctx.obj["RESULTS_PATH"]

    try:
        result = get_result_by_id(result_id, results_dir)
        if result is None:
            print_error(f"Result '{result_id}' not found")
            ctx.exit(1)

        format_benchmark_result_detail(result)
    except Exception as e:
        print_error(f"Failed to load result: {e}")
        ctx.exit(1)
