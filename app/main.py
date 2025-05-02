from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import audio, video, live

app = FastAPI(title="Whisper Transcriber API", version="1.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/")
def read_root():
    return {"message": "Whisper API is running 🎙️"}

# Register routes
app.include_router(audio.router, prefix="/transcribe/audio", tags=["Audio Transcription"])
app.include_router(video.router, prefix="/transcribe/video", tags=["Video Transcription"])
app.include_router(live.router,  prefix="/transcribe/live",  tags=["Live Mic Transcription"])
