#!/usr/bin/env python3
"""
Utility functions for file operations and state management
Simplified to use files as the primary state tracking mechanism
"""

import os
import json
import glob
import logging
from datetime import datetime

logger = logging.getLogger('file_utils')

def ensure_directories(directories):
    """Create directories if they don't exist."""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")

def save_state(filepath, state):
    """Save state to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        logger.debug(f"State saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error saving state to {filepath}: {str(e)}")
        return False

def load_state(filepath, default=None):
    """Load state from a JSON file."""
    if default is None:
        default = {}
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                state = json.load(f)
            logger.debug(f"State loaded from {filepath}")
            return state
        else:
            logger.debug(f"State file {filepath} not found, returning default")
            return default
    except Exception as e:
        logger.error(f"Error loading state from {filepath}: {str(e)}")
        return default

def get_file_list(directory, extension=None):
    """Get a list of files in a directory, optionally filtered by extension."""
    if not os.path.exists(directory):
        logger.warning(f"Directory {directory} does not exist")
        return []
    
    if extension:
        pattern = os.path.join(directory, f"*{extension}")
        files = glob.glob(pattern)
    else:
        files = [os.path.join(directory, f) for f in os.listdir(directory) 
                if os.path.isfile(os.path.join(directory, f))]
    
    logger.debug(f"Found {len(files)} files in {directory}{f' with extension {extension}' if extension else ''}")
    return files

def save_to_file(filepath, content):
    """Save content to a file."""
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        logger.debug(f"Content saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error saving content to {filepath}: {str(e)}")
        return False

def load_from_file(filepath, as_json=True):
    """Load content from a file."""
    try:
        if os.path.exists(filepath):
            if as_json:
                with open(filepath, 'r') as f:
                    content = json.load(f)
                logger.debug(f"Content loaded from {filepath} as json")
                return content
            else:
                with open(filepath, 'r') as f:
                    content = f.read()
                logger.debug(f"Content loaded from {filepath} as plain file")
                return content
                
        else:
            logger.debug(f"File {filepath} not found, returning default")
            return None
    except Exception as e:
        logger.error(f"Error loading content from {filepath}: {str(e)}")
        return None

def save_doi(doi_id, doi_value, output_dir):
    """Save DOI to a file and update DOI state incrementally."""
    filename = os.path.join(output_dir, f"{doi_id}.txt")
    success = save_to_file(filename, doi_value)
    
    # Update DOI state file incrementally
    state_file = os.path.join(os.path.dirname(output_dir), 'pipeline_state', 'doi_extraction.json')
    state = load_state(state_file, {'processed_dois': [], 'last_updated': None})
    
    if doi_id not in state['processed_dois']:
        state['processed_dois'].append(doi_id)
    
    state['last_updated'] = datetime.now().isoformat()
    state['count'] = len(state['processed_dois'])
    
    save_state(state_file, state)
    return success

def save_data_section(doi_id, data_section, output_dir, ready_dir=None):
    """Save data section to a file and optionally to a ready-for-LLM directory."""
    filename = os.path.join(output_dir, f"{doi_id}.txt")
    success = save_to_file(filename, data_section)
    
    # Also save to ready_dir if provided
    if ready_dir and success:
        ready_filename = os.path.join(ready_dir, f"{doi_id}.txt")
        success = save_to_file(ready_filename, data_section)
    
    # Update data section state file incrementally
    state_file = os.path.join(os.path.dirname(output_dir), 'pipeline_state', 'data_section.json')
    state = load_state(state_file, {'processed_sections': [], 'last_updated': None})
    
    if doi_id not in state['processed_sections']:
        state['processed_sections'].append(doi_id)
    
    state['last_updated'] = datetime.now().isoformat()
    state['count'] = len(state['processed_sections'])
    
    save_state(state_file, state)
    return success

def save_llm_result(doi_id, llm_result, output_dir):
    """Save LLM result to a JSON file."""
    filename = os.path.join(output_dir, f"{doi_id}.json")
    success = save_state(filename, llm_result)
    
    # Update LLM state file incrementally
    state_file = os.path.join(os.path.dirname(output_dir), 'pipeline_state', 'llm_extraction.json')
    state = load_state(state_file, {'processed_items': [], 'last_updated': None})
    
    if doi_id not in state['processed_items']:
        state['processed_items'].append(doi_id)
    
    state['last_updated'] = datetime.now().isoformat()
    state['count'] = len(state['processed_items'])
    
    save_state(state_file, state)
    return success

def move_processed_file(src_file, processed_dir):
    """Move a file to a processed directory after it's been processed."""
    try:
        if not os.path.exists(processed_dir):
            os.makedirs(processed_dir, exist_ok=True)
        
        basename = os.path.basename(src_file)
        dest_file = os.path.join(processed_dir, basename)
        
        if os.path.exists(dest_file):
            # Add timestamp to avoid overwriting
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            name, ext = os.path.splitext(basename)
            dest_file = os.path.join(processed_dir, f"{name}_{timestamp}{ext}")
        
        os.rename(src_file, dest_file)
        logger.debug(f"Moved {src_file} to {dest_file}")
        return True
    except Exception as e:
        logger.error(f"Error moving {src_file} to {processed_dir}: {str(e)}")
        return False

def get_file_age(filepath):
    """Get the age of a file in seconds."""
    try:
        mtime = os.path.getmtime(filepath)
        now = datetime.now().timestamp()
        return now - mtime
    except Exception as e:
        logger.error(f"Error getting age of {filepath}: {str(e)}")
        return None

def get_latest_files(directory, extension=None, count=10):
    """Get a list of the latest files in a directory, sorted by modification time."""
    files = get_file_list(directory, extension)
    if not files:
        return []
    
    # Sort by modification time (newest first)
    files.sort(key=os.path.getmtime, reverse=True)
    
    # Return requested count
    return files[:count]