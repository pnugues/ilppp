"""
Bigram counting
Usage: python count_bigrams.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys

import regex


def tokenize(text):
    words = regex.findall("\p{L}+", text)
    return words


def count_bigrams(words):
    bigrams = [words[inx] + "\t" + words[inx + 1] for inx in range(len(words) - 1)]

    frequency_bigrams = {}
    for bigram in bigrams:
        if bigram in frequency_bigrams:
            frequency_bigrams[bigram] += 1
        else:
            frequency_bigrams[bigram] = 1
    return frequency_bigrams


if __name__ == '__main__':
    text = sys.stdin.read().lower()
    words = tokenize(text)
    frequency_bigrams = count_bigrams(words)
    for bigram in frequency_bigrams:
        print(frequency_bigrams[bigram], "\t", bigram)
