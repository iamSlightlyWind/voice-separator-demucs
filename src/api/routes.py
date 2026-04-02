from __future__ import annotations

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path

import torch
from fastapi import BackgroundTasks
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from src.core import AudioSeparator, DEFAULT_MODEL, SUPPORTED_MODELS, get_audio_separator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Voice Separator Demucs API",
    description="API-only service for separating vocals and background audio with Demucs.",
    version="2.0.0",
)

ALLOWED_AUDIO_FORMATS = {
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/flac",
    "audio/mp4",
    "audio/aac",
    "audio/ogg",
    "application/octet-stream",
}
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg"}


def _validate_upload(file: UploadFile) -> None:
    if file.content_type in ALLOWED_AUDIO_FORMATS:
        return
    suffix = Path(file.filename or "").suffix.lower()
    if suffix in ALLOWED_EXTENSIONS:
        return
    raise HTTPException(
        status_code=400,
        detail=f"Unsupported file format. Use one of: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
    )


@app.get("/health")
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "default_model": DEFAULT_MODEL,
        "gpu_available": torch.cuda.is_available(),
        "device": "cuda" if torch.cuda.is_available() else "cpu",
    }


@app.get("/models")
async def models() -> dict[str, object]:
    return {
        "default_model": DEFAULT_MODEL,
        "models": AudioSeparator.get_available_models(),
    }


@app.post("/separate")
async def separate_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    model: str = DEFAULT_MODEL,
) -> FileResponse:
    if model not in SUPPORTED_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model: {model}. Supported models: {list(SUPPORTED_MODELS.keys())}",
        )

    _validate_upload(file)

    input_suffix = Path(file.filename or "input.wav").suffix or ".wav"
    stem_name = Path(file.filename or "audio").stem or "audio"

    try:
        separator = get_audio_separator(model)
    except Exception as exc:
        logger.exception("Failed to initialize separator")
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        temp_root = Path(tempfile.mkdtemp(prefix="voice-separator-"))
        upload_path = temp_root / f"input{input_suffix}"
        output_dir = temp_root / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        content = await file.read()
        upload_path.write_bytes(content)

        result_paths = separator.separate_stems(
            str(upload_path),
            ["vocals", "other"],
            output_dir=output_dir,
        )

        zip_path = temp_root / f"{stem_name}_separated.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(result_paths["vocals"], arcname="vocals.mp3")
            archive.write(result_paths["other"], arcname="other.mp3")

        background_tasks.add_task(shutil.rmtree, temp_root, ignore_errors=True)
        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename=zip_path.name,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Audio separation failed")
        raise HTTPException(status_code=500, detail=f"Audio separation failed: {exc}") from exc
    finally:
        try:
            await file.close()
        except OSError:
            pass
