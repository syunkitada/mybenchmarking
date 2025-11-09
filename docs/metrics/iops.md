# IOPS - Input/Output Operations Per Second

## Definition

IOPS (Input/Output Operations Per Second) measures the number of read or write operations a storage device can perform per second. It's the primary metric for random I/O performance.

## What It Measures

IOPS quantifies storage device responsiveness and is crucial for:

- Database performance
- Virtual machine host performance
- Applications with many small file operations
- Random access workloads

## Formula

```
IOPS = Number of I/O Operations / Time (seconds)
```

## Factors Affecting IOPS

1. **Storage Type**

   - HDD: 80-120 IOPS (mechanical seek limits)
   - SATA SSD: 80,000-100,000 IOPS
   - NVMe SSD: 400,000-1,000,000+ IOPS

2. **Block Size**

   - Smaller blocks = higher IOPS potential
   - 4KB blocks: Standard for IOPS measurement
   - Larger blocks reduce IOPS but increase throughput

3. **Queue Depth**

   - Higher queue depth can increase IOPS
   - Diminishing returns beyond optimal depth
   - Also increases latency

4. **Access Pattern**
   - Random vs sequential
   - Read vs write
   - Mixed workloads

## Typical Values

### Random 4KB IOPS

**NVMe SSD:**

- Read: 400,000-1,000,000 IOPS
- Write: 300,000-900,000 IOPS

**SATA SSD:**

- Read: 80,000-100,000 IOPS
- Write: 60,000-90,000 IOPS

**HDD (7200 RPM):**

- Read: 80-120 IOPS
- Write: 80-120 IOPS

## Interpretation Guidelines

### Good Performance

- **Database server**: 10,000+ IOPS (SSD required)
- **Web server**: 1,000-5,000 IOPS
- **File server**: 500-2,000 IOPS
- **Desktop/laptop**: 300-1,000 IOPS

### Poor Performance Indicators

- IOPS significantly below device specifications
- High latency (>10ms for SSD, >20ms for HDD)
- Inconsistent IOPS across test runs
- IOPS degradation under load

## IOPS vs Throughput

| Metric            | Best For              | Typical Scenario |
| ----------------- | --------------------- | ---------------- |
| IOPS              | Random, small I/O     | Databases, VMs   |
| Throughput (MB/s) | Sequential, large I/O | Video, backups   |

**Example:**

- 100,000 IOPS × 4KB = 400 MB/s
- 1,000 IOPS × 1MB = 1,000 MB/s

Same throughput, very different access patterns!

## Measuring IOPS

### Using fio

```bash
fio --name=randread --ioengine=libaio --iodepth=32 \
    --rw=randread --bs=4k --direct=1 --size=1G \
    --numjobs=1 --runtime=60 --group_reporting
```

Look for: `IOPS=45.2k` in output

### Important Considerations

1. Use 4KB block size for standard comparison
2. Use direct I/O to bypass cache
3. Test with queue depth 1, 16, 32, 64
4. Run both read and write tests separately
5. Test mixed workloads (70/30 read/write)

## Related Metrics

- **Latency**: Time per operation (inverse relationship with IOPS)
- **Throughput**: MB/s or GB/s (IOPS × block size)
- **Queue Depth**: Concurrent operations in flight

## Related Tools

- [fio](../disk/fio.md) - Best for IOPS testing
- [bonnie++](../disk/bonnie++.md) - File system testing
