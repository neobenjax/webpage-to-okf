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
4. Copy the entire contents of [`devtools-snippet/extractor.js`](file:///root/workstation/webinfo_to_knowledge-basd/devtools-snippet/extractor.js).
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
python3 skill/scripts/heavy_lifter.py
```

#### Run on a specific raw import file:
```bash
python3 skill/scripts/heavy_lifter.py scaffold/raw_imports/building-scalable-systems.md
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
Load the [`skill/SKILL.md`](file:///root/workstation/webinfo_to_knowledge-basd/skill/SKILL.md) skill into your AI Agent (e.g., Google Antigravity / AGY / AI Assistant) to perform high-level cognitive curation:

1. **Executive Summary**: Add an engaging blockquote summary at the top (`> [!NOTE] Summary: ...`).
2. **Key Takeaways**: Create a bulleted section under `## Key Takeaways` highlighting 3-5 core takeaways.
3. **Header Hierarchy & Polish**: Ensure logical heading levels (`# Title` -> `## Section` -> `### Sub-section`) and convert vague titles into descriptive headings.
4. **Callout Enhancement**: Convert standard notes/warnings into GitHub Flavored Markdown alerts (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`).
5. **Cross-Referencing & Semantic Tags**: Elevate auto-generated tags into standardized domain keywords and add references.

---

### Step 5 — Schema Validation & Quality Gate 🔍
Run the Knowledge Base validation script to verify 100% compliance against the JSON schema and quality rules:

```bash
python3 skill/scripts/validate_kb.py
```

#### Validation Rules Checked:
- ✅ Mandatory YAML frontmatter fields present (`title`, `type`, `description`, `source_url`, `date_scraped`, `status`, `category`, `tags`).
- ✅ `type` matches valid OKF types (`article`, `concept`, `guide`, `reference`, `tutorial`, `spec`).
- ✅ `category` matches valid taxonomy folders (`architecture`, `concepts`, `guides`, `reference`, `tooling`, `tutorials`).
- ✅ Body text starts with an `# H1` header and contains > 30 words.

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
└── skill/
    ├── SKILL.md                        # AI Agent Skill definition & instructions
    └── scripts/
        ├── heavy_lifter.py             # Python sanitization & auto-tagging script
        └── validate_kb.py              # Knowledge base schema validator
```

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

```bash
python3 -m http.server 8000
```
Open `http://localhost:8000` in your browser.
