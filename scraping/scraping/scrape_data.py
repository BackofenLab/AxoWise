from extract_doi import setup_chrome_driver
from bs4 import BeautifulSoup
import time
import os
import glob
import pathlib
import json

def extract_data_section():

    data_keywords = ["Data and code availability",
                    "Data and Code Availability",
                    "Data and software availability",
                    "Data and Software Availability",
                    "Data and Materials Availability",
                    "Data and materials availability",
                    "Availability of data and materials",
                    "Availability of Data and Materials",
                    "Data availability statement",
                    "Data Availability Statement",
                    "Software availability",
                    "Software Availability",
                    "Data availability",
                    "Data Availability",
                    "Code availability",
                    "Code Availability",
                    "Accession codes",
                    "Accession Codes",
                    "Accession numbers",
                    "Accession Numbers",
                    "Data sharing",
                    "Data Sharing",
                    "Data deposition",
                    "Data Deposition",
                    "Data reporting",
                    "Data Reporting",
                    "Code available",
                    "Code Available",
                    "Data archive",
                    "Data Archive",
                    "Data access",
                    "Data Access",
                    "Independent data access",
                    "Independent Data Access",
                    "Data resources",
                    "Data Resources",
                    "Methods"]

    for filename in glob.glob(os.path.join(str(pathlib.Path().resolve()), "_*.txt")):
        print(filename)

        driver = setup_chrome_driver()

        results = []
        output_file = f"{filename}.json"

        try:
            with open(filename, 'r') as f:
                content = f.readlines()

                for doi in content:
                    url = doi.strip()

                    driver.get(url)
                    time.sleep(3)
                    html = driver.page_source

                    soup = BeautifulSoup(html, 'html.parser')

                    for heading in soup.find_all(["h2","h3","h4"]):

                        if any(keyword in heading.get_text() for keyword in data_keywords) and "Methods" not in heading.get_text():
                            paragraph = heading.next_sibling

                            if paragraph:
                                results.append({"DOI": url, "header": heading.get_text(), "paragraph": paragraph.get_text()})
                                    
                    save_to_json(results, output_file)

        finally:
            driver.quit()

def save_to_json(results, output_file):

    for idx, data in enumerate(results, start=1):
        data["serial_number"] = idx

    with open(output_file, "w", encoding="utf-8") as f2:
        json.dump(results, f2, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    extract_data_section()