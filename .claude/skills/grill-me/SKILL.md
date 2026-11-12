---
name: grill-me
description: Interview the user about an idea, plan, or feature until nothing is left to guess. Use when the user says "grill me", "poke holes in this", "what am I missing", or describes something they want to build without details.
---

# grill-me

Interview the user until you both understand exactly what is being built. Do not build anything during the interview.

## How to ask

1. Ask in rounds. In each round, ask only the questions you can ask now without guessing an answer you have not heard yet.
2. Number every question. Give your recommended answer under each one, so the user can reply "yes to all" or correct one.
3. Keep rounds short: three to five questions.
4. After each round, work out which new questions the answers opened up, and ask those next.

## What to cover

- Who is this for, and what do they do today instead?
- What is the smallest version that is useful?
- What does done look like, in a way a test can check?
- What must it never do?
- What happens with empty, huge, or wrong input?
- What is deliberately left out?

## Rules

- Look up facts yourself (files, the repo, the docs). Only decisions go to the user.
- If the user says "take your recommendations", accept your own answers and move on.
- Stop when a stranger could build it from your notes.
- End with a summary: the decisions made, as a short list. Offer to save it to `docs/SCOPE.md` and to run `/ticket`.
