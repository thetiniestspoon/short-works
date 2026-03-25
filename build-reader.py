#!/usr/bin/env python3
"""
Build script for Short Works reader site.
Reads content/*.md files and generates reader/index.html.
No external dependencies — uses only Python standard library.
"""

import os
import re
import html

CONTENT_DIR = "content"
OUTPUT_FILE = os.path.join("reader", "index.html")

# Parallax scene configs: gradient backgrounds for each piece transition
# These are placeholder scenes — swap with real imagery later
SCENE_CONFIGS = {
    "01-brooklyn-summer": {
        "gradient": "linear-gradient(180deg, #1a2a3a 0%, #0d1a2a 40%, #1a3040 100%)",
        "label": "Brooklyn summer",
    },
    "02-pancakes": {
        "gradient": "linear-gradient(180deg, #3a2a1a 0%, #2a1f12 40%, #4a3520 100%)",
        "label": "Pancakes",
    },
    "04-reflection": {
        "gradient": "linear-gradient(180deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%)",
        "label": "Reflection",
    },
    "05-misfits": {
        "gradient": "linear-gradient(180deg, #3a1a1a 0%, #2e1212 40%, #4a2020 100%)",
        "label": "Misfits",
    },
    "07-constance": {
        "gradient": "linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 40%, #2a2a2a 100%)",
        "label": "The Virtues of Constance",
    },
    "08-uncle": {
        "gradient": "linear-gradient(180deg, #1a2a3a 0%, #0d1520 40%, #1a2530 100%)",
        "label": "Uncle",
    },
    "09-doorjam": {
        "gradient": "linear-gradient(180deg, #3a2010 0%, #4a2a0a 40%, #2a1505 100%)",
        "label": "Doorjam",
    },
    "10-drown": {
        "gradient": "linear-gradient(180deg, #0a1520 0%, #0d1a2e 40%, #1a2a3a 100%)",
        "label": "Drown",
    },
    "12-beloved-creation": {
        "gradient": "linear-gradient(180deg, #1a1a2e 0%, #2a1a3a 40%, #1a1520 100%)",
        "label": "His Beloved Creation",
    },
    "13-transcendent-love": {
        "gradient": "linear-gradient(180deg, #1a2e1a 0%, #0d200d 40%, #1a3a1a 100%)",
        "label": "Transcendent Love",
    },
}

# Types that get prose treatment (justified, indented, drop cap)
PROSE_TYPES = {
    "prose-poem", "flash-fiction", "allegorical-fiction", "dark-comedy",
    "creative-prose", "fantasy-fragment",
}

