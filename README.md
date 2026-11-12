# Transcriber

Upload a recording and get the text back, on your own Mac. Free, private, no account or API key. Built with the AI-Native Startup kit below.

## Run the transcriber

1. Set up once (downloads about 480 MB the first time you transcribe):
   ```bash
   python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
   ```
2. Start it:
   ```bash
   .venv/bin/uvicorn app.server:app --host 127.0.0.1 --port 8000
   ```
3. Open http://127.0.0.1:8000 in your browser, choose an mp3, m4a, wav or webm file (up to 50 MB and 15 minutes), and click **Transcribe**.
4. Click **Download .txt** to save the text. Stop the server with Ctrl+C.

To run the checks: `bash tests/make_fixtures.sh && .venv/bin/pytest -q`, then, with the server running, `.venv/bin/python scripts/done_check.py`.

---

# AI-Native Startup starter kit

A shared setup for a small team where everyone builds with AI on their own computer. Copy this folder into a new GitHub repo, and every teammate's AI reads the same rules, the same scope, and the same history.

From the workshop "The AI-Native Startup: Prototyping, Prompting, and Building as a Team" at the eHub at UC Berkeley.

## What is in here

| File | What it does |
|---|---|
| `CLAUDE.md` | The team's standing instructions. Claude Code reads it at the start of every session, on every teammate's machine. |
| `docs/SCOPE.md` | What you are building and what you are not. |
| `docs/DEVLOG.md` | Append-only log of what changed and why. Never edit old entries. |
| `docs/FINDINGS.md` | Append-only log of what you learned, especially mistakes. The AI reads it before starting work. |
| `.claude/skills/grill-me/` | `/grill-me`: the AI interviews you until the idea has no gaps. |
| `.claude/skills/ticket/` | `/ticket`: turns a request into GitHub issues someone else can build without asking you anything. |
| `.claude/skills/8020/` | `/8020`: sets the goal, cuts work to the vital few, writes `FOCUS.md`, and calls out drift. |
| `.claude/skills/coach/` and `judge/` | A second opinion before you build, and an independent review after. |
| `CHEATSHEET.md` | One page: the loop, the good prompt, the habits. |
| `example/` | The interview tracker built in the workshop, with the exact prompts that made it. |

## Set up in 10 minutes

1. Install the Claude desktop app and open the Code tab. Install GitHub Desktop or the `gh` command line tool.
2. Create a private GitHub repo for your startup. Copy the contents of this folder into it and push.
3. Every teammate clones the repo and opens that folder in Claude Code.
4. Run `/8020` once together to write `FOCUS.md`.
5. Run `/grill-me` on the first feature, then `/ticket` to file it as issues.

## The team rules, in short

- Everything lives in the repo. If it is only in a chat, it does not exist.
- Logs are append-only. Add a new entry, never rewrite an old one.
- One issue per sitting of work. An issue is written so a stranger could build it.
- Pull before you start, push when you stop.
- When the rules need to change, change `CLAUDE.md` in a pull request so everyone gets the change.

## Credit

The grill-me idea comes from Matt Pocock's open source skills (github.com/mattpocock/skills). The version here is written fresh for this kit.

## Other repos worth cloning

| Repo | Why |
|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | Engineering skills for AI coding agents. Where the grill-me idea comes from. |
| [obra/superpowers](https://github.com/obra/superpowers) | A skills framework and a development method: plan, test first, review. |
| [anthropics/skills](https://github.com/anthropics/skills) | Anthropic's public skills repo. Good examples of how a skill is written. |
| [github/spec-kit](https://github.com/github/spec-kit) | Toolkit for spec-driven development: write the spec, then let the AI build it. |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Shrinks command output before the AI reads it, which saves tokens. |
| [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | Recipes for building your own product on top of Claude. |
