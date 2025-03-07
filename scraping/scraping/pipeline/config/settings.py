"""
Configuration settings for the research data extraction pipeline.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Browser settings
HEADLESS = True
PAGE_LOAD_TIMEOUT = 30
USER_AGENT_ENABLED = True

# Crawling settings
SCROLL_PAUSE_TIME = 1.5
RANDOM_DELAY_MIN = 7
RANDOM_DELAY_MAX = 25

# Journals to scrape
JOURNALS = [
    'Nature', 'Science', 'Cell', 'Immunity', 'Circulation', 
    'Gastroenterology', 'Gut', 'Neuro-Oncology', 'Cancer Cell', 'Cell Metabolism', 
    'Nature Immunology', 'Nature Biotechnology', 'Nature Medicine', 'Nature Genetics', 
    'Nature Neuroscience', 'Nature Cancer', 'Nature Methods', 'Nature Metabolism', 
    'Nature Microbiology', 'Nature Nanotechnology', 'Science Immunology', 'Science Bulletin', 
    'Cancer Discovery', 'Cell Research', 'Bioactive materials', 'Molecular Cancer', 
    'Molecular Neurodegeneration', 'Cell Stem Cell', 'Cell Host & Microbe', 'Nature cell biology',
    'Nature Biomedical Engineering', 'Cellular & Molecular Immunology', 'Lancet Microbe, The',
    'Lancet Oncology, The', 'Science Translational Medicine', 'Nucleic Acids Research',
    'National Science Review', 'Journal of Hepatology', 'Military Medical Research',
    'Lancet Infectious Diseases, The', 'Signal Transduction and Targeted Therapy', 'Annals of the Rheumatic Diseases',
    'Journal of Hematology & Oncology'
]

# JOURNALS = [
#     'Nature', 'Science', 'Cell'
# ]

# Batch size for journal processing
JOURNAL_BATCH_SIZE = 3

# Base URL for 10x Genomics publications with pagination support
BASE_URL_TEMPLATE = "https://www.10xgenomics.com/publications?sortBy=master%3Apublications-relevance&page=1&refinementList%5Bspecies%5D%5B0%5D=Human&refinementList%5Bspecies%5D%5B1%5D=Mouse"

# Keywords for data availability sections
DATA_KEYWORDS = [
    "Data and code availability",
    "Data and Code Availability",
    "DATA AND CODE AVAILABILITY",
    "Data and software availability",
    "Data and Software Availability",
    "Data and Materials Availability",
    "Data and materials availability",
    "Availability of data and materials",
    "Availability of Data and Materials",
    "Data availability statement",
    "Data Availability Statement",
    "Software availability",
    "Software Availability",
    "Data availability and accession codes",
    "Materials and data availability",
    "Data availability",
    "Data Availability",
    "DATA AVAILABILITY",
    "Code availability",
    "Code Availability",
    "CODE AVAILABILITY",
    "Accession codes",
    "Accession Codes",
    "Accession numbers",
    "Accession Numbers",
    "ACCESSION NUMBERS",
    "Data sharing",
    "Data Sharing",
    "Data deposition",
    "Data Deposition",
    "Data reporting",
    "Data Reporting",
    "Code available",
    "Code Available",
    "Data archive",
    "Data Archive",
    "Data access",
    "Data Access",
    "Independent data access",
    "Independent Data Access",
    "Data resources",
    "Data Resources"
]

# LLM settings
LLM_MODEL = "llama3.1:8b"  # Default model
LLM_TEMPERATURE = 0
LLM_MAX_RETRIES = 2
LLM_MAX_ITERATIONS = 15
LLM_MAX_EXECUTION_TIME = 60

# Evaluation metrics
EVALUATION_METRICS = [
    "execution_time",
    "accession_codes_count",
    "scripts_count",
    "analysis_data_count",
    "validation_score"
]