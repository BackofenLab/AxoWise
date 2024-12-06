import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random
import json
import os
import glob
import pathlib


def setup_chrome_driver(user_agent):
    """Sets up a ChromeDriver with a randomized User-Agent."""
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')  # Add randomized User-Agent
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Mask automation flags
    # chrome_options.add_argument('--headless')  # run in headless mode to save resources, works best with headless on ScienceDirect, gives error when uncommented
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("start-maximized")

    return uc.Chrome(options=chrome_options)

def scrape_data(data_keywords):
    """Scrapes Data Availability section from Journals,
        Performance will be optimized in future"""

    for filename in glob.glob(os.path.join(str(pathlib.Path().resolve()), "_*.txt")):
        ua = UserAgent()

        results = []
        output_file = f"{filename}_udc.json"

        try:
            with open(filename, 'r') as f:
                content = f.readlines()
                
                for doi in content:
                    url = doi.strip()

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

                                            results.append({"DOI": url, 
                                                "header": heading.get_text(), 
                                                "paragraph": substring})
                                            
                                        elif '/nar' in url or '/neuonc' in url or '/nsr' in url:
                                            paragraph = heading.find_next_siblings("p", limit=3)
                                            results.append({"DOI": url, 
                                                "header": heading.get_text(), 
                                                "paragraph": str(paragraph)})

                                        else:    
                                            results.append({"DOI": url, 
                                                "header": heading.get_text(), 
                                                "paragraph": paragraph.get_text()})

                            if data_found is not True:
                                with open(f"{filename}_no_data.txt", "a", encoding="utf-8") as f2:
                                    f2.write(doi)

                            save_to_json(results, output_file)
                            
                        else: 
                            with open(f"{filename}_error_list.txt", "a", encoding="utf-8") as f3:
                                f3.write(doi)
                    
                    finally:
                        driver.quit()

        except Exception as e:
            print(f"Error occured: {e}")

def rerun_error_list(data_keywords):
    """Re-runs *_error_list.txt files,
        Code will be optimized in future"""

    for filename in glob.glob(os.path.join(str(pathlib.Path().resolve()), "*error_list.txt")):

        ua = UserAgent()
        results = []

        if filename.endswith('_error_list.txt'):
            base_filename = filename[:-len('_error_list.txt')]
        output_file = f"{base_filename}_udc.json"

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
                                                "paragraph": substring
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
                                                "paragraph": paragraph.get_text()
                                            }
                                            results.append(new_entry) 

                            if not data_found:
                                with open(f"{base_filename}_no_data.txt", "a", encoding="utf-8") as f2:
                                    f2.write(doi)

                            save_to_json(results, output_file)
                            
                        else: 
                            with open(f"{base_filename}_error_list_retry.txt", "a", encoding="utf-8") as f3:
                                f3.write(doi)

                    finally:
                        driver.quit()

        except Exception as e:
            print(f"Error occured: {e}")

def save_to_json(results, output_file):
    """Saves Data Availability section to json files"""

    for idx, data in enumerate(results, start=1):
        data["serial_number"] = idx

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)    



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
    # rerun_error_list(data_keywords)