"""
Computing the analytical solution of regression
Implementation with numpy arrays and matrices.
Matrices are very close to matlab notation, while
arrays are preferable overall.
"""
__author__ = 'Pierre Nugues'

import matplotlib.pyplot as plt
import numpy as np


def regression_matrix(X, y, reg=0.0):
    """
    Computes the regression using numpy matrices
    :param observations, regularization
    :return: weights, ŷ, se, sse
    """
    if reg != 0.0:
        print('Regularized')
    I = np.identity(X.shape[1])
    w = (X.T * X + reg * I).I * X.T * y
    y_hat = X * w
    se = np.square(y_hat - y)
    sse = (y_hat - y).T * (y_hat - y)
    return w, y_hat, se, sse


def regression_array(X, y, reg=0.0):
    """
    Computes the regression using numpy arrays
    :param observations:
    :return: weights, ŷ, sse
    """
    if reg != 0.0:
        print('Regularized')
    I = np.identity(X.shape[1])
    w = (np.linalg.inv(X.T @ X + reg * I) @ X.T) @ y
    # Or directly with pinv()
    # w = np.linalg.pinv(X) @ y
    y_hat = X @ w
    se = (y_hat - y) * (y_hat - y)
    sse = (y_hat - y).T @ (y_hat - y)
    return w, y_hat, se, sse


if __name__ == '__main__':
    # Loading the data set
    stat_en = open('../salammbo/salammbo_a_en.tsv').read().strip().split('\n')
    stat_fr = open('../salammbo/salammbo_a_fr.tsv').read().strip().split('\n')
    pattern = [('red', 's'), ('green', '^')]
    lang = [None] * 2

    # Regression with arrays
    for i, stats in enumerate([stat_en, stat_fr]):
        observations = [[1] + list(map(float, obs.split())) for obs in stats]
        x_l = [obs[1] for obs in observations]
        y_l = [obs[2] for obs in observations]
        lang[i] = plt.scatter(x_l, y_l, color=pattern[i][0], marker=pattern[i][1])
        X = np.array(observations)[:, :-1]
        y = np.array(observations)[:, -1]
        w, y_hat, se, sse = regression_array(X, y)
        print('Language:', i)
        print('X:', X)
        print('y:', y)
        print('ŷ:', y_hat)
        print('Squared errors:', se)
        print("Weights", w.T)
        print("SSE", sse)
        plt.plot([min(x_l), max(x_l)],
                 [([1, min(x_l)] @ w), ([1, max(x_l)] @ w)],
                 color=pattern[i][0])
    plt.title("Salammbô")
    plt.xlabel("Letter count")
    plt.ylabel("A count")
    plt.legend((lang[0], lang[1]), ('English', 'French'), loc='lower right', scatterpoints=1)
    plt.show()

    # With matrices
    for i, stats in enumerate([stat_en, stat_fr]):
        observations = [[1] + list(map(float, obs.split())) for obs in stats]
        x_l = [obs[1] for obs in observations]
        y_l = [obs[2] for obs in observations]
        lang[i] = plt.scatter(x_l, y_l, color=pattern[i][0], marker=pattern[i][1])
        X = np.matrix(observations)[:, :-1]
        y = np.matrix(observations)[:, -1]
        w, y_hat, se, sse = regression_matrix(X, y)
        print('Language:', i)
        print('X:', X)
        print('y:', y)
        print('ŷ:', y_hat)
        print('Squared errors:', se)
        print("Weights", w.T)
        print("SSE", sse)

        w = np.array(w)
        plt.plot([min(x_l), max(x_l)],
                 [([1, min(x_l)] @ w), ([1, max(x_l)] @ w)],
                 color=pattern[i][0])
    plt.title("Salammbô")
    plt.xlabel("Letter count")
    plt.ylabel("A count")
    plt.legend((lang[0], lang[1]), ('English', 'French'), loc='lower right', scatterpoints=1)
    plt.show()

    print('Trying regularization with a singular matrix')
    # Creation of a singular matrix by duplicating a column
    observations = [obs[0:-1] + [obs[-2]] + [obs[-1]] for obs in observations]
    X = np.array(observations)[:, :-1]
    y = np.array(observations)[:, -1]
    print('X:', X)
    print('y:', y)
    try:
        regression_array(X, y)
    except:
        print(np.linalg.linalg.LinAlgError)
        print("Singular matrix: Could not be inverted.")

    # Singular matrix with regularization
    w, y_hat, se, sse = regression_array(X, y, reg=0.01)
    print('Weights:', w)
    print('Predictions:', y_hat)
    print('Errors:', se)
    print('SSE:', sse)

    # Trying regularization with a quasi singular matrix
    print('Trying regularization with a quasi singular matrix')
    np.set_printoptions(precision=10)
    observations[0][2] -= 0.000001
    X = np.array(observations)[:, :-1]
    y = np.array(observations)[:, -1]
    print('X:', X)
    print('y:', y)
    # No regularization
    print('No regularization:')
    w, y_hat, se, sse = regression_array(X, y)
    print('Weights:', w)
    print('Predictions:', y_hat)
    print('Errors:', se)
    print('SSE:', sse)

    # With regularization
    print('With regularization')
    w, y_hat, se, sse = regression_array(X, y, reg=0.01)
    print('Weights:', w)
    print('Predictions:', y_hat)
    print('Errors:', se)
    print('SSE:', sse)
