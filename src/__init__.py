# src/__init__.py

# Import necessary modules and functions for easy access when the package is imported
from .data_loader import fetch_filing_history, extract_def14a_urls, download_and_save_filings
from .preprocessing import preprocess_text, analyze_term_patterns
from .feature_engineering import extract_features
from .model import build_model, save_model, load_model
from .training import train_model
from .evaluation import evaluate_model
from .deployment import deploy_model

# Optional: You can define what gets imported when 'from your_package_name import *' is used
__all__ = [
    'fetch_filing_history', 'extract_def14a_urls', 'download_and_save_filings',
    'preprocess_text', 'analyze_term_patterns', 'extract_features',
    'build_model', 'save_model', 'load_model',
    'train_model', 'evaluate_model', 'deploy_model'
]

# You can also include any package-level variables or configuration here if needed

