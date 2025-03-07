#!/usr/bin/env python3
"""
Statistics utility for the research data extraction pipeline
Provides real-time progress monitoring and calculation of metrics
"""

import os
import json
import time
from datetime import datetime, timedelta
import logging
from tabulate import tabulate
import math
from utils.file_utils import get_file_list, load_state

logger = logging.getLogger('stats')

def calculate_completion_rate(count, total_time_seconds):
    """Calculate items per minute rate."""
    if total_time_seconds <= 0:
        return 0
    
    # Convert to items per minute
    return (count / total_time_seconds) * 60

def estimate_completion_time(items_remaining, rate_per_minute):
    """Estimate time to completion based on current rate."""
    if rate_per_minute <= 0:
        return "Unknown"
    
    # Calculate minutes remaining
    minutes_remaining = items_remaining / rate_per_minute
    
    # Convert to hours and minutes
    hours = int(minutes_remaining // 60)
    mins = int(minutes_remaining % 60)
    
    if hours > 24:
        days = hours // 24
        hours = hours % 24
        return f"{days}d {hours}h {mins}m"
    elif hours > 0:
        return f"{hours}h {mins}m"
    else:
        return f"{mins}m"

def get_component_stats(state_file, output_dir, component_name):
    """Get statistics for a pipeline component."""
    stats = {
        'name': component_name,
        'status': 'Unknown',
        'count': 0,
        'total': 0,
        'completion': 0,
        'start_time': None,
        'end_time': None,
        'duration': None,
        'rate': 0,
        'estimate': 'Unknown'
    }
    
    # Load state file
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
            
            if component_name in state:
                component = state[component_name]
                stats['status'] = component.get('status', 'Unknown')
                stats['count'] = component.get('count', 0)
            
            # Get timestamps
            if 'start_time' in state:
                stats['start_time'] = datetime.fromisoformat(state['start_time'])
            
            if 'end_time' in state:
                stats['end_time'] = datetime.fromisoformat(state['end_time'])
            elif stats['start_time']:
                # If running, end time is now
                stats['end_time'] = datetime.now()
            
            # Calculate duration
            if stats['start_time'] and stats['end_time']:
                duration = (stats['end_time'] - stats['start_time']).total_seconds()
                hours = int(duration // 3600)
                minutes = int((duration % 3600) // 60)
                seconds = int(duration % 60)
                stats['duration'] = f"{hours}h {minutes}m {seconds}s"
            
            # Calculate rate
            if stats['count'] > 0 and stats['start_time'] and stats['end_time']:
                duration_seconds = (stats['end_time'] - stats['start_time']).total_seconds()
                if duration_seconds > 0:
                    stats['rate'] = calculate_completion_rate(stats['count'], duration_seconds)
            
        except Exception as e:
            logger.error(f"Error loading state file {state_file}: {str(e)}")
    
    # Count files in output directory
    component_dir = os.path.join(output_dir, component_name.replace('_', '_'))
    if os.path.exists(component_dir):
        extension = '.txt' if component_name == 'data_section' else '.json' if component_name == 'llm_extraction' else '.txt'
        files = get_file_list(component_dir, extension)
        stats['count'] = len(files)
    
    # If pipeline state has DOI total, use it for completion percentage
    if component_name != 'doi_extraction' and os.path.exists(os.path.join(os.path.dirname(state_file), 'pipeline_state.json')):
        try:
            with open(os.path.join(os.path.dirname(state_file), 'pipeline_state.json'), 'r') as f:
                pipeline_state = json.load(f)
                if 'doi_extraction' in pipeline_state and 'count' in pipeline_state['doi_extraction']:
                    stats['total'] = pipeline_state['doi_extraction']['count']
                    if stats['total'] > 0:
                        stats['completion'] = (stats['count'] / stats['total']) * 100
        except Exception as e:
            logger.error(f"Error loading pipeline state: {str(e)}")
    
    # Estimate remaining time
    if stats['rate'] > 0 and stats['total'] > 0 and stats['status'] == 'running':
        remaining = stats['total'] - stats['count']
        stats['estimate'] = estimate_completion_time(remaining, stats['rate'])
    
    return stats

def get_pipeline_progress(state_dir, output_dir):
    """Get overall pipeline progress."""
    pipeline_state_file = os.path.join(state_dir, 'pipeline_state.json')
    
    progress = {
        'status': 'Unknown',
        'components': {},
        'start_time': None,
        'current_time': datetime.now(),
        'elapsed': None,
        'mode': None
    }
    
    # Load pipeline state
    if os.path.exists(pipeline_state_file):
        try:
            with open(pipeline_state_file, 'r') as f:
                state = json.load(f)
            
            progress['status'] = state.get('status', 'Unknown')
            progress['mode'] = state.get('mode', 'Unknown')
            
            if 'start_time' in state:
                progress['start_time'] = datetime.fromisoformat(state['start_time'])
                
                # Calculate elapsed time
                elapsed_seconds = (progress['current_time'] - progress['start_time']).total_seconds()
                hours = int(elapsed_seconds // 3600)
                minutes = int((elapsed_seconds % 3600) // 60)
                seconds = int(elapsed_seconds % 60)
                progress['elapsed'] = f"{hours}h {minutes}m {seconds}s"
        
        except Exception as e:
            logger.error(f"Error loading pipeline state: {str(e)}")
    
    # Get component stats
    components = ['doi_extraction', 'data_section', 'llm_extraction', 'evaluation']
    for component in components:
        component_state_file = os.path.join(state_dir, f'{component}.json')
        progress['components'][component] = get_component_stats(pipeline_state_file, output_dir, component)
    
    return progress

def display_progress_bar(completion, width=50):
    """Display a text-based progress bar."""
    filled_width = int(width * completion / 100)
    bar = '█' * filled_width + '░' * (width - filled_width)
    return f"[{bar}] {completion:.1f}%"

def display_pipeline_stats(state_dir, output_dir):
    """Display pipeline statistics."""
    progress = get_pipeline_progress(state_dir, output_dir)
    
    # Print header
    print("\n" + "="*80)
    print(f"RESEARCH DATA EXTRACTION PIPELINE - {progress['status'].upper()}")
    print("="*80)
    
    # Print overall information
    print(f"Mode: {progress['mode']}")
    if progress['start_time']:
        print(f"Started: {progress['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Elapsed: {progress['elapsed'] if progress['elapsed'] else 'Unknown'}")
    print("-"*80)
    
    # Prepare table data
    table_data = []
    for name, stats in progress['components'].items():
        # Format rate with proper units
        rate_str = f"{stats['rate']:.1f} items/min" if stats['rate'] > 0 else "N/A"
        
        # Format progress bar and percentage
        if stats['total'] > 0:
            progress_bar = display_progress_bar(stats['completion'])
            completion_str = f"{progress_bar}"
        else:
            completion_str = "N/A"
        
        # Format count with total if available
        if stats['total'] > 0:
            count_str = f"{stats['count']} / {stats['total']}"
        else:
            count_str = f"{stats['count']}"
        
        table_data.append([
            name.replace('_', ' ').title(),
            stats['status'],
            count_str,
            rate_str,
            stats['estimate'],
            completion_str
        ])
    
    # Print table
    headers = ["Component", "Status", "Count", "Rate", "Est. Remaining", "Progress"]
    print(tabulate(table_data, headers=headers, tablefmt="simple"))
    print("-"*80)
    
    # Print recent activity
    print("\nRecent Activity:")
    for name, stats in progress['components'].items():
        if stats['status'] == 'running':
            component_dir = os.path.join(output_dir, name.replace('_', '_'))
            if os.path.exists(component_dir):
                extension = '.txt' if name == 'data_section' else '.json' if name == 'llm_extraction' else '.txt'
                files = get_file_list(component_dir, extension)
                if files:
                    # Sort by modification time (newest first)
                    files.sort(key=os.path.getmtime, reverse=True)
                    
                    # Display 5 most recent files
                    print(f"\n{name.replace('_', ' ').title()} recent files:")
                    for i, file in enumerate(files[:5]):
                        mtime = datetime.fromtimestamp(os.path.getmtime(file))
                        print(f"  - {os.path.basename(file)} ({mtime.strftime('%H:%M:%S')})")
    
    print("\n" + "="*80)

def monitor_pipeline(state_dir, output_dir, refresh_interval=5):
    """Monitor pipeline progress in real-time."""
    try:
        while True:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display stats
            display_pipeline_stats(state_dir, output_dir)
            
            # Check if pipeline is complete
            progress = get_pipeline_progress(state_dir, output_dir)
            if progress['status'] in ['completed', 'error']:
                print("\nPipeline has finished. Press Ctrl+C to exit.")
            
            # Wait for refresh interval
            time.sleep(refresh_interval)
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    # If run directly, display pipeline stats
    STATE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pipeline_state')
    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Start monitoring
    monitor_pipeline(STATE_DIR, OUTPUT_DIR)