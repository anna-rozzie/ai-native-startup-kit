# Findings

Append-only. What we learned, especially what went wrong. Claude reads the latest entries before starting work, so the same mistake is not made twice.

Format:

## YYYY-MM-DD, <short title>
**What happened:** <the surprise or the mistake>
**Cause:** <why>
**Rule from now on:** <what we do differently>

---

## 2026-11-13, faster-whisper breaks with the newest PyAV
**What happened:** Every audio file, even a valid WAV, failed to decode with `open() got an unexpected keyword argument 'metadata_errors'`. Our code turned it into "could not be read as audio", which hid the real cause.
**Cause:** `pip install faster-whisper` pulled PyAV 19, which removed an option that faster-whisper 1.2.1 still passes.
**Rule from now on:** Install from the pinned `requirements.txt` (PyAV 15.1.0). When a friendly error appears for a file that should work, print the underlying exception before changing code.
