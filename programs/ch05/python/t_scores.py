"""
t-scores of bigrams in a corpus
Usage: python t_scores.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import math

import regex


def tokenize(text):
    words = regex.findall("\p{L}+", text)
    return words


def count_unigrams(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2]) for inx in range(len(words) - 1)]

    frequency_bigrams = {}
    for bigram in bigrams:
        if bigram in frequency_bigrams:
            frequency_bigrams[bigram] += 1
        else:
            frequency_bigrams[bigram] = 1
    return frequency_bigrams


def t_scores(words, freq_unigrams, freq_bigrams):
    ts = {}
    for bigram in freq_bigrams:
        ts[bigram] = ((freq_bigrams[bigram] -
                      freq_unigrams[bigram[0]] *
                      freq_unigrams[bigram[1]] /
                      len(words)) /
                      math.sqrt(freq_bigrams[bigram]))
    return ts


if __name__ == '__main__':
    text = sys.stdin.read().lower()
    words = tokenize(text)
    frequency = count_unigrams(words)
    frequency_bigrams = count_bigrams(words)
    ts = t_scores(words, frequency, frequency_bigrams)

    for bigram in sorted(ts, key=ts.get):
        print(ts[bigram], "\t", bigram, "\t", frequency[bigram[0]], "\t", frequency[bigram[1]], "\t",
              frequency_bigrams[bigram])
