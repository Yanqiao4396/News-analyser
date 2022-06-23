"""Create a sheet of summary of analysis"""
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def words_graph(words_list=None):

    words_list = ['app', 'authorities', 'breaking', 'cases', 'china', 'chinese', 'city'
    'coronavirus', 'covid', 'days', 'food', 'government', 'lockdown', 'march'
    'media', 'millions', 'officials', 'online', 'outbreak', 'policy', 'politics'
    'quarantine', 'reported', 'residents', 'restrictions', 'shanghai', 'testing'
    'time', 'virus', 'zerocovid']

    # Create a list of word
    text=" ".join(words_list)
    # Create the wordcloud object
    wordcloud = WordCloud(width=480, height=480, margin=0).generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()

if __name__ == "__main__":
    words_graph()