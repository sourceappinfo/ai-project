import os
import pickle
import logging
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, f1_score
from sklearn.model_selection import train_test_split
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_data(processed_data_path, feature_col='text', label_col='label'):
    """Load the processed data for evaluation."""
    if not os.path.exists(processed_data_path):
        logging.error(f"Processed data file not found at {processed_data_path}")
        return None, None

    logging.info(f"Loading processed data from {processed_data_path}")
    data = pd.read_csv(processed_data_path)

    if feature_col not in data.columns or label_col not in data.columns:
        logging.error(f"Columns '{feature_col}' or '{label_col}' not found in data.")
        return None, None

    X = data[feature_col]
    y = data[label_col]

    return X, y

def load_model(model_path):
    """Load the trained machine learning model from a file."""
    if not os.path.exists(model_path):
        logging.error(f"Model file not found at {model_path}")
        return None

    logging.info(f"Loading model from {model_path}")
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None

def evaluate_model(model, X_test, y_test):
    """Evaluate the model using test data."""
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
    """Main function for evaluating the model."""
    config_path = os.path.join('config', 'config.yaml')
    if not os.path.exists(config_path):
        logging.error(f"Configuration file not found at {config_path}")
        return

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    processed_data_path = config['data']['processed_data_path']
    model_path = config['model']['output_path']

    # Load data
    X, y = load_data(processed_data_path)
    if X is None or y is None:
        logging.error("Failed to load data. Exiting.")
        return

    # Split data into training and testing sets (if not already split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Load the trained model
    model = load_model(model_path)
    if model is None:
        logging.error("Failed to load model. Exiting.")
        return

    # Evaluate the model
    evaluation_results = evaluate_model(model, X_test, y_test)
    if evaluation_results:
        evaluation_results_path = 'evaluation_results.txt'
        with open(evaluation_results_path, 'w') as f:
            for key, value in evaluation_results.items():
                f.write(f"{key}: {value}\n")

if __name__ == "__main__":
    main()
