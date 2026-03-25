# Short Works Reader Site — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a GitHub Pages reader site for 14 literary works with parallax scene transitions, following the Apologies to Gryphons pattern.

**Architecture:** Hybrid build — content lives as markdown files with YAML frontmatter, a Python build script compiles them into a single `reader/index.html` with all CSS/JS inline. GitHub Actions deploys the `reader/` directory to Pages.

**Tech Stack:** Python 3 (standard library only — custom markdown-to-HTML), static HTML/CSS/JS, GitHub Actions

---

### Task 1: Create content markdown files

**Files:**
- Create: `content/01-brooklyn-summer.md`
- Create: `content/02-pancakes.md`
- Create: `content/03-fear.md`
- Create: `content/04-reflection.md`
- Create: `content/05-misfits.md`
- Create: `content/06-kisses-storms.md`
- Create: `content/07-constance.md`
- Create: `content/08-uncle.md`
- Create: `content/09-doorjam.md`
- Create: `content/10-drown.md`
- Create: `content/11-kiss-vomit.md`
- Create: `content/12-beloved-creation.md`
- Create: `content/13-transcendent-love.md`
- Create: `content/14-zoe.md`

- [ ] **Step 1: Extract all texts from Dropbox sources and create content files**

Each file has YAML frontmatter (`title`, `type`) followed by the piece text. Extract from `.docx` via Python zipfile, from `.txt` directly, from `.pdf` via the known text. Fix encoding (curly quotes, em dashes). Apply migration rules per spec (strip cover letters, notes, GPT conversation, labels).

- [ ] **Step 2: Verify all 14 files exist and content is clean**

Run: `ls content/*.md | wc -l` — expected: 14
Spot-check: read first/last lines of each file to confirm frontmatter and content.

- [ ] **Step 3: Commit**

```bash
git add content/
git commit -m "Add all 14 content files migrated from Dropbox sources"
```

---

### Task 2: Create the build script

**Files:**
- Create: `build-reader.py`

- [ ] **Step 1: Write `build-reader.py`**

The script must:
1. Read all `content/*.md` files in filename order
2. Parse YAML frontmatter (title, type) — use simple string parsing, no PyYAML dependency
3. Convert body text to HTML paragraphs (split on double newlines, wrap in `<p>`, handle single newlines as `<br>` for poetry)
4. Apply CSS class per type: `prose` (default), `poetry` (left-aligned, line breaks preserved), `hybrid` (mixed), `micro-poem` (centered), `prose-poetry` (paired with visual break)
5. Generate the complete HTML with:
   - Inline CSS (adapted from Gryphons reader — warm parchment palette, dark mode, 70ch, serif, progress bar, nav)
   - Parallax scene dividers between non-micro-poem pieces (placeholder gradient scenes initially)
   - Drop caps on first paragraph of prose pieces
   - Dot navigation and header navigation
   - Dark/light toggle with localStorage persistence
   - Scroll animations (fade-in sections, progress bar, active nav tracking)
   - All JS inline at bottom
6. Write output to `reader/index.html`

- [ ] **Step 2: Run the build**

Run: `python build-reader.py`
Expected: `reader/index.html` created, no errors

- [ ] **Step 3: Verify output**

Check: `ls -la reader/index.html` — file exists and is non-empty
Open in browser to verify rendering.

- [ ] **Step 4: Commit**

```bash
git add build-reader.py reader/index.html
git commit -m "Add build script and generated reader site"
```

---

### Task 3: Create GitHub Actions deploy workflow

**Files:**
- Create: `.github/workflows/deploy-reader.yml`

- [ ] **Step 1: Write the workflow file**

```yaml
name: Deploy Reader to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'reader/**'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: reader

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/deploy-reader.yml
git commit -m "Add GitHub Actions workflow for Pages deployment"
```

---

### Task 4: Create README

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README**

Brief README with collection description, read-online link, and build instructions.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "Add README with collection description and build instructions"
```

---

### Task 5: Create .gitignore

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Write .gitignore**

```
__pycache__/
*.pyc
.superpowers/
.DS_Store
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "Add .gitignore"
```
