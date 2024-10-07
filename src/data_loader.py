import os
import pandas as pd
import logging
import yaml
import requests
from bs4 import BeautifulSoup

# Configure logging
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)  # Set debug level for detailed logging

def load_config(config_path='config/config.yaml'):
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration from {config_path}: {e}")
        return None

def fetch_filing_history(cik):
    """Fetch filing history for a given CIK using the SEC JSON endpoint."""
    logger.debug(f"Fetching filing history for CIK: {cik}")
    headers = {'User-Agent': 'SourceAppINC/1.0 (source.app.info@gmail.com)'}
    url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors
        logger.info(f"Filing history fetched for CIK: {cik}")
        return response.json()  # Return JSON content
    except requests.RequestException as e:
        logger.error(f"Error fetching filing history for CIK {cik}: {e}")
        return None

def extract_def14a_urls(filing_history):
    """Extract DEF 14A URLs from the JSON filing history."""
    def14a_urls = []
    if filing_history and 'filings' in filing_history and 'recent' in filing_history['filings']:
        recent_filings = filing_history['filings']['recent']
        for form_type, accession_number, primary_document in zip(recent_filings['form'], recent_filings['accessionNumber'], recent_filings['primaryDocument']):
            if form_type == 'DEF 14A':
                filing_url = f"https://www.sec.gov/Archives/edgar/data/{filing_history['cik']}/{accession_number.replace('-', '')}/{primary_document}"
                def14a_urls.append(filing_url)
    else:
        logger.warning("No recent filings found in filing history.")
    return def14a_urls

def download_and_save_filing(cik, url, raw_data_dir):
    """Download and save a single DEF 14A filing for a given CIK."""
    headers = {'User-Agent': 'SourceAppINC/1.0 (source.app.info@gmail.com)'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        filing_text = soup.get_text(separator=' ', strip=True)

        if not filing_text:
            logger.error(f"Empty content for filing URL: {url}")
            return

        # Save the text to a file
        filing_name = url.split('/')[-1].replace('.txt', '')  # Name the file by the document name
        save_path = os.path.join(raw_data_dir, f"{cik}_{filing_name}.txt")
        os.makedirs(raw_data_dir, exist_ok=True)  # Ensure the directory exists
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(filing_text)

        logger.info(f"Saved filing for CIK {cik} from {url}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading filing from URL {url}: {e}")

def load_raw_data(raw_data_dir):
    """Load raw text data from saved SEC filings in the raw data directory."""
    logger.info(f"Loading raw data from {raw_data_dir}")
    filings = []
    
    if os.path.exists(raw_data_dir):
        for filename in os.listdir(raw_data_dir):
            if filename.endswith(".txt"):
                try:
                    with open(os.path.join(raw_data_dir, filename), 'r', encoding='utf-8') as file:
                        filing_text = file.read()
                        filings.append({'filename': filename, 'text': filing_text})
                except Exception as e:
                    logger.error(f"Error reading file {filename}: {e}")
        logger.info(f"Loaded {len(filings)} filings from {raw_data_dir}")
        return pd.DataFrame(filings)
    else:
        logger.error(f"Raw data directory {raw_data_dir} does not exist.")
        return pd.DataFrame()

def load_processed_data(file_path):
    """Load processed data from a CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        logger.error(f"File is empty: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        return None

def save_processed_data(processed_data, processed_data_path):
    """Save processed data to a CSV file."""
    try:
        os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
        processed_data.to_csv(processed_data_path, index=False)
        logger.info(f"Processed data saved to {processed_data_path}")
    except Exception as e:
        logger.error(f"Error saving processed data to {processed_data_path}: {e}")

def main():
    """Main function to orchestrate the download and CSV creation process."""
    config_path = os.path.join('config', 'config.yaml')
    config = load_config(config_path)
    
    if config is None:
        logger.error("Configuration not loaded. Exiting.")
        return

    raw_data_dir = config['data']['raw_data_dir']
    processed_data_path = config['data']['processed_data_path']
    ciks = config['sec']['cik_list']

    extracted_data = []  # List to hold extracted data for CSV

    for cik in ciks:
        logger.info(f"Fetching data for CIK: {cik}")
        filing_history = fetch_filing_history(cik)
        if filing_history:
            def14a_urls = extract_def14a_urls(filing_history)
            if def14a_urls:
                for url in def14a_urls:
                    download_and_save_filing(cik, url, raw_data_dir)
                    extracted_data.append({
                        'CIK': cik,
                        'URL': url
                    })
            else:
                logger.info(f"No DEF 14A filings found for CIK {cik}.")
        else:
            logger.info(f"Failed to retrieve filing history for CIK {cik}.")

    # Convert the extracted data to a DataFrame and save to CSV
    filings_df = pd.DataFrame
