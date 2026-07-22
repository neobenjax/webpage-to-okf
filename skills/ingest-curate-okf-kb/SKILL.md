---
name: ingest-curate-okf-kb
description: Ingest raw webpage Markdown copy-pastes, sanitize HTML, auto-tag and route to OKF taxonomy folders, and validate schema compliance.
---

# OKF Ingestion & Curation Skill

This self-contained skill handles the complete workflow of taking raw web content copy-pastes, cleaning HTML residual artifacts, auto-calculating word metrics, inferring OKF taxonomy categories, routing articles to taxonomy folders, and enforcing JSON schema compliance.

---

## 🎯 Skill Trigger
Activate this skill whenever the user explicitly asks to **"ingest"**, **"curate"**, **"sanitize"**, **"route"**, or **"validate"** raw webpage Markdown imports.

---

## ⚙️ Execution Instructions

### Step 1: Run Heavy-Lifter Automation
Execute the heavy lifter script to clean up raw imports and organize them into preliminary taxonomy folders:
```bash
python skills/ingest-curate-okf-kb/scripts/heavy_lifter.py [optional_raw_import_file]
```
*Example (All raw imports):*
```bash
python skills/ingest-curate-okf-kb/scripts/heavy_lifter.py
```
*Example (Single raw import):*
```bash
python skills/ingest-curate-okf-kb/scripts/heavy_lifter.py scaffold/raw_imports/article.md
```

### Step 2: Validate Schema & Quality Gate
Run the validator script to enforce 100% compliance against `scaffold/schema/frontmatter.schema.json`:
```bash
python skills/ingest-curate-okf-kb/scripts/validate_kb.py
```

---

## 📂 Responsibilities & Output Locations

- **Raw Imports Directory**: `scaffold/raw_imports/`
- **Processed Taxonomy Folders**:
  - `scaffold/processed/architecture/`
  - `scaffold/processed/concepts/`
  - `scaffold/processed/guides/`
  - `scaffold/processed/reference/`
  - `scaffold/processed/tooling/`
  - `scaffold/processed/tutorials/`
