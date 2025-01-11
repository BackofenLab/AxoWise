import json
import os

def extract_journal_name(filename):
    """Extract journal name from filename regardless of special characters"""

    name = filename.lstrip('_')
    
    if filename.endswith('_udc_formatted_f_clean.json'):
        name = name.replace('_udc_formatted_f_clean.json', '')
        return name
        
    if filename.endswith('.txt'):
        name = name.replace('.txt', '')
        return name
        
    return name

def read_doi_pairs(filename):
    """Read DOI-PubMed pairs from file line by line."""

    with open(filename) as f:
        for line in f:
            doi, pubmed = line.strip('[] \n').split(',')
            yield doi.strip("' \""), pubmed.strip("' \"")


def process_json(input_files):
    """Process JSON file updating entries with PubMed IDs"""

    for txt_file, json_file in input_files:
                
        doi_map = dict(read_doi_pairs(txt_file))
        print(f"Processing {json_file} with DOIs from {txt_file}")

        with open(json_file) as f:
            data = json.load(f)
            for entry in data:
                # Check if PubMed_ID doesn't already exist
                if 'PubMed_ID' not in entry:
                    if entry['DOI'] in doi_map:
                        entry['PubMed_ID'] = doi_map[entry['DOI']]
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)


def add_pmid_to_json(txt_file, json_file):
    """ Update JSON with PubMed IDs """

    doi_map = dict(read_doi_pairs(txt_file))
    process_json(json_file, doi_map)


if __name__ == "__main__":

    json_files = [os.path.join("files", f) for f in os.listdir("files") if f.startswith('_') and f.endswith('f_clean.json')]
    txt_files = [os.path.join("files", f) for f in os.listdir("files") 
                 if f.startswith('_') and f.endswith('.txt') 
                 and not f.endswith('_no_data.txt')
                 and not "error" in f] 
    
    input_files = []
    for txt_file in txt_files:
        txt_file_input = extract_journal_name(os.path.basename(txt_file))
        for json_file in json_files:
            json_file_input = json_file.split('_')[1]
            if txt_file_input == json_file_input:
                input_files.append([txt_file, json_file])
    
    process_json(input_files)