"""
LLM Extraction Module

This module handles the extraction of accession codes, scripts, and analysis data
from publication data sections using Large Language Models.
"""

import os
import json
import time
import logging
import concurrent.futures
from datetime import datetime
from config import settings
try:
    from llama_index.core.agent import ReActAgent
    from llama_index.llms.ollama import Ollama
    from llama_index.core.tools import FunctionTool
    from llama_index.core import PromptTemplate
    LLAMA_INDEX_AVAILABLE = True
except ImportError:
    LLAMA_INDEX_AVAILABLE = False

# Configure logging
logger = logging.getLogger('llm_extraction')

# Default settings if not imported from config
LLM_MODEL = settings.LLM_MODEL
LLM_TEMPERATURE = settings.LLM_TEMPERATURE 
LLM_MAX_RETRIES = settings.LLM_MAX_RETRIES
LLM_MAX_ITERATIONS = settings.LLM_MAX_ITERATIONS
LLM_MAX_EXECUTION_TIME = settings.LLM_MAX_EXECUTION_TIME


def get_llm(model=None):
    """
    Get LLM instance.
    
    Args:
        model (str, optional): Model name. Defaults to None.
        
    Returns:
        Ollama: LLM instance.
    """
    if not LLAMA_INDEX_AVAILABLE:
        logger.error("llama_index not available. Please install with: pip install llama-index")
        return None
    
    if model is None:
        model = LLM_MODEL
    
    logger.info(f"Initializing LLM with model: {model}")
    
    try:
        return Ollama(
            model=model,
            temperature=LLM_TEMPERATURE
        )
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        return None


def extract_data(text):
    """
    Extract source code URLs, analysis data URLs, and accession codes from scientific text.
    
    Args:
        text (str): Scientific text to extract from.
        
    Returns:
        dict: Extracted data.
    """
    logger.info("Extracting data with LLM")
    
    prompt = f"""
        You are a highly precise extraction tool. I will provide you with a scientific text and you have to extract source code and analysis data URLs, and accession codes for sequencing data from it.
        Your task:
        1. Extract **only** explicitly stated sequencing data accession codes. Do **not** infer or guess accession codes if they are not explicitly mentioned in the text. Do **not** add snippets of Zenodo URLs.
        2. Identify **all** analysis data URLs. Analysis data URLs are on different hosting services where data in the field of Bioinformatics is uploaded. The analysis data can be of different forms: processed data, raw sequencing data, tools for analysis, metadata, objects related to analysis. Do **not** include generic URLs that do not point to the specific webpage where data is uploaded like "https://brain-vasc.cells.ucsc.edu".
        3. Identify source code URLs **only** found on Github, Gitlab or Bitbucket. Source code URLs are those where custom code, custom scripts or analysis scripts are uploaded.

        Return the results **only** in valid JSON format, with no additional text or explanation. Do **not** include any introductory or closing statements.

        The returned JSON should strictly follow the following format:
        {{
            "accession_codes": ["accession_code_1", "accession_code_2"],
            "scripts": ["GitHub_URL_1", "Gitlab_URL_2"],
            "analysis_data": ["analysis_data_URL1", "analysis_data_URL2"]
        }}

        Example Input:
        <<DATA>> Raw sequencing data were deposited at the GEO under accession numbers GSE12345 and GSE67890 and syn12345. Sequencing data is available on Zenodo at https://zenodo.org/record/12345 and https://doi.org/10.1010/zenodo.1234567. 
        Additional analysis scripts are hosted on Zenodo at https://zenodo.org/record/67890 and GitHub at https://github.com/example/repo. The following open-source code and databases were used in this article: JaBbA (v.1.1) (https://github.com/mskilab/JaBbA), 
        gGnome (commit c390d80) (https://github.com/mskilab/gGnome), AmpliconArchitect (https://github.com/virajbdeshpande/AmpliconArchitect). High-throughput sequencing (HTS) of T cell receptor β (TRB) and T cell receptor ⍺ (TRA) dataset are available from Adaptive Biotechnologies (http://clients.adaptivebiotech.com/login). Custom code is available on GitHub at https://gitlab.com/xyz/repo." <<END DATA>>

        Example Output:
        {{
            "accession_codes": [
                "GSE12345",
                "GSE67890",
                "syn12345"
            ],
            "scripts": [
                "https://github.com/example/repo",
                "https://gitlab.com/xyz/repo"
            ],
            "analysis_data": [
                "https://zenodo.org/record/12345",
                "https://doi.org/10.1010/zenodo.1234567",
                "https://zenodo.org/record/67890",
            ]
        }}

        Strict Rules:
        1. accession_codes: Include ONLY valid formats:
            - ONLY include accession codes that are found in the text
            - Do NOT infer or make up accession codes
            - No snippets of Zenodo URL should be added
            - If no accession codes are available, leave the "accession_codes" section empty: "accession_codes": [].

        2. scripts: Include ONLY:
            - Github, Gitlab or Bitbucket URLs with code/scripts
            - Do **NOT** add any database/software/tool repositories
            - If no source code URLs are available, leave the "scripts" section empty: "scripts": [].

        3. analysis_data: Include URLs related to analysis:
            - ONLY include analysis data URLs that are explicitly stated in the input text
            - If no analysis data URLs are available, leave the "analysis_data" section empty: "analysis_data": [].

        4. If there is no input text then return JSON:
        {{
            "accession_codes": [],
            "scripts": [],
            "analysis_data": []
        }}

        Input Text to Process:
        <<DATA>> {text} <<END DATA>>
        """

    try:
        llm = get_llm()
        if not llm:
            return empty_result()
            
        logger.info("Sending request to LLM")
        
        response = llm.complete(prompt).text.strip()
        
        # Try to parse the response as JSON
        try:
            result = json.loads(response)
            logger.info("Successfully parsed LLM response as JSON")
            
            # Validate structure
            if not isinstance(result.get('accession_codes', []), list):
                raise ValueError("accession_codes must be a list")
            if not isinstance(result.get('scripts', []), list):
                raise ValueError("scripts must be a list")
            if not isinstance(result.get('analysis_data', []), list):
                raise ValueError("analysis_data must be a list")
                
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Raw response: {response}")
            
            # Return empty result on parsing error
            return empty_result()
        
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        return empty_result()


