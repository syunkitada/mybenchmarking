# dd - Data Duplicator (Disk Benchmark)

## Overview

dd is a Unix utility for copying and converting files. While not a dedicated benchmark tool, it's commonly used for quick sequential I/O performance tests and is available on all Unix-like systems.

## What It Measures

- **Sequential write throughput**: MB/s or GB/s
- **Sequential read throughput**: MB/s or GB/s
- **Time taken**: Duration of the operation

## Installation

dd is pre-installed on all Linux distributions as part of coreutils.

## Usage Examples

### Sequential Write Test

```bash
# Write 1GB with 1MB blocks
dd if=/dev/zero of=testfile bs=1M count=1024 oflag=direct

# Clear cache first for accurate write test
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches
dd if=/dev/zero of=testfile bs=1M count=1024 oflag=direct
```

### Sequential Read Test

```bash
# Clear cache first
sync; echo 3 | sudo tee /proc/sys/vm/drop_caches

# Read the test file
dd if=testfile of=/dev/null bs=1M
```

### Large File Test

```bash
# Write 10GB
dd if=/dev/zero of=testfile bs=1M count=10240 oflag=direct

# Show progress during operation (Linux)
dd if=/dev/zero of=testfile bs=1M count=10240 oflag=direct status=progress
```

### Different Block Sizes

```bash
# 4KB blocks (typical for random I/O)
dd if=/dev/zero of=testfile bs=4K count=262144 oflag=direct

# 1MB blocks (typical for sequential I/O)
dd if=/dev/zero of=testfile bs=1M count=1024 oflag=direct

# 4MB blocks (large sequential I/O)
dd if=/dev/zero of=testfile bs=4M count=256 oflag=direct
```

### Bypassing Cache

```bash
# Direct I/O (bypass cache) - more accurate
dd if=/dev/zero of=testfile bs=1M count=1024 oflag=direct

# Synchronized I/O (ensure data is written to disk)
dd if=/dev/zero of=testfile bs=1M count=1024 conv=fdatasync
```

## Understanding Output

Example output:

```
1024+0 records in
1024+0 records out
1073741824 bytes (1.1 GB, 1.0 GiB) copied, 5.23456 s, 205 MB/s
```

### Key Metrics

- **bytes copied**: Total data transferred
- **time**: Duration of operation
- **MB/s or GB/s**: Throughput (higher is better)

### Typical Values

#### NVMe SSD

- **Sequential Write**: 2-5 GB/s
- **Sequential Read**: 3-7 GB/s

#### SATA SSD

- **Sequential Write**: 400-550 MB/s
- **Sequential Read**: 500-600 MB/s

#### HDD

- **Sequential Write**: 100-180 MB/s
- **Sequential Read**: 120-200 MB/s

## Common Parameters

- `if=FILE`: Input file (`/dev/zero` for writes, `testfile` for reads)
- `of=FILE`: Output file (`testfile` for writes, `/dev/null` for reads)
- `bs=SIZE`: Block size (4K, 1M, 4M, etc.)
- `count=N`: Number of blocks to copy
- `oflag=direct`: Use direct I/O (bypass cache)
- `conv=fdatasync`: Synchronize data before finishing
- `status=progress`: Show progress during operation (Linux)

## Use Cases

- Quick sequential I/O check
- Verifying storage system throughput
- Testing file system performance
- Creating test files
- Disk-to-disk transfer speed testing

## Interpretation Tips

1. **Cache effects**: Always clear cache or use `oflag=direct` for accurate results
2. **Block size impact**: Larger blocks typically give higher throughput
3. **File location**: Test on actual filesystem, not /tmp (may be in RAM)
4. **Multiple runs**: Run 3-5 times and average for consistent results
5. **File size**: Use files larger than system RAM to avoid cache skewing

## Clearing System Cache

```bash
# Flush file system buffers
sync

# Drop caches (requires root)
echo 3 | sudo tee /proc/sys/vm/drop_caches
```

## Complete Benchmark Script

```bash
#!/bin/bash
# Complete dd benchmark script

echo "Clearing cache..."
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

echo "Sequential Write Test (1GB)..."
dd if=/dev/zero of=testfile bs=1M count=1024 oflag=direct 2>&1 | grep copied

echo ""
echo "Clearing cache..."
sync
echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

echo "Sequential Read Test (1GB)..."
dd if=testfile of=/dev/null bs=1M 2>&1 | grep copied

echo ""
echo "Cleaning up..."
rm testfile

echo "Done!"
```

## Limitations

- **Only sequential I/O**: Cannot test random I/O patterns
- **No IOPS measurement**: Only measures throughput
- **No latency data**: Doesn't provide latency percentiles
- **Basic metrics**: For comprehensive testing, use fio instead

## When to Use dd vs fio

**Use dd when:**

- Quick sequential throughput check needed
- Tool must be pre-installed (no installation possible)
- Simple test sufficient

**Use fio when:**

- Need random I/O testing
- Need IOPS measurements
- Need latency percentiles
- Need comprehensive benchmark data

## Related Documentation

- [Metrics: Throughput](../metrics/throughput.md)
- [fio - Flexible I/O Tester](fio.md)
- [bonnie++ Disk Benchmark](bonnie++.md)
