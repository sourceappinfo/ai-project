import requests
import logging  
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
import yaml
import os

# Import patterns
from src.patterns import patterns

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load SpaCy model for Named Entity Recognition
nlp = spacy.load('en_core_web_sm')

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Function to clean and preprocess text
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
   Here are the rest of the edits and improvements for the **preprocessing.py** script:

```python
# src/preprocessing.py

import requests
import logging  
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
import yaml
import os

# Import patterns
from src.patterns import patterns

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load SpaCy model for Named Entity Recognition
nlp = spacy.load('en_core_web_sm')

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Function to clean and preprocess text
def preprocess_text(text):
    """
    Clean and preprocess the text data by converting it to lowercase,
    removing non-alphanumeric characters, and lemmatizing the tokens.
    """
    try:
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
        preprocessed_text = ' '.join(tokens)
        return preprocessed_text
    except Exception as e:
        logging.error(f"Error during text preprocessing: {e}")
        return None

# Function to download and parse filing document
def download_and_parse_filing(url):
    """
    Download the filing document from the given URL and preprocess it.
    """
    headers = {'User-Agent': 'SourceAppINC/1.0 (source.app.info@gmail.com)'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        raw_text = soup.get_text(separator=' ', strip=True)
        return preprocess_text(raw_text)  # Preprocess the text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading filing from URL {url}: {e}")
        return None

# Function to perform Named Entity Recognition (NER)
def named_entity_recognition(text):
    """
    Perform Named Entity Recognition (NER) using the SpaCy model.
    """
    try:
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities
    except Exception as e:
        logging.error(f"Error during Named Entity Recognition: {e}")
        return []

# Function to analyze text for term patterns using regular expressions
def analyze_term_patterns(text, patterns):
    """
    Analyze text for term patterns using regular expressions.
    """
    try:
        term_counts = defaultdict(int)
        for pattern in patterns:
            regex = re.compile(pattern, re.IGNORECASE)  # Case insensitive search
            count = len(regex.findall(text))   
            term_counts[pattern] += count
        return term_counts
    except Exception as e:
        logging.error(f"Error during pattern analysis: {e}")
        return defaultdict(int)

# Function to save analysis results to a CSV file using pandas
def save_results_to_csv(term_analysis_results, output_file):
    """
    Save the analysis results to a CSV file using pandas.
    """
    try:
        df = pd.DataFrame(term_analysis_results).T.fillna(0).astype(int)
        df.index.name = 'CIK'
        df.to_csv(output_file)
        logging.info(f"Term analysis results have been saved to '{output_file}'.")
    except Exception as e:
        logging.error(f"Error saving results to CSV: {e}")

# Function to load configuration
def load_config(config_path='config/config.yaml'):
    """
    Load the YAML configuration file.
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return None

# Main function to fetch random companies' DEF 14A filings and analyze them
def main():
    # Load the YAML configuration
    config = load_config()
    if not config:
        logging.error("Failed to load configuration. Exiting.")
        return
    
    processed_data_path = config['data']['processed_data_path']
    ciks = config['sec']['cik_list']

    all_def14a_urls = {}
    
    for cik in ciks:
        logging.info(f"Processing CIK: {cik}")
        filing_history = fetch_filing_history(cik)
        if filing_history:
            def14a_urls = extract_def14a_urls(filing_history)
            if def14a_urls:
                all_def14a_urls[cik] = def14a_urls
                logging.info(f"Found {len(def14a_urls)} DEF 14A filings for CIK {cik}.")
            else:
                logging.info(f"No DEF 14A filings found for CIK {cik}.")
    
    logging.info("DEF 14A URLs extraction completed.")

    # Analyze term patterns in all collected filings
    term_analysis_results = defaultdict(lambda: defaultdict(int))

    for cik, urls in all_def14a_urls.items():
        for url in urls:
            text = download_and_parse_filing(url)
            if text:
                term_counts = analyze_term_patterns(text, patterns)
                for term, count in term_counts.items():
                    term_analysis_results[cik][term] += count

                # Perform Named Entity Recognition (NER)
                entities = named_entity_recognition(text)
                logging.info(f"Named Entities for CIK {cik}: {entities}")

    # Print term analysis results to the terminal
    print("\nTerm Analysis Results:")
    for cik, terms in term_analysis_results.items():
        print(f"\nCIK: {cik}")
        for term, count in terms.items():
            print(f"Term: {term}, Count: {count}")

    # Save results to a CSV file
    save_results_to_csv(term_analysis_results, processed_data_path)

if __name__ == "__main__":
    main()
