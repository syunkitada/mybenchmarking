# Benchmark Results

This directory stores benchmark result files organized by category.

## Structure

Results are organized into subdirectories by benchmark category:

```
results/
├── cpu/
│   ├── 2025-11-09_143022_sysbench.json
│   └── 2025-11-09_150315_stress-ng.json
├── memory/
│   ├── 2025-11-09_144500_sysbench-memory.json
│   └── 2025-11-09_151000_mbw.json
├── disk/
│   ├── 2025-11-09_145030_fio.json
│   └── 2025-11-09_152000_dd.json
└── network/
    ├── 2025-11-09_150000_iperf3.json
    └── 2025-11-09_153000_netperf.json
```

## File Naming Convention

Files are named with timestamp and tool name for easy sorting:

```
YYYY-MM-DD_HHMMSS_<tool-name>.json
```

## Result File Format

Each result file references a system profile and contains:

- Benchmark metadata (timestamp, category, tool)
- System profile reference
- Current system configuration (kernel, software versions)
- Benchmark parameters
- Raw results and metrics

Example:

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
      "parameters": {
        "intel_pstate": "active",
        "transparent_hugepage": "always"
      },
      "cpu_governor": "performance"
    },
    "software": {
      "sysbench_version": "1.0.20"
    }
  },
  "benchmark_parameters": {
    "threads": 8,
    "time": 60
  },
  "results": {
    "events_per_second": 12543.67
  }
}
```

## Usage

Save a new benchmark result:

```bash
mybench save
```

List all results:

```bash
mybench list
```

Filter by system or category:

```bash
mybench list --system my-desktop --category cpu
```

View a specific result:

```bash
mybench show <result-id>
```

Compare two results:

```bash
mybench compare <result-id-1> <result-id-2>
```
