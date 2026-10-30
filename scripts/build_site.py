#!/usr/bin/env python3
"""Build site/index.html from content/*.json and copy what the page links to.

The site is fully static and self-contained: fonts, images, audio, evidence
and downloads all live under site/, so the folder can be served as is.

Usage: python3 scripts/build_site.py
"""

import html
import json
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_docs import POSTS, QUOTES, SOURCES, VERIFIED, capture_status, claims_for_source, post_sources, quote_text, where  # noqa: E402
from verify import x_length  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
thread = json.loads((ROOT / "content/thread.json").read_text())
src_doc = json.loads((ROOT / "content/sources.json").read_text())
narration = json.loads((SITE / "assets/audio/thread-narration.json").read_text())
checks_file = ROOT / "evidence/checks.json"
checks = json.loads(checks_file.read_text()) if checks_file.exists() else None
e = html.escape
N = len(POSTS)


def copy_assets():
    dl = SITE / "downloads"
    dl.mkdir(exist_ok=True)
    for f in ["THREAD.md", "SOURCES.md", "redbelly-thread.docx", "redbelly-thread.pdf"]:
        shutil.copy2(ROOT / "submission" / f, dl / f)
    shutil.copy2(ROOT / "docs/FACT_CHECK.md", dl / "FACT_CHECK.md")
    for sub in ["captures", "manual"]:
        dst = SITE / "evidence" / sub
        if dst.exists():
            shutil.rmtree(dst)
        src = ROOT / "evidence" / sub
        if src.exists():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.md", "*.json"))
        else:
            dst.mkdir(parents=True)


def post_html(p):
    sources = "".join(f'<a class="chip" href="#source-{s}">{s}</a>' for s in post_sources(p))
    img = ""
    if p["image"]:
        f = p["image"]["file"]
        img = (f'<figure><a href="assets/img/thread/{f}"><img src="assets/img/thread/{f}" width="1600" height="900" '
               f'loading="lazy" alt="{e(p["image"]["alt"])}"></a></figure>'
               f'<details><summary>Alt text for this image</summary><p>{e(p["image"]["alt"])}</p></details>')
    return f"""
<li class="post" id="post-{p['n']}">
  <span class="num" aria-hidden="true">{p['n']}/{N}</span>
  <article class="card" aria-label="Post {p['n']} of {N}">
    <div class="card-head">
      <span class="mono">{x_length(p['text'])}/280 characters</span>
      <span class="tools">
        <button class="btn small" type="button" data-play="{p['n']}" aria-label="Play narration from post {p['n']}">Play</button>
        <button class="btn small" type="button" data-copy-post="{p['n']}">Copy</button>
      </span>
    </div>
    <p class="post-text" id="text-{p['n']}">{e(p['text'])}</p>
    {img}
    <div class="card-foot"><span class="label">Sources</span>{sources}<a class="chip" href="#fact-{p['n']}">{len(p['claims'])} claims checked</a></div>
  </article>
</li>"""


def source_html(s):
    tag = '<span class="status ok">Task resource</span>' if s.get("task_resource") else ""
    return f"""
<article class="card source" id="source-{s['id']}">
  <p class="label">{s['id']}</p>
  <h3>{e(s['title'])}</h3>
  <p>{e(s['publisher'])}. Accessed {VERIFIED}.</p>
  <a class="url" href="{e(s['url'])}" rel="noopener noreferrer">{e(s['url'])}</a>
  <p>Supports {', '.join(claims_for_source(s['id']))}. {len(s['quotes'])} quotes.</p>
  {tag}
</article>"""


def fact_html(p):
    rows = []
    for c in p["claims"]:
        qs = []
        for qid in c["evidence"]:
            s, q = QUOTES[qid]
            path, status = capture_status(qid)
            cls = "ok" if status != "Manual screenshot pending" else "warn"
            link = (f'<a href="{path}">View screenshot</a>' if (ROOT / path).exists() else "")
            qs.append(f"""<div class="quote"><q>{e(quote_text(q))}</q>
  <div class="meta"><span class="mono">{qid} | {e(where(qid))}</span><span class="status {cls}">{status}</span>{link}
  <a href="{e(s['url'])}" rel="noopener noreferrer">Open source</a></div></div>""")
        rows.append(f'<div class="claim"><h4><span class="mono">{c["id"]}</span>{e(c["text"])}</h4>{"".join(qs)}</div>')
    return f"""
<details class="card fc" id="fact-{p['n']}">
  <summary><span class="mono">{p['n']}/{N}</span>{e(p['text'].split(chr(10))[0])}</summary>
  <div class="claims">{''.join(rows)}</div>
</details>"""


