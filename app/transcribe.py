"""Turn an audio file into text, locally, with faster-whisper."""

from functools import lru_cache

from faster_whisper import WhisperModel, decode_audio

MODEL_SIZE = "small"
SAMPLE_RATE = 16000
MAX_MINUTES = 15


class TranscribeError(Exception):
    """A failure with a message that is safe to show to the user."""


@lru_cache(maxsize=1)
def _get_model() -> WhisperModel:
    # Downloads the model once (about 480 MB), then loads it from the local cache.
    return WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")


def transcribe(path: str) -> str:
    try:
        audio = decode_audio(path, sampling_rate=SAMPLE_RATE)
    except Exception as exc:
        raise TranscribeError("This file could not be read as audio.") from exc

    if len(audio) == 0:
        raise TranscribeError("No speech was found in this recording.")
    if len(audio) / SAMPLE_RATE > MAX_MINUTES * 60:
        raise TranscribeError(
            f"This recording is longer than {MAX_MINUTES} minutes. Please upload a shorter one."
        )

    # vad_filter skips silent stretches, so silence gives no text instead of made-up words.
    segments, _info = _get_model().transcribe(audio, vad_filter=True)
    text = " ".join(s.text.strip() for s in segments).strip()

    if not text:
        raise TranscribeError("No speech was found in this recording.")
    return text
