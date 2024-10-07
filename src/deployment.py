import os
import joblib
import logging
from sklearn.pipeline import Pipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def save_model(model, output_path):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        joblib.dump(model, output_path)
        logging.info(f"Model saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving model to {output_path}: {e}")

def load_model(model_path):
    if not os.path.exists(model_path):
        logging.error(f"Model file not found at {model_path}")
        return None

    try:
        model = joblib.load(model_path)
        logging.info(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        logging.error(f"Error loading model from {model_path}: {e}")
        return None

def deploy_model(model, model_path):
    save_model(model, model_path)
    logging.info("Model deployed and saved to disk.")
