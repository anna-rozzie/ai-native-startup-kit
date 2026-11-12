# 1. Local transcription engine and speed check

## Goal
A Python function that turns an audio file into text on this Mac, plus a script that measures its speed. Serves FOCUS.md vital few #1 (audio in, text out) and #4 (clear errors).

## Touches
- `app/transcribe.py` (new)
- `tests/test_transcribe.py` (new)
- `tests/make_fixtures.sh` (new)
- `scripts/speed_check.py` (new)
- `requirements.txt` (new)
- `.gitignore` (add `.venv/`, `tests/fixtures/`)

## Must not touch
- `CLAUDE.md`, `docs/`, `.claude/`, `example/`

## Settled choices
- Engine: `faster-whisper`, model `small`, `device="cpu"`, `compute_type="int8"`, language auto-detected.
- Python 3.13 in a virtual environment at `.venv/`. Dependencies pinned in `requirements.txt`. Tests use `pytest`.
- No ffmpeg: audio is decoded with `faster_whisper.decode_audio` (bundled PyAV).
- The model is loaded once and reused, not reloaded per call.
- Public function: `transcribe(path: str) -> str`. Raises `TranscribeError` with a plain-language message for every failure.
- Limits: files over 15 minutes of audio raise `TranscribeError("This recording is longer than 15 minutes. Please upload a shorter one.")`.
- Empty result (silence) raises `TranscribeError("No speech was found in this recording.")`.
- Undecodable file raises `TranscribeError("This file could not be read as audio.")`.
- Test audio is generated with the macOS `say` command, never committed: `tests/make_fixtures.sh` creates `speech.wav` (one known English sentence), `silence.wav` (5 s of silence), `not_audio.wav` (a text file renamed), and `long_memo.m4a` (about 2 minutes of speech).

## Acceptance criteria
- [ ] `transcribe("tests/fixtures/speech.wav")` returns text containing the key words of the spoken sentence (case-insensitive).
- [ ] `silence.wav` raises `TranscribeError` with the "No speech" message.
- [ ] `not_audio.wav` raises `TranscribeError` with the "could not be read" message.
- [ ] Audio longer than 15 minutes raises the "longer than 15 minutes" message (test may mock the duration).
- [ ] `python scripts/speed_check.py tests/fixtures/long_memo.m4a` prints the audio length and seconds taken, and exits 0 only if it took under 60 s. Result recorded in `docs/DEVLOG.md`. If it fails with `small`, retry with `base`, record both, and record the switch in `docs/SCOPE.md` Settled decisions.

## Edge cases
- Silent file: error, not empty success (test).
- Non-audio file with an audio extension: error (test).
- First run downloads the model (about 480 MB): the speed check excludes load time and says so.

## Test command
```bash
bash tests/make_fixtures.sh && .venv/bin/pytest -q && .venv/bin/python scripts/speed_check.py tests/fixtures/long_memo.m4a
```

## Depends on
None.
