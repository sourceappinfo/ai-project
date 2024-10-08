# src/train_model.py

import yaml
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_config(config_path='config/config.yaml'):
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logging.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return None

def load_data(processed_data_path):
    """Load processed data from a CSV file."""
    logging.info(f"Loading processed data from {processed_data_path}")
    try:
        data = pd.read_csv(processed_data_path)
        return data
    except FileNotFoundError:
        logging.error(f"File not found: {processed_data_path}")
        return None
    except pd.errors.EmptyDataError:
        logging.error(f"File is empty: {processed_data_path}")
        return None
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

def train_model(X_train, y_train, config):
    """Train the model using a text classification pipeline."""
    max_df = config['nlp'].get('max_df', 0.7)  # Default to 0.7 if not set in config
    stop_words = config['nlp'].get('stopwords', 'english')

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words=stop_words, max_df=max_df)),
        ('clf', MultinomialNB())
    ])

    logging.info("Training the model...")
    pipeline.fit(X_train, y_train)
    return pipeline

def evaluate_model(pipeline, X_test, y_test):
    """Evaluate the model and print classification report."""
    logging.info("Evaluating the model...")
    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred, digits=4)
    logging.info("Model evaluation complete.")
    logging.info("\n" + report)
    return report

def save_model(pipeline, model_output_path):
    """Save the trained model to a file."""
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(pipeline, model_output_path)
    logging.info(f"Model saved to {model_output_path}")

def main():
    # Load the configuration
    config = load_config()
    if config is None:
        logging.error("Configuration loading failed. Exiting...")
        return

    processed_data_path = config['data']['processed_data_path']
    model_output_path = config['model']['output_path']

    # Load the processed data
    data = load_data(processed_data_path)
    if data is None:
        logging.error("Data loading failed. Exiting...")
        return

    # Check if required columns exist
    if 'text' not in data.columns or 'label' not in data.columns:
        logging.error("Required columns 'text' or 'label' not found in data.")
        return

    X = data['text']
    y = data['label']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    pipeline = train_model(X_train, y_train, config)

    # Evaluate the model
    report = evaluate_model(pipeline, X_test, y_test)

    # Save the trained model
    save_model(pipeline, model_output_path)

if __name__ == "__main__":
    main()
