import os
import cv2
import numpy as np
from .utils import setup_logger

logger = setup_logger('ingestion')

try:
    import pdfplumber
except ImportError:
    pdfplumber = None
    logger.warning("pdfplumber not found. Digital PDF extraction will not work.")

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None
    logger.warning("PyMuPDF (fitz) not found. PDF to Image conversion will not work.")


def load_file(file_path):
    """
    Determines if file is PDF or Image and routes accordingly.
    Returns a list of dicts: [{'text': '...', 'image': np.array}]
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        return process_pdf(file_path)
    elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        return process_image_file(file_path)
    else:
        logger.error(f"Unsupported file format: {ext}")
        return []

def process_image_file(file_path):
    logger.info(f"Processing image: {file_path}")
    img = cv2.imread(file_path)
    return [{'text': None, 'image': img, 'page': 1}]

def process_pdf(pdf_path):
    logger.info(f"Processing PDF: {pdf_path}")
    results = []
    
    # Try to extract text directly first (Digital PDF)
    if pdfplumber:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    
                    # Also convert to image for OCR backup / Layout analysis
                    # We use PyMuPDF (fitz) for better image conversion usually, 
                    # but pdfplumber relies on it anyway. Let's stick to fitz for image rendering.
                    pass
        except Exception as e:
            logger.warning(f"pdfplumber failed: {e}")
    else:
        logger.warning("pdfplumber not installed. Skipping direct text extraction.")

    # Use PyMuPDF for reliable rendering
    if fitz:
        try:
            doc = fitz.open(pdf_path)
            for i in range(len(doc)):
                page = doc.load_page(i)
                
                # Extract text via PyMuPDF as well
                text = page.get_text()
                
                # Render page to image
                pix = page.get_pixmap(dpi=300)
                img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
                
                # Convert RGB/RGBA to BGR for OpenCV
                if pix.n == 3: # RGB
                    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                elif pix.n == 4: # RGBA
                    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
                else:
                    img_bgr = img_array # Grayscale?

                results.append({
                    'text': text if text.strip() else None,
                    'image': img_bgr,
                    'page': i + 1
                })
        except Exception as e:
            logger.error(f"PyMuPDF failed: {e}")
    else:
        logger.error("PyMuPDF is not installed. Cannot process PDF images.")
    
    return results
