# netperf - Network Performance Benchmark

## Overview

netperf is a comprehensive network performance testing tool that measures various aspects of network performance including bandwidth, latency, and transaction rates.

## What It Measures

- **TCP Stream**: Bulk data transfer bandwidth
- **UDP Stream**: UDP bandwidth and packet loss
- **TCP RR**: Request-response latency and transaction rate
- **TCP CRR**: Connect-request-response (connection setup cost)

## Installation

### Ubuntu/Debian

```bash
sudo apt update && sudo apt install netperf
```

### RHEL/Fedora/CentOS

```bash
sudo dnf install netperf
```

## Usage Examples

### Server Mode

```bash
netserver
```

### TCP Stream (Bandwidth)

```bash
netperf -H <server-ip> -l 60 -- -m 65536
```

### TCP Request-Response (Latency)

```bash
netperf -H <server-ip> -t TCP_RR -l 60
```

### UDP Stream

```bash
netperf -H <server-ip> -t UDP_STREAM -l 60
```

### Multiple Parallel Streams

```bash
for i in {1..4}; do netperf -H <server-ip> -l 60 & done
wait
```

## Understanding Output

TCP_STREAM output:

```
Recv   Send    Send
Socket Socket  Message  Elapsed
Size   Size    Size     Time     Throughput
bytes  bytes   bytes    secs.    10^6bits/sec

 87380  16384  16384    60.00     941.23
```

TCP_RR output:

```
Local /Remote
Socket Size   Request  Resp.   Elapsed  Trans.
Send   Recv   Size     Size    Time     Rate
bytes  bytes  bytes    bytes   secs.    per sec

16384  87380  1        1       60.00    25432.45
```

### Typical Values

**TCP_STREAM (1 Gbps)**

- Throughput: 920-950 Mbits/sec

**TCP_RR (Request-Response)**

- Transactions/sec: 20,000-30,000 on 1 Gbps

## Common Parameters

- `-H HOST`: Target host
- `-t TEST`: Test type (TCP_STREAM, TCP_RR, UDP_STREAM, etc.)
- `-l TIME`: Test duration in seconds
- `-- -m SIZE`: Message size

## Related Documentation

- [Metrics: Bandwidth](../metrics/bandwidth.md)
- [Metrics: Latency](../metrics/latency.md)
- [iperf3](iperf3.md)
