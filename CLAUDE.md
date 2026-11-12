# Team instructions

Every teammate's Claude reads this file at the start of every session. Keep it short. Change it by pull request.

## Start of every session

1. Read `FOCUS.md`, `docs/SCOPE.md`, and the last five entries of `docs/DEVLOG.md` and `docs/FINDINGS.md`.
2. Run `git pull`.
3. If the request does not trace to the goal in `FOCUS.md`, say so in one line and ask whether to continue or park it.

## How we work

- Discuss first, build on "go". For anything larger than a small fix, propose a plan and wait.
- One thing at a time. Finish it, verify it, log it, then start the next.
- Write the test cases before the code. A change is done when its tests pass, not when it looks right.
- Never tell a teammate to check something by hand that a script can check.
- After three failed attempts at the same fix, stop. Summarize what was tried and ask.

## What goes where

| Thing | Where |
|---|---|
| What we are building and not building | `docs/SCOPE.md` |
| What changed and why | `docs/DEVLOG.md` (append-only) |
| What we learned, mistakes included | `docs/FINDINGS.md` (append-only) |
| Work to do | GitHub issues, written with `/ticket` |
| Current goal and vital few | `FOCUS.md`, written with `/8020` |

## End of every piece of work

1. Run the tests and report the real result.
2. Append one entry to `docs/DEVLOG.md`: date, who, what changed, why.
3. If anything surprised you or went wrong, append it to `docs/FINDINGS.md`.
4. Commit with a clear message and push. Work on a branch, open a pull request, never push straight to `main`.

## Append-only rule

`DEVLOG.md` and `FINDINGS.md` only grow. Add new entries at the bottom. Never edit or delete an old entry. If an old entry is wrong, add a new one that corrects it.

## Secrets

API keys and passwords go in `.env`, which is in `.gitignore`. Never commit one. Never paste one into a chat.

## Our conventions

<!-- Add your own: stack, naming, tone, what the product must never do. -->
- Stack: Python 3.13 in `.venv/`, faster-whisper (local), FastAPI + one plain HTML page, pytest. Localhost only.
- Plain language in everything users read.