def checks_html():
    if not checks:
        return '<p class="checks-meta">Run python3 scripts/verify.py to fill this in.</p>'
    cls = {"PASS": "ok", "FAIL": "bad", "WARN": "warn", "PENDING": "warn"}
    c = checks["counts"]
    items = "".join(
        f'<li><span class="status {cls[r["status"]]}">{r["status"]}</span><span>{e(r["check"])}'
        + (f'<small>{e(r["detail"])}</small>' if r["detail"] and r["status"] != "PASS" else "")
        + "</span></li>" for r in checks["results"])
    return (f'<p class="checks-meta">Last run {checks["ran"]}{" with live source checks" if checks["live"] else ""}. '
            f'{c["PASS"]} passed, {c["FAIL"]} failed, {c["WARN"]} warnings, {c["PENDING"]} pending.</p>'
            f'<ul class="checks">{items}</ul>')


def page():
    total_claims = sum(len(p["claims"]) for p in POSTS)
    n_img = sum(1 for p in POSTS if p["image"])
    passed = f'{checks["counts"]["PASS"]} of {len(checks["results"])}' if checks else "not run"
    mins, secs = divmod(round(narration["duration"]), 60)
    nar = json.dumps({"posts": narration["posts"], "cues": narration["cues"]}).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Redbelly Without the Jargon</title>
<meta name="description" content="A nine post X thread that explains Redbelly in everyday words, with images, narration, sources and a claim by claim fact check.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0c1317">
<meta property="og:title" content="Redbelly Without the Jargon">
<meta property="og:description" content="Real assets. Verified people. Rules built in.">
<meta property="og:image" content="assets/img/og-image.png">
<link rel="icon" href="assets/img/dao-icon.png">
<link rel="stylesheet" href="assets/css/tokens.css">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<a class="skip" href="#thread">Skip to the thread</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="#top" aria-label="Back to top">
      <img class="logo-dark" src="assets/img/dao-logo-on-dark.png" alt="Redbelly DAO" width="56" height="40">
      <img class="logo-light" src="assets/img/dao-logo-on-light.png" alt="Redbelly DAO" width="56" height="40">
    </a>
    <nav aria-label="Sections">
      <a href="#thread">Thread</a><a href="#sources">Sources</a><a href="#fact-check">Fact check</a>
      <a href="#checks">Checks</a><a href="#downloads">Downloads</a>
    </nav>
    <button class="btn small" id="theme" type="button">Light theme</button>
  </div>
</header>

<main id="top">
<div class="hero">
  <div class="wrap">
    <p class="label">X thread entry | Redbelly DAO Task Board</p>
    <h1>Redbelly, explained <em>without the jargon</em>.</h1>
    <p>{N} posts that explain what Redbelly does and why it matters, for a friend, a parent or a business owner. Every fact is traced to a public source, quote by quote.</p>
    <ul class="stats">
      <li>{N} <span>posts</span></li><li>{n_img} <span>images</span></li><li>{total_claims} <span>claims</span></li>
      <li>{len(QUOTES)} <span>quotes</span></li><li>{len(SOURCES)} <span>sources</span></li><li>{passed} <span>checks passed</span></li>
    </ul>
    <div class="actions">
      <button class="btn primary" type="button" id="copy-all">Copy whole thread</button>
      <a class="btn" href="#fact-check">See the fact check</a>
    </div>
  </div>
</div>
<div class="notice"><div class="wrap"><span class="status warn">Before judging</span><span>Do not share this page or post the thread publicly before judging. The DAO posts the winning entry.</span></div></div>

