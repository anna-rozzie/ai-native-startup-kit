---
name: judge
description: An independent review after building. Use when the user says "judge this", "review this harshly", "is this done", or before merging a pull request.
---

# judge

Review finished work as a stranger would. Run this in a fresh session or a subagent, so the reviewer has not seen the reasoning that produced the work and cannot be talked into it.

1. Read the issue or the stated goal. Read the acceptance criteria.
2. Run the tests yourself. Do not trust a reported result.
3. Score each acceptance criterion: pass, fail, or not verifiable, with the evidence.
4. Try to break it: empty input, huge input, wrong input, doing things twice.
5. Report failures first, most serious first. Be specific: file, line, what happens, what should happen.
6. Verdict in one line: ship, fix then ship, or rethink.

Every failure you find becomes a new test case and a `docs/FINDINGS.md` entry.
