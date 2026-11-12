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
