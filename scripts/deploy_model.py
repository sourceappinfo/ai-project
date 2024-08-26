# src/deploy_model.py

import os
import pickle
import logging
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Load configuration
config_path = os.path.join('config', 'config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

model_path = config['model']['output_path']
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

    except Exception as e:
        logging.error(f"Error loading model or vectorizer: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to make predictions."""
    if not model or not vectorizer:
        return jsonify({'error': 'Model or vectorizer not loaded'}), 500

    try:
        data = request.get_json()
        if 'text' not in data:
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

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({'error': 'Error during prediction'}), 500

if __name__ == '__main__':
    load_model_and_vectorizer()
    app.run(host='0.0.0.0', port=5000)

