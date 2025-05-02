import asyncio
import websockets
import wave


SERVER_URI = "ws://localhost:8000/transcribe/live/"
AUDIO_FILE = "sample.wav"


CHUNK_SIZE = 2048

async def send_audio():
    async with websockets.connect(SERVER_URI) as websocket:
        print("Connected to server")

        with wave.open(AUDIO_FILE, 'rb') as wf:
            print("Streaming audio...")
            while True:
                chunk = wf.readframes(CHUNK_SIZE)
                if not chunk:
                    break
                await websocket.send(chunk)
                await asyncio.sleep(CHUNK_SIZE / wf.getframerate())

        print("Finished sending audio")
        await websocket.close()

async def receive_transcripts():
    async with websockets.connect(SERVER_URI) as websocket:
        async def send_audio():
            with wave.open(AUDIO_FILE, 'rb') as wf:
                while True:
                    chunk = wf.readframes(CHUNK_SIZE)
                    if not chunk:
                        break
                    await websocket.send(chunk)
                    await asyncio.sleep(CHUNK_SIZE / wf.getframerate())

        sender = asyncio.create_task(send_audio())

        try:
            while True:
                response = await websocket.recv()
                print("📝 Partial Transcript:", response)
        except websockets.exceptions.ConnectionClosed:
            print("Server closed connection")
        finally:
            sender.cancel()

asyncio.run(receive_transcripts())
