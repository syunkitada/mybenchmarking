"""System detection utilities for auto-detecting hardware specs."""

import os
import platform
import re
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple


def detect_cpu_info() -> Dict[str, any]:
    """
    Detect CPU information from /proc/cpuinfo.

    Returns:
        Dict with CPU model, cores, threads
    """
    cpu_info = {}

    if Path("/proc/cpuinfo").exists():
        with open("/proc/cpuinfo", "r") as f:
            content = f.read()

        # Extract model name
        model_match = re.search(r"model name\s*:\s*(.+)", content)
        if model_match:
            cpu_info["model"] = model_match.group(1).strip()

        # Count physical cores and threads
        siblings = re.findall(r"siblings\s*:\s*(\d+)", content)
        cpu_cores = re.findall(r"cpu cores\s*:\s*(\d+)", content)

        if cpu_cores:
            cpu_info["cores"] = int(cpu_cores[0])
        if siblings:
            cpu_info["threads"] = int(siblings[0])
    else:
        # Fallback to platform module
        cpu_info["model"] = platform.processor() or "Unknown"
        cpu_info["cores"] = os.cpu_count() or 1
        cpu_info["threads"] = os.cpu_count() or 1

    return cpu_info


def detect_memory_info() -> Dict[str, any]:
    """
    Detect memory information from /proc/meminfo.

    Returns:
        Dict with total memory in GB
    """
    memory_info = {}

    if Path("/proc/meminfo").exists():
        with open("/proc/meminfo", "r") as f:
            content = f.read()

        # Extract total memory in kB
        mem_match = re.search(r"MemTotal:\s*(\d+)\s*kB", content)
        if mem_match:
            mem_kb = int(mem_match.group(1))
            memory_info["total_gb"] = round(mem_kb / (1024 * 1024))

    return memory_info


def detect_disk_info() -> Dict[str, any]:
    """
    Detect primary disk information.

    Returns:
        Dict with disk type and capacity
    """
    disk_info = {"type": "Unknown"}

    # Try to get root filesystem info
    try:
        result = subprocess.run(
            ["df", "-h", "/"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:
                fields = lines[1].split()
                if len(fields) >= 2:
                    size_str = fields[1]
                    # Parse size (e.g., "100G")
                    size_match = re.match(r"(\d+\.?\d*)([GMK])", size_str)
                    if size_match:
                        value = float(size_match.group(1))
                        unit = size_match.group(2)
                        if unit == "G":
                            disk_info["capacity_gb"] = int(value)
                        elif unit == "T":
                            disk_info["capacity_gb"] = int(value * 1024)
    except Exception:
        pass

    return disk_info


def detect_network_info() -> Dict[str, any]:
    """
    Detect network interface information.

    Returns:
        Dict with primary network interface
    """
    network_info = {}

    # Try to find primary network interface
    try:
        result = subprocess.run(
            ["ip", "route", "get", "1.1.1.1"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            # Parse: "1.1.1.1 via ... dev eth0 ..."
            match = re.search(r"dev\s+(\S+)", result.stdout)
            if match:
                network_info["interface"] = match.group(1)
    except Exception:
        pass

    return network_info


def detect_os_info() -> str:
    """
    Detect operating system information.

    Returns:
        OS name and version string
    """
    try:
        # Try to read /etc/os-release
        if Path("/etc/os-release").exists():
            with open("/etc/os-release", "r") as f:
                content = f.read()

            name_match = re.search(r'PRETTY_NAME="(.+)"', content)
            if name_match:
                return name_match.group(1)
    except Exception:
        pass

    # Fallback
    return f"{platform.system()} {platform.release()}"


def detect_kernel_info() -> Dict[str, str]:
    """
    Detect kernel information.

    Returns:
        Dict with kernel version and governor
    """
    kernel_info = {"version": platform.release()}

    # Try to detect CPU governor
    governor_path = Path("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    if governor_path.exists():
        try:
            with open(governor_path, "r") as f:
                kernel_info["cpu_governor"] = f.read().strip()
        except Exception:
            pass

    return kernel_info


def is_virtual_machine() -> Tuple[bool, Optional[str]]:
    """
    Detect if running in a virtual machine.

    Returns:
        Tuple of (is_vm, hypervisor_type)
    """
    # Check systemd-detect-virt
    try:
        result = subprocess.run(
            ["systemd-detect-virt"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            virt_type = result.stdout.strip()
            if virt_type != "none":
                return True, virt_type
    except Exception:
        pass

    # Check /proc/cpuinfo for hypervisor flag
    if Path("/proc/cpuinfo").exists():
        with open("/proc/cpuinfo", "r") as f:
            if "hypervisor" in f.read():
                return True, "unknown"

    return False, None
