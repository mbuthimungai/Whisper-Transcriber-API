import whisper
import os

model = whisper.load_model("base")

def transcribe_audio(file_path: str) -> dict:
    result = model.transcribe(file_path)
    return {
        "text": result["text"],
        "duration": result["segments"][-1]["end"] if result["segments"] else 0.0
    }
