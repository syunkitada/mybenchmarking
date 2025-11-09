# Implementation Plan: Linux Server Benchmark Documentation Toolkit

**Date**: November 9, 2025 | **Spec**: `.specify/SPEC.md`  
**Input**: The application uses Python. Use uv.

## Summary

Build a documentation-centric toolkit for Linux server benchmarking that provides comprehensive guides for CPU, memory, disk, and network benchmark tools. The system stores benchmark results as JSON files in Git with separate system profiles for immutable hardware specs, enabling performance tracking across physical machines and VMs (including QEMU/KVM) with detailed configuration history. Primary focus is on usable documentation with simple file-based result storage for personal benchmark tracking.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**:

- Click (CLI framework) - industry standard for Python CLIs
- Pydantic v2 (data validation and JSON schema) - type-safe models with validation
- Rich (terminal formatting and tables) - beautiful CLI output
- PyYAML (optional config file support)

**Storage**: File-based JSON in Git repository

- `systems/*.json` - System profile files (immutable hardware specs, physical vs VM)
- `results/{category}/*.json` - Benchmark result files (timestamped, with mutable config)
- `docs/{category}/*.md` - Markdown documentation organized by benchmark category

**Testing**: pytest with minimal coverage (per constitution: test data integrity and analysis accuracy only)  
**Target Platform**: Linux (Ubuntu, Debian, RHEL, Fedora, CentOS)  
**Project Type**: Single CLI application with modular structure  
**Package Manager**: uv (modern, fast Python package installer and resolver)

**Performance Goals**:

- Result save/load operations < 1 second
- Query/filter 100+ results < 2 seconds
- JSON validation < 100ms

**Constraints**:

- Human-readable JSON (pretty-printed, 2-space indent)
- Git-friendly file formats (consistent formatting)
- No database dependencies (files only)
- Works completely offline
- Zero external tool dependencies for core functionality

**Scale/Scope**:

- Document 10+ commonly used benchmark tools
- Support 100+ saved benchmark results per category
- Handle 10+ system profiles (physical + VMs)
- 5-10 core CLI commands
- Documentation is primary deliverable

## Constitution Check

_GATE: Must pass before implementation. Based on `.github/CONSTITUTION.md`_

### ✅ 1. Working First - Functionality over perfection

**Compliance**: PASS

- Plan prioritizes MVP with basic documentation structure and JSON save/load
- Advanced analysis deferred to later phases
- Focuses on working prototypes: Phase 0-1 delivers usable system
- Avoids premature optimization

**Application**: Start with simplest file I/O, manual system profile creation, basic CLI commands. Add convenience features only after core works.

### ✅ 2. Minimal Testing - Strategic testing over comprehensive coverage

**Compliance**: PASS

- Testing focused on critical paths:
  - JSON schema validation (data integrity)
  - Result comparison accuracy (core analysis feature)
  - System profile reference integrity
- Explicitly skips trivial code (file I/O, formatting)
- Manual verification acceptable for documentation content

**Application**: ~3-5 test files covering models, storage integrity, comparison math. No tests for CLI glue code or output formatting.

### ✅ 3. Layered Small Modules - Composability over monolithic design

**Compliance**: PASS

- Clear separation: cli/ models/ storage/ analysis/ utils/
- Each module < 200 lines (target: 50-150 lines per file)
- Single responsibility per module
- Unidirectional dependencies: cli → storage/analysis → models

**Application**: 15-20 small files vs 3-4 large files. Easy to understand and modify individual pieces.

### ✅ 4. Documentation First - Clear, accessible documentation over automation

**Compliance**: PASS

- Documentation is literally the primary deliverable
- Phase 2 dedicated entirely to writing tool docs
- Copy-paste ready examples in every doc
- Interpretation guidance included
- Code exists to support doc workflow, not vice versa

**Application**: Write documentation for 10+ tools before building advanced analysis features. Documentation structure matters more than clever code.

### ✅ 5. Simple Data Storage - Human-readable files over databases

**Compliance**: PASS

- JSON files stored directly in repo
- Separate system profiles avoid duplication (DRY principle)
- Pretty-printed for GitHub readability
- No database, no complex storage layer
- Files are self-documenting with clear field names

**Application**: Plain `json.dump()` with `indent=2`. File naming convention: `YYYY-MM-DD_HHMMSS_tool.json`. No ORMs, no migrations, no complexity.

**GATE RESULT**: ✅ ALL CHECKS PASSED - Proceed with implementation

