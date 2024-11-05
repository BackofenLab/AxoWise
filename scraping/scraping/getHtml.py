from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import re

def setup_chrome_driver():
    """set up Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless') 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()),
        options = chrome_options
    )

    return driver

def scrape_publications():
    """scrapes the full HTML content with infinite scroll"""

    base_url = "https://www.10xgenomics.com/publications?refinementList%5Bspecies%5D%5B0%5D=Human&page=1"   #scrape publications related to Human species only
    
    driver = setup_chrome_driver()

    try:
        driver.get(base_url)

        last_height = driver.execute_script("return document.body.scrollHeight")    # to get the initial height of page

        while True:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    # scroll down to the bottom

            time.sleep(1)

            new_height = driver.execute_script("return document.body.scrollHeight") # height of new page with more content

            publication_elements = driver.find_element(By.CLASS_NAME, "PublicationSearch")  # find and extract HTML
            html_content = publication_elements.get_attribute("outerHTML")

            with open("publications_test.html", "w", encoding="utf-8") as f:
                f.write(html_content + "\n")

            if new_height == last_height:   # no change in height, all content is loaded
                print("Reached the end of the page.")
                break
            last_height = new_height

    finally:
        driver.quit()

def get_doi():
    """extracts DOI URLs from .html"""

    url = r"./publications_humans.html"
    with open(url, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')

    searchHits = soup.find_all('a', {'class':'css-1nszd81 es4dp9v0'})   #class contains only DOI and PubMedID

    with open("searchHits_test.txt", "w", encoding="utf-8") as f2:
        for hit in searchHits:
            pattern = r'https://doi.org/[^\s"]+'    #pick only DOI hrefs
            url = re.search(pattern, str(hit))

            if url:
                f2.write(str(url[0]) + "\n")


if __name__ == "__main__":
    scrape_publications()
    get_doi()
