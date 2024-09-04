'''
#beautiful soup - parsing html & xml module
#https://pypi.org/project/beautifulsoup4/
#to handle infinte scrolling use selenium
#time module- handles pauses in scrolling of page
#requests module does not work for non static html pages

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time 

def scrape_reviews(url,max_scrolls=100,scroll_pause_time=10):

    # Set up Selenium with headless Chrome

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options) #initialize web driver

    #url finder
    driver.get(url)
    #print("url acquired")

    # Click the "see all reviews" button if it exists
    try:
        # Wait until the button is clickable and then click it
        see_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='See all reviews']/ancestor::button"))
    )

        print("Button found. Attempting to click...")
        see_all_button.click()
        print("Button clicked successfully.")

        time.sleep(2)  # Wait for content to load

    except Exception as e:

        print("No 'See More reviews' button found or couldn't click it:", e)
        driver.quit()

        return []

    reviews =set()
    last_review_count = 0

    #to parse and collect reviews
    for i in range(max_scrolls):
        
        print(f"Scroll iteration: {i+1}")
        # Wait for reviews to load
        WebDriverWait(driver, 10).until
        (
            EC.presence_of_element_located((By.CLASS_NAME, 'h3YV2d'))
        )

        # Parse and collect reviews
        print("parsing")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div_elements = soup.find_all('div', class_='h3YV2d')

        # Extract and add unique reviews
        print("review found and adding")
        new_reviews = set(div.text.strip() for div in div_elements)
        print(f"Number of reviews found in this scroll: {len(new_reviews)}")
        
        if len(new_reviews) > last_review_count:
            reviews.update(new_reviews)
            last_review_count = len(reviews)
        else:
            print("No new reviews found, stopping...")
            break

        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new content to load
        time.sleep(scroll_pause_time)

    driver.quit()
    return list(reviews)

#main

url="https://play.google.com/store/apps/details?id=com.lumoslabs.lumosity&hl=en_IN"
reviews = scrape_reviews(url)

for review in reviews:
     print(review)
     print()
     print()
print(len(reviews)) #3'''