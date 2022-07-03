"""Analyze sentiment and term frequency from texts"""
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
import article_capture
import string

import nltk
nltk.download("wordnet")
nltk.download('omw-1.4')
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.sentiment import SentimentIntensityAnalyzer

from gensim.corpora import Dictionary
from gensim.models import LdaModel

import pyLDAvis 
import pyLDAvis.gensim_models
import os

class CorpusPreprocess:
    """Remove punctuations and words which express no meanings like 'is', 'a',
        and tokenize texts into forms into words
    """
    def __init__(self,corpus) -> None:
        self.corpus = corpus

    def punctuations_and_stop_words_remove(self):
        with open(f".{os.path.sep}data{os.path.sep}stop_words.txt") as f:
            stop_words = f.read()
            # Get a list of stop words
            stop_words = stop_words.split(", ")

        self.corpus = list(map(lambda x:re.sub(r'[0-9]+', '', x),self.corpus))
        for idx, text in enumerate(self.corpus):
            # Get rid of all the punctuation
            text = text.translate(str.maketrans("","",string.punctuation))
            words = text.split()
            words = [word for word in words if word.lower() not in stop_words]
            self.corpus[idx]=" ".join(words)
        return self.corpus


    def stem_words(self):
        ps = SnowballStemmer(language="english")
        for corpus_idx, text in enumerate(self.corpus):
            words = text.split()
            words = list(map(lambda word: ps.stem(word), words))
            self.corpus[corpus_idx] = " ".join(words)
        return self.corpus

    # def lemmatize_words(self):
    #     lemmatizer = WordNetLemmatizer()
    #     a = ["worked hards ideas to slowly returning","This was a bad ideas"]
    #     for corpus_idx, text in enumerate(a):
    #         words = text.split()
    #         words = list(map(lambda word: lemmatizer.lemmatize(word), words))
    #         a[corpus_idx] = " ".join(words)
    #     print(a)

    def preprocess_corpus(self):
        self.punctuations_and_stop_words_remove()
        self.stem_words()
        return self.corpus


class TopicModel:
    def __init__(self, input_corpus) -> None:
        self.corpus = input_corpus

    def tokenize_words(self):
        pass
        # Split the documents into tokens
        # tokenizer = RegexpTokenizer(r'\w+')
        # for idx in range(len(self.corpus)):
        #     self.corpus[idx] = self.corpus[idx].lower()  # Convert to lowercase
        #     self.corpus[idx] = tokenizer.tokenize(self.corpus[idx])  # Split into words

        # # Remove numbers, but not words that contain numbers.
        # self.corpus = [[token for token in doc if not token.isnumeric()] for doc in self.corpus]

        # # Remove words that are only one character.
        # self.corpus = [[token for token in doc if len(token) > 1] for doc in self.corpus]

    def bag_of_words(self):
        self.corpus = [words.split() for words in self.corpus ]
        print(self.corpus)
        # Create a dictionary representation of the documents.
        dictionary = Dictionary(self.corpus)
        # Bag-of-words representation of the documents.
        corpus = [dictionary.doc2bow(doc) for doc in self.corpus]
        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            chunksize=2000,
            alpha='auto',
            eta='auto',
            iterations=200,
            num_topics=2,
            passes=5,
            eval_every=None
        )
        pyLDAvis.enable_notebook()
        vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary.id2token, mds = "mmds", R = 10)
        vis


class TfidfAnalysis:
    """Analyze term-frequency and inverse document frequency to get the top features which can represent this topic"""
    def __init__(self,cleaned_corpus) -> None:
        self.cleaned_corpus = cleaned_corpus
    def analyze(self):
        vectorizer = TfidfVectorizer(
            lowercase= True,
            max_features= 50,
            max_df= 0.8,
            min_df = 3,
            ngram_range= (1,1),
            stop_words="english",
            binary= True
        ) 
        vectors = vectorizer.fit_transform(self.cleaned_corpus)
        # print(vectors)
        token = vectorizer.get_feature_names_out()
        return token

    def get_keywords(self):
        # self.stem_words()
        return self.analyze()


class SentimentAnalyzer:
    """Provide the sentiment analysis to check the topic is positive or negative """
    def __init__(self,corpus) -> None:
        nltk.download(["vader_lexicon"])
        self.corpus = corpus
    def get_sentiment(self):
        analyzer = SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(self.corpus)

class SummaryController:
    """Call other classes to execute them and generate summary"""
    def __init__(self, corpus) -> None:
        self.corpus = corpus

    def get_analysis(self):
        Tfidf_summary = TfidfAnalysis(self.corpus)
        features = Tfidf_summary.get_keywords()
        sentiment_summary = SentimentAnalyzer(self.corpus[0])
        return features, sentiment_summary.get_sentiment()



if __name__ == "__main__":
    a = article_capture.ArticleCaptureController("Ukraine","Reuters")
    corpus = a.get_corpus()           
    b = CorpusPreprocess(corpus).punctuations_and_stop_words_remove()
    Tfidf_sample = TfidfAnalysis(b)
    print(Tfidf_sample.get_keywords())
    # sentiment_sample = SentimentAnalyzer(a.get_corpus()[0])
    # print(sentiment_sample.get_sentiment())