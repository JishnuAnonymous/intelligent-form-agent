import re
import json
from . import config
from .utils import setup_logger

logger = setup_logger('extractor')

class FormExtractor:
    def __init__(self):
        self.patterns = config.PATTERNS
        self.synonyms = config.FIELD_SYNONYMS

    def extract_fields(self, text):
        """
        Main extraction method.
        Input: Raw text (str)
        Output: Dict of extracted fields
        """
        data = {
            "name": None,
            "dob": None,
            "phone": None,
            "email": None,
            "address": None,
            "amount": None,
            "form_id": None,
            "signature_detected": False
        }

        # 1. Regex Extraction
        data['email'] = self._extract_regex('email', text)
        data['phone'] = self._extract_regex('phone', text)
        data['date'] = self._extract_regex('date', text) # General date
        data['amount'] = self._extract_regex('currency', text)
        
        # 2. Keyword/Context Extraction
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            # Simple keyword value lookups (e.g. "Name: John Doe")
            if not data['name']:
                data['name'] = self._find_value_by_keywords(line, self.synonyms['name'])
            
            if not data['dob']: # distinct from regex date finding
                 val = self._find_value_by_keywords(line, self.synonyms['dob'])
                 if val: data['dob'] = val

            if not data['address']:
                 val = self._find_value_by_keywords(line, self.synonyms['address'])
                 if val: data['address'] = val
            
            if not data['form_id']:
                 val = self._find_value_by_keywords(line, self.synonyms['form_id'])
                 if val: data['form_id'] = val

            # Signature Detection
            if "signature" in line_lower:
                data['signature_detected'] = True

        # Fallbacks or Cleanups
        if data['date'] and not data['dob']:
            data['dob'] = data['date'] # Assumption if explicit DOB not found

        return data

    def _extract_regex(self, key, text):
        match = re.search(self.patterns[key], text)
        return match.group(0) if match else None

    def _find_value_by_keywords(self, line, keywords):
        """
        Looks for "Keyword: Value" pattern.
        """
        lower_line = line.lower()
        for kw in keywords:
            if kw in lower_line:
                # Split by colon or just take the rest of the line
                # e.g. "Name: John" or "Name John"
                # We prioritize colon
                if ':' in line:
                    parts = line.split(':', 1)
                    if kw in parts[0].lower():
                        return parts[1].strip()
                
                # If no colon, maybe it's "Name John Doe"
                # Check if line starts with keyword
                if lower_line.startswith(kw):
                    return line[len(kw):].strip()
        return None
