from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import spacy

def reject_cookies(driver):
    wait = WebDriverWait(driver, 10)
    refuse_cookies_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Tout refuser"]'))
    )
    refuse_cookies_button.click()

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait for the page to load
    time.sleep(2)

def search(research, driver):
    search_box = driver.find_element(By.NAME, "q")    
    search_box.send_keys(research)
    search_box.send_keys(Keys.RETURN)
    
    # Ensure search results are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )

    print(f"Research '{research}' done!")
    # Scroll to ensure all results are loaded
    scroll_to_bottom(driver)

def collect_urls(driver):
    # Modify selector to only target natural search results.
    search_results = driver.find_elements(By.CSS_SELECTOR, 'div#rso .g a')
    urls = []
    for result in search_results:
        href = result.get_attribute('href')
        if href not in urls and 'google.com' not in href:
            urls.append(href)
    return urls

def save_urls_to_csv(urls, filename='urls.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for url in urls:
            writer.writerow([url])
            print(f"\t\033[92m✅ URL added:\033[0m {url[:30]}...")

# Analyzing page text and finding potential destinations
def find_destinations(text):
    # Charge language model
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(text)
    # Use a set to eliminate duplicates and filter short entities
    destinations = {ent.text for ent in doc.ents if ent.label_ == "LOC" and len(ent.text) > 2}
    return list(destinations)

def visit_and_extract_text(driver, url):
    driver.get(url)
    text_elements = driver.find_elements(By.TAG_NAME, "p")
    all_text = " ".join([el.text for el in text_elements])
    return all_text

def main():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chromedriver_path = './chromedriver'
    service = Service(executable_path=chromedriver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://www.google.com')

    reject_cookies(driver)
    search("les meilleures destinations de vacances", driver)

    urls = collect_urls(driver)

    for url in urls:
        page_text = visit_and_extract_text(driver, url)
        destinations = find_destinations(page_text)
        print(f"URL: {url} - Potential destinations: {destinations}")
    
    save_urls_to_csv(urls)

    driver.quit()

if __name__ == '__main__':
    main()
