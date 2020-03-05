"""Gradient descent for linear regression
"""

__author__ = 'Pierre Nugues'

import random
import vector
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
    error = vector.sub(y, vector.mul_mat_vec(X, w))
    return vector.dot(error, error)


def normalize(observations):
    maxima = [max([obs[i] for obs in observations]) for i in range(len(observations[0]))]
    return ([[obs[i] / maxima[i]
              for i in range(len(observations[0]))] for obs in observations],
            maxima)


def predict(X, w):
    return vector.mul_mat_vec(X, w)


def fit_stoch(X, y, alpha, w,
              epochs=500,
              epsilon=1.0e-5):
    """
    Stochastic gradient descent
    :param X:
    :param y:
    :param alpha:
    :param w:
    :param epochs:
    :param epsilon:
    :return:
    """
    global logs, logs_stoch
    logs = []
    logs_stoch = []
    random.seed(0)
    idx = list(range(len(X)))
    for epoch in range(epochs):
        random.shuffle(idx)
        for i in idx:
            y_hat = predict([X[i]], w)[0]
            loss = y[i] - y_hat
            gradient = vector.mul(loss, X[i])
            w = vector.add(w, vector.mul(alpha, gradient))
            logs_stoch += (w, alpha, sse(X, y, w))
        if vector.norm(gradient) < epsilon:
            print('Gradient', vector.norm(gradient))
            break
        logs += (w, alpha, sse(X, y, w))
    print("Epoch", epoch)
    return w


def fit_batch(X, y, alpha, w,
              epochs=500,
              epsilon=1.0e-5):
    """
    Batch gradient descent
    :param X:
    :param y:
    :param alpha:
    :param w:
    :param epochs:
    :param epsilon:
    :return:
    """
    global logs
    logs = []
    alpha /= len(X)
    for epoch in range(epochs):
        y_hat = predict(X, w)
        loss = vector.sub(y, y_hat)
        gradient = vector.mul_mat_vec(vector.transpose(X), loss)
        w = vector.add(w, vector.mul(alpha, gradient))
        logs += (w, alpha, sse(X, y, w))
        if vector.norm(gradient) < epsilon:
            break
    print("Epoch", epoch)
    return w


if __name__ == '__main__':
    normalized = True
    debug = False
    X, y = datasets.load_tsv(
        'https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')

    alpha = 1.0e-10
    if normalized:
        X, maxima_X = normalize(X)
        maxima_y = max(y)
        y = [yi / maxima_y for yi in y]
        maxima = maxima_X + [maxima_y]
        alpha = 1.0
        print("-Normalized-")

    print("===Batch descent===")
    w = [0.0] * (len(X))
    w = fit_batch(X, y, alpha, w)
    print("Weights", w)
    print("SSE", sse(X, y, w))
    if normalized:
        print("Restored weights", [w[i] * maxima[-1] / maxima[i] for i in range(len(w))])
    if debug:
        print("Logs", logs)
    plt.scatter(range(len(logs[2::3])), logs[2::3], c='b', marker='x')
    plt.title("Batch gradient descent: Sum of squared errors")
    plt.show()
    plt.plot(list(map(lambda pair: pair[0], logs[0::3])),
             list(map(lambda pair: pair[1], logs[0::3])),
             marker='o')
    for i in range(len(logs[0::3])):
        plt.annotate(i, xy=logs[0::3][i])
    plt.title("Batch gradient descent: Weights")
    plt.show()

    print("===Stochastic descent===")
    w = [0.0] * (len(X))
    w = fit_stoch(X, y, alpha, w)
    print("Weights", w)
    print("SSE", sse(X, y, w))
    if normalized:
        print("Restored weights", [w[i] * maxima[-1] / maxima[i] for i in range(len(w))])
    if debug:
        print("Logs", logs)
        print("Logs stoch.", logs_stoch)
    plt.scatter(range(len(logs[2::3])), logs[2::3], c='b', marker='x')
    plt.title("Stochastic gradient descent: Sum of squared errors")
    plt.show()
    plt.plot(list(map(lambda pair: pair[0], logs[0::3])),
             list(map(lambda pair: pair[1], logs[0::3])),
             marker='o')
    for i in range(len(logs[0::3])):
        plt.annotate(i, xy=logs[0::3][i])
    plt.title("Stochastic gradient descent: Weights")
    plt.show()
    plt.scatter(range(len(logs_stoch[2::3])),
                logs_stoch[2::3],
                c='b', marker='x')
    plt.title("Stochastic gradient descent: Sum of squared errors (individual updates)")
    plt.show()
    plt.plot(list(map(lambda pair: pair[0], logs_stoch[0::3])),
             list(map(lambda pair: pair[1], logs_stoch[0::3])),
             marker='o')
    plt.title("Stochastic gradient descent: Weights (individual updates)")
    plt.show()
