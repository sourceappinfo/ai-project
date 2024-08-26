# src/feature_engineering.py

import logging
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from patterns import get_pattern_terms

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prepare_data_for_modeling(processed_data_path, text_column='text', label_column='label'):
    """
    Prepare data for machine learning modeling. This includes loading the data,
    splitting it into training and testing sets, and vectorizing the text data.
    """
    logging.info(f"Loading processed data from {processed_data_path}")
    data = pd.read_csv(processed_data_path)

    if text_column not in data.columns or label_column not in data.columns:
        logging.error(f"Columns '{text_column}' or '{label_column}' not found in data.")
        return None, None, None, None

    # Extract features and labels
    X = data[text_column]
    y = data[label_column]

    # Split the data into training and testing sets
    logging.info("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logging.info("Data preparation complete.")

    return X_train, X_test, y_train, y_test

def vectorize_text_data(X_train, X_test):
    """
    Vectorize text data using TF-IDF vectorization.
    """
    logging.info("Vectorizing text data using TF-IDF...")
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    logging.info("Text vectorization complete.")
    
    return X_train_vec, X_test_vec, vectorizer

if __name__ == "__main__":
    # Example usage
    processed_data_path = 'data/processed/sec_filings_processed.csv'  # Update path as needed
    X_train, X_test, y_train, y_test = prepare_data_for_modeling(processed_data_path)
    if X_train is not None and X_test is not None:
        X_train_vec, X_test_vec, vectorizer = vectorize_text_data(X_train, X_test)

