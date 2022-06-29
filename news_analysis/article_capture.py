"""Capture relative news text from websites"""

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions

class ArticleSearch:
    """Search in the news websites and grab the links of articles in the news media according to the query"""
    def __init__(self, search_words:str) -> None:
        self.search_words = search_words
        # Make browser doesn't show up
        self.options = ChromeOptions()
        self.options.headless = True
        self.response = None
        self.driver = Chrome(executable_path='./drivers/chromedriver',options=self.options)

    def NBC_search(self):
        #Convert into the forms of query as a part of url
        self.search_words = self.search_words.replace(" ", "+")
        self.driver.get(f"https://www.nbcnews.com/search/?q={self.search_words}")
        elements = self.driver.find_elements_by_class_name("gs-title")
        self.driver.quit
        # Grab links in the attributes
        links = map(lambda x:x.get_attribute("href"),elements)
        #Avoid repeat_links
        filtered_links = set(ele for ele in links if ele is not None)
        return filtered_links


    def CNN_search(self):
        #Convert into thE forms of query as a part of url
        self.search_words = self.search_words.replace(" ", "%20")
        self.driver.get(f"https://www.cnn.com/search?q={self.search_words}&size=10&sort=relevance&types=article")
        elements = self.driver.find_elements_by_class_name("cnn-search__result-headline")
        self.driver.quit
        #Target the children
        elements = map(lambda x:x.find_element_by_css_selector("*"),elements)
        links = map(lambda x:x.get_attribute("href"),elements)
        #Avoid repeat contents
        filtered_links = set(ele for ele in links if ele is not None)
        return filtered_links

    def Reuters_search(self):
        #Convert into the forms of query as a part of url
        self.search_words = self.search_words.replace(" ", "+")
        self.driver.get(f"https://www.reuters.com/site-search/?query={self.search_words}&sort=relevance&offset=0")
        elements = self.driver.find_elements_by_css_selector("[data-testid=Heading]")
        self.driver.quit
        # Grab links in the attributes
        links = map(lambda x:x.get_attribute("href"),elements)
        #Avoid repeat_links
        filtered_links = set(ele for ele in links if ele is not None)
        return filtered_links

    def WP_search(self):
        #Convert into the forms of query as a part of url
        self.search_words = self.search_words.replace(" ", "+")
        self.driver.get(f"https://www.washingtonpost.com/search/?query={self.search_words}&btn-search=&facets=%7B%22time%22%3A%22all%22%2C%22sort%22%3A%22relevancy%22%2C%22section%22%3A%5B%5D%2C%22author%22%3A%5B%5D%7D")
        elements = self.driver.find_elements_by_class_name("single-result mt-sm pb-sm")
        print(elements)
        self.driver.quit
        # Grab links in the attributes
        links = map(lambda x:x.get_attribute("href"),elements)
        #Avoid repeat_links
        filtered_links = set(ele for ele in links if ele is not None)
        return filtered_links

class PageParse:
    """Scrape the HTML elements from websites and convert them into readable texts"""
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
        self.raw_article = bs.find_all("div")

    def CNN_filter(self):
        bs = BeautifulSoup(self.content, "html.parser")
        # Get raw contents with tags and attributes based on the specific attribute
        self.raw_article = bs.find_all("div", class_="Paragraph__component")
        self.raw_article.extend(bs.find_all("p"))

    def Reuters_filter(self):
        bs = BeautifulSoup(self.content, "html.parser")
        self.raw_article = bs.find_all("div", class_="article-body__content__17Yit paywall-article")[:10]

    def WP_filter(self):
        bs = BeautifulSoup(self.content, "html.parser")
        # Get raw contents with tags and attributes based on the specific attribute
        self.raw_article = bs.find_all("div", class_="article-body")

    def restructure(self):
        # Strip the tags and attributes
        self.article_texts_list = list(map(lambda x: x.text,self.raw_article))
        self.article_texts = " ".join(self.article_texts_list)
        self.article_texts = self.article_texts.replace("\n","")
        return self.article_texts

class ArticleCaptureController:
    """Do the article capture with the search words and output a corpus"""
    def __init__(self, search_words, search_media = None) -> None:
        self.articles_search = ArticleSearch(search_words)
        self.corpus = []
        self.search_media = search_media
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
    
    def Reuters_caller(self):
        article_links = self.articles_search.Reuters_search()
        for link in article_links:
            article = PageParse(link)
            article.getText()
            article.Reuters_filter()
            polished_article = article.restructure()
            self.corpus.append(polished_article)        

    def WP_caller(self):
        article_links = self.articles_search.WP_search()
        for link in article_links:
            article = PageParse(link)
            article.getText()
            article.WP_filter()
            polished_article = article.restructure()
            self.corpus.append(polished_article)              

    def get_corpus(self):
        "The main method to return corpus"
        # If user targets specific media, then just call the targeted one
        if self.search_media != None:
            exec(f"self.{self.search_media}_caller()")
        # the articles aren't promised to scraped because of the variety of styles of HTML
        # So for the articles which are failed to scrape, delete the null string to clean the outcome
            while ('' in self.corpus):
                self.corpus.remove('')
            return self.corpus

        # Scrape from all the three media. It's a default option
        self.NBC_caller()
        self.CNN_caller()
        self.Reuters_caller()
        while ('' in self.corpus):
            self.corpus.remove('')
        return self.corpus

if __name__ == "__main__":
    a = ArticleCaptureController("china covid","CNN")
    print(len(a.get_corpus()))