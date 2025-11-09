# bonnie++ - File System Benchmark

## Overview

bonnie++ is a comprehensive file system and disk I/O benchmark tool that tests both character and block I/O performance. It provides a thorough evaluation of disk and file system performance.

## What It Measures

- **Sequential output**: Character and block output rates (KB/s)
- **Sequential input**: Character and block input rates (KB/s)
- **Random seeks**: Seeks per second
- **Sequential create/stat/delete**: File creation, stat, and deletion operations per second
- **Random create/stat/delete**: Random file operations per second
- **CPU usage**: Percentage CPU used during tests

## Installation

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install bonnie++
```

### RHEL/Fedora/CentOS

```bash
sudo dnf install bonnie++
# or
sudo yum install bonnie++
```

## Usage Examples

### Basic Test

```bash
bonnie++ -u root
```

### Specify Test Size (2x RAM recommended)

```bash
# For system with 16GB RAM, use 32GB
bonnie++ -u root -s 32G
```

### Test Specific Directory

```bash
bonnie++ -u root -d /mnt/testdisk
```

### Complete Test with Multiple Files

```bash
bonnie++ -u root -s 16G -n 128 -d /mnt/testdisk
```

### Quick Test (Smaller Size)

```bash
bonnie++ -u root -s 4G -n 64
```

## Understanding Output

Example output (CSV format):

```
1.98,1.98,myhost,1,1605123456,32G,,,98765,45,123456,67,,,98765,23,,,567,234,890,12,,,456,78,,,234,56,234,45,123,23,567,12,,,89,34
```

bonnie++ produces CSV output. Use `-h` flag or `bon_csv2html` to convert to readable format:

```bash
bonnie++ -u root -s 16G | bon_csv2html > results.html
```

Example HTML output shows:

**Sequential Output (Per Character)**

- **Write**: 98,765 K/s
- **CPU%**: 45%

**Sequential Output (Per Block)**

- **Write**: 123,456 K/s
- **CPU%**: 67%

**Sequential Input (Per Character)**

- **Read**: 98,765 K/s
- **CPU%**: 23%

**Random Seeks**

- **Seeks/s**: 567
- **CPU%**: 12%

**Sequential Create/Delete**

- **Create**: 234 files/s
- **Read**: 456 files/s
- **Delete**: 890 files/s

### Key Metrics

- **Per Character I/O**: Single-byte I/O performance
- **Per Block I/O**: Block-based I/O performance (more realistic)
- **Seeks**: Random seek performance (important for HDDs)
- **File operations**: Metadata operations (create/stat/delete)

### Typical Values

#### NVMe SSD

- **Sequential Read**: 2-5 GB/s (2,000,000-5,000,000 K/s)
- **Sequential Write**: 1-4 GB/s
- **Random Seeks**: 10,000-50,000 /s
- **File Creates**: 50,000-200,000 /s

#### SATA SSD

- **Sequential Read**: 400-600 MB/s (400,000-600,000 K/s)
- **Sequential Write**: 300-500 MB/s
- **Random Seeks**: 5,000-15,000 /s
- **File Creates**: 20,000-80,000 /s

#### HDD

- **Sequential Read**: 100-200 MB/s (100,000-200,000 K/s)
- **Sequential Write**: 80-180 MB/s
- **Random Seeks**: 80-120 /s
- **File Creates**: 200-800 /s

## Common Parameters

- `-u USER`: Run as specified user (often root for full access)
- `-s SIZE`: File size for I/O tests (should be 2x RAM)
- `-n NUM[:MAX:MIN:CHUNK]`: Number of files for file operation tests
- `-d DIR`: Directory to perform tests in
- `-m MACHINE`: Machine name for reporting
- `-x NUM`: Number of test iterations
- `-q`: Quiet mode, CSV output only

## Use Cases

- Comprehensive file system performance evaluation
- Comparing different file systems (ext4, xfs, btrfs)
- Testing storage arrays
- Validating RAID configurations
- Before/after system changes comparison

## Interpretation Tips

1. **File size matters**: Use 2x RAM size to avoid cache effects
2. **Per-block is realistic**: Block I/O more representative of real workloads
3. **Seeks for HDDs**: Critical metric for spinning disk performance
4. **File operations**: Important for workloads with many small files
5. **CPU percentage**: High CPU% may indicate system bottleneck
6. **Multiple runs**: Results can vary, run 3-5 times and average

## Complete Benchmark Example

```bash
#!/bin/bash
# Complete bonnie++ benchmark

# Determine RAM size and calculate test size
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
TEST_SIZE=$((RAM_GB * 2))G

echo "System RAM: ${RAM_GB}GB"
echo "Test size: ${TEST_SIZE}"
echo ""
echo "Running bonnie++ benchmark..."

# Run test and convert to HTML
bonnie++ -u root -s ${TEST_SIZE} -n 128 -d . -m $(hostname) \
    | tee bonnie_results.csv \
    | bon_csv2html > bonnie_results.html

echo ""
echo "Results saved to bonnie_results.html"
echo "Open in browser to view formatted results"
```

## Converting Results

### To HTML

```bash
bon_csv2html < results.csv > results.html
```

### To Plain Text Table

```bash
bon_csv2txt < results.csv
```

## Limitations

- Takes longer to run than simpler tools
- CSV output format requires conversion for readability
- Large file sizes needed for accurate results (2x RAM)
- May stress system significantly during test

## Related Documentation

- [Metrics: IOPS](../metrics/iops.md)
- [Metrics: Throughput](../metrics/throughput.md)
- [fio - Flexible I/O Tester](fio.md)
- [dd Disk Benchmark](dd.md)
