"""System configuration data models for mutable system state."""

from typing import Dict, Optional
from pydantic import BaseModel, Field


class KernelConfig(BaseModel):
    """Kernel configuration."""

    version: str = Field(description="Kernel version")
    parameters: Optional[Dict[str, str]] = Field(
        None, description="Kernel parameters affecting performance"
    )
    cpu_governor: Optional[str] = Field(None, description="CPU frequency governor")
    scaling_max_freq: Optional[str] = Field(
        None, description="Maximum CPU scaling frequency"
    )


class SoftwareVersions(BaseModel):
    """Software version information."""

    model_config = {"extra": "allow"}


class SystemConfiguration(BaseModel):
    """Mutable system configuration captured at benchmark time."""

    os: str = Field(description="Operating system name and version")
    kernel: KernelConfig = Field(description="Kernel configuration")
    software: Optional[SoftwareVersions] = Field(
        None, description="Relevant software versions"
    )
    environment: Optional[Dict[str, str]] = Field(
        None, description="Environment variables"
    )
