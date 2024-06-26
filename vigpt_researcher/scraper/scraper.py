from concurrent.futures.thread import ThreadPoolExecutor # ThreadPoolExecutor is used to run multiple threads
from langchain_community.document_loaders import PyMuPDFLoader # PyMuPDFLoader is used to load PDFs
from langchain_community.retrievers import ArxivRetriever # ArxivRetriever is used to retrieve papers from arxiv
from functools import partial 
""" 
functools.partial function in Python is used to fix a certain number of arguments of a function and generate a new function.
This new function takes the remaining arguments as input and keeps the fixed arguments fixed.
It is useful when we want to pass a function as an argument to another function, but need to fix some of the arguments.
"""
import requests # requests is used to make HTTP requests
from bs4 import BeautifulSoup # BeautifulSoup is used to parse HTML


class Scraper:
    """
    Scraper class to extract the content from the links
    """
    def __init__(self, urls, user_agent):
        """
        Initialize the Scraper class.
        Args:
            urls:
        """
        self.urls = urls
        self.session = requests.Session() # for persistent connection
        self.session.headers.update({
            "User-Agent": user_agent
        }) # Identify the user agent to the server such as browser, device, etc.

    def run(self):
        """
        Extracts the content from the links
        """
        partial_extract = partial(self.extract_data_from_link, session=self.session)
        with ThreadPoolExecutor(max_workers=20) as executor:
            contents = executor.map(partial_extract, self.urls)
        res = [content for content in contents if content['raw_content'] is not None]
        return res

    def extract_data_from_link(self, link, session):
        """
        Extracts the data from the link
        """
        content = ""
        try:
            if link.endswith(".pdf"):
                content = self.scrape_pdf_with_pymupdf(link)
            elif "arxiv.org" in link:
                doc_num = link.split("/")[-1] # Extract the document number from the link 
                content = self.scrape_pdf_with_arxiv(doc_num)
            elif link:
                content = self.scrape_text_with_bs(link, session)

            if len(content) < 100:
                return {'url': link, 'raw_content': None}
            return {'url': link, 'raw_content': content}
        except Exception as e:
            return {'url': link, 'raw_content': None}

    def scrape_text_with_bs(self, link, session):
        # We use get method of requests module to get the content of the webpage
        # Session object allows us to persist certain parameters across requests (like headers or cookies)
        response = session.get(link, timeout=4)
        soup = BeautifulSoup(response.content, 'lxml', from_encoding=response.encoding)

        for script_or_style in soup(["script", "style"]):
            script_or_style.extract() # Remove <script> and <style> tags from the soup

        raw_content = self.get_content_from_url(soup)
        lines = (line.strip() for line in raw_content.splitlines()) # Split the raw content into lines
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        content = "\n".join(chunk for chunk in chunks if chunk)
        return content

    def scrape_pdf_with_pymupdf(self, url) -> str:
        """Scrape a pdf with pymupdf

        Args:
            url (str): The url of the pdf to scrape

        Returns:
            str: The text scraped from the pdf
        """
        loader = PyMuPDFLoader(url)
        doc = loader.load()
        return str(doc)

    def scrape_pdf_with_arxiv(self, query) -> str:
        """Scrape a pdf with arxiv
        default document length of 70000 about ~15 pages or None for no limit

        Args:
            query (str): The query to search for

        Returns:
            str: The text scraped from the pdf
        """
        retriever = ArxivRetriever(load_max_docs=2, doc_content_chars_max=None)
        docs = retriever.get_relevant_documents(query=query)
        return docs[0].page_content

    def get_content_from_url(self, soup):
        """Get the text from the soup

        Args:
            soup (BeautifulSoup): The soup to get the text from

        Returns:
            str: The text from the soup
        """
        text = ""
        tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5']
        for element in soup.find_all(tags):
            text += element.text + "\n"
        return text