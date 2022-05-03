import sys
import regex as re
from math import log


def count_letters(text):
    letters = {}
    for c in text:
        letters[c] = letters.get(c, 0) + 1
    return letters


def relative_freqs(letters):
    frequencies = {}
    nbr_car = 0
    for letter in letters:
        nbr_car += letters[letter]
    for letter in letters:
        frequencies[letter] = letters[letter] / nbr_car
    return frequencies


def entropy(rel_frequencies):
    entropy = 0.0
    for letter in rel_frequencies:
        entropy -= rel_frequencies[letter] * log(rel_frequencies[letter], 2.0)
    return entropy


def cross_entropy(rel_frequency_p, rel_frequency_q):
    cross_entropy = 0.0
    for letter in rel_frequency_p:
        if rel_frequency_q.get(letter, 0) != 0:
            cross_entropy -= rel_frequency_p[letter] * log(rel_frequency_q[letter], 2.0)
    return cross_entropy


def clean_text(text):
    """
    Removes all the chars below ASCII code 32
    :param text:
    :return:
    """
    return re.sub('[\x00-\x1f]', '', text)


# file_p = sys.argv[1]
# file_m = sys.argv[2]
files_p = ['../../corpus/Salammbo/salammbo_train_wikisource.txt',
           '../../corpus/Salammbo/salammbo_ch15.txt',
           '../../corpus/notredame.txt',
           '../../corpus/1984/1984.txt']
file_m = '../../corpus/Salammbo/salammbo_train_wikisource.txt'

print("{:7} {:7} {:7} {:7}".format('H(P)', 'H(M)', 'H(P, M)', 'D(P||M)'))
for file_p in files_p:
    text_p = clean_text(open(file_p).read())
    text_m = clean_text(open(file_m).read())
    letters_p = count_letters(text_p)
    letters_m = count_letters(text_m)

    rel_frequency_p = relative_freqs(letters_p)
    rel_frequency_m = relative_freqs(letters_m)

    entropy_p = entropy(rel_frequency_p)
    entropy_m = entropy(rel_frequency_m)
    cross_entropy_v = cross_entropy(rel_frequency_p, rel_frequency_m)
    divergence = - entropy_p + cross_entropy_v
    print("{:6.5f} {:6.5f} {:6.5f} {:6.5f}".format(entropy_p, entropy_m, cross_entropy_v, divergence))
