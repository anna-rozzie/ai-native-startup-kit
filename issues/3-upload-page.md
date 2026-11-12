# 3. Upload page, transcript display and .txt download

## Goal
One plain HTML page where you pick an audio file, see "Working…", then read the transcript and download it as `.txt`. Serves FOCUS.md vital few #2 and #3, and closes the "done when" check.

## Touches
- `app/static/index.html` (new; inline CSS and JS, no frameworks, no build step)
- `app/server.py` (serve the page at `GET /`)
- `tests/test_page.py` (new)
- `scripts/done_check.py` (new)
- `README.md` (add a short "Run the transcriber" section at the top)

## Must not touch
- The `/transcribe` response format from #2
- `CLAUDE.md`, `docs/` except the DEVLOG entry, `.claude/`, `example/`

## Settled choices
- Page title and heading: "Transcriber". Plain language, readable font, no design polish.
- A file picker limited to `.mp3,.m4a,.wav,.webm` and a "Transcribe" button.
- While waiting: button disabled, text "Working… this can take up to a minute."
- On success: transcript in a read-only text area, plus a "Download .txt" button that saves the text under the `filename` from the server. The download is built in the browser (no second request).
- On error: the server's `error` message shown in a visible message area; button re-enabled.
- No external scripts, fonts or requests: the page works offline.
- `scripts/done_check.py` starts nothing itself; with the server running, it uploads `tests/fixtures/long_memo.m4a` to `/transcribe`, and passes only if the reply is 200, the text is non-empty, and it took under 60 s.

## Acceptance criteria
- [ ] `GET /` returns 200 with HTML containing "Transcriber", a file input with the four accepted types, and a "Download .txt" control.
- [ ] The page HTML contains no `http://` or `https://` references to other hosts (test).
- [ ] `python scripts/done_check.py` passes against the running server: this is the FOCUS.md "done when" check. Result logged in `docs/DEVLOG.md`.
- [ ] README explains in plain language how to install and run it in four steps or fewer.

## Edge cases
- Error replies show the message, not raw JSON (checked by the JS reading `error`).
- Choosing a new file after a result clears the old transcript.

## Test command
```bash
.venv/bin/pytest -q && .venv/bin/python scripts/done_check.py
```

## Depends on
#2
