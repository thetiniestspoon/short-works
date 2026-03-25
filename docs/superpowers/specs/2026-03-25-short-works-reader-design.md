# Short Works — Reader Site Design Spec

## Overview

A curated collection of 14 literary works by Shawn Jordan, published as a single-page GitHub Pages reader site with parallax imagery transitions between pieces. Follows the pattern established by the Apologies to Gryphons reader site.

**Live URL:** `thetiniestspoon.github.io/short-works`

## Collection Title

**Short Works**

## Pieces (Emotional Arc Ordering)

| # | Title | Type | Parallax Scene After |
|---|-------|------|---------------------|
| 1 | Brooklyn summer | prose-poem | Yes — pier/skyline/water |
| 2 | Pancakes | prose-poetry (paired) | Yes — kitchen/morning light |
| 3 | Fear | micro-poem (interstitial) | No — ornament divider only |
| 4 | Reflection | prose-poem | Yes — still water/twilight |
| 5 | Misfits | flash-fiction | Yes — reception hall/red |
| 6 | kisses/storms | micro-poem (interstitial) | No — ornament divider only |
| 7 | The Virtues of Constance | dark-comedy | Yes — highway/night/headlights |
| 8 | Uncle | hybrid (prose + poetry fragments) | Yes — pool/hospital/car |
| 9 | Doorjam | allegorical-fiction | Yes — door facade/rats/fire |
| 10 | Drown | prose-poem | Yes — storm/ocean/spotlight |
| 11 | kiss/vomit | micro-poem (interstitial) | No — ornament divider only |
| 12 | His Beloved Creation | creative-prose | Yes — lab/lightning/creature |
| 13 | Transcendent Love | poetry | Yes — storm/rain/dance |
| 14 | Zoe | fantasy-fragment | No — ends with closing ornament + footer |

**Ordering rationale:** Light to dark to light. Opens with warmth (Brooklyn summer), descends through alienation, rage, and grief (Misfits, Uncle, Doorjam), then resolves through rescue, acceptance, ecstasy, and wonder (Drown, Beloved Creation, Transcendent Love, Zoe).

## Architecture

### Repo Structure

```
short-works/
  README.md
  build-reader.py
  reader/
    index.html              (generated output — deployed to GitHub Pages)
    images/                 (parallax layer assets from Writing Pictures + generated)
  content/
    01-brooklyn-summer.md
    02-pancakes.md
    03-fear.md
    04-reflection.md
    05-misfits.md
    06-kisses-storms.md
    07-constance.md
    08-uncle.md
    09-doorjam.md
    10-drown.md
    11-kiss-vomit.md
    12-beloved-creation.md
    13-transcendent-love.md
    14-zoe.md
  scenes/
    scene-config.json       (per-piece parallax layer definitions)
  docs/
    superpowers/specs/      (this spec)
  .github/
    workflows/
      deploy-reader.yml
```

### Content File Format

Each piece is a markdown file with YAML frontmatter:

```yaml
---
title: Brooklyn summer
type: prose-poem        # prose-poem | poetry | flash-fiction | hybrid | micro-poem | fantasy-fragment | creative-prose | dark-comedy | allegorical-fiction | prose-poetry
---

A New York summer usually feels like you're sticking your head into an oven...
```

Parallax scene configuration lives separately in `scenes/scene-config.json`:

```json
{
  "01-brooklyn-summer": {
    "layers": [
      { "image": "brooklyn-water.png", "speed": 0.3 },
      { "image": "brooklyn-pier.png", "speed": 0.6 },
      { "image": "brooklyn-skyline.png", "speed": 0.8 }
    ]
  }
}
```

### Build Script (`build-reader.py`)

- Reads `content/*.md` files in filename order (01-, 02-, etc.)
- Parses YAML frontmatter for title and type
- Converts markdown body to HTML (paragraphs, line breaks, emphasis)
- Applies styling class per type (justified prose, left-aligned poetry, hybrid sections, centered micro-poems)
- Generates parallax scene divs between pieces using `scenes/scene-config.json`
- Outputs single `reader/index.html` with all CSS and JS inline
- Dependencies: Python standard library + `mistune` or `markdown` for markdown parsing

### Deployment

- GitHub Actions: push to `main` on `reader/**` triggers deploy (identical to Gryphons workflow)
- Build runs locally: `python build-reader.py` generates `reader/index.html`
- Commit generated output, push to trigger deploy
- Local preview: open `reader/index.html` directly or `python -m http.server -d reader`