def empty_result():
    """Return an empty result dictionary."""
    return {
        "accession_codes": [],
        "scripts": [],
        "analysis_data": []
    }


def review_data(text, extracted_data):
    """
    Validate extracted data against the original text.
    
    Args:
        text (str): Original text.
        extracted_data (dict): Extracted data to validate.
        
    Returns:
        dict: Validation results.
    """
    logger.info("Validating extracted data with LLM")
    
    # Convert extracted_data to string if it's a dict
    if isinstance(extracted_data, dict):
        extracted_data = json.dumps(extracted_data)
    
    prompt = f"""You are a validation tool. Return EXACTLY and ONLY a JSON object matching this structure - NO additional text or explanation:

        {{
            "is_valid": true,
            "validation":
            {{
                "accession_codes": {{
                    "valid_count": 0,
                    "invalid_count": 0
                }},
                "scripts": {{
                    "valid_count": 0,
                    "invalid_count": 0
                }},
                "analysis_data": {{
                    "valid_count": 0,
                    "invalid_count": 0
                }}
            }}
        }}

        Validation Rules:
        1. Return ONLY the JSON - no text before or after
        2. Scripts is **ONLY** GitHub, Bitlab or Bitbucket URLs.
        3. Results should **NOT** include "GSE12345", "GSE67890", "syn12345" in accession_codes, or "https://zenodo.org/record/12345", "https://doi.org/10.1010/zenodo.1234567", "http://clients.adaptivebiotech.com/login", "https://zenodo.org/record/67890" in analysis_data, or "https://github.com/example/repo", "https://github.com/mskilab/JaBbA", "https://github.com/mskilab/gGnome", "https://github.com/virajbdeshpande/AmpliconArchitect", "http://clients.adaptivebiotech.com/login", "https://gitlab.com/xyz/repo" in scripts"
        4. NO URLs should be in the extracted_data that are not explicitly stated in text.
        5. NO generic URLs should be added (e.g. "http://bigd.big.ac.cn/"), there should be URLs that point to a specific webpage where the data is uploaded.
        6. analysis_data should **NOT** contain Github, Gitlab or Bitbucket URLs.
        7. analysis_data should only contain URLs and not textual sentences.
        8. accession_codes should **not** contain name of the database like GEO, only accession code should be present.
        8. **NO** duplication in any category.

        Strict rules:
        - Do **NOT** add anything to the output that is not explicitly mentioned in the input text.
        
        Input Text to validate against:
        {text}

        Extracted data to validate:
        {extracted_data}

        Return the results **only** in valid JSON format with **no additional text**. Follow this format exactly:
        {{
            "accession_codes": [],
            "scripts": [],
            "analysis_data": []
        }}
    """

    try:
        llm = get_llm()
        if not llm:
            return invalid_validation_result()
            
        logger.info("Sending validation request to LLM")
        
        response = llm.complete(prompt).text.strip()
        
        # Remove any markdown code blocks if present
        response = response.replace('```json', '').replace('```', '').strip()
        
        # Try to parse the response as JSON
        try:
            result = json.loads(response)
            logger.info("Successfully parsed validation response as JSON")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse validation response as JSON: {e}")
            logger.error(f"Raw response: {response}")
            
            # Return empty result on parsing error
            return invalid_validation_result()
        
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return invalid_validation_result()


