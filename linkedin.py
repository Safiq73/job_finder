import csv
import requests
from bs4 import BeautifulSoup
import random, time
import utils


file = open('linkedin-jobs.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)
writer.writerow(['Title',  'isExperienceEligible', 'years_occurrence', 'Company', 'Location', 'Link'])

PAST_DATE = 15
LOCATION = "India"
ROLE = "Python Developer"
USER_EXP = 2
TOTAL_PAGES = 20


def get_desc(job_link):
    desc = requests.get(job_link).text
    time.sleep(random.randint(4,6)+random.random())
    
    return BeautifulSoup(desc, 'html.parser').find(class_= 'description__text description__text--rich').find("section").get_text(strip = True)


def linkedin_scraper(webpage, page_number):
    
    next_page = webpage.format(role = ROLE.replace(" ", "%20"), past_date= PAST_DATE*24*60*60, location = LOCATION, offset = page_number)
    print(next_page)
    
    response = requests.get(next_page)
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')

    for job in jobs:
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        job_location = job.find('span', class_='job-search-card__location').text.strip()
        job_link = job.find('a', class_='base-card__full-link')['href']
        
        desc = ""
        try:
            desc = get_desc(job_link)
        except AttributeError:
            print("Failed *****")
            retry = 0
            while not desc and retry <3:
                desc = get_desc(job_link)
                retry +=1
                if desc:
                    print("passed*****")
            
        occurrences =utils.findExperienceOccurrence(desc.lower().replace("\n",' '))
        isExperienceEligible = utils.isExperienceEligible(occurrences, USER_EXP)
        print(occurrences, isExperienceEligible)
        

        writer.writerow([job_title, isExperienceEligible, occurrences, job_company, job_location, job_link])

    print('Data updated')

    if page_number < 25*TOTAL_PAGES:
        page_number += 25
        linkedin_scraper(webpage, page_number)
        time.sleep(random.randint(1,3))
    else:
        file.close()
        print('File closed')

linkedin_scraper('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={role}&location={location}&f_TPR=r{past_date}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start={offset}', 0)  
