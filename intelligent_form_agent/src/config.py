import os
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(DATA_DIR, 'outputs')
SAMPLE_DIR = os.path.join(DATA_DIR, 'sample_forms')
DB_PATH = os.path.join(DATA_DIR, 'forms.db')

# Tesseract Configuration
# Attempt to find tesseract in common locations if not in PATH
TESSERACT_CMD = 'tesseract'
if sys.platform == 'win32':
    common_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        os.environ.get('TESSERACT_PATH')
    ]
    for path in common_paths:
        if path and os.path.exists(path):
            TESSERACT_CMD = path
            break

# Extraction Patterns (Regex)
PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'(?:(?:\+|00)88|01)?\d{11}|(?:\+?1[-. ]?)?\(?[2-9]\d{2}\)?[-. ]?\d{3}[-. ]?\d{4}', # Basic global + US match
    'date': r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',
    'currency': r'[\$€£]\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
}

# Field Mappings (Synonyms)
FIELD_SYNONYMS = {
    'name': ['name', 'full name', 'applicant name', 'client name'],
    'dob': ['dob', 'date of birth', 'birth date'],
    'phone': ['phone', 'mobile', 'cell', 'contact info', 'telephone'],
    'email': ['email', 'e-mail', 'email address'],
    'address': ['address', 'residence', 'location'],
    'amount': ['amount', 'total', 'price', 'cost'],
    'form_id': ['form id', 'application id', 'id number', 'reference no']
}

# QA Configuration
TFIDF_TOP_K = 3
