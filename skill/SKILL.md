---
name: knowledge-base-curator
description: Turn raw webpage copy-pastes into a standardized, polished Knowledge Base using DevTools DOM extraction, Python heavy-lifting, and AI cognitive curation.
---

# Knowledge Base Curator Skill

This skill governs the complete workflow of extracting web content page-by-page, normalizing it into a Knowledge Base scaffold, and elevating raw articles into publication-ready knowledge artifacts.

## Architecture & Responsibilities

```
+--------------------------------------------------------+
| 1. Chrome DevTools JS Extractor (devtools-snippet)     |
|    - Converts DOM to Markdown & extracts meta tags     |
+--------------------------------------------------------+
                           |
                           v
+--------------------------------------------------------+
| 2. Raw Imports Landing (/scaffold/raw_imports/*.md)    |
|    - Target location for raw copy-pasted Markdown     |
+--------------------------------------------------------+
                           |
                           v
+--------------------------------------------------------+
| 3. Heavy-Lifter Script (skill/scripts/heavy_lifter.py)  |
|    - HTML cleanup & line normalization                 |
|    - Dynamic word count & reading time calculation     |
|    - Keyword auto-tagging & category inference         |
|    - Routing file to /scaffold/processed/<category>/   |
+--------------------------------------------------------+
                           |
                           v
+--------------------------------------------------------+
| 4. AI Agent Cognitive Thinking & Polishing             |
|    - Synthesizes Executive Summary & Key Takeaways     |
|    - Polishes ambiguous headers into clear concepts    |
|    - Generates semantic taxonomy & inter-links         |
|    - Validates schema compliance (validate_kb.py)      |
+--------------------------------------------------------+
```

---

## Agent Workflow Instructions

When the user asks you to process or refine Knowledge Base articles:

### Step 1: Execute Heavy-Lifter Script
Run the deterministic script to clean up raw imports and organize them into preliminary taxonomy folders:
```bash
python3 skill/scripts/heavy_lifter.py
```

### Step 2: Cognitive Polish & Taxonomy Alignment
Inspect the normalized files in `scaffold/processed/` and perform AI cognitive enrichment:
1. **Executive Summary**: Ensure every article has an engaging blockquote summary at the top (`> [!NOTE] Summary`).
2. **Key Takeaways**: Add a bulleted section under `## Key Takeaways` highlighting 3-5 critical concepts.
3. **Heading Hierarchy**: Ensure logical progression (`# Title` -> `## Major Topics` -> `### Sub-topics`).
4. **Code & Quote Callouts**: Convert standard quotes or notes into GitHub Flavored Markdown alerts (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`).
5. **Tag Refinement**: Review auto-generated tags and elevate them to standardized domain keywords.

### Step 3: Validation & Quality Gate
Run the validator script to ensure 100% compliance:
```bash
python3 skill/scripts/validate_kb.py
```

---

## Standardization Schema

All articles must strictly comply with `scaffold/schema/frontmatter.schema.json`:

```yaml
---
title: "Clean Article Title"
description: "High-level summary"
source_url: "https://example.com/source"
domain: "example.com"
date_scraped: "YYYY-MM-DD"
status: "published"
category: "architecture | concepts | guides | reference | tooling"
tags:
  - "tag-1"
  - "tag-2"
reading_time_min: 5
scaffold_version: "1.0.0"
---
```
