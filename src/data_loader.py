# src/data_loader.py

import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_raw_data(file_path):
    """
    Load raw data from a specified file path.
    """
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None

    try:
        data = pd.read_csv(file_path)
        logging.info(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {e}")
        return None

def save_processed_data(data, file_path):
    """
    Save processed data to a specified file path.
    """
    try:
        data.to_csv(file_path, index=False)
        logging.info(f"Processed data saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving data to {file_path}: {e}")

def load_config(config_path='config/config.yaml'):
    """
    Load configuration from a YAML file.
    """
    import yaml
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logging.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logging.error(f"Error loading configuration from {config_path}: {e}")
        return None

# Example usage
if __name__ == "__main__":
    config = load_config()
    if config:
        raw_data_path = config['data']['raw_data_path']
        processed_data_path = config['data']['processed_data_path']
        raw_data = load_raw_data(raw_data_path)
        if raw_data is not None:
            # Further processing or operations can be done here
            save_processed_data(raw_data, processed_data_path)

