"""Capture relative news text from websites"""

from lib2to3.pgen2 import driver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions

class ArticleSearch:
    """Search articles in the news media according to the query"""
    def __init__(self, search_words:str) -> None:
        self.search_word = search_words
        # Make browser doesn't show up
        self.options = ChromeOptions()
        self.options.headless = True
        self.response = None
        self.driver = Chrome(executable_path='./drivers/chromedriver',options=self.options)

    def NBC_search(self):
        #Convert into the forms of query as a part of url
        self.search_word = self.search_word.replace(" ", "+")
        self.driver.get(f"https://www.nbcnews.com/search/?q={self.search_word}")
        elements = self.driver.find_elements_by_class_name("gs-title")
        self.driver.quit
        links = map(lambda x:x.get_attribute("href"),elements)
        #Avoid repeat_links
        filtered_links = set(ele for ele in links if ele is not None)
        return filtered_links


    def CNN_search(self):
        #Convert into thE forms of query as a part of url
        self.search_word = self.search_word.replace(" ", "%20")
        self.driver.get(f"https://www.cnn.com/search?q={self.search_word}&size=10&sort=relevance")
        elements = self.driver.find_elements_by_class_name("cnn-search__result-headline")
        self.driver.quit
        #Target the children
        elements = map(lambda x:x.find_element_by_css_selector("*"),elements)
        links = map(lambda x:x.get_attribute("href"),elements)
        #Avoid repeat contents
        filtered_links = set(ele for ele in links if ele is not None)
        return filtered_links


class PageParse:
    """Take the HTML from a website and scrape the article contents"""
    def __init__(self,url) -> None:
        self.url = url
        self.content = ""
        self.article_texts_list = []
        self.raw_article = []
        self.article_texts = ""
        
    def getText(self):
        page = requests.get(self.url)
        self.content = page.content

    def NBC_filter(self):
        bs = BeautifulSoup(self.content, "html.parser")
        # Get raw contents with tags and attributes based on the specific attribute
        self.raw_article = bs.find_all("div", class_ = "article-body__content")

    def CNN_filter(self):
        bs = BeautifulSoup(self.content, "html.parser")
        # Get raw contents with tags and attributes based on the specific attribute
        self.raw_article = bs.find_all("div", class_="pg-rail-tall__body")


    def restructure(self):
        # Strip the tags and attributes
        self.article_texts_list = list(map(lambda x: x.text,self.raw_article))
        self.article_texts = " ".join(self.article_texts_list)
        return self.article_texts

class ArticleCaptureController:
    """Do the article capture with the search words and output the articles"""
    def __init__(self, search_words) -> None:
        self.articles_search = ArticleSearch(search_words)
        self.corpus = []

    def NBC_caller(self):
        article_links = self.articles_search.NBC_search()
        for link in article_links:
            article = PageParse(link)
            article.getText()
            article.NBC_filter()
            polished_article = article.restructure()
            self.corpus.append(polished_article)
    def CNN_caller(self):
        article_links = self.articles_search.CNN_search()
        for link in article_links:
            article = PageParse(link)
            article.getText()
            article.CNN_filter()
            polished_article = article.restructure()
            self.corpus.append(polished_article)
    
    def get_corpus(self):
        self.NBC_caller()
        self.CNN_caller()
        return self.corpus

if __name__ == "__main__":
    a = ArticleCaptureController("China covid")
    print(len(a.get_corpus()))