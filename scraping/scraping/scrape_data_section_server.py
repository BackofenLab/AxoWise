import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from webdriver_manager.core.os_manager import ChromeType
import time
import random
import json
import os
from ast import literal_eval
import re


def setup_chrome_driver(user_agent):
    """Sets up a ChromeDriver with a randomized User-Agent."""
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--headless=new')  # new headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')  # Fix for DevToolsActivePort issue

    
    try:
        # first try using Chromium
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        try:
            # try Chrome if Chromium fails
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Failed to initialize either Chromium or Chrome: {str(e)}")
            raise
            
    return driver



def scrape_data(data_keywords):
    """Scrapes Data Availability section from Journals,
        Performance will be optimized in future"""
    
    files = [f for f in os.listdir('.') if f.startswith('_') and f.endswith('.txt')]
    # files = ['_Bioactive materials_Molecular Cancer_Molecular Neurodegeneration.txt']
    for filename in files:
        # print("filename:", filename)
        ua = UserAgent()

        results = []
        output_file = "scrape_ds_test.json"
        content = []
        with open(filename, 'r') as f:
            for line in f:
                items = literal_eval(line)
                content.append(items[0])
            
    
        for doi in content:
            url = doi.strip()
            # print("DOI:", url)

            user_agent = ua.random  # uses either Chrome, Firefox or Safari
            driver = setup_chrome_driver(user_agent)

            try:
                driver.get(url)
                time.sleep(random.uniform(7, 25))   # to depict human behavior

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                data_found = False

                if "References" in str(soup) or "Abstract" in str(soup):    # to ensure page content is loading
                    for heading in soup.find_all(["h2","h3","h4","b"]):
                        # print(heading.get_text())
                        
                        if any(keyword in heading.get_text() for keyword in data_keywords):
                            # print("HEADING: ",heading.get_text())
                            data_found = True
                            paragraph = heading.next_sibling

                            if paragraph:
                                if 'scitranslmed' in url or '/science' in url or '/sciimmunol' in url:
                                    parent_div = heading.find_parent('div')
                                    text = str(parent_div)
                                    start_phrase = heading.get_text()
                                    end_phrase = "</div>"

                                    substring = text[text.find(start_phrase):text.find(end_phrase) + len(end_phrase)]
                                    substring = substring.split('</b>', 1)[1].strip()
                                    substring = substring.rstrip('</div>')

                                    results.append({"DOI": url, 
                                        "header": heading.get_text(), 
                                        "paragraph": str(substring)})
                                    
                                elif '/nar' in url or '/neuonc' in url or '/nsr' in url:
                                    paragraph = heading.find_next_siblings("p", limit=3)
                                    results.append({"DOI": url, 
                                        "header": heading.get_text(), 
                                        "paragraph": str(paragraph)})

                                else:
                                    results.append({"DOI": url, 
                                        "header": heading.get_text(), 
                                        "paragraph": str(paragraph)})


                    if not data_found:
                        # print('data not found')
                        filename = filename.rstrip(".txt")
                        with open(f"{filename}_no_data.txt", "a", encoding="utf-8") as f2:
                            f2.write(doi + "\n")

                    # print(results)
                    save_to_json(results, output_file)
                    
                else: 
                    # print('error occured')
                    filename = filename.rstrip(".txt")
                    with open(f"{filename}_error_list.txt", "a", encoding="utf-8") as f3:
                        f3.write(doi + "\n")
            
            finally:
                driver.quit()


