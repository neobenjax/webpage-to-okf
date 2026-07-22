---
name: index-categorize-okf-bundle
description: Copy structure & markdown files from an input KB directory into a root knowledge-catalog/<collection_name>/ folder, then generate self-contained index.md and index.json catalogs with internal relative links.
---

# OKF Knowledge Base Categorization & Indexing Skill

This self-contained skill handles automated collection naming, file copying, taxonomy categorization, concept cross-linking, and catalog index generation for any Knowledge Base directory adhering to Open Knowledge Foundation (OKF) conventions.

---

## 🎯 Skill Trigger
Activate this skill whenever the user explicitly asks to **"categorize"**, **"index"**, or **"organize"** a Knowledge Base directory (e.g. `scaffold/processed` or a custom folder path).

*Example User Prompts:*
- *"Organize the knowledge base in the `scaffold/processed` folder as it is part of a collection about decoding responsible ai."*
- *"Categorize and index the articles in `scaffold/processed`."*

---

## ⚙️ AI Agent & Script Workflow Instructions

When triggered:

### Step 1: Identify Collection Name & Folder Path
1. Identify the custom source directory path containing OKF Markdown files (e.g. `scaffold/processed`).
2. Identify or infer a descriptive collection name from the user prompt or domain content (e.g., `decoding-responsible-ai-collection`).

### Step 2: Run the Indexer & Catalog Copy Script
Execute the script located inside this skill bundle, passing the source directory and collection name:
```bash
python .agents/skills/index-categorize-okf-bundle/scripts/kb_indexer.py <source_directory> [collection_name]
```
*Example:*
```bash
python .agents/skills/index-categorize-okf-bundle/scripts/kb_indexer.py scaffold/processed decoding-responsible-ai-collection
```

#### What the Script Executed Behind the Scenes:
1. **Copies Files**: Copies all subdirectories and `.md` files from `scaffold/processed/` into `knowledge-catalog/<collection_name>/` at the project root.
2. **Generates Index**: Creates `index.md` and `index.json` directly inside `knowledge-catalog/<collection_name>/`.
3. **Internal Relative Links**: All links inside `index.md` and `index.json` point to the copied internal files (`architecture/...`, `concepts/...`, `guides/...`).
4. **Source Files Intact**: Leaves source files in `scaffold/processed/` untouched.

### Step 3: Present Summary to User
Print a comprehensive summary detailing:
- Identified collection name & output catalog path (`knowledge-catalog/<collection_name>/`).
- Total copied articles & category breakdown.
- Links to `index.md` and `index.json`.

---

## 📂 OKF Taxonomy Standard

Documents copied into `knowledge-catalog/<collection_name>/` are categorized into standard OKF taxonomy folders:

| Category | Subdirectory Path | Description |
| :--- | :--- | :--- |
| **`architecture`** | `architecture/` | System design, patterns, microservices, decoupling, infrastructure |
| **`concepts`** | `concepts/` | High-level overviews, theoretical foundations, ethical principles, definitions |
| **`guides`** | `guides/` | Step-by-step how-to tutorials, walkthroughs, setup guides |
| **`reference`** | `reference/` | API specs, JSON schemas, syntax docs, cheat sheets |
| **`tooling`** | `tooling/` | Build tools, CLI frameworks, Docker, Git, linters |
| **`tutorials`** | `tutorials/` | End-to-end learning modules and instructional walkthroughs |
