# src/__init__.py

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

from .preprocessing import preprocess_text, analyze_term_patterns, named_entity_recognition
from .feature_engineering import extract_features
from .model import build_model, save_model, load_model, evaluate_model
from .training import train_model
from .deployment import deploy_model

# Import patterns
from .patterns import patterns

# Define what gets imported when 'from src import *' is used
__all__ = [
    'fetch_filing_history', 'extract_def14a_urls', 'download_and_save_filing',
    'preprocess_text', 'analyze_term_patterns', 'named_entity_recognition', 'extract_features',
    'build_model', 'save_model', 'load_model', 'evaluate_model',
    'train_model', 'deploy_model', 'patterns',
    'load_raw_data', 'load_processed_data', 'save_processed_data', 'load_config'
]
