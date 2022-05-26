"""Capture relative news text from websites"""

import requests
from bs4 import BeautifulSoup

class pageParse:
    """Take the HTML from a website."""
    def __init__(self,url) -> None:
        self.url = url

    def getText(self):
        page = requests.get(self.url)
        return page.content


