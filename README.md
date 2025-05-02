# Whisper Transcriber API (FastAPI)

This is the backend for the [Whisper Transcriber App](https://github.com/mbuthimungai/Whisper-Transcriber-App), built with FastAPI and powered by OpenAI's Whisper (or whisper.cpp) for real-time and file-based transcription.

---

## Features

- **Live mic transcription** via WebSockets
- **Audio file transcription** (`.wav`, `.mp3`, etc)
- **Video file transcription** (`.mp4` → audio → text)
- Supports both [Whisper (Python)](https://github.com/openai/whisper) and [whisper.cpp (C++)](https://github.com/ggerganov/whisper.cpp)

---

## Getting Started

### 1. Clone the API

```bash
git clone https://github.com/mbuthimungai/Whisper-Transcriber-API.git
cd Whisper-Transcriber-API
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Install Whisper (Python version)

```bash
pip install git+https://github.com/openai/whisper.git
```

> If you're using whisper.cpp, make sure it’s compiled and callable from a subprocess in your system.

### 4. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

Server will run on `http://localhost:8000` by default.

---

## Requirements

- Python 3.10+
- `ffmpeg` installed and in PATH
- Either `whisper` (Python) or `whisper.cpp` (C++) installed

---

## API Endpoints

| Endpoint            | Method | Description                                   |
| ------------------- | ------ | --------------------------------------------- |
| `/transcribe/live`  | WS     | Live audio streaming + transcript (WebSocket) |
| `/transcribe/audio` | POST   | Upload audio file                             |
| `/transcribe/video` | POST   | Upload video file                             |

---

## Use with the Mobile App

You can connect this API to the mobile client:
[Whisper Transcriber App (React Native)](https://github.com/mbuthimungai/Whisper-Transcriber-App)

Example:

```ts
export default {
  WS_BASE_URL: "ws://<your-ip>:8000",
  HTTP_BASE_URL: "http://<your-ip>:8000",
};
```

---

## To-Do

- [ ] Dockerize the application
- [ ] Add language detection
- [ ] Add SRT/VTT export
- [ ] Improve chunk handling and error messages
- [ ] whisper.cpp wrapper support for live stream

---

## Author

**Mbuthi Mungai**
Senior Software Engineer
🔗 [GitHub](https://github.com/mbuthimungai) • [LinkedIn](https://www.linkedin.com/in/mbuthi-mungai/)
