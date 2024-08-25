import requests
import yaml
import os
import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch filing history for a given CIK
def fetch_filing_history(cik):
    headers = {'User-Agent': 'SourceAppINC/1.0 (source.app.info@gmail.com)'}
    url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching filing history for CIK {cik}: {e}")
        return None

# Function to extract DEF 14A URLs from filing history
def extract_def14a_urls(filing_history):
    def14a_urls = []
    if 'filings' in filing_history and 'recent' in filing_history['filings']:
        recent_filings = filing_history['filings']['recent']
        for form_type, accession_number, primary_document in zip(recent_filings['form'], recent_filings['accessionNumber'], recent_filings['primaryDocument']):
            if form_type == 'DEF 14A':
                filing_url = f"https://www.sec.gov/Archives/edgar/data/{filing_history['cik']}/{accession_number.replace('-', '')}/{primary_document}"
                def14a_urls.append(filing_url)
    return def14a_urls

# Function to download and save filing documents
def download_and_save_filings(cik, urls, raw_data_dir):
    headers = {'User-Agent': 'SourceAppINC/1.0 (source.app.info@gmail.com)'}
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            filing_text = soup.get_text(separator=' ', strip=True)

            # Save the text to a file
            filing_name = url.split('/')[-1].replace('.txt', '')  # Name the file by the document name
            save_path = os.path.join(raw_data_dir, f"{cik}_{filing_name}.txt")
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(filing_text)

            logging.info(f"Saved filing for CIK {cik} from {url}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error downloading filing from URL {url}: {e}")

def main():
    # Load the YAML configuration
    config_path = os.path.join('config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    raw_data_dir = config['data']['raw_data_dir']
    ciks = config['sec']['cik_list']

    # Ensure the raw data directory exists
    os.makedirs(raw_data_dir, exist_ok=True)

    # Fetch and save filings for each CIK
    for cik in ciks:
        logging.info(f"Fetching data for CIK: {cik}")
        filing_history = fetch_filing_history(cik)
        if filing_history:
            def14a_urls = extract_def14a_urls(filing_history)
            if def14a_urls:
                download_and_save_filings(cik, def14a_urls, raw_data_dir)
            else:
                logging.info(f"No DEF 14A filings found for CIK {cik}.")

if __name__ == "__main__":
    main()

