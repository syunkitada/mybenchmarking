# Throughput - Data Transfer Rate

## Definition

Throughput measures the amount of data transferred per unit of time, typically expressed in MB/s (megabytes per second) or GB/s (gigabytes per second). It's the primary metric for sequential I/O and bulk data transfer performance.

## What It Measures

Throughput quantifies:

- Sequential read/write performance
- Bulk data transfer rates
- File copy speeds
- Streaming performance
- Backup/restore speeds

## Formula

```
Throughput = Data Transferred / Time
Common units: KB/s, MB/s, GB/s
```

## Factors Affecting Throughput

1. **Block Size**

   - Larger blocks = higher throughput
   - 128KB-1MB typical for sequential workloads
   - 4KB blocks limit maximum throughput

2. **Storage Technology**

   - Interface bandwidth (SATA, NVMe, network)
   - Device capabilities
   - RAID configuration

3. **Queue Depth**

   - Higher depth can increase throughput
   - Especially important for NVMe

4. **Access Pattern**
   - Sequential access achieves maximum throughput
   - Random access reduces throughput significantly

## Typical Values

### Sequential Throughput

**NVMe SSD:**

- Read: 3-7 GB/s
- Write: 2-5 GB/s

**SATA SSD:**

- Read: 500-600 MB/s (SATA III limit ~550 MB/s)
- Write: 400-550 MB/s

**HDD (7200 RPM):**

- Read: 120-200 MB/s
- Write: 100-180 MB/s

**Network:**

- 1 Gbps: ~110-120 MB/s (theoretically 125 MB/s)
- 10 Gbps: ~1.1-1.2 GB/s
- 100 Gbps: ~11-12 GB/s

## Interpretation Guidelines

### Good Performance

- Achieves 80-95% of theoretical maximum
- Consistent across multiple runs
- Scales with block size appropriately
- No degradation over time

### Poor Performance Indicators

- <50% of device specifications
- High variance between runs
- Performance drops with larger files
- Throughput drops under sustained load

## Throughput vs IOPS

Different workloads require different optimization:

| Workload Type | Optimize For | Example Applications                  |
| ------------- | ------------ | ------------------------------------- |
| Sequential    | Throughput   | Video editing, backups, file transfer |
| Random        | IOPS         | Databases, VMs, web servers           |

**Relationship:**

```
Throughput = IOPS × Block Size
```

Example:

- 100,000 IOPS × 4KB = 400 MB/s
- 4,000 IOPS × 128KB = 512 MB/s

## Measuring Throughput

### Using fio

```bash
# Sequential read
fio --name=seqread --ioengine=libaio --iodepth=32 \
    --rw=read --bs=128k --direct=1 --size=4G \
    --runtime=60 --group_reporting
```

Look for: `BW=2.5GiB/s` in output

### Using dd

```bash
dd if=/dev/zero of=testfile bs=1M count=1024 oflag=direct
```

Look for: `1073741824 bytes copied, 5.23456 s, 205 MB/s`

## Block Size Impact

| Block Size | Use Case                | Typical Result                |
| ---------- | ----------------------- | ----------------------------- |
| 4KB        | Random I/O, databases   | Lower throughput, higher IOPS |
| 128KB      | General sequential      | Balanced performance          |
| 1MB        | Large file transfers    | Maximum throughput            |
| 4MB        | Video, very large files | Maximum sequential throughput |

## Network Throughput

### TCP vs UDP

- **TCP**: Reliable, includes overhead, ~90-95% of link speed
- **UDP**: Lower overhead, can achieve ~98% of link speed

### Bandwidth Units

- **Bits vs Bytes**: Network typically measured in bits/sec
  - 1 Gbps = 125 MB/s (theoretical)
  - Practical TCP throughput: 110-120 MB/s
  - 10 Gbps = 1,100-1,200 MB/s practical

## Related Metrics

- **IOPS**: Operations per second (for random I/O)
- **Latency**: Time per operation
- **Bandwidth**: Often used interchangeably with throughput

## Related Tools

- [fio](../disk/fio.md) - Comprehensive I/O testing
- [dd](../disk/dd.md) - Simple sequential testing
- [iperf3](../network/iperf3.md) - Network throughput
