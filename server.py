import asyncio
import websockets
import cv2
import numpy as np

async def video_stream(websocket, path):  # ✅ Added path argument
    cap = cv2.VideoCapture(0)  # Open webcam

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            _, buffer = cv2.imencode('.jpg', frame)
            await websocket.send(buffer.tobytes())  # Send frame as bytes
            
            await asyncio.sleep(0.03)  # Prevent high CPU usage

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

    finally:
        cap.release()

async def main():
    async with websockets.serve(video_stream, "localhost", 8765):
        await asyncio.Future()  # Keep server running indefinitely

if __name__ == "__main__":
    asyncio.run(main())  # ✅ Proper event loop handling
