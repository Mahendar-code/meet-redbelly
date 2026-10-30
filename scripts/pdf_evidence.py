#!/usr/bin/env python3
"""Render highlighted crops of the PDF quotes for the evidence captures.

For every quote on a PDF source, the script downloads the PDF, finds each
fragment on the stated page, draws a red box around it, covers banned terms
with solid boxes, and saves a crop to evidence/.raw/<quote id>-pdf.png.
capture_evidence.mjs then adds the header.

Needs: pdfplumber (which brings pypdfium2) and Pillow.
Usage: python3 scripts/pdf_evidence.py
"""

import io
import json
import pathlib
import re
import sys

import pdfplumber
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sourcelib import fetch, normalise  # noqa: E402
from terms import BANNED  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "evidence" / ".raw"
DPI = 120
RED = (239, 83, 80)


def fragment_regex(fragment):
    # Tolerate line breaks, PDF hyphenation and curly quotes between words.
    words = normalise(fragment).split(" ")
    parts = []
    for w in words:
        w = re.escape(w).replace("'", "['\u2019]")
        parts.append(w.replace(r"\-", r"-\s*"))
    return r"\s+".join(parts)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    sources = json.loads((ROOT / "content" / "sources.json").read_text())["sources"]
    for s in sources:
        if s["type"] != "pdf":
            continue
        pdf = pdfplumber.open(io.BytesIO(fetch(s["url"])))
        for q in s["quotes"]:
            page = pdf.pages[q["page"] - 1]
            scale = DPI / 72
            img = page.to_image(resolution=DPI).original.convert("RGB")
            draw = ImageDraw.Draw(img, "RGBA")
            boxes = []
            for frag in q["fragments"]:
                hits = page.search(fragment_regex(frag), regex=True, case=False)
                if not hits:
                    raise SystemExit(f"{q['id']}: fragment not found on page {q['page']}: {frag[:60]}")
                for ch in hits[0]["chars"]:
                    boxes.append((ch["x0"], ch["top"], ch["x1"], ch["bottom"]))
            # Merge character boxes into one box per text line.
            lines = {}
            for x0, top, x1, bottom in boxes:
                key = round(top)
                l = lines.setdefault(key, [x0, top, x1, bottom])
                l[0], l[1], l[2], l[3] = min(l[0], x0), min(l[1], top), max(l[2], x1), max(l[3], bottom)
            for x0, top, x1, bottom in lines.values():
                r = [x0 * scale - 4, top * scale - 3, x1 * scale + 4, bottom * scale + 3]
                draw.rectangle(r, fill=RED + (30,), outline=RED, width=3)
            for _, rx in BANNED:
                for hit in page.search(rx.pattern, regex=True, case=False):
                    draw.rectangle([hit["x0"] * scale - 2, hit["top"] * scale - 2,
                                    hit["x1"] * scale + 2, hit["bottom"] * scale + 2], fill=(12, 19, 23, 255))
            ys = [v[1] for v in lines.values()] + [v[3] for v in lines.values()]
            top = max(0, min(ys) * scale - 140)
            bottom = min(img.height, max(ys) * scale + 140)
            crop = img.crop((0, int(top), img.width, int(bottom)))
            if crop.width > 1240:
                crop = crop.resize((1240, int(crop.height * 1240 / crop.width)), Image.LANCZOS)
            crop.save(RAW / f"{q['id']}-pdf.png")
            print("ok  ", q["id"], "page", q["page"])


if __name__ == "__main__":
    main()
