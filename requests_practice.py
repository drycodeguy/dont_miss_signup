import yaml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
import time

load_dotenv()

email = os.getenv('PRACTISCORE_EMAIL')
password = os.getenv('PRACTISCORE_PASSWORD')
#print(email,password)

def match_metadata_scraper(target_url):
    match_metadata = {}
    url_list = []

    options = Options()
    #options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://practiscore.com/login')
    driver.find_element('name', 'username').send_keys(email)
    driver.find_element('name', 'password').send_keys(password)
    time.sleep(10)
    driver.find_element('css selector', 'button[type="submit"]').click()
    time.sleep(10)
    
    for target in target_url: 
        driver.get(target)
        html = driver.page_source
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
            url_list.append(url)
            match_metadata[match_id] = {
                'url': url,
                'reg_time': None
            }
    for targets in url_list:
        driver.get(targets)
        html2 = driver.page_source
        #print(html2)   
        soup2 = BeautifulSoup(html2, "html.parser")
        for p in soup2.find_all('p'):
            if 'Registration opens on' in p.get_text():
                reg_time = p.find('strong').get_text()
                print(reg_time)
                break
    #driver.quit() 
    return match_metadata


with open('config/clubs.yaml') as f:
    config = yaml.safe_load(f)

print(match_metadata_scraper(config['clubs']))
input("press enter to close")               
