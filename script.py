from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chromedriver_path = './chromedriver'

    service = Service(executable_path=chromedriver_path)

    # Initialize Chrome driver with specified options & service
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get('https://www.youtube.com')
    driver.quit()

if __name__ == '__main__':
    main()

