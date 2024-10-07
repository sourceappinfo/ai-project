import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
# Import necessary modules and functions for easy access when the package is imported
from .data_loader import (
    fetch_filing_history, 
    extract_def14a_urls, 
    download_and_save_filing, 
    load_raw_data, 
    load_processed_data, 
    save_processed_data, 
    load_config
)
from .preprocessing import preprocess_text, analyze_term_patterns
from .feature_engineering import extract_features
from .model import build_model, save_model, load_model, evaluate_model
from .training import train_model
from .deployment import deploy_model

# Import patterns
from .patterns import patterns

# Optional: You can define what gets imported when 'from your_package_name import *' is used
__all__ = [
    'fetch_filing_history', 'extract_def14a_urls', 'download_and_save_filing',
    'preprocess_text', 'analyze_term_patterns', 'extract_features',
    'build_model', 'save_model', 'load_model', 'evaluate_model',
    'train_model', 'deploy_model', 'patterns',
    'load_raw_data', 'load_processed_data', 'save_processed_data', 'load_config'
]
