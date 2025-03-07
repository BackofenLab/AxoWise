"""
Data Section Extraction Module

This module handles the extraction of data availability sections from publications.
Updated to work with the new main.py parallel processing framework.
"""

import os
import time
import random
import re
import tempfile
import concurrent.futures
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import threading
import json

# Import utilities
from utils.browser import setup_chrome_driver
from utils.file_utils import save_to_file
from utils.logger import get_logger

# Import settings
from config.settings import DATA_KEYWORDS, RANDOM_DELAY_MIN, RANDOM_DELAY_MAX

# Set up logger
logger = get_logger(__name__)

# Thread-local storage for driver management
thread_local = threading.local()


def extract_data_section(doi_url, pmid=None, doi_id=None, output_dir=None, ready_dir=None):
    """
    Extract data availability section from a publication.
    
    Args:
        doi_url (str): DOI URL of the publication.
        pmid (str, optional): PubMed ID of the publication. Defaults to None.
        doi_id (str, optional): Identifier for the DOI. Defaults to None.
        output_dir (str, optional): Directory to save output. Defaults to None.
        ready_dir (str, optional): Directory to save ready files for LLM. Defaults to None.
        
    Returns:
        dict: Extracted data section or None if not found.
    """
    logger.info(f"Extracting data section for DOI: {doi_url}")
    
    # Create a new driver for each extraction to avoid conflicts
    driver = None
    
    try:
        # Create a new driver for each extraction
        driver = setup_chrome_driver(use_random_user_agent=True)
        
        # Load the page
        driver.get(doi_url)
        
        # Wait for the page to load (random delay to mimic human behavior)
        delay = random.uniform(RANDOM_DELAY_MIN, RANDOM_DELAY_MAX)
        logger.debug(f"Waiting {delay:.2f} seconds for page to load")
        time.sleep(delay)
        
        # Get page source
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        # Check if page content is loading properly
        if "References" in str(soup) or "Abstract" in str(soup):
            # Search for data availability section
            data_found = False
            result = None
            
            for heading in soup.find_all(["h2", "h3", "h4", "b"]):
                heading_text = heading.get_text()
                
                # Check if heading contains a data keyword
                if any(keyword in heading_text for keyword in DATA_KEYWORDS):
                    logger.info(f"Found data section heading: {heading_text}")
                    data_found = True
                    
                    # Extract paragraph or section following the heading
                    paragraph = extract_paragraph_by_journal(doi_url, heading, soup)
                    
                    if paragraph:
                        # Clean HTML from paragraph
                        paragraph_clean = clean_html(paragraph)
                        
                        # Create result dictionary
                        result = {
                            "DOI": doi_url,
                            "header": heading_text,
                            "paragraph": paragraph_clean,
                            "PubMed_ID": pmid
                        }
                        
                        # Save to output directory if provided - with full JSON structure
                        if output_dir and doi_id:
                            output_path = os.path.join(output_dir, f"{doi_id}.txt")
                            with open(output_path, 'w', encoding='utf-8') as f:
                                json.dump(result, f, indent=2)
                        
                        # Save to ready directory if provided - just the paragraph for LLM
                        if ready_dir and doi_id:
                            ready_path = os.path.join(ready_dir, f"{doi_id}.txt")
                            with open(ready_path, 'w', encoding='utf-8') as f:
                                f.write(paragraph_clean)
                        
                        logger.info(f"Extracted data section for DOI: {doi_url}")
                        return result
            
            if not data_found:
                logger.warning(f"No data section found for DOI: {doi_url}")
        else:
            logger.warning(f"Page content not loading properly for DOI: {doi_url}")
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting data section for DOI {doi_url}: {str(e)}")
        return None
    finally:
        # Always close the driver properly
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.warning(f"Error closing driver: {str(e)}")


def extract_paragraph_by_journal(doi_url, heading, soup):
    """
    Extract paragraph following a heading, with journal-specific handling.
    
    Args:
        doi_url (str): DOI URL of the publication.
        heading: BeautifulSoup heading element.
        soup: BeautifulSoup object.
        
    Returns:
        str: Extracted paragraph or None if not found.
    """
    # Define journal-specific extraction logic
    if 'scitranslmed' in doi_url or '/science' in doi_url or '/sciimmunol' in doi_url:
        # Science family journals
        parent_div = heading.find_parent('div')
        if parent_div:
            text = str(parent_div)
            start_phrase = heading.get_text()
            end_phrase = "</div>"
            
            substring = text[text.find(start_phrase):text.find(end_phrase) + len(end_phrase)]
            
            if '</b>' in substring:
                substring = substring.split('</b>', 1)[1].strip()
            
            substring = substring.rstrip('</div>')
            return substring
    
    elif '/nar' in doi_url or '/neuonc' in doi_url or '/nsr' in doi_url:
        # NAR, Neuro-Oncology, National Science Review
        paragraphs = heading.find_next_siblings("p", limit=3)
        if paragraphs:
            return str(paragraphs)
    
    else:
        # Default extraction - get next sibling
        paragraph = heading.next_sibling
        if paragraph:
            return str(paragraph)
    
    return None


def clean_html(html_text):
    """
    Remove HTML tags and clean up the text.
    
    Args:
        html_text (str): HTML text to clean.
        
    Returns:
        str: Cleaned text.
    """
    # Remove HTML tags
    text_no_html = re.sub(r'<[^>]+>', '', html_text)
    
    # Normalize whitespace
    text_clean = re.sub(r'\s+', ' ', text_no_html).strip()
    
    return text_clean


