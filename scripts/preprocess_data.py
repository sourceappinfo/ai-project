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
        
    # Join tokens back into a single string
    preprocessed_text = ' '.join(tokens)
        
    return preprocessed_text

# Function to download and parse filing document
def download_and_parse_filing(url):
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
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities
        
# Function to analyze text for term patterns using regular expressions
def analyze_term_patterns(text, patterns):
    term_counts = defaultdict(int)
    for pattern in patterns:
        regex = re.compile(pattern, re.IGNORECASE)  # Case insensitive search
        count = len(regex.findall(text))   
        term_counts[pattern] += count
    return term_counts
        
# Function to save analysis results to a CSV file using pandas
def save_results_to_csv(term_analysis_results, output_file):
    # Create a DataFrame with CIKs as rows and terms as columns
    df = pd.DataFrame(term_analysis_results).T.fillna(0).astype(int)
    df.index.name = 'CIK'
    df.to_csv(output_file)
    logging.info(f"Term analysis results have been saved to '{output_file}'.")
        
# Function to load configuration
def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
        
# Main function to fetch random companies' DEF 14A filings and analyze them
def main():
    # Load the YAML configuration
    config = load_config()
        
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
    
    # Expanded keywords or patterns to search for in filings
    patterns = [
        r"CEO Pay Ratio", r"CEO to Worker Pay Ratio", r"CEO Compensation Ratio", r"CEO Pay",
        r"CEO Compensation", r"Executive Pay", r"Executive Compensation", r"Pay Ratio", r"Pay Gap", r"Compensation",
        r"Base Salary", r"Long-Term Incentive Plan", r"Short-Term Incentive Plan", r"Stock-Based Compensation",
        r"Performance Metrics", r"Incentive Compensation", r"Deferred Compensation", r"Severance Agreement",
        r"Golden Parachute", r"Clawback Policy", r"Equity Compensation", r"Bonus Plan", r"Compensation Consultant",
        r"Peer Group Analysis", r"Board Diversity", r"Diversity of the Board", r"Board Composition", r"Board Demographics",
        r"Gender Diversity", r"Ethnic Diversity", r"Board Gender Diversity", r"Board Ethnic Diversity",
        r"Board Members", r"Board Structure", r"Independent Directors", r"Board Independence",
        r"Board Tenure", r"Board Refreshment", r"Diversity", r"Inclusivity", r"Inclusion", r"Equity", r"LGBT",
        r"Minority", r"Equality", r"Equal Employment Opportunity", r"Inclusive Culture", r"Equity and Inclusion",
        r"Unconscious Bias", r"Diversity Metrics", r"Gender Pay Gap", r"Equal Pay", r"Affirmative Action",
        r"Minority Representation", r"Disability Inclusion", r"ESG Policies", r"Environmental, Social, and Governance",
        r"ESG", r"Climate",  r"Sustainability Practices", r"ESG Strategy", r"Sustainability Policies",
        r"Environmental Impact", r"Social Responsibility", r"ESG Initiatives", r"Sustainability Goals",
        r"ESG Disclosures", r"Corporate Social Responsibility", r"CSR", r"Sustainability", r"Green Initiatives",
        r"Climate Risk", r"Climate Change", r"Carbon Emissions", r"Carbon Footprint", r"Renewable Energy",
        r"Water Usage", r"Energy Efficiency", r"Waste Management", r"Recycling", r"Environmental Stewardship",
        r"Ethical Sourcing", r"Human Rights", r"Labor Practices", r"Net Zero Commitment", r"Carbon Neutral",
        r"Climate Adaptation", r"Environmental Goals", r"Social Justice", r"Greenhouse Gas Emissions",
        r"Renewable Resources", r"Water Conservation", r"Social Impact", r"Energy Transition", r"Environmental Policy",
        r"Sustainable Investment", r"Total Employees", r"Number of Employees", r"Total Workforce", r"Employee Count",
        r"Headcount", r"Total Headcount", r"Number of Full-Time Employees", r"Number of Part-Time Employees",
        r"Workforce Diversity", r"Employee Demographics", r"Employee Benefits", r"Employee Engagement",
        r"Employee Turnover", r"Employee Retention", r"Human Capital", r"Human Resources", r"HR Policies",
        r"Subsidiaries", r"List of Subsidiaries", r"Subsidiary Information", r"Subsidiary Companies",
        r"Controlled Entities", r"Subsidiary List", r"Entities under Control", r"Joint Ventures",
        r"Partnerships", r"Affiliated Companies", r"Business Units", r"Corporate Structure",
        r"Liquidity", r"Working Capital", r"Inventory", r"Accounts Receivable", r"Accounts Payable",
        r"Capital Expenditures", r"Depreciation", r"Amortization", r"Interest Expense", r"Tax Rate",
        r"Deferred Tax", r"Tax Liability", r"Goodwill", r"Intangible Assets", r"Financial Performance",
        r"Revenue", r"Net Income", r"EBITDA", r"Gross Margin", r"Operating Margin", r"Profitability", r"Income Statement", r"Balance Sheet",
        r"Cash Flow Statement", r"Cost of Goods Sold", r"Operating Income", r"Net Profit Margin",
        r"Financial Statement Analysis", r"Credit Rating", r"Debt Maturity", r"Shareholder Equity",
        r"Gross Profit", r"Revenue Recognition", r"Financial Highlights",

        # Risk Management and Market Conditions
        r"Risk Factors", r"Market Conditions", r"Industry Trends", r"Economic Environment",
        r"Competitive Landscape", r"Risk Management", r"Operational Risk", r"Financial Risk", r"Market Risk",
        r"Compliance Risk", r"Cybersecurity Risk", r"Regulatory Risk", r"Litigation Risk",
        r"Environmental Risk", r"Reputational Risk", r"Audit Fees", r"Internal Audit", r"Whistleblower Policy",
        r"Fraud Risk", r"Risk Oversight", r"Enterprise Risk Management", r"Credit Risk", r"Market Volatility",
        r"Interest Rate Risk", r"Liquidity Risk", r"Operational Audit",

        # Business
        # Business Strategy and Growth
        r"Growth Strategy", r"Expansion Plans", r"Market Share", r"Research and Development",
        r"Innovation", r"Product Development", r"Patents", r"Intellectual Property", r"Trademarks",
        r"Technology Investments", r"Digital Transformation", r"Product Launch", r"Strategic Initiatives",
        r"Corporate Strategy", r"Mergers and Acquisitions", r"M&A", r"Divestitures", r"Organic Growth",
        r"Strategic Partnerships", r"Joint Ventures", r"Business Alliances", r"Market Expansion",
        r"Brand Strategy", r"Digital Innovation", r"Business Development", r"Strategic Planning",
        r"Market Penetration", r"Customer Acquisition", r"Product Roadmap", r"Competitive Strategy",

        # Legal, Compliance, and Regulatory
        r"Litigation", r"Legal Proceedings", r"Compliance", r"Regulatory Environment", r"Taxation",
        r"Regulatory Compliance", r"Anti-Corruption", r"Anti-Bribery", r"Data Privacy", r"GDPR",
        r"CCPA", r"Legal Risks", r"Intellectual Property Rights", r"Patent Litigation",
        r"Regulatory Affairs", r"Government Relations", r"Sanctions Compliance", r"Legal Strategy",
        r"Litigation Management", r"Compliance Program", r"Compliance Training",

        # Governance and Reporting
        r"Accounting Policies", r"Auditors", r"Audit Report", r"Internal Controls", r"Disclosure Controls",
        r"Sarbanes-Oxley Act", r"SOX", r"SEC Filings", r"10-K", r"10-Q", r"8-K", r"Proxy Statement", r"Annual Report",
        r"Quarterly Report", r"Management's Discussion and Analysis", r"MD&A", r"Forward-Looking Statements",
        r"Safe Harbor", r"Shareholder Proposals", r"Investor Relations", r"Analyst Reports", r"Corporate Governance",
        r"Governance Structure", r"Audit Committee", r"Compensation Committee", r"Nominating Committee",
        r"Board Independence", r"Board Meetings", r"Governance Practices", r"Corporate Bylaws",
        r"Board Responsibilities", r"Conflict of Interest", r"Governance Code", r"Shareholder Rights",
        r"Voting Rights", r"Governance Policies",

        # Other Single Words and Phrases
        r"Diversity", r"Gender", r"Race", r"Ethnicity", r"Renewable", r"Inclusion", r"Equity", r"Governance",
        r"Sustainability", r"Ethics", r"Transparency", r"Accountability", r"Integrity", r"Compliance", r"Risk",
        r"Social", r"Social Impact", r"Impact", r"Responsibility", r"Corporate Responsibility",
        r"Corporate Social Responsibility", r"Strategy", r"Profit", r"Loss", r"Revenue", r"Expense", r"Assets",
        r"Liabilities", r"Debt", r"Equity", r"Capital", r"Market", r"Competition", r"Technology", r"Digital",
        r"Social", r"Environmental", r"Climate", r"Carbon", r"Water", r"Energy", r"Recycling", r"Community",
        r"Workforce", r"Employee", r"Board", r"Director", r"Executive", r"Shareholder", r"Investor", r"Stakeholder",
        r"Dividend", r"Voting", r"Proxy", r"Committee", r"Meeting", r"Resolution", r"Proposal", r"Policy",
        r"Standards", r"Guidelines", r"Regulation", r"Legislation"
    ]

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