def invalid_validation_result():
    """Return a default validation result for error cases."""
    return {
        "is_valid": False,
        "validation": {
            "accession_codes": {
                "valid_count": 0,
                "invalid_count": 0,
                "invalid_items": []
            },
            "scripts": {
                "valid_count": 0,
                "invalid_count": 0,
                "invalid_items": []
            },
            "analysis_data": {
                "valid_count": 0,
                "invalid_count": 0,
                "invalid_items": []
            }
        },
        "error_messages": ["Failed to validate extraction"]
    }


def setup_extraction_agent():
    """
    Set up a ReActAgent for data extraction.
    
    Returns:
        ReActAgent: Configured agent.
    """
    if not LLAMA_INDEX_AVAILABLE:
        logger.error("llama_index not available. Please install with: pip install llama-index")
        return None
    
    logger.info("Setting up extraction agent")
    
    try:
        # Define extraction tool
        extract_tool = FunctionTool.from_defaults(
            fn=extract_data,
            name="extract_data",
            description="Extracts source code URLs, analysis data URLs and accession codes from scientific text"
        )

        # Define review tool
        review_tool = FunctionTool.from_defaults(
            fn=review_data,
            name="review_data",
            description="Validates extracted data against the original text"
        )

        # Define system prompt
        system_prompt = """You are designed to extract and validate source code URLs, analysis data URLs, and accession codes from scientific text.

        ## Tools
        You have access to these tools:
        {tool_desc}

        ## Process
        1. extract data using extract_data
        2. validate using review_data
        3. If validation fails, try extract_data again

        ## Output Format
        Please use this format:

        ```
        Thought: I need to [action] because [reason]
        Action: tool name
        Action Input: {{"text": "input text"}}
        ```

        Please ALWAYS start with a Thought and please ALWAYS pass extracted_data to review_tool only and NOT to extract_data.

        Return **ONLY** the JSON object with no additional text before or after the JSON object.

        If this format is used, the user will respond in the following format:

        ```
        Observation: tool response
        ```

        You should keep repeating the above format until you have all the extracted information. At that point, you MUST respond
        in the the following format:

        ```
        Thought: I can answer without using any more tools.
        Answer: [your answer here in JSON format]
        ```

        When validation is successful:
        Thought: Extraction and validation complete
        Answer: [final extracted and validated data]

        ## Current Conversation
        Below is the current conversation consisting of interleaving human and assistant messages.
        """

        # Get LLM instance
        llm = get_llm()
        if not llm:
            return None

        # Create agent
        agent = ReActAgent.from_tools(
            [extract_tool, review_tool],
            llm=llm,
            verbose=True,
            max_retries=LLM_MAX_RETRIES,
            max_iterations=LLM_MAX_ITERATIONS,
            max_execution_time=LLM_MAX_EXECUTION_TIME
        )

        # Set custom system prompt
        react_system_prompt = PromptTemplate(system_prompt)
        agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})

        return agent
    
    except Exception as e:
        logger.error(f"Error setting up extraction agent: {str(e)}")
        return None


