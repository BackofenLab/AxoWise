#!/usr/bin/env python3
"""
Research Data Extraction Pipeline - Simplified Main Entry Point
- Fixed resume_parallel functionality
- Simplified code structure
- Improved state management
- Better error handling
"""

import os
import argparse
import json
import time
import threading
from datetime import datetime
import logging
import signal

# Import modules
from modules.doi_extraction import extract_dois
from modules.data_section import extract_data_sections
from modules.llm_extraction import process_with_llm
from modules.evaluation import evaluate_results

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('pipeline')

# Define state file paths
STATE_DIR = 'pipeline_state'
DOI_STATE = os.path.join(STATE_DIR, 'doi_extraction.json')
DATA_SECTION_STATE = os.path.join(STATE_DIR, 'data_section.json')
LLM_STATE = os.path.join(STATE_DIR, 'llm_extraction.json')
PIPELINE_STATE = os.path.join(STATE_DIR, 'pipeline_state.json')

# Define output directories
OUTPUT_DIR = 'output'
DOI_DIR = os.path.join(OUTPUT_DIR, 'dois')
DATA_SECTION_DIR = os.path.join(OUTPUT_DIR, 'data_sections')
LLM_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'llm_results')
READY_FOR_LLM_DIR = os.path.join(OUTPUT_DIR, 'ready_for_llm')

# Signal file for communication between processes
DATA_SECTION_SIGNAL = os.path.join(STATE_DIR, 'data_section_completed.signal')

# Global stop event for graceful shutdown
stop_event = threading.Event()

def ensure_directories(directories):
    """Create directories if they don't exist."""
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def save_state(filepath, state):
    """Save state to a JSON file."""
    try:
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
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
            return state
        else:
            return default
    except Exception as e:
        logger.error(f"Error loading state from {filepath}: {str(e)}")
        return default

def get_file_list(directory, extension=None):
    """Get a list of files in a directory, optionally filtered by extension."""
    if not os.path.exists(directory):
        return []
    
    if extension:
        return [os.path.join(directory, f) for f in os.listdir(directory) 
                if f.endswith(extension) and os.path.isfile(os.path.join(directory, f))]
    else:
        return [os.path.join(directory, f) for f in os.listdir(directory) 
                if os.path.isfile(os.path.join(directory, f))]

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Research Data Extraction Pipeline')
    parser.add_argument('--mode', type=str, required=True, choices=[
        'full', 'doi_extraction', 'data_section', 'llm_extraction',
        'evaluate', 'resume', 'parallel', 'resume_parallel', 'rebuild_state', 'stats'
    ], help='Pipeline execution mode')
    parser.add_argument('--workers-data', type=int, default=4, help='Number of workers for data section extraction')
    parser.add_argument('--workers-llm', type=int, default=2, help='Number of workers for LLM processing')
    parser.add_argument('--journals', type=str, nargs='+', help='Journal names to process')
    parser.add_argument('--batch-size', type=int, default=50, help='Batch size for processing')
    return parser.parse_args()

def init_pipeline():
    """Initialize pipeline directories and state files."""
    # Create necessary directories
    ensure_directories([
        STATE_DIR, OUTPUT_DIR, DOI_DIR, DATA_SECTION_DIR, 
        LLM_OUTPUT_DIR, READY_FOR_LLM_DIR
    ])
    
    # Initialize pipeline state if it doesn't exist
    if not os.path.exists(PIPELINE_STATE):
        initial_state = {
            'start_time': datetime.now().isoformat(),
            'mode': None,
            'status': 'initialized',
            'doi_extraction': {'status': 'pending', 'count': 0},
            'data_section': {'status': 'pending', 'count': 0},
            'llm_extraction': {'status': 'pending', 'count': 0},
            'evaluation': {'status': 'pending'},
            'last_updated': datetime.now().isoformat()
        }
        save_state(PIPELINE_STATE, initial_state)
    
    return load_state(PIPELINE_STATE)

def update_pipeline_state(component, status, count=None):
    """Update pipeline state for a specific component."""
    state = load_state(PIPELINE_STATE)
    state[component]['status'] = status
    if count is not None:
        state[component]['count'] = count
    state['last_updated'] = datetime.now().isoformat()
    save_state(PIPELINE_STATE, state)
    return state

def count_dois_in_files(file_list):
    """Count the total number of DOIs in a list of DOI files."""
    total_dois = 0
    for file_path in file_list:
        try:
            with open(file_path, 'r') as f:
                # Count non-empty lines
                lines = [line.strip() for line in f.readlines() if line.strip()]
                total_dois += len(lines)
        except Exception as e:
            logger.error(f"Error reading DOI file {file_path}: {str(e)}")
    return total_dois

