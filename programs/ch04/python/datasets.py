"""
Reader of libsvm format
"""
__author__ = 'Pierre Nugues'
import numpy as np
from urllib.request import urlopen


def read_libsvm_file(file_path):
    """
    Read a libsvm file. The format is not sparse
    :param file_path:
    :return: X, y as lists
    """
    data = open(file_path).read().strip().split('\n')
    observations = [data[i].split() for i in range(len(data))]

    y = [float(obs[0]) for obs in observations]
    # We add the intercept
    X = [['0:1'] + obs[1:] for obs in observations]
    X = [list(map(lambda x: float(x.split(':')[1]), obs)) for obs in X]
    return X, y


def read_array_from_tsv(file_path):
    """
    Read a tsv file. The response is the last column
    :param file_path:
    :return: X, y as np.array
    """
    observations = open(file_path).read().strip().split('\n')
    observations = [list(map(float, obs.split())) for obs in observations]
    X = np.array(observations)[:, :-1]
    X = np.hstack((np.ones((len(X), 1)), X))
    y = np.array(observations)[:, -1]
    return X, y


def read_tsv(file_path):
    """
    Read a tsv file. The response is the last column
    :param file_path:
    :return: X, y as lists
    """
    observations = open(file_path).read().strip().split('\n')
    observations = [[1] + list(map(float, obs.split())) for obs in observations]
    X = [obs[:-1] for obs in observations]
    y = [obs[-1] for obs in observations]
    return X, y


def load_tsv(file):
    observations = urlopen(file).read().decode('utf-8').strip().split('\n')
    observations = [[1] + list(map(float, obs.split())) for obs in observations]
    X = [obs[:-1] for obs in observations]
    y = [obs[-1] for obs in observations]
    return X, y


if __name__ == '__main__':
    X, y = read_tsv('../salammbo/salammbo_a_en.tsv')
    print('X:', X)
    print('y:', y)
    X, y = load_tsv('https://raw.githubusercontent.com/pnugues/ilppp/master/programs/ch04/salammbo/salammbo_a_en.tsv')
    print('X:', X)
    print('y:', y)
    X, y = read_libsvm_file('../salammbo/salammbo_a_e_binary.libsvm')
    print('X:', X)
    print('y:', y)
