from scrape_data_section import setup_chrome_driver
import time
import random
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from collections import Counter

def categorize_no_data(dic):

    """Categorize "no data"; whether Data Section is not found or the publication is not accessible publicly"""
    no_data_found = Counter()
    
    files = [f for f in os.listdir('.') if f.startswith('_') and f.endswith('no_data.txt')]

    for filename in files:
        
        ua = UserAgent()
        if not os.path.exists(filename):
            continue
            
        with open(filename, 'r') as f:
            print("filename:", filename)

            content = f.readlines()
            
            for doi in content:
                # print(doi)
                url = doi.strip()

                user_agent = ua.random  # uses either Chrome, Firefox or Safari
                driver = setup_chrome_driver(user_agent)

                try:
                    driver.get(url)
                    time.sleep(random.uniform(7, 25))   # to depict human behavior

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    for heading in soup.find_all(["h2","h3","h4","b"]):
                        # print("Heading", heading)
                        if "Acknowledgements" in heading or "Results" in heading:    
                            for j_name, full_name in dic.items():
                                if j_name in url:
                                    no_data_found[full_name] += 1
                
                finally:
                    driver.quit()

        print("DATA NOT FOUND:", no_data_found)
    return no_data_found


if __name__ == "__main__":

    dic = {'bioactmat':'Bioactive Materials',
           '/s13024':'Mole. Neurodegeneration',
           '/s12943':'Mole. Cancer',
           'j.cmet':'Cell Metabolism',
           '/s41590':'Nat. Immunology',
           '/s41587':'Nat. Biotech.',
           '/nbt':'Nat. Biotech.',
           'j.stem':'Cell Stem Cell',
           'j.chom':'Cell Host & Microbe',
           '/s41556':'Nat. Cell Bio.',
           'j.ccell':'Cancer Cell',
           'gutjnl':'Gut',
           'neuonc':'Neuro-Oncology',
           'j.immuni':'Immunity',
           'j.gastro':'Gastroenterology',
           'CIRCULATIONAHA':'Circulation',
           '/s13045':'J. Hematology & Oncology',
           'annrheumdis':'A. Rheumatic Diseases',
           'S1473':'L. Infectious Diseases',
           '/s41392':'Signal Trans. TT',
           '/nar/':'Nucleic Acids R.',
           'scitranslmed':'Sci. Trans. Medicine',
           '/S1470':'Lancet Oncology',
           '/nsr/':'National Sci. Review',
           'j.jhep':'J. of Hepatology',
           '/s40779':'Military Medical R.',
           '/S2666':'Lancet Microbe',
           '/s41551':'Nat. Biomed. Eng.',
           '/s41423':'Cellular & Mole. Imm.',
           'nmeth':'Nat. Methods',
           '/s43018':'Nat. Cancer',
           '/s42255':'Nat. Metabolism',
           '/s41593':'Nat. Neuroscience',
           '/s41588':'Nat. Genetics',
           '/s41591':'Nat. Medicine',
           '/s41564':'Nat. Microbio.',
           '/s41565':'Nat. Nanotech.',
           'sciimmunol':'Sci. Imm.',
           '/science.':'Science',
           'j.cell':'Cell',
           '/s41586':'Nature',
           'j.scib':'Sci. Bulletin',
           '.CD-':'Cancer Discovery',
           '/s41422':'Cell Research',
           '/cr.':'Cell Research'}

    no_data_found = categorize_no_data(dic)
    # print("FINAL:", no_data_found)

