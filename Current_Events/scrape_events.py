from selenium import webdriver
import os
import time

CURRENT_DIR = os.path.abspath(os.getcwd())
# Set up the Selenium driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--no-sandbox")  # Bypass OS security model

driver = webdriver.Chrome(options=options)
try:
    # Navigate to the website
    driver.get('https://rowan.campuslabs.com/engage/events.ics')

    # wait for download
    time.sleep(2) 
 
finally:
    # Close the browser
    driver.quit()