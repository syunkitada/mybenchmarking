# Bandwidth - Network Data Transfer Rate

## Definition

Bandwidth measures the maximum rate of data transfer across a network connection, typically expressed in bits per second (bps), megabits per second (Mbps), or gigabits per second (Gbps).

## What It Measures

Bandwidth quantifies:

- Network throughput capacity
- Data transfer speed
- Link utilization
- Available network capacity

## Common Units

### Bits vs Bytes

- **Network**: Typically measured in bits/sec (Mbps, Gbps)
- **Storage**: Typically measured in bytes/sec (MB/s, GB/s)
- **Conversion**: 8 bits = 1 byte

```
1 Gbps = 1,000 Mbps = 125 MB/s (theoretical)
```

### Unit Conversions

- 1 Kbps = 1,000 bits per second
- 1 Mbps = 1,000,000 bits per second
- 1 Gbps = 1,000,000,000 bits per second

## Typical Values

### Network Links

**Ethernet:**

- 100 Mbps (Fast Ethernet): ~11-12 MB/s practical
- 1 Gbps (Gigabit): ~110-120 MB/s practical (94-96% efficiency)
- 10 Gbps: ~1,100-1,200 MB/s practical
- 100 Gbps: ~11-12 GB/s practical

**Wi-Fi:**

- Wi-Fi 5 (802.11ac): 433 Mbps - 1.3 Gbps per stream
- Wi-Fi 6 (802.11ax): 600 Mbps - 1.2 Gbps per stream
- Practical throughput: 40-60% of theoretical

## Theoretical vs Practical Bandwidth

### TCP Overhead

- IP headers: 20 bytes
- TCP headers: 20 bytes
- Ethernet: 38 bytes overhead per packet
- **Result**: ~94-96% efficiency for large transfers

### UDP Overhead

- Lower overhead than TCP
- Can achieve ~98% of link capacity
- No reliability guarantees

## Factors Affecting Bandwidth

1. **Physical Link**

   - Cable quality (Cat5e vs Cat6 vs fiber)
   - Link speed negotiation
   - Distance limitations

2. **Protocol Overhead**

   - TCP: ~94-96% efficiency
   - UDP: ~98% efficiency
   - Encryption: Additional overhead

3. **Network Congestion**

   - Shared bandwidth
   - Packet loss and retransmissions
   - Buffer overflow

4. **TCP Window Size**
   - Limits maximum throughput
   - BDP (Bandwidth-Delay Product)
   - TCP tuning required for high-speed/high-latency

## Measuring Bandwidth

### Using iperf3

```bash
# Server
iperf3 -s

# Client (TCP)
iperf3 -c <server-ip> -t 60

# Client (UDP with 1 Gbps target)
iperf3 -c <server-ip> -u -b 1G -t 60
```

### Understanding iperf3 Output

```
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-60.00  sec  6.54 GBytes   938 Mbits/sec    0   sender
[  5]   0.00-60.00  sec  6.54 GBytes   938 Mbits/sec        receiver
```

**Key values:**

- 938 Mbits/sec on 1 Gbps link = 93.8% efficiency (good!)
- Retr = 0: No retransmissions (excellent)

## Bandwidth vs Latency

Independent but related metrics:

| Scenario  | Bandwidth | Latency | Example         |
| --------- | --------- | ------- | --------------- |
| Local LAN | 1 Gbps    | 0.5 ms  | Office network  |
| Satellite | 100 Mbps  | 600 ms  | Remote location |
| LTE       | 50 Mbps   | 50 ms   | Mobile network  |

**Bandwidth-Delay Product:**

```
BDP = Bandwidth × Round-Trip Time
```

High BDP networks (high bandwidth + high latency) require larger TCP buffers.

## Application Requirements

| Application         | Bandwidth Need | Notes                            |
| ------------------- | -------------- | -------------------------------- |
| 4K video streaming  | 25 Mbps        | Per stream                       |
| HD video streaming  | 5-8 Mbps       | Per stream                       |
| Video conferencing  | 1-4 Mbps       | Per participant                  |
| Large file transfer | Max available  | Time = Size / Bandwidth          |
| Web browsing        | 1-10 Mbps      | Variable by content              |
| VoIP                | 64-128 Kbps    | Low bandwidth, needs low latency |

## Optimizing Bandwidth Utilization

### Network Level

1. **Use appropriate cables**: Cat6 for Gigabit, fiber for 10G+
2. **Reduce hops**: Fewer routers/switches
3. **Quality equipment**: Good switches and NICs
4. **Minimize interference**: Especially for Wi-Fi

### Protocol Level

1. **TCP tuning**: Adjust window sizes
2. **Parallel streams**: Use multiple connections
3. **Compression**: Reduce data size
4. **Protocol selection**: UDP for streaming, TCP for reliability

### Testing Multiple Streams

```bash
iperf3 -c <server-ip> -P 4 -t 60
```

Parallel streams can improve utilization on high-latency links.

## Common Bottlenecks

1. **Cable/Interface**: 100 Mbps NIC on Gigabit network
2. **Switch capacity**: Oversubscribed switch
3. **Internet connection**: ISP bandwidth limit
4. **TCP window size**: Limits high BDP links
5. **CPU**: Processing overhead for encryption or compression

## Interpretation Guidelines

### Good Performance

- Achieves 90-96% of link capacity (TCP)
- Consistent bandwidth across test duration
- Low retransmissions (<0.1%)
- Bidirectional performance balanced

### Poor Performance Indicators

- <80% of link capacity
- High retransmissions (>1%)
- Bandwidth drops over time
- Asymmetric performance (upload vs download)

## Related Metrics

- **Throughput**: Application-level data transfer rate
- **Latency**: Time delay (affects perceived performance)
- **Packet loss**: Reduces effective bandwidth
- **Jitter**: Affects streaming quality

## Related Tools

- [iperf3](../network/iperf3.md) - Standard bandwidth testing
- [netperf](../network/netperf.md) - Comprehensive network testing
