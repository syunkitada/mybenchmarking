# sysbench - CPU Benchmark

## Overview

sysbench is a scriptable multi-threaded benchmark tool that can test CPU, memory, file I/O, and database performance. For CPU benchmarking, it performs prime number calculations to stress-test processor capabilities.

## What It Measures

- **Events per second**: Number of prime calculations completed per second
- **Total events**: Total number of prime number calculations performed
- **Latency**: Minimum, average, maximum, and 95th percentile latency in milliseconds
- **Thread performance**: Multi-threaded CPU workload simulation

## Installation

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install sysbench
```

### RHEL/Fedora/CentOS

```bash
sudo dnf install sysbench
# or
sudo yum install sysbench
```

## Usage Examples

### Basic CPU Test (Single Thread)

```bash
sysbench cpu --cpu-max-prime=20000 run
```

### Multi-Threaded CPU Test

```bash
# Test with 8 threads for 60 seconds
sysbench cpu --cpu-max-prime=20000 --threads=8 --time=60 run
```

### Maximum Thread Test

```bash
# Use all available CPU threads
sysbench cpu --cpu-max-prime=20000 --threads=$(nproc) --time=60 run
```

### Different Prime Calculation Ranges

```bash
# Lighter workload
sysbench cpu --cpu-max-prime=10000 --threads=4 --time=30 run

# Heavier workload
sysbench cpu --cpu-max-prime=50000 --threads=8 --time=120 run
```

## Understanding Output

Example output:

```
CPU speed:
    events per second:  12543.67

General statistics:
    total time:                          60.0001s
    total number of events:              752620

Latency (ms):
         min:                                    0.63
         avg:                                    0.64
         max:                                    1.23
         95th percentile:                        0.68
```

### Key Metrics

- **events per second**: Higher is better. Indicates how many prime calculations completed per second
- **total events**: Total work completed during the test period
- **min/avg/max latency**: Lower is better. Time taken to complete individual calculations
- **95th percentile**: 95% of calculations completed within this time

### Typical Values

- **Desktop CPU (8 cores)**: 10,000-15,000 events/sec
- **Server CPU (16+ cores)**: 20,000-40,000 events/sec
- **High-end workstation**: 15,000-25,000 events/sec

## Common Parameters

- `--cpu-max-prime=N`: Calculate prime numbers up to N (default: 10000)
- `--threads=N`: Number of worker threads (default: 1)
- `--time=N`: Test duration in seconds (default: 10)
- `--events=N`: Stop after N events instead of time-based

## Use Cases

- Comparing CPU performance before/after system changes
- Testing CPU scaling across different thread counts
- Validating CPU frequency governor settings
- Benchmarking VMs vs physical hardware
- Testing thermal throttling under sustained load

## Interpretation Tips

1. **Single-thread performance**: Run with `--threads=1` to test per-core performance
2. **Scaling efficiency**: Compare results with 1, 2, 4, 8+ threads to see how well workloads scale
3. **Consistency**: Run multiple times and average results for stable measurements
4. **CPU governor**: Use `performance` governor for maximum and consistent results
5. **Background processes**: Close other applications for accurate measurements

## Related Documentation

- [Metrics: Events Per Second](../metrics/events_per_second.md)
- [Metrics: Latency](../metrics/latency.md)
