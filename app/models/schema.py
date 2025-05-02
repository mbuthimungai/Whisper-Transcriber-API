from pydantic import BaseModel

class TranscriptionResponse(BaseModel):
    filename: str
    transcription: str
    duration_seconds: float