def extract_with_llm(text):
    """
    Extract data from text using LLM.
    
    Args:
        text (str): Text to extract from.
        
    Returns:
        dict: Extracted data.
    """
    # Check if text is provided
    if not text or (isinstance(text, str) and not text.strip()):
        logger.warning("Empty text provided for extraction")
        return empty_result()
    
    # Simple extraction for short text
    if isinstance(text, str) and len(text) < 1000:
        logger.info("Using simple extraction for short text")
        return extract_data(text)
    
    # Use ReAct agent for complex extraction
    try:
        # If llama_index is not available, fall back to simple extraction
        if not LLAMA_INDEX_AVAILABLE:
            logger.warning("llama_index not available, falling back to simple extraction")
            return extract_data(text)
        
        logger.info("Using ReAct agent for complex extraction")
        agent = setup_extraction_agent()
        
        if not agent:
            logger.warning("Failed to set up extraction agent, falling back to simple extraction")
            return extract_data(text)
        
        response = agent.chat(text)
        
        # Reset agent to free resources
        agent.reset()
        
        # Parse response
        try:
            result = json.loads(response.response)
            return result
        except json.JSONDecodeError:
            logger.warning("Failed to parse agent response as JSON, using fallback extraction")
            return extract_data(text)
        
    except Exception as e:
        logger.error(f"Error in ReAct agent: {e}")
        logger.info("Falling back to simple extraction")
        return extract_data(text)


def extract_with_llm_batch(data_sections):
    """
    Extract data from multiple data sections.
    
    Args:
        data_sections (list): List of data section dictionaries.
        
    Returns:
        list: List of extraction results.
    """
    results = []
    
    for data_section in data_sections:
        # Handle both string data sections and dictionary data sections
        if isinstance(data_section, dict):
            doi_url = data_section.get("DOI")
            paragraph = data_section.get("paragraph")
            pmid = data_section.get("PubMed_ID")
        else:
            # Assume it's a file path
            try:
                with open(data_section, 'r') as f:
                    content = f.read()
                
                # Try to parse as JSON
                try:
                    data = json.loads(content)
                    doi_url = data.get("DOI")
                    paragraph = data.get("paragraph")
                    pmid = data.get("PubMed_ID")
                except json.JSONDecodeError:
                    # If not JSON, treat the whole content as paragraph
                    doi_url = os.path.basename(data_section)
                    paragraph = content
                    pmid = None
            except Exception as e:
                logger.error(f"Error reading file {data_section}: {str(e)}")
                continue
        
        if paragraph:
            # Extract data
            extraction_result = extract_with_llm(paragraph)
            
            # Add metadata
            result = {
                "DOI": doi_url,
                "PubMed_ID": pmid,
                "results": extraction_result
            }
            
            results.append(result)
    
    return results


