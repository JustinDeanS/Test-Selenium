from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up the Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--incognito")  # Open in incognito mode

driver = webdriver.Chrome(options=chrome_options)

# Open Amazon
driver.get("https://www.amazon.com")

# Wait for the search bar to be present
search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
)

# Search for a product
search_query = "laptop"
search_bar.send_keys(search_query)
search_bar.send_keys(Keys.RETURN)

# Wait for search results to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
)

# Extract product information
products = []
for i in range(1, 11):  # Extract information for the first 10 products
    try:
        title = driver.find_element(By.XPATH, f'(//h2/a/span)[{i}]').text
        price = driver.find_element(By.XPATH, f'(//span[@class="a-price-whole"])[{i}]').text
        rating = driver.find_element(By.XPATH, f'(//span[@class="a-icon-alt"])[{i}]').text
        products.append({"Title": title, "Price": price, "Rating": rating})
    except Exception as e:
        print(f"Error extracting information for product {i}: {e}")

# Close the browser
driver.quit()

# Save product information to a CSV file
df = pd.DataFrame(products)
df.to_csv("amazon_products.csv", index=False)

print("Product information saved to amazon_products.csv")
