import cv2
import numpy as np

# These imports will work once you build out the rest of your src/ modules
# from src.gesture_recognition import GestureTracker
# from src.segmentation import HumanSegmenter
# from src.visual_effects import apply_invisibility

def main():
    # 1. Initialize Webcam
    cap = cv2.VideoCapture(0)
    
    # 2. Initialize Core Modules (Uncomment when classes are ready)
    # tracker = GestureTracker()
    # segmenter = HumanSegmenter()
    
    background = None
    current_mode = "visible"  # Application starts in visible mode
    
    print("Starting GhostVision (Two-Handed Edition)...")
    print("Controls:")
    print(" - Step out of frame and press 'b' to capture the background.")
    print(" - Raise TWO CLOSED FISTS to become INVISIBLE.")
    print(" - Raise TWO OPEN PALMS to become VISIBLE.")
    print(" - Press 'q' to quit.")
    
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
            gesture = None # Placeholder until the tracker is active
            
            # Step B: Update State based on the two-handed gestures
            # if gesture == "INVISIBLE":
            #     current_mode = "invisible"
            # elif gesture == "VISIBLE":
            #     current_mode = "visible"
            
            # Step C: Apply Segmentation and Visual Effects
            # if current_mode == "invisible":
            #     mask = segmenter.get_mask(frame)
            #     display_frame = apply_invisibility(frame, background, mask)
            pass

        # --- User Interface ---
        # Change text color based on mode (Green for visible, Blue for invisible)
        text_color = (0, 255, 0) if current_mode == "visible" else (255, 150, 0)
        cv2.putText(display_frame, f"Mode: {current_mode.upper()}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)
        
        if background is None:
            cv2.putText(display_frame, "Step away and press 'b' to capture background", 
                        (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        else:
            # Show gesture instructions once background is captured
            cv2.putText(display_frame, "Two Fists: INVISIBLE | Two Palms: VISIBLE", 
                        (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Show the final output
        cv2.imshow('GhostVision', display_frame)

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
