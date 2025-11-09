# Research: Linux Server Benchmark Documentation Toolkit

**Date**: November 9, 2025  
**Phase**: 0 - Research & Technology Decisions

This document consolidates research findings for all technical unknowns identified in the implementation plan.

---

## 1. uv Best Practices

### Decision: Use uv as primary package manager

**Rationale**:

- **Speed**: 10-100x faster than pip for package installation and resolution
- **Reliability**: Uses Rust-based resolver (same as Cargo), more deterministic than pip
- **Modern**: Designed for Python 3.7+ with modern packaging standards
- **Lock file**: `uv.lock` provides reproducible builds (like poetry.lock)
- **Compatibility**: Works with standard `pyproject.toml`, no vendor lock-in

**Key Commands**:

```bash
uv init                    # Initialize project
uv add <package>           # Add dependency
uv sync                    # Install from lockfile
uv run <command>           # Run in project environment
uv pip compile             # Generate requirements.txt
```

**pyproject.toml Structure**:

```toml
[project]
name = "mybench"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1.7",
    "pydantic>=2.5.0",
    "rich>=13.7.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.4.3"]

[project.scripts]
mybench = "mybench.cli.main:cli"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Development Workflow**:

1. `uv sync` - Install dependencies from lock
2. `uv run mybench` - Run CLI in isolated env
3. `uv add --dev pytest` - Add dev dependency
4. `uv pip freeze > requirements.txt` - For deployment

**Alternatives Considered**:

- **pip**: Too slow, no lockfile, dependency resolution issues
- **poetry**: Heavy, slower than uv, additional tool to learn
- **pip-tools**: Better than pip but slower than uv, less ergonomic

---

## 2. System Detection Techniques

### Decision: Use /proc filesystem + platform module

**Rationale**:

- **Cross-distro**: /proc is standard across all Linux distributions
- **No dependencies**: Built into Linux kernel, always available
- **Lightweight**: No external libraries for basic detection
- **Python standard**: platform module in stdlib for OS info

**Detection Methods**:

**CPU Information**:

```python
# /proc/cpuinfo for detailed CPU info
with open('/proc/cpuinfo') as f:
    # Parse: model name, cpu cores, siblings

# platform.processor() for basic info
import platform
platform.processor()  # "x86_64"
```

**Memory Information**:

```python
# /proc/meminfo for RAM details
with open('/proc/meminfo') as f:
    # Parse: MemTotal, MemAvailable
```

**OS/Kernel**:

```python
import platform
platform.system()        # "Linux"
platform.release()       # "5.15.0-91-generic"
platform.version()       # Full kernel version string

# /etc/os-release for distro info
with open('/etc/os-release') as f:
    # Parse: NAME, VERSION_ID
```

**VM vs Physical Detection**:

```python
# Check for hypervisor in /proc/cpuinfo
with open('/proc/cpuinfo') as f:
    content = f.read()
    if 'hypervisor' in content:
        # Running in VM

# Check /sys/class/dmi/id/product_name
with open('/sys/class/dmi/id/product_name') as f:
    product = f.read().strip()
    # "QEMU", "VirtualBox", "VMware" indicate VM

# Check /proc/modules for kvm
with open('/proc/modules') as f:
    if 'kvm' in f.read():
        # KVM hypervisor present
```

**QEMU/KVM Metadata**:

```python
# For VMs, check:
# /sys/devices/virtual/dmi/id/chassis_asset_tag
# /proc/cmdline for boot parameters
# /sys/hypervisor/type (if available)
```

**Alternatives Considered**:

- **psutil library**: Adds dependency, overkill for simple detection
- **systemd tools**: Not available on all distros, requires subprocess calls
- **lshw/dmidecode**: Requires root, external command execution

**Implementation Strategy**:

- Create `utils/detect.py` with functions for each detection type
- Gracefully handle missing /proc files
- Return None for undetectable values (don't fail)
- Cache detection results in memory (run once per CLI invocation)

---

## 3. Pydantic v2 Patterns

### Decision: Use Pydantic v2 with model_dump(mode='json')

**Rationale**:

- **Type Safety**: Compile-time type checking with mypy/pyright
- **Validation**: Automatic validation on model creation
- **JSON Serialization**: Built-in `model_dump()` and `model_validate()`
- **Performance**: Pydantic v2 is 5-50x faster than v1 (Rust core)
- **Schema Generation**: Auto-generate JSON schemas for documentation

**Key Patterns**:

**Model Definition**:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional

class SystemProfile(BaseModel):
    profile_id: str = Field(..., description="Unique identifier")
    profile_name: str
    type: Literal["physical", "virtual"]
    created: datetime
    hardware: HardwareSpecs
    virtualization: Optional[VirtualizationSpecs] = None

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "profile_id": "my-desktop",
                "profile_name": "My Desktop PC",
                "type": "physical",
                ...
            }]
        }
    }
```

