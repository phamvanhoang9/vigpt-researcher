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
    
    options = options_available[selenium_web_browser]()
    