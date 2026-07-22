#!/usr/bin/env python3
"""
Heavy-Lifter Script for Knowledge Base Processing
Handles deterministic tasks:
- YAML frontmatter parsing & clean reconstruction
- HTML residual sanitization
- Heading hierarchy normalization
- Automated keyword density auto-tagging & category inference
- File routing from raw_imports to processed/ taxonomy folders
"""

import os
import re
import sys
import json
from pathlib import Path

# Ensure UTF-8 output encoding for cross-platform compatibility (e.g. Windows console)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

VALID_CATEGORIES = {'architecture', 'guides', 'reference', 'concepts', 'tooling', 'tutorials'}

CATEGORY_KEYWORDS = {
    "architecture": ["architecture", "design pattern", "microservices", "monolith", "module federation", "system design", "decoupled", "infrastructure"],
    "guides": ["how-to", "tutorial", "step-by-step", "getting started", "setup", "configuration", "install", "guide", "example"],
    "reference": ["api", "spec", "specification", "schema", "cheat sheet", "syntax", "endpoint", "reference", "documentation"],
    "concepts": ["overview", "understanding", "introduction", "what is", "paradigm", "concept", "fundamentals", "theory"],
    "tooling": ["webpack", "vite", "docker", "git", "cli", "devtools", "plugin", "npm", "linter"]
}

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

def sanitize_markdown_body(body):
    """Strips leftover HTML tags and cleans line endings."""
    cleaned = re.sub(r'</?(?:span|div|section|article|font|center)[^>]*>', '', body, flags=re.IGNORECASE)
    cleaned = cleaned.replace('&nbsp;', ' ')
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()

def infer_category_and_tags(title, description, body, existing_tags, existing_category=None):
    """Infers taxonomy category and enriches tag list based on keyword density."""
    if existing_category and str(existing_category).lower() in VALID_CATEGORIES and str(existing_category).lower() != "uncategorized":
        best_category = str(existing_category).lower()
    else:
        full_text = f"{title} {description} {body}".lower()
        scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                matches = len(re.findall(r'\b' + re.escape(kw) + r'\b', full_text))
                scores[cat] += matches
                
        best_category = max(scores, key=scores.get)
        if scores[best_category] == 0:
            best_category = "concepts"

    discovered_tags = set(existing_tags or [])
    full_text = f"{title} {description} {body}".lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in full_text and len(kw) > 3:
                discovered_tags.add(kw.replace(' ', '-'))
                
    return best_category, sorted(list(discovered_tags))

def rebuild_frontmatter(meta, category, tags, word_count, default_title):
    """Constructs clean YAML frontmatter block adhering to schema standards."""
    reading_time = max(1, round(word_count / 200))
    
    meta['title'] = meta.get('title') or default_title
    valid_types = ['article', 'concept', 'guide', 'reference', 'tutorial', 'spec']
    meta['type'] = meta.get('type') if meta.get('type') in valid_types else 'article'
    meta['description'] = meta.get('description') or f"Extracted knowledge base document on {meta['title']}"
    meta['source_url'] = meta.get('source_url') or 'https://knowledge.base/local-import'
    meta['date_scraped'] = meta.get('date_scraped') or '2026-07-22'
    meta['category'] = category
    meta['tags'] = tags
    meta['reading_time_min'] = meta.get('reading_time_min') or reading_time
    meta['status'] = 'normalized'
    meta['scaffold_version'] = meta.get('scaffold_version') or '1.0.0'
    
    yaml_lines = ['---']
    for k, v in meta.items():
        if isinstance(v, list):
            yaml_lines.append(f"{k}:")
            for item in v:
                escaped_item = str(item).replace('"', '\\"')
                yaml_lines.append(f'  - "{escaped_item}"')
        elif isinstance(v, int):
            yaml_lines.append(f"{k}: {v}")
        else:
            val_str = str(v).replace('"', '\\"')
            yaml_lines.append(f'{k}: "{val_str}"')
    yaml_lines.append('---')
    return '\n'.join(yaml_lines)

def process_file(file_path, output_dir):
    """Processes a single raw import markdown file."""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File {file_path} not found.")
        return None
    if not path.is_file():
        print(f"Error: Path {file_path} is not a file.")
        return None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    meta, raw_body = parse_frontmatter(content)
    body = sanitize_markdown_body(raw_body)
    
    default_title = path.stem.replace('-', ' ').title()
    title = meta.get('title', default_title)
    description = meta.get('description', '')
    existing_tags = meta.get('tags', [])
    existing_category = meta.get('category', None)
    
    word_count = len(body.split())
    category, tags = infer_category_and_tags(title, description, body, existing_tags, existing_category)
    
    # Ensure H1 header exists if missing
    if not body.startswith('# '):
        body = f"# {title}\n\n{body}"
        word_count = len(body.split())

    frontmatter = rebuild_frontmatter(meta, category, tags, word_count, default_title)
    full_document = f"{frontmatter}\n\n{body}\n"
    
    target_category_dir = Path(output_dir) / category
    target_category_dir.mkdir(parents=True, exist_ok=True)
    
    slug = path.stem
    target_file = target_category_dir / f"{slug}.md"
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(full_document)
        
    summary = {
        "source_file": str(path),
        "target_file": str(target_file),
        "title": title,
        "category": category,
        "tags_count": len(tags),
        "word_count": word_count,
        "status": "normalized"
    }
    return summary

def collect_target_files(arg_path, raw_imports_dir):
    files = []
    if arg_path:
        path = Path(arg_path)
        if not path.exists():
            print(f"Error: Target path '{arg_path}' does not exist.")
            return []
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(list(path.rglob('*')))
    else:
        files.extend(list(raw_imports_dir.rglob('*')))

    valid_files = []
    for f in files:
        if not f.is_file():
            continue
        if f.name.lower() in ['index.md', 'readme.md', '.gitkeep']:
            continue
        if any(part.startswith('.') for part in f.parts):
            continue
        # Process files ending with .md or .markdown
        if f.suffix.lower() in ['.md', '.markdown']:
            valid_files.append(f)

    return sorted(valid_files)

def main():
    base_dir = Path('.').resolve()
    raw_imports_dir = base_dir / 'scaffold' / 'raw_imports'
    processed_dir = base_dir / 'scaffold' / 'processed'
    
    arg_path = sys.argv[1] if len(sys.argv) > 1 else None
    target_files = collect_target_files(arg_path, raw_imports_dir)

    print(f"⚙️ Running Heavy-Lifter on {len(target_files)} raw import(s)...")
    results = []
    
    for f in target_files:
        res = process_file(f, processed_dir)
        if res:
            results.append(res)
            print(f"  ✅ Processed: {f.name} -> {res['category']}/{Path(res['target_file']).name}")

    print("\n📊 Heavy-Lifter Summary:")
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()

