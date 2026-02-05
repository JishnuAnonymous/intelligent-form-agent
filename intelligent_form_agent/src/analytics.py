from .storage import StorageManager
import pandas as pd
from collections import Counter
from .utils import setup_logger
import json

logger = setup_logger('analytics')

class AnalyticsEngine:
    def __init__(self):
        self.storage = StorageManager()

    def get_global_stats(self):
        forms = self.storage.get_all_forms()
        total_forms = len(forms)
        
        if total_forms == 0:
            return {"total_forms": 0, "message": "No data available"}

        df_data = []
        for f in forms:
            data = json.loads(f.extracted_data)
            df_data.append(data)
        
        df = pd.DataFrame(df_data)
        
        # Compute Stats
        missing_fields = {}
        for col in ['name', 'phone', 'email']:
            if col in df.columns:
                missing_count = df[col].isnull().sum() + (df[col] == '').sum()
                missing_fields[col] = int(missing_count) # Convert numpy int to py int
        
        signature_missing = int((~df['signature_detected']).sum()) if 'signature_detected' in df.columns else 0

        return {
            "total_forms": total_forms,
            "missing_fields_stats": missing_fields,
            "forms_missing_signature": signature_missing
        }
