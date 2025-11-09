# Tasks: Linux Server Benchmark Documentation Toolkit

**Input**: Design documents from `.specify/`  
**Prerequisites**: PLAN.md, SPEC.md, research.md

**Tests**: Per constitution ("Minimal Testing"), tests are ONLY for critical paths: JSON validation, storage integrity, and comparison accuracy.

**Organization**: Tasks grouped by user story (US1-US5) to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

- [x] T001 Initialize uv project with pyproject.toml in repository root
- [x] T002 Create directory structure: src/mybench/, systems/, results/{cpu,memory,disk,network}/, docs/{cpu,memory,disk,network,metrics}/, tests/
- [x] T003 [P] Configure .gitignore for Python (**pycache**, _.pyc, .venv/, _.egg-info)
- [x] T004 [P] Add README.md files to systems/ and results/ explaining structure
- [x] T005 [P] Install dependencies via uv: click, pydantic, rich

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models and utilities that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create Pydantic models for HardwareSpecs (CPU, memory, disk, network) in src/mybench/models/system.py
- [x] T007 Create Pydantic models for VirtualizationSpecs (hypervisor, vcpu, topology) in src/mybench/models/system.py
- [x] T008 Create SystemProfile model (physical/virtual, hardware, virtualization) in src/mybench/models/system.py
- [x] T009 Create KernelConfig model (version, parameters, governor) in src/mybench/models/config.py
- [x] T010 Create SystemConfiguration model (os, kernel, software, environment) in src/mybench/models/config.py
- [x] T011 Create BenchmarkResult model (schema_version, timestamp, category, tool, system_profile_id, configuration, results) in src/mybench/models/result.py
- [x] T012 [P] Implement atomic JSON save function in src/mybench/storage/base.py
- [x] T013 [P] Implement JSON load with validation in src/mybench/storage/base.py
- [x] T014 [P] Create system detection utilities (/proc parsing) in src/mybench/utils/detect.py
- [x] T015 Create Click command group structure in src/mybench/cli/main.py with version option

**Test for Foundational (Critical Path)**:

- [x] T016 Test Pydantic model validation with valid and invalid data in tests/test_models.py
- [x] T017 Test atomic JSON save/load integrity in tests/test_storage.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Comprehensive Benchmark Documentation (Priority: P1) 🎯 MVP

**Goal**: Create organized documentation for 10+ benchmark tools across 4 categories with installation instructions, usage examples, and interpretation guidance.

**Independent Test**: Browse docs/ directory on GitHub and verify each category has multiple tool docs with copy-paste examples.

### Implementation for User Story 1

- [x] T018 [P] [US1] Create sysbench CPU documentation in docs/cpu/sysbench.md with installation, usage examples, and interpretation
- [x] T019 [P] [US1] Create stress-ng CPU documentation in docs/cpu/stress-ng.md with installation, usage examples, and interpretation
- [x] T020 [P] [US1] Create sysbench memory documentation in docs/memory/sysbench-memory.md with installation, usage examples, and interpretation
- [x] T021 [P] [US1] Create mbw memory documentation in docs/memory/mbw.md with installation, usage examples, and interpretation
- [x] T022 [P] [US1] Create fio disk documentation in docs/disk/fio.md with installation, usage examples, and interpretation
- [x] T023 [P] [US1] Create dd disk documentation in docs/disk/dd.md with installation, usage examples, and interpretation
- [x] T024 [P] [US1] Create bonnie++ disk documentation in docs/disk/bonnie++.md with installation, usage examples, and interpretation
- [x] T025 [P] [US1] Create iperf3 network documentation in docs/network/iperf3.md with installation, usage examples, and interpretation
- [x] T026 [P] [US1] Create netperf network documentation in docs/network/netperf.md with installation, usage examples, and interpretation
- [x] T027 [P] [US1] Create IOPS metric documentation in docs/metrics/iops.md with definition and typical values
- [x] T028 [P] [US1] Create throughput metric documentation in docs/metrics/throughput.md with definition and typical values
- [x] T029 [P] [US1] Create latency metric documentation in docs/metrics/latency.md with definition and typical values
- [x] T030 [P] [US1] Create bandwidth metric documentation in docs/metrics/bandwidth.md with definition and typical values
- [x] T031 [P] [US1] Create main README.md in docs/ with navigation to all categories and tools

**Checkpoint**: User Story 1 complete - Documentation is browsable and contains 10+ tools with examples

