# My Benchmarking Toolkit

A comprehensive Linux server benchmark documentation and result tracking toolkit. This project provides:

- **Documentation** for CPU, memory, disk, and network benchmark tools
- **Result Storage** as Git-friendly JSON files with system profile management
- **Analysis Tools** for comparing results and tracking performance trends
- **CLI Interface** for easy benchmark result management

## Features

### 📚 Comprehensive Documentation

Browse documentation for 10+ benchmark tools across 4 categories:

- **CPU**: sysbench, stress-ng
- **Memory**: sysbench-memory, mbw
- **Disk**: fio, dd, bonnie++
- **Network**: iperf3, netperf
- **Metrics**: IOPS, throughput, latency, bandwidth

### 💾 Personal Benchmark Storage

- Save benchmark results as human-readable JSON files
- Store system profiles separately (physical machines and VMs)
- Track configuration changes (kernel parameters, software versions)
- Git-friendly format for version control

### 📊 Analysis & Comparison

- Compare two benchmark results with percentage changes
- Track performance trends over time
- Detect configuration differences between runs
- Filter and query results by system, category, or label

## Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd mybenchmarking

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Or use uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Basic Workflow

#### 1. Create a System Profile

```bash
# Interactive creation
mybench system create

# Auto-detect current system
mybench system detect

# List profiles
mybench system list

# Show profile details
mybench system show my-desktop
```

#### 2. Save Benchmark Results

```bash
# Interactive save
mybench save

# Example with options
mybench save --category cpu --tool sysbench --system my-desktop --label baseline
```

#### 3. List and View Results

```bash
# List all results
mybench list

# Filter by system
mybench list --system my-desktop

# Filter by category
mybench list --category cpu

# Show result details
mybench show 2025-11-09_143022_sysbench
```

#### 4. Compare and Analyze

```bash
# Compare two results
mybench compare diff 2025-11-09_143022_sysbench 2025-11-10_150000_sysbench

# Show configuration changes
mybench compare diff <result1> <result2> --show-config

# Show performance trends
mybench compare trend --system my-desktop --category cpu

# Show specific metric trend
mybench compare trend --system my-desktop --metric events_per_second
```

## Example Workflow

### Scenario: Benchmarking CPU Performance Changes

```bash
# 1. Create system profile (once)
mybench system detect --profile-id my-server --name "Production Server"

# 2. Run baseline benchmark
sysbench cpu --threads=8 --time=60 run > baseline_output.txt

# 3. Save baseline result
mybench save \
  --category cpu \
  --tool sysbench \
  --system my-server \
  --label baseline

# 4. Make system changes (e.g., kernel tuning)
# ... update kernel parameters ...

# 5. Run new benchmark
sysbench cpu --threads=8 --time=60 run > optimized_output.txt

# 6. Save new result
mybench save \
  --category cpu \
  --tool sysbench \
  --system my-server \
  --label optimized

# 7. Compare results
mybench compare diff \
  2025-11-09_100000_sysbench \
  2025-11-09_120000_sysbench \
  --show-config

# 8. View trends
mybench compare trend --system my-server --category cpu
```

## Directory Structure

```
mybenchmarking/
├── docs/                    # Benchmark tool documentation
│   ├── cpu/                # CPU benchmark tools
│   ├── memory/             # Memory benchmark tools
│   ├── disk/               # Disk I/O benchmark tools
│   ├── network/            # Network benchmark tools
│   └── metrics/            # Metric definitions
├── systems/                # System profile storage
│   └── *.json             # System profile files
├── results/                # Benchmark results storage
│   ├── cpu/               # CPU benchmark results
│   ├── memory/            # Memory benchmark results
│   ├── disk/              # Disk benchmark results
│   └── network/           # Network benchmark results
├── src/mybench/           # Source code
└── tests/                 # Test suite
```

## System Profile Example

Physical machine profile:

```json
{
  "profile_id": "my-desktop",
  "profile_name": "My Desktop PC",
  "type": "physical",
  "created": "2025-11-09",
  "hardware": {
    "cpu": {
      "model": "Intel Core i7-9700K",
      "cores": 8,
      "threads": 8
    },
    "memory": {
      "total_gb": 32,
      "type": "DDR4"
    }
  }
}
```

Virtual machine profile:

```json
{
  "profile_id": "vm-test01",
  "profile_name": "Test VM",
  "type": "virtual",
  "virtualization": {
    "hypervisor": "QEMU/KVM",
    "host_system": "my-desktop"
  },
  "hardware": {
    "cpu": {
      "vcpus": 4,
      "cpu_mode": "host-passthrough"
    }
  }
}
```

## Benchmark Result Example

```json
{
  "schema_version": "1.0",
  "timestamp": "2025-11-09T14:30:22Z",
  "category": "cpu",
  "tool": "sysbench",
  "label": "baseline",
  "system_profile_id": "my-desktop",
  "configuration": {
    "os": "Ubuntu 22.04.3 LTS",
    "kernel": {
      "version": "5.15.0-91-generic",
      "cpu_governor": "performance"
    }
  },
  "benchmark_parameters": {
    "threads": 8,
    "time": 60
  },
  "results": {
    "events_per_second": 12543.67,
    "total_time": 60.0001
  }
}
```

## CLI Commands Reference

### System Profile Management

- `mybench system create` - Create a system profile interactively
- `mybench system detect` - Auto-detect and create system profile
- `mybench system list` - List all system profiles
- `mybench system show <profile-id>` - Show profile details

### Benchmark Results

- `mybench save` - Save a benchmark result
- `mybench list [--system ID] [--category TYPE] [--label TAG]` - List results with filters
- `mybench show <result-id>` - Show result details

### Analysis

- `mybench compare diff <id1> <id2> [--show-config]` - Compare two results
- `mybench compare trend --system <id> [--category TYPE] [--metric NAME]` - Show trends

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mybench --cov-report=html

# Run specific test file
pytest tests/test_storage.py -v
```

### Development Process

This project is managed by [speckit](https://github.com/github/spec-kit). See `.specify/` directory for specifications and planning documents.

## Contributing

See `CONTRIBUTING.md` for guidelines on adding new benchmark tool documentation or features.

## License

[Add your license here]
