import logging
from typing import Dict, Any
from llama_index.core.agent import ReActAgent
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import FunctionTool
from llama_index.core import PromptTemplate
import json
import time
import os

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

def get_shared_llm_llama():
    """Returns a shared LLM instance of Llama3.1:8b"""
    return Ollama(
        model="llama3.1:8b", 
        temperature=0
    )

def get_shared_llm_deepseek():
    """Returns a shared LLM instance of deepseek-r1"""
    return Ollama(
        model="deepseek-r1:8b", 
        temperature=0
    )


def extract_data(text: str) -> str:
    """Extracts source code URLs and accession codes from scientific text."""
    
    prompt = f"""
        You are a highly precise extraction tool. I will provide you with a scientific text and you have to extract source code and analysis data URLs, and accession codes for sequencing data from it.
        Your task:
        1. Extract **only** explicitly stated sequencing data accession codes and their respective database names (e.g., GEO, ENA, SRA, etc.). Do **not** infer or guess accession codes if they are not explicitly mentioned in the text.
        2. Identify **all** sequencing data URLs, including URLs from **Zenodo**. For Zenodo, include any URL explicitly mentioned. Sequencing data URLs are of hosting services where sequencing data in the field of Bioinformatics is uploaded.
        3. Identify **all** source code URLs, including URLs from **GitHub** and **Zenodo**. Source code URLs are those where custom code or custom scripts are uploaded.

        Return the results **only** in valid JSON format, with no additional text or explanation. Do **not** include any introductory or closing statements.

        The returned JSON should strictly follow the following format:
        {{
            "accession_codes": {{
                "database_name_1": ["accession_code_1", "accession_code_2"],
                "database_name_2": ["accession_code_3"]
            }},
            "sequencing_data": ["sequencing_data_URL1", "sequencing_data_URL2"],
            "source_code": ["GitHub_URL", "Zenodo_URL"]
        }}

        Example Input:
        <<DATA>> Raw sequencing data were deposited at the GEO under accession numbers GSE12345 and GSE67890. Sequencing data is available on Zenodo at https://zenodo.org/record/12345 and https://doi.org/10.1010/zenodo.1234567. 
        Additional analysis scripts are hosted on Zenodo at https://zenodo.org/record/67890 and GitHub at https://github.com/example/repo. The following open-source code and databases were used in this article: JaBbA (v.1.1) (https://github.com/mskilab/JaBbA), 
        gGnome (commit c390d80) (https://github.com/mskilab/gGnome), AmpliconArchitect (https://github.com/virajbdeshpande/AmpliconArchitect). High-throughput sequencing (HTS) of T cell receptor β (TRB) and T cell receptor ⍺ (TRA) dataset are available from Adaptive Biotechnologies (http://clients.adaptivebiotech.com/login) <<END DATA>>

        Example Output:
        {{
            "accession_codes": {{
                "GEO": ["GSE12345", "GSE67890"]
            }},
            "sequencing_data": [
                "https://zenodo.org/record/12345",
                "https://doi.org/10.1010/zenodo.1234567",
                "http://clients.adaptivebiotech.com/login"
            ],
            "source_code": [
                "https://github.com/example/repo",
                "https://zenodo.org/record/67890"
            ]
        }}

        Strict Rules:
        1. accession_codes: Include ONLY valid formats:
            - Accession codes must strictly follow common formats (e.g., GSE followed by numbers for GEO, PRJ followed by alphanumeric strings for SRA, etc.)
            - ONLY include accession codes that match valid formats
            - If no accession codes are available, leave the "accession codes" section empty: "accession_codes": {{}}.

        2. sequencing_data: Include URLs for databases:
            - ONLY include sequencing data URLs that are explicitly stated in the input text
            - If no sequencing data URLs are available, leave the "sequencing data" section empty: "sequencing_data": [].

        3. source_code: Include ONLY:
        - Github URLs with code/scripts
        - Zenodo URLs with code/scripts
        - Do **NOT** add any database/software/tool repositories
        - If no source code URLs are available, leave the "source code" section empty: "source_code": [].

        - ONLY return the JSON structure as shown, with **no additional text or explanation**.

        Input Text to Process:
        <<DATA>> {text} <<END DATA>>
        """
    try:
        llm=get_shared_llm_llama()
        response = llm.complete(prompt).text.strip()
        result = json.loads(response)
        # logger.info(result)
        
        # Validate structure
        if not isinstance(result.get('accession_codes', {}), dict):
            raise ValueError("accession_codes must be a dictionary")
        if not isinstance(result.get('sequencing_data', []), list):
            raise ValueError("sequencing_data must be a list")
        if not isinstance(result.get('source_code', []), list):
            raise ValueError("source_code must be a list")
            
        # logger.info(f"Extraction result: {result}")
        return json.dumps(result)
        
    except Exception as e:
        # logger.error(f"Extraction error: {e}")
        return json.dumps({
            "accession_codes": {},
            "sequencing_data": [],
            "source_code": []
        })



