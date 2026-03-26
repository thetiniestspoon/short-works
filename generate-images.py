#!/usr/bin/env python3
"""
Generate all parallax scene images via LLM Gateway + Gemini.
Saves PNGs to reader/images/.
"""

import json
import base64
import os
import sys
import time
import urllib.request
import urllib.error

GATEWAY_URL = "https://api.llmgateway.io/v1/chat/completions"
API_KEY = "llmgtwy_dnteDMFXS2C32f8Y5f1OLvvJgs3fqvZtQPNiWhiW"
MODEL = "gemini-2.5-flash-image"
OUTPUT_DIR = os.path.join("reader", "images")

STYLE_PREFIX = (
    "Generate a 21:9 ultrawide panoramic image. Style: moody, atmospheric, "
    "painterly with muted desaturated warm tones. No text or watermarks. "
)

# All 30 image prompts: (filename, prompt)
PROMPTS = [
    # Scene 1: Brooklyn Summer
    ("brooklyn-bg.png",
     STYLE_PREFIX + "Panoramic dusk skyline of lower Manhattan seen from across the East River. Deep indigo sky bleeding into rose and amber at the horizon. City lights just beginning to flicker on. Neon reflections in calm water. Slightly impressionistic, warm muted palette."),
    ("brooklyn-mid.png",
     STYLE_PREFIX + "Old Brooklyn waterfront — rusted warehouse silhouettes, graffiti-streaked fences, cobblestone street edge. Seen from pier level. Dark shapes against sunset glow. Industrial romance. Elements on dark background, suitable for layering."),
    ("brooklyn-fg.png",
     STYLE_PREFIX + "Wooden pier railing in close-up, slightly out of focus. Iron bollards. The railing frames the view like a theatre proscenium. Dark, nearly silhouetted, weathered wood and iron. Elements on dark background, suitable for layering."),

    # Scene 2: Pancakes
    ("pancakes-bg.png",
     STYLE_PREFIX + "Soft golden morning light streaming through a kitchen window. Warm amber and honey tones. Light rays catching dust motes, casting long warm shadows. Slightly overexposed, dreamy quality. Vermeer-like light in a warm kitchen."),
    ("pancakes-mid.png",
     STYLE_PREFIX + "A cast iron skillet seen from above with a single golden pancake. Steam wisps rising. Butter melting. Painterly, slightly abstracted. Warm golden-brown tones. Elements on dark background, suitable for layering."),
    ("pancakes-fg.png",
     STYLE_PREFIX + "Close-up: syrup bottle edge, a fork, the curve of a plate rim. Domestic still life fragments, slightly blurred. Dark maple-amber tones. Elements on dark background, suitable for layering."),

    # Scene 3: Reflection
    ("reflection-bg.png",
     STYLE_PREFIX + "Twilight sky — deep indigo with the last bleeding edge of rose at the horizon. Stars just emerging, faint pinpricks. Vast, bruise-colored sky. Moody and contemplative."),
    ("reflection-mid.png",
     STYLE_PREFIX + "Perfectly still dark water surface reflecting a twilight sky. The reflection is slightly distorted — stars wobble. A sense of depth pulling downward. Dark, glassy, mysterious. Elements on dark background."),
    ("reflection-fg.png",
     STYLE_PREFIX + "Shore edge — dark reeds and grass silhouettes framing the bottom of the scene. Twilight water beyond. Dark edges, suitable for layering on dark background."),

    # Scene 4: Misfits
    ("misfits-bg.png",
     STYLE_PREFIX + "Grand Southern reception hall — high walls with ornate portrait frames, crystal chandelier light casting warm pools. Everything bathed in a deep red-amber wash. Portraits of stern old men. Oil-painting quality."),
    ("misfits-mid.png",
     STYLE_PREFIX + "Round banquet table from slightly above — white tablecloth, congealed food, half-empty wine glasses. Red napkins. The detritus of a formal meal. Red tones dominate. Elements on dark background."),
    ("misfits-fg.png",
     STYLE_PREFIX + "Close-up: the edge of a wedding cake, gleaming steel knife catching light. A single red rose petal on white tablecloth. Dark foreground framing. Elements on dark background."),

    # Scene 5: Constance
    ("constance-bg.png",
     STYLE_PREFIX + "Night highway stretching to a vanishing point. Total darkness except for the cone of headlights illuminating asphalt. Stars or distant city glow on the horizon. Hypnotic, menacing perspective. Deep blacks and cool grays."),
    ("constance-mid.png",
     STYLE_PREFIX + "Highway guardrails rushing past — metal barriers catching headlight glare, motion-blurred. Sense of speed and enclosure. Streaked light on metal. Elements on dark background."),
    ("constance-fg.png",
     STYLE_PREFIX + "Interior car view elements — dark frame of a rearview mirror, dashboard edge, silhouette of an umbrella handle. Intimate, claustrophobic framing. Nearly black except for reflected highlights. Elements on dark background."),

    # Scene 6: Uncle
    ("uncle-bg.png",
     STYLE_PREFIX + "Hotel swimming pool seen from underwater — the surface above ripples with light, chlorine blue-green. Everything slightly distorted, compressed, pressure-heavy. Cold institutional blue. Subtle trickles of red dissolving in the water."),
    ("uncle-mid.png",
     STYLE_PREFIX + "Hospital corridor — fluorescent light, linoleum floor, trailing IV tubes and wires. Long perspective vanishing point. Sterile, grey-blue, empty. A single figure far down the hallway. Elements on dark background."),
    ("uncle-fg.png",
     STYLE_PREFIX + "Car backseat view — dark edge of a car window, seatbelt crossing frame, a child's hand pressed against glass. Cramped, confined perspective. Dark with reflected highway lights. Elements on dark background."),

    # Scene 7: Doorjam
    ("doorjam-bg.png",
     STYLE_PREFIX + "A house consumed by fire at night — roaring masts of smoke silhouetted against orange-red sky. Structure barely visible through flames. Apocalyptic warmth. Deep amber and charcoal."),
    ("doorjam-mid.png",
     STYLE_PREFIX + "An ornate carved wooden door — eagles, ships, frontiersmen, fireworks etched in woodgrain. Carvings glow from within as if lit by fire behind. Smoke curling around edges. Gothic detail, museum quality. Elements on dark background."),
    ("doorjam-fg.png",
     STYLE_PREFIX + "Bloodied fingertips pressed against wood grain. Splintered, desperate. Close-up, nearly abstract. Dark except for red of fingertips and grain of oak catching firelight. Elements on dark background."),

    # Scene 8: Drown
    ("drown-bg.png",
     STYLE_PREFIX + "Storm sky split by jagged lightning — charcoal clouds cracking with white-blue electric light. Mountainous ocean waves below. Overwhelming scale. Dark blue-black with violent white flashes."),
    ("drown-mid.png",
     STYLE_PREFIX + "A ship's spotlight beam cutting through rain and spray — a single column of piercing white light sweeping across churning black water. The beam is the focal point, searching. Elements on dark background."),
    ("drown-fg.png",
     STYLE_PREFIX + "Close-up: hands clawing upward from water — fingers breaking the surface, grasping at air. Rain streaking past. Dark, desperate, elemental. Hands barely above waterline. Elements on dark background."),

    # Scene 9: Beloved Creation
    ("beloved-bg.png",
     STYLE_PREFIX + "Electric summer night sky — a single massive lightning bolt connecting heaven to earth. Purple-black sky crackling with energy. Gothic grandeur. The bolt illuminates everything for an instant."),
    ("beloved-mid.png",
     STYLE_PREFIX + "Laboratory scene — silhouette of a figure on a table, wires and apparatus surrounding it. Warm amber light emanating from the figure's chest area, contrasting with cold blue lab. Frankenstein reimagined with tenderness. Elements on dark background."),
    ("beloved-fg.png",
     STYLE_PREFIX + "Two hands reaching toward each other — one smooth, one scarred with visible suture lines. Almost touching. Warm light between them. Michelangelo's Creation of Adam reimagined with gentleness and scars. Elements on dark background."),

    # Scene 10: Transcendent Love
    ("transcendent-bg.png",
     STYLE_PREFIX + "Sky splitting open — streams of golden-white light ripping through a dark storm. Light curves and flows like sound waves made visible. Rain falls through light beams. Celestial, rapturous."),
    ("transcendent-mid.png",
     STYLE_PREFIX + "Two figures dancing in rain — silhouetted, embracing, spinning. Trees around them bend in wind. Lightning illuminates them from behind. The dance is the stillness at the center of the storm. Elements on dark background."),
    ("transcendent-fg.png",
     STYLE_PREFIX + "Rain streaking past in close-up — individual droplets caught mid-fall, lit from behind by golden light. The rain is almost musical, each drop a note. Warm gold through cold water. Elements on dark background."),
]


