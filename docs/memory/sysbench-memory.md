# sysbench - Memory Benchmark

## Overview

sysbench memory test measures memory bandwidth and latency through sequential and random read/write operations. It's useful for testing memory subsystem performance and identifying memory-related bottlenecks.

## What It Measures

- **Memory transfer rate**: MB/s for read/write operations
- **Total operations**: Number of memory operations completed
- **Total transferred**: Total amount of data transferred
- **Latency**: Minimum, average, and maximum operation latency

## Installation

See [sysbench CPU documentation](sysbench.md#installation) for installation instructions.

## Usage Examples

### Basic Memory Test

```bash
sysbench memory run
```

### Sequential Write Test

```bash
sysbench memory --memory-oper=write --memory-access-mode=seq run
```

### Random Read Test

```bash
sysbench memory --memory-oper=read --memory-access-mode=rnd run
```

### Large Block Size Test

```bash
# Test with 1MB blocks
sysbench memory --memory-block-size=1M --memory-total-size=10G run
```

### Multi-Threaded Memory Test

```bash
# Test with 4 threads
sysbench memory --threads=4 --memory-total-size=10G run
```

### Comprehensive Memory Benchmark

```bash
# Sequential read
sysbench memory --memory-oper=read --memory-access-mode=seq \
  --memory-total-size=10G --threads=1 run

# Sequential write
sysbench memory --memory-oper=write --memory-access-mode=seq \
  --memory-total-size=10G --threads=1 run

# Random read
sysbench memory --memory-oper=read --memory-access-mode=rnd \
  --memory-total-size=10G --threads=1 run

# Random write
sysbench memory --memory-oper=write --memory-access-mode=rnd \
  --memory-total-size=10G --threads=1 run
```

## Understanding Output

Example output:

```
Total operations: 10485760 (1234567.89 per second)

10240.00 MiB transferred (1205.63 MiB/sec)

General statistics:
    total time:                          8.4912s
    total number of events:              10485760

Latency (ms):
         min:                                    0.00
         avg:                                    0.00
         max:                                    0.25
         95th percentile:                        0.00
```

### Key Metrics

- **MiB/sec**: Memory bandwidth (higher is better)
- **Operations per second**: Number of memory operations completed
- **Latency**: Time to complete memory operations (lower is better)

### Typical Values (DDR4-3200)

- **Sequential Read**: 25,000-35,000 MiB/s
- **Sequential Write**: 20,000-30,000 MiB/s
- **Random Read**: 15,000-25,000 MiB/s
- **Random Write**: 10,000-20,000 MiB/s

## Common Parameters

- `--memory-oper=read|write`: Operation type
- `--memory-access-mode=seq|rnd`: Sequential or random access
- `--memory-block-size=SIZE`: Block size (default: 1K)
- `--memory-total-size=SIZE`: Total amount of data to transfer (default: 100G)
- `--threads=N`: Number of parallel threads

## Use Cases

- Comparing memory performance across systems
- Testing memory bandwidth with different access patterns
- Evaluating memory scaling with multiple threads
- Identifying memory bottlenecks
- Validating NUMA configuration impact

## Interpretation Tips

1. **Sequential vs Random**: Sequential should be faster than random
2. **Read vs Write**: Reads typically faster than writes
3. **Thread scaling**: Memory bandwidth should increase with more threads up to a point
4. **Block size impact**: Larger blocks generally achieve higher bandwidth
5. **Cache effects**: Small data sizes may fit in CPU cache, skewing results

## Memory Performance Factors

- **Memory type**: DDR3, DDR4, DDR5
- **Memory speed**: 2400MHz, 3200MHz, 4800MHz, etc.
- **Memory channels**: Dual-channel vs quad-channel
- **NUMA topology**: Local vs remote memory access
- **CPU memory controller**: Different CPUs have different memory bandwidth

## Related Documentation

- [Metrics: Throughput](../metrics/throughput.md)
- [Metrics: Bandwidth](../metrics/bandwidth.md)
- [Metrics: Latency](../metrics/latency.md)
- [mbw - Memory Bandwidth Benchmark](mbw.md)
