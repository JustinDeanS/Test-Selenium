from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Replace these with your actual Reddit credentials
reddit_username = 'your_username'
reddit_password = 'your_password'
subreddit = 'python'

# Set up the Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--incognito")  # Open in incognito mode

driver = webdriver.Chrome(options=chrome_options)

try:
    # Open Reddit login page
    driver.get("https://www.reddit.com/login/")

    # Wait for the username input field to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginUsername"))
    )

    # Enter username
    username_input = driver.find_element(By.ID, "loginUsername")
    username_input.send_keys(reddit_username)
    
    # Enter password
    password_input = driver.find_element(By.ID, "loginPassword")
    password_input.send_keys(reddit_password)
    password_input.send_keys(Keys.RETURN)

    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search Reddit"]'))
    )

    # Navigate to the subreddit
    driver.get(f"https://www.reddit.com/r/{subreddit}/")

    # Wait for the posts to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.Post'))
    )

    # Extract post information and upvote
    posts = []
    for i in range(1, 11):  # Extract information for the first 10 posts
        try:
            post = driver.find_element(By.XPATH, f'(//div[@data-click-id="body"])[{i}]')
            title = post.find_element(By.XPATH, './/h3').text
            url = post.find_element(By.XPATH, './/a').get_attribute('href')

            upvote_button = post.find_element(By.XPATH, './/div[@id="vote-arrows"]//button[@aria-label="upvote"]')
            upvote_button.click()

            posts.append({"Title": title, "URL": url})

            # Sleep for a while to avoid triggering anti-bot measures
            time.sleep(2)
        except Exception as e:
            print(f"Error extracting or upvoting post {i}: {e}")

finally:
    # Close the browser
    driver.quit()

# Save post information to a CSV file
df = pd.DataFrame(posts)
df.to_csv("reddit_posts.csv", index=False)

print("Post information saved to reddit_posts.csv")
