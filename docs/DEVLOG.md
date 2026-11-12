# Dev log

Append-only. New entries go at the bottom. Never edit an old entry.

Format:

## YYYY-MM-DD, <name>
**Changed:** <what>
**Why:** <reason, with the issue number>
**Tests:** <what ran and the result>

---

## 2026-11-13, Anna (with Claude)
**Changed:** Set the project up as a local audio transcriber. Wrote `FOCUS.md` with /8020, filled `docs/SCOPE.md` from a /grill-me interview, set the stack in `CLAUDE.md`, and wrote three tickets with /ticket in `issues/` (engine, server, page).
**Why:** Start of the project; learning the method end to end. Tickets are files because issues are turned off on this fork.
**Tests:** None yet; no code. Each ticket lists its own test command.

## 2026-11-13, Anna (with Claude)
**Changed:** Built the local transcription engine: `app/transcribe.py` (`transcribe(path) -> str`, plain-language `TranscribeError`s), tests in `tests/test_transcribe.py`, test audio made by `tests/make_fixtures.sh` with macOS `say`, `scripts/speed_check.py`, pinned `requirements.txt`.
**Why:** Issue #1 (`issues/1-transcribe-engine.md`), FOCUS vital few #1 and #4.
**Tests:** `pytest`: 6 passed (speech words found, silence error, non-audio error, missing file error, over-15-minutes error, model loaded once). Speed check: model `small` on CPU took 17.7 s for a 128 s memo, PASS (limit 60 s). Tests were run first and failed before the code existed.

## 2026-11-13, Anna (with Claude)
**Changed:** Added the local server `app/server.py`: `POST /transcribe` takes one audio upload, checks type and size, transcribes it with `app/transcribe.py`, and returns `{"text", "filename"}` or `{"error"}` in plain language. Uploads go to a temp file that is always deleted. Tests in `tests/test_server.py`. Server packages added to `requirements.txt`.
**Why:** Issue #2 (`issues/2-upload-server.md`), FOCUS vital few #1 and #4.
**Tests:** `pytest`: 19 passed (13 new; tests written first and failed before the code). Live check with `curl` against `uvicorn` on 127.0.0.1:8000: 2-minute memo returned 200 with 360 words in 18.3 s; PDF and silence returned the right 400 messages; server listens on 127.0.0.1 only; no temp files left.
