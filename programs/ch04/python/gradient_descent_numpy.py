"""Gradient descent for linear regression with numpy
"""
import random
import numpy as np
import datasets
import matplotlib.pyplot as plt

__author__ = 'Pierre Nugues'


def sse(X, y, w):
    """
    Sum of squared errors
    :param X:
    :param y:
    :param w:
    :return:
    """
    error = y - X @ w
    return error.T @ error


def normalize(Xy):
    maxima = np.amax(Xy, axis=0)
    D = np.diag(maxima)
    D_inv = np.linalg.inv(D)
    Xy = Xy @ D_inv
    return (Xy, maxima)


def stoch_descent(X, y, alpha, w):
    """
    Stochastic gradient descent
    :param X:
    :param y:
    :param alpha:
    :param w:
    :return:
    """
    global logs, logs_stoch
    logs = []
    logs_stoch = []
    random.seed(0)
    idx = list(range(len(X)))
    for epoch in range(500):
        random.shuffle(idx)
        w_old = w
        for i in idx:
            loss = y[i] - X[i] @ w
            gradient = loss * X[i].reshape(-1, 1)
            w = w + alpha * gradient
            logs_stoch += (w, alpha, sse(X, y, w))
        if np.linalg.norm(w - w_old) / np.linalg.norm(w) < 0.005:
            print("Epoch", epoch)
            break
        logs += (w, alpha, sse(X, y, w))
    return w


def batch_descent(X, y, alpha, w):
    """
    Batch gradient descent
    :param X:
    :param y:
    :param alpha:
    :param w:
    :return:
    """
    global logs
    logs = []
    alpha /= len(X)
    for epoch in range(1, 500):
        loss = y - X @ w
        gradient = X.T @ loss
        w_old = w
        w = w + alpha * gradient
        logs += (w, alpha, sse(X, y, w))
        if np.linalg.norm(w - w_old) / np.linalg.norm(w) < 0.0005:
            print("Epoch", epoch)
            break
    return w


if __name__ == '__main__':
    normalized = True
    debug = False
    X, y = datasets.load_tsv(
        'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')
    # Predictors
    X = np.array(X)
    # Response
    y = np.array([y]).T

    alpha = 1.0e-10
    if normalized:
        X, maxima_X = normalize(X)
        y, maxima_y = normalize(y)
        maxima = np.concatenate((maxima_X, maxima_y))
        alpha = 1.0
        print("-Normalized-")

    print("===Batch descent===")
    w = np.zeros(X.shape[1]).reshape((-1, 1))
    w = batch_descent(X, y, alpha, w)
    print("Weights", w)
    print("SSE", sse(X, y, w))
    if normalized:
        maxima = maxima.reshape(-1, 1)
        print("Restored weights", maxima[-1, 0] * (w / maxima[:-1, 0:1]))
    if debug:
        print("Logs", logs)
    plt.scatter(range(len(logs[2::3])), logs[2::3], c='b', marker='x')
    plt.title("Batch gradient descent: Sum of squared errors")
    plt.show()
    plt.plot(list(map(lambda pair: pair[0], logs[0::3])), list(map(lambda pair: pair[1], logs[0::3])), marker='o')
    for i in range(len(logs[0::3])):
        plt.annotate(i, xy=logs[0::3][i])
    plt.title("Batch gradient descent: Weights")
    plt.show()

    print("===Stochastic descent===")
    w = np.zeros(X.shape[1]).reshape((-1, 1))
    w = stoch_descent(X, y, alpha, w)
    print("Weights", w)
    print("SSE", sse(X, y, w))
    if normalized:
        maxima = maxima.reshape(-1, 1)
        print("Restored weights", maxima[-1, 0] * (w / maxima[:-1, 0:1]))
    if debug:
        print("Logs", logs)
        print("Logs stoch.", logs_stoch)
    plt.scatter(range(len(logs[2::3])), logs[2::3], c='b', marker='x')
    plt.title("Stochastic gradient descent: Sum of squared errors")
    plt.show()
    plt.plot(list(map(lambda pair: pair[0], logs[0::3])), list(map(lambda pair: pair[1], logs[0::3])), marker='o')
    plt.title("Stochastic gradient descent: Weights")
    plt.show()
    plt.scatter(range(len(logs_stoch[2::3])), logs_stoch[2::3], c='b', marker='x')
    plt.title("Stochastic gradient descent: Sum of squared errors (individual updates)")
    plt.show()
    plt.plot(list(map(lambda pair: pair[0], logs_stoch[0::3])), list(map(lambda pair: pair[1], logs_stoch[0::3])),
             marker='o')
    plt.title("Stochastic gradient descent: Weights (individual updates)")
    plt.show()
