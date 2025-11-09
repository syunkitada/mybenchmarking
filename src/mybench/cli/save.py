"""CLI command for saving benchmark results."""

import click
import json
from datetime import datetime
from pathlib import Path
from pydantic import ValidationError

from ..models.result import BenchmarkResult
from ..models.config import (
    SystemConfiguration,
    KernelConfig,
    SoftwareVersions,
)
from ..storage.results import save_benchmark_result
from ..storage.profiles import profile_exists
from ..utils.format import print_success, print_error, console


@click.command(name="save")
@click.option(
    "--category",
    type=click.Choice(["cpu", "memory", "disk", "network"]),
    prompt=True,
    help="Benchmark category",
)
@click.option("--tool", prompt=True, help="Benchmark tool name")
@click.option("--system", "system_profile_id", prompt=True, help="System profile ID")
@click.option("--label", help="Optional label for this result")
@click.option(
    "--config-file",
    type=click.Path(exists=True),
    help="JSON file with configuration details",
)
@click.option(
    "--results-file",
    type=click.Path(exists=True),
    help="JSON file with benchmark results",
)
@click.pass_context
def save_cmd(ctx, category, tool, system_profile_id, label, config_file, results_file):
    """Save a benchmark result."""
    systems_dir = ctx.obj["SYSTEMS_PATH"]
    results_dir = ctx.obj["RESULTS_PATH"]

    # Verify system profile exists
    if not profile_exists(system_profile_id, systems_dir):
        print_error(f"System profile '{system_profile_id}' not found")
        console.print(
            "[yellow]Tip: Run 'mybench system list' to see available profiles[/]"  # noqa: E501
        )
        ctx.exit(1)

    console.print("\n[bold cyan]Saving benchmark result...[/]\n")

    # Get configuration
    if config_file:
        with open(config_file, "r") as f:
            config_data = json.load(f)
            config = SystemConfiguration(**config_data)
    else:
        console.print("[yellow]System Configuration:[/]")
        os_name = click.prompt("OS name and version", type=str)

        console.print("\n[yellow]Kernel Configuration:[/]")
        kernel_version = click.prompt("Kernel version", type=str)
        cpu_governor = click.prompt(
            "CPU governor", type=str, default="", show_default=False
        )

        # Collect kernel parameters
        console.print("\n[dim]Enter kernel parameters (key=value), empty to finish:[/]")
        kernel_params = {}
        while True:
            param = click.prompt("Parameter", type=str, default="")
            if not param:
                break
            if "=" in param:
                key, value = param.split("=", 1)
                kernel_params[key.strip()] = value.strip()

        kernel = KernelConfig(
            version=kernel_version,
            parameters=kernel_params if kernel_params else None,
            cpu_governor=cpu_governor if cpu_governor else None,
        )

        # Software versions
        console.print(
            "\n[dim]Enter software versions (name=version), empty to finish:[/]"  # noqa: E501
        )
        software_dict = {}
        while True:
            software = click.prompt("Software", type=str, default="")
            if not software:
                break
            if "=" in software:
                key, value = software.split("=", 1)
                software_dict[key.strip()] = value.strip()

        software = SoftwareVersions(**software_dict) if software_dict else None

        # Environment variables
        console.print(
            "\n[dim]Enter environment variables (key=value), empty to finish:[/]"  # noqa: E501
        )
        env_vars = {}
        while True:
            env_var = click.prompt(
                "Environment variable", type=str, default=""
            )  # noqa: E501
            if not env_var:
                break
            if "=" in env_var:
                key, value = env_var.split("=", 1)
                env_vars[key.strip()] = value.strip()

        config = SystemConfiguration(
            os=os_name,
            kernel=kernel,
            software=software,
            environment=env_vars if env_vars else None,
        )

    # Get benchmark parameters and results
    if results_file:
        with open(results_file, "r") as f:
            results_data = json.load(f)
            benchmark_parameters = results_data.get("parameters", {})
            results = results_data.get("results", {})
            raw_output = results_data.get("raw_output")
    else:
        console.print("\n[yellow]Benchmark Parameters:[/]")
        console.print("[dim]Enter parameters (key=value), empty to finish:[/]")
        benchmark_parameters = {}
        while True:
            param = click.prompt("Parameter", type=str, default="")
            if not param:
                break
            if "=" in param:
                key, value = param.split("=", 1)
                # Try to convert to number if possible
                try:
                    value = float(value) if "." in value else int(value)
                except ValueError:
                    pass
                benchmark_parameters[key.strip()] = value

        console.print("\n[yellow]Results:[/]")
        console.print("[dim]Enter results (metric=value), empty to finish:[/]")
        results = {}
        while True:
            result = click.prompt("Result", type=str, default="")
            if not result:
                break
            if "=" in result:
                key, value = result.split("=", 1)
                # Try to convert to number if possible
                try:
                    value = float(value) if "." in value else int(value)
                except ValueError:
                    pass
                results[key.strip()] = value

        raw_output = click.prompt(
            "\nRaw output (optional)",
            type=str,
            default="",
            show_default=False,  # noqa: E501
        )

    # Create benchmark result
    try:
        benchmark_result = BenchmarkResult(
            timestamp=datetime.now(),
            category=category,
            tool=tool,
            label=label,
            system_profile_id=system_profile_id,
            configuration=config,
            benchmark_parameters=benchmark_parameters,
            results=results,
            raw_output=raw_output if raw_output else None,
        )

        filepath = save_benchmark_result(benchmark_result, results_dir)
        print_success(f"Benchmark result saved: {filepath.relative_to(Path.cwd())}")
    except ValidationError as e:
        print_error(f"Validation error: {e}")
        ctx.exit(1)
    except Exception as e:
        print_error(f"Failed to save result: {e}")
        ctx.exit(1)
