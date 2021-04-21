#!/usr/bin/env python3

import feedparser
import re
import time
import os

def file_to_list(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.read().split("\n")

    return lines

def save_file(filename, lines, sort=False):
    if sort:
        lines.sort()
    print(f'Saving {filename}, sort={sort}')
    with open(filename, 'w') as f:
        f.write("\n".join(lines))

def add_if_unique(line, array):
    if line not in array:
       array.append(line)
       print(f"UNIQUE: {line}")

    return array
 
def convert_str_to_words(string):
    words = re.sub('[^A-Za-z0-9-\ ]+', '', string).split(' ')
    return words

def commit_and_push():
    files = ["headlines.txt", "feeds.txt", "relevant.txt", "relevant_lower.txt"]
    for f in files:
        os.system(f'git add {f}')

    os.system('git commit -m "Updated wordlist..."')
    os.system('git push')

words_lower = file_to_list('relevant_lower.txt')
words = file_to_list('relevant.txt')
headlines = file_to_list('headlines.txt')

while True:
    print("Searching for new headlines...")
    feeds = file_to_list('feeds.txt')
    for feed in feeds:
        for item in feedparser.parse(feed)["entries"]:
            headline = item["title"]
            add_if_unique(headline, headlines)
            words_from_headline_lower = convert_str_to_words(headline.lower())
            words_from_headline = convert_str_to_words(headline)

            for word in words_from_headline_lower:
                add_if_unique(word, words_lower)

            for word in words_from_headline:
                add_if_unique(word, words)

    print("Saving files...")
    save_file('headlines.txt', headlines)
    save_file('relevant.txt', words, sort=True)
    save_file('relevant_lower.txt', words_lower, sort=True)
    commit_and_push()
    print("Files saved! Waiting 1 hour until next search...")
    time.sleep(3600)
