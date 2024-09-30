import PyPDF2
import docx
import logging
import pickle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("extractors.log"),  # Log to a file
        logging.StreamHandler()                  # Log to console
    ]
)

def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        logging.info("Successfully extracted text from PDF.")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(docx_file):
    try:
        doc = docx.Document(docx_file)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'  # Preserve paragraph breaks
        logging.info("Successfully extracted text from DOCX.")
        return text
    except Exception as e:
        logging.error(f"Error extracting text from DOCX: {e}")
        return ""

def save_extracted_text(text, filename):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(text, f)
        logging.info(f"Extracted text saved to {filename}.")
    except Exception as e:
        logging.error(f"Error saving extracted text to {filename}: {e}")

def load_extracted_text(filename):
    try:
        with open(filename, 'rb') as f:
            text = pickle.load(f)
        logging.info(f"Extracted text loaded from {filename}.")
        return text
    except Exception as e:
        logging.error(f"Error loading extracted text from {filename}: {e}")
        return ""
