
import ollama
import json
import re
import os

def send_to_llm_sourcecode(input_data, file):

    prompt = f"""
        You are a highly precise extraction tool. I will provide you with the DOI of a scientific publication and its 'Data Availability' section.

        Your task is to dentify **all** source code URLs, including URLs from **GitHub** and **Zenodo**. For Zenodo, include any URL explicitly mentioned, regardless of whether it refers to sequencing data or source code. **Do not include URLs from any other sources**.

        **Return the results **only** in valid JSON format with no additional text or explanation. The response must strictly follow the format below. Do **not** return a list or any other format.**

        The returned JSON must follow this structure exactly, **do not return a list of any kind** and do **not** add any closing statement:
        {{
            "source code": ["GitHub_URL", "Zenodo_URL"]
        }}

        Example Input:
        DOI: <<DOI>> 10.1234/example.doi <<END DOI>>
        Data Availability: <<DATA>> Raw sequencing data were deposited at the GEO under accession numbers GSE12345 and GSE67890. Sequencing data is available on Zenodo at https://zenodo.org/record/12345 and https://doi.org/10.1010/zenodo.1234567. Additional analysis scripts are hosted on GitHub at https://github.com/example/repo. <<END DATA>>

        Example Output:
        {{
            "source code": [
                "https://github.com/example/repo",
                "https://zenodo.org/record/12345",
                "https://doi.org/10.1010/zenodo.1234567"
            ]
        }}

        Strict Rules:
        - **Only return the JSON structure** as shown above, with **no additional text or explanation**.
        - If no source code URLs are available, return an empty list for source code: "source code": [].
        - Include **all Zenodo URLs** explicitly mentioned in the text, regardless of their stated purpose, and ensure that **no other URLs** (except GitHub or Zenodo) are included in the "source code" section.
        - Do **NOT** return data in anoy other format other than JSON.

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
            "source code": []
        }

        zenodo_urls_in_input = re.findall(r'https?://doi\.org/\d+\.\d+/zenodo\.\d+', input_data['Data Availability'])
        
        if response and hasattr(response, 'message'):

            try:
                # Ensure we're only trying to parse JSON, remove any other text
                content = response.message['content']
                # Find the first { and last }
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    parsed = json.loads(json_str)
                    
                    if isinstance(parsed, dict):
                        if "source code" in parsed:
                            result["source code"] = parsed["source code"]
                            
            except json.JSONDecodeError:
                # print(f"Could not parse response as JSON: {response.message['content']}")
                error_file = os.path.splitext(os.path.basename(file))[0] + "_error_LLM.txt"
                error_path = os.path.join("files", error_file)
                with open(error_path, "a", encoding="utf-8") as f2:
                    f2.write(input_data["DOI"] + "\n")
    
        # print("RESULT BEFORE:", result)
        if zenodo_urls_in_input:
            existing_urls = set(result["source code"])
            for url in zenodo_urls_in_input:
                if url not in existing_urls:
                    result["source code"].append(url)
        # print("RESULT: ", result)
        return result
        
    except Exception as e:
        print(f"Error processing response: {str(e)}")
        # return {
        #     "accession codes": [],
        #     "source code": []
        # }

def send_to_llm_accessioncodes(input_data, file):
    prompt = f"""
    You are a highly precise extraction tool. I will provide you with the DOI of a scientific publication and its 'Data Availability' section.

    Your task is to extract only explicitly stated sequencing data accession codes and their respective database names (e.g., GEO, ENA, SRA, etc.). Do not infer or guess accession codes if they are not explicitly mentioned in the text.

    Return the results **only** in valid JSON format in the following structure with no additional text or explanation. Do not include any introductory or closing statements.
    {{
        "accession codes": {{
            "database_name_1": ["accession_code_1", "accession_code_2"],
            "database_name_2": ["accession_code_3"]
        }}
    }}

    Example Input: 
    DOI: <<DOI>> 10.1234/example.doi <<END DOI>> 
    Data Availability: <<DATA>> Raw sequencing data were deposited at the GEO under accession numbers GSE12345 and GSE67890. The source code is available on GitHub at https://github.com/example/repo. <<END DATA>>

    Example Output:
    {{
        "accession codes": {{
            "GEO": ["GSE12345", "GSE67890"]
        }}
    }}

    Strict Rules:
    - Do not include any information that is not explicitly written in the provided text.
    - If you cannot find any relevant data for accession codes, leave it empty (e.g., "accession codes": {{}}).
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
            "accession codes": []
        }

        
        if response and hasattr(response, 'message'):
            try:
                content = response.message['content'].strip()
                start = content.find('{')   # find the first {
                end = content.rfind('}') + 1    # find the last }
                if start != -1 and end != -1:
                    json_str = content[start:end+1]

                    # Additional cleanup to ensure valid JSON
                    json_str = re.sub(r'```json\s*', '', json_str)  # remove markdown code blocks
                    json_str = re.sub(r'\s*```', '', json_str)
                    json_str = re.sub(r'[\n\r\t]', '', json_str)    # remove newlines and tabs
                
                    parsed = json.loads(json_str)
                                        
                    if isinstance(parsed, dict) and "accession codes" in parsed:
                        result["accession codes"] = parsed["accession codes"]
                        
                else:
                    print("No JSON structure found in response")

                return result
                            
            except json.JSONDecodeError:
                # print(f"Could not parse response as JSON: {response.message['content']}")
                error_file = os.path.splitext(os.path.basename(file))[0] + "_error_LLM.txt"
                error_path = os.path.join("files", error_file)
                with open(error_path, "a", encoding="utf-8") as f2:
                    f2.write(input_data["DOI"] + "\n")
                return result
        
        
    except Exception as e:
        print(f"Error processing response: {str(e)}")
        # return {
        #     "accession codes": [],
        #     "source code": []
        # }


