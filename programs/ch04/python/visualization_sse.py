"""
Show the sum of squared errors of regression as a
function of the weight parameters
"""
__author__ = 'Pierre Nugues'
import io
import math

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def sum_squared_errors(X, y, w):
    """
    Sum of the squared errors:
    Prediction: X.w = ŷ
    Error: ŷ - y
    :param X: The input matrix: The predictors
    :param y: The output vector: The response
    :param w: The weight vector: The model
    :return: The error
    """
    return sum([(np.dot(X[i, :], w) - y[i]) ** 2 for i in range(len(X))])


def compute_3d_matrices(data):
    """
    Compute the 3D matrix of errors
    Axes x and y, the weights
    Axis z the error
    :param data:
    :return:
    """
    D = np.array(data)
    O = np.ones((len(data), 1))
    M = np.hstack((O, D))

    X = M[:, 0:-1]
    y = M[:, -1]

    w0_range = np.linspace(-1000, 1000, 100)
    w1_range = np.linspace(0, 0.15, 100)
    x_axis, y_axis = np.meshgrid(w0_range, w1_range)
    z_axis = np.array([math.log10(sum_squared_errors(X, y, [w0, w1])) for w0 in w0_range for w1 in w1_range])
    z_axis = z_axis.reshape(x_axis.shape)
    return x_axis, y_axis, z_axis


def plot(data, color):
    X, Y, Z = compute_3d_matrices(data)
    surf = ax.plot_surface(Y, X, Z, rstride=1, cstride=1, cmap=color,
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)


if __name__ == '__main__':
    raw_data_a = io.open('../salammbo/salammbo_a_fr.tsv').read().strip()
    raw_data_e = io.open('../salammbo/salammbo_e_fr.tsv').read().strip()
    data_a = [list(map(int, row.split('\t'))) for row in raw_data_a.split('\n')]
    data_e = [list(map(int, row.split('\t'))) for row in raw_data_e.split('\n')]

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.gca(projection='3d')

    plot(data_a, plt.cm.coolwarm)
    plot(data_e, plt.cm.Blues)

    plt.show()
