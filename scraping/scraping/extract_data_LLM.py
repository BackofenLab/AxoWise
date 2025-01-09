
import ollama
import json
import re
import os

def send_to_llm(input_data):

    prompt = f"""
        You are a highly precise extraction tool. I will provide you with the DOI of a scientific publication and its 'Data Availability' section.

        Your task:
        1. Extract **only** explicitly stated sequencing data accession codes and their respective database names (e.g., GEO, ENA, SRA, etc.). Do **not** infer or guess accession codes if they are not explicitly mentioned in the text.
        2. Identify **all** source code URLs, including URLs from **GitHub** and **Zenodo**. For Zenodo, include any URL explicitly mentioned, regardless of whether it refers to sequencing data or source code. **Do not include URLs from any other sources**.

        Return the results **only** in valid JSON format, with no additional text or explanation. Do **not** include any introductory or closing statements.

        The returned JSON should strictly follow the following format:
        {{
            "accession codes": {{
                "database_name_1": ["accession_code_1", "accession_code_2"],
                "database_name_2": ["accession_code_3"]
            }},
            "source code": ["GitHub_URL", "Zenodo_URL"]
        }}

        Example Input:
        DOI: <<DOI>> 10.1234/example.doi <<END DOI>>
        Data Availability: <<DATA>> Raw sequencing data were deposited at the GEO under accession numbers GSE12345 and GSE67890. Sequencing data is available on Zenodo at https://zenodo.org/record/12345 and https://doi.org/10.1010/zenodo.1234567. Additional analysis scripts are hosted on Zenodo at https://zenodo.org/record/67890 and GitHub at https://github.com/example/repo. <<END DATA>>

        Example Output:
        {{
            "accession codes": {{
                "GEO": ["GSE12345", "GSE67890"]
            }},
            "source code": [
                "https://github.com/example/repo",
                "https://zenodo.org/record/12345",
                "https://doi.org/10.1010/zenodo.1234567",
                "https://zenodo.org/record/67890"
            ]
        }}

        Strict Rules:
        - Only return the JSON structure as shown, with **no additional text or explanation**.
        - If no accession codes are available, leave the "accession codes" section empty: "accession codes": {{}}.
        - If no source code URLs are available, leave the "source code" section empty: "source code": [].
        - Accession codes must strictly follow common formats (e.g., GSE followed by numbers for GEO, PRJ followed by alphanumeric strings for SRA, etc.). **Only include accession codes that match valid formats**.
        - Include **all Zenodo URLs** explicitly mentioned in the text, regardless of their stated purpose, and ensure that **no other URLs** (except GitHub or Zenodo) are included in the "source code" section.

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

        zenodo_urls_in_input = re.findall(r'https?://doi\.org/\d+\.\d+/zenodo\.\d+', input_data['Data Availability'])
        
        if response and hasattr(response, 'message'):

            try:
                parsed = json.loads(response.message['content'])
                
                if isinstance(parsed, dict):
                    result.update(parsed)
            except json.JSONDecodeError:
                print(f"Could not parse response as JSON: {response.message['content']}")
    
        # print("RESULT BEFORE:", result)
        if zenodo_urls_in_input:
            existing_urls = set(result["source code"])
            for url in zenodo_urls_in_input:
                if url not in existing_urls:
                    result["source code"].append(url)
        return result
        
    except Exception as e:
        # print(f"Error processing response: {str(e)}")
        return {
            "accession codes": [],
            "source code": []
        }

def process_file():
    files = [f for f in os.listdir('.') if f.startswith('_') and f.endswith('formatted.json')]
    # files = ["scrape_ds_test_formatted.json"]

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
                # print('Input data:', input_data['Data Availability'])

                try:
                    result = send_to_llm(input_data)
                    found_ac_1 = False
                    found_ac_2 = False

                    # to prevent hallucination in accession codes
                    if 'GEO' in result.get('accession codes', {}):
                        found_ac_1 = any('GSE12345' in codes for codes in result['accession codes']['GEO'])
                        found_ac_2 = any('GSE67890' in codes for codes in result['accession codes']['GEO'])
                    
                    # to prevent hallucination in source code URLs
                    new_source_code = []
                    if result.get('source code', []) != []:
                        for url in result.get('source code', []):
                            if 'github.com' in url.lower():
                                if 'github.com' in input_data['Data Availability']:
                                    new_source_code.append(url)
                            elif 'zenodo' in url.lower():
                                if 'zenodo' in input_data['Data Availability'].lower():
                                    new_source_code.append(url)

                    result['source code'] = new_source_code

                    if found_ac_1 or found_ac_2:
                        result = {'accession codes': {}, 'source code': {new_source_code}} 
                    
                    results.append({
                        "DOI": doi,
                        "results": result
                    })
                    
                except Exception as e:
                    print(f"Error processing DOI {doi}: {str(e)}")


        # for i in results: 
            # print(i)
            output_file = file.rstrip('.json')
            output_file = f"{output_file}_LLM.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4)


if __name__ == "__main__":
    process_file()
