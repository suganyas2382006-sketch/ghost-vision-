import cv2
import numpy as np

def apply_invisibility(frame, background, mask):
    """
    Replaces the segmented human mask with the saved background.
    """
    mask_bool = mask > 127
    mask_3d = np.stack([mask_bool] * 3, axis=-1)
    output_frame = np.where(mask_3d, background, frame)
    return output_frame.astype(np.uint8)
