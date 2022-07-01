# News Analysis

News Analysis is a tool for providing brief insight into one news topic. It aims to give the users a general idea about the top words around one topic and if authors in news media have negative or positive opinions on it. This tool is developed to provide a first glimpse of the new topics to embrace a rough insight. It can also help users to give a sound idea. Just imagine you hear a topic and are curious about it. Other than reading long, retailed and maybe tedious articles, you can use this tool to get top keywords first. It will not only make you decide if you are interested in this topic but also make you read articles more smoothly.

## Installation

Installing News Analysis tool requires a version of Python greater than 3.8. Because it's a personal project still in development and only accessible to a small number of people, it's not uploaded to `PyPI`. Therefore, the only way to use this project is by cloning it and executing `poetry install` command to add necessary packages. Most importantly, the `Chrome` browser is required to call the' Selenium' package successfully.

## Usage of News Analysis

To use this tool, run the `poetry install` in the root directory to create a virtual environment and then execute `cd news_analysis` to the correct running path. Finally, run `poetry run python main.py SEARCH_WORDS` Within `SEARCH_WORDS` are the topics you want to explore and it should be in the Snake case if there are is than one word

Also if you have the prefer media, you can specify it by adding `--search-media MEDIA` following the previous command.
Until now, this tool accepts three media **CNN**, **NBC** and **Reuters**. Please feel free to select any of them with the right name and case.

An exmample below

```bash
yanqiao@a:~/News_analysis/news_analysis$ poetry run python3 main.py covid_China  --search-media CNN
```

Then after about 1 minute, sentiment analysis result like below will show up:

```bash
😆, Here is the sentiment analysis result
{'neg': 0.034, 'neu': 0.884, 'pos': 0.082, 'compound': 0.4404}
```

As well as a wordcloud which represents the top features.

![Wordcloud](wordcloud.png)

## More

- The process of calling package `Selenium` takes time and isn't stable. Please be patient. If the terminal doesn't prompt anything for more than 1 minutes, please shut it down and re-execute with the sample command. It happens sometimes.
- Please make sure the topic you choose exists. Right nwo the tool hasn't yet had the ability to show up failure message because the developer believes this situation is minor and can be avoid manually
- This tool is still in development, please expect it to be cooler. There are some aspects can be improved and the developer is working on
  - add topic modeling analysis feature
  - overcome the instability from the usage of `Selenium`
  - add more news media to explore more widely
  - add tests
