from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    search_results = driver.find_elements(By.CSS_SELECTOR, 'div#search a')
    urls = [result.get_attribute('href') for result in search_results]
    return urls

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
    print(urls)

    driver.quit()

if __name__ == '__main__':
    main()
