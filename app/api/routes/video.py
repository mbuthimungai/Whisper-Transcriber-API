from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_handler import save_upload_file
from app.services.video_utils import extract_audio_from_video
from app.services.whisper_runner import transcribe_audio
from app.models.schema import TranscriptionResponse

router = APIRouter()

@router.post("/", response_model=TranscriptionResponse)
async def upload_video(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    video_path = save_upload_file(file)

    try:
        audio_path = extract_audio_from_video(video_path)
        result = transcribe_audio(audio_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return TranscriptionResponse(
        filename=file.filename,
        transcription=result["text"],
        duration_seconds=result["duration"]
    )
