# Intelligent Form Agent

A clean, efficient, and intelligent CLI tool for processing forms, answering questions, and generating insights without Generative AI.

## Features

- **Ingestion**: Supports Images (JPG/PNG) and PDFs.
- **Extraction**: Uses OpenCV and Tesseract OCR for robust text extraction.
- **QA Pipeline**: Answers questions about specific forms or across the entire document collection using TF-IDF/Cosine Similarity.
- **Summarization**: Generates key insight summaries for documents.
- **Local & Private**: Runs 100% locally with no external API calls.

## Setup

1.  **Prerequisites**:
    - Python 3.8+
    - **Tesseract OCR** (Must be installed and in PATH)
        - Windows: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
        - Linux: `sudo apt-get install tesseract-ocr`

2.  **Installation**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The agent is controlled entirely via `src/main.py`.

### 1. Ingest Forms
Process a single file or an entire folder of documents.

```bash
# Process a folder of images/pdfs
python -m src.main --folder data/samples

# Process a single file
python -m src.main --file path/to/invoice.jpg
```

### 2. Ask Questions
Ask a question about a specific form (by ID) or across all forms.

```bash
# Specific Form (ID returned during ingestion)
python -m src.main --ask "What is the total amount?" --form_id 1

# Holistic QA (Search across all forms)
python -m src.main --ask "Who are the vendors?" --ask_all
```

### 3. Summarization
Generate a summary of extracted fields and key content.

```bash
python -m src.main --summary --form_id 1
```

### 4. Global Analytics
View global stats about processed forms.

```bash
python -m src.main --analytics
```

## Graphical User Interface (UI)

If you prefer a visual interface, we have re-implemented a simple Dashboard.

```bash
streamlit run ui/app.py
```

## Demo & Test Data

We have provided a demo script that generates sample data and runs through all key scenarios.

```bash
# Generates data/samples (including a real PDF) and runs the pipeline
python create_test_pdf.py  # Generates data/test_form.pdf
python demo.py
```

## Structure

- `src/`: Core source code.
- `data/`: Storage for forms (and `samples` for demo).
- `instance/`: SQLite database.
- `demo.py`: Automation script for demonstration.
