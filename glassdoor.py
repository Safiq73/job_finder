from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import utils
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


query = 'python developer'
location = 'india'
level = 'entry_level'
users_exp = 2
past_date = 15
anonymous = False
total_pages = 20
url_link = f'https://www.glassdoor.co.in/Job/python-developer-jobs-SRCH_KO0,16.htm?fromAge={past_date}'


chrome_options = Options()

service = Service(ChromeDriverManager().install())

chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#Change chrome driver path accordingly
chrome_driver = "/usr/bin/google-chrome-stable"
args = {}
if not anonymous:
    args = {"options":chrome_options, "service":service}
driver = webdriver.Chrome(**args)

# Store pages in a table called postings
postings = []

starttime = datetime.now()
start = time.time()
for i in range(0,total_pages):
    time.sleep(random.randint(1,3)+random.random())
    driver.execute_script('''window.open("{}","_blank");'''.format(url_link))
    # driver.get(str(url_link))
    search_results = driver.find_elements(By.CSS_SELECTOR, 'ul[aria-label="Jobs List"]')
   
    # search_results = driver.find_elements(By.ID, 'css-5lfssm eu4oa1w0')
    for i, result in enumerate(search_results):
        try:
            result.click()
    
        except:
            continue
        
        
        sleep_time = random.randint(1,3) + random.random() 
        # time.sleep(sleep_time) 
        desc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'jobDescriptionText')))
        desc = str(BeautifulSoup(desc.get_attribute('innerHTML'),'html.parser'))
        
        occurrences =utils.findExperienceOccurrence(desc.lower().replace("\n",' '))
        isExperienceEligible = utils.isExperienceEligible(occurrences, users_exp)
        time.sleep(sleep_time)
        print(occurrences, isExperienceEligible)
        # continue
    
        # try:
        #     next_page_link = driver.find_element('//a[@aria-label="Next Page"]').click()
        # except:
        #     break

        
        ## Job title
        result_html = driver.find_element(By.ID, 'jobsearch-ViewjobPaneWrapper')
        
        # result_html = result.get_attribute('innerHTML')
        # soup = BeautifulSoup(result_html,'html.parser')
        try:
            job_title = result_html.find_element(By.CSS_SELECTOR, '.jobsearch-JobInfoHeader-title > span:first-child').text.replace("\n- job post", "")
        except:
            job_title = None
    
        ## Urgent or not
        postings.append({'title': job_title, "isExperienceEligible": isExperienceEligible,"years_occurrence": occurrences, 'link':result.get_attribute("href")  })

driver.close()
end = time.time()
pd.DataFrame(postings).to_csv("indeed_jobs.csv")
print('Finished')
print('start from time:'+str(starttime))
print(f"Runtime of the program is {end - start}")