---

## Phase 4: User Story 2 - Personal Benchmark Result Storage (Priority: P1) 🎯 MVP

**Goal**: Enable saving benchmark results as JSON files with system profile references, supporting both physical and virtual machines.

**Independent Test**: Create a system profile, save a benchmark result referencing it, commit to Git, verify files are human-readable on GitHub.

### Implementation for User Story 2

- [x] T032 [US2] Implement save_system_profile() in src/mybench/storage/profiles.py using atomic write
- [x] T033 [US2] Implement load_system_profile() in src/mybench/storage/profiles.py with validation
- [x] T034 [US2] Implement list_system_profiles() in src/mybench/storage/profiles.py
- [x] T035 [US2] Implement save_benchmark_result() in src/mybench/storage/results.py using atomic write with timestamp filename
- [x] T036 [US2] Implement load_benchmark_result() in src/mybench/storage/results.py with validation
- [x] T037 [US2] Implement list_benchmark_results() in src/mybench/storage/results.py with category filter
- [x] T038 [US2] Create 'mybench system create' command in src/mybench/cli/system.py with interactive prompts for profile creation
- [x] T039 [US2] Create 'mybench system list' command in src/mybench/cli/system.py with Rich table output
- [x] T040 [US2] Create 'mybench system show <id>' command in src/mybench/cli/system.py with detailed display
- [x] T041 [US2] Create 'mybench save' command in src/mybench/cli/save.py with interactive prompts (category, tool, system_profile_id, label, configuration, results)
- [x] T042 [US2] Create 'mybench list' command in src/mybench/cli/list.py with filters (--system, --category, --label) and Rich table output
- [x] T043 [US2] Create 'mybench show <result-id>' command in src/mybench/cli/show.py with full result display
- [x] T044 [US2] Add auto-directory creation to storage functions (systems/, results/{category}/)

**Test for User Story 2 (Critical Path)**:

- [x] T045 [US2] Test system profile save/load with data integrity verification in tests/test_storage.py
- [x] T046 [US2] Test benchmark result save/load with profile reference validation in tests/test_storage.py
- [x] T047 [US2] Test file naming convention and sortability in tests/test_storage.py

**Checkpoint**: User Story 2 complete - Can create profiles and save results via CLI, files are Git-friendly

---

## Phase 5: User Story 3 - Result Analysis and Visualization (Priority: P2)

**Goal**: Analyze and visualize benchmark results to understand performance trends and identify changes.

**Independent Test**: Save multiple results for a system over time, run compare/trend commands, verify output shows performance deltas.

### Implementation for User Story 3

- [x] T048 [P] [US3] Implement calculate_delta() function in src/mybench/analysis/compare.py for percentage differences
- [x] T049 [P] [US3] Implement compare_results() function in src/mybench/analysis/compare.py returning comparison dict
- [x] T050 [US3] Implement detect_config_changes() in src/mybench/analysis/compare.py to identify configuration differences
- [x] T051 [US3] Implement generate_trend_data() in src/mybench/analysis/compare.py for time-series aggregation
- [x] T052 [US3] Create 'mybench compare <id1> <id2>' command in src/mybench/cli/compare.py with Rich table showing deltas
- [x] T053 [US3] Add --config flag to 'mybench compare' to highlight configuration changes
- [x] T054 [US3] Create 'mybench trend <system-id>' command in src/mybench/cli/compare.py showing performance over time
- [x] T055 [US3] Add --category filter to 'mybench trend' command
- [x] T056 [P] [US3] Implement format_comparison_table() in src/mybench/utils/format.py using Rich tables
- [x] T057 [P] [US3] Implement format_trend_output() in src/mybench/utils/format.py using Rich tables

**Test for User Story 3 (Critical Path)**:

- [ ] T058 [US3] Test calculate_delta() accuracy with known values (<1% error) in tests/test_analysis.py
- [ ] T059 [US3] Test compare_results() with different metrics in tests/test_analysis.py
- [ ] T060 [US3] Test detect_config_changes() identifies kernel parameter differences in tests/test_analysis.py

**Checkpoint**: User Story 3 complete - Can compare results and see performance trends with accurate calculations

---

## Phase 6: User Story 4 - Metric Interpretation Guidance (Priority: P2)

**Goal**: Enhance documentation with interpretation guidance to help users understand benchmark metrics.

