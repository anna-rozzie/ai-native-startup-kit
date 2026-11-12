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

## 2026-11-13, A file named ".wav" has no extension in Python
**What happened:** The test for an upload named just `.wav` was rejected as the wrong file type.
**Cause:** Python's `PurePath(".wav").suffix` is empty, because a name starting with a dot counts as a hidden file, not an extension.
**Rule from now on:** Read the extension and the name stem with the same helper logic, and keep an edge-case test for odd names.

## 2026-11-13, A browser can be tested end to end without clicking a file picker
**What happened:** The browser test needed a real audio file in the file picker, which a script cannot open.
**Cause:** File pickers only open on a real click, by design.
**Rule from now on:** In browser checks, build a `File` from fetched bytes and set it on the input with `DataTransfer`, then click the real buttons. Capture downloads by wrapping `URL.createObjectURL`, since the page frees the link right after saving.
