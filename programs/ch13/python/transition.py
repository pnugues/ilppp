"""
Transitions for Nivre's parser
The parser state consists of the stack, the queue, and the partial graph
The partial graph is represented as a dictionary
"""

__author__ = "Pierre Nugues"

import conll
import dparser


def shift(stack, queue, graph):
    """
    Shift the first word in the queue onto the stack
    :param stack:
    :param queue:
    :param graph:
    :return:
    """
    stack = [queue[0]] + stack
    queue = queue[1:]
    return stack, queue, graph


def reduce(stack, queue, graph):
    """
    Remove the first item from the stack
    :param stack:
    :param queue:
    :param graph:
    :return:
    """
    return stack[1:], queue, graph


def right_arc(stack, queue, graph, deprel=False):
    """
    Creates an arc from the top of the stack to the first in the queue
    and shifts
    The deprel argument is either read from the manually-annotated corpus
    (deprel=False) or assigned by the parser. In this case, the deprel
    argument has a value
    :param stack:
    :param queue:
    :param graph:
    :param deprel: either read from the manually-annotated corpus (value false)
    or assigned by the parser
    :return:
    """
    graph['heads'][queue[0]['id']] = stack[0]['id']
    if deprel:
        graph['deprels'][queue[0]['id']] = deprel
    else:
        graph['deprels'][queue[0]['id']] = queue[0]['deprel']
    return shift(stack, queue, graph)


def left_arc(stack, queue, graph, deprel=False):
    """
    Creates an arc from the first in the queue to the top of the stack
    and reduces it.
    The deprel argument is either read from the manually-annotated corpus
    (deprel=False) or assigned by the parser. In this case, the deprel
    argument has a value
    :param stack:
    :param queue:
    :param graph:
    :param deprel: either read from the manually-annotated corpus (value false)
    or assigned by the parser
    :return:
    """
    graph['heads'][stack[0]['id']] = queue[0]['id']
    if deprel:
        graph['deprels'][stack[0]['id']] = deprel
    else:
        graph['deprels'][stack[0]['id']] = stack[0]['deprel']
    return reduce(stack, queue, graph)


def can_reduce(stack, graph):
    """
    Checks that the top of the stack has a head
    :param stack:
    :param graph:
    :return:
    """
    if not stack:
        return False
    if stack[0]['id'] in graph['heads']:
        return True
    else:
        return False


def can_leftarc(stack, graph):
    """
    Checks that the top of the has no head
    :param stack:
    :param graph:
    :return:
    """
    if not stack:
        return False
    if stack[0]['id'] in graph['heads']:
        return False
    else:
        return True


def can_rightarc(stack):
    """
    Simply checks there is a stack
    :param stack:
    :return:
    """
    if not stack:
        return False
    else:
        return True


def empty_stack(stack, graph):
    """
    Pops the items in the stack. If they have no head, they are assigned
    a ROOT head
    :param stack:
    :param graph:
    :return:
    """
    for word in stack:
        if word['id'] not in graph['heads']:
            graph['heads'][word['id']] = '0'
            graph['deprels'][word['id']] = 'ROOT'
    stack = []
    return stack, graph


def equal_graphs(sentence, graph):
    """
    Checks that the graph corresponds to the gold standard annotation of a sentence
    :param sentence:
    :param graph:
    :return:
    """
    equal = True
    for word in sentence:
        if word['id'] in graph['heads'] and word['head'] == graph['heads'][word['id']]:
            pass
        else:
            print(word, flush=True)
            equal = False
    return equal


if __name__ == '__main__':
    pass
