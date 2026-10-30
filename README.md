# Meet Redbelly

An X thread entry for the Redbelly DAO Community Task Board challenge to explain Redbelly to someone outside the industry, in everyday words, without the B-word or any stand-in for it.

**Format chosen: X thread.** 9 posts, 5 images, every fact traced to a public source.

> Do not post this thread, share the website, or make this repository public before judging. The DAO posts the winning entry.

## The deliverables

| Required | Where it is |
| --- | --- |
| 1. The entry: an X thread of 5 to 10 posts, as text in a document, with images attached | [`submission/redbelly-thread.docx`](submission/redbelly-thread.docx), the same content as [PDF](submission/redbelly-thread.pdf) and [Markdown](submission/THREAD.md). Images in [`submission/images/`](submission/images/) |
| 2. A short list of the sources used for any facts | [`submission/SOURCES.md`](submission/SOURCES.md) |

Everything else in this repository exists so the entry can be checked:

| Extra | Where it is |
| --- | --- |
| Claim by claim fact check | [`docs/FACT_CHECK.md`](docs/FACT_CHECK.md): 28 claims, each tied to verbatim quotes |
| Screenshots of every quote on its source | [`evidence/captures/`](evidence/captures/), 48 screenshots with the quote highlighted (46 automated, 2 taken by hand) |
| Saved text of every source | [`evidence/snapshots/`](evidence/snapshots/) |
| Automated checks | [`scripts/verify.py`](scripts/verify.py), results in [`evidence/checks.json`](evidence/checks.json) |
| Website with the whole thread, narration, sources and checks | [`site/index.html`](site/index.html) |
| Editable image sources | [`design/templates/`](design/templates/) (HTML and CSS, rendered to PNG) |
| Brand kit compliance notes | [`docs/BRAND_COMPLIANCE.md`](docs/BRAND_COMPLIANCE.md) |

## The thread

```text
1/9  Redbelly in one sentence: a public network, built in Australia, where real financial assets
     like bonds, investment funds and loans can be issued, managed and traded as digital items,
     with ID checks and the rules built in.
2/9  The problem: money and paperwork pass between several companies, each with its own records.
3/9  The idea: a digital concert ticket, but for a financial asset. This is called tokenisation.
4/9  The people using it are verified, rules are checked automatically, privacy is protected.
5/9  No single computer gets the final say. Once confirmed, it is final.
6/9  Where it comes from: University of Sydney and CSIRO research. Live since November 2024.
7/9  Used in Project Acacia, a Reserve Bank of Australia research project.
8/9  Who tested what on it, and a plain statement that the RBA endorses no participant.
9/9  Why it matters, in one line each for a business, an investor and everyone.
```

That is a summary. The exact text of each post is in [`submission/THREAD.md`](submission/THREAD.md).

## How the task rules are met

| Rule from the brief | How | Checked by |
| --- | --- | --- |
| No B-word or stand-in anywhere, including captions and on-screen text | Not in the posts, alt text, images, website, documents, audio or code. Source screenshots have it blacked out, and saved source text has it replaced with `[redacted]` | `verify.py` scans every text file, the image templates, the DOCX, the PDF and a speech-to-text transcript of the narration |
| Facts accurate, from public Redbelly material | 28 claims, 48 quotes, 12 sources. Every Project Acacia fact is backed by the RBA's own releases and final report | `verify.py` finds every quote in the saved sources. `--live` re-checks the live pages |
| Not posted publicly before judging | Website has `noindex`, deploy guide puts it behind a password | `verify.py` checks the `noindex` tag |
| No price talk, advice or promise of returns | No token, price or investment outcome is mentioned | `verify.py` word list on the posts, alt text and images |
| No unlicensed music, images or footage | All images are original, built from HTML. Fonts are OFL. The logo is from the DAO brand kit. Narration is Kokoro (Apache 2.0). No music | [`docs/LICENSES.md`](docs/LICENSES.md) |
| No unchecked AI text, no made-up facts | Every claim maps to a verbatim quote with a screenshot | `verify.py`, including a negative control that a fabricated quote is rejected |
| No personal credit inside the deliverable | No names, handles, emails, signatures or "made by" lines | `verify.py` on the entry, website and whole repo |

## Check it yourself

Needs Python 3.9 or later and nothing else:

```bash
python3 scripts/verify.py
```

Re-check every quote against the live websites as well:

```bash
python3 scripts/verify.py --live
```

Current result: 41 passed, 0 failed offline, and 42 passed with `--live` (checked 30 October 2026).

## View the website

Open `site/index.html` in a browser. Captions on the audio player only load when the site is served over http, so for the full experience:

```bash
python3 -m http.server 8080 --directory site
```

Then open http://localhost:8080. To put it on a server, see [`docs/DEPLOY.md`](docs/DEPLOY.md).

## Rebuild

Everything is generated from two files: [`content/thread.json`](content/thread.json) (posts, alt text, claims) and [`content/sources.json`](content/sources.json) (sources and quotes). After editing them:

```bash
pip install -r requirements.txt
npm install && npx playwright install chromium
bash scripts/build_all.sh
```

`bash scripts/build_all.sh --sources` also re-downloads every source and re-takes the screenshots. Rebuilding the narration needs the Kokoro model files; the steps are at the top of [`scripts/narrate.py`](scripts/narrate.py).

## Layout

```text
content/      thread.json and sources.json, the single source of truth
submission/   what gets submitted: DOCX, PDF, Markdown, SOURCES.md, images
site/         the static website, self-contained
design/       editable image templates and the print layout for the PDF
evidence/     source snapshots, screenshots, transcript, check results
docs/         fact check, brand compliance, deploy guide, licences
scripts/      build and verification scripts
```
