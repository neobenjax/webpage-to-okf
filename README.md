# Webpage to OKF Knowledge Base Pipeline 🚀

A comprehensive, production-grade toolchain and workflow designed to extract webpage content directly from Chrome Developer Tools, format it into standardized **Open Knowledge Foundation (OKF)** YAML frontmatter Markdown files, organize them into a ready-to-work scaffold, and curate them using Python automation and AI Agent skills.

---

## 🏗️ Architecture & Pipeline Overview

```mermaid
flowgraph TD
    A[Webpage in Browser] -->|Run devtools-snippet/extractor.js| B[Raw Markdown + Frontmatter]
    B -->|Paste & Save| C[scaffold/raw_imports/*.md]
    C --> D[heavy_lifter.py Script]
    subgraph Automation & AI Curation
        D -->|HTML Sanitization, Metrics, Auto-Tagging, Routing| E[scaffold/processed/category/*.md]
        E --> F[AI Agent Skill - SKILL.md]
        F -->|Executive Summaries, Key Takeaways, Header Polish| G[Polished OKF Article]
    end
    G --> H[validate_kb.py Schema Gate]
```

---

## 📖 Comprehensive Step-by-Step User Workflow

Follow this complete step-by-step guide to convert any webpage into a standardized, polished Knowledge Base article.

### Step 1 — Extract Page Content in Chrome DevTools 🌐
1. Open the target webpage in Google Chrome.
2. Open Chrome Developer Tools:
   - **Windows / Linux**: Press `F12` or `Ctrl + Shift + I`
   - **macOS**: Press `Cmd + Option + I`
3. Click on the **Console** tab.
4. Copy the entire contents of [`devtools-snippet/extractor.js`](devtools-snippet/extractor.js).
5. Paste the script into the DevTools Console and press `Enter`.

#### What Happens Behind the Scenes:
- **DOM Extraction**: Automatically locates the primary article container (`<main>`, `<article>`, `#content`, or `.article-body`) and strips non-content elements (navigation bars, headers, footers, advertisements, sidebars, scripts).
- **Markdown Conversion**: Converts DOM elements (`<h1>-<h6>`, `<p>`, `<ul>/<ol>`, `<table>`, `<code>/<pre>`, `<a>`, `<img>`) into clean Markdown formatting.
- **OKF Metadata Harvesting**: Extracts page metadata to build standardized YAML Frontmatter, including mandatory OKF fields:
  - `title`: Extracted title.
  - `type`: Mandatory OKF artifact type (defaults to `"article"`).
  - `description`: Meta description or article summary.
  - `source_url`: Canonical URL of the webpage.
  - `domain`: Origin domain name.
  - `date_scraped`: Current date in ISO format (`YYYY-MM-DD`).
  - `status`: Set to `"raw_import"`.
  - `category`: Set to `"uncategorized"`.
  - `tags`: Inferred tags from URL path and domain.
  - `reading_time_min`: Calculated reading duration.
- **Auto Clipboard Copy**: The output is logged to the console and **automatically copied to your clipboard** (`copy()`).

---

### Step 2 — Save into Scaffold Raw Imports 📁
1. Open your code editor and navigate to the project directory.
2. Create a new `.md` file inside `scaffold/raw_imports/` using a descriptive slug name (e.g., `scaffold/raw_imports/building-scalable-systems.md`).
3. Paste your clipboard content into the newly created file and save it.

---

### Step 3 — Execute Heavy-Lifter Automation ⚙️
Run the Python heavy-lifter script to sanitize, calculate word counts, infer taxonomy categories, auto-generate tags, and route the file into its respective topic folder.

#### Run on all raw imports:
```bash
python .agents/skills/ingest-curate-okf-kb/scripts/heavy_lifter.py
```

#### Run on a specific raw import file:
```bash
python .agents/skills/ingest-curate-okf-kb/scripts/heavy_lifter.py scaffold/raw_imports/building-scalable-systems.md
```

