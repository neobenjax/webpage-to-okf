# Knowledge Base Scaffold

Welcome to your structured Open Knowledge Base scaffold! This repository structure is designed for harvesting web content, organizing articles, and polishing them using AI Agent skills.

## Directory Structure

```text
scaffold/
├── raw_imports/          # 1. Paste raw DevTools scraped Markdown files here
├── processed/            # 2. Polished & categorized output files landed here
│   ├── architecture/     # System architecture & patterns
│   ├── concepts/         # Core definitions & conceptual overviews
│   ├── guides/           # How-to articles & tutorials
│   └── reference/        # Technical specifications & API refs
├── schema/               # JSON Schema for YAML frontmatter
│   └── frontmatter.schema.json
└── templates/            # Article formatting template
    └── article_template.md
```

## Workflow

1. **Scrape**: Open Chrome DevTools Console on any article, paste `devtools-snippet/extractor.js`, and hit Enter.
2. **Save**: Paste clipboard contents into `scaffold/raw_imports/<article-slug>.md`.
3. **Run Pipeline**: Invoke the Agent Skill or execute `python3 skill/scripts/heavy_lifter.py` to process, clean, auto-tag, and categorize raw imports into `scaffold/processed/`.
