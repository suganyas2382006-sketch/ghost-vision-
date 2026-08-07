# GhostVision 👻

GhostVision is a lightweight, computer vision-based Python application that allows users to become invisible in a live video stream using two-handed gesture controls. 

By leveraging **OpenCV** for image processing and **MediaPipe** for real-time human segmentation and 3D hand tracking, the system replaces the user's silhouette with a pre-captured background, creating a seamless "invisibility cloak" effect.

---

## 🚀 Features

*   **Real-Time Human Segmentation:** Separates the user from the background without the need for a physical green screen.
*   **Two-Handed Gesture Controls:** State toggling using accurate 3D hand landmark detection.
*   **Dynamic Background Substitution:** Replaces the segmented user with a clean background matrix.
*   **Lightweight & Modular:** Optimized for high FPS on standard webcams with a clean, object-oriented codebase.

---

## 📂 Project Structure

```text
ghostvision/
├── src/
│   ├── __init__.py               # Exposes core modules
│   ├── gesture_recognition.py    # MediaPipe hand tracking & logic
│   ├── segmentation.py           # MediaPipe selfie segmentation
│   └── visual_effects.py         # OpenCV image math & masking
├── main.py                       # Main application loop
├── requirements.txt              # Dependencies
└── README.md                     # Project documentation
