# 2. Local server with an upload endpoint

## Goal
A small local web server that accepts one audio upload, checks it, transcribes it with issue #1's function, and returns the text. Serves FOCUS.md vital few #1 and #4.

## Touches
- `app/server.py` (new)
- `tests/test_server.py` (new)
- `requirements.txt` (add `fastapi`, `uvicorn`, `python-multipart`, `httpx` for tests)

## Must not touch
- `app/transcribe.py` behaviour (only import it)
- `CLAUDE.md`, `docs/` except the DEVLOG entry, `.claude/`, `example/`

## Settled choices
- FastAPI, served by uvicorn on `127.0.0.1:8000` only (never `0.0.0.0`).
- `POST /transcribe` takes one multipart field `file`.
- Allowed extensions: `.mp3`, `.m4a`, `.wav`, `.webm` (case-insensitive). Max 50 MB.
- Success: `200` with JSON `{"text": "...", "filename": "<original name with .txt>"}`.
- Errors: JSON `{"error": "<plain-language message>"}` with `400` for bad input (wrong type, too big, too long, no speech, unreadable) and `500` for anything unexpected (message: "Something went wrong while transcribing. Please try again.").
- The upload is written to a temporary file and deleted in a `finally` block, success or failure. Nothing else is written to disk.
- Run command: `.venv/bin/uvicorn app.server:app --host 127.0.0.1 --port 8000`.
- Tests use FastAPI's `TestClient` and may replace `transcribe` with a fake to stay fast, except one real end-to-end test on `speech.wav`.

## Acceptance criteria
- [ ] Uploading `speech.wav` returns 200 with non-empty `text` and `filename == "speech.txt"`.
- [ ] Uploading a `.pdf` returns 400 with the message "Please upload an mp3, m4a, wav or webm file."
- [ ] Uploading a file over 50 MB returns 400 with "This file is larger than 50 MB. Please upload a smaller one."
- [ ] A `TranscribeError` from the engine becomes a 400 carrying the same message.
- [ ] Any other exception becomes a 500 with the generic message.
- [ ] After each test request, no temporary upload file remains (test checks the temp path is gone).
- [ ] A request with no file returns 400, not a crash.

## Edge cases
- Upper-case extension `MEMO.M4A` is accepted (test).
- File name with spaces or non-English letters gives a sensible `.txt` name (test).

## Test command
```bash
.venv/bin/pytest -q
```

## Depends on
#1
