import streamlit as st
from extractors import extract_text_from_pdf, extract_text_from_docx
from summarizer import TextSummarizer
import logging
import os

# Configure logging
log_file_path = os.path.join(os.path.dirname(__file__), "app.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),  # Log to a file
        logging.StreamHandler()               # Log to console
    ]
)
st.title("Generative AI for Document Summarization")

# Instantiate the TextSummarizer
summarizer = TextSummarizer()

uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    document_text = ""

    if uploaded_file.type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document_text = extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        document_text = uploaded_file.read().decode('utf-8')

    # Display the original document text
    st.subheader("Original Document")
    st.write(document_text)

    # Log the extracted text length for debugging
    logging.info(f"Extracted text length: {len(document_text)} characters")

    # Generate and display summary
    if document_text:
        try:
            summary = summarizer.summarize_text(document_text)  # Ensure the extracted text is passed
            st.subheader("Summarized Document")
            st.write(summary)
        except Exception as e:
            st.error("Error generating summary.")
            logging.error(f"Error in summarization: {e}")
    else:
        st.warning("No text was extracted from the document.")
