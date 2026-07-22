#!/usr/bin/env python3
"""
OKF Knowledge Base Collection Indexer & Categorizer Script
Cross-platform tool to:
1. Copy all structure and markdown files from an input Knowledge Base directory into a root `knowledge-catalog/<collection_name>/` folder.
2. Scan copied files, extract YAML frontmatter, compute concept cross-links.
3. Generate self-contained human-readable `index.md` and machine-readable `index.json` inside the collection folder using internal relative links.
"""

import os
import re
import sys
import json
import shutil
from datetime import datetime
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

VALID_CATEGORIES = ['architecture', 'concepts', 'guides', 'reference', 'tooling', 'tutorials', 'uncategorized']

def create_kb_collection_index(input_dir, collection_name=None):
    base_dir = Path('.').resolve()
    input_path = Path(input_dir).resolve()
    
    if not input_path.exists() or not input_path.is_dir():
        print(f"Error: Input directory '{input_dir}' does not exist or is not a directory.")
        sys.exit(1)

    # Infer collection name if omitted
    if not collection_name:
        collection_name = f"{input_path.name}-collection"
    
    # Destination collection directory in root knowledge-catalog/
    collection_dir = base_dir / 'knowledge-catalog' / collection_name
    collection_dir.mkdir(parents=True, exist_ok=True)

    print(f"📋 Initializing Knowledge Catalog Collection: '{collection_name}'...")
    print(f"  📥 Source Directory: '{input_path.relative_to(base_dir)}'")
    print(f"  📁 Target Catalog Directory: '{collection_dir.relative_to(base_dir)}'")

    # Step 1: Copy structure and markdown files to collection_dir
    copied_count = 0
    for src_file in input_path.rglob('*.md'):
        if src_file.name.lower() in ['index.md', 'readme.md']:
            continue
        rel_from_input = src_file.relative_to(input_path)
        dest_file = collection_dir / rel_from_input
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dest_file)
        copied_count += 1

    print(f"  ✅ Copied {copied_count} file(s) into '{collection_dir.relative_to(base_dir)}'")

    # Step 2: Scan copied markdown files inside collection_dir
    md_files = [f for f in collection_dir.rglob('*.md') if f.name.lower() not in ['index.md', 'readme.md']]

    documents = {}
    categories_map = {cat: [] for cat in VALID_CATEGORIES}
    tag_cloud = {}

    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  ⚠️ Warning: Could not read {file_path}: {e}")
            continue

        meta, body = parse_frontmatter(content)
        
        # Internal relative path inside collection_dir
        rel_inside_collection = str(file_path.relative_to(collection_dir)).replace('\\', '/')
        title = meta.get('title', file_path.stem.replace('-', ' ').title())
        category = meta.get('category', 'uncategorized')
        if category not in VALID_CATEGORIES:
            category = 'uncategorized'

        tags = meta.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]

        word_count = len(body.split())
        reading_time = meta.get('reading_time_min', max(1, round(word_count / 200)))

        doc_info = {
            "id": file_path.stem,
            "title": title,
            "type": meta.get('type', 'article'),
            "description": meta.get('description', ''),
            "source_url": meta.get('source_url', ''),
            "domain": meta.get('domain', ''),
            "date_scraped": meta.get('date_scraped', ''),
            "status": meta.get('status', 'normalized'),
            "category": category,
            "tags": tags,
            "reading_time_min": reading_time,
            "word_count": word_count,
            "relative_path": rel_inside_collection,
            "body_snippet": body[:300].replace('\n', ' ')
        }

        documents[rel_inside_collection] = doc_info
        categories_map[category].append(doc_info)

        for tag in tags:
            tag_slug = tag.lower().strip()
            if tag_slug not in tag_cloud:
                tag_cloud[tag_slug] = {"tag": tag, "count": 0, "articles": []}
            tag_cloud[tag_slug]["count"] += 1
            tag_cloud[tag_slug]["articles"].append({"title": title, "path": rel_inside_collection})

    # Step 3: Build concept cross-link network graph
    concept_edges = []
    doc_paths = list(documents.keys())

    for i in range(len(doc_paths)):
        for j in range(i + 1, len(doc_paths)):
            doc1 = documents[doc_paths[i]]
            doc2 = documents[doc_paths[j]]

            shared_tags = set(doc1['tags']).intersection(set(doc2['tags']))
            if shared_tags:
                concept_edges.append({
                    "source": doc1['relative_path'],
                    "target": doc2['relative_path'],
                    "source_title": doc1['title'],
                    "target_title": doc2['title'],
                    "relationship": "shared_tags",
                    "details": list(shared_tags)
                })

            if doc1['title'].lower() in doc2['body_snippet'].lower():
                concept_edges.append({
                    "source": doc2['relative_path'],
                    "target": doc1['relative_path'],
                    "source_title": doc2['title'],
                    "target_title": doc1['title'],
                    "relationship": "concept_mention",
                    "details": doc1['title']
                })
            elif doc2['title'].lower() in doc1['body_snippet'].lower():
                concept_edges.append({
                    "source": doc1['relative_path'],
                    "target": doc2['relative_path'],
                    "source_title": doc1['title'],
                    "target_title": doc2['title'],
                    "relationship": "concept_mention",
                    "details": doc2['title']
                })

    active_categories = {k: v for k, v in categories_map.items() if len(v) > 0}

    # Step 4: Machine-readable index.json
    index_json_data = {
        "collection_name": collection_name,
        "generated_at": datetime.now().isoformat(),
        "source_directory": str(input_path.relative_to(base_dir)).replace('\\', '/'),
        "catalog_directory": str(collection_dir.relative_to(base_dir)).replace('\\', '/'),
        "total_documents": len(documents),
        "categories_count": len(active_categories),
        "tags_count": len(tag_cloud),
        "categories": active_categories,
        "tag_cloud": tag_cloud,
        "concept_edges": concept_edges,
        "documents": documents
    }

    json_index_path = collection_dir / 'index.json'
    with open(json_index_path, 'w', encoding='utf-8') as f:
        json.dump(index_json_data, f, indent=2)
    print(f"  ✅ Generated machine-readable index: {json_index_path.relative_to(base_dir)}")

    # Step 5: Render human-readable index.md
    index_md_lines = [
        f"# Knowledge Base Collection Index: {collection_name} 📚",
        "",
        "> [!NOTE]",
        "> This collection index was automatically generated by `skills/index-categorize-okf-bundle/scripts/kb_indexer.py`. All validated documents have been copied into this self-contained collection folder.",
        "",
        "## 📊 Collection Overview",
        f"- **Collection Name**: `{collection_name}`",
        f"- **Source Directory**: `{input_path.relative_to(base_dir)}`",
        f"- **Catalog Path**: `{collection_dir.relative_to(base_dir)}`",
        f"- **Total Articles**: {len(documents)}",
        f"- **Active Categories**: {len(active_categories)}",
        f"- **Unique Concept Tags**: {len(tag_cloud)}",
        f"- **Last Indexed**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "## 📁 Category Navigation",
    ]

    for cat in sorted(active_categories.keys()):
        index_md_lines.append(f"- [{cat.title()} (#{len(active_categories[cat])})](#-{cat})")

    index_md_lines.extend(["", "---", ""])

    for cat, docs in sorted(active_categories.items()):
        index_md_lines.append(f"### 📂 {cat.title()}")
        index_md_lines.append("")
        for doc in docs:
            tag_str = ", ".join([f"`{t}`" for t in doc['tags']]) if doc['tags'] else "*None*"
            index_md_lines.append(f"#### 📄 [{doc['title']}]({doc['relative_path']})")
            index_md_lines.append(f"- **Type**: `{doc['type']}` | **Reading Time**: {doc['reading_time_min']} min | **Word Count**: {doc['word_count']}")
            if doc['description']:
                index_md_lines.append(f"- **Description**: {doc['description']}")
            index_md_lines.append(f"- **Tags**: {tag_str}")
            if doc['source_url']:
                index_md_lines.append(f"- **Source**: [{doc['domain'] or 'Original Link'}]({doc['source_url']})")

            related_links = []
            for edge in concept_edges:
                if edge['source'] == doc['relative_path']:
                    related_links.append(f"[{edge['target_title']}]({edge['target']}) ({', '.join(edge['details']) if isinstance(edge['details'], list) else edge['details']})")
                elif edge['target'] == doc['relative_path']:
                    related_links.append(f"[{edge['source_title']}]({edge['source']}) ({', '.join(edge['details']) if isinstance(edge['details'], list) else edge['details']})")

            if related_links:
                unique_related = list(set(related_links))
                index_md_lines.append(f"- **Related Concepts**: {'; '.join(unique_related)}")

            index_md_lines.append("")

    index_md_lines.extend([
        "---",
        "",
        "## 🏷️ Concept & Tag Cloud",
        ""
    ])

    for tag_slug, tag_data in sorted(tag_cloud.items()):
        art_links = [f"[{a['title']}]({a['path']})" for a in tag_data['articles']]
        index_md_lines.append(f"- **`{tag_data['tag']}`** ({tag_data['count']}): {', '.join(art_links)}")

    index_md_lines.extend([
        "",
        "---",
        "",
        "## 🤖 AI Agent Source of Truth Instruction",
        "When querying topics covered in this knowledge base collection:",
        "1. Load `index.json` or read `index.md` in this collection folder to identify relevant concepts.",
        "2. Follow relative article links to retrieve exact source content.",
        "3. Ground all answers directly in the indexed Markdown documents.",
        ""
    ])

    index_md_path = collection_dir / 'index.md'
    with open(index_md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_md_lines))
    print(f"  ✅ Generated human-readable index: {index_md_path.relative_to(base_dir)}")

    summary = {
        "collection_name": collection_name,
        "source_directory": str(input_path.relative_to(base_dir)).replace('\\', '/'),
        "catalog_directory": str(collection_dir.relative_to(base_dir)).replace('\\', '/'),
        "total_documents": len(documents),
        "json_index": str(json_index_path.relative_to(base_dir)).replace('\\', '/'),
        "markdown_index": str(index_md_path.relative_to(base_dir)).replace('\\', '/'),
        "categories_breakdown": {cat: len(docs) for cat, docs in active_categories.items()}
    }

    print("\n📊 Knowledge Catalog Summary:")
    print(json.dumps(summary, indent=2))
    return summary

def main():
    base_dir = Path('.').resolve()
    default_input = base_dir / 'scaffold' / 'processed'

    input_dir = sys.argv[1] if len(sys.argv) > 1 else str(default_input)
    collection_name = sys.argv[2] if len(sys.argv) > 2 else None

    create_kb_collection_index(input_dir, collection_name)

if __name__ == '__main__':
    main()
