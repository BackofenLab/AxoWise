"""
DOI Extraction Module

This module handles the extraction of DOIs and PMIDs from publication websites.
Includes pagination support to extract DOIs across multiple pages.
All DOIs for a journal batch are saved in a single file.
"""

import os
import time
import re
import json
import urllib.parse
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# import utilities
from utils.browser import setup_chrome_driver
from utils.file_utils import save_to_file, ensure_directories, load_state, save_state

# import settings - if possible, otherwise use defaults
try:
    from config.settings import (
        OUTPUT_DIR,
        JOURNAL_BATCH_SIZE,
        BASE_URL_TEMPLATE,
        SCROLL_PAUSE_TIME,
        JOURNALS
    )
except ImportError:
    # default values if settings can't be imported
    OUTPUT_DIR = "output"
    JOURNAL_BATCH_SIZE = 3
    BASE_URL_TEMPLATE = "https://www.10xgenomics.com/publications?sortBy=master%3Apublications-relevance&page=1&refinementList%5Bspecies%5D%5B0%5D=Human&refinementList%5Bspecies%5D%5B1%5D=Mouse"
    SCROLL_PAUSE_TIME = 1.5

# Set up logger
logger = logging.getLogger("doi_extraction")


def build_url(journals_batch, page_num=1):
    """
    Build URL for the journals batch with pagination.
    
    Args:
        journals_batch (list): List of journal names to include in the URL.
        page_num (int, optional): Page number for pagination. Defaults to 1.
        
    Returns:
        tuple: (url, filename_prefix) - The constructed URL and filename prefix.
    """
    # Construct base URL with current page number
    base_url = f"https://www.10xgenomics.com/publications?sortBy=master%3Apublications-relevance&page={page_num}&refinementList%5Bspecies%5D%5B0%5D=Human&refinementList%5Bspecies%5D%5B1%5D=Mouse"
    
    filename_prefix = ""
    
    # Add journal filters
    for count, journal in enumerate(journals_batch):
        filename_prefix += f"_{journal}"
        base_url += f"&refinementList%5Bjournal%5D%5B{count}%5D={urllib.parse.quote(journal)}"
    
    return base_url, filename_prefix


def extract_doi_from_html(html_content):
    """
    Extract DOI URLs and PMIDs from HTML content.
    
    Args:
        html_content (str): HTML content to parse.
        
    Returns:
        list: List of lists, each containing [doi_url, pmid].
    """
    paper_ids = []
    doi_entry = None
    pmid_entry = None

    soup = BeautifulSoup(html_content, 'html.parser')
    # Updated class name to match the current website structure
    searchHits = soup.find_all('a', {'class': 'css-1nszd81 ebym1kq0'})

    for hit in searchHits:
        if 'DOI' in str(hit):    
            pattern_doi = r'https://doi.org/[^\s"]+'
            doi_match = re.search(pattern_doi, str(hit))
            if doi_match:
                doi_entry = str(doi_match[0])
                pmid_entry = None
        
        elif 'PubMed' in str(hit):
            pattern_pmid = r'pubmed\.ncbi\.nlm\.nih\.gov/(\d+)'
            pmid_match = re.search(pattern_pmid, hit['href'])
            if pmid_match:
                pmid_entry = pmid_match.group(1)

                if doi_entry:
                    paper_ids.append([doi_entry, pmid_entry])
                    doi_entry = None
                    pmid_entry = None
            
    return paper_ids