def run_doi_extraction(args):
    """Run DOI extraction component and update state."""
    logger.info("Starting DOI extraction...")
    update_pipeline_state('doi_extraction', 'running')
    
    # Extract DOIs
    doi_files = extract_dois(
        journals=args.journals, 
        output_dir=DOI_DIR,
        state_file=DOI_STATE
    )
    
    # Count actual DOIs in the files
    doi_count = count_dois_in_files(doi_files)
    
    # Update final state with the actual DOI count
    update_pipeline_state('doi_extraction', 'completed', doi_count)
    logger.info(f"DOI extraction completed. Extracted {doi_count} DOIs in {len(doi_files)} files.")
    
    return doi_files

def run_data_section_extraction(args, dois=None):
    """Run data section extraction component."""
    logger.info("Starting data section extraction...")
    update_pipeline_state('data_section', 'running')
    
    if not dois:
        # Load DOIs from files if not provided
        dois = get_file_list(DOI_DIR, '.txt')
        if not dois:
            logger.error("No DOIs found for data section extraction")
            update_pipeline_state('data_section', 'error')
            return []
    
    # Extract data sections in batches
    processed_sections = extract_data_sections(
        dois, 
        output_dir=DATA_SECTION_DIR,
        ready_dir=READY_FOR_LLM_DIR,
        workers=args.workers_data,
        batch_size=args.batch_size
    )
    
    # Update state
    update_pipeline_state('data_section', 'completed', len(processed_sections))
    logger.info(f"Data section extraction completed. Processed {len(processed_sections)} sections.")
    return processed_sections

def run_llm_extraction(args, data_sections=None):
    """Run LLM extraction component."""
    logger.info("Starting LLM extraction...")
    update_pipeline_state('llm_extraction', 'running')
    
    if not data_sections:
        # Load data sections from READY_FOR_LLM_DIR if not provided
        data_sections = get_file_list(READY_FOR_LLM_DIR, '.txt')
        if not data_sections:
            logger.error("No data sections found for LLM extraction")
            update_pipeline_state('llm_extraction', 'error')
            return []
    
    # Process with LLM
    processed_items = process_with_llm(
        data_sections, 
        output_dir=LLM_OUTPUT_DIR,
        workers=args.workers_llm,
        batch_size=args.batch_size
    )
    
    # Update state
    update_pipeline_state('llm_extraction', 'completed', len(processed_items))
    logger.info(f"LLM extraction completed. Processed {len(processed_items)} items.")
    return processed_items

def run_evaluation(args):
    """Run evaluation component."""
    logger.info("Starting evaluation...")
    update_pipeline_state('evaluation', 'running')
    
    # Run evaluation
    logger.info(LLM_OUTPUT_DIR)
    results = evaluate_results(LLM_OUTPUT_DIR)
    
    eval_result = os.path.join(OUTPUT_DIR,"evaluation")
    logger.info(results)
    with open(f"{eval_result}/eval.json",'w') as file:
        json.dump(results,file,indent=2)

    # Update state
    update_pipeline_state('evaluation', 'completed')
    logger.info("Evaluation completed.")
    return results

def data_section_worker(args, dois):
    """Worker function for data section extraction thread."""
    try:
        # Run data section extraction
        processed_sections = run_data_section_extraction(args, dois)
        
        # Signal completion by creating a signal file
        with open(DATA_SECTION_SIGNAL, 'w') as f:
            f.write(f"Completed at {datetime.now().isoformat()}")
            
        logger.info("Data section extraction completed and signaled.")
        return processed_sections
    
    except Exception as e:
        logger.error(f"Error in data section worker: {str(e)}", exc_info=True)
        return []

