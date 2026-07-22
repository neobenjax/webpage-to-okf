// JavaScript for Knowledge Base Studio Dashboard

let devtoolsSnippetText = '';

// Load DevTools Extractor Snippet text
async function loadSnippet() {
  try {
    const res = await fetch('./devtools-snippet/extractor.js');
    if (res.ok) {
      devtoolsSnippetText = await res.text();
    } else {
      devtoolsSnippetText = `// Run in Chrome DevTools Console\n(function() { console.log("DevTools Extractor Ready"); })();`;
    }
  } catch (e) {
    devtoolsSnippetText = `// Chrome DevTools Extractor Script\n(function extract() { console.log("Run script from devtools-snippet/extractor.js"); })();`;
  }
  document.getElementById('snippet-code-display').textContent = devtoolsSnippetText;
}

function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(panel => panel.classList.remove('active'));

  const activeBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
  if (activeBtn) activeBtn.classList.add('active');

  const panel = document.getElementById(`tab-${tabId}`);
  if (panel) panel.classList.add('active');
}

function copySnippetCode() {
  const text = devtoolsSnippetText;
  navigator.clipboard.writeText(text).then(() => {
    const btnText = document.getElementById('copy-btn-text');
    btnText.textContent = 'Copied!';
    setTimeout(() => {
      btnText.textContent = 'Copy Script';
    }, 2000);
  });
}

function runLiveConverter() {
  const input = document.getElementById('sandbox-input').value.trim();
  if (!input) {
    document.getElementById('sandbox-output').value = 'Please enter HTML or text in the input box above.';
    return;
  }

  // Basic conversion simulation
  let title = 'Sample Web Article';
  const h1Match = input.match(/<h1[^>]*>(.*?)<\/h1>/i);
  if (h1Match) title = h1Match[1].replace(/<[^>]+>/g, '').trim();

  let body = input
    .replace(/<h1[^>]*>(.*?)<\/h1>/gi, '\n# $1\n')
    .replace(/<h2[^>]*>(.*?)<\/h2>/gi, '\n## $1\n')
    .replace(/<h3[^>]*>(.*?)<\/h3>/gi, '\n### $1\n')
    .replace(/<p[^>]*>(.*?)<\/p>/gi, '\n$1\n')
    .replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1\n')
    .replace(/<[^>]+>/g, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  const today = new Date().toISOString().split('T')[0];
  const wordCount = body.split(/\s+/).length;

  const output = `---
title: "${title}"
description: "Converted live content snippet"
source_url: "https://example.com/sandbox-page"
domain: "example.com"
date_scraped: "${today}"
status: "raw_import"
category: "uncategorized"
tags:
  - "web-content"
  - "sandbox"
reading_time_min: ${Math.max(1, Math.ceil(wordCount / 200))}
---

# ${title}

${body}`;

  document.getElementById('sandbox-output').value = output;
}

// Sample default content for converter
document.addEventListener('DOMContentLoaded', () => {
  loadSnippet();
  const sampleInput = `<h1>Building Scalable Knowledge Bases</h1>
<p>Knowledge management requires standardized schemas and automated scraping pipelines. By combining DOM parsing with AI agent reasoning, technical teams can synthesize web content seamlessly.</p>
<h2>Key Principles</h2>
<ul>
  <li>Standardized YAML frontmatter for searchability</li>
  <li>Separation of heavy-lifting Python scripts and LLM cognitive curation</li>
  <li>Structured taxonomy folders</li>
</ul>`;
  document.getElementById('sandbox-input').value = sampleInput;
  runLiveConverter();
});
