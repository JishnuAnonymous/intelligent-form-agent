import argparse
import sys
import os
import json
from .ingestion import load_file
from .preprocessing import preprocess_image
from .ocr import extract_text_from_image
from .extractor import FormExtractor
from .storage import StorageManager
from .qa import QAEcosystem
from .summarizer import Summarizer
from .analytics import AnalyticsEngine
from . import utils

logger = utils.setup_logger('main')

def process_file(filepath):
    # 1. Ingestion
    pages = load_file(filepath)
    if not pages:
        logger.error("No content loaded.")
        return

    full_text = ""
    # Process only first page for this MVP if multi-page, or concat? 
    # Let's simple concat text
    
    for page in pages:
        if page['text']:
            full_text += page['text'] + "\n"
        elif page['image'] is not None:
             # 2. Preprocessing
             processed_img = preprocess_image(page['image'])
             if processed_img is not None:
                 # 3. OCR
                 text = extract_text_from_image(processed_img)
                 full_text += text + "\n"
    
    # 4. Extraction
    extractor = FormExtractor()
    data = extractor.extract_fields(full_text)
    data['raw_text'] = full_text # optionally store here for display
    
    # 5. Storage
    storage = StorageManager()
    form_id = storage.save_form(filepath, full_text, data)
    
    print(json.dumps(data, indent=2, default=str))
    print(f"\n[INFO] Form saved with ID: {form_id}")
    return form_id

def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        logger.error(f"Folder not found: {folder_path}")
        return

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg'))]
    print(f"Found {len(files)} files in {folder_path}...")
    
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        print(f"Processing {filename}...")
        try:
            process_file(filepath)
        except Exception as e:
            logger.error(f"Failed to process {filename}: {e}")

def ask_question(question, form_id):
    storage = StorageManager()
    form = storage.get_form(form_id)
    if not form:
        logger.error(f"Form ID {form_id} not found.")
        return

    qa = QAEcosystem()
    try:
        extracted = json.loads(form.extracted_data)
    except:
        extracted = {}
        
    answer = qa.answer_question(question, form.raw_text, extracted)
    print(f"\nQ: {question}\nA: {answer}")

def ask_all(question):
    storage = StorageManager()
    forms = storage.get_all_forms()
    
    if not forms:
        print("No forms processed yet.")
        return

    context = [f.raw_text for f in forms]
    
    qa = QAEcosystem()
    answer = qa.answer_across_documents(question, context)
    print(f"\n[Holistic] Q: {question}\nA: {answer}")

def get_summary(form_id):
    storage = StorageManager()
    form = storage.get_form(form_id)
    if not form:
        logger.error(f"Form ID {form_id} not found.")
        return

    summ = Summarizer()
    try:
        extracted = json.loads(form.extracted_data)
    except:
        extracted = {}
        
    summary_text = summ.generate_summary(extracted, form.raw_text)
    print(f"\n=== Summary for Form {form_id} ===\n{summary_text}")

def show_analytics():
    analytics = AnalyticsEngine()
    stats = analytics.get_global_stats()
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Intelligent Form Agent CLI")
    parser.add_argument('--file', help="Path to form file to process")
    parser.add_argument('--folder', help="Path to folder of forms to process")
    parser.add_argument('--ask', help="Question to ask")
    parser.add_argument('--form_id', type=int, help="Form ID for QA context (specific form)")
    parser.add_argument('--ask_all', action='store_true', help="Ask question across ALL processed forms (requires --ask)")
    parser.add_argument('--summary', action='store_true', help="Generate summary for a form (requires --form_id)")
    parser.add_argument('--analytics', action='store_true', help="Show global stats")

    args = parser.parse_args()

    utils.ensure_dirs()

    if args.file:
        process_file(args.file)
    elif args.folder:
        process_folder(args.folder)
    elif args.ask:
        if args.ask_all:
             ask_all(args.ask)
        elif args.form_id:
             ask_question(args.ask, args.form_id)
        else:
            print("Error: For QA, provide either --form_id OR --ask_all")
    elif args.summary and args.form_id:
        get_summary(args.form_id)
    elif args.analytics:
        show_analytics()
    else:
        parser.print_help()
