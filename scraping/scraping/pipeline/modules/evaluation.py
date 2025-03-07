"""
Evaluation Module

This module handles the evaluation of LLM extraction results.
"""

import os
import json
import time
from collections import Counter, defaultdict
import re

# Import utilities
from utils.logger import get_logger
from utils.file_utils import load_from_file

# Import settings
from config.settings import OUTPUT_DIR

# Set up logger
logger = get_logger(__name__)


def evaluate_results(llm_result_files=None):
    """
    Evaluate LLM extraction results.
    
    Args:
        llm_result_files (list): List of LLM result file paths.
        
    Returns:
        dict: Evaluation results.
    """
    #if llm_result_files is None:
    llm_dir = os.path.join(OUTPUT_DIR, "llm_results")
    logger.info(llm_dir)
    print(llm_dir)
    llm_result_files = [os.path.join(llm_dir, f) for f in os.listdir(llm_dir) if f.endswith('.json')]
    
    logger.info(f"Evaluating {len(llm_result_files)} LLM result files")
    
    # Load results
    results = []
    for file in llm_result_files:
        result = load_from_file(file, as_json=True)
        if result:
            results.append(result)
    
    logger.info(f"Loaded {len(results)} valid results")
    
    # Initialize simplified evaluation metrics (only includes requested fields)
    evaluation = {
        "total_papers": len(results),
        "total_papers_with_data": 0,
        "data_statistics": {
            "accession_codes": {
                "total": 0,
                "most_common": []
            },
            "scripts": {
                "total": 0,
                "domains": {}
            },
            "analysis_data": {
                "total": 0,
                "domains": {}
            }
        },
        "execution_time": {}
    }
    
    # Counters for aggregate statistics
    all_accession_codes = []
    all_scripts = []
    all_analysis_data = []
    
    # Process each result
    for result in results:
        extraction_results = result.get("results", {})
        
        # Process accession codes
        accession_codes = extraction_results.get("accession_codes", [])
        if accession_codes:
            all_accession_codes.extend(accession_codes)
        
        # Process scripts
        scripts = extraction_results.get("scripts", [])
        if scripts:
            all_scripts.extend(scripts)
            
            # Count domains for scripts
            for script in scripts:
                domain = extract_domain(script)
                if domain:
                    evaluation["data_statistics"]["scripts"]["domains"][domain] = evaluation["data_statistics"]["scripts"]["domains"].get(domain, 0) + 1
        
        # Process analysis data
        analysis_data = extraction_results.get("analysis_data", [])
        if analysis_data:
            all_analysis_data.extend(analysis_data)
            
            # Count domains for analysis data
            for data_url in analysis_data:
                domain = extract_domain(data_url)
                if domain:
                    evaluation["data_statistics"]["analysis_data"]["domains"][domain] = evaluation["data_statistics"]["analysis_data"]["domains"].get(domain, 0) + 1
        
        # Count papers with any data
        if accession_codes or scripts or analysis_data:
            evaluation["total_papers_with_data"] += 1
    
    # Calculate aggregate statistics
    evaluation["data_statistics"]["accession_codes"]["total"] = len(all_accession_codes)
    evaluation["data_statistics"]["scripts"]["total"] = len(all_scripts)
    evaluation["data_statistics"]["analysis_data"]["total"] = len(all_analysis_data)
    
    # Calculate most common accession codes
    if all_accession_codes:
        code_counter = Counter(all_accession_codes)
        evaluation["data_statistics"]["accession_codes"]["most_common"] = code_counter.most_common(10)
    
    # Record execution time for this evaluation
    execution_time = time.time()
    evaluation["execution_time"] = {
        "timestamp": execution_time,
        "iso_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(execution_time))
    }
    
    logger.info(f"Evaluation completed: {evaluation['total_papers_with_data']} papers with data out of {evaluation['total_papers']} total papers")
    
    return evaluation


def extract_domain(url):
    """
    Extract domain from URL.
    
    Args:
        url (str): URL to extract domain from.
        
    Returns:
        str: Domain name or None if not found.
    """
    if not url or not isinstance(url, str):
        return None
    
    domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
    if domain_match:
        return domain_match.group(1)
    
    return None


if __name__ == "__main__":
    # If script is run directly, for testing
    # evaluation_results = evaluate_results()
    # print(json.dumps(evaluation_results, indent=2))
    import sys
    
    if len(sys.argv) > 1:
        result_dir = sys.argv[1]
        
        if os.path.isdir(result_dir):
            result_files = [os.path.join(result_dir, f) for f in os.listdir(result_dir) if f.endswith('.json')]
            evaluation_results = evaluate_results(result_files)
            print(json.dumps(evaluation_results, indent=2))
        else:
            print(f"Error: {result_dir} is not a directory")
    else:
        print("Usage: python evaluation.py <llm_results_directory>")