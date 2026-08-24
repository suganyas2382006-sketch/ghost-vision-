import cv2
import mediapipe as mp
import numpy as np

class HumanSegmenter:
    def __init__(self, model_selection=1):
        """
        Initializes the MediaPipe Selfie Segmentation model.
        model_selection: 
        - 0 is optimized for close-up selfies.
        - 1 is optimized for full-body/general scenes.
        """
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segmentor = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=model_selection)

    def get_mask(self, frame, threshold=0.5):
        """
        Processes the frame and returns a single-channel binary mask.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self.segmentor.process(rgb_frame)
        rgb_frame.flags.writeable = True
        
        mask = results.segmentation_mask
        binary_mask = (mask > threshold).astype(np.uint8) * 255
        binary_mask = cv2.GaussianBlur(binary_mask, (5, 5), 0)
        
        return binary_mask
