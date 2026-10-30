"""Fetch, extract, normalise and search source documents.

Used by snapshot_sources.py (to save redacted text snapshots into
evidence/snapshots) and by verify.py (to check every quote against those
snapshots, or against the live pages with --live).
"""

import io
import re
import shutil
import subprocess
import tempfile
import unicodedata
import urllib.request
from html.parser import HTMLParser

from terms import redact

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


class _Text(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "template"}
    BREAK = {"p", "div", "h1", "h2", "h3", "h4", "h5", "li", "br", "section",
             "tr", "td", "a", "span", "button", "article", "header", "footer"}

    def __init__(self):
        super().__init__()
        self.out = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag in self.BREAK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def html_to_text(raw):
    p = _Text()
    p.feed(raw.decode("utf-8", errors="ignore"))
    lines = [re.sub(r"\s+", " ", l).strip() for l in "".join(p.out).split("\n")]
    out, prev = [], None
    for l in lines:
        if l and l != prev:
            out.append(l)
        prev = l
    return "\n".join(out)


def pdf_to_pages(raw):
    """Return a list of page texts. Uses pdftotext if present, else pypdf."""
    if shutil.which("pdftotext"):
        with tempfile.TemporaryDirectory() as d:
            src = f"{d}/in.pdf"
            open(src, "wb").write(raw)
            txt = subprocess.run(["pdftotext", src, "-"], capture_output=True,
                                 check=True).stdout.decode("utf-8", "ignore")
        pages = txt.split("\f")
        return pages[:-1] if pages and not pages[-1].strip() else pages
    from pypdf import PdfReader  # optional dependency
    return [p.extract_text() or "" for p in PdfReader(io.BytesIO(raw)).pages]


_QUOTES = {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
           "\u2013": "-", "\u2014": "-", "\u2012": "-", "\u2015": "-",
           "\u00a0": " ", "\u00ad": ""}


def normalise(text):
    text = unicodedata.normalize("NFKC", text)
    for a, b in _QUOTES.items():
        text = text.replace(a, b)
    # Rejoin words hyphenated across PDF line breaks, then collapse whitespace.
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    return re.sub(r"\s+", " ", text).strip()


def snapshot_text(source, raw):
    """Build the stored snapshot: normalised, redacted, with page markers for PDFs."""
    if source["type"] == "pdf":
        parts = [f"[[page {i}]] {normalise(p)}" for i, p in enumerate(pdf_to_pages(raw), 1)]
        return redact("\n".join(parts)) + "\n"
    return redact(normalise(html_to_text(raw))) + "\n"


def find_quote(snapshot, quote):
    """True if all fragments appear in order (on the stated PDF page, if any)."""
    hay = snapshot
    if quote.get("page"):
        m = re.search(r"\[\[page %d\]\](.*?)(?=\n\[\[page \d+\]\]|\Z)" % quote["page"],
                      snapshot, re.S)
        if not m:
            return False
        hay = m.group(1)
    hay = normalise(redact(hay)).lower()
    pos = 0
    for frag in quote["fragments"]:
        i = hay.find(normalise(frag).lower(), pos)
        if i < 0:
            return False
        pos = i + len(frag)
    return True
