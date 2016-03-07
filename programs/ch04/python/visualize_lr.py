"""
Visualization of the maximum likelihood with the logistic function
"""

__author__ = 'Pierre Nugues'

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from datasets import read_libsvm_file


def logistic(x):
    try:
        return 1 / (1 + math.exp(-x))
    except:
        return 0


logistic = np.vectorize(logistic)


def compute_likelihood(X, y, w):
    """
    Computes the likelihood of a partition given the weights
    :param X: The observations
    :param y: The class
    :param w0:
    :param w1:
    :param w2:
    :return:
    """
    X = logistic(np.dot(X, w))
    val = 1.0
    for i in range(len(X)):
        if y[i] == 0:  # If in class 0, the prob. to be in class 1 is 0. We take 1 - P
            val *= 1 - X[i]
        else:
            val *= X[i]
    return val


def plot_likelihood_surf(w0_opt, w1_range, w2_range):
    z_axis = np.array([[None] * len(w2_range) for i in range(len(w1_range))])
    x_axis, y_axis = np.meshgrid(w1_range, w2_range)
    z_axis = z_axis.reshape(x_axis.shape)

    for i in range(len(w1_range)):
        for j in range(len(w2_range)):
            z_axis[j, i] = compute_likelihood(X, y, [w0_opt, w1_range[i], w2_range[j]])
    return x_axis, y_axis, z_axis


def plot_logistic_surf(x_range, y_range, w_opt):
    z_axis = np.array([[None] * len(y_range) for i in range(len(x_range))])
    x_axis, y_axis = np.meshgrid(x_range, y_range)
    z_axis = z_axis.reshape(x_axis.shape)

    # We plot the probability surface as a function of x and y

    for i in range(len(x_range)):
        for j in range(len(y_range)):
            z_axis[j, i] = logistic(np.dot([1, x_range[i], y_range[j]], w_opt))
    return x_axis, y_axis, z_axis


if __name__ == '__main__':
    X, y = read_libsvm_file('../salammbo/salammbo_a_binary.libsvm')

    """
    Values found with R
    Coefficients:
                                 Estimate                Std. Error                   z value Pr(>|z|)
    (Intercept)  5.636568881389995234e+00  2.533168869198490283e+05  2.000000000000000164e-05  0.99998
    lettres     -1.833732150319406229e-01  3.503859485659139068e+02 -5.199999999999999544e-04  0.99958
    as           2.779328979299188429e+00  5.267388230572927569e+03  5.299999999999999807e-04  0.99958
    """
    """
    Values found by my impl. of gradient descent
    w0: -0.001966632190134919	w1: -1.2301484430755214	w2: 18.558733427826855
    """
    v1 = compute_likelihood(X, y, [5.636568881389995234, -0.1833732150319406229, 2.779328979299188429])
    v2 = compute_likelihood(X, y, [-0.001966, -1.23076923077, 18.5869565217])
    # print(v1, v2)

    # We plot the likelihood surface as a function of w
    w0_opt = 5.636568881389995234
    w1_range = np.linspace(-0.25, -0.1, 100)
    w2_range = np.linspace(1., 4., 200)
    x_axis, y_axis, z_axis = plot_likelihood_surf(w0_opt, w1_range, w2_range)

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.gca(projection='3d')

    surf = ax.plot_surface(y_axis, x_axis, z_axis, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

    # Now, given w, we plot the logistic surface representing the probabilities
    x_range = np.linspace(0, 100000, 200)
    y_range = np.linspace(0, 10000, 200)
    w_opt = [5.636568881389995234, -0.1833732150319406229, 2.779328979299188429]

    x_axis, y_axis, z_axis = plot_logistic_surf(x_range, y_range, w_opt)

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.gca(projection='3d')

    surf = ax.plot_surface(y_axis, x_axis, z_axis, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()