#### Heavy-Lifter Responsibilities:
- **HTML Sanitization**: Removes lingering inline HTML tags, style attributes, and unwanted line breaks.
- **OKF Type Enforcement**: Ensures the mandatory `type` key is present (`article`, `concept`, `guide`, `reference`, `tutorial`, `spec`).
- **Keyword Density Auto-Categorization**: Analyzes word frequencies to categorize the article into:
  - `architecture/`: System design, patterns, microservices, infrastructure.
  - `concepts/`: Overview articles, definitions, theoretical foundations.
  - `guides/`: Tutorials, step-by-step instructions, how-to articles.
  - `reference/`: API specifications, schemas, syntax docs.
  - `tooling/`: Build tools, CLI frameworks, Docker, Git.
- **Taxonomy Routing**: Moves the normalized draft to `scaffold/processed/<category>/<article-slug>.md` with `status: "normalized"`.

---

### Step 4 — AI Agent Skill Cognitive Polish 🧠
Load the [`.agents/skills/ingest-curate-okf-kb/SKILL.md`](.agents/skills/ingest-curate-okf-kb/SKILL.md) skill into your AI Agent (e.g., Google Antigravity / AGY / AI Assistant) to perform high-level cognitive curation:

1. **Executive Summary**: Add an engaging blockquote summary at the top (`> [!NOTE] Summary: ...`).
2. **Key Takeaways**: Create a bulleted section under `## Key Takeaways` highlighting 3-5 core takeaways.
3. **Header Hierarchy & Polish**: Ensure logical heading levels (`# Title` -> `## Section` -> `### Sub-section`) and convert vague titles into descriptive headings.
4. **Callout Enhancement**: Convert standard notes/warnings into GitHub Flavored Markdown alerts (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`).
5. **Cross-Referencing & Semantic Tags**: Elevate auto-generated tags into standardized domain keywords and add references.

---

### Step 5 — Schema Validation & Quality Gate 🔍
Run the Knowledge Base validation script to verify 100% compliance against the JSON schema and quality rules:

```bash
python .agents/skills/ingest-curate-okf-kb/scripts/validate_kb.py
```

#### Validation Rules Checked:
- ✅ Mandatory YAML frontmatter fields present (`title`, `type`, `description`, `source_url`, `date_scraped`, `status`, `category`, `tags`).
- ✅ `type` matches valid OKF types (`article`, `concept`, `guide`, `reference`, `tutorial`, `spec`).
- ✅ `category` matches valid taxonomy folders (`architecture`, `concepts`, `guides`, `reference`, `tooling`, `tutorials`).
- ✅ Body text starts with an `# H1` header and contains > 30 words.

---

### Step 6 — OKF Categorization & Collection Indexing 📚
Instruct your AI Agent to **"categorize"**, **"index"**, or **"organize"** a Knowledge Base directory (e.g., `"Organize the knowledge base in scaffold/processed as decoding-responsible-ai-collection"`).

```bash
python .agents/skills/index-categorize-okf-bundle/scripts/kb_indexer.py scaffold/processed decoding-responsible-ai-collection
```

#### What Happens Behind the Scenes:
1. **Copies Structure & Files**: Copies all subdirectories and markdown files into `knowledge-catalog/<collection_name>/` at the project root.
2. **Generates Collection Index**: Creates `index.md` and `index.json` inside `knowledge-catalog/<collection_name>/` referencing the copied files with internal relative links (`architecture/...`, `concepts/...`, `guides/...`).
3. **Leaves Source Intact**: The original files in `scaffold/processed/` remain untouched.

---

### Step 7 — AI Agent Source of Truth Querying 🤖
Instruct your AI Agent to **"query"** the Knowledge Base when asking domain questions. The Agent Skill [`.agents/skills/query-okf-source-of-truth/SKILL.md`](.agents/skills/query-okf-source-of-truth/SKILL.md) enforces the **Source-of-Truth Rule**:
1. AI Agent checks `index.json` / `index.md` in `knowledge-catalog/<collection_name>/` **first**.
2. Retrieves matching Markdown documents via relative file paths.
3. Formats responses grounded directly in Knowledge Base content with clickable relative file citations.

---

## 📂 Repository Structure

```text
webpage-to-okf/
├── README.md                           # Master workflow & documentation
├── index.html                          # Interactive Web Dashboard Studio
├── styles.css                          # Modern Dark Theme CSS
├── app.js                              # Dashboard interactive logic
├── devtools-snippet/
│   └── extractor.js                    # Chrome DevTools Console DOM Scraper
├── knowledge-catalog/                  # 3. Root Organized Knowledge Collections
│   └── decoding-responsible-ai-collection/
│       ├── index.md                    # Generated human-readable master index catalog
│       ├── index.json                  # Generated machine-readable index & concept graph
│       ├── architecture/               # Copied collection documents
│       ├── concepts/
│       └── guides/
├── scaffold/
│   ├── README.md                       # Scaffold guide
│   ├── raw_imports/                    # 1. Landing directory for raw scraped .md files
│   │   └── sample_scraped_article.md
│   ├── processed/                      # 2. Curated & categorized Knowledge Base
│   │   ├── architecture/
│   │   ├── concepts/
│   │   ├── guides/
│   │   ├── reference/
│   │   └── tooling/
│   ├── schema/
│   │   └── frontmatter.schema.json     # JSON Schema for OKF YAML Frontmatter
│   └── templates/
│       └── article_template.md         # Markdown article template
└── .agents/
    └── skills/                         # Decoupled & Portable Agent Skills
        ├── index-categorize-okf-bundle/
        │   ├── SKILL.md                # Categorization & Indexing Agent Skill
        │   └── scripts/
        │       └── kb_indexer.py       # Standalone KB indexer & collection copier
        ├── ingest-curate-okf-kb/
        │   ├── SKILL.md                # Web page extraction & curation Agent Skill
        │   └── scripts/
        │       ├── heavy_lifter.py     # Standalone HTML sanitization & router script
        │       └── validate_kb.py      # Standalone schema validator script
        └── query-okf-source-of-truth/
            └── SKILL.md                # Source of Truth Query Agent Skill
```,StartLine:114,TargetContent:

---

## 📜 OKF Standard Frontmatter Specification

Every document in the Knowledge Base strictly adheres to `scaffold/schema/frontmatter.schema.json`:

```yaml
---
title: "Understanding Micro-Frontend Architectures"
type: "article"                            # MANDATORY: article | concept | guide | reference | tutorial | spec
description: "Comprehensive deep dive into micro-frontend decoupling."
source_url: "https://example.com/posts/micro-frontend"
domain: "example.com"
date_scraped: "2026-07-22"
status: "published"                        # raw_import | normalized | reviewed | published
category: "architecture"                   # architecture | concepts | guides | reference | tooling
tags:
  - "micro-frontend"
  - "webpack"
reading_time_min: 4
scaffold_version: "1.0.0"
---
```

---

## 🌐 Interactive Dashboard Studio

Launch the local interactive Web Studio to test the browser snippet, preview live HTML-to-Markdown conversions, and inspect the scaffold visually:

### Running the Local Web Server

- **Windows**:
  ```bash
  python -m http.server 8000
  ```
- **macOS / Linux**:
  ```bash
  python3 -m http.server 8000
  ```

Open `http://localhost:8000` in your web browser.

#### 🔧 Troubleshooting HTTP Server Issues:
1. **`python3` command not recognized on Windows**:
   - On Windows, Python is usually invoked via `python` or `py`. Use `python -m http.server 8000`.
2. **Port 8000 in use (`OSError: [Errno 10048] / Address already in use`)**:
   - Run on an alternative port: `python -m http.server 8080` (or `python3 -m http.server 8080`).
3. **CORS errors when opening `index.html` directly**:
   - Avoid opening `file:///path/to/index.html` directly in the browser. Using the local HTTP server (`http://localhost:8000`) allows `fetch('./devtools-snippet/extractor.js')` to load properly.

