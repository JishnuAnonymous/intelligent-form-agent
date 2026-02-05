import logging
import json
import os
from . import config

def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger('utils')

def save_json(data, filename):
    filepath = os.path.join(config.OUTPUT_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, default=str)
        logger.info(f"Saved JSON to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to save JSON: {e}")
        return None

def ensure_dirs():
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    os.makedirs(config.SAMPLE_DIR, exist_ok=True)
