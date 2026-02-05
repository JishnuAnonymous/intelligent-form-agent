import cv2
import numpy as np
from .utils import setup_logger

logger = setup_logger('preprocessing')

def preprocess_image(image_path_or_array):
    """
    Applies preprocessing pipeline to an image:
    1. Grayscale
    2. Denoising
    3. Thresholding
    Returns the processed image.
    """
    try:
        if isinstance(image_path_or_array, str):
            img = cv2.imread(image_path_or_array)
            if img is None:
                raise ValueError(f"Could not load image at {image_path_or_array}")
        else:
            img = image_path_or_array

        # 1. Grayscale
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        # 2. Denoise (Gaussian Blur)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 3. Thresholding (Adaptive)
        # This helps with varying lighting conditions
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Optional: Dilation/Erosion to remove noise
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.dilate(thresh, kernel, iterations=1)
        processed = cv2.erode(processed, kernel, iterations=1)

        logger.info("Image preprocessing successful")
        return processed

    except Exception as e:
        logger.error(f"Error in preprocessing: {e}")
        return None
