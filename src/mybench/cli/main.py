"""Main CLI entry point."""

import click
from pathlib import Path

from .system import system
from .save import save_cmd
from .list import list_cmd
from .show import show_cmd
from .compare import compare


# Get project version
__version__ = "0.1.0"


@click.group()
@click.version_option(version=__version__, prog_name="mybench")
@click.pass_context
def cli(ctx):
    """
    Linux Server Benchmark Documentation Toolkit.

    A tool for documenting benchmark tools and tracking benchmark results
    across physical machines and VMs.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Set up base paths
    ctx.obj["BASE_PATH"] = Path.cwd()
    ctx.obj["SYSTEMS_PATH"] = ctx.obj["BASE_PATH"] / "systems"
    ctx.obj["RESULTS_PATH"] = ctx.obj["BASE_PATH"] / "results"
    ctx.obj["DOCS_PATH"] = ctx.obj["BASE_PATH"] / "docs"


# Register subcommands
cli.add_command(system)
cli.add_command(save_cmd, name="save")
cli.add_command(list_cmd, name="list")
cli.add_command(show_cmd, name="show")
cli.add_command(compare)


if __name__ == "__main__":
    cli()
