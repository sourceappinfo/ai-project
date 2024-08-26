import requests
import yaml
import os
import logging
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from retrying import retry  # You might need to install this package using pip
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def fetch_filing_history(cik):
    """Fetch filing history for a given CIK from the SEC."""
    headers = {'User-Agent': 'SourceAppINC/1.0 (source.app.info@gmail.com)'}
    url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching filing history for CIK {cik}: {e}")
        raise  # Re-raise exception to trigger retry

def extract_def14a_urls(filing_history):
    """Extract DEF 14A URLs from the filing history."""
    def14a_urls = []
    if filing_history and 'filings' in filing_history and 'recent' in filing_history['filings']:
        recent_filings = filing_history['filings']['recent']
        for form_type, accession_number, primary_document in zip(recent_filings['form'], recent_filings['accessionNumber'], recent_filings['primaryDocument']):
            if form_type == 'DEF 14A':
                filing_url = f"https://www.sec.gov/Archives/edgar/data/{filing_history['cik']}/{accession_number.replace('-', '')}/{primary_document}"
                def14a_urls.append(filing_url)
    else:
        logging.warning(f"No recent filings found in filing history.")
    return def14a_urls

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def download_and_save_filing(cik, url, raw_data_dir):
    """Download and save a single DEF 14A filing for a given CIK."""
    headers = {'User-Agent': 'SourceAppINC/1.0 (source.app.info@gmail.com)'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        filing_text = soup.get_text(separator=' ', strip=True)

        if not filing_text:
            logging.error(f"Empty content for filing URL: {url}")
            return

        # Save the text to a file
        filing_name = url.split('/')[-1].replace('.txt', '')  # Name the file by the document name
        save_path = os.path.join(raw_data_dir, f"{cik}_{filing_name}.txt")
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(filing_text)

        logging.info(f"Saved filing for CIK {cik} from {url}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading filing from URL {url}: {e}")
        raise  # Re-raise exception to trigger retry

def main():
    """Main function to orchestrate the download process."""
    config_path = os.path.join('config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    raw_data_dir = config['data']['raw_data_dir']
    ciks = config['sec']['cik_list']

    # Ensure the raw data directory exists
    os.makedirs(raw_data_dir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust number of workers as needed
        future_to_url = {}
        
        for cik in ciks:
            logging.info(f"Fetching data for CIK: {cik}")
            filing_history = fetch_filing_history(cik)
            if filing_history:
                def14a_urls = extract_def14a_urls(filing_history)
                if def14a_urls:
                    for url in def14a_urls:
                        future = executor.submit(download_and_save_filing, cik, url, raw_data_dir)
                        future_to_url[future] = url
                else:
                    logging.info(f"No DEF 14A filings found for CIK {cik}.")
            else:
                logging.info(f"Failed to retrieve filing history for CIK {cik}.")

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error processing URL {url}: {e}")

if __name__ == "__main__":
    main()

