# stress-ng - System Stress Testing

## Overview

stress-ng is a comprehensive stress testing tool that can stress-test CPU, memory, I/O, and other system components. It provides a wide variety of stress methods and is excellent for stability testing and thermal validation.

## What It Measures

- **Operations per second (bogo ops)**: Number of stress operations completed
- **Real time**: Actual wall-clock time taken
- **User/System time**: CPU time spent in user vs kernel mode
- **CPU utilization**: Percentage of CPU used during test

## Installation

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install stress-ng
```

### RHEL/Fedora/CentOS

```bash
sudo dnf install stress-ng
# or
sudo yum install epel-release
sudo yum install stress-ng
```

## Usage Examples

### Basic CPU Stress

```bash
# Stress all CPU cores for 60 seconds
stress-ng --cpu 0 --timeout 60s
```

### Specific Number of Workers

```bash
# Stress with 4 CPU workers
stress-ng --cpu 4 --timeout 60s --metrics-brief
```

### CPU with Performance Metrics

```bash
# Detailed CPU stress with metrics
stress-ng --cpu $(nproc) --cpu-method all --timeout 60s --metrics
```

### Specific CPU Stress Methods

```bash
# Integer math operations
stress-ng --cpu 4 --cpu-method int64 --timeout 30s --metrics-brief

# Floating point operations
stress-ng --cpu 4 --cpu-method double --timeout 30s --metrics-brief

# Matrix operations
stress-ng --cpu 4 --cpu-method matrix --timeout 30s --metrics-brief
```

### Combined Stress Test

```bash
# CPU + Memory stress
stress-ng --cpu 4 --vm 2 --vm-bytes 1G --timeout 60s --metrics-brief
```

## Understanding Output

Example output:

```
stress-ng: info:  [12345] dispatching hogs: 8 cpu
stress-ng: info:  [12345] successful run completed in 60.01s
stress-ng: info:  [12345] stressor       bogo ops real time  usr time  sys time   bogo ops/s
stress-ng: info:  [12345]                           (secs)    (secs)    (secs)   (real time)
stress-ng: info:  [12345] cpu             1234567     60.01    479.20      0.45     20571.91
```

### Key Metrics

- **bogo ops**: "Bogus operations" - abstract work units completed
- **bogo ops/s (real time)**: Operations per second (higher is better)
- **usr time**: Time spent executing user-space code
- **sys time**: Time spent in kernel (should be low for CPU tests)

### Typical Values

- **Desktop CPU (8 cores)**: 150,000-250,000 bogo ops/s
- **Server CPU (16+ cores)**: 300,000-500,000 bogo ops/s
- **Per-core performance**: 18,000-30,000 bogo ops/s

## Common Parameters

- `--cpu N`: Number of CPU workers (0 = all cores)
- `--cpu-method METHOD`: Specific stress method (int32, int64, double, etc.)
- `--timeout TIME`: Test duration (e.g., 60s, 2m, 1h)
- `--metrics`: Show detailed metrics
- `--metrics-brief`: Show brief metrics summary
- `--verify`: Verify results for correctness testing

## Available CPU Methods

- `int8`, `int16`, `int32`, `int64`: Integer operations
- `float`, `double`, `longdouble`: Floating point operations
- `matrix`: Matrix operations
- `fft`: Fast Fourier Transform
- `gcd`: Greatest common divisor
- `pi`: Pi calculation
- `prime`: Prime number calculation
- `all`: Cycle through all methods

## Use Cases

- **Stability testing**: Verify system stability under load
- **Thermal validation**: Test cooling system effectiveness
- **CPU stress comparison**: Compare different CPUs or configurations
- **Power consumption testing**: Measure power draw under full load
- **Multi-component stress**: Test CPU, memory, and I/O simultaneously

## Interpretation Tips

1. **Thermal throttling**: Watch for bogo ops/s dropping over time indicating thermal issues
2. **Comparison baseline**: Use same method and duration for consistent comparisons
3. **System stability**: Run for extended periods (30min+) for stability validation
4. **Method selection**: Use `--cpu-method all` for comprehensive testing
5. **Resource monitoring**: Monitor temperatures and frequencies during stress tests

## Common Stress Scenarios

### Maximum CPU Load

```bash
stress-ng --cpu 0 --cpu-load 100 --timeout 5m --metrics
```

### Partial CPU Load (50%)

```bash
stress-ng --cpu 0 --cpu-load 50 --timeout 5m --metrics
```

### Long-Duration Stability Test

```bash
stress-ng --cpu 0 --timeout 30m --metrics --verify
```

## Related Documentation

- [Metrics: Operations Per Second](../metrics/throughput.md)
- [sysbench CPU](sysbench.md)
