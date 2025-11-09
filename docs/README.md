# Linux Benchmark Tools Documentation

Comprehensive documentation for system benchmarking tools covering CPU, memory, disk, and network performance testing.

## Quick Navigation

### By Component

- **[CPU Benchmarks](#cpu-benchmarks)** - Processor performance testing
- **[Memory Benchmarks](#memory-benchmarks)** - RAM bandwidth and latency
- **[Disk Benchmarks](#disk-benchmarks)** - Storage I/O performance
- **[Network Benchmarks](#network-benchmarks)** - Network throughput and latency

### By Metric

- **[Understanding Metrics](#understanding-metrics)** - What the numbers mean
- **[Typical Values](#typical-values)** - Expected performance ranges
- **[Interpretation Guide](#interpretation-guide)** - How to read results

---

## CPU Benchmarks

Tools for testing processor performance, multi-core scaling, and computational capabilities.

### [sysbench](cpu/sysbench.md)

- **Best for**: Multi-threaded CPU performance
- **Measures**: Events per second, latency
- **Use case**: General CPU benchmarking, comparison testing
- **Quick start**: `sysbench cpu --threads=$(nproc) --time=60 run`

### [stress-ng](cpu/stress-ng.md)

- **Best for**: Stress testing, stability validation, thermal testing
- **Measures**: Bogo operations per second
- **Use case**: System stress testing, thermal validation
- **Quick start**: `stress-ng --cpu 0 --timeout 60s --metrics`

---

## Memory Benchmarks

Tools for testing memory bandwidth, latency, and throughput.

### [sysbench-memory](memory/sysbench-memory.md)

- **Best for**: Memory bandwidth testing with various patterns
- **Measures**: MB/s for sequential and random access
- **Use case**: Memory subsystem performance evaluation
- **Quick start**: `sysbench memory --memory-total-size=10G run`

### [mbw](memory/mbw.md)

- **Best for**: Quick memory bandwidth check
- **Measures**: Memory copy bandwidth (memcpy, dumb, mcblock)
- **Use case**: Quick memory performance snapshot
- **Quick start**: `mbw 500`

---

## Disk Benchmarks

Tools for testing storage performance including IOPS, throughput, and latency.

### [fio](disk/fio.md)

**⭐ Recommended - Industry Standard**

- **Best for**: Comprehensive disk I/O testing
- **Measures**: IOPS, bandwidth, latency percentiles
- **Use case**: Detailed storage performance analysis
- **Quick start**:
  ```bash
  fio --name=test --ioengine=libaio --iodepth=32 --rw=randread --bs=4k --direct=1 --size=1G --runtime=60
  ```

### [dd](disk/dd.md)

- **Best for**: Quick sequential throughput test
- **Measures**: Sequential read/write MB/s
- **Use case**: Simple bandwidth check, always available
- **Quick start**: `dd if=/dev/zero of=testfile bs=1M count=1024 oflag=direct`

### [bonnie++](disk/bonnie++.md)

- **Best for**: File system comprehensive testing
- **Measures**: Sequential I/O, random seeks, file operations
- **Use case**: File system evaluation, comprehensive testing
- **Quick start**: `bonnie++ -u root -s 16G`

---

## Network Benchmarks

Tools for testing network bandwidth, latency, and throughput.

### [iperf3](network/iperf3.md)

**⭐ Recommended - Industry Standard**

- **Best for**: Network bandwidth measurement
- **Measures**: Bandwidth (Gbps/Mbps), jitter, packet loss
- **Use case**: Network throughput testing
- **Quick start**:
  ```bash
  # Server: iperf3 -s
  # Client: iperf3 -c <server-ip> -t 60
  ```

### [netperf](network/netperf.md)

- **Best for**: Comprehensive network testing with various patterns
- **Measures**: Bandwidth, latency, transaction rate
- **Use case**: Detailed network performance analysis
- **Quick start**:
  ```bash
  # Server: netserver
  # Client: netperf -H <server-ip> -l 60
  ```

---

## Understanding Metrics

Core performance metrics and what they mean:

### [IOPS](metrics/iops.md) - Input/Output Operations Per Second

- **What**: Number of I/O operations completed per second
- **When**: Random access workloads (databases, VMs)
- **Typical**:
  - NVMe: 400K-1M IOPS
  - SATA SSD: 80K-100K IOPS
  - HDD: 80-120 IOPS

### [Throughput](metrics/throughput.md) - Data Transfer Rate

- **What**: Amount of data transferred per second (MB/s, GB/s)
- **When**: Sequential workloads (video, backups, file transfers)
- **Typical**:
  - NVMe: 3-7 GB/s read
  - SATA SSD: 500-600 MB/s
  - HDD: 120-200 MB/s

### [Latency](metrics/latency.md) - Operation Response Time

- **What**: Time from request to completion (ms, μs)
- **When**: Response time matters (interactive applications)
- **Typical**:
  - NVMe: 100-300 μs
  - SATA SSD: 0.5-1.0 ms
  - HDD: 8-15 ms

### [Bandwidth](metrics/bandwidth.md) - Network Capacity

- **What**: Network data transfer rate (Mbps, Gbps)
- **When**: Network performance testing
- **Typical**:
  - 1 Gbps link: 920-950 Mbps (TCP)
  - 10 Gbps link: 9.2-9.5 Gbps
  - Wi-Fi 6: 600-1200 Mbps per stream

---

## Typical Values

Quick reference for expected performance:

### Storage Performance

| Device Type  | Random IOPS (4K) | Sequential Read | Sequential Write |
| ------------ | ---------------- | --------------- | ---------------- |
| NVMe SSD     | 400K-1M          | 3-7 GB/s        | 2-5 GB/s         |
| SATA SSD     | 80K-100K         | 500-600 MB/s    | 400-550 MB/s     |
| HDD 7200 RPM | 80-120           | 120-200 MB/s    | 100-180 MB/s     |

### Network Performance

| Link Type        | TCP Bandwidth | UDP Bandwidth | Latency          |
| ---------------- | ------------- | ------------- | ---------------- |
| 1 Gbps Ethernet  | 920-950 Mbps  | ~980 Mbps     | 0.1-1 ms (LAN)   |
| 10 Gbps Ethernet | 9.2-9.5 Gbps  | ~9.8 Gbps     | 0.1-0.5 ms (LAN) |
| Wi-Fi 6          | 400-800 Mbps  | Variable      | 2-10 ms          |

### CPU Performance (sysbench)

| CPU Type                | Events/sec (8 cores) | Notes            |
| ----------------------- | -------------------- | ---------------- |
| Desktop (i7-9700K)      | 12,000-15,000        | Consumer-grade   |
| Server (Xeon)           | 20,000-40,000        | Server-optimized |
| High-end (Threadripper) | 25,000-50,000        | Many cores       |

---

## Interpretation Guide

### Reading Benchmark Results

1. **Compare like with like**: Same tool, same parameters, same duration
2. **Run multiple times**: Average 3-5 runs for consistency
3. **Check percentiles**: P95/P99 matter more than average for user experience
4. **Consider context**: Different workloads need different metrics
5. **Look for consistency**: Low variance indicates stable performance

### Performance Red Flags

- ❌ Results far below device specifications (>30% lower)
- ❌ High variance between test runs (>10% difference)
- ❌ Performance degradation over time
- ❌ High latency percentile spread (P99 >> 2× average)
- ❌ Thermal throttling (performance drops as test continues)

### Good Performance Indicators

- ✅ Achieves 80-95% of device specifications
- ✅ Consistent results across multiple runs
- ✅ Low percentile spread (P99 < 2× average)
- ✅ Performance scales with resources (threads, queue depth)
- ✅ Stable under sustained load

---

## Getting Started

1. **Choose the right tool** for your workload type
2. **Read the tool-specific documentation** for proper usage
3. **Run baseline tests** before making changes
4. **Make one change at a time** to isolate effects
5. **Document your configuration** (kernel version, drivers, settings)
6. **Run multiple iterations** for statistical validity

## Saving Your Results

Use mybench CLI to save and track benchmark results:

```bash
# Save a benchmark result
mybench save

# List all results
mybench list

# Compare two results
mybench compare <result-id-1> <result-id-2>
```

See [mybench CLI documentation](../README.md) for more details.

---

## Additional Resources

- **Installation guides**: Each tool page includes distribution-specific install commands
- **Usage examples**: Copy-paste ready examples for common scenarios
- **Metric definitions**: Detailed explanations in the metrics/ directory
- **Typical values**: Expected performance ranges for common hardware

## Contributing

Found an error or want to add documentation for another tool? See [CONTRIBUTING.md](../CONTRIBUTING.md).

---

_Last updated: November 9, 2025_
