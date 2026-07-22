#!/usr/bin/env python3
"""
Knowledge Base Validation Script
Validates all articles in scaffold/processed/ against schema compliance and quality rules.
"""

import sys
import json
from pathlib import Path
from heavy_lifter import parse_frontmatter

def validate_article(path):
    errors = []
    warnings = []
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    meta, body = parse_frontmatter(content)
    
    # Required frontmatter keys
    required_keys = ['title', 'description', 'source_url', 'date_scraped', 'status', 'category', 'tags']
    for key in required_keys:
        if key not in meta or not meta[key]:
            errors.append(f"Missing required frontmatter key: '{key}'")

    # Category validation
    valid_categories = ['concepts', 'guides', 'reference', 'architecture', 'tutorials', 'tooling']
    if meta.get('category') not in valid_categories:
        errors.append(f"Invalid category '{meta.get('category')}'. Must be one of: {valid_categories}")

    # Body length check
    if len(body.split()) < 30:
        warnings.append("Article body is under 30 words (potentially empty or corrupted import).")

    # Header check
    if not body.startswith('# '):
        warnings.append("Article body does not start with an H1 header (# Title).")

    return {
        "file": str(path.relative_to(path.parents[2])),
        "title": meta.get('title', 'Unknown'),
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

def main():
    base_dir = Path(__file__).resolve().parent.parent.parent
    processed_dir = base_dir / 'scaffold' / 'processed'

    files = list(processed_dir.rglob('*.md'))
    print(f"🔍 Validating {len(files)} Knowledge Base article(s)...")

    all_valid = True
    for f in files:
        report = validate_article(f)
        if report['valid']:
            print(f"  ✅ {report['file']} - Valid! ({len(report['warnings'])} warnings)")
        else:
            all_valid = False
            print(f"  ❌ {report['file']} - INVALID:")
            for err in report['errors']:
                print(f"     - {err}")
        for warn in report['warnings']:
            print(f"     ⚠️  {warn}")

    if not all_valid:
        sys.exit(1)

if __name__ == '__main__':
    main()
