import cv2

from src.gesture_recognition import GestureTracker
from src.segmentation import HumanSegmenter
from src.visual_effects import apply_invisibility


def main():
    # ============================================================
    # 1. Initialize Webcam
    # ============================================================
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        return

    # ============================================================
    # 2. Initialize Computer Vision Modules
    # ============================================================
    tracker = GestureTracker()
    segmenter = HumanSegmenter()

    # ============================================================
    # 3. Application State
    # ============================================================
    background = None
    current_mode = "visible"

    print("\n========================================")
    print("       GhostVision - Started")
    print("========================================")
    print("Controls:")
    print("  B -> Capture background")
    print("  Two closed fists -> INVISIBLE")
    print("  Two open palms  -> VISIBLE")
    print("  Q -> Quit")
    print("========================================\n")

    # ============================================================
    # 4. Main Real-Time Processing Loop
    # ============================================================
    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            print("Warning: Could not read camera frame.")
            continue

        # Mirror the camera for natural selfie-view
        frame = cv2.flip(frame, 1)

        # Start with the original frame
        display_frame = frame.copy()

        # ========================================================
        # Keyboard Controls
        # ========================================================
        key = cv2.waitKey(1) & 0xFF

        # --------------------------------------------------------
        # Capture background
        # --------------------------------------------------------
        if key == ord("b"):
            background = frame.copy()
            current_mode = "visible"

            print("Background captured successfully!")
            print("Step back into the frame and raise TWO CLOSED FISTS.")

        # --------------------------------------------------------
        # Quit
        # --------------------------------------------------------
        elif key == ord("q"):
            print("Closing GhostVision...")
            break

        # ========================================================
        # Main Vision Pipeline
        # ========================================================
        if background is not None:

            # ----------------------------------------------------
            # Step A: Detect hand gesture
            # ----------------------------------------------------
            gesture = tracker.detect_gesture(frame)

            # ----------------------------------------------------
            # Step B: Update application mode
            # ----------------------------------------------------
            if gesture == "INVISIBLE":
                current_mode = "invisible"

            elif gesture == "VISIBLE":
                current_mode = "visible"

            # ----------------------------------------------------
            # Step C: Apply invisibility effect
            # ----------------------------------------------------
            if current_mode == "invisible":

                # Generate human segmentation mask
                mask = segmenter.get_mask(frame)

                # Replace human region with captured background
                display_frame = apply_invisibility(
                    frame,
                    background,
                    mask
                )

        # ========================================================
        # User Interface
        # ========================================================

        # Green = visible
        # Orange/Blue = invisible
        if current_mode == "visible":
            text_color = (0, 255, 0)
        else:
            text_color = (255, 150, 0)

        # --------------------------------------------------------
        # Current mode
        # --------------------------------------------------------
        cv2.putText(
            display_frame,
            f"Mode: {current_mode.upper()}",
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            text_color,
            2,
            cv2.LINE_AA
        )

        # --------------------------------------------------------
        # Instructions
        # --------------------------------------------------------
        if background is None:

            cv2.putText(
                display_frame,
                "Step away and press 'B' to capture background",
                (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
                cv2.LINE_AA
            )

        else:

            cv2.putText(
                display_frame,
                "Two Fists: INVISIBLE | Two Palms: VISIBLE",
                (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

        # --------------------------------------------------------
        # Display final frame
        # --------------------------------------------------------
        cv2.imshow("GhostVision", display_frame)

    # ============================================================
    # 5. Cleanup
    # ============================================================
    cap.release()
    cv2.destroyAllWindows()


# ================================================================
# Application Entry Point
# ================================================================
if __name__ == "__main__":
    main()
