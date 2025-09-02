# app.py - The Python Flask server for our NLP application.

# First, ensure you have the necessary libraries installed:
# pip install Flask flask-cors textblob spacy nrclex
# python -m spacy download en_core_web_sm

import spacy
from flask import Flask, request, jsonify
from textblob import TextBlob
from flask_cors import CORS
from collections import Counter
from string import punctuation
# New library for Emotion Analysis
from nrclex import NRCLex 
# For summarization
from heapq import nlargest
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the spaCy model for Named Entity Recognition and other NLP tasks
# 'en_core_web_sm' is a small English model that's efficient for web apps.
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("spaCy model loaded successfully")
except OSError:
    logger.info("Downloading spaCy model...")
    try:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
        logger.info("spaCy model downloaded and loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load spaCy model: {e}")
        nlp = None

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) to allow our frontend
# to communicate with this backend.
CORS(app)

@app.route("/")
def home():
    # A simple route to check if the server is running.
    return "NLP Server is running!"

@app.route("/health")
def health_check():
    """Health check endpoint to verify all dependencies are working"""
    status = {
        'status': 'healthy',
        'spacy_loaded': nlp is not None,
        'textblob_available': True,
        'nrclex_available': True
    }
    
    # Test TextBlob
    try:
        test_blob = TextBlob("test")
        status['textblob_working'] = True
    except Exception as e:
        status['textblob_working'] = False
        status['textblob_error'] = str(e)
    
    # Test NRCLex
    try:
        test_emotion = NRCLex("test")
        status['nrclex_working'] = True
    except Exception as e:
        status['nrclex_working'] = False
        status['nrclex_error'] = str(e)
    
    if not all([status['spacy_loaded'], status['textblob_working'], status['nrclex_working']]):
        status['status'] = 'unhealthy'
        return jsonify(status), 503
    
    return jsonify(status)

# Define the main endpoint for our NLP analysis
@app.route('/analyze', methods=['POST'])
def analyze_text():
    """
    This function receives text and performs:
    1. Sentiment Analysis
    2. Named Entity Recognition
    3. Emotion Analysis
    4. Text Summarization
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        if not text.strip():
            return jsonify({'error': 'Empty text provided'}), 400

        # Initialize response data
        response_data = {
            'sentiment': {'label': 'Unknown', 'score': 0.0},
            'entities': [],
            'emotions': {},
            'summary': '',
            'warnings': []
        }

        # --- 1. Sentiment Analysis using TextBlob ---
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0.1:
                sentiment = 'Positive'
            elif polarity < -0.1:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
            
            response_data['sentiment'] = {
                'label': sentiment,
                'score': polarity
            }
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            response_data['warnings'].append(f"Sentiment analysis failed: {str(e)}")

        # --- 2. Named Entity Recognition (NER) using spaCy ---
        if nlp is not None:
            try:
                doc = nlp(text)
                entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
                response_data['entities'] = entities
            except Exception as e:
                logger.error(f"NER failed: {e}")
                response_data['warnings'].append(f"Named Entity Recognition failed: {str(e)}")
        else:
            response_data['warnings'].append("spaCy model not available - NER disabled")

        # --- 3. Emotion Analysis using NRCLex ---
        try:
            emotion_object = NRCLex(text)
            emotions = emotion_object.raw_emotion_scores
            response_data['emotions'] = emotions
        except Exception as e:
            logger.error(f"Emotion analysis failed: {e}")
            response_data['warnings'].append(f"Emotion analysis failed: {str(e)}")

        # --- 4. Text Summarization using spaCy ---
        if nlp is not None:
            try:
                doc = nlp(text)
                # Get a list of stop words and punctuation
                stopwords = list(nlp.Defaults.stop_words)
                
                # Calculate word frequencies (ignoring stopwords and punctuation)
                word_frequencies = {}
                for word in doc:
                    if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                        if word.text not in word_frequencies.keys():
                            word_frequencies[word.text] = 1
                        else:
                            word_frequencies[word.text] += 1
                
                # Normalize frequencies
                max_frequency = max(word_frequencies.values()) if word_frequencies else 0
                for word in word_frequencies.keys():
                    if max_frequency > 0:
                        word_frequencies[word] = (word_frequencies[word]/max_frequency)

                # Score sentences based on word frequencies
                sentence_tokens = [sent for sent in doc.sents]
                sentence_scores = {}
                for sent in sentence_tokens:
                    for word in sent:
                        if word.text.lower() in word_frequencies.keys():
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word.text.lower()]
                            else:
                                sentence_scores[sent] += word_frequencies[word.text.lower()]

                # Get the top 30% of sentences as the summary
                select_length = int(len(sentence_tokens)*0.3)
                # Ensure we get at least one sentence
                select_length = max(select_length, 1) 

                summary_sentences = nlargest(select_length, sentence_scores, key=sentence_scores.get)
                summary = [word.text for word in summary_sentences]
                summary = " ".join(summary)
                
                response_data['summary'] = summary
            except Exception as e:
                logger.error(f"Summarization failed: {e}")
                response_data['warnings'].append(f"Text summarization failed: {str(e)}")
        else:
            response_data['warnings'].append("spaCy model not available - summarization disabled")

        # Remove warnings if empty
        if not response_data['warnings']:
            del response_data['warnings']

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Unexpected error in analyze_text: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# This allows you to run the app directly from the command line using "python app.py"
if __name__ == '__main__':
    # Running on port 5000 in debug mode for development.
    logger.info("Starting NLP Server on port 5000...")
    app.run(port=5000, debug=True)

