"""
Drawing inequalities in two chapters of Salammbô
"""
__author__ = 'Pierre Nugues'
import numpy as np
import matplotlib.pyplot as plt
import vector
import random


def paint_half_plane(xr, yr, v, sign, color):
    xl = []
    yl = []
    for x in xr:
        for y in yr:
            if sign * (vector.dot([1, -x], v) - y) > 0:
                xl.append(x)
                yl.append(y)
    plt.plot(xl, yl, color)


if __name__ == '__main__':
    # This Boolean is to visualize either all the chapters or two of them
    two_chapters = False
    data_fr = open('../salammbo/salammbo_a_fr.tsv').read().strip().split('\n')
    data_en = open('../salammbo/salammbo_a_en.tsv').read().strip().split('\n')
    data_fr = [list(map(int, data_fr[i].split('\t')))[::-1] for i in range(len(data_fr))]
    data_en = [list(map(int, data_en[i].split('\t')))[::-1] for i in range(len(data_en))]
    xr = np.linspace(0.06, 0.07, 150)
    yr = np.linspace(-100, 100, 150)
    plt.xlim(0.06, 0.07)
    plt.ylim(-100, 100)
    # plt.plot([0.065883207], [0.049203592], 'b.')

    # circle = plt.Circle((0.065883207, 0.049203592), 0.0001, color='blue')
    # plt.gca().add_patch(circle)
    if two_chapters:
        data_fr = data_fr[0:2]
        data_en = data_en[0:2]
        xr = np.linspace(0.02, 0.12, 150)
        yr = np.linspace(-1500, 1000, 150)
        plt.xlim(0.02, 0.12)
        plt.ylim(-1500, 1000)

    random.seed(2)
    colors_fr = ['r.', 'g.', 'b', 'c.', 'm.', 'y.', 'k.', 'r.', 'g.', 'b.', 'c.', 'm.', 'y.', 'k.', 'r.']
    colors_en = list(colors_fr)
    random.shuffle(colors_en)

    for i in range(len(data_fr)):
        paint_half_plane(xr, yr, data_fr[i], -1, colors_fr[i])
        paint_half_plane(xr, yr, data_en[i], 1, colors_en[i])

    plt.show()
