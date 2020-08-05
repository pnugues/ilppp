"""Fibonacci
"""
__author__ = "Pierre Nugues"


def memo_function(f):
    cache = {}

    def memo(x):
        if x in cache:
            return cache[x]
        else:
            cache[x] = f(x)
            return cache[x]

    return memo


@memo_function
def fibonacci(n):
    """
    Fibonacci with memo function
    :param n:
    :return:
    """
    if n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


f_numbers = {}


def fibonacci2(n):
    """
    Fibonacci with memoization. Ad hoc implementation
    :param n:
    :return:
    """
    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n in f_numbers:
        return f_numbers[n]
    else:
        f_numbers[n] = fibonacci2(n - 1) + fibonacci2(n - 2)
        return f_numbers[n]


print(fibonacci(100))
print(fibonacci2(100))
