#!/usr/bin/env python3
"""Build the submission documents from content/*.json.

Writes:
  submission/THREAD.md            the entry as text, ready to paste into X
  submission/SOURCES.md           deliverable 2: the sources used for every fact
  submission/redbelly-thread.docx the entry as a Word document, images attached
  design/print/submission.html    print layout used by build_pdf.mjs for the PDF
  docs/FACT_CHECK.md              claim by claim evidence matrix

Needs python-docx for the DOCX (pip install python-docx). Everything else is stdlib.
Usage: python3 scripts/build_docs.py
"""

import html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from verify import x_length  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
thread = json.loads((ROOT / "content/thread.json").read_text())
src_doc = json.loads((ROOT / "content/sources.json").read_text())
SOURCES = {s["id"]: s for s in src_doc["sources"]}
QUOTES = {q["id"]: (s, q) for s in src_doc["sources"] for q in s["quotes"]}
POSTS = thread["posts"]
N = len(POSTS)
VERIFIED = "30 October 2026"
CLAIM_INDEX = {c["id"]: p["n"] for p in POSTS for c in p["claims"]}


def quote_text(q):
    return " [...] ".join(q["fragments"])


def where(qid):
    s, q = QUOTES[qid]
    return f"{s['id']} PDF p.{q['page']} (printed p.{q['printed_page']})" if q.get("page") else s["id"]


def post_sources(p):
    seen = []
    for c in p["claims"]:
        for e in c["evidence"]:
            sid = QUOTES[e][0]["id"]
            if sid not in seen:
                seen.append(sid)
    return sorted(seen)


def claims_for_source(sid):
    return sorted({c["id"] for p in POSTS for c in p["claims"] for e in c["evidence"] if QUOTES[e][0]["id"] == sid})


def capture_status(qid):
    q = QUOTES[qid][1]
    if q.get("manual_capture"):
        done = (ROOT / "evidence/manual" / f"{qid}.png").exists()
        return (f"evidence/manual/{qid}.png", "Manual screenshot added" if done else "Manual screenshot pending")
    return (f"evidence/captures/{qid}.png", "Captured automatically")


# ---------------------------------------------------------------- THREAD.md
def thread_md():
    imgs = [p["n"] for p in POSTS if p["image"]]
    out = [
        f"# {thread['title']}",
        "",
        f"Format: X thread, {N} posts. Images: {len(imgs)} PNG files at 1600 x 900, attached to posts "
        + ", ".join(map(str, imgs[:-1])) + f" and {imgs[-1]}. Facts last verified {VERIFIED}.",
        "",
        "Each post is in a plain text block so it can be copied exactly. The character count uses X's rules "
        "(a link counts as 23). Sources for every fact are listed in SOURCES.md, and the claim by claim "
        "evidence is in docs/FACT_CHECK.md.",
        "",
    ]
    for p in POSTS:
        out += [f"## Post {p['n']} of {N}", "", "```text", p["text"], "```", "",
                f"- Characters: {x_length(p['text'])} of 280"]
        if p["image"]:
            out += [f"- Image: `images/{p['image']['file']}`", f"- Alt text: {p['image']['alt']}"]
        else:
            out += ["- Image: none"]
        out += ["- Sources: " + ", ".join(post_sources(p)), ""]
    out += ["## Posting notes", "",
            "- Post 1 first, then reply to each post with the next one, in order.",
            "- Attach each image to the post listed above and paste its alt text into X's description field.",
            "- Post 9 carries the only link in the thread.",
            "- Do not post publicly before judging. The DAO posts the winning entry.", ""]
    return "\n".join(out)


