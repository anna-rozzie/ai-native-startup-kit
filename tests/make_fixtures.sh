#!/usr/bin/env bash
# Generates test audio with the macOS `say` command. Output is not committed.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p fixtures
cd fixtures

VOICE="Samantha"

# One short known sentence.
[ -f speech.wav ] || say -v "$VOICE" -o speech.wav --data-format=LEI16@16000 \
  "The quick brown fox jumps over the lazy dog near the river bank."

# Five seconds of silence.
[ -f silence.wav ] || python3 - <<'PY'
import wave
with wave.open("silence.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
    w.writeframes(b"\x00\x00" * 16000 * 5)
PY

# A text file pretending to be audio.
[ -f not_audio.wav ] || echo "this is not audio" > not_audio.wav

# About two minutes of speech, as an m4a like an iPhone voice memo.
if [ ! -f long_memo.m4a ]; then
  PARA="Good morning everyone. This is a short voice memo about our weekly planning. \
First, we reviewed the budget for the next quarter and agreed to keep spending flat. \
Second, the design team will share three new layouts for the home page on Friday. \
Third, we need volunteers to test the mobile app before the release next month. \
Please send me your questions by email, and remember that the office is closed on Monday."
  TEXT="$PARA $PARA $PARA $PARA $PARA"
  say -v "$VOICE" -r 150 -o long_memo.m4a --file-format=m4af --data-format=aac "$TEXT"
fi

ls -la
