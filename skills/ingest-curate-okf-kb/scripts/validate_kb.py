#!/usr/bin/env python3
"""
Knowledge Base Validation Script
Validates all articles in scaffold/processed/ against schema compliance and quality rules.
Self-contained script suitable for portable execution.
"""

import sys
import re
import json
from pathlib import Path

# Ensure UTF-8 output encoding for cross-platform compatibility (e.g. Windows console)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def parse_frontmatter(content):
    """Extracts YAML frontmatter block and markdown body."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return {}, content.strip()
    raw_yaml, body = match.group(1), match.group(2)
    meta = {}
    current_key = None
    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('- ') and current_key:
            val = line[2:].strip().strip('"').strip("'")
            if current_key not in meta or not isinstance(meta[current_key], list):
                meta[current_key] = []
            meta[current_key].append(val)
        elif ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.startswith('[') and val.endswith(']'):
                items = [i.strip().strip('"').strip("'") for i in val[1:-1].split(',')]
                meta[key] = items
            elif val.isdigit():
                meta[key] = int(val)
            else:
                meta[key] = val
            current_key = key
    return meta, body.strip()

def validate_article(path):
    errors = []
    warnings = []
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    meta, body = parse_frontmatter(content)
    
    required_keys = ['title', 'type', 'description', 'source_url', 'date_scraped', 'status', 'category', 'tags']
    for key in required_keys:
        if key not in meta or not meta[key]:
            errors.append(f"Missing required frontmatter key: '{key}'")

    valid_types = ['article', 'concept', 'guide', 'reference', 'tutorial', 'spec']
    if meta.get('type') not in valid_types:
        errors.append(f"Invalid type '{meta.get('type')}'. Must be one of: {valid_types}")

    valid_categories = ['concepts', 'guides', 'reference', 'architecture', 'tutorials', 'tooling']
    if meta.get('category') not in valid_categories:
        errors.append(f"Invalid category '{meta.get('category')}'. Must be one of: {valid_categories}")

    if len(body.split()) < 30:
        warnings.append("Article body is under 30 words (potentially empty or corrupted import).")

    if not body.startswith('# '):
        warnings.append("Article body does not start with an H1 header (# Title).")

    return {
        "file": str(path),
        "title": meta.get('title', 'Unknown'),
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def main():
    base_dir = Path('.').resolve()
    processed_dir = base_dir / 'scaffold' / 'processed'

    if not processed_dir.exists():
        print(f"Error: Processed directory '{processed_dir}' does not exist.")
        sys.exit(1)

    files = [f for f in processed_dir.rglob('*.md') if f.name.lower() not in ['index.md', 'readme.md']]
    print(f"🔍 Validating {len(files)} Knowledge Base article(s)...")

    all_valid = True
    for f in files:
        report = validate_article(f)
        rel_path = str(f.relative_to(base_dir)).replace('\\', '/')
        if report['valid']:
            print(f"  ✅ {rel_path} - Valid! ({len(report['warnings'])} warnings)")
        else:
            all_valid = False
            print(f"  ❌ {rel_path} - INVALID:")
            for err in report['errors']:
                print(f"     - {err}")
        for warn in report['warnings']:
            print(f"     ⚠️  {warn}")

    if not all_valid:
        sys.exit(1)

if __name__ == '__main__':
    main()
