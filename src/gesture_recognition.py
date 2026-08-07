import cv2
import mediapipe as mp

class GestureTracker:
    def __init__(self, static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7):
        """
        Initializes the MediaPipe Hands model for gesture recognition.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=0.5
        )
        # Landmark IDs for finger tips
        self.tip_ids = [4, 8, 12, 16, 20]

    def detect_gesture(self, frame):
        """
        Processes an image frame and determines if the user wants to be visible or invisible.
        Returns: "INVISIBLE" (Open Palm), "VISIBLE" (Closed Fist), or None
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])

                if len(lm_list) != 0:
                    fingers_up = self._get_fingers_up(lm_list)
                    
                    # 1. Check Open Palm (Turn Invisible)
                    if fingers_up == [1, 1, 1, 1, 1]:
                        gesture = "INVISIBLE"
                        
                    # 2. Check Closed Fist (Turn Visible)
                    elif fingers_up == [0, 0, 0, 0, 0]:
                        gesture = "VISIBLE"

        return gesture

    def _get_fingers_up(self, lm_list):
        """
        Determines which fingers are currently raised.
        Returns a list of 5 integers (1 for up, 0 for down) representing [Thumb, Index, Middle, Ring, Pinky]
        """
        fingers = []

        # Thumb
        if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
