import logging
import pickle
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import BartTokenizer, BartForConditionalGeneration


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("summarizer.log"),  # Log to a file
        logging.StreamHandler()                   # Log to console
    ]
)


# Load the BART model and tokenizer from Hugging Face
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

class TextSummarizer:
    def __init__(self, model_name='t5-base'):
        try:
            # Load pre-trained T5 model and tokenizer
            self.model = T5ForConditionalGeneration.from_pretrained(model_name)
            self.tokenizer = T5Tokenizer.from_pretrained(model_name)
            logging.info("Model and tokenizer loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading model or tokenizer: {e}")
            raise

    def summarize_text(self, text, max_length=300):
        try:
            # Tokenize the input text
            inputs = self.tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
            
            # Generate the summary
            summary_ids = self.model.generate(
                inputs,
                max_length=max_length,
                min_length=30,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )
            
            # Decode the summary to human-readable text
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            logging.info("Summary generated successfully.")
            return summary
        except Exception as e:
            logging.error(f"Error generating summary: {e}")
            return ""

    def save_model(self, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump((self.model.state_dict(), self.tokenizer), f)
            logging.info(f"Model saved to {filename}.")
        except Exception as e:
            logging.error(f"Error saving model to {filename}: {e}")

    def load_model(self, filename):
        try:
            with open(filename, 'rb') as f:
                state_dict, tokenizer = pickle.load(f)
                self.model.load_state_dict(state_dict)
                self.tokenizer = tokenizer
            logging.info(f"Model loaded from {filename}.")
        except Exception as e:
            logging.error(f"Error loading model from {filename}: {e}")