def process_file():
    files = [os.path.join("files", f) for f in os.listdir("files") if f.startswith('_') and f.endswith('f_clean.json')]
    # files = ["files/scrape_ds_test.json"]

    for file in files:
        # file=file.removeprefix("files/")
        print("Filename:", file)
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            results = []
            for entry in data:
                doi = entry.get("DOI", "")
                # print("DOI:", doi)
                data_availability = entry.get("paragraph", "")
                input_data = {
                    "DOI": doi,
                    "Data Availability": data_availability
                }

                try:
                    result_sc = send_to_llm_sourcecode(input_data, file)
                    result_ac = send_to_llm_accessioncodes(input_data, file)
                    found_ac_1 = False
                    found_ac_2 = False

                    # to prevent hallucination in accession codes
                    if 'GEO' in result_ac.get('accession codes', {}):
                        found_ac_1 = any('GSE12345' in codes for codes in result_ac['accession codes']['GEO'])
                        found_ac_2 = any('GSE67890' in codes for codes in result_ac['accession codes']['GEO'])
                    
                    # to prevent hallucination in source code URLs
                    new_source_code = []
                    if result_sc.get('source code', []) != []:
                        for url in result_sc.get('source code', []):
                            if 'github.com' in url.lower():
                                if 'github.com' in input_data['Data Availability'] and "https://github.com/example/repo" not in input_data["Data Availability"]:
                                    new_source_code.append(url)
                            elif 'zenodo' in url.lower():
                                if 'zenodo' in input_data['Data Availability'].lower() and "https://zenodo.org/record/12345" not in input_data['Data Availability'].lower() and "https://doi.org/10.1010/zenodo.1234567":
                                    new_source_code.append(url)

                    result_sc['source code'] = new_source_code

                    if found_ac_1 or found_ac_2:
                        result_ac = {'accession codes': {}, 'source code': {new_source_code}} 
                    
                    results.append({
                        "DOI": doi,
                        "results": [result_ac, result_sc]
                    })
                    
                    
                except Exception as e:
                    # print(f"Error processing DOI {doi}: {str(e)}")
                    error_file = os.path.splitext(os.path.basename(file))[0] + "_error_LLM.txt"
                    error_path = os.path.join("files", error_file)
                    with open(error_path, "a", encoding="utf-8") as f2:
                        f2.write(doi + "\n")
            # print("PROCESSED RESULT:", results)

            
            # output_file = f"files/{file.rstrip(".json")}_LLM_dummy.json"
            output_file = os.path.splitext(os.path.basename(file))[0] + "_LLM.json"
            output_path = os.path.join("files", output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4)


if __name__ == "__main__":
    process_file()