def llm_worker(args):
    """Worker function for LLM extraction thread."""
    try:
        # Initialize tracking sets
        processed_files = set()
        
        # Continue until stop event is set or data section extraction is complete
        # and all files have been processed
        while not stop_event.is_set():
            # Get current list of files in the ready-for-llm directory
            current_files = set(get_file_list(READY_FOR_LLM_DIR, '.txt'))
            
            # Find new files that haven't been processed
            new_files = current_files - processed_files
            
            if new_files:
                # Process new files
                logger.info(f"Processing {len(new_files)} new data sections")
                process_with_llm(
                    list(new_files), 
                    output_dir=LLM_OUTPUT_DIR,
                    workers=args.workers_llm,
                    batch_size=args.batch_size
                )
                
                # Update processed files set
                processed_files.update(new_files)
                
                # Update state with current count
                update_pipeline_state('llm_extraction', 'running', len(processed_files))
            
            # Check if data section extraction is complete and all files processed
            if (os.path.exists(DATA_SECTION_SIGNAL) and 
                    current_files == processed_files):
                logger.info("All data sections processed. LLM extraction complete.")
                break
            
            # Sleep briefly to avoid high CPU usage
            time.sleep(1)
        
        # Final state update
        if not stop_event.is_set():
            update_pipeline_state('llm_extraction', 'completed', len(processed_files))
        
        return list(processed_files)
    
    except Exception as e:
        logger.error(f"Error in LLM worker: {str(e)}", exc_info=True)
        return []

def run_parallel_pipeline(args, resume=False):
    """Run pipeline with parallel processing for data section and LLM extraction."""
    logger.info(f"Starting {'resumed ' if resume else ''}parallel pipeline...")
    
    # Initialize or load state
    pipeline_state = init_pipeline()
    pipeline_state['mode'] = 'parallel'
    pipeline_state['status'] = 'running'
    save_state(PIPELINE_STATE, pipeline_state)
    
    # Remove signal file if it exists
    if os.path.exists(DATA_SECTION_SIGNAL):
        os.remove(DATA_SECTION_SIGNAL)
    
    # Step 1: DOI extraction (if not resuming or not completed)
    dois = []
    if resume and pipeline_state['doi_extraction']['status'] == 'completed':
        logger.info("Resuming: DOI extraction already completed")
        dois = get_file_list(DOI_DIR, '.txt')
    else:
        dois = run_doi_extraction(args)
    
    # Skip if no DOIs
    if not dois:
        logger.error("No DOIs to process. Pipeline cannot continue.")
        update_pipeline_state('data_section', 'error')
        update_pipeline_state('llm_extraction', 'error')
        return
    
    # Step 2: Get pending DOIs for resuming data section extraction
    pending_dois = dois
    if resume:
        # Get already processed data sections
        processed_sections = get_file_list(DATA_SECTION_DIR, '.txt')
        processed_doi_ids = {os.path.splitext(os.path.basename(p))[0] for p in processed_sections}
        
        # Filter out DOIs that have already been processed
        pending_dois = [
            doi for doi in dois 
            if os.path.splitext(os.path.basename(doi))[0] not in processed_doi_ids
        ]
        
        logger.info(f"Resuming data section extraction: {len(pending_dois)} DOIs remaining out of {len(dois)}")
    
    # Step 3: Run data section extraction and LLM extraction in parallel
    data_thread = threading.Thread(
        target=data_section_worker,
        args=(args, pending_dois)
    )
    
    llm_thread = threading.Thread(
        target=llm_worker,
        args=(args,)
    )
    
    # Set threads as daemon to ensure they exit when the main program exits
    data_thread.daemon = True
    llm_thread.daemon = True
    
    # Start threads
    data_thread.start()
    llm_thread.start()
    
    try:
        # Wait for threads to complete
        data_thread.join()
        llm_thread.join()
        
        # Step 4: Run evaluation
        run_evaluation(args)
        
        # Update final pipeline state
        pipeline_state = load_state(PIPELINE_STATE)
        pipeline_state['status'] = 'completed'
        pipeline_state['end_time'] = datetime.now().isoformat()
        save_state(PIPELINE_STATE, pipeline_state)
        
        logger.info("Parallel pipeline completed.")
    
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user.")
        stop_event.set()
        
        # Update pipeline state
        pipeline_state = load_state(PIPELINE_STATE)
        pipeline_state['status'] = 'interrupted'
        pipeline_state['end_time'] = datetime.now().isoformat()
        save_state(PIPELINE_STATE, pipeline_state)
    
    except Exception as e:
        logger.error(f"Error in parallel pipeline: {str(e)}", exc_info=True)
        stop_event.set()
        
        # Update pipeline state
        pipeline_state = load_state(PIPELINE_STATE)
        pipeline_state['status'] = 'error'
        pipeline_state['error'] = str(e)
        pipeline_state['end_time'] = datetime.now().isoformat()
        save_state(PIPELINE_STATE, pipeline_state)

