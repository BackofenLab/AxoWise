#!/usr/bin/env python3
"""
Update metadata in LLM results files to match the corresponding data sections files.

This script:
1. Scans the data_sections directory for all JSON/TXT files
2. Scans the llm_results directory for all JSON files
3. Matches files by filename (without extension)
4. Updates the DOI and PubMed_ID in the llm_results files with values from data_sections
5. Saves the updated llm_results files
"""

import os
import json
import glob
from pathlib import Path

# Define paths
OUTPUT_DIR = "output"  # Change this if your output directory is elsewhere
DATA_SECTIONS_DIR = os.path.join(OUTPUT_DIR, "data_sections")
LLM_RESULTS_DIR = os.path.join(OUTPUT_DIR, "llm_results")

def load_json_file(filepath):
    """Load a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def save_json_file(data, filepath):
    """Save data to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def update_llm_results():
    """Update DOI and PubMed_ID in LLM results files from data sections."""
    # Ensure directories exist
    if not os.path.exists(DATA_SECTIONS_DIR) or not os.path.exists(LLM_RESULTS_DIR):
        print(f"Error: One or both directories don't exist: {DATA_SECTIONS_DIR}, {LLM_RESULTS_DIR}")
        return

    # Get all data section files
    data_section_files = glob.glob(os.path.join(DATA_SECTIONS_DIR, "*.json"))
    if not data_section_files:
        # Try TXT files if no JSON files found
        data_section_files = glob.glob(os.path.join(DATA_SECTIONS_DIR, "*.txt"))
    
    if not data_section_files:
        print(f"No data section files found in {DATA_SECTIONS_DIR}")
        return

    # Get all LLM result files
    llm_result_files = glob.glob(os.path.join(LLM_RESULTS_DIR, "*.json"))
    if not llm_result_files:
        print(f"No LLM result files found in {LLM_RESULTS_DIR}")
        return

    # Create mapping of filenames (without extension) to file paths
    data_section_map = {Path(file).stem: file for file in data_section_files}
    llm_result_map = {Path(file).stem: file for file in llm_result_files}

    print(f"Found {len(data_section_map)} data section files and {len(llm_result_map)} LLM result files")

    # Counter for updates
    updated_count = 0
    error_count = 0

    # Process each LLM result file
    for filename, llm_file_path in llm_result_map.items():
        # Check if corresponding data section file exists
        if filename in data_section_map:
            data_section_path = data_section_map[filename]
            
            # Load both files
            data_section = load_json_file(data_section_path)
            llm_result = load_json_file(llm_file_path)
            
            if data_section and llm_result:
                # Update DOI and PubMed_ID in LLM result
                try:
                    # Save original values for logging
                    original_doi = llm_result.get("DOI")
                    original_pmid = llm_result.get("PubMed_ID")
                    
                    # Update with values from data section
                    llm_result["DOI"] = data_section.get("DOI")
                    llm_result["PubMed_ID"] = data_section.get("PubMed_ID")
                    
                    # Save updated LLM result
                    if save_json_file(llm_result, llm_file_path):
                        updated_count += 1
                        print(f"Updated {filename}: DOI changed from '{original_doi}' to '{llm_result['DOI']}', PubMed_ID from '{original_pmid}' to '{llm_result['PubMed_ID']}'")
                    else:
                        error_count += 1
                except Exception as e:
                    print(f"Error updating {filename}: {e}")
                    error_count += 1
            else:
                print(f"Error: Could not load one or both files for {filename}")
                error_count += 1
        else:
            print(f"Warning: No matching data section file found for LLM result {filename}")

    print(f"\nSummary: Updated {updated_count} files with {error_count} errors")

if __name__ == "__main__":
    update_llm_results()