## Project Structure

### Documentation (this feature)

```text
.specify/
├── SPEC.md              # Feature specification (existing)
├── PLAN.md              # This file
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
└── memory/
    └── constitution.md  # Constitution memory
```

### Source Code (repository root)

```text
mybenchmarking/
├── pyproject.toml           # uv project configuration
├── uv.lock                  # uv dependency lockfile
├── README.md                # Project overview and quickstart
├── .gitignore               # Exclude __pycache__, .venv, etc.
├── .github/
│   └── CONSTITUTION.md      # Project principles (existing)
├── systems/                 # System profile storage
│   ├── .gitkeep
│   └── README.md            # How to create profiles
├── results/                 # Benchmark results storage
│   ├── cpu/
│   │   └── .gitkeep
│   ├── memory/
│   │   └── .gitkeep
│   ├── disk/
│   │   └── .gitkeep
│   └── network/
│       └── .gitkeep
├── docs/                    # Benchmark tool documentation
│   ├── cpu/
│   │   ├── sysbench.md
│   │   ├── stress-ng.md
│   │   └── ...
│   ├── memory/
│   │   ├── sysbench-memory.md
│   │   ├── mbw.md
│   │   └── ...
│   ├── disk/
│   │   ├── fio.md
│   │   ├── dd.md
│   │   └── ...
│   ├── network/
│   │   ├── iperf3.md
│   │   ├── netperf.md
│   │   └── ...
│   └── metrics/
│       ├── iops.md
│       ├── throughput.md
│       ├── latency.md
│       └── bandwidth.md
├── src/
│   └── mybench/             # Main package
│       ├── __init__.py      # Package version
│       ├── __main__.py      # CLI entry point (python -m mybench)
│       ├── cli/             # Command implementations
│       │   ├── __init__.py
│       │   ├── main.py      # Click command group
│       │   ├── system.py    # System profile commands
│       │   ├── save.py      # Save benchmark result
│       │   ├── list.py      # List results/systems
│       │   ├── show.py      # Show details
│       │   └── compare.py   # Compare results
│       ├── models/          # Pydantic data models
│       │   ├── __init__.py
│       │   ├── system.py    # SystemProfile + Hardware specs
│       │   ├── result.py    # BenchmarkResult
│       │   └── config.py    # SystemConfiguration (kernel, software)
│       ├── storage/         # File I/O layer
│       │   ├── __init__.py
│       │   ├── base.py      # Common file operations
│       │   ├── profiles.py  # System profile CRUD
│       │   └── results.py   # Result CRUD
│       ├── analysis/        # Analysis and comparison
│       │   ├── __init__.py
│       │   ├── compare.py   # Diff two results
│       │   └── trends.py    # Time-series analysis
│       └── utils/           # Utilities
│           ├── __init__.py
│           ├── detect.py    # Auto-detect system specs
│           └── format.py    # Rich formatting helpers
└── tests/
    ├── __init__.py
    ├── conftest.py          # pytest fixtures
    ├── test_models.py       # Pydantic validation tests
    ├── test_storage.py      # JSON integrity tests
    └── test_analysis.py     # Comparison accuracy tests
```

**Structure Decision**: Single project structure selected because:

- This is a CLI tool, not a web app (no frontend/backend split)
- All components run locally (no client/server architecture)
- File-based storage eliminates need for separate data layer
- Modular structure within single project provides sufficient organization
- Aligns with "Layered Small Modules" principle without over-engineering

## Complexity Tracking

> **Not applicable** - No constitution violations to justify.

All design decisions comply with constitution principles. Using standard patterns (CLI with Click, file-based JSON storage, small modules) with no added complexity.

---

## Phase 0: Outline & Research

### Unknowns to Research

1. **uv best practices**

   - How to structure pyproject.toml for uv
   - uv vs pip for dependency management
   - uv lock file management
   - uv in development vs production

2. **System detection techniques**

   - Cross-distro CPU/RAM/disk detection
   - VM vs physical detection methods
   - QEMU/KVM metadata extraction
   - Kernel parameter reading

3. **Pydantic v2 patterns**

   - JSON serialization best practices
   - Custom validators for nested models
   - Optional fields with defaults
   - Schema versioning strategies

4. **Click CLI patterns**

   - Multi-level command groups
   - Interactive prompts vs flags
   - Output formatting with Rich integration
   - Error handling and exit codes

5. **JSON file management**
   - Atomic writes for data integrity
   - File naming conventions for sortability
   - Directory traversal performance
   - Handling concurrent access (Git operations)