def rerun_error_list(data_keywords):
    """Re-runs *_error_list.txt files,
        Code will be optimized in future"""

    files = [os.path.join("files", f) for f in os.listdir("files") if f.startswith('_') and f.endswith('f_clean.json')]

    for filename in files:
        # print("Filename:", filename)
        ua = UserAgent()
        results = []

        if filename.endswith('_error_list.txt'):
            base_filename = filename[:-len('_error_list.txt')]
        output_file = f"files/{base_filename}_udc.json"

        with open(output_file, 'r', encoding='utf-8') as f:
            results = json.load(f)

        try:
            with open(filename, 'r') as f:
                content = f.readlines() 

                for doi in content:
                    url = doi.strip()
                    user_agent = ua.random
                    driver = setup_chrome_driver(user_agent)

                    try:
                        driver.get(url)
                        time.sleep(random.uniform(7, 25))  # to depict human behavior

                        html = driver.page_source
                        soup = BeautifulSoup(html, "html.parser")
                        data_found = False

                        if "References" in str(soup) or "Abstract" in str(soup):  # publication is loading successfully
                            for heading in soup.find_all(["h2","h3","h4"]):

                                if any(keyword in heading.get_text() for keyword in data_keywords):
                                    data_found = True
                                    paragraph = heading.next_sibling     


                                    if paragraph:
                                        if 'scitranslmed' in url or '/science' in url or '/sciimmunol' in url:
                                            parent_div = heading.find_parent('div')
                                            text = str(parent_div)
                                            start_phrase = heading.get_text()
                                            end_phrase = "</div>"
                                            substring = text[text.find(start_phrase):text.find(end_phrase) + len(end_phrase)]

                                            substring = substring.split('</b>', 1)[1].strip()
                                            substring = substring.rstrip('</div>')

                                            new_entry = {
                                                "DOI": url,
                                                "header": heading.get_text(),
                                                "paragraph": str(substring)
                                            }
                                            results.append(new_entry) 
                                            
                                        elif 'nar' in url or '/neuonc' in url:
                                            paragraph = heading.find_next_siblings("p", limit=3)
                                            new_entry = {
                                                "DOI": url,
                                                "header": heading.get_text(),
                                                "paragraph": str(paragraph)
                                            }
                                            results.append(new_entry) 

                                        else:
                                            new_entry = {
                                                "DOI": url,
                                                "header": heading.get_text(),
                                                "paragraph": str(paragraph.get_text())
                                            }
                                            results.append(new_entry) 

                            if not data_found:
                                no_data_file = os.path.splitext(os.path.basename(file))[0] + "_no_data.txt"
                                no_data_path = os.path.join("files", no_data_file)
                                with open(no_data_path, "a", encoding="utf-8") as f2:
                                    f2.write(doi + "\n")

                            save_to_json(results, output_file)
                            
                        else: 
                            error_file = os.path.splitext(os.path.basename(file))[0] + "_error_list_retry.txt"
                            error_path = os.path.join("files", error_file)
                            with open(error_path, "a", encoding="utf-8") as f2:
                                f2.write(doi + "\n")

                    finally:
                        driver.quit()

        except Exception as e:
            print(f"Error occured: {e}")



def save_to_json(results, output_file):
    """Saves Data Availability section to json files"""

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)    



def merge_data_code_section():
    """Publications having Data Availability and Code Availability separate are merged in a single entry"""

    files = [f for f in os.listdir('.') if f.startswith('_') and f.endswith('udc.json')]
    # files = ['scrape_ds_test.json']
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
        
        output_file = file.rstrip('.json')
        with open(f"{output_file}_formatted.json","w") as f:
            json.dump(formated_data, f, indent=4)



def clean_html():
    """Remove unnecessary HTML elements from 'paragraph' """

    
    files = [f for f in os.listdir('.') if f.startswith('_') and f.endswith('udc_formatted.json')]
    # files = ['scrape_ds_test.json']
    for file in files:
        results = []
        try:
            with open(file,'r', encoding="utf-8") as f:
                data = json.load(f)
            
            for each in data:
                para = each["paragraph"]
                text_no_html = re.sub(r'<[^>]+>', '', para)
                text_clean = re.sub(r'\s+', ' ', text_no_html).strip()

                result_entry = {
                    "DOI": each["DOI"],
                    "header": each["header"],
                    "paragraph": text_clean
                }
                results.append(result_entry)

            output_file = file.rstrip(".json")
            with open(f"{output_file}_f_clean.json","w") as f:
                json.dump(results, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")



if __name__ == "__main__":

    data_keywords = ["Data and code availability",
        "Data and Code Availability",
        "DATA AND CODE AVAILABILITY",
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
        "Data availability and accession codes",
        "Materials and data availability",
        "Data availability",
        "Data Availability",
        "DATA AVAILABILITY",
        "Code availability",
        "Code Availability",
        "CODE AVAILABILITY",
        "Accession codes",
        "Accession Codes",
        "Accession numbers",
        "Accession Numbers",
        "ACCESSION NUMBERS",
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
        "Data Resources"]
   
    # scrape_data(data_keywords)
    # merge_data_code_section()
    # clean_html()
