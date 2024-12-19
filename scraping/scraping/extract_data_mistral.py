import os
import json
import ollama
import time

def send_to_mistral(input_data):

    prompt = f"""
    You are a highly precise extraction tool. I will provide you with the DOI of a scientific publication and its 'Data Availability' section.

    Your task:
    1. Extract only explicitly stated sequencing data accession codes and their respective database names (e.g., GEO, ENA, SRA, etc.). Do not infer or guess accession codes if they are not explicitly mentioned in the text.
    2. Identify source code URLs, but only include URLs from GitHub or Zenodo. Ignore other sources.

    Return the results **only** in valid JSON format in the following structure with no additional text or explanation. Do not include any introductory or closing statements.
    {{
        "accession codes": {{
            "database_name_1": ["accession_code_1", "accession_code_2"],
            "database_name_2": ["accession_code_3"]
        }},
        "source code": ["GitHub_URL", "Zenodo_URL"]
    }}

    Example Input: 
    DOI: <<DOI>> 10.1234/example.doi <<END DOI>> 
    Data Availability: <<DATA>> Raw sequencing data were deposited at the GEO under accession numbers GSE12345 and GSE67890. The source code is available on GitHub at https://github.com/example/repo. <<END DATA>>

    Example Output:
    {{
        "accession codes": {{
            "GEO": ["GSE12345", "GSE67890"]
        }},
        "source code": ["https://github.com/example/repo"]
    }}

    Strict Rules:
    - Do not include any information that is not explicitly written in the provided text.
    - If you cannot find any relevant data for a section, leave it empty (e.g., "accession codes": {{}}, "source code": []).
    - Accession codes must match common formats (e.g., GSE followed by numbers for GEO, PRJ followed by alphanumerics for SRA, etc.). Ignore anything that does not conform to a recognized format.

    Input Data:
    DOI: <<DOI>> {input_data['DOI']} <<END DOI>>
    Data Availability: <<DATA>> {input_data['Data Availability']} <<END DATA>>
    """


    response = ollama.chat(model="llama3.1:8b", messages=[
        {
            "role": "user",
            "content": prompt
        }
    ])
    
    try:
        result = {
            "accession codes": [],
            "source code": []
        }
        
        if response and hasattr(response, 'message'):

            try:
                parsed = json.loads(response.message['content'])
                if isinstance(parsed, dict):
                    result.update(parsed)
            except json.JSONDecodeError:
                # print(f"Could not parse response as JSON: {response.message['content']}")
                parsed = {"accession codes": [], "source code": []}
        # print(response)    
        return result
        
    except Exception as e:
        # print(f"Error processing response: {str(e)}")
        return {
            "accession codes": [],
            "source code": []
        }

def process_json_files():

    files = [f for f in os.listdir('.') if f.startswith('_') and f.endswith('formatted.json')]
    # file = "_Bioactive materials_Molecular Cancer_Molecular Neurodegeneration_udc_formatted.json"
    for file in files:
        print("Filename:", file)

        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            results = []
            for entry in data:
                doi = entry.get("DOI", "")
                data_availability = entry.get("paragraph", "")
                input_data = {
                    "DOI": doi,
                    "Data Availability": data_availability
                }
                # print('Processing DOI:', doi)

                try:
                    # start_time = time.time()
                    result = send_to_mistral(input_data)
                    found1 = False
                    found2 = False

                    # Check for 'GEO' in accession codes
                    if 'GEO' in result.get('accession codes', {}):
                        found1 = any('GSE12345' in codes for codes in result['accession codes']['GEO'])
                        found2 = any('GSE67890' in codes for codes in result['accession codes']['GEO'])

                    # print(found1, found2)

                    # Modify result if excluded codes are found
                    if found1 or found2:
                        result = {'accession codes': {}, 'source code': []}
                    # end_time = time.time()
                    # print("Execution time:", end_time-start_time)
                    results.append({
                        "DOI": doi,
                        "results": result
                    })
                    # print(f"Processed entry. Result: {result}")
                except Exception as e:
                    print(f"Error processing DOI {doi}: {str(e)}")
            
            # print(results)
            # Save results to output file
            output_file = file.rstrip('.json')
            output_file = f"{output_file}_llama3.1-8b.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4)

if __name__ == "__main__":
    
    process_json_files()