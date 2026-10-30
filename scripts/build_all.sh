#!/usr/bin/env bash
# Rebuild everything that is generated from content/*.json, then verify.
#
#   bash scripts/build_all.sh            images, documents, PDF, website, checks
#   bash scripts/build_all.sh --sources  also re-download sources and re-take screenshots
#
# Narration is rebuilt separately because it needs the Kokoro model files:
#   python3 scripts/narrate.py --model kokoro-v1.0.onnx --voices voices-v1.0.bin
#   python3 scripts/transcribe.py
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "${1:-}" == "--sources" ]]; then
  python3 scripts/snapshot_sources.py
  python3 scripts/pdf_evidence.py
  node scripts/capture_evidence.mjs
fi

node scripts/render_images.mjs
python3 scripts/build_docs.py
node scripts/build_pdf.mjs
python3 scripts/build_site.py
python3 scripts/verify.py > /dev/null || true   # first pass writes checks.json for the site
python3 scripts/build_site.py
python3 scripts/verify.py