def rebuild_pipeline_state():
    """Rebuild pipeline state from existing files."""
    logger.info("Rebuilding pipeline state from existing files...")
    
    # Initialize new state
    state = {
        'start_time': datetime.now().isoformat(),
        'mode': 'rebuilt',
        'status': 'completed',
        'doi_extraction': {'status': 'unknown', 'count': 0},
        'data_section': {'status': 'unknown', 'count': 0},
        'llm_extraction': {'status': 'unknown', 'count': 0},
        'evaluation': {'status': 'unknown'},
        'last_updated': datetime.now().isoformat()
    }
    
    # Count DOIs
    dois = get_file_list(DOI_DIR, '.txt')
    if dois:
        state['doi_extraction']['status'] = 'completed'
        state['doi_extraction']['count'] = len(dois)
    
    # Count data sections
    data_sections = get_file_list(DATA_SECTION_DIR, '.txt')
    if data_sections:
        state['data_section']['status'] = 'completed'
        state['data_section']['count'] = len(data_sections)
    
    # Count LLM outputs
    llm_outputs = get_file_list(LLM_OUTPUT_DIR, '.json')
    if llm_outputs:
        state['llm_extraction']['status'] = 'completed'
        state['llm_extraction']['count'] = len(llm_outputs)
    
    # Save rebuilt state
    save_state(PIPELINE_STATE, state)
    logger.info("Pipeline state rebuilt.")
    return state

