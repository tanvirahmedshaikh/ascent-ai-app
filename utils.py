import streamlit as st
from pypdf import PdfReader
import io

def process_uploaded_files(uploaded_files):
    """Reads text from uploaded files (PDF, TXT, MD) and combines them."""
    combined_text = ""
    if uploaded_files:
        for file in uploaded_files:
            try:
                if file.type == "application/pdf":
                    pdf_reader = PdfReader(io.BytesIO(file.getvalue()))
                    for page in pdf_reader.pages:
                        combined_text += page.extract_text() + "\n\n"
                else:  # Assumes .txt, .md, etc.
                    combined_text += file.getvalue().decode("utf-8") + "\n\n"
            except Exception as e:
                st.error(f"Error processing file {file.name}: {e}")
    return combined_text