import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

# Search Tool
web_search_tool = DuckDuckGoSearchRun()

# Scraper Tool
@tool
def scrape_website(url: str) -> str:
    """
    Read full text of a webpage
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all('p')
        text_content = " ".join([p.text for p in paragraphs])

        return text_content[:3000]

    except Exception as e:
        return f"Error scraping website: {e}"