def generate_image(prompt, filename, retries=2):
    """Call the gateway and save the resulting image."""
    payload = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    req = urllib.request.Request(
        GATEWAY_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            # Extract image from response
            choices = data.get("choices", [])
            if not choices:
                print(f"  WARNING: No choices in response for {filename}")
                return False

            msg = choices[0].get("message", {})
            images = msg.get("images", [])

            if not images:
                print(f"  WARNING: No images in response for {filename}")
                return False

            # Get the base64 data
            img_url = images[0].get("image_url", {}).get("url", "")
            if not img_url.startswith("data:"):
                print(f"  WARNING: Unexpected image format for {filename}")
                return False

            # Decode and save
            _, b64_data = img_url.split(",", 1)
            img_bytes = base64.b64decode(b64_data)

            output_path = os.path.join(OUTPUT_DIR, filename)
            with open(output_path, "wb") as f:
                f.write(img_bytes)

            size_kb = len(img_bytes) / 1024
            print(f"  Saved {filename} ({size_kb:.0f} KB)")
            return True

        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            print(f"  HTTP {e.code} for {filename}: {body[:200]}")
            if attempt < retries and e.code in (429, 500, 502, 503):
                wait = (attempt + 1) * 5
                print(f"  Retrying in {wait}s...")
                time.sleep(wait)
            else:
                return False
        except Exception as e:
            print(f"  Error for {filename}: {e}")
            if attempt < retries:
                time.sleep(3)
            else:
                return False

    return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = len(PROMPTS)
    success = 0
    failed = []

    print(f"Generating {total} images via Gemini...\n")

    for i, (filename, prompt) in enumerate(PROMPTS):
        # Skip if already exists
        output_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print(f"[{i+1}/{total}] {filename} — already exists, skipping")
            success += 1
            continue

        print(f"[{i+1}/{total}] Generating {filename}...")
        if generate_image(prompt, filename):
            success += 1
        else:
            failed.append(filename)

        # Rate limiting — 2 seconds between requests
        if i < total - 1:
            time.sleep(2)

    print(f"\nDone: {success}/{total} images generated")
    if failed:
        print(f"Failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