def display_pipeline_stats(state_dir=STATE_DIR, output_dir=OUTPUT_DIR):
    """Display pipeline statistics."""
    # Load pipeline state
    pipeline_state = load_state(PIPELINE_STATE, {
        'status': 'unknown',
        'mode': 'unknown',
        'start_time': 'unknown',
        'doi_extraction': {'status': 'unknown', 'count': 0},
        'data_section': {'status': 'unknown', 'count': 0},
        'llm_extraction': {'status': 'unknown', 'count': 0},
        'evaluation': {'status': 'unknown'},
    })
    
    # Calculate elapsed time if start_time exists
    elapsed = "Unknown"
    if pipeline_state.get('start_time') and pipeline_state['start_time'] != 'unknown':
        try:
            start_time = datetime.fromisoformat(pipeline_state['start_time'])
            end_time = (datetime.fromisoformat(pipeline_state.get('end_time', datetime.now().isoformat())))
            elapsed_seconds = (end_time - start_time).total_seconds()
            
            # Format as hours, minutes, seconds
            hours = int(elapsed_seconds // 3600)
            minutes = int((elapsed_seconds % 3600) // 60)
            seconds = int(elapsed_seconds % 60)
            elapsed = f"{hours}h {minutes}m {seconds}s"
        except:
            elapsed = "Error calculating"
    
    # Print header
    print("\n" + "="*70)
    print(f"PIPELINE STATUS: {pipeline_state['status'].upper()}")
    print("="*70)
    
    # Print summary
    print(f"Mode: {pipeline_state['mode']}")
    print(f"Started: {pipeline_state.get('start_time', 'Unknown')}")
    if 'end_time' in pipeline_state:
        print(f"Ended: {pipeline_state['end_time']}")
    print(f"Elapsed: {elapsed}")
    print("-"*70)
    
    # Get file counts
    doi_files = get_file_list(DOI_DIR, '.txt')
    data_section_files = get_file_list(DATA_SECTION_DIR, '.txt')
    ready_for_llm_files = get_file_list(READY_FOR_LLM_DIR, '.txt')
    llm_output_files = get_file_list(LLM_OUTPUT_DIR, '.json')
    
    # Count actual DOIs (not just files)
    actual_doi_count = count_dois_in_files(doi_files)
    
    # Print component status
    print("Component Status:")
    print("-"*70)
    print(f"DOI Extraction:      {pipeline_state['doi_extraction']['status']} ({pipeline_state['doi_extraction']['count']} DOIs)")
    print(f"Data Section:        {pipeline_state['data_section']['status']} ({pipeline_state['data_section']['count']} items)")
    print(f"LLM Extraction:      {pipeline_state['llm_extraction']['status']} ({pipeline_state['llm_extraction']['count']} items)")
    print(f"Evaluation:          {pipeline_state['evaluation']['status']}")
    print("-"*70)
    
    print("File Counts:")
    print("-"*70)
    print(f"DOI Files:           {len(doi_files)} files containing {actual_doi_count} DOIs")
    print(f"Data Sections:       {len(data_section_files)}")
    print(f"Ready for LLM:       {len(ready_for_llm_files)}")
    print(f"LLM Results:         {len(llm_output_files)}")
    print("="*70)
    
    # Check for discrepancies
    if actual_doi_count != pipeline_state['doi_extraction']['count']:
        print(f"Warning: DOI count mismatch. State: {pipeline_state['doi_extraction']['count']}, Actual: {actual_doi_count}")
    
    if len(data_section_files) != pipeline_state['data_section']['count']:
        print(f"Warning: Data section count mismatch. State: {pipeline_state['data_section']['count']}, Files: {len(data_section_files)}")
    
    if len(llm_output_files) != pipeline_state['llm_extraction']['count']:
        print(f"Warning: LLM output count mismatch. State: {pipeline_state['llm_extraction']['count']}, Files: {len(llm_output_files)}")
    
    print("\n")

def signal_handler(sig, frame):
    """Handle interrupt signals."""
    logger.info(f"Received signal {sig}. Shutting down...")
    stop_event.set()

def main():
    """Main entry point for the pipeline."""
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    args = parse_arguments()
    
    # Initialize pipeline
    pipeline_state = init_pipeline()
    pipeline_state['mode'] = args.mode
    save_state(PIPELINE_STATE, pipeline_state)
    
    try:
        if args.mode == 'stats':
            # Display pipeline statistics
            display_pipeline_stats()
            
        elif args.mode == 'rebuild_state':
            # Rebuild pipeline state from existing files
            rebuild_pipeline_state()
            
        elif args.mode == 'doi_extraction':
            # Run DOI extraction only
            run_doi_extraction(args)
            
        elif args.mode == 'data_section':
            # Run data section extraction only
            run_data_section_extraction(args)
            
        elif args.mode == 'llm_extraction':
            # Run LLM extraction only
            run_llm_extraction(args)
            
        elif args.mode == 'evaluate':
            # Run evaluation only
            run_evaluation(args)
            
        elif args.mode == 'full':
            # Run full pipeline sequentially
            logger.info("Starting full pipeline execution...")
            dois = run_doi_extraction(args)
            data_sections = run_data_section_extraction(args, dois)
            llm_results = run_llm_extraction(args, data_sections)
            eval_results = run_evaluation(args)
            
            # Update final pipeline state
            pipeline_state = load_state(PIPELINE_STATE)
            pipeline_state['status'] = 'completed'
            pipeline_state['end_time'] = datetime.now().isoformat()
            save_state(PIPELINE_STATE, pipeline_state)
            
            logger.info("Full pipeline completed.")
            
        elif args.mode == 'parallel':
            # Run pipeline with parallel processing
            run_parallel_pipeline(args)
            
        elif args.mode == 'resume':
            # Resume pipeline execution sequentially
            logger.info("Resuming pipeline execution...")
            
            # Check pipeline state
            if pipeline_state['doi_extraction']['status'] != 'completed':
                run_doi_extraction(args)
            else:
                logger.info("DOI extraction already completed, skipping...")
            
            if pipeline_state['data_section']['status'] != 'completed':
                run_data_section_extraction(args)
            else:
                logger.info("Data section extraction already completed, skipping...")
            
            if pipeline_state['llm_extraction']['status'] != 'completed':
                run_llm_extraction(args)
            else:
                logger.info("LLM extraction already completed, skipping...")
            
            if pipeline_state['evaluation']['status'] != 'completed':
                run_evaluation(args)
            else:
                logger.info("Evaluation already completed, skipping...")
            
            # Update final pipeline state
            pipeline_state = load_state(PIPELINE_STATE)
            pipeline_state['status'] = 'completed'
            pipeline_state['end_time'] = datetime.now().isoformat()
            save_state(PIPELINE_STATE, pipeline_state)
            
            logger.info("Pipeline resume completed.")
            
        elif args.mode == 'resume_parallel':
            # Resume pipeline with parallel processing
            run_parallel_pipeline(args, resume=True)
            
        else:
            logger.error(f"Unknown mode: {args.mode}")
    
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user.")
        # Update pipeline state
        pipeline_state = load_state(PIPELINE_STATE)
        pipeline_state['status'] = 'interrupted'
        pipeline_state['end_time'] = datetime.now().isoformat()
        save_state(PIPELINE_STATE, pipeline_state)
    
    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}", exc_info=True)
        # Update pipeline state
        pipeline_state = load_state(PIPELINE_STATE)
        pipeline_state['status'] = 'error'
        pipeline_state['error'] = str(e)
        pipeline_state['end_time'] = datetime.now().isoformat()
        save_state(PIPELINE_STATE, pipeline_state)

if __name__ == "__main__":
    main()