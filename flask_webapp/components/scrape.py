"""
    This script is used to scrape a webpage using Selenium and BeautifulSoup.
    It extracts the body content, cleans it, and splits it into manageable chunks.

    Still need to do some refining of how it extracts and cleans the content.
    Also need to look into if I am correctly using selenium.webdriver
"""
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver

def scrape_website(website):
    print(f'Scraping {website}...')

    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(website)
        print('Website loaded...')
        html = driver.page_source
        return html
    
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content = soup.find('body')
    if body_content:
        return body_content.get_text()
    return None

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    cleaned_content = soup.get_text(separator='\n')
    cleaned_content = '\n'.join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]
