"""
Likelihood ratios of bigrams in a corpus
Usage: python likelihood_ratio.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
from math import log

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


def likelihood_ratio(words, freq_unigrams, freq_bigrams):
    lr = {}
    for bigram in freq_bigrams:
        p = freq_unigrams[bigram[1]] / len(words)
        p1 = freq_bigrams[bigram] / freq_unigrams[bigram[0]]
        p2 = ((freq_unigrams[bigram[1]] - freq_bigrams[bigram])
              / (len(words) - freq_unigrams[bigram[0]]))
        if p1 != 1.0 and p2 != 0.0:
            lr[bigram] = 2.0 * (
                log_f(freq_bigrams[bigram],
                      freq_unigrams[bigram[0]], p1) +
                log_f(freq_unigrams[bigram[1]] -
                      freq_bigrams[bigram],
                      len(words) - freq_unigrams[bigram[0]], p2) -
                log_f(freq_bigrams[bigram],
                      freq_unigrams[bigram[0]], p) -
                log_f(freq_unigrams[bigram[1]] -
                      freq_bigrams[bigram],
                      len(words) - freq_unigrams[bigram[0]], p))
    return lr


def log_f(k, N, p):
    return k * log(p) + (N - k) * log(1 - p)


if __name__ == '__main__':
    text = sys.stdin.read().lower()
    words = tokenize(text)
    frequency = count_unigrams(words)
    frequency_bigrams = count_bigrams(words)
    ts = likelihood_ratio(words, frequency, frequency_bigrams)

    for bigram in sorted(ts, key=ts.get):
        print(ts[bigram], "\t", bigram, "\t", frequency[bigram[0]], "\t", frequency[bigram[1]], "\t",
              frequency_bigrams[bigram])