def process_dois_from_file(file_path, output_dir=None, ready_dir=None):
    """
    Process DOIs from a single file.
    
    Args:
        file_path (str): Path to the DOI file.
        output_dir (str, optional): Directory to save output. Defaults to None.
        ready_dir (str, optional): Directory to save ready files for LLM. Defaults to None.
        
    Returns:
        list: List of extracted data sections.
    """
    results = []
    batch_name = os.path.basename(file_path).replace('.txt', '')
    
    try:
        # Read the DOI file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            lines = content.split('\n')
            
            logger.info(f"Processing {len(lines)} DOIs from file: {file_path}")
            
            # Process each line (DOI) in the file
            for i, line in enumerate(lines):
                if not line.strip():
                    continue
                
                try:
                    # Parse DOI and PMID from the line
                    parts = line.split('\t')
                    doi_url = parts[0].strip()
                    
                    # Extract PMID if available
                    pmid = None
                    if len(parts) > 1 and 'PMID:' in parts[1]:
                        pmid_part = parts[1].strip()
                        pmid = pmid_part.split('PMID:')[1].strip()
                    
                    # Create a unique DOI ID - use batch name (file name) and counter
                    doi_id = f"{batch_name}_{i+1}"
                    
                    # Add small random delay between requests
                    time.sleep(random.uniform(0.1, 0.5))
                    
                    # Extract data section
                    result = extract_data_section(doi_url, pmid, doi_id, output_dir, ready_dir)
                    
                    if result:
                        results.append(result)
                        logger.info(f"Processed DOI {i+1}/{len(lines)} from {file_path}")
                    
                except Exception as e:
                    logger.error(f"Error processing DOI at line {i+1} in {file_path}: {str(e)}")
                    continue
    
    except Exception as e:
        logger.error(f"Error reading DOI file {file_path}: {str(e)}")
    
    logger.info(f"Completed processing file {file_path}, extracted {len(results)} data sections")
    return results


def process_batch(batch, output_dir=None, ready_dir=None):
    """
    Process a batch of DOI files.
    
    Args:
        batch (list): List of DOI file paths.
        output_dir (str, optional): Directory to save output. Defaults to None.
        ready_dir (str, optional): Directory to save ready files for LLM. Defaults to None.
        
    Returns:
        list: List of extracted data sections.
    """
    results = []
    
    for file_path in batch:
        batch_results = process_dois_from_file(file_path, output_dir, ready_dir)
        results.extend(batch_results)
    
    return results


def extract_data_sections(doi_files, output_dir=None, ready_dir=None, workers=4, batch_size=1):
    """
    Extract data sections for multiple DOI files with parallel processing support.
    
    Args:
        doi_files (list): List of DOI file paths.
        output_dir (str, optional): Directory to save output. Defaults to None.
        ready_dir (str, optional): Directory to save ready files for LLM. Defaults to None.
        workers (int, optional): Number of worker threads. Defaults to 4.
        batch_size (int, optional): Size of batches for processing. Defaults to 1.
        
    Returns:
        list: List of extracted data sections.
    """
    # Create output directories if provided
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    if ready_dir:
        os.makedirs(ready_dir, exist_ok=True)
    
    # Divide DOI files into batches for parallel processing
    # Use smaller batch size for DOI files since each file contains multiple DOIs
    batches = [doi_files[i:i+batch_size] for i in range(0, len(doi_files), batch_size)]
    
    logger.info(f"Processing {len(doi_files)} DOI files in {len(batches)} batches with {workers} workers")
    
    all_results = []
    
    if workers <= 1:
        # Sequential processing
        for i, batch in enumerate(batches):
            logger.info(f"Processing batch {i+1}/{len(batches)}")
            batch_results = process_batch(batch, output_dir, ready_dir)
            all_results.extend(batch_results)
    else:
        # Parallel processing with worker threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit all batches to the executor
            future_to_batch = {
                executor.submit(process_batch, batch, output_dir, ready_dir): i 
                for i, batch in enumerate(batches)
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_batch):
                batch_index = future_to_batch[future]
                try:
                    batch_results = future.result()
                    all_results.extend(batch_results)
                    logger.info(f"Completed batch {batch_index+1}/{len(batches)}, "
                               f"extracted {len(batch_results)} data sections")
                except Exception as e:
                    logger.error(f"Error processing batch {batch_index+1}: {str(e)}")
    
    logger.info(f"Completed extraction of {len(all_results)} data sections from {len(doi_files)} DOI files")
    return all_results


if __name__ == "__main__":
    # If script is run directly, for testing
    import sys
    import logging
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1:
        if os.path.isfile(sys.argv[1]):
            # Process a single DOI file
            output_dir = 'test_output' if len(sys.argv) <= 2 else sys.argv[2]
            ready_dir = 'test_ready' if len(sys.argv) <= 3 else sys.argv[3]
            
            os.makedirs(output_dir, exist_ok=True)
            os.makedirs(ready_dir, exist_ok=True)
            
            results = process_dois_from_file(sys.argv[1], output_dir, ready_dir)
            print(f"Extracted {len(results)} data sections")
        else:
            # Process a DOI URL directly
            doi_url = sys.argv[1]
            pmid = sys.argv[2] if len(sys.argv) > 2 else None
            
            result = extract_data_section(doi_url, pmid)
            print(json.dumps(result, indent=2))
    else:
        print("Usage: python data_section.py <doi_file_or_url> [output_dir] [ready_dir]")