# iperf3 - Network Bandwidth Measurement

## Overview

iperf3 is the standard tool for measuring network bandwidth between two hosts. It supports TCP, UDP, and SCTP protocols.

## What It Measures

- **Bandwidth**: Throughput in Mbits/sec or Gbits/sec
- **Jitter**: Variation in packet arrival times (UDP)
- **Packet loss**: Percentage of lost packets (UDP)
- **Retransmits**: TCP retransmission count

## Installation

### Ubuntu/Debian

```bash
sudo apt update && sudo apt install iperf3
```

### RHEL/Fedora/CentOS

```bash
sudo dnf install iperf3
```

## Usage Examples

### Server Mode

```bash
iperf3 -s
```

### Client - TCP Test

```bash
iperf3 -c <server-ip> -t 60
```

### Client - UDP Test

```bash
iperf3 -c <server-ip> -u -b 1G -t 60
```

### Parallel Streams

```bash
iperf3 -c <server-ip> -P 4 -t 60
```

### Reverse Mode (Server Sends)

```bash
iperf3 -c <server-ip> -R -t 60
```

### Bidirectional Test

```bash
iperf3 -c <server-ip> --bidir -t 60
```

## Understanding Output

```
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-60.00  sec  6.54 GBytes   938 Mbits/sec    0   sender
[  5]   0.00-60.00  sec  6.54 GBytes   938 Mbits/sec        receiver
```

### Typical Values

- **1 Gbps Link**: 920-950 Mbits/sec (TCP), ~940 Mbits/sec (UDP)
- **10 Gbps Link**: 9.2-9.5 Gbits/sec
- **100 Mbps Link**: 92-95 Mbits/sec

## Common Parameters

- `-s`: Server mode
- `-c HOST`: Client mode, connect to HOST
- `-t TIME`: Test duration in seconds
- `-P NUM`: Number of parallel streams
- `-u`: UDP mode instead of TCP
- `-b RATE`: Target bandwidth for UDP
- `-R`: Reverse mode (server sends)
- `-i INTERVAL`: Report interval in seconds

## Related Documentation

- [Metrics: Bandwidth](../metrics/bandwidth.md)
- [netperf](netperf.md)
