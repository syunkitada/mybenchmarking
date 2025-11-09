"""System profile data models."""

from typing import Literal, Optional
from datetime import date
from pydantic import BaseModel, Field


class CPUSpec(BaseModel):
    """CPU specifications."""

    model: str = Field(description="CPU model name")
    cores: int = Field(description="Number of physical cores", gt=0)
    threads: int = Field(description="Number of threads", gt=0)
    base_clock_ghz: Optional[float] = Field(None, description="Base clock speed in GHz")
    max_clock_ghz: Optional[float] = Field(
        None, description="Max turbo clock speed in GHz"
    )


class VirtualCPUSpec(BaseModel):
    """Virtual CPU specifications for VMs."""

    vcpus: int = Field(description="Number of virtual CPUs", gt=0)
    cpu_mode: Optional[str] = Field(
        None, description="CPU mode (e.g., host-passthrough)"
    )
    pinning: Optional[str] = Field(None, description="CPU pinning configuration")


class MemorySpec(BaseModel):
    """Memory specifications."""

    total_gb: int = Field(description="Total memory in GB", gt=0)
    type: Optional[str] = Field(None, description="Memory type (e.g., DDR4)")
    speed_mhz: Optional[int] = Field(None, description="Memory speed in MHz")
    hugepages: Optional[bool] = Field(None, description="Hugepages enabled")
    hugepage_size: Optional[str] = Field(None, description="Hugepage size (e.g., 2MB)")


class DiskSpec(BaseModel):
    """Disk specifications."""

    model: Optional[str] = Field(None, description="Disk model name")
    type: str = Field(description="Disk type (e.g., NVMe SSD, qcow2)")
    capacity_gb: int = Field(description="Disk capacity in GB", gt=0)
    backend: Optional[str] = Field(
        None, description="Disk backend for VMs (e.g., virtio-blk)"
    )
    cache_mode: Optional[str] = Field(None, description="Cache mode for VMs")
    io_mode: Optional[str] = Field(None, description="I/O mode for VMs")


class NetworkSpec(BaseModel):
    """Network specifications."""

    interface: Optional[str] = Field(None, description="Network interface name")
    model: Optional[str] = Field(None, description="Network model")
    speed_gbps: Optional[float] = Field(None, description="Network speed in Gbps")
    backend: Optional[str] = Field(None, description="Network backend for VMs")


class HardwareSpecs(BaseModel):
    """Complete hardware specifications."""

    cpu: CPUSpec | VirtualCPUSpec = Field(description="CPU specifications")
    memory: MemorySpec = Field(description="Memory specifications")
    disk: DiskSpec = Field(description="Disk specifications")
    network: NetworkSpec = Field(description="Network specifications")


class VirtualizationSpecs(BaseModel):
    """Virtualization-specific specifications."""

    hypervisor: str = Field(description="Hypervisor type (e.g., QEMU/KVM)")
    host_system: Optional[str] = Field(
        None, description="Reference to host system profile ID"
    )
    cpu_type: Optional[str] = Field(None, description="CPU virtualization type")
    cpu_topology: Optional[str] = Field(None, description="CPU topology configuration")


class SystemProfile(BaseModel):
    """System profile containing immutable hardware specifications."""

    profile_id: str = Field(description="Unique profile identifier")
    profile_name: str = Field(description="Human-readable profile name")
    type: Literal["physical", "virtual"] = Field(description="System type")
    created: date = Field(description="Profile creation date")
    hardware: HardwareSpecs = Field(description="Hardware specifications")
    virtualization: Optional[VirtualizationSpecs] = Field(
        None, description="Virtualization specs for VMs"
    )
    notes: Optional[str] = Field(None, description="Additional notes")
