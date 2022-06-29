"""Implement the news analysis tool"""

from article_capture import ArticleCaptureController
from txt_analysis import SummaryController, CorpusPreprocess
from summary_create import words_graph

if __name__ == "__main__":
    corpus = ArticleCaptureController("covid china", "CNN").get_corpus()
    cleaned_corpus = CorpusPreprocess(corpus).punctuations_and_stop_words_remove()
    summary = SummaryController(corpus).get_analysis()
    print(summary)
    words_graph(summary[0])