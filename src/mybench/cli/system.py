"""System profile CLI commands."""

import click
from datetime import date
from pathlib import Path
from pydantic import ValidationError

from ..models.system import (
    SystemProfile,
    HardwareSpecs,
    CPUSpec,
    VirtualCPUSpec,
    MemorySpec,
    DiskSpec,
    NetworkSpec,
    VirtualizationSpecs,
)
from ..storage.profiles import (
    save_system_profile,
    load_system_profile,
    list_system_profiles,
    profile_exists,
)
from ..utils.format import (
    format_system_profiles_table,
    format_system_profile_detail,
    print_success,
    print_error,
    console,
)
from ..utils.detect import (
    detect_cpu_info,
    detect_memory_info,
    is_virtual_machine,
)


@click.group(name="system")
def system():
    """Manage system profiles."""
    pass


@system.command(name="create")
@click.option(
    "--profile-id",
    prompt=True,
    help="Unique profile identifier (e.g., my-desktop)",  # noqa: E501
)
@click.option("--name", prompt=True, help="Human-readable profile name")
@click.option(
    "--type",
    type=click.Choice(["physical", "virtual"]),
    prompt=True,
    help="System type",
)
@click.pass_context
def create_profile(ctx, profile_id, name, type):
    """Create a new system profile interactively."""
    systems_dir = ctx.obj["SYSTEMS_PATH"]

    # Check if profile already exists
    if profile_exists(profile_id, systems_dir):
        print_error(f"Profile '{profile_id}' already exists")
        ctx.exit(1)

    console.print("\n[bold cyan]Creating system profile...[/]\n")

    # Collect hardware specs
    console.print("[yellow]CPU Specifications:[/]")
    if type == "physical":
        cpu_model = click.prompt("CPU model", type=str)
        cpu_cores = click.prompt("Number of cores", type=int)
        cpu_threads = click.prompt("Number of threads", type=int)
        base_clock = click.prompt(
            "Base clock (GHz)", type=float, default=None, show_default=False
        )
        max_clock = click.prompt(
            "Max clock (GHz)", type=float, default=None, show_default=False
        )
        cpu_spec = CPUSpec(
            model=cpu_model,
            cores=cpu_cores,
            threads=cpu_threads,
            base_clock_ghz=base_clock if base_clock else None,
            max_clock_ghz=max_clock if max_clock else None,
        )
    else:
        vcpus = click.prompt("Number of vCPUs", type=int)
        cpu_mode = click.prompt(
            "CPU mode (e.g., host-passthrough)", type=str, default=""
        )
        pinning = click.prompt("CPU pinning (e.g., 0-3)", type=str, default="")
        cpu_spec = VirtualCPUSpec(
            vcpus=vcpus,
            cpu_mode=cpu_mode if cpu_mode else None,
            pinning=pinning if pinning else None,
        )

    console.print("\n[yellow]Memory Specifications:[/]")
    mem_total = click.prompt("Total memory (GB)", type=int)
    mem_type = click.prompt("Memory type (e.g., DDR4)", type=str, default="")
    mem_speed = click.prompt("Memory speed (MHz)", type=int, default=0)
    hugepages = click.confirm("Hugepages enabled?", default=False)
    hugepage_size = None
    if hugepages:
        hugepage_size = click.prompt(
            "Hugepage size (e.g., 2MB)", type=str, default="2MB"
        )

    memory_spec = MemorySpec(
        total_gb=mem_total,
        type=mem_type if mem_type else None,
        speed_mhz=mem_speed if mem_speed else None,
        hugepages=hugepages if hugepages else None,
        hugepage_size=hugepage_size,
    )

    console.print("\n[yellow]Disk Specifications:[/]")
    disk_model = click.prompt("Disk model", type=str, default="")
    disk_type = click.prompt("Disk type (e.g., NVMe SSD, qcow2)", type=str)
    disk_capacity = click.prompt("Disk capacity (GB)", type=int)

    disk_spec = DiskSpec(
        model=disk_model if disk_model else None,
        type=disk_type,
        capacity_gb=disk_capacity,
    )

    if type == "virtual":
        backend = click.prompt("Disk backend (e.g., virtio-blk)", type=str, default="")
        cache_mode = click.prompt("Cache mode", type=str, default="")
        io_mode = click.prompt("I/O mode", type=str, default="")
        disk_spec.backend = backend if backend else None
        disk_spec.cache_mode = cache_mode if cache_mode else None
        disk_spec.io_mode = io_mode if io_mode else None

    console.print("\n[yellow]Network Specifications:[/]")
    net_interface = click.prompt("Network interface", type=str, default="")
    net_speed = click.prompt("Network speed (Gbps)", type=float, default=0.0)

    network_spec = NetworkSpec(
        interface=net_interface if net_interface else None,
        speed_gbps=net_speed if net_speed else None,
    )

    if type == "virtual":
        net_model = click.prompt(
            "Network model (e.g., virtio-net)", type=str, default=""
        )
        net_backend = click.prompt(
            "Network backend (e.g., vhost-net)", type=str, default=""
        )
        network_spec.model = net_model if net_model else None
        network_spec.backend = net_backend if net_backend else None

    hardware = HardwareSpecs(
        cpu=cpu_spec, memory=memory_spec, disk=disk_spec, network=network_spec
    )

    # Virtualization specs for VMs
    virtualization = None
    if type == "virtual":
        console.print("\n[yellow]Virtualization Specifications:[/]")
        hypervisor = click.prompt("Hypervisor (e.g., QEMU/KVM)", type=str)
        host_system = click.prompt("Host system profile ID", type=str, default="")
        cpu_type = click.prompt(
            "CPU type (e.g., host-passthrough)", type=str, default=""
        )
        cpu_topology = click.prompt("CPU topology", type=str, default="")
        virtualization = VirtualizationSpecs(
            hypervisor=hypervisor,
            host_system=host_system if host_system else None,
            cpu_type=cpu_type if cpu_type else None,
            cpu_topology=cpu_topology if cpu_topology else None,
        )

    notes = click.prompt("\nNotes (optional)", type=str, default="")

    # Create profile
    try:
        profile = SystemProfile(
            profile_id=profile_id,
            profile_name=name,
            type=type,
            created=date.today(),
            hardware=hardware,
            virtualization=virtualization,
            notes=notes if notes else None,
        )

        filepath = save_system_profile(profile, systems_dir)
        print_success(f"System profile created: {filepath.relative_to(Path.cwd())}")
    except ValidationError as e:
        print_error(f"Validation error: {e}")
        ctx.exit(1)
    except Exception as e:
        print_error(f"Failed to save profile: {e}")
        ctx.exit(1)