### Research Tasks

**Task 1: uv Project Setup**

- Research: uv documentation, pyproject.toml structure
- Evaluate: uv vs poetry vs pip-tools
- Outcome: Optimal uv configuration for this project

**Task 2: System Detection**

- Research: /proc filesystem, platform module, distro library
- Evaluate: psutil vs manual /proc parsing
- Outcome: Reliable cross-distro detection method

**Task 3: Pydantic Best Practices**

- Research: Pydantic v2 docs, JSON serialization
- Evaluate: model_dump() vs dict() patterns
- Outcome: Type-safe models with clean JSON output

**Task 4: CLI Design Patterns**

- Research: Click documentation, typer comparison
- Evaluate: Decorator vs imperative command definition
- Outcome: Intuitive command structure

**Task 5: File Storage Patterns**

- Research: JSON atomic writes, file locking
- Evaluate: Direct write vs temp-and-move
- Outcome: Safe concurrent file operations

**Output**: `research.md` with findings and decisions for all unknowns

---

## Phase 1: Design & Contracts

**Prerequisites**: research.md complete

### Data Model Design

Extract entities from SPEC.md and design complete data models in `data-model.md`:

**Core Entities**:

1. **SystemProfile** - Immutable hardware specs

   - Physical machine specs (CPU, RAM, disk, network)
   - Virtual machine specs (hypervisor, vcpu, topology)
   - Unique profile_id for referencing

2. **BenchmarkResult** - Single benchmark run

   - References SystemProfile by ID
   - Contains mutable SystemConfiguration
   - Stores benchmark parameters and results

3. **SystemConfiguration** - Mutable system state

   - Kernel version and parameters
   - Software versions
   - Environment variables

4. **Hardware Specifications** - Physical/virtual hardware

   - CPU details (model, cores, clock)
   - Memory details (size, type, speed)
   - Disk details (model, type, capacity)
   - Network details (interface, speed)

5. **Virtualization Specs** - VM-specific metadata
   - Hypervisor type (QEMU/KVM)
   - Host system reference
   - CPU topology and pinning
   - Hugepages configuration

### API Contracts

Since this is a file-based system with CLI interface, "contracts" are:

1. **File Schema Contracts** (JSON schemas in `/contracts/`):

   - `system-profile.schema.json` - System profile structure
   - `benchmark-result.schema.json` - Result file structure
   - `schema-version-1.0.md` - Human-readable schema docs

2. **CLI Command Contracts** (in `quickstart.md`):

   - Command signatures
   - Input/output formats
   - Exit codes
   - Error messages

3. **File Naming Conventions** (in `data-model.md`):
   - System profiles: `{profile-id}.json`
   - Results: `{YYYY-MM-DD}_{HHMMSS}_{tool}.json`
   - Categories: cpu/, memory/, disk/, network/

### Agent Context Update

After generating data-model.md and contracts:

- Run `.specify/scripts/bash/update-agent-context.sh copilot`
- Add Python + uv + Click + Pydantic + Rich to technology context
- Update with project structure and module organization
- Preserve any manual additions between markers

**Output**:

- `data-model.md` - Complete entity descriptions with relationships
- `contracts/` - JSON schemas and CLI contract docs
- `quickstart.md` - Quick start guide with examples
- Updated agent context file

---

## Re-evaluation: Constitution Check Post-Design

**To be performed after Phase 1 completion:**

1. **Working First**: Verify Phase 0-1 delivers minimal working system
2. **Minimal Testing**: Confirm test scope limited to critical paths
3. **Layered Small Modules**: Check module count and file sizes
4. **Documentation First**: Validate docs are prioritized
5. **Simple Data Storage**: Ensure no complexity creep in storage layer

**Expected Result**: All gates remain PASS. If violations emerge, document justification in Complexity Tracking table.

---

## Next Steps

This plan document (PLAN.md) establishes the foundation. To proceed:

1. ✅ **Phase 0**: Generate `research.md` by researching all unknowns listed above
2. ⏳ **Phase 1**: Generate `data-model.md`, `contracts/`, and `quickstart.md`
3. ⏳ **Phase 1**: Update agent context with technology stack
4. ⏳ **Phase 2**: Generate detailed `tasks.md` with `/speckit.tasks` command
5. ⏳ **Implementation**: Begin coding based on tasks.md

**Command ends here** - Report: Plan complete at `.specify/PLAN.md`. Ready for Phase 0 research generation.
