---
name: query-okf-source-of-truth
description: Source-of-Truth Knowledge Base Query Skill. Instructs AI Agents to check the root knowledge-catalog/<collection_name>/ index first before answering user queries.
---

# OKF Knowledge Base Query & Source-of-Truth Skill

This self-contained skill mandates that the AI Agent **always check the root `knowledge-catalog/` collections FIRST** as its primary source of truth whenever a user asks a question or queries information related to topics covered in the Knowledge Base.

---

## 🎯 Skill Trigger
Activate this skill whenever the user:
- Asks a question about topics present in the Knowledge Base (e.g. Responsible AI, Micro-Frontends, Ethics, System Architecture, OKF schemas).
- Explicitly asks to **"query"**, **"search"**, or **"consult"** the Knowledge Base.

---

## 🛑 Primary Constraint: Source-of-Truth Rule
> [!IMPORTANT]
> **DO NOT** generate answers from general LLM pre-training memory or external web search without inspecting the Knowledge Base first. The Knowledge Base articles indexed in `knowledge-catalog/` or `scaffold/processed/` are the authoritative source of truth.

---

## 🔍 Step-by-Step Retrieval Protocol

### Step 1: Consult the Collection Index Map
Before answering, inspect the collection index files in `knowledge-catalog/<collection_name>/`:
1. **Machine-Readable Search**: Read `index.json` in the active collection folder (e.g. `knowledge-catalog/decoding-responsible-ai-collection/index.json`) to perform fast keyword, category, or tag matching across document titles, descriptions, and concept relationship edges (`concept_edges`).
2. **Human Index Navigation**: View `index.md` in the active collection folder to see the complete catalog and concept cross-references.

### Step 2: Read Matched Knowledge Base Articles
Using the relative file paths found in `index.json` / `index.md` (e.g. `knowledge-catalog/decoding-responsible-ai-collection/architecture/classifying_ai_ethics_dilemmas_by_cause.md`), inspect target `.md` files using `view_file`.

### Step 3: Ground Answer in Knowledge Base Content
Construct your response strictly using empirical facts, definitions, and guidelines extracted from the Knowledge Base articles.

### Step 4: Cite Sources with Relative File Links
Always include relative Markdown file links and section references to the underlying source documents in your final response:
- Example: `According to [Decoding Responsible AI](knowledge-catalog/decoding-responsible-ai-collection/concepts/decoding_responsible_ai_intro.md#L19), ...`

---

## 💡 Example Query Workflow

**User Query**: *"What are the core ethical principles for Responsible AI?"*

1. **Agent Action**: Read `knowledge-catalog/decoding-responsible-ai-collection/index.json` and search for `"ethics"` or `"principles"`.
2. **Result**: Matched `knowledge-catalog/decoding-responsible-ai-collection/concepts/principles_for_trust_and_transparency.md`.
3. **Agent Action**: Call `view_file` on `knowledge-catalog/decoding-responsible-ai-collection/concepts/principles_for_trust_and_transparency.md`.
4. **Agent Response**: Provide a synthesized answer with relative file links and exact citations.
