import os
import logging
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, f1_score
from sklearn.model_selection import train_test_split
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

from .feature_engineering import preprocess_text
from .patterns import patterns

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_data(processed_data_path, feature_col='text', label_col='label'):
    if not os.path.exists(processed_data_path):
        logging.error(f"Processed data file not found at {processed_data_path}")
        return None, None

    data = pd.read_csv(processed_data_path)
    if feature_col not in data.columns or label_col not in data.columns:
        logging.error(f"Columns '{feature_col}' or '{label_col}' not found in data.")
        return None, None

    X = data[feature_col]
    y = data[label_col]
    return X, y

def load_model(model_path):
    if not os.path.exists(model_path):
        logging.error(f"Model file not found at {model_path}")
        return None

    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None

def evaluate_model(model, X_test, y_test):
    if model is None or X_test is None or y_test is None:
        logging.error("Invalid model or test data.")
        return

    try:
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
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

        plot_confusion_matrix(confusion, 'confusion_matrix.png')

        return {
            'accuracy': accuracy,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'classification_report': report,
            'confusion_matrix': confusion
        }
    except Exception as e:
        logging.error(f"Error during model evaluation: {e}")

def plot_confusion_matrix(conf_matrix, output_path):
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig(output_path)
    plt.close()
    logging.info(f"Confusion matrix plot saved to {output_path}")