@system.command(name="detect")
@click.option("--profile-id", prompt=True, help="Unique profile identifier")
@click.option("--name", prompt=True, help="Human-readable profile name")
@click.pass_context
def detect_profile(ctx, profile_id, name):
    """Auto-detect current system and create profile."""
    systems_dir = ctx.obj["SYSTEMS_PATH"]

    # Check if profile already exists
    if profile_exists(profile_id, systems_dir):
        print_error(f"Profile '{profile_id}' already exists")
        ctx.exit(1)

    console.print("\n[bold cyan]Detecting system configuration...[/]\n")

    # Detect if virtual machine
    is_vm, hypervisor = is_virtual_machine()
    system_type = "virtual" if is_vm else "physical"

    console.print(f"[green]System type: {system_type}[/]")
    if is_vm and hypervisor:
        console.print(f"[green]Hypervisor: {hypervisor}[/]")

    # Detect CPU
    cpu_info = detect_cpu_info()
    if system_type == "physical":
        cpu_spec = CPUSpec(
            model=cpu_info.get("model", "Unknown"),
            cores=cpu_info.get("cores", 1),
            threads=cpu_info.get("threads", 1),
            base_clock_ghz=cpu_info.get("base_clock_ghz"),
            max_clock_ghz=cpu_info.get("max_clock_ghz"),
        )
    else:
        cpu_spec = VirtualCPUSpec(
            vcpus=cpu_info.get("cores", 1),
            cpu_mode=None,
            pinning=None,
        )

    # Detect memory
    mem_info = detect_memory_info()
    memory_spec = MemorySpec(
        total_gb=mem_info.get("total_gb", 1),
        type=mem_info.get("type"),
        speed_mhz=mem_info.get("speed_mhz"),
    )

    # Placeholder disk and network specs (detection is complex)
    disk_spec = DiskSpec(
        type="Unknown",
        capacity_gb=100,
    )
    network_spec = NetworkSpec()

    hardware = HardwareSpecs(
        cpu=cpu_spec,
        memory=memory_spec,
        disk=disk_spec,
        network=network_spec,
    )

    # Create virtualization specs if VM
    virtualization = None
    if is_vm and hypervisor:
        virtualization = VirtualizationSpecs(
            hypervisor=hypervisor,
        )

    notes = f"Auto-detected on {date.today()}"

    try:
        profile = SystemProfile(
            profile_id=profile_id,
            profile_name=name,
            type=system_type,
            created=date.today(),
            hardware=hardware,
            virtualization=virtualization,
            notes=notes,
        )

        filepath = save_system_profile(profile, systems_dir)
        print_success(f"System profile created: {filepath.relative_to(Path.cwd())}")
        console.print("\n[yellow]Note: Some values may need manual correction[/]")
    except Exception as e:
        print_error(f"Failed to save profile: {e}")
        ctx.exit(1)


@system.command(name="list")
@click.pass_context
def list_profiles(ctx):
    """List all system profiles."""
    systems_dir = ctx.obj["SYSTEMS_PATH"]

    try:
        profiles = list_system_profiles(systems_dir)
        if not profiles:
            console.print("[yellow]No system profiles found[/]")
            return

        table = format_system_profiles_table(profiles)
        console.print(table)
    except Exception as e:
        print_error(f"Failed to list profiles: {e}")
        ctx.exit(1)


@system.command(name="show")
@click.argument("profile_id")
@click.pass_context
def show_profile(ctx, profile_id):
    """Show detailed information about a system profile."""
    systems_dir = ctx.obj["SYSTEMS_PATH"]

    try:
        profile = load_system_profile(profile_id, systems_dir)
        format_system_profile_detail(profile)
    except FileNotFoundError:
        print_error(f"Profile '{profile_id}' not found")
        ctx.exit(1)
    except Exception as e:
        print_error(f"Failed to load profile: {e}")
        ctx.exit(1)