def extract_dois_for_journals_batch(journals_batch, output_dir, state):
    """
    Extract DOIs for a batch of journals with pagination support.
    
    Args:
        journals_batch (list): List of journal names to process.
        output_dir (str): Directory to save extracted DOIs.
        state (dict): Current state for resumption.
        
    Returns:
        tuple: (output_filename, paper_ids) - The output filename and list of extracted paper IDs.
    """
    # Build batch identifier and filename
    _, filename_prefix = build_url(journals_batch)
    batch_id = filename_prefix.strip('_')
    output_filename = f"{batch_id}.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    # Check if this batch has already been processed
    if batch_id in state.get('processed_batches', []):
        logger.info(f"Batch {batch_id} already processed, skipping...")
        return output_path, []
    
    logger.info(f"Processing journals: {', '.join(journals_batch)}")
    
    all_paper_ids = []
    page_num = 1
    has_more_data = True
    
    # Set up Chrome driver once for all pages in this batch
    driver = setup_chrome_driver()
    
    try:
        while has_more_data:
            # Build URL for current page
            base_url, _ = build_url(journals_batch, page_num)
            logger.info(f"Processing page {page_num}: {base_url}")
            
            try:
                # Load the page
                driver.get(base_url)
                time.sleep(2)  # Wait for initial page load
                
                # Find the publication elements
                publication_elements = driver.find_element(By.CLASS_NAME, "PublicationSearch")
                
                # Check if we have any search hits on this page
                searchHits = driver.find_elements(By.CSS_SELECTOR, 'a.css-1nszd81.ebym1kq0')
                if not searchHits:
                    logger.info(f"No search hits found on page {page_num}, stopping pagination")
                    has_more_data = False
                    continue
                
                # Infinite scroll on this page
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    
                    if new_height == last_height:
                        logger.info(f"Reached the end of page {page_num}")
                        break
                    
                    last_height = new_height
                
                # Extract DOIs from this fully scrolled page
                html_content = publication_elements.get_attribute("outerHTML")
                page_paper_ids = extract_doi_from_html(html_content)
                
                if not page_paper_ids:
                    logger.info(f"No paper IDs found on page {page_num}, stopping pagination")
                    has_more_data = False
                else:
                    logger.info(f"Extracted {len(page_paper_ids)} DOIs from page {page_num}")
                    all_paper_ids.extend(page_paper_ids)
                    
                    # Move to next page
                    page_num += 1
                    
            except Exception as e:
                logger.error(f"Error on page {page_num}: {str(e)}")
                logger.info("No more pages available")
                has_more_data = False
    
    finally:
        # Close the Chrome driver after processing all pages
        driver.quit()
    
    # Save all DOIs to a single file
    if all_paper_ids:
        # Format the content for the file
        content_lines = []
        for i, paper_id in enumerate(all_paper_ids):
            doi_url = paper_id[0]
            pmid = paper_id[1]
            content_lines.append(f"{doi_url}\tPMID: {pmid if pmid else 'None'}")
        
        # Join all lines with newlines
        file_content = "\n".join(content_lines)
        
        # Save to file
        if save_to_file(output_path, file_content):
            logger.info(f"Saved {len(all_paper_ids)} DOIs to {output_filename}")
            
            # Update state
            if 'processed_batches' not in state:
                state['processed_batches'] = []
            state['processed_batches'].append(batch_id)
            state['count'] = state.get('count', 0) + len(all_paper_ids)
            state['last_updated'] = datetime.now().isoformat()
    
    return output_path, all_paper_ids


def extract_dois(journals=None, output_dir=None, state_file=None):
    """
    Extract DOIs for the specified journals across all available pages.
    
    Args:
        journals (list, optional): List of journal names to process. Defaults to None.
        output_dir (str, optional): Directory to save extracted DOIs. Defaults to None.
        state_file (str, optional): Path to state file. Defaults to None.
        
    Returns:
        list: List of paths to extracted DOI files.
    """
    # Use default values if not provided
    if journals is None:
        journals = JOURNALS
    
    if output_dir is None:
        output_dir = os.path.join(OUTPUT_DIR, "dois")
    
    if state_file is None:
        state_file = os.path.join(os.path.dirname(output_dir), "pipeline_state", "doi_extraction.json")
    
    # Ensure directories exist
    ensure_directories([output_dir, os.path.dirname(state_file)])
    
    # Initialize or load state
    state = load_state(state_file, {
        'start_time': datetime.now().isoformat(),
        'processed_batches': [],
        'count': 0,
        'status': 'initialized',
        'last_updated': datetime.now().isoformat()
    })
    
    # Update state to indicate we're starting
    state['status'] = 'running'
    state['last_updated'] = datetime.now().isoformat()
    save_state(state_file, state)
    
    logger.info(f"Starting DOI extraction for journals: {', '.join(journals)}")
    
    # List to store all extracted DOI files
    result_files = []
    total_dois = 0
    
    # Process journals in batches
    for i in range(0, len(journals), JOURNAL_BATCH_SIZE):
        journals_batch = journals[i:i + JOURNAL_BATCH_SIZE]
        
        # Extract DOIs for this batch
        output_file, paper_ids = extract_dois_for_journals_batch(journals_batch, output_dir, state)
        
        # Add to results and count
        if output_file and os.path.exists(output_file):
            result_files.append(output_file)
            total_dois += len(paper_ids)
        
        # Save updated state after each batch
        save_state(state_file, state)
        
        logger.info(f"Completed batch {i//JOURNAL_BATCH_SIZE + 1}/{(len(journals)-1)//JOURNAL_BATCH_SIZE + 1}")
    
    # Update final state
    state['status'] = 'completed'
    state['end_time'] = datetime.now().isoformat()
    state['count'] = total_dois
    save_state(state_file, state)
    
    logger.info(f"DOI extraction completed. Total DOIs extracted: {total_dois} in {len(result_files)} files")
    return result_files


if __name__ == "__main__":
    # Set up logging when run directly
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create output directory
    doi_output_dir = os.path.join(OUTPUT_DIR, "dois")
    os.makedirs(doi_output_dir, exist_ok=True)
    
    # Extract DOIs for all journals or a subset for testing
    dois = extract_dois(journals=JOURNALS[:5], output_dir=doi_output_dir)
    print(f"Extracted DOIs saved to: {', '.join(dois)}")