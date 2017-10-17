#!/usr/bin/env python3

import fire
import progressbar
import random
import re
import wikipedia

def load_most_commons_words(fileName="most_common_words.txt"):
    with open(fileName, "r") as f:
        return [s.replace("\n", "") for s in f.readlines()]

def simplify_article_and_return_words(page):
    return re.sub(r'\W+', ' ', page.lower()).split()

class WikiToMatrix:
    """
    Scrap n wikipedia articles, tranform them to matrix n x w where:
    row -> article
    collumn -> occurance of word in article.

    Words are selected from most common words in english data.
    """

    def run(self, articles_number, words_number, result_file):
        result = []

        most_common_words = load_most_commons_words()
        most_common_words = most_common_words[:words_number]

        if words_number > len(most_common_words):
            raise ValueError("most_common_words database too small: {} > {}".format(
                words_number, len(most_common_words)))

        bar = progressbar.ProgressBar()
        for n in bar(range(articles_number)):
            article_words_occurrence = [0] * words_number
            while True:
                try:
                    page = wikipedia.page(wikipedia.random(), auto_suggest=True)
                    break
                except Exception:
                     pass

            for word in simplify_article_and_return_words(page.content):
                if word in most_common_words:
                    article_words_occurrence[most_common_words.index(word)] += 1

            result.append(article_words_occurrence)

        with open(result_file, "w") as f:
            f.write("\n".join([",".join(str(number) for number in row) for row in result]))


if __name__ == "__main__":
    fire.Fire(WikiToMatrix)

