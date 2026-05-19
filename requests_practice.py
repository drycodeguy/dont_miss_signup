import yaml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def match_metadata_scraper(target_url):
    match_metadata = {}
    for target in target_url: 
        #Headless browser init
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(target)
        html = driver.page_source
        driver.quit()

        #print(html)
        #Html parsing
        soup = BeautifulSoup(html, "html.parser")
        match_registration = soup.find_all('div', id=lambda x: x and x.startswith('item_'))
        
        #Metadata extraction
        for match in match_registration:
            #Unique match id
            match_id = match['id']
            a_tag = match.find('a')
            #Match reg url 
            url = a_tag['href']
            match_metadata[match_id] = {
                'url': url,
                'reg_time': None
            }
    return match_metadata

with open('config/clubs.yaml') as f:
    config = yaml.safe_load(f)

print(match_metadata_scraper(config['clubs']))