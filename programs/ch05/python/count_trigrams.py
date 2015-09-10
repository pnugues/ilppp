"""
Trigram counting
Usage: python count_trigrams.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys

import regex


def tokenize(text):
    words = regex.findall("\p{L}+", text)
    return words


def count_trigrams(words):
    trigrams = ["\t".join(words[inx:inx + 3]) for inx in range(len(words) - 2)]
    frequency_trigrams = {}
    for trigram in trigrams:
        if trigram in frequency_trigrams:
            frequency_trigrams[trigram] += 1
        else:
            frequency_trigrams[trigram] = 1
    return frequency_trigrams


if __name__ == '__main__':
    text = sys.stdin.read().lower()
    words = tokenize(text)
    frequency_trigrams = count_trigrams(words)
    for trigram in frequency_trigrams:
        print(frequency_trigrams[trigram], "\t", trigram)
