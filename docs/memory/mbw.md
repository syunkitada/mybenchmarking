# mbw - Memory Bandwidth Benchmark

## Overview

mbw (Memory BandWidth benchmark) is a simple tool that measures memory copy bandwidth. It provides quick measurements of memory subsystem performance using different copy methods.

## What It Measures

- **Memory copy bandwidth**: MB/s for different memory copy methods
- **MEMCPY**: Standard C library memcpy performance
- **DUMB**: Simple assignment loop
- **MCBLOCK**: Block-based memory copy

## Installation

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install mbw
```

### From Source (if not in repos)

```bash
git clone https://github.com/raas/mbw.git
cd mbw
make
sudo make install
```

## Usage Examples

### Basic Memory Bandwidth Test

```bash
mbw 500
```

Tests with 500MB of data using all copy methods.

### Specific Number of Tests

```bash
# Run 10 tests
mbw -n 10 500
```

### Test Specific Array Size

```bash
# Test with different array sizes
mbw 100    # 100 MB
mbw 500    # 500 MB
mbw 1000   # 1000 MB (1 GB)
mbw 5000   # 5000 MB (5 GB)
```

### Quiet Mode (Results Only)

```bash
mbw -q 500
```

## Understanding Output

Example output:

```
Long uses 8 bytes. Allocating 2*524288000 elements = 8388608000 bytes of memory.
Using 262144000 bytes as blocks for memcpy block copy test.
0       Method: MEMCPY  Elapsed: 0.683  MiB/s: 11696.88 Copy: 7.999 GiB
1       Method: MEMCPY  Elapsed: 0.682  MiB/s: 11710.26 Copy: 7.999 GiB
2       Method: MEMCPY  Elapsed: 0.683  MiB/s: 11696.88 Copy: 7.999 GiB
AVG     Method: MEMCPY  Elapsed: 0.683  MiB/s: 11701.34 Copy: 7.999 GiB
0       Method: DUMB    Elapsed: 1.225  MiB/s: 6519.18  Copy: 7.999 GiB
1       Method: DUMB    Elapsed: 1.224  MiB/s: 6524.49  Copy: 7.999 GiB
2       Method: DUMB    Elapsed: 1.225  MiB/s: 6519.18  Copy: 7.999 GiB
AVG     Method: DUMB    Elapsed: 1.225  MiB/s: 6520.95  Copy: 7.999 GiB
0       Method: MCBLOCK Elapsed: 0.683  MiB/s: 11696.88 Copy: 7.999 GiB
1       Method: MCBLOCK Elapsed: 0.682  MiB/s: 11710.26 Copy: 7.999 GiB
2       Method: MCBLOCK Elapsed: 0.683  MiB/s: 11696.88 Copy: 7.999 GiB
AVG     Method: MCBLOCK Elapsed: 0.683  MiB/s: 11701.34 Copy: 7.999 GiB
```

### Key Metrics

- **MiB/s**: Memory bandwidth in MiB per second (higher is better)
- **AVG**: Average of multiple test runs
- **Method**: Different memory copy implementations

### Typical Values (DDR4)

- **MEMCPY**: 10,000-20,000 MiB/s (optimized C library function)
- **DUMB**: 5,000-8,000 MiB/s (simple loop, less optimized)
- **MCBLOCK**: 10,000-20,000 MiB/s (block-based, similar to memcpy)

## Common Parameters

- `SIZE`: Amount of memory to test in MB (required)
- `-n NUM`: Number of test iterations (default: 10)
- `-q`: Quiet mode, print results only
- `-t TYPE`: Test specific method (0=memcpy, 1=dumb, 2=mcblock)

## Use Cases

- Quick memory bandwidth check
- Comparing memory performance across systems
- Validating memory configuration
- Testing memory channel configuration
- Before/after memory upgrade comparison

## Interpretation Tips

1. **MEMCPY is fastest**: Should give highest bandwidth using optimized code
2. **DUMB is baseline**: Shows performance without optimizations
3. **Multiple runs**: Averages help account for system variance
4. **Test size matters**: Use larger sizes (>=500MB) to avoid cache effects
5. **Consistency**: Low variance between runs indicates stable system

## Memory Bandwidth Factors

- **Memory type and speed**: DDR3, DDR4, DDR5 with different frequencies
- **Number of memory channels**: More channels = higher bandwidth
- **CPU architecture**: Different memory controllers have different max bandwidth
- **System load**: Background processes can reduce available bandwidth

## Comparison Example

```bash
# Before memory upgrade
mbw -n 5 1000
# Note the AVG MiB/s values

# After memory upgrade
mbw -n 5 1000
# Compare the AVG MiB/s values
```

## Related Documentation

- [Metrics: Bandwidth](../metrics/bandwidth.md)
- [Metrics: Throughput](../metrics/throughput.md)
- [sysbench Memory](sysbench-memory.md)
