"""Create a sheet of summary of Tf-idf analysis"""
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def words_graph(words_list):
    """Generate a wordcloud to visualize the top features of Tf-idf"""
    # Create a list of word
    text=" ".join(words_list)
    # Create the wordcloud object
    wordcloud = WordCloud(width=480, height=480, margin=0).generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()