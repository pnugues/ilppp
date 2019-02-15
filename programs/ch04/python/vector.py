"""
Elementary vector and matrix operations
"""
import math

__author__ = 'Pierre Nugues'


def add(u, v):
    """
    Addition of vectors: u + v
    :param u:
    :param v:
    :return:
    """
    return [u_i + v_i for u_i, v_i in zip(u, v)]


def sub(u, v):
    """
    Vector subtraction:  u - v
    :param u:
    :param v:
    :return:
    """
    return [u_i - v_i for u_i, v_i in zip(u, v)]


def mul(alpha, v):
    """
    Vector multiplication by a scalar: alpha . u
    :param alpha:
    :param v:
    :return:
    """
    return [alpha * v_i for v_i in v]


def dot(u, v):
    """
    Dot product of two vectors: u . v
    :param u:
    :param v:
    :return:
    """
    return sum([u_i * v_i for u_i, v_i in zip(u, v)])


def norm(v):
    """
    Euclidean norm of a vector ||v||2
    :param v:
    :return:
    """
    return math.sqrt(dot(v, v))


def norm1(v):
    """
    Norm of a vector with d1 ||v||1
    :param v:
    :return:
    """
    return sum([math.fabs(coord) for coord in v])


def heaviside(v):
    """
    Heaviside function: H(v)
    :param v:
    :return:
    """
    return [1 if coord >= 0 else 0 for coord in v]


def cosine(u, v):
    """
    Cosine of two vectors
    :param u:
    :param v:
    :return:
    """
    return dot(u, v) / (norm(u) * norm(v))


def mul_mat(alpha, M):
    """
    Multiplication of a matrix by a scalar alpha M
    :param alpha:
    :param M:
    :return:
    """
    return [mul(alpha, row) for row in M]


def mul_mat_vec(M, v):
    """
    Matrix vector multiplication: Mv
    :param M:
    :param v:
    :return:
    """
    return [dot(row, v) for row in M]


def mul_mat_mat(M, N):
    """
    Matrix multiplication: MN
    :param M:
    :param N:
    :return:
    """
    return [mul_mat_vec(M, column(N, i)) for i in range(len(N[0]))]


def transpose(M):
    """
    Transpose of a matrix Mt
    :param M:
    :return:
    """
    return [column(M, i) for i in range(len(M[0]))]


def column(M, i):
    """
    Extraction of column i of a matrix
    :param M:
    :param i:
    :return:
    """
    return [row[i] for row in M]


if __name__ == '__main__':
    print(norm([1, 1]))
    print(norm1([1, 1]))
    print(heaviside([-1.4, 0, 2, -9]))
    print(transpose([[1, 3], [2, 4]]))
    print(column([[1, 3, 5], [2, 4, 8], [1, 7, 2]], 1))
    print(column([[1, 3, 5], [2, 4, 8], [1, 7, 2]], -1))
    print(column([[1, 3, 5], [2, 4, 8], [1, 7, 2]], slice(0, -1, 1)))
    print(mul_mat(3, [[1, 2], [2, 4]]))
    print(mul_mat_vec([[1, 2], [2, 4]], [2, 3]))
    print(mul_mat_mat([[1, 2], [2, 4]], [[1, 3], [2, 4]]))
    print(mul_mat_mat([[1, 2, 3]], [[1, 3], [2, 4], [1, 7]]))
