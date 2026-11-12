"""Local web server: accepts one audio upload and returns its transcript.

Run: .venv/bin/uvicorn app.server:app --host 127.0.0.1 --port 8000
"""

import logging
import os
import tempfile
from pathlib import PurePath

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.transcribe import TranscribeError, transcribe

ALLOWED_EXTENSIONS = {".mp3", ".m4a", ".wav", ".webm"}
MAX_BYTES = 50 * 1024 * 1024
CHUNK = 1024 * 1024
TEMP_DIR = None  # None means the system temp folder; tests point it elsewhere.

MSG_NO_FILE = "Please choose an audio file to upload."
MSG_WRONG_TYPE = "Please upload an mp3, m4a, wav or webm file."
MSG_TOO_BIG = "This file is larger than 50 MB. Please upload a smaller one."
MSG_UNEXPECTED = "Something went wrong while transcribing. Please try again."

log = logging.getLogger("transcriber")
app = FastAPI(title="Transcriber")


def error(status: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": message})


@app.exception_handler(RequestValidationError)
async def bad_request(_request: Request, _exc: RequestValidationError) -> JSONResponse:
    return error(400, MSG_NO_FILE)


class _TooBig(Exception):
    pass


def txt_name(upload_name: str) -> str:
    """'team meeting.m4a' -> 'team meeting.txt'; folders in the name are dropped."""
    base = PurePath(upload_name.replace("\\", "/")).name
    stem = base.rsplit(".", 1)[0] if "." in base else base
    return f"{stem or 'transcript'}.txt"


def _save_to_temp(upload: UploadFile, suffix: str) -> str:
    fd, path = tempfile.mkstemp(suffix=suffix, dir=TEMP_DIR)
    try:
        size = 0
        with os.fdopen(fd, "wb") as out:
            while chunk := upload.file.read(CHUNK):
                size += len(chunk)
                if size > MAX_BYTES:
                    raise _TooBig
                out.write(chunk)
    except BaseException:
        os.unlink(path)
        raise
    return path


@app.post("/transcribe")
def transcribe_upload(file: UploadFile | None = File(None)) -> JSONResponse:
    if file is None or not file.filename:
        return error(400, MSG_NO_FILE)

    base = PurePath(file.filename.replace("\\", "/")).name
    suffix = "." + base.rsplit(".", 1)[1].lower() if "." in base else ""
    if suffix not in ALLOWED_EXTENSIONS:
        return error(400, MSG_WRONG_TYPE)

    try:
        path = _save_to_temp(file, suffix)
    except _TooBig:
        return error(400, MSG_TOO_BIG)

    try:
        text = transcribe(path)
    except TranscribeError as exc:
        return error(400, str(exc))
    except Exception:
        log.exception("Unexpected error while transcribing %s", file.filename)
        return error(500, MSG_UNEXPECTED)
    finally:
        os.unlink(path)

    return JSONResponse({"text": text, "filename": txt_name(file.filename)})
