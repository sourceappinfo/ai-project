import os
import joblib
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from .feature_engineering import prepare_data_for_modeling

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def build_model():
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    logging.info("RandomForest model created.")
    return model

def save_model(model, model_path):
    try:
        with open(model_path, 'wb') as file:
            joblib.dump(model, file)
        logging.info(f"Model saved at {model_path}")
    except Exception as e:
        logging.error(f"Error saving model: {e}")

def load_model(model_path):
    if not os.path.exists(model_path):
        logging.error(f"Model file not found at {model_path}")
        return None
    try:
        with open(model_path, 'rb') as file:
            model = joblib.load(file)
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None

def evaluate_model(model, X_test, y_test):
    try:
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f"