**Independent Test**: View any tool documentation and verify it includes metric definitions with typical values and interpretation tips.

### Implementation for User Story 4

- [ ] T061 [P] [US4] Add "Metrics Explained" section to docs/cpu/sysbench.md with events_per_second interpretation
- [ ] T062 [P] [US4] Add "Metrics Explained" section to docs/cpu/stress-ng.md with operations_per_second interpretation
- [ ] T063 [P] [US4] Add "Metrics Explained" section to docs/memory/sysbench-memory.md with bandwidth interpretation
- [ ] T064 [P] [US4] Add "Metrics Explained" section to docs/disk/fio.md with IOPS, bandwidth, latency interpretation
- [ ] T065 [P] [US4] Add "Metrics Explained" section to docs/disk/dd.md with throughput interpretation
- [ ] T066 [P] [US4] Add "Metrics Explained" section to docs/network/iperf3.md with bandwidth, jitter interpretation
- [ ] T067 [P] [US4] Add "Typical Values" section to docs/metrics/iops.md with SSD vs HDD vs NVMe comparisons
- [ ] T068 [P] [US4] Add "Typical Values" section to docs/metrics/throughput.md with disk/network type comparisons
- [ ] T069 [P] [US4] Add "Typical Values" section to docs/metrics/latency.md with acceptable ranges
- [ ] T070 [P] [US4] Add "Interpretation Guide" section to each metric doc explaining when values are good/poor
- [ ] T071 [P] [US4] Create docs/interpretation.md with general guidance on reading benchmark results
- [ ] T072 [US4] Add links from tool docs to relevant metric definitions

**Checkpoint**: User Story 4 complete - Documentation includes comprehensive interpretation guidance

---

## Phase 7: User Story 5 - Tool Installation and Setup Guides (Priority: P3)

**Goal**: Provide distribution-specific installation instructions for all documented benchmark tools.

**Independent Test**: Follow installation instructions for a tool on a fresh system and verify it installs successfully.

### Implementation for User Story 5

- [ ] T073 [P] [US5] Add Ubuntu/Debian installation section to docs/cpu/sysbench.md
- [ ] T074 [P] [US5] Add RHEL/Fedora installation section to docs/cpu/sysbench.md
- [ ] T075 [P] [US5] Add Ubuntu/Debian installation section to docs/cpu/stress-ng.md
- [ ] T076 [P] [US5] Add RHEL/Fedora installation section to docs/cpu/stress-ng.md
- [ ] T077 [P] [US5] Add Ubuntu/Debian installation section to docs/memory/mbw.md (compile from source)
- [ ] T078 [P] [US5] Add Ubuntu/Debian installation section to docs/disk/fio.md
- [ ] T079 [P] [US5] Add RHEL/Fedora installation section to docs/disk/fio.md
- [ ] T080 [P] [US5] Add Ubuntu/Debian installation section to docs/disk/bonnie++.md
- [ ] T081 [P] [US5] Add Ubuntu/Debian installation section to docs/network/iperf3.md
- [ ] T082 [P] [US5] Add RHEL/Fedora installation section to docs/network/iperf3.md
- [ ] T083 [P] [US5] Add prerequisites section to each tool doc listing dependencies
- [ ] T084 [US5] Create docs/installation-guide.md with general Linux package management tips

**Checkpoint**: User Story 5 complete - All tools have complete installation instructions

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that enhance the overall toolkit

- [x] T085 [P] Add 'mybench system detect' command in src/mybench/cli/system.py for auto-detecting current system
- [x] T086 [P] Implement auto-detect current system configuration in src/mybench/utils/detect.py (kernel, software versions)
- [ ] T087 [P] Add --export json/csv option to 'mybench list' command for data export
- [x] T088 [P] Add color coding to comparison output (green=improvement, red=regression) in format.py
- [x] T089 [P] Improve error messages with actionable next steps throughout CLI commands
- [x] T090 [P] Add input validation with helpful error messages to all CLI prompts
- [x] T091 Create project README.md with quickstart guide and example workflow
- [x] T092 Add usage examples to README.md showing common workflows
- [ ] T093 [P] Create CONTRIBUTING.md with instructions for adding new tool documentation
- [ ] T094 Add shell completion support (optional) for bash/zsh
- [x] T095 Final review: ensure all JSON files are pretty-printed with consistent formatting

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately ✅
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories ⚠️
- **User Stories (Phase 3-7)**: All depend on Foundational completion
  - US1 (Documentation) - Independent, can start after Phase 2
  - US2 (Storage) - Independent, can start after Phase 2
  - US3 (Analysis) - Depends on US2 (needs stored results)
  - US4 (Interpretation) - Depends on US1 (enhances existing docs)
  - US5 (Installation) - Depends on US1 (adds to existing docs)
