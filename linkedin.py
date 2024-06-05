from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Replace these with your actual LinkedIn credentials
linkedin_username = 'your_email'
linkedin_password = 'your_password'
job_search_query = 'Software Engineer'

# Set up the Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--incognito")  # Open in incognito mode

driver = webdriver.Chrome(options=chrome_options)

try:
    # Open LinkedIn login page
    driver.get("https://www.linkedin.com/login")
    
    # Wait for the username input field to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    # Enter username
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(linkedin_username)
    
    # Enter password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(linkedin_password)
    password_input.send_keys(Keys.RETURN)
    
    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search"]'))
    )

    # Search for jobs
    search_bar = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Search"]')
    search_bar.send_keys(job_search_query)
    search_bar.send_keys(Keys.RETURN)
    
    # Wait for search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Jobs"]'))
    )
    
    # Click on the Jobs tab
    jobs_tab = driver.find_element(By.XPATH, '//button[text()="Jobs"]')
    jobs_tab.click()

    # Wait for job results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.jobs-search__results-list'))
    )

    # Extract job information
    jobs = []
    for i in range(1, 11):  # Extract information for the first 10 jobs
        try:
            job_title = driver.find_element(By.XPATH, f'(//div[@class="full-width artdeco-entity-lockup__content ember-view"]/div/h3)[{i}]').text
            company_name = driver.find_element(By.XPATH, f'(//div[@class="full-width artdeco-entity-lockup__subtitle ember-view"]/a)[{i}]').text
            location = driver.find_element(By.XPATH, f'(//div[@class="artdeco-entity-lockup__caption ember-view"]/div)[{i}]').text
            date_posted = driver.find_element(By.XPATH, f'(//time)[{i}]').text
            jobs.append({"Job Title": job_title, "Company Name": company_name, "Location": location, "Date Posted": date_posted})
        except Exception as e:
            print(f"Error extracting information for job {i}: {e}")

finally:
    # Close the browser
    driver.quit()

# Save job information to a CSV file
df = pd.DataFrame(jobs)
df.to_csv("linkedin_jobs.csv", index=False)

print("Job information saved to linkedin_jobs.csv")