<section class="block" id="thread">
  <div class="wrap">
    <p class="label">The entry</p>
    <h2>The thread</h2>
    <p class="intro">Post 1 goes first, and each later post is a reply to the one before it. Images go on posts {', '.join(str(p['n']) for p in POSTS if p['image'])}, each with its alt text.</p>
    <div class="thread-grid">
      <ol class="posts">{''.join(post_html(p) for p in POSTS)}
      </ol>
      <aside class="side">
        <div class="card panel">
          <p class="label">Listen</p>
          <h3>The thread, read aloud</h3>
          <p>Narrated with the Kokoro open model, voice af_heart. {mins} min {secs:02d} s. The post being read is highlighted.</p>
          <audio id="narration" controls preload="metadata">
            <source src="assets/audio/thread-narration.mp3" type="audio/mpeg">
            <track kind="captions" src="assets/audio/thread-narration.vtt" srclang="en" label="English" default>
          </audio>
          <div class="now" id="now" aria-live="polite"><span class="mono">Ready</span>Press play, or use Play on any post.</div>
        </div>
        <div class="card panel">
          <p class="label">Ground rules followed</p>
          <p>No B-word or stand-in for it, no price talk, no personal credit, no emoji, no em dashes. Checked by script on every build.</p>
          <a class="btn" href="#checks">See all checks</a>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="block" id="sources">
  <div class="wrap">
    <p class="label">Deliverable 2</p>
    <h2>Sources</h2>
    <p class="intro">Every fact comes from these {len(SOURCES)} public sources. Redbelly's own pages explain what it does. The Reserve Bank of Australia's releases and final report back up everything about Project Acacia.</p>
    <div class="grid">{''.join(source_html(s) for s in src_doc['sources'])}</div>
  </div>
</section>

<section class="block" id="fact-check">
  <div class="wrap">
    <p class="label">Verification</p>
    <h2>Fact check, claim by claim</h2>
    <p class="intro">Each post is broken into the claims it makes. Each claim links to verbatim quotes, with a screenshot of the quote highlighted on the source. Banned words in source pages are blacked out in the screenshots.</p>
    {''.join(fact_html(p) for p in POSTS)}
  </div>
</section>

<section class="block" id="checks">
  <div class="wrap">
    <p class="label">Automated checks</p>
    <h2>What the build checks</h2>
    <p class="intro">scripts/verify.py runs these checks on the whole package, not just the posts. It needs only Python. Add --live to re-check every quote against the live sources.</p>
    {checks_html()}
  </div>
</section>

<section class="block" id="downloads">
  <div class="wrap">
    <p class="label">Files</p>
    <h2>Downloads</h2>
    <p class="intro">The submission document comes in three formats with the same text. Images are 1600 x 900 PNG, the brand kit size for an X single image post.</p>
    <div class="downloads">
      <a class="btn primary" href="downloads/redbelly-thread.docx" download>Thread (DOCX)</a>
      <a class="btn" href="downloads/redbelly-thread.pdf" download>Thread (PDF)</a>
      <a class="btn" href="downloads/THREAD.md" download>Thread (Markdown)</a>
      <a class="btn" href="downloads/SOURCES.md" download>Sources</a>
      <a class="btn" href="downloads/FACT_CHECK.md" download>Fact check</a>
      {''.join(f'<a class="btn" href="assets/img/thread/{p["image"]["file"]}" download>Image for post {p["n"]}</a>' for p in POSTS if p['image'])}
      <a class="btn" href="assets/audio/thread-narration.mp3" download>Narration (MP3)</a>
      <a class="btn" href="assets/audio/thread-narration.vtt" download>Captions (VTT)</a>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <p>Prepared for the Redbelly DAO Community Task Board. Facts last verified {VERIFIED}.</p>
    <p>This explains what Redbelly does. It is not financial advice, and it says nothing about prices or returns.</p>
    <p>Fonts: Be Vietnam Pro and JetBrains Mono (SIL Open Font License). Logo from the DAO Task Board brand kit. Narration: Kokoro-82M (Apache 2.0).</p>
  </div>
</footer>
<div class="toast" id="toast" role="status"></div>
<script type="application/json" id="narration-data">{nar}</script>
<script src="assets/js/site.js"></script>
</body>
</html>
"""


def main():
    copy_assets()
    (SITE / "index.html").write_text(page())
    print("wrote site/index.html")


if __name__ == "__main__":
    main()
