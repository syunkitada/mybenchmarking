# System Profiles

This directory stores system profile files that describe the hardware specifications of your benchmark systems.

## Structure

Each system profile is a JSON file named with a unique profile ID:

```
systems/
├── my-desktop.json
├── my-laptop.json
└── vm-test01.json
```

## Creating a System Profile

Use the CLI to create a new system profile:

```bash
mybench system create
```

Or manually create a JSON file following the schema:

### Physical Machine Example

```json
{
  "profile_id": "my-desktop",
  "profile_name": "My Desktop PC",
  "type": "physical",
  "created": "2025-11-09",
  "hardware": {
    "cpu": {
      "model": "Intel Core i7-9700K",
      "cores": 8,
      "threads": 8,
      "base_clock_ghz": 3.6,
      "max_clock_ghz": 4.9
    },
    "memory": {
      "total_gb": 32,
      "type": "DDR4",
      "speed_mhz": 3200
    },
    "disk": {
      "model": "Samsung 970 EVO Plus",
      "type": "NVMe SSD",
      "capacity_gb": 1000
    },
    "network": {
      "interface": "Intel I219-V",
      "speed_gbps": 1
    }
  },
  "notes": "Primary development workstation"
}
```

### Virtual Machine Example

```json
{
  "profile_id": "vm-test01",
  "profile_name": "Test VM 01",
  "type": "virtual",
  "created": "2025-11-09",
  "virtualization": {
    "hypervisor": "QEMU/KVM",
    "host_system": "my-desktop",
    "cpu_type": "host-passthrough",
    "cpu_topology": "sockets=1,cores=4,threads=1"
  },
  "hardware": {
    "cpu": {
      "vcpus": 4,
      "cpu_mode": "host-passthrough",
      "pinning": "0-3"
    },
    "memory": {
      "total_gb": 8,
      "hugepages": true,
      "hugepage_size": "2MB"
    },
    "disk": {
      "backend": "virtio-blk",
      "type": "qcow2",
      "capacity_gb": 100,
      "cache_mode": "none",
      "io_mode": "native"
    },
    "network": {
      "model": "virtio-net",
      "backend": "vhost-net"
    }
  },
  "notes": "Performance testing VM"
}
```

## Usage

List all system profiles:

```bash
mybench system list
```

View a specific profile:

```bash
mybench system show my-desktop
```

Auto-detect current system (for quick profile creation):

```bash
mybench system detect
```
