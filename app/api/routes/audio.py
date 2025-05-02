from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_handler import save_upload_file
from app.services.whisper_runner import transcribe_audio
from app.models.schema import TranscriptionResponse
router = APIRouter()

@router.get("/test")
async def test_audio():
    return {"message": "Audio route works!"}




router = APIRouter()

@router.post("/", response_model=TranscriptionResponse)
async def upload_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    path = save_upload_file(file)
    result = transcribe_audio(path)

    return TranscriptionResponse(
        filename=file.filename,
        transcription=result["text"],
        duration_seconds=result["duration"]
    )
