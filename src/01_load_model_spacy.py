import spacy
from transformers import pipeline

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

nlp.to_disk('save_model_nlp')
