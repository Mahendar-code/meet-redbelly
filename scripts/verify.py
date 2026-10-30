#!/usr/bin/env python3
"""Check the entry against the task rules and the DAO brand kit.

Runs with the Python standard library only. Every check prints PASS, FAIL,
WARN or PENDING. The script exits with code 1 if anything FAILs.

  python3 scripts/verify.py          offline: quotes checked against evidence/snapshots
  python3 scripts/verify.py --live   also re-download every source and check the quotes there

Results are also written to evidence/checks.json (read by the website).
"""

import argparse
import datetime
import json
import pathlib
import re
import shutil
import struct
import subprocess
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import terms  # noqa: E402
from sourcelib import find_quote, html_to_text, normalise  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXT_EXT = {".md", ".txt", ".json", ".html", ".css", ".js", ".mjs", ".py", ".sh",
            ".vtt", ".svg", ".xml", ".yml", ".yaml", ".conf", ".gitignore", ""}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".raw"}

results = []


def record(status, name, detail=""):
    results.append({"status": status, "check": name, "detail": detail})
    print(f"{status:<8}{name}" + (f"\n        {detail}" if detail and status != "PASS" else ""))


def ok_if(cond, name, detail_fail, detail_pass=""):
    record("PASS" if cond else "FAIL", name, detail_pass if cond else detail_fail)


def rel(p):
    return str(p.relative_to(ROOT))


def text_files():
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            if p.suffix in TEXT_EXT or p.name in {".gitignore", "LICENSE"}:
                yield p


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    xml = re.sub(r"</w:p>|<w:br/>", "\n", xml)
    return re.sub(r"<[^>]+>", "", xml)


def pdf_text(path):
    if shutil.which("pdftotext"):
        return subprocess.run(["pdftotext", str(path), "-"], capture_output=True).stdout.decode("utf-8", "ignore")
    try:
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
    except ImportError:
        return None


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


# X counts every URL as 23 characters and most Latin text as 1 per character.
URL = re.compile(r"(https?://\S+|\b[\w-]+\.(?:network|com|org|net|io|au|gov\.au)\b[^\s]*)", re.I)


def x_length(text):
    n = 0
    for ch in URL.sub("", text):
        cp = ord(ch)
        light = cp <= 4351 or 8192 <= cp <= 8205 or 8208 <= cp <= 8223 or 8242 <= cp <= 8247
        n += 1 if light else 2
    return n + 23 * len(URL.findall(text))


