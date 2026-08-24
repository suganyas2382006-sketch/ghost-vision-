import cv2
import mediapipe as mp
import math

class GestureTracker:
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7):
        """
        Initializes the MediaPipe Hands model for gesture recognition.
        max_num_hands is set to 2 to track both hands simultaneously.
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=0.5
        )
        self.tip_ids = [4, 8, 12, 16, 20]

    def detect_gesture(self, frame):
        """
        Processes an image frame and determines if the user wants to be visible or invisible.
        Returns: "INVISIBLE" (Both Closed Fists), "VISIBLE" (Both Open Palms), or None
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        gesture = None

        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            hands_fingers = []
            
            for hand_landmarks in results.multi_hand_landmarks:
                lm_list = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])

                if len(lm_list) != 0:
                    hands_fingers.append(self._get_fingers_up(lm_list))
            
            if len(hands_fingers) == 2:
                # Both hands closed fists
                if hands_fingers[0] == [0, 0, 0, 0, 0] and hands_fingers[1] == [0, 0, 0, 0, 0]:
                    gesture = "INVISIBLE"
                # Both hands open palms
                elif hands_fingers[0] == [1, 1, 1, 1, 1] and hands_fingers[1] == [1, 1, 1, 1, 1]:
                    gesture = "VISIBLE"

        return gesture

    def _get_fingers_up(self, lm_list):
        """
        Determines which fingers are raised.
        Returns [Thumb, Index, Middle, Ring, Pinky] (1 for up, 0 for down)
        """
        fingers = []

        # Thumb calculation
        tip_dist = math.hypot(lm_list[4][1] - lm_list[17][1], lm_list[4][2] - lm_list[17][2])
        knuckle_dist = math.hypot(lm_list[3][1] - lm_list[17][1], lm_list[3][2] - lm_list[17][2])
        
        if tip_dist > knuckle_dist:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers calculation
        for id in range(1, 5):
            if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
