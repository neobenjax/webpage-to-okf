/**
 * Chrome DevTools Extractor Script
 * Converts any webpage into clean Markdown with standardized YAML Frontmatter.
 * 
 * Usage:
 * 1. Open Chrome DevTools (F12 or Cmd+Option+I -> Console tab).
 * 2. Copy and paste this script into the console and press Enter.
 * 3. The output Markdown + Frontmatter will be printed to console and copied to your clipboard!
 */
(function extractToKnowledgeBaseMarkdown() {
  console.log("🚀 Starting Knowledge Base DOM Extractor...");

  // 1. Identify primary content container
  function findMainContent() {
    const candidates = [
      'main',
      'article',
      '[role="main"]',
      '#content',
      '.content',
      '.post-content',
      '.article-content',
      '.entry-content',
      '.markdown-body'
    ];

    for (const selector of candidates) {
      const el = document.querySelector(selector);
      if (el && el.innerText && el.innerText.trim().length > 200) {
        return el.cloneNode(true);
      }
    }
    
    // Fallback to body
    const bodyClone = document.body.cloneNode(true);
    // Strip non-content elements
    const stripSelectors = [
      'header', 'footer', 'nav', 'aside', 'script', 'style', 'noscript', 'iframe',
      '.sidebar', '.comments', '.ad', '.ads', '.banner', '.menu', '#nav'
    ];
    stripSelectors.forEach(sel => {
      bodyClone.querySelectorAll(sel).forEach(el => el.remove());
    });
    return bodyClone;
  }

  // 2. Extract Page Metadata for YAML Frontmatter
  function getPageMetadata() {
    const getMeta = (propName) => {
      const el = document.querySelector(`meta[name="${propName}"], meta[property="${propName}"]`);
      return el ? el.getAttribute('content') : '';
    };

    const rawTitle = document.title || document.querySelector('h1')?.innerText || 'Untitled Page';
    const cleanTitle = rawTitle.replace(/[\r\n]+/g, ' ').replace(/"/g, '\\"').trim();
    const description = (getMeta('description') || getMeta('og:description') || '').replace(/"/g, '\\"').trim();
    const canonicalUrl = document.querySelector('link[rel="canonical"]')?.getAttribute('href') || window.location.href;
    const siteName = getMeta('og:site_name') || window.location.hostname;
    
    const today = new Date().toISOString().split('T')[0];

    // Infer basic tags from URL path and domain
    const pathSegments = window.location.pathname.split('/').filter(Boolean);
    const tags = Array.from(new Set([
      window.location.hostname.replace('www.', '').split('.')[0],
      ...pathSegments.slice(0, 3)
    ])).filter(t => t && t.length > 2 && !/^\d+$/.test(t));

    return {
      title: cleanTitle,
      description: description || "Extracted webpage content for knowledge base",
      source_url: canonicalUrl,
      domain: siteName,
      date_scraped: today,
      tags: tags
    };
  }

  // 3. Convert DOM to Markdown (Lightweight AST Walker)
  function domToMarkdown(node) {
    if (!node) return '';
    
    // Text node
    if (node.nodeType === Node.TEXT_NODE) {
      return node.textContent.replace(/\s+/g, ' ');
    }

    if (node.nodeType !== Node.ELEMENT_NODE) return '';

    // Ignore hidden elements
    const style = window.getComputedStyle ? window.getComputedStyle(node) : null;
    if (style && (style.display === 'none' || style.visibility === 'hidden')) {
      return '';
    }

    const tagName = node.tagName.toLowerCase();

    // Ignore noise elements
    if (['script', 'style', 'noscript', 'svg', 'form', 'button', 'input'].includes(tagName)) {
      return '';
    }

    // Process children
    const getChildrenMd = () => {
      let childMd = '';
      node.childNodes.forEach(child => {
        childMd += domToMarkdown(child);
      });
      return childMd;
    };

    switch (tagName) {
      case 'h1':
        return `\n\n# ${getChildrenMd().trim()}\n\n`;
      case 'h2':
        return `\n\n## ${getChildrenMd().trim()}\n\n`;
      case 'h3':
        return `\n\n### ${getChildrenMd().trim()}\n\n`;
      case 'h4':
        return `\n\n#### ${getChildrenMd().trim()}\n\n`;
      case 'h5':
        return `\n\n##### ${getChildrenMd().trim()}\n\n`;
      case 'h6':
        return `\n\n###### ${getChildrenMd().trim()}\n\n`;

      case 'p':
        const pContent = getChildrenMd().trim();
        return pContent ? `\n\n${pContent}\n\n` : '';

      case 'blockquote':
        const bqContent = getChildrenMd().trim().split('\n').map(line => `> ${line}`).join('\n');
        return `\n\n${bqContent}\n\n`;

      case 'ul':
        let ulContent = '';
        node.querySelectorAll(':scope > li').forEach(li => {
          ulContent += `- ${domToMarkdown(li).trim()}\n`;
        });
        return `\n\n${ulContent}\n`;

      case 'ol':
        let olContent = '';
        let idx = 1;
        node.querySelectorAll(':scope > li').forEach(li => {
          olContent += `${idx++}. ${domToMarkdown(li).trim()}\n`;
        });
        return `\n\n${olContent}\n`;

      case 'pre':
        const codeEl = node.querySelector('code');
        const lang = codeEl ? (codeEl.className.match(/language-(\w+)/) || [])[1] || '' : '';
        const rawCode = node.innerText.trim();
        return `\n\n\`\`\`${lang}\n${rawCode}\n\`\`\`\n\n`;

      case 'code':
        if (node.parentElement && node.parentElement.tagName.toLowerCase() === 'pre') {
          return node.innerText;
        }
        return `\`${node.innerText.trim()}\``;

      case 'a':
        const href = node.getAttribute('href');
        const linkText = getChildrenMd().trim();
        if (!href || href.startsWith('javascript:') || !linkText) return linkText;
        // Resolve relative links
        try {
          const absoluteUrl = new URL(href, window.location.href).href;
          return `[${linkText}](${absoluteUrl})`;
        } catch (e) {
          return `[${linkText}](${href})`;
        }

      case 'img':
        const src = node.getAttribute('src');
        const alt = node.getAttribute('alt') || 'Image';
        if (!src) return '';
        try {
          const absoluteSrc = new URL(src, window.location.href).href;
          return `![${alt}](${absoluteSrc})`;
        } catch (e) {
          return `![${alt}](${src})`;
        }

      case 'strong':
      case 'b':
        const strongText = getChildrenMd().trim();
        return strongText ? `**${strongText}**` : '';

      case 'em':
      case 'i':
        const emText = getChildrenMd().trim();
        return emText ? `*${emText}*` : '';

      case 'hr':
        return `\n\n---\n\n`;

      case 'table':
        return convertTableToMd(node);

      case 'div':
      case 'section':
      case 'article':
      case 'main':
      case 'span':
      default:
        return getChildrenMd();
    }
  }

  // Helper for Markdown Tables
  function convertTableToMd(tableNode) {
    const rows = Array.from(tableNode.querySelectorAll('tr'));
    if (rows.length === 0) return '';

    let mdTable = '\n\n';
    rows.forEach((row, rowIndex) => {
      const cols = Array.from(row.querySelectorAll('th, td')).map(cell => {
        return cell.innerText.replace(/[\r\n]+/g, ' ').replace(/\|/g, '\\|').trim();
      });
      mdTable += `| ${cols.join(' | ')} |\n`;
      
      // Add table header separator line after row 0
      if (rowIndex === 0) {
        const sep = cols.map(() => '---').join(' | ');
        mdTable += `| ${sep} |\n`;
      }
    });
    return mdTable + '\n\n';
  }

  // 4. Clean Markdown output (remove multi-blank lines, etc.)
  function cleanMarkdown(md) {
    return md
      .replace(/\n{3,}/g, '\n\n')
      .replace(/[ \t]+\n/g, '\n')
      .trim();
  }

  // 5. Construct Final YAML Frontmatter + Markdown Body
  const meta = getPageMetadata();
  const mainNode = findMainContent();
  const rawMd = domToMarkdown(mainNode);
  const cleanedMd = cleanMarkdown(rawMd);

  const yamlFrontmatter = [
    '---',
    `title: "${meta.title}"`,
    `description: "${meta.description}"`,
    `source_url: "${meta.source_url}"`,
    `domain: "${meta.domain}"`,
    `date_scraped: "${meta.date_scraped}"`,
    `status: "raw_import"`,
    `category: "uncategorized"`,
    `tags:`,
    ...meta.tags.map(t => `  - "${t}"`),
    `reading_time_min: ${Math.max(1, Math.ceil(cleanedMd.split(/\s+/).length / 200))}`,
    '---',
    '',
    cleanedMd
  ].join('\n');

  // 6. Print to Console & Copy to Clipboard
  console.log("✅ Knowledge Base Markdown Generated Successfully!");
  console.log("--------------------------------------------------");
  console.log(yamlFrontmatter);
  console.log("--------------------------------------------------");

  if (typeof copy === 'function') {
    copy(yamlFrontmatter);
    console.log("📋 COPIED TO CLIPBOARD! You can now paste this directly into raw_imports/page.md");
  } else {
    console.warn("⚠️ `copy()` is only available in standard Chrome DevTools Console. Select the text above to copy manually.");
  }

  return yamlFrontmatter;
})();