def load_data_section(file_path):
    """
    Load data section from file.
    
    Args:
        file_path (str): Path to data section file.
    
    Returns:
        dict: Data section content.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Try to parse as JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # If not JSON, create a minimal structure
            return {
                "DOI": os.path.basename(file_path).replace('.txt', ''),
                "paragraph": content,
                "PubMed_ID": None
            }
    except Exception as e:
        logger.error(f"Error loading data section from {file_path}: {str(e)}")
        return None


def process_data_section(file_path, output_dir):
    """
    Process a single data section.
    
    Args:
        file_path (str): Path to data section file.
        output_dir (str): Directory to save results.
    
    Returns:
        str: Path to output file.
    """
    # Get the DOI or file basename to use as output filename
    doi_id = os.path.basename(file_path).replace('.txt', '')
    output_file = os.path.join(output_dir, f"{doi_id}.json")
    
    # Skip if output already exists
    if os.path.exists(output_file):
        logger.info(f"Output already exists for {doi_id}, skipping")
        return output_file
    
    try:
        # Load data section
        data_section = load_data_section(file_path)
        if not data_section:
            logger.error(f"Failed to load data section from {file_path}")
            return None
        
        # Extract data
        paragraph = data_section.get("paragraph", "")
        result = extract_with_llm(paragraph)
        
        # Create output structure
        output = {
            "DOI": data_section.get("DOI", doi_id),
            "PubMed_ID": data_section.get("PubMed_ID"),
            "extraction_time": datetime.now().isoformat(),
            "results": result
        }
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"Processed {doi_id} and saved to {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error processing data section {file_path}: {str(e)}")
        return None


def process_batch(batch, output_dir, start_time=None):
    """
    Process a batch of data sections.
    
    Args:
        batch (list): List of data section file paths.
        output_dir (str): Directory to save results.
        start_time (float, optional): Start time for progress tracking.
    
    Returns:
        list: List of processed output file paths.
    """
    processed_files = []
    
    for i, file_path in enumerate(batch):
        if start_time:
            # Calculate and display progress
            elapsed = time.time() - start_time
            files_per_second = (i + 1) / elapsed if elapsed > 0 else 0
            remaining = (len(batch) - i - 1) / files_per_second if files_per_second > 0 else 0
            
            logger.info(f"Processing {i+1}/{len(batch)} - {files_per_second:.2f} files/sec, "
                       f"est. remaining: {int(remaining//60)}m {int(remaining%60)}s")
        
        output_file = process_data_section(file_path, output_dir)
        if output_file:
            processed_files.append(output_file)
    
    return processed_files


def process_with_llm(data_sections, output_dir, workers=2, batch_size=50):
    """
    Process multiple data sections with parallel execution.
    
    Args:
        data_sections (list): List of data section file paths.
        output_dir (str): Directory to save results.
        workers (int, optional): Number of worker threads. Defaults to 2.
        batch_size (int, optional): Size of batches for processing. Defaults to 50.
    
    Returns:
        list: List of processed output file paths.
    """
    logger.info(f"Processing {len(data_sections)} data sections with {workers} workers")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Track start time for progress estimation
    start_time = time.time()
    
    # Process all data sections
    processed_files = []
    
    if workers <= 1:
        # Sequential processing
        processed_files = process_batch(data_sections, output_dir, start_time)
    else:
        # Process in batches with parallel execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # Create batches
            batches = [data_sections[i:i+batch_size] for i in range(0, len(data_sections), batch_size)]
            
            # Submit batches to executor
            futures = []
            for batch in batches:
                future = executor.submit(process_batch, batch, output_dir)
                futures.append(future)
            
            # Collect results
            for future in concurrent.futures.as_completed(futures):
                try:
                    batch_results = future.result()
                    processed_files.extend(batch_results)
                    logger.info(f"Completed batch, {len(processed_files)}/{len(data_sections)} total")
                except Exception as e:
                    logger.error(f"Error processing batch: {str(e)}")
    
    # Calculate statistics
    elapsed = time.time() - start_time
    files_per_second = len(processed_files) / elapsed if elapsed > 0 else 0
    
    logger.info(f"Completed processing {len(processed_files)} data sections in {elapsed:.2f} seconds "
               f"({files_per_second:.2f} files/sec)")
    
    return processed_files


if __name__ == "__main__":
    # If script is run directly, for testing
    import sys
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
        if os.path.isfile(input_file):
            # If input is a file
            data_section = load_data_section(input_file)
            if data_section:
                result = extract_with_llm(data_section.get("paragraph", ""))
                print(json.dumps(result, indent=2))
        else:
            # If input is a text string
            result = extract_with_llm(input_file)
            print(json.dumps(result, indent=2))
    else:
        print("Usage: python llm_extraction.py <input_file_or_text>")