# Cheat sheet

## The loop
Describe. Run. Look. Correct. Repeat in small steps.

## Before you build
1. Ask for five ideas. Pick one. Build one thing today.
2. `/grill-me` until there is nothing left to guess.
3. Plan first. Build on "go".

## A good prompt has
- **Goal:** who it is for and what they can do
- **Format:** where it runs, what it must not need
- **Done means:** what a test can check
- **Tests first:** write the test cases, then build until they pass
- **Do not touch:** what must stay as it is
- **Log it:** keep FINDINGS.md of what went wrong

## When it is going in circles
Three failed fixes in a row: stop. New chat. Restate the problem, paste the error, say what was tried.

## Team
- Everyone on GitHub, one repo
- Same `CLAUDE.md`, same skills, pulled by everyone
- `SCOPE.md` for what, `DEVLOG.md` for what changed, `FINDINGS.md` for what we learned
- Logs are append-only
- Work lives in issues written with `/ticket`
- `/8020` keeps the goal in `FOCUS.md`

## Tokens
- New chat for each task. Long chats cost more every message.
- Point at files. Do not paste them.
- Biggest model to build, small model to search and summarize.
- Tight scope: say which files to touch.
- Let logs carry memory between sessions, so you do not re-explain.
