from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Replace these with your actual Gmail credentials
gmail_username = 'your_email@gmail.com'
gmail_password = 'your_password'

# Set up the Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--incognito")  # Open in incognito mode

driver = webdriver.Chrome(options=chrome_options)

try:
    # Open Gmail login page
    driver.get("https://mail.google.com/")

    # Enter email
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    email_input.send_keys(gmail_username)
    email_input.send_keys(Keys.RETURN)

    # Wait for the password input to be present
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    time.sleep(2)  # Additional wait time in case of network delay
    password_input.send_keys(gmail_password)
    password_input.send_keys(Keys.RETURN)

    # Wait for the inbox to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="UI"]'))
    )

    # Find the latest unread email
    latest_unread_email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.zE'))
    )
    latest_unread_email.click()

    # Wait for the email content to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ii.gt'))
    )

    # Extract the email subject
    email_subject = driver.find_element(By.CSS_SELECTOR, 'h2.hP').text

    # Extract the email body
    email_body = driver.find_element(By.CSS_SELECTOR, 'div.a3s.aiL').text

    # Save the extracted email content to a text file
    with open("latest_email.txt", "w") as file:
        file.write(f"Subject: {email_subject}\n\n")
        file.write(f"Body:\n{email_body}\n")

    print("Latest email content saved to latest_email.txt")

finally:
    # Close the browser
    driver.quit()
