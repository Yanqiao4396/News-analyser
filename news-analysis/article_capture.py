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

class textScrape:
    """Select the main article content from the whole html"""
    def __init__(self,content) -> None:
        self.content = content
        self.article_texts_list = []
        self.raw_article = []
        self.article_texts = ""

    def BBC_filter(self):
        bs = BeautifulSoup(self.content, "html.parser")
        # Get raw contents with tags and attributes based on the specific attribute
        self.raw_article = bs.find_all("div",attrs={"data-component": "text-block"})

    def Guardian_filter(self):
        bs = BeautifulSoup(self.content, "html.parser")
        # Get raw contents with tags and attributes based on the specific attribute
        self.raw_article = bs.find_all("article")

    def CNN_filter(self):
        bs = BeautifulSoup(self.content, "html.parser")
        # Get raw contents with tags and attributes based on the specific attribute
        self.raw_article = bs.find_all("div", class_="pg-rail-tall__body")

    def restructure(self):
        # Strip the tags and attributes
        self.article_texts_list = list(map(lambda x: x.text,self.raw_article))
        self.article_texts = " ".join(self.article_texts_list)


bbc = pageParse("https://www.cnn.com/2022/05/26/politics/senate-domestic-terrorism-bill-vote/index.html")

bbc_content = textScrape(bbc.getText())
bbc_content.CNN_filter()
print(bbc_content.restructure())