def parse_frontmatter(text):
    """Parse YAML-like frontmatter from markdown content."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            val = val.strip().strip('"').strip("'")
            meta[key.strip()] = val
    return meta, parts[2].strip()


def markdown_to_html(text, piece_type):
    """Convert simple markdown to HTML based on piece type."""
    text = html.escape(text)
    # Restore quotes and dashes
    text = text.replace("&amp;mdash;", "\u2014")
    text = text.replace("&quot;", '"')

    if piece_type == "poetry":
        # Poetry: preserve line breaks, group stanzas
        stanzas = re.split(r"\n\n+", text)
        parts = []
        for stanza in stanzas:
            lines = stanza.strip().split("\n")
            parts.append("<p class=\"poem-stanza\">" + "<br>\n".join(lines) + "</p>")
        return "\n".join(parts)

    elif piece_type == "micro-poem":
        # Micro-poem: centered, preserve line breaks
        lines = text.strip().split("\n")
        return "<p class=\"micro-poem-text\">" + "<br>\n".join(lines) + "</p>"

    elif piece_type == "hybrid":
        # Hybrid (Uncle): detect prose vs poetry sections
        # Poetry sections are lines that don't form full paragraphs
        paragraphs = re.split(r"\n\n+", text)
        parts = []
        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue
            lines = para.split("\n")
            # Heuristic: if most lines are short (< 60 chars), treat as poetry
            avg_len = sum(len(l) for l in lines) / max(len(lines), 1)
            if avg_len < 60 and len(lines) > 1:
                parts.append("<div class=\"hybrid-verse\">" +
                           "<p class=\"poem-stanza\">" + "<br>\n".join(lines) + "</p>" +
                           "</div>")
            else:
                css_class = "drop-cap" if i == 0 else ""
                if css_class:
                    parts.append(f'<p class="{css_class}">{para}</p>')
                else:
                    parts.append(f"<p>{para}</p>")
        return "\n".join(parts)

    elif piece_type == "prose-poetry":
        # Prose-poetry (Pancakes): two pieces separated by blank line, visual break between
        paragraphs = re.split(r"\n\n+", text)
        parts = []
        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue
            css_class = "drop-cap" if i == 0 else ""
            if css_class:
                parts.append(f'<p class="{css_class}">{para}</p>')
            else:
                parts.append(f"<p>{para}</p>")
            # Add visual break after first piece
            if i == 0 and len(paragraphs) > 1:
                parts.append('<div class="section-break">&middot; &middot; &middot;</div>')
        return "\n".join(parts)

    else:
        # Default prose treatment
        paragraphs = re.split(r"\n\n+", text)
        parts = []
        for i, para in enumerate(paragraphs):
            para = para.strip()
            if not para:
                continue
            css_class = "drop-cap" if i == 0 else ""
            if css_class:
                parts.append(f'<p class="{css_class}">{para}</p>')
            else:
                parts.append(f"<p>{para}</p>")
        return "\n".join(parts)


def build_parallax_scene(slug):
    """Generate a parallax scene divider."""
    config = SCENE_CONFIGS.get(slug)
    if not config:
        return ""
    return f'''
    <div class="parallax-scene" style="background: {config["gradient"]};">
      <div class="parallax-layer parallax-layer-1"></div>
      <div class="parallax-layer parallax-layer-2"></div>
      <div class="parallax-layer parallax-layer-3"></div>
    </div>
'''


def build_piece_html(slug, meta, body_html, index):
    """Generate HTML for a single piece."""
    title = meta.get("title", "")
    piece_type = meta.get("type", "prose-poem")
    piece_id = f"piece-{index + 1}"

    # Determine CSS classes for the piece container
    if piece_type in PROSE_TYPES:
        container_class = "prose"
    elif piece_type == "poetry":
        container_class = "poetry"
    elif piece_type == "hybrid":
        container_class = "hybrid"
    elif piece_type == "micro-poem":
        container_class = "micro-poem"
    elif piece_type == "prose-poetry":
        container_class = "prose"
    else:
        container_class = "prose"

    # Build the title block
    if piece_type == "micro-poem":
        # Micro-poems: no title divider, just the centered text
        title_html = ""
    else:
        border_style = 'style="border-top:none;margin-top:0;padding-top:0;"' if index == 0 else ""
        title_html = f'''
    <div class="piece-divider" {border_style}>
      <h2 class="piece-heading">{html.escape(title)}</h2>
      <span class="piece-ornament">&middot; &middot; &middot;</span>
    </div>
'''

    return f'''
    <section class="piece-section" id="{piece_id}">
      {title_html}
      <div class="{container_class}">
        {body_html}
      </div>
    </section>
'''


def build_nav_header(pieces):
    """Generate the fixed header navigation."""
    links = ['<a href="#title">Top</a>']
    for i, (slug, meta, _) in enumerate(pieces):
        title = meta.get("title", "")
        piece_type = meta.get("type", "")
        if piece_type == "micro-poem":
            continue  # Skip micro-poems in nav
        short = title[:20] + ("..." if len(title) > 20 else "")
        links.append(f'<a href="#piece-{i + 1}">{html.escape(short)}</a>')
    return "\n    ".join(links)


def build_dot_nav(pieces):
    """Generate the dot navigation sidebar."""
    dots = []
    for i, (slug, meta, _) in enumerate(pieces):
        title = meta.get("title", "")
        piece_type = meta.get("type", "")
        if piece_type == "micro-poem":
            continue
        dots.append(
            f'<a href="#piece-{i + 1}" title="{html.escape(title)}">'
            f'<span class="dot-label">{html.escape(title)}</span></a>'
        )
    return "\n  ".join(dots)


def generate_html(pieces):
    """Generate the complete reader HTML."""
    nav_links = build_nav_header(pieces)
    dot_nav = build_dot_nav(pieces)

    # Build all piece sections with parallax scenes between them
    body_parts = []
    for i, (slug, meta, body_html) in enumerate(pieces):
        piece_html = build_piece_html(slug, meta, body_html, i)
        body_parts.append(piece_html)

        # Add parallax scene after non-micro-poem pieces (not after last piece)
        if meta.get("type") != "micro-poem" and i < len(pieces) - 1:
            scene = build_parallax_scene(slug)
            if scene:
                body_parts.append(scene)
        elif meta.get("type") == "micro-poem":
            # Micro-poems get a subtle ornament divider
            body_parts.append('<div class="micro-divider">&middot;</div>')

    all_pieces_html = "\n".join(body_parts)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Short Works &mdash; Shawn Jordan</title>
<style>
  :root {{
    --bg: #f5f0e8;
    --bg-alt: #ebe5d8;
    --text: #2c2416;
    --text-muted: #6b5d4d;
    --accent: #8b7355;
    --border: #c9bda8;
    --pull-bg: #efe9de;
    --progress-bg: #d4c9b8;
    --progress-fill: #8b7355;
  }}

  html.dark {{
    --bg: #1a1612;
    --bg-alt: #231e18;
    --text: #d4c9b8;
    --text-muted: #8b7d6b;
    --accent: #c4a97d;
    --border: #3d3428;
    --pull-bg: #231e18;
    --progress-bg: #2a2319;
    --progress-fill: #c4a97d;
  }}

  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  html {{
    scroll-behavior: smooth;
    font-size: 18px;
  }}

  body {{
    font-family: Georgia, 'Times New Roman', 'Palatino Linotype', serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.9;
    transition: background-color 0.4s ease, color 0.4s ease;
    min-height: 100vh;
  }}

  #progress-bar {{
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: 3px;
    background: var(--progress-fill);
    z-index: 1000;
    transition: width 0.1s linear;
  }}

  header {{
    position: fixed;
    top: 3px;
    right: 0;
    left: 0;
    z-index: 999;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 1.5rem;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    opacity: 0;
    transform: translateY(-100%);
    transition: opacity 0.3s ease, transform 0.3s ease, background-color 0.4s ease;
  }}

  header.visible {{
    opacity: 1;
    transform: translateY(0);
  }}

  header nav {{
    display: flex;
    gap: 0.8rem;
    align-items: center;
    flex-wrap: wrap;
  }}

  header nav a {{
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.2s;
  }}

  header nav a:hover, header nav a.active-nav {{ color: var(--accent); }}

  .dark-toggle {{
    background: none;
    border: 1px solid var(--border);
    color: var(--text-muted);
    font-family: Georgia, serif;
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    padding: 0.3rem 0.7rem;
    cursor: pointer;
    border-radius: 3px;
    transition: all 0.3s ease;
    white-space: nowrap;
    flex-shrink: 0;
  }}

  .dark-toggle:hover {{
    color: var(--accent);
    border-color: var(--accent);
  }}

  main {{
    max-width: 70ch;
    margin: 0 auto;
    padding: 6rem 1.5rem 4rem;
  }}

  .title-block {{
    text-align: center;
    margin-bottom: 4rem;
    padding: 3rem 0;
  }}

  .collection-title {{
    font-size: 2rem;
    font-variant: small-caps;
    letter-spacing: 0.15em;
    font-weight: normal;
    color: var(--text);
    margin-bottom: 0.5rem;
  }}

  .collection-author {{
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 1rem;
  }}

  .collection-ornament {{
    display: block;
    margin: 1.5rem auto 0;
    color: var(--accent);
    font-size: 1.2rem;
    letter-spacing: 0.6em;
    opacity: 0.5;
  }}

  /* Piece dividers */
  .piece-divider {{
    text-align: center;
    margin: 6rem 0 2rem;
    padding: 4rem 0 3rem;
    border-top: 1px solid var(--border);
  }}

  .piece-heading {{
    font-size: 1.4rem;
    font-variant: small-caps;
    letter-spacing: 0.15em;
    font-weight: normal;
    color: var(--text);
    margin-bottom: 0.5rem;
  }}

  .piece-ornament {{
    display: block;
    margin: 1rem auto 0;
    color: var(--accent);
    font-size: 1rem;
    letter-spacing: 0.6em;
    opacity: 0.5;
  }}

  /* Prose styling */
  .prose p {{
    margin-bottom: 1.5rem;
    text-align: justify;
    text-indent: 2rem;
    hyphens: auto;
    -webkit-hyphens: auto;
  }}

  .prose p:first-of-type,
  .section-break + p {{
    text-indent: 0;
  }}

  .drop-cap::first-letter {{
    float: left;
    font-size: 4.2rem;
    line-height: 0.75;
    padding: 0.1rem 0.5rem 0 0;
    color: var(--accent);
    font-weight: normal;
    font-family: Georgia, 'Palatino Linotype', serif;
  }}

  /* Poetry styling */
  .poetry .poem-stanza {{
    margin-bottom: 1.8rem;
    text-align: left;
    line-height: 2;
  }}

  /* Hybrid styling */
  .hybrid p {{
    margin-bottom: 1.5rem;
    text-align: justify;
    text-indent: 2rem;
    hyphens: auto;
    -webkit-hyphens: auto;
  }}

  .hybrid p:first-of-type {{
    text-indent: 0;
  }}

  .hybrid-verse {{
    margin: 2.5rem 0;
    padding-left: 2rem;
  }}

  .hybrid-verse .poem-stanza {{
    text-align: left;
    text-indent: 0;
    line-height: 2.2;
    font-style: italic;
    color: var(--text-muted);
  }}

  /* Micro-poem styling */
  .micro-poem {{
    text-align: center;
    padding: 3rem 0;
  }}

  .micro-poem-text {{
    font-size: 1.15em;
    line-height: 2.2;
    font-style: italic;
    color: var(--text);
  }}

  .micro-divider {{
    text-align: center;
    margin: 1rem 0;
    color: var(--accent);
    font-size: 1rem;
    opacity: 0.4;
  }}

  /* Section break */
  .section-break {{
    text-align: center;
    margin: 3rem 0;
    color: var(--accent);
    font-size: 0.9rem;
    letter-spacing: 0.8em;
    opacity: 0.4;
  }}

  /* Parallax scenes */
  .parallax-scene {{
    position: relative;
    height: 70vh;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 calc(-50vw + 50%);
    width: 100vw;
  }}

  .parallax-layer {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    opacity: 0.15;
  }}

  .parallax-layer-1 {{
    background: radial-gradient(ellipse at 30% 50%, rgba(255,255,255,0.1) 0%, transparent 70%);
  }}

  .parallax-layer-2 {{
    background: radial-gradient(ellipse at 70% 30%, rgba(255,255,255,0.08) 0%, transparent 60%);
  }}

  .parallax-layer-3 {{
    background: radial-gradient(ellipse at 50% 80%, rgba(255,255,255,0.05) 0%, transparent 50%);
  }}

  /* Scroll animations */
  .piece-section {{
    opacity: 0;
    transform: translateY(12px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }}

  .piece-section.visible {{
    opacity: 1;
    transform: translateY(0);
  }}

  /* Dot navigation */
  #section-nav {{
    position: fixed;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    z-index: 998;
  }}

  #section-nav a {{
    display: block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--border);
    transition: background 0.3s ease, transform 0.3s ease;
    position: relative;
    text-decoration: none;
  }}

  #section-nav a.active {{
    background: var(--accent);
    transform: scale(1.3);
  }}

  #section-nav a:hover {{
    background: var(--accent);
  }}

  #section-nav a .dot-label {{
    display: none;
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.6rem;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    white-space: nowrap;
    font-family: Georgia, serif;
  }}

  #section-nav a:hover .dot-label {{
    display: block;
  }}

  /* Footer */
  footer {{
    max-width: 70ch;
    margin: 0 auto;
    padding: 3rem 1.5rem 4rem;
    text-align: center;
    border-top: 1px solid var(--border);
  }}

  footer p {{
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    line-height: 2;
  }}

  footer .ornament {{
    color: var(--accent);
    opacity: 0.4;
    font-size: 0.9rem;
    letter-spacing: 0.6em;
    margin-bottom: 1rem;
  }}

  /* Responsive */
  @media (max-width: 768px) {{
    html {{ font-size: 16px; }}
    main {{ padding: 5rem 1.2rem 3rem; }}
    .title-block {{ margin-bottom: 3rem; padding: 2rem 0; }}
    .piece-heading {{ font-size: 1.2rem; }}
    .parallax-scene {{ height: 40vh; }}
    #section-nav {{ display: none; }}
    .piece-divider {{ margin: 4rem 0 1.5rem; padding: 3rem 0 2rem; }}
    header nav {{ gap: 0.4rem; }}
    header nav a {{ font-size: 0.55rem; }}
    .drop-cap::first-letter {{ font-size: 3.2rem; }}
  }}
</style>
</head>
<body>

<div id="progress-bar"></div>

<header id="header">
  <nav>
    {nav_links}
  </nav>
  <button class="dark-toggle" id="darkToggle" aria-label="Toggle dark mode">Lamplight</button>
</header>

<nav id="section-nav" aria-label="Piece navigation">
  {dot_nav}
</nav>

<main>
  <div class="title-block" id="title">
    <h1 class="collection-title">Short Works</h1>
    <p class="collection-author">Shawn Jordan</p>
    <span class="collection-ornament">&middot; &middot; &middot;</span>
  </div>

  {all_pieces_html}
</main>

<footer>
  <div class="ornament">&middot; &middot; &middot;</div>
  <p>Short Works &mdash; Shawn Jordan</p>
  <p>&copy; Shawn Jordan. All rights reserved.</p>
</footer>

<script>
(function() {{
  // Dark mode toggle
  const toggle = document.getElementById('darkToggle');
  const html = document.documentElement;

  if (localStorage.getItem('dark') === 'true') {{
    html.classList.add('dark');
    toggle.textContent = 'Daylight';
  }}

  toggle.addEventListener('click', function() {{
    html.classList.toggle('dark');
    const isDark = html.classList.contains('dark');
    localStorage.setItem('dark', isDark);
    toggle.textContent = isDark ? 'Daylight' : 'Lamplight';
  }});

  // Progress bar
  const progressBar = document.getElementById('progress-bar');
  function updateProgress() {{
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = progress + '%';
  }}

  // Header visibility
  const header = document.getElementById('header');
  let lastScroll = 0;
  function updateHeader() {{
    const scrollTop = window.scrollY;
    if (scrollTop > 300) {{
      header.classList.add('visible');
    }} else {{
      header.classList.remove('visible');
    }}
    lastScroll = scrollTop;
  }}

  // Section fade-in
  const sections = document.querySelectorAll('.piece-section');
  const observer = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      if (entry.isIntersecting) {{
        entry.target.classList.add('visible');
      }}
    }});
  }}, {{ threshold: 0.1 }});

  sections.forEach(function(section) {{
    observer.observe(section);
  }});

  // Dot navigation active state
  const dots = document.querySelectorAll('#section-nav a');
  const pieceIds = Array.from(dots).map(function(d) {{
    return d.getAttribute('href').substring(1);
  }});

  function updateDots() {{
    let activeId = pieceIds[0];
    for (let i = 0; i < pieceIds.length; i++) {{
      const el = document.getElementById(pieceIds[i]);
      if (el && el.getBoundingClientRect().top <= window.innerHeight * 0.4) {{
        activeId = pieceIds[i];
      }}
    }}
    dots.forEach(function(dot) {{
      const href = dot.getAttribute('href').substring(1);
      dot.classList.toggle('active', href === activeId);
    }});
  }}

  // Active nav link in header
  const navLinks = document.querySelectorAll('header nav a');
  function updateNavLinks() {{
    let activeHref = '#title';
    for (let i = 0; i < pieceIds.length; i++) {{
      const el = document.getElementById(pieceIds[i]);
      if (el && el.getBoundingClientRect().top <= window.innerHeight * 0.4) {{
        activeHref = '#' + pieceIds[i];
      }}
    }}
    navLinks.forEach(function(link) {{
      link.classList.toggle('active-nav', link.getAttribute('href') === activeHref);
    }});
  }}

  // Parallax scroll effect
  const scenes = document.querySelectorAll('.parallax-scene');
  function updateParallax() {{
    scenes.forEach(function(scene) {{
      const rect = scene.getBoundingClientRect();
      const speed = 0.3;
      if (rect.top < window.innerHeight && rect.bottom > 0) {{
        const offset = (rect.top - window.innerHeight) * speed;
        const layers = scene.querySelectorAll('.parallax-layer');
        layers.forEach(function(layer, i) {{
          const layerSpeed = (i + 1) * 0.15;
          layer.style.transform = 'translateY(' + (offset * layerSpeed) + 'px)';
        }});
      }}
    }});
  }}

  // Throttled scroll handler
  let ticking = false;
  window.addEventListener('scroll', function() {{
    if (!ticking) {{
      requestAnimationFrame(function() {{
        updateProgress();
        updateHeader();
        updateDots();
        updateNavLinks();
        updateParallax();
        ticking = false;
      }});
      ticking = true;
    }}
  }});

  // Initial calls
  updateProgress();
  updateHeader();
  updateDots();
}})();
</script>

</body>
</html>'''


def main():
    # Read all content files
    files = sorted(f for f in os.listdir(CONTENT_DIR) if f.endswith(".md"))
    pieces = []

    for filename in files:
        slug = filename.replace(".md", "")
        filepath = os.path.join(CONTENT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        meta, body = parse_frontmatter(raw)
        piece_type = meta.get("type", "prose-poem")
        body_html = markdown_to_html(body, piece_type)
        pieces.append((slug, meta, body_html))

    # Generate HTML
    html_output = generate_html(pieces)

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"Built {OUTPUT_FILE} ({len(pieces)} pieces, {len(html_output):,} bytes)")


if __name__ == "__main__":
    main()
