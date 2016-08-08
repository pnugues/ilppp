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
    trigrams = [tuple(words[inx:inx + 3])
                for inx in range(len(words) - 2)]
    frequencies = {}
    for trigram in trigrams:
        if trigram in frequencies:
            frequencies[trigram] += 1
        else:
            frequencies[trigram] = 1
    return frequencies


if __name__ == '__main__':
    text = sys.stdin.read().lower()
    words = tokenize(text)
    frequency_trigrams = count_trigrams(words)
    for trigram in frequency_trigrams:
        print(frequency_trigrams[trigram], "\t", trigram)
