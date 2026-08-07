import cv2
import mediapipe as mp
import numpy as np

class HumanSegmenter:
    def __init__(self, model_selection=1):
        """
        Initializes the MediaPipe Selfie Segmentation model.
        model_selection: 
        - 0 is optimized for close-up selfies (faster).
        - 1 is optimized for full-body/general scenes (better accuracy for stepping back).
        """
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segmentor = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=model_selection)

    def get_mask(self, frame, threshold=0.5):
        """
        Processes the frame to extract the human silhouette.
        Returns a single-channel binary mask where the human is 255 (white) and the background is 0 (black).
        """
        # Convert the BGR image to RGB (required by MediaPipe)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Improve performance by marking the image as not writeable to pass by reference
        rgb_frame.flags.writeable = False
        results = self.segmentor.process(rgb_frame)
        rgb_frame.flags.writeable = True
        
        # The raw mask contains confidence values from 0.0 (definitely background) to 1.0 (definitely human)
        mask = results.segmentation_mask
        
        # Apply the threshold to create a strict black & white binary mask
        # Anything above the threshold becomes 1, then we multiply by 255 to make it standard white
        binary_mask = (mask > threshold).astype(np.uint8) * 255
        
        # Optional: Apply a small blur to the mask edges to make the invisibility blend smoother
        binary_mask = cv2.GaussianBlur(binary_mask, (5, 5), 0)
        
        return binary_mask
