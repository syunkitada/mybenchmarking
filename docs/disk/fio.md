# fio - Flexible I/O Tester

## Overview

fio (Flexible I/O Tester) is the industry-standard disk benchmarking tool. It provides comprehensive I/O workload simulation with fine-grained control over I/O patterns, queue depths, and concurrency.

## What It Measures

- **IOPS**: Input/Output Operations Per Second
- **Bandwidth**: Throughput in KB/s or MB/s
- **Latency**: Minimum, average, maximum, and percentile latencies
- **CPU usage**: System and user CPU utilization during I/O

## Installation

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install fio
```

### RHEL/Fedora/CentOS

```bash
sudo dnf install fio
# or
sudo yum install fio
```

## Usage Examples

### Random Read IOPS Test

```bash
fio --name=randread --ioengine=libaio --iodepth=32 --rw=randread \
    --bs=4k --direct=1 --size=1G --numjobs=1 --runtime=60 \
    --group_reporting
```

### Random Write IOPS Test

```bash
fio --name=randwrite --ioengine=libaio --iodepth=32 --rw=randwrite \
    --bs=4k --direct=1 --size=1G --numjobs=1 --runtime=60 \
    --group_reporting
```

### Sequential Read Bandwidth Test

```bash
fio --name=seqread --ioengine=libaio --iodepth=32 --rw=read \
    --bs=128k --direct=1 --size=4G --numjobs=1 --runtime=60 \
    --group_reporting
```

### Sequential Write Bandwidth Test

```bash
fio --name=seqwrite --ioengine=libaio --iodepth=32 --rw=write \
    --bs=128k --direct=1 --size=4G --numjobs=1 --runtime=60 \
    --group_reporting
```

### Mixed Read/Write (70/30)

```bash
fio --name=mixed --ioengine=libaio --iodepth=32 --rw=randrw \
    --rwmixread=70 --bs=4k --direct=1 --size=1G --numjobs=4 \
    --runtime=60 --group_reporting
```

### Latency-Focused Test

```bash
fio --name=latency --ioengine=libaio --iodepth=1 --rw=randread \
    --bs=4k --direct=1 --size=1G --runtime=60 \
    --lat_percentiles=1 --group_reporting
```

## Understanding Output

Example output:

```
randread: (g=0): rw=randread, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=libaio, iodepth=32
fio-3.28
Starting 1 process
randread: Laying out IO file (1 file / 1024MiB)

randread: (groupid=0, jobs=1): err= 0: pid=12345: Sat Nov  9 00:00:00 2025
  read: IOPS=45.2k, BW=177MiB/s (185MB/s)(10.4GiB/60001msec)
    slat (usec): min=2, avg=3.45, max=456
    clat (usec): min=145, avg=704.12, max=12345
     lat (usec): min=150, avg=707.57, max=12350
    clat percentiles (usec):
     |  1.00th=[  245],  5.00th=[  330], 10.00th=[  400],
     | 20.00th=[  490], 30.00th=[  570], 40.00th=[  635],
     | 50.00th=[  685], 60.00th=[  740], 70.00th=[  807],
     | 80.00th=[  889], 90.00th=[ 1004], 95.00th=[ 1106],
     | 99.00th=[ 1369], 99.50th=[ 1500], 99.90th=[ 1926],
     | 99.95th=[ 2180], 99.99th=[ 3130]
  cpu          : usr=5.32%, sys=12.54%, ctx=2712345, majf=0, minf=41
```

### Key Metrics

- **IOPS**: Operations per second (higher is better for random I/O)
- **BW (Bandwidth)**: Throughput (higher is better for sequential I/O)
- **slat**: Submission latency
- **clat**: Completion latency (most important)
- **lat**: Total latency (submission + completion)
- **Percentiles**: Distribution of latencies

### Typical Values

#### NVMe SSD

- **Random Read 4K**: 400K-1M IOPS
- **Random Write 4K**: 300K-900K IOPS
- **Sequential Read**: 3-7 GB/s
- **Sequential Write**: 2-5 GB/s

#### SATA SSD

- **Random Read 4K**: 80K-100K IOPS
- **Random Write 4K**: 60K-90K IOPS
- **Sequential Read**: 500-600 MB/s
- **Sequential Write**: 400-550 MB/s

#### HDD

- **Random Read 4K**: 80-120 IOPS
- **Random Write 4K**: 80-120 IOPS
- **Sequential Read**: 120-200 MB/s
- **Sequential Write**: 100-180 MB/s

## Common Parameters

- `--name=NAME`: Job name
- `--ioengine=ENGINE`: I/O engine (libaio, io_uring, sync, etc.)
- `--iodepth=N`: Queue depth for async engines
- `--rw=TYPE`: I/O pattern (read, write, randread, randwrite, randrw)
- `--bs=SIZE`: Block size (4k, 8k, 128k, 1m, etc.)
- `--size=SIZE`: Total I/O size per job
- `--numjobs=N`: Number of parallel jobs
- `--runtime=SECS`: Time-based runtime
- `--direct=1`: Bypass OS cache (O_DIRECT)
- `--group_reporting`: Aggregate results across all jobs

## Job File Example

Save as `benchmark.fio`:

```ini
[global]
ioengine=libaio
direct=1
size=1G
runtime=60
group_reporting

[randread-4k]
rw=randread
bs=4k
iodepth=32
numjobs=1

[randwrite-4k]
rw=randwrite
bs=4k
iodepth=32
numjobs=1

[seqread-128k]
rw=read
bs=128k
iodepth=32
numjobs=1
```

Run with:

```bash
fio benchmark.fio
```

## Use Cases

- **Storage performance testing**: Benchmark different storage types
- **Workload simulation**: Simulate database or application I/O patterns
- **Performance tuning**: Test effects of different I/O depths and block sizes
- **SSD endurance testing**: Long-running write tests
- **Latency characterization**: Measure 99th percentile latencies

## Interpretation Tips

1. **Queue depth matters**: Higher iodepth increases IOPS but also latency
2. **Block size impact**: Larger blocks increase bandwidth but reduce IOPS
3. **Random vs Sequential**: Completely different performance characteristics
4. **Direct I/O**: Use `--direct=1` to bypass caching for true disk performance
5. **Multiple jobs**: Increase numjobs to saturate high-performance devices
6. **Percentile latencies**: Focus on 95th/99th percentiles for real-world impact

## Advanced Examples

### Database Simulation

```bash
fio --name=db --ioengine=libaio --iodepth=8 --rw=randrw \
    --rwmixread=75 --bs=8k --direct=1 --size=10G --numjobs=16 \
    --runtime=300 --group_reporting
```

### Latency Testing

```bash
fio --name=lowlat --ioengine=libaio --iodepth=1 --rw=randread \
    --bs=4k --direct=1 --size=1G --runtime=60 \
    --lat_percentiles=1 --clat_percentiles=1
```

## Related Documentation

- [Metrics: IOPS](../metrics/iops.md)
- [Metrics: Throughput](../metrics/throughput.md)
- [Metrics: Latency](../metrics/latency.md)
- [dd Disk Benchmark](dd.md)
