# src/training.py

import yaml
import logging
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from feature_engineering import prepare_data_for_modeling

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path='config/config.yaml'):
    """
    Load the configuration file.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def train_model(X_train, y_train):
    """
    Train the machine learning model.
    """
    # Create a text classification pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.7)),
        ('clf', MultinomialNB())
    ])

    logging.info("Training the model...")
    pipeline.fit(X_train, y_train)

    return pipeline

def save_model(model, model_output_path):
    """
    Save the trained model to a file.
    """
    joblib.dump(model, model_output_path)
    logging.info(f"Model saved to {model_output_path}")

def main():
    # Load the YAML configuration
    config = load_config()

    processed_data_path = config['data']['processed_data_path']
    model_output_path = config['model']['output_path']

    # Prepare data for modeling
    X_train, X_test, y_train, y_test = prepare_data_for_modeling(processed_data_path)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    logging.info("Evaluating the model...")
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(report)

    # Save the trained model
    save_model(model, model_output_path)

if __name__ == "__main__":
    main()