def words(text):
    text = text.lower().replace("tokenization", "tokenisation").replace("red belly", "redbelly")
    return re.findall(r"[a-z0-9']+", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="re-download sources and check quotes live")
    args = ap.parse_args()

    thread = json.loads((ROOT / "content/thread.json").read_text())
    src_doc = json.loads((ROOT / "content/sources.json").read_text())
    sources = {s["id"]: s for s in src_doc["sources"]}
    quotes = {q["id"]: (s, q) for s in src_doc["sources"] for q in s["quotes"]}
    posts = thread["posts"]
    total = len(posts)

    print("== Entry: the thread itself")
    ok_if(5 <= total <= 10, f"Thread has 5 to 10 posts ({total})", "task asks for roughly 5 to 10 posts")
    lengths = [x_length(p["text"]) for p in posts]
    over = [f"post {p['n']}: {l}" for p, l in zip(posts, lengths) if l > 280]
    ok_if(not over, f"Every post fits X's 280 character limit (longest {max(lengths)})", "; ".join(over))
    bad_num = [p["n"] for i, p in enumerate(posts, 1) if p["n"] != i or not p["text"].rstrip().endswith(f"{i}/{total}")]
    ok_if(not bad_num, "Posts are numbered 1/N to N/N in order", f"bad numbering on posts {bad_num}")

    entry_text = "\n".join(p["text"] for p in posts)
    alt_text = "\n".join(p["image"]["alt"] for p in posts if p["image"])
    tpl_text = "\n".join(html_to_text((ROOT / "design/templates" / p["image"]["template"]).read_bytes())
                         for p in posts if p["image"])
    visible = "\n".join([entry_text, alt_text, tpl_text])

    hits = terms.find_banned(visible)
    ok_if(not hits, "Entry (posts, alt text, on-image text) has no banned term or stand-in", f"{hits}")
    m = terms.PRICE_TALK.findall(visible)
    ok_if(not m, "Entry has no price talk, advice or promise of returns", f"found: {sorted(set(m))}")
    m = terms.JARGON.findall(entry_text + alt_text)
    ok_if(not m, "Posts and alt text avoid insider jargon", f"found: {sorted(set(m))}")
    m = terms.PERSONAL_CREDIT.findall(visible)
    ok_if(not m, "Entry has no personal credit (names, handles, emails, signatures)", f"found: {m}")
    m = terms.EMOJI.findall(visible)
    ok_if(not m, "Entry has no emoji (DAO voice rule)", f"found {len(m)}")

    print("== Entry: images")
    imgs = [p for p in posts if p["image"]]
    problems = []
    for p in imgs:
        f = ROOT / "submission/images" / p["image"]["file"]
        if not f.exists():
            problems.append(f"{f.name} missing")
            continue
        size = png_size(f)
        if size != (1600, 900):
            problems.append(f"{f.name} is {size}, expected 1600x900 PNG")
        if f.stat().st_size > 5 * 1024 * 1024:
            problems.append(f"{f.name} is over X's 5 MB image limit")
        if (ROOT / "site/assets/img/thread" / f.name).read_bytes() != f.read_bytes():
            problems.append(f"site copy of {f.name} differs from submission copy")
        if not (ROOT / "design/templates" / p["image"]["template"]).exists():
            problems.append(f"editable source {p['image']['template']} missing")
    ok_if(not problems, f"{len(imgs)} images: 1600x900 PNG, under 5 MB, editable source present", "; ".join(problems))
    bad_alt = [p["n"] for p in imgs if not (20 <= len(p["image"]["alt"]) <= 1000)]
    ok_if(not bad_alt, "Every image has alt text within X's 1000 character limit", f"posts {bad_alt}")
    stale = [p["image"]["file"] for p in imgs
             if (ROOT / "design/templates" / p["image"]["template"]).stat().st_mtime >
             (ROOT / "submission/images" / p["image"]["file"]).stat().st_mtime + 1]
    record("WARN" if stale else "PASS", "Images are newer than their templates",
           f"re-run node scripts/render_images.mjs for {stale}" if stale else "")

    print("== Facts: every claim traced to a quote")
    no_claims = [p["n"] for p in posts if not p["claims"]]
    ok_if(not no_claims, "Every post carries at least one sourced claim", f"posts {no_claims}")
    claims = [c for p in posts for c in p["claims"]]
    dangling = [(c["id"], e) for c in claims for e in c["evidence"] if e not in quotes]
    ok_if(not dangling and all(c["evidence"] for c in claims),
          f"All {len(claims)} claims point to existing quotes", f"{dangling}")
    used = {e for c in claims for e in c["evidence"]}
    unused = sorted(set(quotes) - used)
    record("WARN" if unused else "PASS", "Every quote in sources.json is used by a claim", f"unused: {unused}" if unused else "")

    missing = []
    for qid, (s, q) in quotes.items():
        snap = ROOT / "evidence/snapshots" / f"{s['id']}.txt"
        if not snap.exists() or not find_quote(snap.read_text(), q):
            missing.append(qid)
    ok_if(not missing, f"All {len(quotes)} quotes found verbatim in the saved source snapshots",
          f"not found: {missing}")
    fake = {"fragments": ["Redbelly was founded on the Moon in 1802."]}
    any_snap = (ROOT / "evidence/snapshots/S03.txt").read_text()
    ok_if(not find_quote(any_snap, fake), "Negative control: a made-up quote is rejected",
          "the quote matcher accepted a fabricated quote")

    if args.live:
        from sourcelib import fetch, snapshot_text
        live_missing = []
        for sid, s in sources.items():
            try:
                live = snapshot_text(s, fetch(s["url"]))
            except Exception as e:
                live_missing.append(f"{sid} unreachable ({e})")
                continue
            live_missing += [q["id"] for q in s["quotes"] if not find_quote(live, q)]
        ok_if(not live_missing, "LIVE: every quote still present on the live sources", f"{live_missing}")

    print("== Sources")
    ok_if(all(s["url"].startswith("https://") for s in sources.values()), "All sources use https", "")
    task_res = [s["id"] for s in sources.values() if s.get("task_resource")]
    ok_if(len(task_res) >= 3, f"Uses the task's listed resources ({', '.join(task_res)})", "too few task resources cited")
    primary = [s["id"] for s in sources.values() if "rba.gov.au" in s["url"]]
    ok_if(bool(primary), f"Central bank facts backed by RBA primary sources ({', '.join(primary)})", "no RBA source")

    print("== Evidence screenshots")
    cap_index = json.loads((ROOT / "evidence/captures/index.json").read_text())
    have = {c["quote"] for c in cap_index["captures"] if (ROOT / "evidence" / c["file"]).exists()}
    manual = {q["id"] for _, q in quotes.values() if q.get("manual_capture")}
    lacking = sorted(set(quotes) - have - manual)
    ok_if(not lacking, f"{len(have)} quotes have an automated capture", f"no capture: {lacking}")
    pending = sorted(m for m in manual if not (ROOT / "evidence/manual" / f"{m}.png").exists())
    record("PENDING" if pending else "PASS", f"Manual screenshots present for the {len(manual)} quotes that need one",
           f"still to add: {', '.join(p + '.png' for p in pending)}" if pending else "")

    print("== Whole repository")
    banned_hits, dash_hits, filler_hits, email_hits = [], [], [], []
    for f in text_files():
        t = f.read_text(errors="ignore")
        if terms.find_banned(t):
            banned_hits.append(rel(f))
        if terms.DASHES.search(t):
            dash_hits.append(rel(f))
        # Filler verbs are a rule for our own copy, so third-party snapshots are exempt.
        if f.name != "terms.py" and "snapshots" not in f.parts and terms.FILLER.search(t):
            filler_hits.append(rel(f))
        if re.search(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", t, re.I):
            email_hits.append(rel(f))
    ok_if(not banned_hits, "No banned term or stand-in in any text file in the repo", f"{banned_hits}")
    ok_if(not dash_hits, "No em dash or en dash anywhere (DAO voice rule)", f"{dash_hits}")
    ok_if(not filler_hits, "No filler verbs banned by the DAO voice rules", f"{filler_hits}")
    ok_if(not email_hits, "No email addresses anywhere in the repo", f"{email_hits}")

    print("== Brand tokens")
    tokens = (ROOT / "site/assets/css/tokens.css").read_text().lower()
    palette = set(re.findall(r"#[0-9a-f]{6}\b", tokens)) | {"#dc2626", "#ffdad7", "#ffffff"}
    off = {}
    for f in list((ROOT / "design/templates").glob("*.css")) + list((ROOT / "design/templates").glob("*.html")) + \
            list((ROOT / "site/assets/css").glob("*.css")) + [ROOT / "site/index.html"]:
        if f.exists():
            for c in set(re.findall(r"#[0-9a-fA-F]{6}\b", f.read_text())):
                if c.lower() not in palette:
                    off.setdefault(rel(f), []).append(c)
    ok_if(not off, "Every colour used is a DAO brand kit token", f"{off}")
    css = "\n".join(f.read_text() for f in (ROOT / "site/assets/css").glob("*.css")) + \
        (ROOT / "design/templates/card.css").read_text()
    fonts = set(re.findall(r'font-family:\s*"([^"]+)"', css))
    ok_if(fonts <= {"Be Vietnam Pro", "JetBrains Mono"}, f"Only brand fonts are used ({', '.join(sorted(fonts))})", f"{fonts}")

    print("== Narration (Kokoro)")
    audio = ROOT / "site/assets/audio"
    meta = json.loads((audio / "thread-narration.json").read_text())
    ok_if((audio / "thread-narration.mp3").exists() and meta["voice"] == "af_heart",
          f"Narration present, voice {meta['voice']}, {meta['duration']:.0f} s", "missing narration or wrong voice")
    spoken = " ".join(c["text"] for c in meta["cues"])
    written = " ".join(re.sub(r"\s*\d+/\d+\s*$", "", p["text"]).replace("\n", " ") for p in posts)
    ok_if(normalise(spoken) == normalise(written), "Caption cues match the thread text exactly", "captions differ from posts")
    tr = ROOT / "evidence/narration-transcript.txt"
    if tr.exists():
        heard = set(words(tr.read_text().split("\n\n", 1)[-1]))
        expected = words(written)
        recall = sum(w in heard for w in expected) / len(expected)
        ok_if(recall >= 0.9, f"Speech-to-text of the audio matches the thread ({recall:.0%} of words heard)",
              f"only {recall:.0%} of words heard")
        ok_if(not terms.find_banned(tr.read_text()), "Audio transcript has no banned term", "banned term heard")
    else:
        record("WARN", "Speech-to-text transcript not found", "evidence/narration-transcript.txt")

    print("== Submission documents and website")
    flat = lambda s: normalise(s).lower()
    md = (ROOT / "submission/THREAD.md").read_text()
    ok_if(all(flat(p["text"]) in flat(md) for p in posts), "THREAD.md contains every post verbatim", "a post is missing or altered")
    docx = ROOT / "submission/redbelly-thread.docx"
    dt = docx_text(docx) if docx.exists() else ""
    ok_if(dt and all(flat(p["text"]) in flat(dt) for p in posts), "DOCX contains every post verbatim", "a post is missing or altered")
    ok_if(dt and not terms.find_banned(dt), "DOCX has no banned term", "banned term in DOCX")
    pdf = ROOT / "submission/redbelly-thread.pdf"
    ptxt = pdf_text(pdf) if pdf.exists() else ""
    if ptxt is None:
        record("WARN", "PDF text check skipped", "install poppler-utils or pypdf to check the PDF")
    else:
        ok_if(ptxt and not terms.find_banned(ptxt) and all(flat(p["text"].split("\n")[0]) in flat(ptxt) for p in posts),
              "PDF contains every post and no banned term", "PDF missing or contains a banned term")

    if pdf.exists() and shutil.which("pdffonts"):
        rows = subprocess.run(["pdffonts", str(pdf)], capture_output=True).stdout.decode().splitlines()[2:]
        names = sorted({r.split()[0].split("+")[-1] for r in rows if r.strip()})
        stray = [n for n in names if not n.startswith(("BeVietnamPro", "JetBrainsMono"))]
        ok_if(not stray, f"PDF embeds only brand fonts ({', '.join(names)})", f"other fonts embedded: {stray}")

    html = (ROOT / "site/index.html").read_text()
    page_text = html_to_text(html.encode())
    ok_if(all(flat(p["text"]) in flat(page_text) for p in posts), "Website shows every post verbatim", "a post is missing or altered")
    ok_if('name="robots" content="noindex' in html, "Website asks search engines not to index it before judging", "noindex meta missing")
    refs = re.findall(r'(?:src|href)="([^"#?]+)', html)
    broken = [r for r in refs if not r.startswith(("http://", "https://", "mailto:", "data:"))
              and not (ROOT / "site" / r).exists()]
    ok_if(not broken, f"All {len(refs)} local links and assets on the website resolve", f"{broken}")
    ext = [r for r in re.findall(r'<(?:script|link|img|audio|source|track)[^>]+(?:src|href)="(https?://[^"]+)', html)]
    ok_if(not ext, "Website loads nothing from third-party servers", f"{ext}")
    ok_if(not terms.PERSONAL_CREDIT.search(page_text), "Website has no personal credit", "found personal credit")

    counts = {s: sum(r["status"] == s for r in results) for s in ("PASS", "FAIL", "WARN", "PENDING")}
    print(f"\n{counts['PASS']} passed, {counts['FAIL']} failed, {counts['WARN']} warnings, {counts['PENDING']} pending")
    out = {"ran": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
           "live": args.live, "counts": counts, "results": results}
    (ROOT / "evidence/checks.json").write_text(json.dumps(out, indent=2) + "\n")
    sys.exit(1 if counts["FAIL"] else 0)


if __name__ == "__main__":
    main()
