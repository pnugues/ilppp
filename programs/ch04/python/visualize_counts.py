"""Draw counts of A letters across the chapters of Salammbô
in French and English
"""
__author__ = 'Pierre Nugues'

import matplotlib.pyplot as plt


def pair(stats):
    """
    Demux adjacent elements of a list
    :param stats:
    :return:
    """
    counts = stats.split()
    cnt_all = list(map(int, counts[0::2]))  # Letter count
    cnt_one = list(map(int, counts[1::2]))  # A count
    return cnt_all, cnt_one


if __name__ == '__main__':
    stats_en = open('../salammbo/salammbo_a_en.tsv').read()
    stats_fr = open('../salammbo/salammbo_a_fr.tsv').read()
    (cnt_all, cnt_one) = pair(stats_en)
    en = plt.scatter(cnt_all, cnt_one, c='r', marker='x')
    (cnt_all, cnt_one) = pair(stats_fr)
    fr = plt.scatter(cnt_all, cnt_one, c='b', marker='x')
    plt.title("Salammbô")
    plt.xlabel("Letter count")
    plt.ylabel("A count")
    plt.legend((en, fr), ('English', 'French'), loc='lower right', scatterpoints=1)
    plt.show()
