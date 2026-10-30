#!/usr/bin/env python3
"""Download every source in content/sources.json and save a text snapshot.

Snapshots go to evidence/snapshots/<id>.txt. They are normalised (curly quotes
and dashes made plain, whitespace collapsed) and the banned terms are replaced
with [redacted], so the repo stays clean. verify.py checks every quote against
these files offline.

Usage: python3 scripts/snapshot_sources.py
"""

import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sourcelib import fetch, snapshot_text  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "evidence" / "snapshots"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sources = json.loads((ROOT / "content" / "sources.json").read_text())["sources"]
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    failed = []
    for s in sources:
        try:
            text = snapshot_text(s, fetch(s["url"]))
        except Exception as e:  # keep going, report at the end
            failed.append((s["id"], str(e)))
            print(f"FAIL {s['id']} {s['url']}: {e}")
            continue
        header = f"# {s['id']} {s['title']}\n# {s['url']}\n# captured {stamp}\n\n"
        (OUT / f"{s['id']}.txt").write_text(header + text)
        print(f"ok   {s['id']} {len(text):>7} chars  {s['url']}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
