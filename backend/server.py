import cv2
import numpy as np
import base64
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from src.gesture_recognition import GestureTracker
from src.segmentation import HumanSegmenter
from src.visual_effects import apply_invisibility

app = FastAPI(title="GhostVision Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tracker = GestureTracker()
segmenter = HumanSegmenter()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    background = None
    current_mode = "visible"

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            img_data = base64.b64decode(message["image"].split(',')[1])
            np_arr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                continue

            if message.get("command") == "capture_background":
                background = frame.copy()
                
            if background is not None:
                gesture = tracker.detect_gesture(frame)
                if gesture == "INVISIBLE":
                    current_mode = "invisible"
                elif gesture == "VISIBLE":
                    current_mode = "visible"

                if current_mode == "invisible":
                    mask = segmenter.get_mask(frame)
                    frame = apply_invisibility(frame, background, mask)

            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            b64_img = base64.b64encode(buffer).decode('utf-8')
            
            await websocket.send_json({
                "image": f"data:image/jpeg;base64,{b64_img}",
                "mode": current_mode,
                "has_background": background is not None
            })

    except WebSocketDisconnect:
        print("Client disconnected from WebSocket")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
