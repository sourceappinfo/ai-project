import requests
import logging
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import random
import pandas as pd

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

# Function to download and parse filing document
def download_and_parse_filing(url):
    headers = {'User-Agent': 'SourceAppINC/1.0 (source.app.info@gmail.com)'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading filing from URL {url}: {e}")
        return None

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

# Main function to fetch random companies' DEF 14A filings and analyze them
def main():
    # Example list of CIKs; in a real scenario, you'd fetch or generate these
    ciks = ['0000320193', '0000789019', '0001652044', '0001067983', '0001318605', '0001018724', '0001045810', '0001000180', 
            '0001551152', '0001090872', '0000732717', '0000200406', '0000021344', '0000078003', '0000066740', '0001108524', 
            '0001326801', '0000320187', '0000072971', '0000783280', '0000313616', '0000354950', '0000051143', '0000815556', 
            '0000877890', '0000092230', '0000740260', '0000050863', '0001467373']  # Example CIKs for testing
    random_ciks = random.sample(ciks, len(ciks))  # Randomly select 1000 or fewer CIKs if you have a larger list

    all_def14a_urls = {}

    for cik in random_ciks:
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
        # Expanded list of keywords and phrases for pattern recognition in SEC filings
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

    # Print term analysis results to the terminal
    print("\nTerm Analysis Results:")
    for cik, terms in term_analysis_results.items():
        print(f"\nCIK: {cik}")
        for term, count in terms.items():
            print(f"Term: {term}, Count: {count}")

    # Save results to a CSV file
    save_results_to_csv(term_analysis_results, 'data/processed/sec_filings_processed.csv')

if __name__ == "__main__":
    main()

