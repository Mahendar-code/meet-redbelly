#!/usr/bin/env python3
"""Transcribe the narration with Whisper so verify.py can check what it says.

Writes evidence/narration-transcript.txt. Needs: pip install faster-whisper,
plus ffmpeg on the PATH. The base.en model (about 150 MB) downloads on first run.
Usage: python3 scripts/transcribe.py
"""

import pathlib
import subprocess

import numpy as np
from faster_whisper import WhisperModel

ROOT = pathlib.Path(__file__).resolve().parent.parent
MP3 = ROOT / "site/assets/audio/thread-narration.mp3"

raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(MP3), "-f", "f32le", "-ac", "1",
                      "-ar", "16000", "-"], capture_output=True, check=True).stdout
segments, _ = WhisperModel("base.en", device="cpu", compute_type="int8").transcribe(
    np.frombuffer(raw, dtype=np.float32), beam_size=5)
text = " ".join(s.text.strip() for s in segments)
(ROOT / "evidence/narration-transcript.txt").write_text(
    "# Automatic transcript of site/assets/audio/thread-narration.mp3\n"
    "# Engine: faster-whisper base.en (int8, CPU). Used by verify.py to check the audio says what the thread says.\n\n"
    + text + "\n")
print(text)
