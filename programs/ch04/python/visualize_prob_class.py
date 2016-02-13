"""
Visualization of the probability of a class with the logistic function
"""

__author__ = 'Pierre Nugues'

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def logistic(x):
    try:
        return 1 / (1 + math.exp(-x))
    except:
        return 0


logistic = np.vectorize(logistic)


def read_data():
    data = open('../salammbo/salammbo_a_binary.libsvm').read().strip().split('\n')
    observations = [data[i].split() for i in range(len(data))]

    y = [float(obs[0]) for obs in observations]
    X = [['0:1'] + obs[1:] for obs in observations]

    # We assume the data is not sparse
    X = [list(map(lambda x: float(x.split(':')[1]), obs)) for obs in X]
    X = np.array(X)
    return X, y


def compute_prob(w, x, y):
    """
    Computes the likelihood of a partition given the weights
    :param M: The observations
    :param y: The class
    :param w0:
    :param w1:
    :param w2:
    :return:
    """
    z = logistic(np.dot([1, x, y], w))
    """
    # Using logarithms. Will create undeflows
    for i in range(len(X)):
        if y[i] == 0:  # If in class 0, the prob. to be in class 1 is 0. We take 1 - P
            X[i] = math.log10(1 - X[i])
        else:
            X[i] = math.log10(X[i])
    val = sum(X)
    """
    return z


def compute_likelihood(X, y, w0, w1, w2):
    """
    Computes the likelihood of a partition given the weights
    :param M: The observations
    :param y: The class
    :param w0:
    :param w1:
    :param w2:
    :return:
    """
    X = logistic(np.dot(X, [w0, w1, w2]))
    """
    # Using logarithms. Will create undeflows
    for i in range(len(X)):
        if y[i] == 0:  # If in class 0, the prob. to be in class 1 is 0. We take 1 - P
            X[i] = math.log10(1 - X[i])
        else:
            X[i] = math.log10(X[i])
    val = sum(X)
    """
    val = 1.0
    for i in range(len(X)):
        if y[i] == 0:  # If in class 0, the prob. to be in class 1 is 0. We take 1 - P
            val *= 1 - X[i]
        else:
            val *= X[i]
    """if val == 1.0:
        print(w0, w1, w2)"""
    return val


if __name__ == '__main__':
    X, y = read_data()

    """
    Values foud with R
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
    v1 = compute_likelihood(X, y, 5.636568881389995234, -0.1833732150319406229, 2.779328979299188429)
    v2 = compute_likelihood(X, y, -0.001966, -1.23076923077, 18.5869565217)
    # print(v1, v2)

    w0_opt = 5.636568881389995234
    x_range = np.linspace(-10000, 10000, 200)
    y_range = np.linspace(0, 1000000, 200)

    z_axis = np.array([[None] * len(y_range) for i in range(len(x_range))])
    x_axis, y_axis = np.meshgrid(x_range, y_range)
    z_axis = z_axis.reshape(x_axis.shape)

    for i in range(len(x_range)):
        for j in range(len(y_range)):
            z_axis[j, i] = np.array(compute_prob([-0.001966, -1.23076923077, 18.5869565217], x_range[i], x_range[j]))

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.gca(projection='3d')

    surf = ax.plot_surface(y_axis, x_axis, z_axis, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()