# ---------------------------------------------------------------- SOURCES.md
def sources_md():
    out = [f"# Sources", "",
           f"Every fact in the thread comes from the public sources below. All were read and checked on "
           f"{VERIFIED}. Quotes are verbatim; [...] marks text left out. Each quote also has a screenshot in "
           "`evidence/captures/` and a saved text copy in `evidence/snapshots/`.", ""]
    for s in src_doc["sources"]:
        tag = " (task resource)" if s.get("task_resource") else ""
        out += [f"## {s['id']}. {s['title']}{tag}", "",
                f"- Publisher: {s['publisher']}",
                f"- Link: <{s['url']}>",
                f"- Accessed: {VERIFIED}",
                f"- Supports claims: {', '.join(claims_for_source(s['id']))}",
                "- Quotes:"]
        for q in s["quotes"]:
            page = f" (PDF page {q['page']}, printed page {q['printed_page']})" if q.get("page") else ""
            out.append(f"  - `{q['id']}`{page}: \"{quote_text(q)}\"")
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- FACT_CHECK.md
def fact_check_md():
    total_claims = sum(len(p["claims"]) for p in POSTS)
    out = ["# Fact check", "",
           f"{total_claims} claims across {N} posts. Each claim is written out in plain words, then tied to "
           "verbatim quotes from the sources. `python3 scripts/verify.py` confirms every quote is present in "
           "the saved source text (and, with `--live`, on the live page today).", "",
           "Status key: Captured automatically means a screenshot with the quote highlighted is in "
           "`evidence/captures/`. Manual screenshot pending means the text is verified but the page could not "
           "be captured automatically; see `evidence/manual/README.md`.", ""]
    for p in POSTS:
        out += [f"## Post {p['n']}", "", "```text", p["text"], "```", ""]
        for c in p["claims"]:
            out += [f"### {c['id']}. {c['text']}", ""]
            for e in c["evidence"]:
                s, q = QUOTES[e]
                path, status = capture_status(e)
                out += [f"- `{e}` from {where(e)}, {s['publisher']}: \"{quote_text(q)}\"",
                        f"  - {status}: `{path}`"]
            out.append("")
    out += ["## Judgement calls", "",
            "- Post 1 says Redbelly is a public network. The RBA final report lists it as public (S10-Q1) and "
            "public-permissioned (S10-Q2). Public is the plain word for both.",
            "- Post 2 describes how traditional finance works, not Redbelly. It paraphrases the RBA report's "
            "description of separate institutions and manual reconciliation (S10-Q4) and makes no time claim.",
            "- Post 3's concert ticket is an analogy. The fund unit in image 3 is labelled as an illustrative "
            "example, not a real product.",
            "- Post 4 says privacy tech means being verified does not mean showing everyone your details. "
            "Redbelly's own wording is that participants verify their identities while privacy is protected "
            "through zero-knowledge proofs (S03-Q4).",
            "- Post 7 says Project Acacia was run by the RBA and the Digital Finance CRC. Both RBA media releases "
            "call it a joint initiative (S08-Q1).",
            "- Posts 7 and 8 avoid saying Redbelly partnered with, or was approved by, the RBA. Redbelly's own "
            "FAQ says it was not (S04-Q2), and post 8 says so in plain words.",
            "- Post 9 says trades can settle instantly. This is Tokeniser's stated T+0 settlement (S07-Q9) and "
            "Redbelly's deterministic finality (S12-Q6). It is a capability, not a promise about any asset.",
            "- No post mentions a token, a price or an investment outcome.", ""]
    return "\n".join(out)


