# src/deployment.py

import os
import joblib
import logging
from sklearn.pipeline import Pipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_model(model, output_path):
    """
    Save the trained model to a specified output path.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        joblib.dump(model, output_path)
        logging.info(f"Model saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving model to {output_path}: {e}")

def load_model(model_path):
    """
    Load a trained model from a specified file path.
    """
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
    """
    Deploy the trained model by saving it to disk and preparing it for inference.
    """
    # Save the model
    save_model(model, model_path)

    # Example of additional deployment steps, such as setting up a server or API
    # This part will be custom depending on the deployment strategy (e.g., FastAPI, Flask, etc.)
    logging.info("Model deployment steps can be added here.")

if __name__ == "__main__":
    # Example usage
    model_path = 'models/sec_filing_classifier.pkl'  # Update path as needed

    # Load a trained model (Replace with actual model loading or training code)
    model = load_model(model_path)

    # If model is loaded successfully, deploy it
    if model:
        deploy_model(model, model_path)

