# Evidence

Everything here exists so anyone can check every fact in the thread without trusting us.

- `snapshots/`: the text of each source on the day it was checked, saved by `scripts/snapshot_sources.py`. Curly quotes and dashes are made plain, whitespace is collapsed, and banned terms are replaced with `[redacted]` so the repo stays clean. `scripts/verify.py` finds every quote in these files.
- `captures/`: one screenshot per quote, taken by `scripts/capture_evidence.mjs` from the live page (and `scripts/pdf_evidence.py` for the RBA report). The quoted text has a red box around it, and banned terms on the source page are covered by solid dark boxes. The header of each image gives the source ID, quote ID, URL and capture time. `captures/index.json` lists them all.
- `manual/`: screenshots that have to be taken by hand. See `manual/README.md`.
- `narration-transcript.txt`: a speech-to-text transcript of the narration, used to check the audio says what the thread says.
- `checks.json`: the latest results of `scripts/verify.py`.

These are third-party pages, captured for verification only. They are not part of the entry.
