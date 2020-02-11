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
    p_hat = list(map(logistic, np.dot(X, w)))
    likelihood = 1.0
    for i in range(len(p_hat)):
        if y[i] == 1:
            likelihood *= p_hat[i]
        else:  # If in class 0, the prob. to be in this class is 1 - P
            likelihood *= 1 - p_hat[i]
    return likelihood


def plot_likelihood_surf(w0_hat, w1_range, w2_range):
    z_axis = np.array([[0.0] * len(w2_range) for i in range(len(w1_range))])
    x_axis, y_axis = np.meshgrid(w1_range, w2_range)
    z_axis = z_axis.reshape(x_axis.shape)

    for i in range(len(w1_range)):
        for j in range(len(w2_range)):
            z_axis[j, i] = compute_likelihood(X, y, [w0_hat, w1_range[i], w2_range[j]])
    return x_axis, y_axis, z_axis


def plot_logistic_surf(x_range, y_range, w_opt):
    z_axis = np.array([[0.0] * len(y_range) for i in range(len(x_range))])
    x_axis, y_axis = np.meshgrid(x_range, y_range)
    z_axis = z_axis.reshape(x_axis.shape)

    # We compute the probability surface as a function of x and y
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
    # We compute the likelihood of the classes given the observations
    v1 = compute_likelihood(X, y, [5.636568881389995234, -0.1833732150319406229, 2.779328979299188429])
    v2 = compute_likelihood(X, y, [-0.001966, -1.23076923077, 18.5869565217])
    print('The likelihood of the classes found by R:', v1)
    print('The likelihood of the classes found by my implementation of SGD:', v2)

    # We plot the likelihood surface as a function of w.
    # We center it on the optimal values found by R
    # We denote the fitted weights w_hat
    # w0_hat = 5.636568881389995234, w1_hat = -0.1833732150319406229 w2_hat = 2.779328979299188429
    w0_hat = 5.636568881389995234
    w1_range = np.linspace(-0.19, -0.17, 100)
    w2_range = np.linspace(2.5, 3., 200)
    x_axis, y_axis, z_axis = plot_likelihood_surf(w0_hat, w1_range, w2_range)

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.gca(projection='3d')
    surf = ax.plot_surface(y_axis, x_axis, z_axis, rstride=1, cstride=1,
                           cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

    # Now, given w_hat, we plot the logistic surface representing the probabilities
    # (x, y) = (#letters, #a)
    x_range = np.linspace(0, 100000, 200)
    y_range = np.linspace(0, 10000, 200)
    w_hat = [5.636568881389995234, -0.1833732150319406229, 2.779328979299188429]
    # w_hat = [-0.001966632190134919, -1.2301484430755214, 18.558733427826855]

    x_axis, y_axis, z_axis = plot_logistic_surf(x_range, y_range, w_hat)

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.gca(projection='3d')
    surf = ax.plot_surface(y_axis, x_axis, z_axis, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False, alpha=0.2)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    # We plot the observations
    for x, y_class in zip(X, y):
        if y_class == 1:
            ax.scatter(x[2], x[1], y_class, color='green', marker='x')
        else:
            ax.scatter(x[2], x[1], y_class, color='red', marker='x')
    plt.show()
