from selenium import webdriver
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

def scrape_site():
    CURRENT_DIR = os.path.abspath(os.getcwd())
    # Set up the Selenium driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model

    driver = webdriver.Chrome(options=options)

    # Start Scraping
    try:
        # get the URL we want to scrape from
        driver.get("https://banner.rowan.edu/reports/reports.pl?task=Section_Tally")

        # Select from dropdown
        dropdown = driver.find_element(By.NAME, "term")
        dropdown.click()
        
        # Select desired Term from dropdown
        Select(dropdown).select_by_value("202420")  # hardcode Spring 2024
        driver.find_element(By.NAME, "Select Term").click()
        
        # Click search button
        driver.find_element(By.NAME, "Search").click()
        
        # Save the current page's HTML to a file
        with open(os.path.join(CURRENT_DIR, "Spring2024.html"), 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(os.path.join(CURRENT_DIR, "Spring2024.html"))
        return os.path.join(CURRENT_DIR, "Spring2024.html") 

    finally:
        driver.quit()