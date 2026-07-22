# Task List: Fix Execution and Dependencies for webpage-to-okf Pipeline

## Overview
Address the execution failure when running `python3 skill/scripts/heavy_lifter.py .\scaffold\raw_imports\decoding_responsible_ai.md`. Fix Windows console UTF-8 Unicode encoding issues, verify Python standard library dependencies, test raw import processing, validate schema output, and document execution steps.

---

## Activities

- [x] **Task 1: Requirements & Dependency Specification**
  - [x] Inspect and document script dependencies (`heavy_lifter.py` and `validate_kb.py`).
  - [x] Create `requirements.txt` to clearly state Python version requirements and optional dependencies.

- [x] **Task 2: Fix Windows UTF-8 Unicode Encoding Bug in Python Scripts**
  - [x] Update `skill/scripts/heavy_lifter.py` with `sys.stdout.reconfigure(encoding='utf-8')` for cross-platform UTF-8 support.
  - [x] Update `skill/scripts/validate_kb.py` with `sys.stdout.reconfigure(encoding='utf-8')` for cross-platform UTF-8 support.

- [x] **Task 3: Execute Heavy-Lifter Automation on `decoding_responsible_ai.md`**
  - [x] Run `heavy_lifter.py` on `scaffold/raw_imports/decoding_responsible_ai.md`.
  - [x] Confirm file is processed and routed to `scaffold/processed/concepts/decoding_responsible_ai.md`.

- [x] **Task 4: Run Knowledge Base Schema Validation**
  - [x] Run `validate_kb.py` across all processed articles.
  - [x] Ensure zero schema errors and verify standard OKF YAML frontmatter compliance.

- [x] **Task 5: Walkthrough & User Review**
  - [x] Write detailed walkthrough guide detailing changes and manual testing instructions.
  - [x] Request user approval to stash, commit, push to `feature`, merge to `main`, and update versions/publish.

- [x] **Task 6: HTTP Server Troubleshooting & Cross-Platform Documentation**
  - [x] Analyze failure modes when running `python3 -m http.server 8000` on Windows vs POSIX (Linux/macOS).
  - [x] Document command resolution (`python` vs `python3`) and port collision troubleshooting in `README.md`.
  - [x] Verify local HTTP server execution and asset serving (`index.html`, `styles.css`, `app.js`, `devtools-snippet/extractor.js`).

- [x] **Task 7: OKF Categorization, Indexing & Query Agent Skill Implementation**
  - [x] Build cross-platform `skill/scripts/kb_indexer.py` script for scanning KB folders, parsing frontmatter, calculating concept graphs, rendering `index.md`, and building `index.json`.
  - [x] Create `skill/SKILL_CATEGORIZE.md` governing the "categorize" workflow for scanning and indexing any specified KB folder into a dedicated collection directory.
  - [x] Create `skill/SKILL_QUERY.md` governing the "query" workflow for using the KB collection as the primary source of truth.
  - [x] Update master `skill/SKILL.md` to integrate both Categorize and Query Agent Skills.
  - [x] Test `kb_indexer.py` on `scaffold/processed` and verify `index.md` and `index.json` output in `scaffold/collections/`.
  - [x] Update `README.md` and `tasks/tasks.md` with new agent skill commands and usage.

- [x] **Task 8: Agent Skills Standards, Relative Paths & Collection Categorization Refactoring**
  - [x] Update `skill/scripts/kb_indexer.py` to create a dedicated collection directory (`scaffold/collections/<name>/`) without touching original input files, generating lowercase `index.md` and `index.json`.
  - [x] Eliminate all absolute paths across all scripts, skill files, and documentation in favor of relative paths.
  - [x] Standardize `skill/SKILL_CATEGORIZE.md`, `skill/SKILL_QUERY.md`, and `skill/SKILL.md` following https://agentskills.io standards for composable and independent execution.
  - [x] Run full validation tests and verify zero absolute routes or uppercase `INDEX.md` remain.

- [x] **Task 9: Decoupled & Portable Agent Skills Architecture (https://agentskills.io Best Practices)**
  - [x] Create `skills/index-categorize-okf-bundle/` containing `SKILL.md` and `scripts/kb_indexer.py`.
  - [x] Create `skills/ingest-curate-okf-kb/` containing `SKILL.md`, `scripts/heavy_lifter.py`, and `scripts/validate_kb.py`.
  - [x] Create `skills/query-okf-source-of-truth/` containing `SKILL.md`.
  - [x] Remove legacy single `skill/` directory.
  - [x] Update `README.md`, `app.js`, `index.html`, and `tasks/tasks.md` to reference the new decoupled `skills/` architecture.
  - [x] Test script execution from all decoupled skill folders across Windows/POSIX environments.

- [x] **Task 10: Refactor index-categorize-okf-bundle for root `knowledge-catalog/` Copy & Index Generation**
  - [x] Update `skills/index-categorize-okf-bundle/scripts/kb_indexer.py` to copy input KB structure & files into `knowledge-catalog/<collection_name>/`.
  - [x] Generate self-contained `index.md` and `index.json` in `knowledge-catalog/<collection_name>/` referencing copied files with internal relative paths.
  - [x] Update `skills/index-categorize-okf-bundle/SKILL.md` instructions detailing collection identification, copying, and catalog summary output.
  - [x] Clean up legacy `scaffold/collections/` directory.
  - [x] Update `README.md` and `tasks/tasks.md` with new `knowledge-catalog/` commands and architecture.
  - [x] Test end-to-end collection indexing on `scaffold/processed` and verify output.

- [x] **Task 11: Refactor Agent Skills to `.agents/skills/` Directory Standard**
  - [x] Move `skills/` directory to `.agents/skills/` following Agents' Skills best practices.
  - [x] Update path references across `.agents/skills/*/SKILL.md` skill instructions and Python scripts.
  - [x] Update `README.md` workflow steps, commands, and repository structure tree.
  - [x] Verify Knowledge Base validation (`validate_kb.py`) and collection indexing (`kb_indexer.py`).
