"""Analyze sentiment and term frequency from texts"""
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
import article_capture
import string
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


class CorpusPreprocess:
    def __init__(self) -> None:
        pass


class TfidfAnalysis:
    def __init__(self,corpus) -> None:
        self.corpus = corpus
        self.stop_words = []
        self.cleaned_corpus = []
    def clean(self):
        with open("news_analysis/data/stop_words.txt") as f:
            stop_words = f.read()
            # Get a list of stop words
            self.stop_words = stop_words.split(", ")

        self.corpus = list(map(lambda x:re.sub(r'[0-9]+', '', x),self.corpus))
        for text in self.corpus:
            # Get rid of all the punctuation
            text = text.translate(str.maketrans("","",string.punctuation))
            words = text.split()
            words = [word for word in words if word not in self.stop_words]
            self.cleaned_corpus.append(" ".join(words))

    def analyze(self):
        vectorizer = TfidfVectorizer(
            lowercase= True,
            max_features= 20,
            max_df= 1.0,
            min_df = 3,
            ngram_range= (1,2),
            stop_words="english"
        ) 
        vectors = vectorizer.fit_transform(self.cleaned_corpus)
        token = vectorizer.get_feature_names_out()
        return token

class SentimentAnalyzer:
    """Because of the attribute of Vader analyzer that the lexicon it uses accepts the raw words but not the base word
    The preprocessed corpus won't be used here"""
    nltk.download(["vader_lexicon"])
    def __init__(self,corpus) -> None:
        self.corpus = corpus
    def get_sentiment(self):
        analyzer = SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(self.corpus)
if __name__ == "__main__":
    happy = SentimentAnalyzer("wonder")
    print(happy.get_sentiment())