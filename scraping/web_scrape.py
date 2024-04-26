from __future__ import annotations # Required for type hinting in Python 3.7

import logging
import asyncio 
from pathlib import Path 
from sys import platform # Required for determining the operating system

from bs4 import BeautifulSoup # Required for web scraping
from selenium import webdriver # web scraping
from selenium.webdriver.chrome.options import Options as ChromeOptions # Required for ChromeOptions
from selenium.webdriver.common.by import By # Required for locating elements by ...
from selenium.webdriver.firefox.options import Options as FirefoxOptions # Required for FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver # WebDriver is used to interact with the browser
from selenium.webdriver.safari.options import Options as SafariOptions # Required for SafariOptions
from selenium.webdriver.support import expected_conditions as EC # Required for expected_conditions
from selenium.webdriver.support.wait import WebDriverWait # Waiting for the element to load 
from fastapi import WebSocket # It is used to communicate with the client

from scraping import scrape_skills, processing as summary 
from scraping.processing.html import extract_hyperlinks, format_hyperlinks

from concurrent.futures import ThreadPoolExecutor # Required for running blocking code in a separate thread

from scraping.processing.text import summarize_text

executor = ThreadPoolExecutor() # Create a ThreadPoolExecutor object

FILE_DIR = Path(__file__).parent.parent # Get the parent directory of the current file


async def async_browse(
    selenium_web_browser: str,
    user_agent: str,
    fast_llm_model: str,
    summary_token_limit: str,
    llm_provider: str,
    url: str, 
    question: str,
    websocket: WebSocket
) -> str:
    """Browse a website and return the answer and links to the user 
    
    Args:
        selenium_web_browser (str): The web browser used for scraping 
        user_agent (str): The user agent used when scraping 
        url (str): The url of the website to browse 
        question (str): The question asked by the user 
        websocket (WebSocketManager): The websocket manager 
        
    Returns:
        str: The answer and links to the user 
    """
    loop = asyncio.get_event_loop() # Get the current event loop
    executor = ThreadPoolExecutor(max_workers=8) # Choosing max_workers as 8 to avoid overloading the server
    
    print(f"Scraping url {url} with question {question}")
    if websocket: # If the websocket is not None
        await websocket.send_json(
            {
                "type": "logs",
                "output": f"🔎 Browsing the {url} for relevant about: {question}...",
            }
        )
    else:
        print(f"🔎 Browsing the {url} for relevant about: {question}...")
    
    try:
        driver, text = await loop.run_in_executor(
            executor, scrape_text_with_selenium, selenium_web_browser, user_agent, url
        )
        await loop.run_in_executor(executor, add_header, driver)
        summary_text = await loop.run_in_executor(
            executor, summarize_text, fast_llm_model, summary_token_limit, llm_provider, url, text, question, driver
        )
        if websocket:
            await websocket.send_json(
                {
                    "type": "logs",
                    "output": f"📝 Information gathered from url {url}: {summary_text}",
                }
            )
        else:
            print(f"📝 Information gathered from url {url}: {summary_text}")
            
        return f"Information gathered from url {url}: {summary_text}"
    except Exception as e:
        print(f"An error occured while processing the url {url}: {e}")
        return f"Error processing the url {url}: {e}"
    
def browse_website(url: str, question: str) -> tuple[str, WebDriver]:
    """Browse a website and return the answer and links to the user 
    
    Args: 
        url (str): The url of the website to browse 
        question (str): The question asked by the user 
    
    Returns:
        Tuple[str, WebDriver]: The answer and links to the user and the webdriver
    """
    
    if not url:
        return "A URL was not specified, cancelling request to browse website.", None
    
    driver, text = scrape_text_with_selenium(url)
    add_header(driver)
    summary_text = summary.summarize_text(url, text, question, driver)
    
    links = scrape_links_with_selenium(driver, url)
    
    # Limit links to 5
    if len(links) > 5:
        links = links[:5]
    
    close_browser(driver)
    return f"Answer gathered from website: {summary_text} \n \n Links: {links}", driver
    
        
