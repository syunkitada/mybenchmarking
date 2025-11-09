# Latency - Operation Response Time

## Definition

Latency measures the time delay from request initiation to response completion. In storage and network contexts, it represents how long individual operations take to complete, typically measured in milliseconds (ms) or microseconds (μs).

## What It Measures

Latency quantifies:

- Single operation completion time
- System responsiveness
- Time to first byte
- Request-response delay
- User experience impact

## Types of Latency

### Storage Latency

- **Read latency**: Time to retrieve data
- **Write latency**: Time to write data (includes acknowledgment)
- **Average latency**: Mean of all operations
- **Percentile latency**: 95th, 99th, 99.9th percentiles

### Network Latency

- **RTT (Round Trip Time)**: Time for packet to destination and back
- **One-way latency**: Time to destination only
- **Jitter**: Variation in latency over time

## Formula

```
Latency = Time(completion) - Time(request)
```

For storage:

```
Latency = Submission Latency + Queue Time + Service Time
```

## Typical Values

### Storage Latency (4KB Random Operations)

**NVMe SSD:**

- Average: 100-300 μs (0.1-0.3 ms)
- 99th percentile: 1-5 ms

**SATA SSD:**

- Average: 500-1000 μs (0.5-1.0 ms)
- 99th percentile: 5-15 ms

**HDD:**

- Average: 8-15 ms
- 99th percentile: 20-40 ms

### Network Latency (Ping/RTT)

**Same Data Center:**

- 0.1-1 ms

**Same Region:**

- 1-10 ms

**Cross-Country:**

- 30-100 ms

**Intercontinental:**

- 100-300 ms

## Interpretation Guidelines

### Good Latency

- Consistent across operations
- Low percentile spread (e.g., p99 < 2× average)
- Meets application requirements
- No outliers or spikes

### Poor Latency Indicators

- High average latency
- Large percentile spread (p99 >> average)
- Frequent spikes or outliers
- Increasing latency under load

## Latency vs Throughput Trade-off

Often inverse relationship:

- Higher queue depth → Higher throughput, Higher latency
- Lower queue depth → Lower latency, Lower throughput

**Example:**

```
Queue Depth 1:  500 IOPS, 2ms latency
Queue Depth 32: 15,000 IOPS, 64ms latency
```

## Percentile Latencies

Understanding distribution is crucial:

| Percentile    | Meaning                | Importance           |
| ------------- | ---------------------- | -------------------- |
| Average       | Mean value             | General baseline     |
| 50th (median) | Half operations faster | Typical experience   |
| 95th          | 95% faster than this   | Good user experience |
| 99th          | 99% faster than this   | Power users/SLA      |
| 99.9th        | 999/1000 faster        | Worst case scenario  |

**Why percentiles matter:**

- Average can hide outliers
- P99 affects 1 in 100 operations
- For high-traffic systems, 1% can be millions of requests

## Measuring Latency

### Using fio

```bash
fio --name=latency --ioengine=libaio --iodepth=1 \
    --rw=randread --bs=4k --direct=1 --size=1G \
    --runtime=60 --lat_percentiles=1
```

Output shows:

```
clat percentiles (usec):
 | 50.00th=[  285]
 | 95.00th=[  506]
 | 99.00th=[ 1369]
 | 99.90th=[ 1926]
```

### Using ping (Network)

```bash
ping -c 100 <host>
```

Output shows:

```
rtt min/avg/max/mdev = 0.123/0.456/2.345/0.234 ms
```

## Application Requirements

Different applications have different latency needs:

| Application            | Latency Requirement | Notes                      |
| ---------------------- | ------------------- | -------------------------- |
| High-frequency trading | <100 μs             | Microseconds matter        |
| Online gaming          | <50 ms              | User perception            |
| Database OLTP          | <5 ms               | Transaction responsiveness |
| Web pages              | <100 ms             | Page load feel             |
| Video streaming        | <200 ms             | Buffering masks latency    |
| Batch processing       | Seconds-minutes     | Throughput more important  |

## Latency Components

### Storage I/O Stack

1. **Application → System call**: Microseconds
2. **System call → Driver**: Microseconds
3. **Queue wait time**: Variable (queue depth dependent)
4. **Device service time**: Device-dependent
5. **Completion → Application**: Microseconds

### Optimization Tips

- Lower queue depth for latency-sensitive workloads
- Use polling instead of interrupts (for ultra-low latency)
- Minimize software layers
- Use faster storage technology
- Reduce network hops

## Related Metrics

- **IOPS**: Higher IOPS with low latency = excellent performance
- **Throughput**: Can be high even with moderate latency
- **Jitter**: Latency variation (network)

## Related Tools

- [fio](../disk/fio.md) - Storage latency testing
- [iperf3](../network/iperf3.md) - Network latency (UDP jitter)
- [netperf](../network/netperf.md) - TCP_RR for request-response latency
