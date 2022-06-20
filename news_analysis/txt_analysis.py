"""Analyze sentiment and term frequency from texts"""
from operator import index
from turtle import update
from matplotlib.pyplot import text
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
import article_capture
import string
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


class CorpusPreprocess:
    def __init__(self, corpus) -> None:
        self.corpus = corpus
    
    def stop_words_remove(self):
        pass
class TfidfAnalysis:
    def __init__(self,corpus) -> None:
        self.corpus = corpus
        self.cleaned_corpus = []

    def stop_words_remove(self):
        with open("news_analysis/data/stop_words.txt") as f:
            stop_words = f.read()
            # Get a list of stop words
            stop_words = stop_words.split(", ")
        self.corpus = list(map(lambda x:re.sub(r'[0-9]+', '', x),self.corpus))
        for text in self.corpus:
            # Get rid of all the punctuation
            text = text.translate(str.maketrans("","",string.punctuation))
            words = text.split()
            words = [word for word in words if word.lower() not in stop_words]
            self.cleaned_corpus.append(" ".join(words))

    def stem_words(self):
        ps = nltk.SnowballStemmer(language="english")
        for corpus_idx, text in enumerate(self.cleaned_corpus):
            words = text.split()
            words = list(map(lambda word: ps.stem(word), words))
            self.cleaned_corpus[corpus_idx] = " ".join(words)
            

    def analyze(self):
        vectorizer = TfidfVectorizer(
            lowercase= True,
            max_features= 20,
            max_df= 0.8,
            min_df = 5,
            ngram_range= (1,2),
            stop_words="english"
        ) 
        vectors = vectorizer.fit_transform(self.cleaned_corpus)
        token = vectorizer.get_feature_names_out()
        return token

    def get_keywords(self):
        self.stop_words_remove()
        # self.stem_words()
        return self.analyze()


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
    a = article_capture.ArticleCaptureController("china covid")
    print("articles are ready")
    Tfidf_sample = TfidfAnalysis(a.get_corpus())
    print(Tfidf_sample.get_keywords())
    # sentiment_sample = SentimentAnalyzer(a.get_corpus()[0])
    # print(sentiment_sample.get_sentiment())