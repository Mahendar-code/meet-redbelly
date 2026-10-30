#!/usr/bin/env python3
"""Read the thread aloud with Kokoro TTS (voice af_heart) and write:

  site/assets/audio/thread-narration.mp3   the audio
  site/assets/audio/thread-narration.vtt   captions, one cue per sentence
  site/assets/audio/thread-narration.json  where each post starts and ends

Kokoro-82M is Apache 2.0 licensed. The model files are not kept in this repo.
Get them once (about 350 MB):

  pip install kokoro-onnx soundfile
  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
  curl -LO https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

Usage: python3 scripts/narrate.py --model kokoro-v1.0.onnx --voices voices-v1.0.bin
"""

import argparse
import json
import pathlib
import re
import subprocess
import tempfile

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "assets" / "audio"
VOICE = "af_heart"
SENTENCE_GAP = 0.28
POST_GAP = 0.85

# Spoken forms only. The written thread is not changed.
SAY = [
    (re.compile(r"\s*\d+/\d+\s*$"), ""),          # drop the 1/9 counters
    (re.compile(r"\bCSIRO\b"), "C S I R O"),
    (re.compile(r"\bRBA\b"), "R B A"),
    (re.compile(r"\bCRC\b"), "C R C"),
    (re.compile(r"redbelly\.network", re.I), "Red-belly dot network"),
    (re.compile(r"\bRedbelly\b"), "Red-belly"),        # stress both halves
]


def spoken(text):
    for rx, rep in SAY:
        text = rx.sub(rep, text)
    return text.strip()


def sentences(text):
    parts = []
    for line in text.split("\n"):
        line = line.strip()
        if line:
            parts += [s for s in re.split(r"(?<=[.!?:])\s+", line) if s]
    return parts


def stamp(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--voices", required=True)
    ap.add_argument("--speed", type=float, default=1.0)
    args = ap.parse_args()

    kokoro = Kokoro(args.model, args.voices)
    thread = json.loads((ROOT / "content" / "thread.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)

    sr = 24000
    chunks, cues, posts, t = [], [], [], 0.0
    for post in thread["posts"]:
        start = t
        written = sentences(re.sub(r"\s*\d+/\d+\s*$", "", post["text"]))
        for i, sentence in enumerate(written):
            audio, sr = kokoro.create(spoken(sentence), voice=VOICE, speed=args.speed, lang="en-us")
            dur = len(audio) / sr
            cues.append({"start": t, "end": t + dur, "text": sentence, "post": post["n"]})
            chunks.append(audio.astype(np.float32))
            t += dur
            gap = SENTENCE_GAP if i < len(written) - 1 else POST_GAP
            chunks.append(np.zeros(int(gap * sr), dtype=np.float32))
            t += gap
        posts.append({"post": post["n"], "start": round(start, 3), "end": round(t - POST_GAP, 3)})
        print(f"post {post['n']}: {start:6.2f}s to {t - POST_GAP:6.2f}s")

    with tempfile.TemporaryDirectory() as d:
        wav = pathlib.Path(d) / "narration.wav"
        sf.write(wav, np.concatenate(chunks), sr)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100",
                        "-ac", "1", "-codec:a", "libmp3lame", "-b:a", "96k",
                        str(OUT / "thread-narration.mp3")], check=True)

    vtt = ["WEBVTT", ""]
    for n, c in enumerate(cues, 1):
        vtt += [str(n), f"{stamp(c['start'])} --> {stamp(c['end'])}", c["text"], ""]
    (OUT / "thread-narration.vtt").write_text("\n".join(vtt))
    (OUT / "thread-narration.json").write_text(json.dumps(
        {"voice": VOICE, "engine": "Kokoro-82M v1.0 (kokoro-onnx)", "duration": round(t - POST_GAP, 3),
         "posts": posts, "cues": [{**c, "start": round(c["start"], 3), "end": round(c["end"], 3)} for c in cues]},
        indent=2) + "\n")
    print(f"total {t - POST_GAP:.1f}s, {len(cues)} cues")


if __name__ == "__main__":
    main()
