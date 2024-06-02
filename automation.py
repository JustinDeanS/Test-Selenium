from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
import time

# Specify the path to the ChromeDriver
chrome_driver_path = './chromedriver'

# Create Chrome options
# chrome_options = Options()
# chrome_options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
# chrome_options.add_argument('--ignore-ssl-errors')

# Create a Chrome WebDriver service
# service = Service(chrome_driver_path)

# Initialize the Chrome WebDriver with options
chrome_browser = webdriver.Chrome(chrome_driver_path)

# Open the website
chrome_browser.get('https://techwithjustin.net/')
chrome_browser.get('https://www.youtube.com/')

print(chrome_browser.title)

time.sleep(30)

chrome_browser.quit()

