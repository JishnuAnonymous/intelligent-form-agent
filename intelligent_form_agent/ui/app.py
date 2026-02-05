import streamlit as st
import os
import sys
import json
import time

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import main
from src.storage import StorageManager
from src.qa import QAEcosystem
from src.summarizer import Summarizer
from src.ingestion import load_file
from src.preprocessing import preprocess_image
from src.ocr import extract_text_from_image
from src.extractor import FormExtractor
from src import utils

# Page Config
st.set_page_config(
    page_title="Intelligent Form Agent", 
    page_icon="🤖", 
    layout="centered"
)

# Custom CSS for polish
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50; 
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .summary-box {
        background-color: #ffffff;
        color: #000000;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Intelligent Form Agent")
st.markdown("### Secure, Local, Intelligent Document Processing")

# Initialize Session State
if 'form_id' not in st.session_state: st.session_state['form_id'] = None
if 'extracted_data' not in st.session_state: st.session_state['extracted_data'] = {}
if 'raw_text' not in st.session_state: st.session_state['raw_text'] = ""
if 'summary' not in st.session_state: st.session_state['summary'] = ""

# --- SECTION 1: UPLOAD ---
st.markdown("---")
st.subheader("1. Upload Document")
uploaded_file = st.file_uploader("Upload Invoice/Image/PDF", type=['pdf', 'png', 'jpg', 'jpeg'])

if uploaded_file:
    if st.button("Process Document"):
        with st.spinner("Analyzing document..."):
            # Save temp file
            utils.ensure_dirs()
            temp_path = os.path.join("data", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Processing Pipeline
            # 1. Ingestion
            pages = load_file(temp_path)
            full_text = ""
            for p in pages:
                    if p['text']: full_text += p['text'] + "\n"
                    elif p['image'] is not None:
                        processed = preprocess_image(p['image'])
                        text = extract_text_from_image(processed)
                        full_text += text + "\n"
            
            # 2. Extraction
            ext = FormExtractor()
            data = ext.extract_fields(full_text)
            
            # 3. Save
            storage = StorageManager()
            fid = storage.save_form(temp_path, full_text, data)
            
            # 4. Summarize immediately
            summ = Summarizer()
            summary_text = summ.generate_summary(data, full_text)

            # Update State
            st.session_state['form_id'] = fid
            st.session_state['extracted_data'] = data
            st.session_state['raw_text'] = full_text
            st.session_state['summary'] = summary_text
            
            st.success("Document processed successfully!")
            time.sleep(0.5)
            st.rerun()

# --- SECTION 2: RESULTS ---
if st.session_state['form_id']:
    st.markdown("---")
    
    # Two columns: visual left, data right (or stacked for mobile friendliness)
    # Let's do stacked for clarity as requested
    
    # 2. Short Summary
    st.subheader("2. Short Summary")
    st.markdown(f"""
    <div class="summary-box">
        {st.session_state['summary'].replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("View Full Extracted Data"):
        st.json(st.session_state['extracted_data'])

    # --- SECTION 3: QA ---
    st.markdown("---")
    st.subheader("3. Ask Questions")
    
    # Suggest Questions
    data = st.session_state['extracted_data']
    suggestions = []
    if data.get('amount'): suggestions.append("What is the total amount?")
    if data.get('date'): suggestions.append("When is the date?")
    if data.get('name'): suggestions.append("Who is the customer?")
    suggestions.append("Summarize this document.")
    
    st.markdown("**Suggested Questions:**")
    
    # Grid for suggestions
    cols = st.columns(len(suggestions))
    for i, q in enumerate(suggestions):
        if cols[i].button(q, key=f"sugg_{i}"):
            st.session_state['current_question'] = q
    
    # Input
    user_q = st.text_input("Or type your own question:", value=st.session_state.get('current_question', ''))
    
    if user_q:
        qa = QAEcosystem()
        # Answer
        ans = qa.answer_question(user_q, st.session_state['raw_text'], st.session_state['extracted_data'])
        st.info(f"**Answer:** {ans}")

# --- Footer ---
st.markdown("---")
st.caption("Intelligent Form Agent v1.0 | Local Processing | No Data Sent to Cloud")
