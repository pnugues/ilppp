"""
Show the sum of squared errors of regression as a
function of the weight parameters
"""
__author__ = 'Pierre Nugues'
import math

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from datasets import read_tsv


def sum_squared_errors(X, y, w):
    """
    Sum of the squared errors:
    Prediction: X.w = ŷ
    Error (loss): y - ŷ
    :param X: The input matrix: The predictors
    :param y: The output vector: The response
    :param w: The weight vector: The model
    :return: The error
    """
    v = y - np.dot(X, w)
    return np.dot(v, v)


def compute_3d_matrices(X, y):
    """
    Compute the 3D matrix of errors
    Axes x and y, the weights
    Axis z the error
    :param X:
    :param y:
    :return:
    """

    w0_range = np.linspace(-1000, 1000, 100)
    w1_range = np.linspace(0, 0.15, 100)
    x_axis, y_axis = np.meshgrid(w0_range, w1_range)
    z_axis = np.array([math.log10(sum_squared_errors(X, y, [w0, w1]))
                       for w0 in w0_range for w1 in w1_range])
    z_axis = z_axis.reshape(x_axis.shape)
    return x_axis, y_axis, z_axis


def plot(X, y, color):
    X, Y, Z = compute_3d_matrices(X, y)
    surf = ax.plot_surface(Y, X, Z, rstride=1, cstride=1, cmap=color,
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)


if __name__ == '__main__':
    X_a, y_a = read_tsv('../salammbo/salammbo_a_fr.tsv')
    X_e, y_e = read_tsv('../salammbo/salammbo_e_fr.tsv')

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.gca(projection='3d')

    plot(X_a, y_a, plt.cm.coolwarm)
    plot(X_e, y_e, plt.cm.Blues)

    plt.show()
