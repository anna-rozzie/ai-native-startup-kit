# The prompts that built Discovery Log

Three prompts, in order. Paste them into Claude Code in an empty folder to rebuild it yourself.

## 1. Many ideas, pick one

```
I'm a first-time founder doing customer discovery. Give me 5 small tools I could build today that would help me learn faster from customer conversations. One line each. Then tell me which one you would build first and why.
```

Picked: the customer interview tracker.

## 2. Grill me

```
/grill-me I want to build a customer interview tracker. Log each conversation, tag the pain points I heard, and show me which pains come up most.
```

Decisions that came out of the interview:

- For a founder working alone. No accounts, no sharing yet.
- Runs as a plain web page. Data stays in the browser.
- An interview needs a name. Pains and notes are optional.
- Pains are typed as comma separated tags, cleaned up on save.
- A pain counts once per interview.
- Left out on purpose: export, sharing, AI summaries. Those became issues.

## 3. Build, tests first

```
Build it as a plain web page I can open in a browser. No install, no accounts, data saved in the browser. Before you write the app, write the test cases that prove it works, then build until they pass. Keep a FINDINGS.md of anything you learn or get wrong along the way.
```

Result: `prebaked/index.html`, 12 passing tests in `prebaked/tests.html`, and three entries in `prebaked/FINDINGS.md`.

## 4. Hand off the rest as issues

```
/ticket Next for the interview tracker: export to CSV, a weekly summary of top pains, and sharing a read-only link with my cofounder.
```
