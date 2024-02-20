

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

df = pd.read_csv("linkedin-jobs.csv")

df = df[df['isExperienceEligible']]
df_filtered = df.drop_duplicates(subset=['Link'])


chrome_options = Options()

    

service = Service(ChromeDriverManager().install())

# chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_argument('--remote-debugging-port=9222')
#Change chrome driver path accordingly
chrome_driver = "/usr/bin/google-chrome-stable"

driver = webdriver.Chrome(options=chrome_options, service=service)

# Switch to the new tab
# driver.switch_to.window(driver.window_handles[1])



for ind , row in df.iterrows():
    url = row["Link"]
    # Open the URL
    
    driver.execute_script('''window.open("{}","_blank");'''.format(url))
    
    time.sleep(2)
    
    if not (ind+1) % 5:
        input("Press any key ")
    # Print the current URL
    print("Visited URL:", driver.current_url)
        
