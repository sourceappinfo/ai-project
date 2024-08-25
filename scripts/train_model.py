import yaml
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Load the YAML configuration
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    processed_data_path = config['data']['processed_data_path']
    model_output_path = config['model']['output_path']

    # Load the processed data
    logging.info(f"Loading processed data from {processed_data_path}")
    data = pd.read_csv(processed_data_path)

    # Assuming 'text' is the column with the filing text and 'label' is the target variable
    X = data['text']
    y = data['label']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a text classification pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.7)),
        ('clf', MultinomialNB())
    ])

    # Train the model
    logging.info("Training the model...")
    pipeline.fit(X_train, y_train)

    # Evaluate the model
    logging.info("Evaluating the model...")
    y_pred = pipeline.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(report)

    # Save the trained model
    joblib.dump(pipeline, model_output_path)
    logging.info(f"Model saved to {model_output_path}")

if __name__ == "__main__":
    main()

