# Installation Guide - General Linux Package Management

## Overview

This guide provides general tips for installing benchmark tools on Linux systems. Specific tool installation instructions are available in each tool's documentation.

## Package Managers by Distribution

### Debian/Ubuntu

```bash
# Update package list
sudo apt update

# Search for packages
apt search <package-name>

# Install package
sudo apt install <package-name>

# Show package information
apt show <package-name>
```

### RHEL/Fedora/CentOS

```bash
# Update package cache (Fedora/CentOS 8+)
sudo dnf check-update

# Search for packages
dnf search <package-name>

# Install package
sudo dnf install <package-name>

# Show package information
dnf info <package-name>

# For older CentOS/RHEL 7
sudo yum install <package-name>
```

### Arch Linux

```bash
# Update system
sudo pacman -Syu

# Search for packages
pacman -Ss <package-name>

# Install package
sudo pacman -S <package-name>

# Show package information
pacman -Si <package-name>
```

## Installing from Source

Some benchmark tools may need to be compiled from source. General steps:

```bash
# Install build essentials
# Debian/Ubuntu:
sudo apt install build-essential git

# RHEL/Fedora:
sudo dnf groupinstall "Development Tools"
sudo dnf install git

# Clone repository
git clone <repository-url>
cd <directory>

# Read installation instructions
cat README.md
cat INSTALL

# Common build steps
./configure
make
sudo make install

# Or with CMake
mkdir build && cd build
cmake ..
make
sudo make install
```

## Common Dependencies

### For CPU Benchmarks

Most CPU benchmarks require minimal dependencies and are available in default repositories.

### For Disk Benchmarks

```bash
# fio dependencies
sudo apt install libaio-dev  # Debian/Ubuntu
sudo dnf install libaio-devel  # RHEL/Fedora
```

### For Network Benchmarks

Network benchmarks typically have no special dependencies beyond standard C libraries.

## Verification After Installation

```bash
# Check if tool is installed
which <tool-name>

# Check version
<tool-name> --version

# View help/usage
<tool-name> --help
```

## Tool-Specific Installation

For detailed installation instructions for each benchmark tool, see:

### CPU Benchmarks

- [sysbench](cpu/sysbench.md#installation)
- [stress-ng](cpu/stress-ng.md#installation)

### Memory Benchmarks

- [sysbench memory](memory/sysbench-memory.md#installation)
- [mbw](memory/mbw.md#installation)

### Disk Benchmarks

- [fio](disk/fio.md#installation)
- [dd](disk/dd.md#installation)
- [bonnie++](disk/bonnie++.md#installation)

### Network Benchmarks

- [iperf3](network/iperf3.md#installation)
- [netperf](network/netperf.md#installation)

## Troubleshooting

### Package Not Found

1. Update package cache: `sudo apt update` or `sudo dnf check-update`
2. Search with different names: `apt search benchmark`
3. Check if package is in a different repository
4. Consider installing from source

### Build Failures

1. Install missing dependencies listed in error messages
2. Check README/INSTALL for specific requirements
3. Search for distribution-specific build instructions
4. Check issue tracker on project repository

### Permission Errors

1. Some benchmarks need root/sudo to access hardware directly
2. Use `sudo` for installation commands
3. For running benchmarks, check tool documentation for required permissions

## Best Practices

1. **Always update package cache first**: `apt update` or `dnf check-update`
2. **Read tool documentation**: Check specific requirements
3. **Install from repositories when possible**: Easier updates and security patches
4. **Keep systems updated**: `apt upgrade` or `dnf upgrade`
5. **Use virtual environments**: Consider containers for isolated testing

## Additional Resources

- [Debian Package Management](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html)
- [Fedora Package Management](https://docs.fedoraproject.org/en-US/quick-docs/dnf/)
- [ArchWiki Package Management](https://wiki.archlinux.org/title/Pacman)
