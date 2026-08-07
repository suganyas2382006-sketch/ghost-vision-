import cv2
import numpy as np

def apply_invisibility(frame, background, mask):
    """
    Replaces the segmented human (defined by the mask) with the saved background.
    
    Args:
        frame: The current live video frame (BGR format).
        background: The saved background image (BGR format).
        mask: The binary mask from the segmentation model (single channel, 255 for human, 0 for background).
        
    Returns:
        The final composite frame with the invisibility effect applied.
    """
    # 1. Convert the single-channel mask into a boolean array (True for human, False for background)
    mask_bool = mask > 127
    
    # 2. Expand the mask to 3 color channels (BGR) so it matches the shape of the video frames
    mask_3d = np.stack([mask_bool] * 3, axis=-1)
    
    # 3. Combine the images using NumPy's `where` function
    # Read as: "Where the mask is True (human), use the saved background pixels. 
    # Otherwise, use the live frame pixels."
    output_frame = np.where(mask_3d, background, frame)
    
    return output_frame.astype(np.uint8)
