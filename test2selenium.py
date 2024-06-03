from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Replace these with your actual Twitter credentials
username = 'your_username'
password = 'your_password'
tweet_text = 'This is an automated tweet using Selenium! #Automation'

# Set up the Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--incognito")  # Open in incognito mode

driver = webdriver.Chrome(options=chrome_options)

try:
    # Open Twitter login page
    driver.get("https://twitter.com/login")
    
    # Wait for the username input field to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "session[username_or_email]"))
    )

    # Enter username
    username_input = driver.find_element(By.NAME, "session[username_or_email]")
    username_input.send_keys(username)
    
    # Enter password
    password_input = driver.find_element(By.NAME, "session[password]")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    
    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Tweet text"]'))
    )

    # Click on the tweet box
    tweet_box = driver.find_element(By.XPATH, '//div[@aria-label="Tweet text"]')
    tweet_box.click()
    tweet_box.send_keys(tweet_text)

    # Click the Tweet button
    tweet_button = driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
    tweet_button.click()

    # Wait for the tweet to be posted
    time.sleep(5)

    # Log out
    profile_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Account menu"]'))
    )
    profile_menu.click()
    
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@href="/logout"]'))
    )
    logout_button.click()

    confirm_logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
    )
    confirm_logout_button.click()

    # Wait for logout to complete
    time.sleep(5)

finally:
    # Close the browser
    driver.quit()
