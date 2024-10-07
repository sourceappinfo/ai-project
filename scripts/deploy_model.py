import os
import pickle
import logging
import yaml
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_path = os.path.join('config', 'config.yaml')
if not os.path.exists(config_path):
    logging.error(f"Configuration file not found at {config_path}")
    raise FileNotFoundError(f"Configuration file not found at {config_path}")

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

model_path = config.get('model', {}).get('output_path', 'models/sec_filing_classifier.pkl')
vectorizer_path = config.get('vectorizer_path', 'models/vectorizer.pkl')

# Load the trained model and vectorizer
model = None
vectorizer = None

def load_model_and_vectorizer():
    """Load the trained model and vectorizer."""
    global model, vectorizer
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        logging.info(f"Model loaded from {model_path}")

        with open(vectorizer_path, 'rb') as file:
            vectorizer = pickle.load(file)
        logging.info(f"Vectorizer loaded from {vectorizer_path}")

    except FileNotFoundError as e:
        logging.error(f"Model or vectorizer file not found: {e}")
        raise
    except Exception as e:
        logging.error(f"Error loading model or vectorizer: {e}")
        raise

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to make predictions."""
    if not model or not vectorizer:
        return jsonify({'error': 'Model or vectorizer not loaded properly'}), 500

    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text data provided'}), 400

        input_text = [data['text']]
        logging.info(f"Received input text for prediction: {input_text}")

        # Transform the input text using the vectorizer
        input_features = vectorizer.transform(input_text)

        # Make prediction
        prediction = model.predict(input_features)
        prediction_prob = model.predict_proba(input_features)[:, 1]

        response = {
            'prediction': int(prediction[0]),
            'prediction_probability': float(prediction_prob[0])
        }

        logging.info(f"Prediction response: {response}")
        return jsonify(response)

    except ValueError as e:
        logging.error(f"Value error during prediction: {e}")
        return jsonify({'error': 'Value error during prediction'}), 400
    except Exception as e:
        logging.error(f"Unexpected error during prediction: {e}")
        return jsonify({'error': 'Unexpected error during prediction'}), 500

if __name__ == '__main__':
    try:
        load_model_and_vectorizer()
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.critical(f"Failed to start the application: {e}")
