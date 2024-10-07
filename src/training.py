import yaml
import logging
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from .feature_engineering import prepare_data_for_modeling  # Correct import

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_config(config_path='config/config.yaml'):
    """
    Load the configuration file.
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logging.info(f"Configuration loaded successfully from {config_path}")
        return config
    except Exception as e:
        logging.error(f"Error loading configuration from {config_path}: {e}")
        return None

def train_model(X_train, y_train):
    """
    Train the machine learning model.
    """
    try:
        # Create a text classification pipeline
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.7)),
            ('clf', MultinomialNB())
        ])

        logging.info("Training the model...")
        pipeline.fit(X_train, y_train)

        return pipeline
    except Exception as e:
        logging.error(f"Error during model training: {e}")
        return None

def save_model(model, model_output_path):
    """
    Save the trained model to a file.
    """
    try:
        joblib.dump(model, model_output_path)
        logging.info(f"Model saved to {model_output_path}")
    except Exception as e:
        logging.error(f"Error saving model to {model_output_path}: {e}")

def main():
    # Load the YAML configuration
    config = load_config()

    if config is None:
        logging.error("Configuration not loaded. Exiting program.")
        return

    processed_data_path = config['data']['processed_data_path']
    model_output_path = config['model']['output_path']

    # Prepare data for modeling
    X_train, X_test, y_train, y_test = prepare_data_for_modeling(processed_data_path)

    if X_train is None or y_train is None:
        logging.error("Data preparation failed. Exiting.")
        return

    # Train the model
    model = train_model(X_train, y_train)

    if model is None:
        logging.error("Model training failed. Exiting.")
        return

    # Evaluate the model
    logging.info("Evaluating the model...")
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(report)

    # Save the trained model
    save_model(model, model_output_path)

if __name__ == "__main__":
    main()