## Reader Site Features

### Typography & Layout

- Serif font stack: Georgia, 'Times New Roman', 'Palatino Linotype', serif
- 70ch max-width, 18px base font size, 1.9 line-height
- Drop caps on first paragraph of each piece (not micro-poems)
- Justified text with CSS hyphenation for prose
- Piece titles in small-caps with `· · ·` ornament dividers
- Responsive: 16px base on mobile, adjusted padding

### Navigation

- Fixed header appears on scroll with piece titles as nav links
- Dot navigation on right side (one dot per piece, label on hover)
- Reading progress bar (3px, fixed top)
- Dark/light toggle ("Lamplight" button)

### Dark Mode

- Light: warm parchment palette (`#f5f0e8` bg, `#2c2416` text, `#8b7355` accent)
- Dark: warm charcoal palette (`#1a1612` bg, `#d4c9b8` text, `#c4a97d` accent)
- Smooth 0.4s transition, preference saved to localStorage

### Parallax Scenes

- Full-bleed panels between pieces, 60-80vh tall
- 2-3 image layers per scene at different scroll speeds (0.3x, 0.6x, 0.8x)
- Initial imagery sourced from Writing Pictures mood board PDF, supplemented later
- Implementation: JS-driven `transform: translateY()` on scroll for smooth parallax
- Mobile fallback: static centered image, no parallax (mobile browsers handle `background-attachment: fixed` poorly)

### Piece Type Styling

| Type | Treatment |
|------|-----------|
| `prose-poem`, `flash-fiction`, `allegorical-fiction`, `dark-comedy`, `creative-prose` | Justified, indented paragraphs, drop cap on first paragraph |
| `poetry` | Left-aligned, preserved line breaks, no justification, no indent |
| `hybrid` | Prose sections justified; poetic fragments left-aligned with extra leading |
| `prose-poetry` (Pancakes) | Like prose-poem but with a visual break between the two companion pieces |
| `micro-poem` | Centered, larger font (1.15em), extra vertical whitespace, no drop cap, no parallax scene after |
| `fantasy-fragment` | Same as prose, ends with ornamental break instead of scene transition |

### Scroll Animations

- Pieces fade in on scroll (opacity 0 → 1, translateY 12px → 0, 0.6s ease)
- Parallax layers move at defined scroll rates
- Section dots update active state based on scroll position

## Content Migration

| Piece | Source File | Migration Action |
|-------|-----------|-----------------|
| Brooklyn summer | `Dropbox/Writing/Brooklyn summer.docx` | Extract text, fix encoding |
| Pancakes | `Dropbox/Writing/Pancakes/Pancakes.pdf` | Join both pieces, strip "Write 1/2" labels |
| Fear | `Dropbox/Writing/Short Poetry.docx` | Extract single poem |
| Reflection | `Dropbox/Writing/Shawn Jordan_Reflection.docx` | Strip cover letter |
| Misfits | `Dropbox/Writing/Misfits.txt` | Clean copy |
| kisses/storms | `Dropbox/Writing/Short Poetry.docx` | Extract single poem |
| Constance | `Dropbox/Writing/Constance/The Virtues of Constance_20221211.docx` | Strip "Notes on Constance" |
| Uncle | `Dropbox/Writing/Uncle.docx` | Keep fragments, strip bare motif list at end |
| Doorjam | `Dropbox/Writing/Anti-Drumpf Therapy/The Pantry Door.docx` | Rename to "Doorjam" |
| Drown | `Dropbox/Writing/Shawn Jordan_Drown.docx` | Extract text, strip title line |
| kiss/vomit | `Dropbox/Writing/Short Poetry.docx` | Extract single poem |
| His Beloved Creation | `Dropbox/Writing/Beloved Creation/His Beloved Creation_20230104.docx` | Extract creative prose only, strip GPT conversation |
| Transcendent Love | `Dropbox/Writing/Shawn Jordan_Transcendent Love.docx` | Strip cover letter |
| Zoe | `Dropbox/Writing/Zoe.docx` | Full text, ends on the knock |

**Encoding cleanup:** All `.docx` extractions need curly quote normalization (Windows-1252 artifacts like `\u0092` → proper UTF-8 curly quotes or straight quotes).

## Not In Scope

- No search functionality
- No comments or social features
- No analytics (can add later)
- No print stylesheet (can add later)
- Camp Camp essay (held for revision, not part of initial collection)
- "Can you not hear it" (held for different venue)
