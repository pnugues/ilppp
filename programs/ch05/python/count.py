"""
A word counting program
Usage: python count.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import regex as re


def tokenize(text):
    words = re.findall('\p{L}+', text)
    return words


def count_unigrams(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


if __name__ == '__main__':
    text = sys.stdin.read().lower()
    words = tokenize(text)
    frequency = count_unigrams(words)
    for word in sorted(frequency.keys(), key=frequency.get, reverse=True):
        print(word, '\t', frequency[word])