**JSON Serialization**:

```python
# To JSON dict
profile.model_dump(mode='json')

# To JSON string
import json
json.dumps(profile.model_dump(mode='json'), indent=2)

# From JSON
profile = SystemProfile.model_validate(json_data)

# From JSON file
with open('profile.json') as f:
    profile = SystemProfile.model_validate_json(f.read())
```

**Nested Models**:

```python
class HardwareSpecs(BaseModel):
    cpu: CPUSpecs
    memory: MemorySpecs
    disk: DiskSpecs
    network: NetworkSpecs

class SystemProfile(BaseModel):
    hardware: HardwareSpecs  # Automatic nesting
```

**Optional Fields with Defaults**:

```python
class BenchmarkResult(BaseModel):
    schema_version: str = "1.0"  # Default value
    label: Optional[str] = None   # Optional field
    raw_output: str | None = None  # Python 3.10+ syntax
```

**Custom Validators**:

```python
from pydantic import field_validator

class SystemProfile(BaseModel):
    profile_id: str

    @field_validator('profile_id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v.islower() or ' ' in v:
            raise ValueError('profile_id must be lowercase without spaces')
        return v
```

**Schema Versioning**:

```python
# Include schema_version in all models
class BenchmarkResult(BaseModel):
    schema_version: str = "1.0"

    @field_validator('schema_version')
    @classmethod
    def check_version(cls, v: str) -> str:
        if v != "1.0":
            raise ValueError(f"Unsupported schema version: {v}")
        return v
```

**Alternatives Considered**:

- **dataclasses**: No validation, manual JSON serialization
- **attrs**: Less mature JSON support, smaller community
- **marshmallow**: Older pattern, more boilerplate than Pydantic v2

---

## 4. Click CLI Patterns

### Decision: Use Click with command groups and Rich integration

**Rationale**:

- **Industry Standard**: Most popular Python CLI framework
- **Decorator-based**: Clean, readable command definitions
- **Command Groups**: Natural multi-level organization
- **Type Safety**: Automatic type conversion from string args
- **Rich Integration**: Works seamlessly with Rich for formatting

**Key Patterns**:

**Basic Command Group**:

```python
import click
from rich.console import Console

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Linux server benchmark documentation toolkit."""
    pass

@cli.command()
def list():
    """List all saved results."""
    console.print("[bold]Benchmark Results[/bold]")
```

**Subcommand Groups**:

```python
@cli.group()
def system():
    """Manage system profiles."""
    pass

@system.command('create')
@click.option('--name', prompt=True, help='Profile name')
@click.option('--type', type=click.Choice(['physical', 'virtual']))
def system_create(name: str, type: str):
    """Create a new system profile."""
    pass

# Usage: mybench system create --name "My PC" --type physical
```

**Interactive Prompts**:

```python
@cli.command()
def save():
    """Save a benchmark result interactively."""
    category = click.prompt(
        'Category',
        type=click.Choice(['cpu', 'memory', 'disk', 'network'])
    )
    tool = click.prompt('Tool name')

    # Or use rich.prompt for nicer interface
    from rich.prompt import Prompt
    label = Prompt.ask("Label (optional)", default="")
```

**File Arguments**:

```python
@cli.command()
@click.argument('file', type=click.File('r'))
def import_result(file):
    """Import result from JSON file."""
    data = json.load(file)
```

**Rich Integration**:

```python
from rich.table import Table
from rich.console import Console

console = Console()

@cli.command()
def list():
    """List results with table."""
    table = Table(title="Benchmark Results")
    table.add_column("Date", style="cyan")
    table.add_column("System", style="green")
    table.add_column("Tool", style="yellow")

    # Add rows...
    console.print(table)
```

**Error Handling**:

