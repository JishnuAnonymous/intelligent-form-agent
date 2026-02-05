import pytesseract
from . import config
from .utils import setup_logger

logger = setup_logger('ocr')

# Set Tesseract Command
pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD

def extract_text_from_image(image):
    """
    Uses Tesseract to extract text from an OpenCV image.
    Returns raw text.
    """
    try:
        # Tesseract expects RGB usually, but works with BGR/Grayscale too.
        # Let's treat it as is often standard.
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"OCR Failed: {e}")
        return ""

def extract_data_from_image(image):
    """
    Returns detailed dataframe with layout info.
    """
    try:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        return data
    except Exception as e:
        logger.error(f"OCR Data Extraction Failed: {e}")
        return None
