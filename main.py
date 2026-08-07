import cv2
import numpy as np

# These imports will work once you build out your src/ modules
# from src.gesture_recognition import GestureTracker
# from src.segmentation import HumanSegmenter
# from src.visual_effects import apply_invisibility, apply_ghost_mode, take_screenshot

def main():
    # 1. Initialize Webcam
    cap = cv2.VideoCapture(0)
    
    # 2. Initialize Core Modules (Uncomment when classes are ready)
    # tracker = GestureTracker()
    # segmenter = HumanSegmenter()
    
    background = None
    current_mode = "normal"  # Available modes: normal, invisible, ghost
    
    print("Starting GhostVision...")
    print("Press 'b' to capture the background (step out of frame first!).")
    print("Press 'q' to quit.")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
            
        # Flip the frame horizontally for a natural selfie-view
        frame = cv2.flip(frame, 1)
        display_frame = frame.copy()
        
        # --- Keyboard Controls ---
        key = cv2.waitKey(1) & 0xFF
        
        # Capture Background
        if key == ord('b'):
            background = frame.copy()
            print("Background captured! You can now step back into the frame.")
            
        # Exit Application
        elif key == ord('q'):
            break

        # --- Main Pipeline (Requires background to be captured first) ---
        if background is not None:
            # Step A: Detect Gestures
            # gesture = tracker.detect_gesture(frame)
            gesture = None # Placeholder until module is built
            
            # Step B: Update State based on Gesture
            # if gesture == "OPEN_PALM":
            #     current_mode = "invisible"
            # elif gesture == "PEACE_SIGN":
            #     current_mode = "ghost"
            # elif gesture == "CLOSED_FIST":
            #     current_mode = "normal"
            # elif gesture == "PINCH":
            #     take_screenshot(display_frame)
            
            # Step C: Apply Segmentation and Visual Effects
            # if current_mode in ["invisible", "ghost"]:
            #     mask = segmenter.get_mask(frame)
                
            #     if current_mode == "invisible":
            #         display_frame = apply_invisibility(frame, background, mask)
            #     elif current_mode == "ghost":
            #         display_frame = apply_ghost_mode(frame, background, mask)
            pass

        # --- User Interface ---
        cv2.putText(display_frame, f"Mode: {current_mode}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if background is None:
            cv2.putText(display_frame, "Step away and press 'b' to capture background", 
                        (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Show the final output
        cv2.imshow('GhostVision', display_frame)

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
