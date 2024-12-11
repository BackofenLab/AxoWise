import json
import os

def format_data():
    """Publications having Data Availability and Code Availability separate are merged in a single entry"""

    files = [f for f in os.listdir('.') if f.startswith('_') and f.endswith('udc.json')]

    for file in files:
        with open(file,'r', encoding="utf-8") as f:
            data = json.load(f)

        duplicates = set()
        new_data = {}
        
        for paper in data:
            if paper['DOI'] in list(duplicates):
                new_data[paper['DOI']]['paragraph'] += "\n"+ paper['paragraph']
            else:
                duplicates.add(paper['DOI'])
                new_data.update({paper['DOI']:paper})

        formated_data = []
        for value in new_data.values():
            formated_data.append(value)
        with open(f"{file}_formatted.json","w") as f:
            json.dump(formated_data, f, indent=4)

if __name__ == "__main__":
    format_data()