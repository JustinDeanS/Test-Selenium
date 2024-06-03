from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--incognito")  # Open in incognito mode

driver = webdriver.Chrome(options=chrome_options)

# Open a website
driver.get("https://www.example.com")

# Wait for the page to load
time.sleep(2)

# Example: Search for a term on Google
driver.get("https://www.google.com")
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python")
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(2)

# Example: Click on the first search result
first_result = driver.find_element(By.XPATH, '(//h3)[1]')
first_result.click()

# Wait for the page to load
time.sleep(3)

# Close the browser
driver.quit()
