"""Measure how long transcription takes. Exits 0 only if it is under 60 seconds.

Usage: .venv/bin/python scripts/speed_check.py <audio file>
Model loading (and the first-run download) is timed separately and not counted.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from faster_whisper import decode_audio  # noqa: E402

from app import transcribe as t  # noqa: E402

LIMIT_SECONDS = 60


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    audio_seconds = len(decode_audio(path, sampling_rate=t.SAMPLE_RATE)) / t.SAMPLE_RATE

    start = time.perf_counter()
    t._get_model()
    load_seconds = time.perf_counter() - start

    start = time.perf_counter()
    text = t.transcribe(path)
    took = time.perf_counter() - start

    print(f"Model: {t.MODEL_SIZE}")
    print(f"Audio length: {audio_seconds:.0f} s")
    print(f"Model load (not counted): {load_seconds:.1f} s")
    print(f"Transcription took: {took:.1f} s (limit {LIMIT_SECONDS} s)")
    print(f"Words: {len(text.split())}")
    print(f"Start of text: {text[:120]}...")
    ok = took < LIMIT_SECONDS
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
