"""
Mutual information of bigrams in a corpus
Usage: python mutual_info.py < corpus.txt
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
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]

    frequency_bigrams = {}
    for bigram in bigrams:
        if bigram in frequency_bigrams:
            frequency_bigrams[bigram] += 1
        else:
            frequency_bigrams[bigram] = 1
    return frequency_bigrams


def mutual_info(words, freq_unigrams, freq_bigrams):
    mi = {}
    factor = len(words) * len(words) / (len(words) - 1)
    for bigram in freq_bigrams:
        mi[bigram] = (
            math.log(factor * freq_bigrams[bigram] /
                     (freq_unigrams[bigram[0]] *
                      freq_unigrams[bigram[1]]), 2))
    return mi


if __name__ == '__main__':
    cutoff = 1
    if len(sys.argv) > 1:
        cutoff = int(sys.argv[1])
    text = sys.stdin.read().lower()
    words = tokenize(text)
    frequency = count_unigrams(words)
    frequency_bigrams = count_bigrams(words)
    mi = mutual_info(words, frequency, frequency_bigrams)

    for bigram in sorted(mi.keys(), key=mi.get, reverse=True):
        if frequency_bigrams[bigram] < cutoff: continue
        print(mi[bigram], '\t', bigram, '\t',
              frequency[bigram[0]], '\t',
              frequency[bigram[1]], '\t',
              frequency_bigrams[bigram])
