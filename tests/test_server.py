from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import server
from app.transcribe import TranscribeError

FIX = Path(__file__).parent / "fixtures"
client = TestClient(server.app)


@pytest.fixture(autouse=True)
def temp_dir(tmp_path, monkeypatch):
    """Send uploads to a private folder so each test can check it is left empty."""
    d = tmp_path / "uploads"
    d.mkdir()
    monkeypatch.setattr(server, "TEMP_DIR", str(d))
    yield d
    assert list(d.iterdir()) == [], "temporary upload file was not deleted"


@pytest.fixture
def fake_transcribe(monkeypatch):
    seen = {}

    def fake(path):
        seen["path"] = path
        seen["existed"] = Path(path).exists()
        return "hello world"

    monkeypatch.setattr(server, "transcribe", fake)
    return seen


def upload(name, data=b"audio bytes"):
    return client.post("/transcribe", files={"file": (name, data)})


# --- end to end, real model ---

def test_real_speech_file_returns_text_and_txt_name():
    r = upload("speech.wav", (FIX / "speech.wav").read_bytes())
    assert r.status_code == 200
    body = r.json()
    assert "fox" in body["text"].lower()
    assert body["filename"] == "speech.txt"


# --- input checks ---

def test_wrong_file_type_is_rejected(fake_transcribe):
    r = upload("notes.pdf")
    assert r.status_code == 400
    assert r.json() == {"error": "Please upload an mp3, m4a, wav or webm file."}
    assert "path" not in fake_transcribe


def test_file_over_50_mb_is_rejected(fake_transcribe):
    r = upload("big.wav", b"\0" * (50 * 1024 * 1024 + 1))
    assert r.status_code == 400
    assert r.json() == {"error": "This file is larger than 50 MB. Please upload a smaller one."}
    assert "path" not in fake_transcribe


def test_file_of_exactly_50_mb_is_accepted(fake_transcribe):
    r = upload("ok.wav", b"\0" * (50 * 1024 * 1024))
    assert r.status_code == 200


def test_no_file_is_a_400_not_a_crash():
    r = client.post("/transcribe")
    assert r.status_code == 400
    assert r.json() == {"error": "Please choose an audio file to upload."}


def test_uppercase_extension_is_accepted(fake_transcribe):
    r = upload("MEMO.M4A")
    assert r.status_code == 200
    assert r.json()["filename"] == "MEMO.txt"


@pytest.mark.parametrize(
    "name, expected",
    [
        ("team meeting 3.mp3", "team meeting 3.txt"),
        ("встреча.webm", "встреча.txt"),
        ("../../etc/evil.wav", "evil.txt"),
        (".wav", "transcript.txt"),
    ],
)
def test_txt_name_is_sensible(fake_transcribe, name, expected):
    r = upload(name)
    assert r.status_code == 200
    assert r.json()["filename"] == expected


def test_upload_is_on_disk_while_transcribing(fake_transcribe):
    upload("memo.wav")
    assert fake_transcribe["existed"] is True


# --- errors from the engine ---

def test_engine_error_becomes_400_with_same_message(monkeypatch):
    def fail(path):
        raise TranscribeError("No speech was found in this recording.")

    monkeypatch.setattr(server, "transcribe", fail)
    r = upload("memo.wav")
    assert r.status_code == 400
    assert r.json() == {"error": "No speech was found in this recording."}


def test_unexpected_error_becomes_500_with_generic_message(monkeypatch):
    def boom(path):
        raise RuntimeError("internal details the user should not see")

    monkeypatch.setattr(server, "transcribe", boom)
    r = upload("memo.wav")
    assert r.status_code == 500
    assert r.json() == {"error": "Something went wrong while transcribing. Please try again."}
