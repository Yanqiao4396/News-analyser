"""Implement the news analysis tool and call all other classes"""

from article_capture import ArticleCaptureController
from txt_analysis import SummaryController, CorpusPreprocess
from summary_create import words_graph
import typer

#Ignore DeprecationWarning to make terminal clean
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def main(search_words, search_media = None):
    """Generate a analysis summary with regard to search words"""
    corpus = ArticleCaptureController(search_words, search_media).get_corpus()
    typer.echo("🚀, The articles are successfully parsed, it's time to do analysis to them")
    cleaned_corpus = CorpusPreprocess(corpus).punctuations_and_stop_words_remove()
    summary = SummaryController(cleaned_corpus).get_analysis()
    typer.echo("😆, Here is the sentiment analysis result")
    print(summary[1])
    # Get the wordcould for the Tf-idf top features
    words_graph(summary[0])

if __name__ == "__main__":
    typer.run(main)