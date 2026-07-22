# Task: Refactor Agent Skills to `.agents/skills/` Standard

- [x] **Task 1: Task Tracking & Feature Branch Setup**
  - [x] Create feature branch `feature/agents-skills-refactoring`.
  - [x] Create task tracking file `tasks/move_skills_to_agents_tasks.md`.

- [x] **Task 2: Codebase Reference & Path Updates**
  - [x] Update `.agents/skills/index-categorize-okf-bundle/SKILL.md` command examples and path references to `.agents/skills/`.
  - [x] Update `.agents/skills/index-categorize-okf-bundle/scripts/kb_indexer.py` string header note to `.agents/skills/index-categorize-okf-bundle/scripts/kb_indexer.py`.
  - [x] Update `.agents/skills/ingest-curate-okf-kb/SKILL.md` command examples and path references to `.agents/skills/`.
  - [x] Update `README.md` command examples, links, and directory tree to `.agents/skills/`.
  - [x] Update `tasks/tasks.md` historical task log references if applicable.

- [x] **Task 3: Verification & Execution Testing**
  - [x] Run `python .agents/skills/ingest-curate-okf-kb/scripts/validate_kb.py` to verify Knowledge Base validation.
  - [x] Run `python .agents/skills/index-categorize-okf-bundle/scripts/kb_indexer.py scaffold/processed decoding-responsible-ai-collection` to verify catalog indexing.
  - [x] Verify generated index content references `.agents/skills/`.

- [x] **Task 4: User Walkthrough & Manual Testing Guide**
  - [x] Prepare detailed walkthrough guide with summary of changes and manual test steps.
  - [x] Request user review and approval before proceeding with git commit, push, merge, versioning, and publishing.

- [x] **Task 5: Git Sync, Versioning (`v0.0.1`), & Branch Cleanup**
  - [x] Commit and push changes to `feature/agents-skills-refactoring`.
  - [x] Ask user for merge approval.
  - [x] Merge into `main`, set version tag `v0.0.1`, push to GitHub, and purge `feature/agents-skills-refactoring`.