# ---------------------------------------------------------------- print HTML for the PDF
def print_html():
    e = html.escape
    rows = []
    for p in POSTS:
        img = ""
        if p["image"]:
            img = (f'<figure><img src="../../submission/images/{p["image"]["file"]}" alt="{e(p["image"]["alt"])}">'
                   f'<figcaption><b>Alt text.</b> {e(p["image"]["alt"])}</figcaption></figure>')
        rows.append(
            f'<section class="post"><div class="meta"><span>Post {p["n"]} of {N}</span>'
            f'<span>{x_length(p["text"])} / 280</span></div>'
            f'<div class="text">{e(p["text"])}</div>{img}'
            f'<div class="src">Sources: {", ".join(post_sources(p))}</div></section>')
    srcs = []
    for s in src_doc["sources"]:
        srcs.append(f'<li><b>{s["id"]}. {e(s["title"])}</b><br>{e(s["publisher"])}. '
                    f'<span class="url">{e(s["url"])}</span><br>Accessed {VERIFIED}. '
                    f'Supports {", ".join(claims_for_source(s["id"]))}.</li>')
    fonts = "".join(
        f'@font-face{{font-family:"Be Vietnam Pro";font-weight:{w};src:url("../../site/assets/fonts/BeVietnamPro-{w}.woff2")}}'
        for w in (400, 500, 600, 700))
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<title>{e(thread['title'])}</title>
<link rel="stylesheet" href="../../site/assets/css/tokens.css">
<style>
{fonts}
@font-face{{font-family:"JetBrains Mono";src:url("../../site/assets/fonts/JetBrainsMono-var.woff2")}}
@page {{ size: A4; margin: 18mm 16mm; }}
body {{ font-family: var(--font-sans); color: var(--on-surface); background: #FFFFFF; font-size: 10.5pt; line-height: 1.5; margin: 0; }}
h1 {{ font-size: 24pt; line-height: 1.15; letter-spacing: -0.02em; margin: 0 0 6pt; }}
h2 {{ font-size: 14pt; margin: 18pt 0 8pt; }}
.label {{ font-size: 8pt; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--outline); }}
.lede {{ color: var(--on-surface-variant); max-width: 150mm; }}
.band {{ background: #1d3140; color: #f1f5f8; padding: 14pt 16pt; border-radius: 8px; margin-bottom: 14pt; }}
.band .label {{ color: #c2ced6; }}
.band p {{ color: #c2ced6; margin: 6pt 0 0; }}
.post {{ border: 1px solid var(--panel-edge); border-radius: 8px; padding: 10pt 12pt; margin: 0 0 10pt; break-inside: avoid; }}
.meta {{ display: flex; justify-content: space-between; font-family: var(--font-mono); font-size: 8pt; letter-spacing: 0.05em; color: var(--outline); border-bottom: 1px solid var(--panel-edge); padding-bottom: 5pt; margin-bottom: 7pt; }}
.text {{ white-space: pre-line; font-size: 11pt; }}
figure {{ margin: 8pt 0 0; }}
figure img {{ width: 100%; border-radius: 4px; display: block; }}
figcaption {{ font-size: 8.5pt; color: var(--on-surface-variant); margin-top: 4pt; }}
.src {{ font-family: var(--font-mono); font-size: 8pt; color: var(--primary); margin-top: 6pt; }}
ol {{ padding-left: 0; list-style: none; }}
li {{ margin-bottom: 7pt; break-inside: avoid; }}
.url {{ font-family: var(--font-mono); font-size: 8pt; color: var(--primary); word-break: break-all; }}
.note {{ font-size: 9pt; color: var(--on-surface-variant); }}
</style>
</head>
<body>
<div class="band"><div class="label">X thread entry</div><h1>{e(thread['title'])}</h1>
<p>{N} posts, {sum(1 for p in POSTS if p['image'])} images. Written for {e(thread['audience'].split(': ')[-1].rstrip('.'))}. Facts last verified {VERIFIED}.</p></div>
{''.join(rows)}
<h2>Sources</h2>
<p class="note">Quotes for every claim, with page numbers and screenshots, are in SOURCES.md and docs/FACT_CHECK.md.</p>
<ol>{''.join(srcs)}</ol>
</body>
</html>
"""


# ---------------------------------------------------------------- DOCX
def build_docx(path):
    from docx import Document
    from docx.enum.text import WD_BREAK
    from docx.shared import Inches, Pt, RGBColor

    ink, muted, accent = RGBColor(0x0F, 0x1A, 0x22), RGBColor(0x59, 0x69, 0x75), RGBColor(0xB3, 0x27, 0x2A)
    doc = Document()
    for st in ("Normal", "Title", "Heading 1", "Heading 2"):
        doc.styles[st].font.name = "Be Vietnam Pro"
        doc.styles[st].font.color.rgb = ink
    doc.styles["Normal"].font.size = Pt(10.5)
    doc.add_paragraph(thread["title"], style="Title")
    intro = doc.add_paragraph()
    intro.add_run(f"X thread entry. {N} posts, {sum(1 for p in POSTS if p['image'])} images (PNG, 1600 x 900). "
                  f"Facts last verified {VERIFIED}.").font.color.rgb = muted

    for p in POSTS:
        doc.add_heading(f"Post {p['n']} of {N}", level=2)
        para = doc.add_paragraph()
        lines = p["text"].split("\n")
        for i, line in enumerate(lines):
            para.add_run(line)
            if i < len(lines) - 1:
                para.add_run().add_break(WD_BREAK.LINE)
        meta = doc.add_paragraph()
        r = meta.add_run(f"{x_length(p['text'])} of 280 characters. Sources: {', '.join(post_sources(p))}.")
        r.font.size, r.font.color.rgb = Pt(8.5), muted
        if p["image"]:
            doc.add_picture(str(ROOT / "submission/images" / p["image"]["file"]), width=Inches(6.2))
            alt = doc.add_paragraph()
            a = alt.add_run("Alt text: ")
            a.bold, a.font.size = True, Pt(8.5)
            b = alt.add_run(p["image"]["alt"])
            b.font.size, b.font.color.rgb = Pt(8.5), muted
            doc.inline_shapes[-1]._inline.docPr.set("descr", p["image"]["alt"])

    doc.add_heading("Sources", level=1)
    for s in src_doc["sources"]:
        para = doc.add_paragraph()
        para.add_run(f"{s['id']}. {s['title']}").bold = True
        para.add_run(f"\n{s['publisher']}. {s['url']}\nAccessed {VERIFIED}. Supports {', '.join(claims_for_source(s['id']))}.")
    note = doc.add_paragraph()
    r = note.add_run("Verbatim quotes for every claim, with page numbers and screenshots, are in SOURCES.md and docs/FACT_CHECK.md.")
    r.font.size, r.font.color.rgb = Pt(8.5), accent
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    doc.core_properties.comments = ""
    doc.core_properties.title = thread["title"]
    doc.save(path)


def main():
    (ROOT / "submission").mkdir(exist_ok=True)
    (ROOT / "design/print").mkdir(parents=True, exist_ok=True)
    (ROOT / "submission/THREAD.md").write_text(thread_md())
    (ROOT / "submission/SOURCES.md").write_text(sources_md())
    (ROOT / "docs/FACT_CHECK.md").write_text(fact_check_md())
    (ROOT / "design/print/submission.html").write_text(print_html())
    build_docx(ROOT / "submission/redbelly-thread.docx")
    print("wrote THREAD.md, SOURCES.md, FACT_CHECK.md, submission.html, redbelly-thread.docx")


if __name__ == "__main__":
    main()
