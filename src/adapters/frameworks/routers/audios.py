from typing import List
from fastapi import APIRouter, UploadFile, HTTPException
from services.transcribe import transcribe

router = APIRouter(
    prefix="/audios",
    tags=["audios"],
    responses={404: {"description": "Not found"}},
)

# Allowed audio MIME types
allowed_audio_types = {"audio/mpeg", "audio/wav", "audio/ogg", "audio/mp3"}


@router.post("/upload")
def upload_files(files: List[UploadFile]):

    for file in files:
        if file.content_type not in allowed_audio_types:
            raise HTTPException(status_code=400, detail="Unsupported audio type")

    return transcribe(files)
