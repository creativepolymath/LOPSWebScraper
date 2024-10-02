import selenium.webdriver as webdriver
# Import the necessary modules from Selenium and BeautifulSoup
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Launching chrome browser")
    
    # Path to the ChromeDriver executable
    chrome_driver_path = "chromedriver.exe"
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    # Initialize the Chrome WebDriver with the specified options
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    
    try:
        # Open the specified website
        driver.get(website)
        print("Page Loaded")
        # Get the page source (HTML content) of the website
        html = driver.page_source
        # Wait for 10 seconds to ensure the page is fully loaded
        time.sleep(10)
        
        return html
    finally:
        # Quit the driver to close the browser
        driver.quit()

def extract_body_content(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    # Extract the body content from the parsed HTML
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    # Parse the body content again to clean it
    soup = BeautifulSoup(body_content, "html.parser")
    
    # Remove all script and style elements from the content
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
        
    # Get the text content, separating lines with a newline character
    cleaned_content = soup.get_text(separator="\n")
    # Remove leading and trailing whitespace from each line and filter out empty lines
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    # Split the DOM content into chunks of a specified maximum length
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
