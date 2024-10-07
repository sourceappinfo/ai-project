import re
import logging
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from .patterns import patterns

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text)
    text = text.lower()
    logging.debug(f"Preprocessed text: {text}")
    return text

def extract_features(data, config):
    try:
        data['text'] = data['text'].apply(preprocess_text)
        vectorizer = CountVectorizer(max_features=config['nlp']['max_features'], 
                                     stop_words=config['nlp']['stopwords'], 
                                     min_df=config['nlp']['min_df'], 
                                     max_df=config['nlp']['max_df'])
        bag_of_words = vectorizer.fit_transform(data['text'])
        tfidf_transformer = TfidfTransformer()
        tfidf_matrix = tfidf_transformer.fit_transform(bag_of_words)
        logging.info("Feature extraction completed successfully.")
        return tfidf_matrix
    except Exception as e:
        logging.error(f"Error in feature extraction: {e}")
        return None

def prepare_data_for_modeling(data, target_column, test_size=0.2, random_state=42):
    try:
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        logging.info("Data preparation for modeling completed successfully.")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error(f"Error in preparing data for modeling: {e}")
        return None, None, None, None
