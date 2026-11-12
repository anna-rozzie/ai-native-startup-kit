# Scope

**Product:** A transcriber for one person on their own Mac: upload an audio file, get back a readable transcript and a `.txt` download, with everything running locally and free.

## In scope
- One plain HTML page served by a small local Python server (localhost only).
- Upload one audio file at a time: `.mp3`, `.m4a`, `.wav`, `.webm`.
- Transcribe locally with `faster-whisper`, model `small`, language auto-detected.
- Show the transcript on the page with a simple "Working…" message while it runs.
- Download the transcript as `.txt`, named after the audio file (`memo.m4a` → `memo.txt`).
- Plain-language errors for: wrong file type, file over 50 MB, audio over 15 minutes, empty or silent audio, transcription failure.
- Automated tests for each piece, run with one command.

## Out of scope
- Cloud transcription APIs (no API key wanted; keeps it free and private).
- Deployment or access from other devices.
- Recording from the microphone, speaker labels, summaries, editing, timestamps in the output.
- Accounts, saved history, a database.
- Design polish beyond clean and readable.

## Never
- Never send audio or text off the machine (after the one-time model download).
- Never write uploaded audio or transcripts to permanent storage; temporary files are deleted when the request ends.
- Never show a success state for an empty transcript.

## Settled decisions
| Date | Decision | Why |
|---|---|---|
| 2026-11-13 | Fresh project, not built on the old RozmaNotes repo | Learning the method from a clean start |
| 2026-11-13 | Local engine `faster-whisper` instead of a cloud API | No API key wanted; free and private |
| 2026-11-13 | `faster-whisper` rather than other local engines | Installs with pip and decodes audio itself; this Mac has no ffmpeg or Homebrew |
| 2026-11-13 | Model `small`, falling back to `base` if too slow | Good accuracy for clear speech; must meet the under-a-minute target on an M3 with 8 GB |
| 2026-11-13 | Python server + one HTML page, localhost only | Simplest stack that keeps the work on one machine |
| 2026-11-13 | Limits: 50 MB and 15 minutes per file | Keeps waits reasonable on a laptop |

## Open questions
- Does `small` transcribe a 2-minute memo in under a minute on this Mac? Measured in the first ticket.
