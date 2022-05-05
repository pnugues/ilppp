"""
Computing the cross-entropies and Kullback-Leibler divergence
"""
__author__ = 'Pierre Nugues'

import sys
import regex as re
from math import log

# The 2nd edition, 2014, did not remove duplicate spaces in Tables 4.1 and 4.5
# To reproduce the 2nd edition, 2014, pages 88 and 93, set ed_2014 to True
ed_2014 = False


def count_chars(text):
    char_counts = {}
    for char in text:
        char_counts[char] = char_counts.get(char, 0) + 1
    return char_counts


def relative_freqs(char_counts):
    frequencies = {}
    nbr_char = sum(char_counts.values())
    for char in char_counts:
        frequencies[char] = char_counts[char] / nbr_char
    return frequencies


def entropy(rel_frequencies):
    entropy = 0.0
    for char in rel_frequencies:
        entropy -= rel_frequencies[char] * log(rel_frequencies[char], 2.0)
    return entropy


def cross_entropy(rel_frequency_p, rel_frequency_q):
    cross_entropy = 0.0
    for char in rel_frequency_p:
        if rel_frequency_q.get(char, 0) != 0:
            cross_entropy -= rel_frequency_p[char] * log(rel_frequency_q[char], 2.0)
    return cross_entropy


def clean_text(text):
    """
    Removes all the chars below ASCII code 32
    :param text:
    :return:
    """
    if not ed_2014:
        text = re.sub(r'\s+', ' ', text)
    return re.sub('[\x00-\x1f]', '', text)


# file_p = sys.argv[1]
# file_m = sys.argv[2]
salammbo_f = '../../corpus/Salammbo/salammbo_wikisource.txt'
text_s = clean_text(open(salammbo_f).read()).strip()

chars_s_upper = count_chars(text_s.upper())
print('Frequencies of characters. Letters set in uppercase')
for char in sorted(chars_s_upper):
    print(char, chars_s_upper[char])
print()

print('Frequencies of characters')
chars_s = count_chars(text_s)
for char in sorted(chars_s):
    print(char, chars_s[char])
print()

rel_frequency_s = relative_freqs(chars_s)
entropy_s = entropy(rel_frequency_s)
print('Entropy Salammbô:', entropy_s)

files_p = ['../../corpus/Salammbo/salammbo_train_wikisource.txt',
           '../../corpus/Salammbo/salammbo_ch15.txt',
           '../../corpus/notredame.txt',
           '../../corpus/1984/1984.txt']
file_m = '../../corpus/Salammbo/salammbo_train_wikisource.txt'

print('Cross-entropies')
print("{:7} {:7} {:7} {:7}".format('H(P)', 'H(M)', 'H(P, M)', 'D(P||M)'))
for file_p in files_p:
    text_p = clean_text(open(file_p).read())
    text_m = clean_text(open(file_m).read())
    chars_p = count_chars(text_p)
    chars_m = count_chars(text_m)

    rel_frequency_p = relative_freqs(chars_p)
    rel_frequency_m = relative_freqs(chars_m)

    entropy_p = entropy(rel_frequency_p)
    entropy_m = entropy(rel_frequency_m)
    cross_entropy_v = cross_entropy(rel_frequency_p, rel_frequency_m)
    divergence = - entropy_p + cross_entropy_v
    print("{:6.5f} {:6.5f} {:6.5f} {:6.5f}".format(entropy_p, entropy_m,
                                                   cross_entropy_v, divergence))