def review_data(text: str, extracted_data: str) -> str:
    """Validates extracted data against the original text."""

    prompt = f"""You are a validation tool. Return EXACTLY and ONLY a JSON object matching this structure - NO additional text or explanation:

        {{
            "is_valid": true,
            "validation":
            {{
                "accession_codes": {{
                    "valid_count": 0,
                    "invalid_count": 0
                }},

                "source_code": {{
                    "valid_count": 0,
                    "invalid_count": 0
                }},
                "sequencing_data": {{
                    "valid_count": 0,
                    "invalid_count": 0
                }}
            }}
        }}

        Validation Rules:
        1. Return ONLY the JSON - no text before or after
        2. Source code is **ONLY** GitHub/Zenodo URLs.
        3. Results should not include "GSE12345", "GSE67890" in accession_codes, or "https://zenodo.org/record/12345", "https://doi.org/10.1010/zenodo.1234567", "http://clients.adaptivebiotech.com/login" in sequencing_data, or "https://github.com/example/repo", or "https://zenodo.org/record/67890 in source_code"
        4. No URLs should be in the extracted_data that are not explicitly stated in text.
        5. No databases in accession_codes should be empty.

        Strict rules:
        - Do **NOT** add anything to the output that is not explicitly mentioned in the extracted_data.
        
        Input Text to validate against:
        {text}

        Extracted data to validate:
        {extracted_data}

        Return the results **only** in valid JSON format with **no additional text**. Follow this format exactly:
        {{
            "accession_codes": {{
                "database_name_1": [],
                "database_name_2": []
            }},
            "sequencing_data": [],
            "source_code": []
        }}
    """
        
    try:
        llm=get_shared_llm_llama()
        response = llm.complete(prompt).text.strip()
        response = response.replace('```json', '').replace('```', '').strip()   # remove any markdown code blocks if present
        
        # logger.info(f"Review raw response: {response}")
        result = json.loads(response)
        # logger.info(f"Review result: {result}")
        return json.dumps(result)
        
    except Exception as e:
        # logger.error(f"Review error: {e}")
        return json.dumps({
            "is_valid": False,
            "validation": {
                "accession_codes": {
                    "valid_count": 0,
                    "invalid_count": 0
                },

                "source_code": {
                    "valid_count": 0,
                    "invalid_count": 0
                },
                "sequencing_data": {
                    "valid_count": 0,
                    "invalid_count": 0
                }
            }
        })

def get_agent():

    extract_tool = FunctionTool.from_defaults(
        fn=extract_data,
        name="extract_data",
        description="Extracts source code URLs and accession codes from scientific text"
    )

    review_tool = FunctionTool.from_defaults(
        fn=review_data,
        name="review_data",
        description="Validates extracted data against the original text"
    )


    system_prompt = """You are designed to extract and validate source code URLs and sequencing data URLs, and accession codes from scientific text.

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

    Please ALWAYS start with a Thought.

    Return **ONLY** the JSON object with no additional text before or after the JSON object.

    If this format is used, the user will respond in the following format:

    ```
    Observation: tool response
    ```

    You should keep repeating the above format until you have all the extracted information. At that point, you MUST respond
    in the the following format:

    ```
    Thought: I can answer without using any more tools.
    Answer: [your answer here]
    ```


    When validation is successful:
    Thought: Extraction and validation complete
    Answer: [final extracted and validated data]

    ## Current Conversation
    Below is the current conversation consisting of interleaving human and assistant messages.
    """

    # llm = Ollama(model="llama3.1:8b", temperature=0.1, request_timeout=60.0)
    # llm = Ollama(model="deepseek-r1:8b", temperature=0.1,request_timeout=90.0)

    agent = ReActAgent.from_tools(
        [extract_tool, review_tool],
        llm=get_shared_llm_llama(),
        verbose=True,
        max_retries=2,
        max_execution_time=60,
        max_iterations=15
    )

    react_system_prompt = PromptTemplate(system_prompt)
    agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})


    return agent

def process_paper(text: str) -> Dict[str, Any]:
    """Process a research paper to extract and validate data."""
    try:
        agent = get_agent()
        response = agent.chat(text)

        # reset if do not want to maintain history between each JSON entry (faster)
        agent.reset()

        return json.loads(response.response)
    except Exception as e:
        # logger.error(f"Processing error: {e}")
        return {
            "accession_codes": {},
            "sequencing_data": [],
            "source_code": []
        }



if __name__ == "__main__":

    files = ["file_input.json"]

    for file in files:
        print("Filename:", file)
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            results = []
            start_time = time.time()
            for entry in data:
                doi = entry.get("DOI", "")
                sample_text = entry.get("paragraph", "")
                pmid = entry.get("PubMed_ID", "")
                
                result = process_paper(sample_text)

                results.append({
                        "DOI": doi,
                        "PubMed_ID": pmid,
                        "results": result
                })
            end_time = time.time()
            print(f"Extracted and validated data: {results}")
            exec_time = end_time - start_time
            exec_time = round(exec_time / 60, 3)
            print("Total execution time: ", exec_time)

            output_path = "file_output.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4)

    output_path = 'evaluation_results.json'
    try:
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            with open(output_path, 'r') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # add new execution time entry
        data.append({
            "run_number": len(data) + 1,
            "execution_time": exec_time
        })

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        with open(output_path, 'w') as f:
            json.dump([{
                "run_number": 1,
                "execution_time": exec_time
            }], f, indent=2)




    # result = process_paper(sample_text["paragraph"])
    # end_time = time.time()
    # print(f"Extracted and validated data: {json.dumps(result, indent=2)}")
    # print("total execution time: ", end_time-start_time)
