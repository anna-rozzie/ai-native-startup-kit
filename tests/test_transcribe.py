from pathlib import Path

import numpy as np
import pytest

from app import transcribe as t
from app.transcribe import TranscribeError, transcribe

FIX = Path(__file__).parent / "fixtures"


def test_speech_returns_the_spoken_words():
    text = transcribe(str(FIX / "speech.wav")).lower()
    for word in ["quick", "brown", "fox", "lazy", "dog", "river"]:
        assert word in text


def test_silence_is_an_error_not_an_empty_success():
    with pytest.raises(TranscribeError, match="No speech was found"):
        transcribe(str(FIX / "silence.wav"))


def test_non_audio_file_is_an_error():
    with pytest.raises(TranscribeError, match="could not be read as audio"):
        transcribe(str(FIX / "not_audio.wav"))


def test_missing_file_is_an_error():
    with pytest.raises(TranscribeError, match="could not be read as audio"):
        transcribe(str(FIX / "does_not_exist.wav"))


def test_over_15_minutes_is_rejected_before_transcribing(monkeypatch):
    sixteen_minutes = np.zeros(t.SAMPLE_RATE * 60 * 16, dtype=np.float32)
    monkeypatch.setattr(t, "decode_audio", lambda path, sampling_rate: sixteen_minutes)

    def must_not_run():
        raise AssertionError("model should not be loaded for a too-long file")

    monkeypatch.setattr(t, "_get_model", must_not_run)
    with pytest.raises(TranscribeError, match="longer than 15 minutes"):
        transcribe("anything.wav")


def test_model_is_loaded_once():
    assert t._get_model() is t._get_model()
