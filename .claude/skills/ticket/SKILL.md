---
name: ticket
description: Turn a request into GitHub issues complete enough that a teammate or another AI session can build them without asking anything. Use when the user says "ticket this", "write issues", "make issues for X", or lists features they want built later.
---

# ticket

A ticket is a GitHub issue on this repo. The person or AI who picks it up may never talk to the author, so every question gets answered in the issue.

## Steps

1. **Read first.** `FOCUS.md`, `docs/SCOPE.md`, recent `docs/DEVLOG.md` entries, and the code the request touches. Anything the repo can answer is not a question for the user.
2. **Split** the request into features, one issue per sitting of work. If two would edit the same files, make one depend on the other.
3. **Ask until nothing is left to guess.** One question at a time, each with your recommended answer. If a feature does not serve the goal in `FOCUS.md`, say so.
4. **Write each issue** with `.github/ISSUE_TEMPLATE/task.md`. Fill in every section. Acceptance criteria must be things a script can check.
5. **File it:**

```bash
gh issue create --title "<title>" --body-file <file> --label ready
```

6. **Report** the issue links in one short list.

If `gh` is not installed or the folder is not a GitHub repo yet, write the issues to `issues/<number>-<slug>.md` instead and say so.
