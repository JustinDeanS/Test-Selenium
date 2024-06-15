from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Replace these with your actual GitHub credentials and repository details
github_username = 'your_username'
github_password = 'your_password'
repository_owner = 'repository_owner'
repository_name = 'repository_name'
issue_title = 'Automated Issue'
issue_body = 'This issue was created using Selenium automation.'

# Set up the Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--incognito")  # Open in incognito mode

driver = webdriver.Chrome(options=chrome_options)

try:
    # Open GitHub login page
    driver.get("https://github.com/login")
    
    # Wait for the username input field to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login_field"))
    )

    # Enter username
    username_input = driver.find_element(By.ID, "login_field")
    username_input.send_keys(github_username)
    
    # Enter password
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(github_password)
    password_input.send_keys(Keys.RETURN)

    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search GitHub"]'))
    )

    # Navigate to the repository
    driver.get(f"https://github.com/{repository_owner}/{repository_name}/issues")

    # Wait for the issues page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn-primary'))
    )

    # Click on the "New issue" button
    new_issue_button = driver.find_element(By.CSS_SELECTOR, 'a.btn-primary')
    new_issue_button.click()

    # Wait for the new issue page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'issue_title'))
    )

    # Enter the issue title
    issue_title_input = driver.find_element(By.ID, 'issue_title')
    issue_title_input.send_keys(issue_title)
    
    # Enter the issue body
    issue_body_input = driver.find_element(By.ID, 'issue_body')
    issue_body_input.send_keys(issue_body)

    # Click on the "Submit new issue" button
    submit_issue_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_issue_button.click()

    # Wait for the issue to be created
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.js-issue-title'))
    )

    # Extract issue details
    created_issue_title = driver.find_element(By.CSS_SELECTOR, 'span.js-issue-title').text
    created_issue_url = driver.current_url

    issue_details = {
        "Title": created_issue_title,
        "URL": created_issue_url
    }

    # Save the issue details to a CSV file
    df = pd.DataFrame([issue_details])
    df.to_csv("created_issue.csv", index=False)

    print("Issue details saved to created_issue.csv")

finally:
    # Close the browser
    driver.quit()
