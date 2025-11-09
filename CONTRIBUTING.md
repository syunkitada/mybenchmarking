# Contributing to mybench

Thank you for your interest in contributing to the Linux Server Benchmark Documentation Toolkit!

## How to Contribute

### Adding Tool Documentation

The primary way to contribute is by adding documentation for additional benchmark tools.

#### Documentation Structure

Each tool documentation should follow this structure:

````markdown
# Tool Name - Category

## Overview

Brief description of what the tool does and what it measures.

## What It Measures

- Bullet points of key metrics
- What aspects of performance it tests

## Installation

### Ubuntu/Debian

```bash
sudo apt install tool-name
```
````

### RHEL/Fedora/CentOS

```bash
sudo dnf install tool-name
```

## Usage Examples

### Example 1: Basic Test

```bash
tool-name --basic-option
```

### Example 2: Advanced Test

```bash
tool-name --advanced-option --parameter=value
```

## Understanding Output

Example output with explanation of key metrics.

### Key Metrics

- **metric_name**: Description (higher/lower is better)

### Typical Values

- Device Type 1: X-Y value range
- Device Type 2: X-Y value range

## Common Parameters

- `--param`: Description
- `--param2`: Description

## Use Cases

- Use case 1
- Use case 2

## Interpretation Tips

1. Tip 1
2. Tip 2

## Related Documentation

- [Related Tool](path/to/tool.md)
- [Related Metric](../metrics/metric.md)

````

#### Steps to Add a New Tool

1. **Choose the category**: CPU, memory, disk, or network
2. **Create the file**: `docs/{category}/{tool-name}.md`
3. **Follow the template**: Use the structure above
4. **Include installation instructions**: For major distributions
5. **Provide usage examples**: At least 3 different scenarios
6. **Add typical values**: For common hardware types
7. **Include interpretation guidance**: Help users understand results
8. **Link to related documentation**: Metrics and related tools

#### Example Pull Request

See existing tool documentation for examples:
- [sysbench](docs/cpu/sysbench.md)
- [fio](docs/disk/fio.md)
- [iperf3](docs/network/iperf3.md)

### Adding Metric Documentation

To add a new metric definition:

1. **Create file**: `docs/metrics/{metric-name}.md`
2. **Include sections**:
   - Definition
   - What It Measures
   - Typical Values (by hardware type)
   - Interpretation Guidelines
   - Related Tools

### Adding CLI Features

To contribute code changes:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Follow the project structure**:
   - CLI commands: `src/mybench/cli/`
   - Models: `src/mybench/models/`
   - Storage: `src/mybench/storage/`
   - Analysis: `src/mybench/analysis/`
   - Utilities: `src/mybench/utils/`
4. **Add tests**: Create tests in `tests/` for critical paths
5. **Follow code style**: Run linters and formatters
6. **Update documentation**: Add/update README.md if needed
7. **Submit pull request**

### Code Style Guidelines

- **Python version**: 3.11+
- **Type hints**: Use type hints for all functions
- **Docstrings**: Document all public functions and classes
- **Line length**: Maximum 79 characters
- **Testing**: Add tests for data integrity and analysis accuracy
- **Naming**: Use descriptive variable and function names

### Testing

Run tests before submitting:

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_models.py

# Run with coverage
uv run pytest --cov=mybench
````

## Project Principles

This project follows specific principles outlined in `.github/CONSTITUTION.md`:

1. **Working First**: Functionality over perfection
2. **Minimal Testing**: Test critical paths only (data integrity, analysis accuracy)
3. **Layered Small Modules**: Keep files small and focused
4. **Documentation First**: Documentation is a primary deliverable
5. **Simple Data Storage**: Human-readable JSON files in Git

## Review Process

1. **Submit Pull Request**: With clear description of changes
2. **Documentation Review**: Ensure documentation is clear and complete
3. **Code Review**: For code changes, ensure tests pass
4. **Merge**: After approval and successful CI checks

## Questions?

- **Documentation questions**: Open an issue with "documentation" label
- **Feature requests**: Open an issue with "enhancement" label
- **Bug reports**: Open an issue with "bug" label

## Getting Started

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/mybenchmarking.git
   cd mybenchmarking
   ```

2. **Set up development environment**:

   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install dependencies
   uv pip install -e ".[dev]"
   ```

3. **Run tests**:

   ```bash
   uv run pytest
   ```

4. **Try the CLI**:
   ```bash
   uv run mybench --help
   ```

## Thank You!

Your contributions help make server benchmarking more accessible to everyone. Thank you for taking the time to contribute!
