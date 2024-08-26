# src/model.py

import os
import joblib
import logging
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, f1_score
from sklearn.model_selection import train_test_split
from data_loader import load_processed_data
from feature_engineering import prepare_data_for_modeling

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_model(model_path):
    """
    Load the trained machine learning model from a file.
    """
    if not os.path.exists(model_path):
        logging.error(f"Model file not found at {model_path}")
        return None

    logging.info(f"Loading model from {model_path}")
    try:
        with open(model_path, 'rb') as file:
            model = joblib.load(file)
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model using test data.
    """
    if model is None or X_test is None or y_test is None:
        logging.error("Invalid model or test data.")
        return

    logging.info("Evaluating the model...")

    try:
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]  # Probabilities for ROC-AUC

        # Calculate evaluation metrics
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        roc_auc = roc_auc_score(y_test, y_prob)
        report = classification_report(y_test, y_pred)
        confusion = confusion_matrix(y_test, y_pred)

        logging.info(f"Accuracy: {accuracy:.4f}")
        logging.info(f"F1 Score: {f1:.4f}")
        logging.info(f"ROC-AUC Score: {roc_auc:.4f}")
        logging.info("Classification Report:\n" + report)
        logging.info("Confusion Matrix:\n" + str(confusion))

        # Return the metrics
        return {
            'accuracy': accuracy,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'classification_report': report,
            'confusion_matrix': confusion
        }
    except Exception as e:
        logging.error(f"Error during model evaluation: {e}")

def main():
    # Load configuration
    config_path = os.path.join('config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    processed_data_path = config['data']['processed_data_path']
    model_path = config['model']['output_path']

    # Prepare data for modeling
    X_train, X_test, y_train, y_test = prepare_data_for_modeling(processed_data_path)

    # Load the trained model
    model = load_model(model_path)
    if model is None:
        logging.error("Failed to load model. Exiting.")
        return

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()