def scrape_text_with_selenium(selenium_web_browser: str, user_agent: str, url: str) -> tuple[WebDriver, str]:
    """Scrape text from a website using selenium 
    
    Args:
        url (str): The url of the website to scrape 
        selenium_web_browser (str): The web browser used to scrape 
        user_agent (str): The user agent used when scraping 
    
    Returns:
        Tuple[WebDriver, str]: The webdriver and the text scraped from the website 
    """
    logging.getLogger("selenium").setLevel(logging.CRITICAL) # Set the logging level to CRITICAL to avoid unnecessary logs
    
    options_available = {
        "chrome": ChromeOptions,
        "safari": SafariOptions,
        "firefox": FirefoxOptions,
    }
    
    options = options_available[selenium_web_browser]() # Get the options for the selected web browser
    options.add_argument(f"user-agent={user_agent}") # Set the user agent for the web browser
    options.add_argument("--headless") # Run the web browser in headless mode
    options.add_argument("--enable-javascript") # Enable JavaScript in the web browser
    
    if selenium_web_browser == "firefox":
        driver = webdriver.Firefox(options=options)
    elif selenium_web_browser == "safari":
        driver = webdriver.Safari(options=options)
    else:
        if platform == "linux" or platform == "linux2":
            options.add_argument("--disable-dev-shm-usage") # Disable the /dev/shm usage in Linux 
            options.add_argument("--remote-debugging-port=9222") # Set the remote debugging port to 9222
        options.add_argument("--no-sandbox")
        options.add_experimental_option("prefs", {"download_restrictions": 3})
        driver = webdriver.Chrome(options=options)
    
    print(f"Scraping url {url}...")
    driver.get(url)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body")) # Wait for the body tag to load
    )
    
    # Check if url is a pdf or arxiv link
    if url.endswith(".pdf"):
        text = scrape_skills.scrape_pdf_with_pymupdf(url)
    elif "arxiv" in url:
        # Parse the document number from the url
        doc_num = url.split("/")[-1]
        text = scrape_skills.scrape_pdf_with_arxiv(doc_num)
    else:
        # Get the HTML content directly from the browser's DOM
        page_source = driver.execute_script("return document.body.outerHTML;")
        soup = BeautifulSoup(page_source, "html.parser")
        
        for script in soup(["script", "style"]):
            script.extract()
            
        text = get_text(soup)
    
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return driver, text
        
def get_text(soup):
    """Get the text from the soup 
    
    Args:
        soup (BeautifulSoup): The soup to get the text from 
    Returns:
        str: The text from the soup 
    """
    text = ""
    tags = ["h1", "h2", "h3", "h4", "h5", "p"]
    for element in soup.find_all(tags): 
        text += element.text + "\n\n"
    return text

def scrape_links_with_selenium(driver: WebDriver, url: str) -> list[str]:
    """Scrape links from a website using selenium 
    
    Args:
        driver (WebDriver): The webdriver to use to scrape the links 
    
    Returns:
        List[str]: The links scraped from the website
    """
    page_source = driver.page_source 
    soup = BeautifulSoup(page_source, "html.parser")
    
    for script in soup(["script", "style"]):
        script.extract()
    
    hyperlinks = extract_hyperlinks(soup, url)
    
    return format_hyperlinks(hyperlinks)

def close_browser(driver: WebDriver) -> None:
    """Close the browser 
    
    Args:
        driver (WebDriver): The webdriver to close 
    
    Returns:
        None 
    """
    driver.quit()

def add_header(driver: WebDriver) -> None:
    """Add a header to the website 
    
    Args: 
        driver (WebDriver): The webdriver to use to add the header 
    
    Returns:
        None
    """
    driver.execute_script(open(f"{FILE_DIR}/js/overlay.js", "r").read())