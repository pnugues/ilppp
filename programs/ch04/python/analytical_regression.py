"""
Computing the analytical solution of regression
Implementation with numpy arrays and matrices.
Matrices are very close to matlab notation, while
arrays are preferable overall.
"""
__author__ = 'Pierre Nugues'

import matplotlib.pyplot as plt
import numpy as np


def regression_matrix(observations, reg=0.0):
    """
    Computes the regression using numpy matrices
    :param observations, regularization
    :return: weights
    """
    if reg != 0.0:
        print('Regularized')
    X = np.matrix(observations)[:, :-1]
    y = np.matrix(observations)[:, -1]
    I = np.identity(X.shape[1])

    w = (X.T * X + reg * I).I * X.T * y
    y_hat = X * w
    sse = (y_hat - y).T * (y_hat - y)
    print("Weights", w.T)
    print("SSE", sse)
    return w


def regression_array(observations):
    """
    Computes the regression using numpy arrays
    :param observations:
    :return:
    """
    X = np.array(observations)[:, :-1]
    y = np.array(observations)[:, -1]
    w = np.dot(np.dot(np.linalg.inv(np.dot(X.T, X)), X.T), y)
    y_hat = np.dot(X, w)
    sse = np.dot((y_hat - y).T, (y_hat - y))
    print("Weights", w.T)
    print("SSE", sse)
    return w


if __name__ == '__main__':
    stat_en = open('../salammbo/salammbo_a_en.tsv').read().strip().split('\n')
    stat_fr = open('../salammbo/salammbo_a_fr.tsv').read().strip().split('\n')
    pattern = [('red', 's'), ('green', '^')]
    lang = [None] * 2
    for i, stats in enumerate([stat_en, stat_fr]):
        observations = [[1] + list(map(float, obs.split())) for obs in stats]
        x = [obs[1] for obs in observations]
        y = [obs[2] for obs in observations]
        lang[i] = plt.scatter(x, y, color=pattern[i][0], marker=pattern[i][1])
        # w = regression_array(observations)
        w = regression_matrix(observations)
        plt.plot([min(x), max(x)], [(np.matrix([1, min(x)]) * w)[0, 0],
                                    (np.matrix([1, max(x)]) * w)[0, 0]],
                 color=pattern[i][0])

    plt.title("Salammbô")
    plt.xlabel("Letter count")
    plt.ylabel("A count")
    plt.legend((lang[0], lang[1]), ('English', 'French'), loc='lower right', scatterpoints=1)
    plt.show()

    print('Trying regularization with a singular matrix')
    # Creation of a singular matrix by duplicating a column
    observations = [obs[0:-1] + [obs[-2]] + [obs[-1]] for obs in observations]
    try:
        regression_matrix(observations)
    except:
        print(np.linalg.linalg.LinAlgError)
        print("Singular matrix: Could not be inverted.")
    regression_matrix(observations, reg=0.01)

    # Trying regularization with a quasi singular matrix
    print('Trying regularization with a quasi singular matrix')
    observations[0][2] -= 0.000001
    # No regularization
    regression_matrix(observations)
    # With regularization
    regression_matrix(observations, reg=0.01)
