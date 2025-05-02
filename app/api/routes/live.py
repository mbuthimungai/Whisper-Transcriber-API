# import uuid
# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from app.services.whisper_runner import transcribe_audio

# from pathlib import Path

# router = APIRouter()
# TEMP_AUDIO_DIR = Path("uploads/live")
# TEMP_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# @router.websocket("/")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     print("Client connected.")

#     audio_file_path = TEMP_AUDIO_DIR / f"{uuid.uuid4()}.wav"

#     try:
#         with open(audio_file_path, "wb") as f:
#             while True:
#                 data = await websocket.receive_bytes()
#                 f.write(data)

#     except WebSocketDisconnect:
#         print("Client disconnected. Processing audio...")

#         # Transcribe the full audio file
#         result = transcribe_audio(str(audio_file_path))

#         # You could use background tasks here too
#         await websocket.close()
#         print("Transcription complete.")
#         return

#     except Exception as e:
#         await websocket.close()
#         raise e

import uuid
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.whisper_runner import transcribe_audio
from pathlib import Path
import wave
router = APIRouter()

CHUNK_DURATION_SEC = 4
TEMP_AUDIO_DIR = Path("uploads/live")
TEMP_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected.")

    session_id = str(uuid.uuid4())
    buffer_path = TEMP_AUDIO_DIR / f"{session_id}_buffer.wav"
    audio_buffer = bytearray()

    

    async def transcribe_and_send(buffer: bytes):

        print(f"[INFO] Chunk size: {len(buffer)}")
        # print(f"[INFO] Saving WAV: {temp_file}")

        temp_file = TEMP_AUDIO_DIR / f"{uuid.uuid4()}.wav"

        with wave.open(str(temp_file), "wb") as wf:
            wf.setnchannels(1)        
            wf.setsampwidth(2)        
            wf.setframerate(16000)    
            wf.writeframes(buffer)

        try:
            result = transcribe_audio(str(temp_file))
            print(result["text"])
            await websocket.send_json({"text": result["text"]})
        except Exception as e:
            await websocket.send_json({"error": str(e)})
        finally:
            temp_file.unlink(missing_ok=True)



    try:
        while True:
            data = await websocket.receive_bytes()
            audio_buffer.extend(data)

            if len(audio_buffer) > 32000 * CHUNK_DURATION_SEC:  # Assuming 16-bit mono @ 16kHz
                await transcribe_and_send(audio_buffer)
                audio_buffer.clear()

    # except WebSocketDisconnect:
    #     print("Client disconnected. Finalizing...")
    #     if audio_buffer:
    #         await transcribe_and_send(audio_buffer)
    #     await websocket.close()
    #     print("Connection closed.")
    except WebSocketDisconnect:
        print("Client disconnected. Finalizing...")

        if audio_buffer:
            await transcribe_and_send(audio_buffer)

        # 🔥 REMOVE this line:
        # await websocket.close()

        print("Connection closed.")


    except Exception as e:
        await websocket.close()
        raise e
