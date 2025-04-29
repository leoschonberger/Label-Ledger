"""
    This script is used to crawl a webpage and extract all links using Selenium and BeautifulSoup.
    It uses a headless browser for efficiency and consistency.
"""
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

def get_all_links(website):
    print(f'Crawling {website} for links...')

    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(website)
        print('Page loaded...')
        html = driver.page_source
        return extract_links(html)
    
    finally:
        driver.quit()

def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return links
