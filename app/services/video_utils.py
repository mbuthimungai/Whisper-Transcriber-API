import subprocess
import uuid
from pathlib import Path

VIDEO_DIR = Path("uploads/video")
AUDIO_DIR = Path("uploads/audio")
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def extract_audio_from_video(video_path: str) -> str:
    audio_filename = f"{uuid.uuid4()}.wav"
    audio_path = AUDIO_DIR / audio_filename

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  
        "-acodec", "pcm_s16le",
        "-ar", "16000",        
        "-ac", "1",            
        str(audio_path)
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to extract audio from video using ffmpeg")

    return str(audio_path)