- **Polish (Phase 8)**: Depends on US1-US3 minimum

### User Story Dependencies

- **US1 (P1)**: Independent - can start after Foundational ✅
- **US2 (P1)**: Independent - can start after Foundational ✅
- **US3 (P2)**: Requires US2 complete (needs stored results to analyze) ⚠️
- **US4 (P2)**: Requires US1 complete (enhances documentation) ⚠️
- **US5 (P3)**: Requires US1 complete (adds to documentation) ⚠️

### Parallel Opportunities

**Setup Phase**:

- T003, T004, T005 can run in parallel

**Foundational Phase**:

- T006-T011 (models) can run in parallel
- T012-T014 (utilities) can run in parallel after models
- T016-T017 (tests) can run in parallel after implementation

**User Story 1** (All tasks can run in parallel):

- T018-T030 (all documentation files) - independent files
- T031 (main README) after others complete

**User Story 2**:

- T032-T034 (profiles) in sequence
- T035-T037 (results) in sequence
- T038-T043 (CLI commands) can run in parallel after storage layer
- T045-T047 (tests) can run in parallel after implementation

**User Story 3**:

- T048-T049 (compare functions) can run in parallel
- T052-T055 (CLI commands) can run in parallel after functions
- T056-T057 (formatting) can run in parallel
- T058-T060 (tests) can run in parallel after implementation

**User Story 4** (All tasks can run in parallel):

- T061-T072 (documentation enhancements) - independent files

**User Story 5** (All tasks can run in parallel):

- T073-T084 (installation instructions) - independent sections

**Polish Phase**:

- T085-T090 (enhancements) can run in parallel
- T091-T095 (documentation) can run in parallel

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. ✅ Complete Phase 1: Setup
2. ✅ Complete Phase 2: Foundational (CRITICAL - blocks everything)
3. ✅ Complete Phase 3: User Story 1 (Documentation) - Can work in parallel
4. ✅ Complete Phase 4: User Story 2 (Storage) - Can work in parallel
5. **STOP and VALIDATE**:
   - Documentation is browsable with 10+ tools
   - Can create profiles and save results
   - Files are human-readable on GitHub
6. **MVP READY** - Core value delivered!

### Incremental Delivery

1. **Foundation** (Phases 1-2) → Project structure and models ready
2. **MVP** (Phases 3-4) → Documentation + Storage = Core value ✅
3. **Enhanced** (+Phase 5) → Add analysis and comparison features
4. **Complete** (+Phases 6-7) → Add interpretation and installation guides
5. **Polished** (+Phase 8) → Convenience features and refinements

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers after Foundational phase:

**Sprint 1** (MVP):

- **Developer A**: User Story 1 (T018-T031) - Documentation
- **Developer B**: User Story 2 (T032-T047) - Storage & CLI

**Sprint 2** (Enhanced):

- **Developer A**: User Story 3 (T048-T060) - Analysis
- **Developer B**: User Story 4 (T061-T072) - Interpretation

**Sprint 3** (Complete):

- **Developer A**: User Story 5 (T073-T084) - Installation
- **Developer B**: Phase 8 (T085-T095) - Polish

---

## Summary Statistics

- **Total Tasks**: 95
- **Setup**: 5 tasks
- **Foundational**: 12 tasks (including 2 tests)
- **User Story 1** (P1): 14 tasks (all parallelizable)
- **User Story 2** (P1): 16 tasks (including 3 tests)
- **User Story 3** (P2): 13 tasks (including 3 tests)
- **User Story 4** (P2): 12 tasks (all parallelizable)
- **User Story 5** (P3): 12 tasks (all parallelizable)
- **Polish**: 11 tasks

**MVP Scope**: Phases 1-4 = 47 tasks (Setup + Foundational + US1 + US2)

**Test Coverage**: 8 critical path tests (per constitution: test data integrity, validation, and comparison accuracy only)

**Parallel Opportunities**: 65 tasks marked [P] can run in parallel when dependencies allow

**Independent Deliverables**: Each user story can be tested independently and provides standalone value
