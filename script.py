from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    chrome_options = Options()
    # Uncomment to run without opening a browser window
    # chrome_options.add_argument("--headless")
    chromedriver_path = './chromedriver'

    service = Service(executable_path=chromedriver_path)

    # Initialize Chrome driver with the specified options and service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Go to Google
    driver.get('https://www.google.com')
    
    # Wait for the "Reject all" cookies button to be clickable and click it
    wait = WebDriverWait(driver, 10)
    refuse_cookies_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="Tout refuser"]'))
    )
    refuse_cookies_button.click()

    # Find the search box
    search_box = driver.find_element(By.NAME, "q")    
    # Enter the search query
    research = "les meilleures destinations de vacances"
    search_box.send_keys(research)
    # Submit the search
    search_box.send_keys(Keys.RETURN)
    print(f"Research '{research}' done!")

    driver.quit()

if __name__ == '__main__':
    main()