```python
@cli.command()
def show(result_id: str):
    """Show result details."""
    try:
        result = load_result(result_id)
    except FileNotFoundError:
        console.print(f"[red]Error:[/red] Result '{result_id}' not found")
        raise click.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise click.Exit(1)
```

**Alternatives Considered**:

- **argparse**: Too verbose, less feature-rich than Click
- **typer**: Built on Click, adds complexity, less mature
- **fire**: Too magical, harder to control behavior

---

## 5. JSON File Management

### Decision: Atomic writes with temp-and-move pattern

**Rationale**:

- **Data Integrity**: Never leave partial/corrupted files
- **Concurrent Access**: Safe for Git operations during write
- **Simplicity**: No file locking complexity needed
- **Cross-platform**: Works on all filesystems

**Implementation Pattern**:

**Atomic Write**:

```python
import json
import tempfile
import os
from pathlib import Path

def save_json(data: dict, filepath: Path) -> None:
    """Atomically save JSON to file."""
    # Create parent directories
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Write to temp file in same directory
    temp = tempfile.NamedTemporaryFile(
        mode='w',
        dir=filepath.parent,
        delete=False,
        suffix='.tmp'
    )

    try:
        # Write JSON with pretty printing
        json.dump(data, temp, indent=2, ensure_ascii=False)
        temp.flush()
        os.fsync(temp.fileno())  # Force write to disk
        temp.close()

        # Atomic rename (POSIX guarantees atomicity)
        os.replace(temp.name, filepath)
    except Exception:
        temp.close()
        os.unlink(temp.name)  # Clean up temp file
        raise
```

**File Naming Convention**:

```python
from datetime import datetime

def generate_result_filename(tool: str) -> str:
    """Generate sortable result filename."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return f"{timestamp}_{tool}.json"
    # Example: 2025-11-09_143022_sysbench.json
```

**Directory Traversal**:

```python
from pathlib import Path

def list_results(category: str | None = None) -> list[Path]:
    """List result files, optionally filtered by category."""
    results_dir = Path("results")

    if category:
        pattern = f"{category}/*.json"
    else:
        pattern = "*/*.json"

    # glob() is fast enough for 100s of files
    return sorted(results_dir.glob(pattern), reverse=True)
```

**JSON Schema Validation**:

```python
from pydantic import ValidationError

def load_result(filepath: Path) -> BenchmarkResult:
    """Load and validate result JSON."""
    with open(filepath) as f:
        data = json.load(f)

    try:
        return BenchmarkResult.model_validate(data)
    except ValidationError as e:
        # Pretty print validation errors
        console.print(f"[red]Invalid JSON schema in {filepath}[/red]")
        console.print(e)
        raise
```

**Handling Concurrent Access**:

- **Read operations**: No locking needed (files are immutable once written)
- **Write operations**: Atomic writes prevent corruption
- **Git operations**: Safe because we use atomic writes
- **No file locking**: Avoid complexity, not needed for this use case

**Alternatives Considered**:

- **File locking (fcntl)**: Overkill, adds complexity, Linux-only
- **Direct writes**: Risk of corruption if interrupted
- **SQLite**: Adds database dependency, against constitution
- **Append-only log**: Not suitable for structured result storage

---

## Technology Stack Summary

**Final Stack**:

- **Python 3.11+**: Modern language features (match, | for Union)
- **uv**: Package management and virtual environment
- **Click 8.1+**: CLI framework
- **Pydantic 2.5+**: Data validation and models
- **Rich 13.7+**: Terminal formatting
- **pytest 7.4+**: Testing framework (dev only)

**No dependencies for**:

- System detection: Use stdlib (platform, /proc parsing)
- JSON: Use stdlib (json module)
- File operations: Use stdlib (pathlib, tempfile)

**Philosophy**: Minimize dependencies, use stdlib where possible, add libraries only for significant value (CLI framework, validation, formatting).

---

## Conclusion

All technical unknowns have been researched and decisions made. Key takeaways:

1. **uv + pyproject.toml**: Modern, fast, standard-compliant
2. **/proc + platform**: Simple, no-dependency system detection
3. **Pydantic v2**: Type-safe models with easy JSON serialization
4. **Click + Rich**: Powerful CLI with beautiful output
5. **Atomic writes**: Safe concurrent file operations without locking

Ready to proceed to **Phase 1: Design & Contracts**.
