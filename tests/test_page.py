import re

from fastapi.testclient import TestClient

from app import server

client = TestClient(server.app)


def page() -> str:
    r = client.get("/")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    return r.text


def test_page_has_title_and_heading():
    html = page()
    assert "<title>Transcriber</title>" in html
    assert re.search(r"<h1[^>]*>Transcriber</h1>", html)


def test_file_input_accepts_exactly_the_four_types():
    html = page()
    m = re.search(r'<input[^>]*type="file"[^>]*accept="([^"]+)"', html)
    assert m, "file input with an accept list not found"
    assert set(m.group(1).split(",")) == {".mp3", ".m4a", ".wav", ".webm"}


def test_has_transcribe_and_download_controls():
    html = page()
    assert re.search(r"<button[^>]*>Transcribe</button>", html)
    assert re.search(r"<button[^>]*>Download \.txt</button>", html)
    assert "<textarea" in html and "readonly" in html


def test_shows_working_message_and_reads_error_field():
    html = page()
    assert "Working… this can take up to a minute." in html
    assert ".error" in html, "page JS must show the server's error message, not raw JSON"


def test_page_makes_no_requests_to_other_hosts():
    html = page()
    assert "http://" not in html and "https://" not in html
    assert "//" not in re.sub(r"<script>.*?</script>", "", html, flags=re.S), "no protocol-relative links"
