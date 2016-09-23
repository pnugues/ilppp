"""
Transitions for Nivre's parser
The data structures consist of the stack, the queue, and the parser state
The parser state is represented as a dictionary
"""

__author__ = "Pierre Nugues"

import conll
import dparser


def shift(stack, queue, state):
    """
    Shift the first word in the queue onto the stack
    :param stack:
    :param queue:
    :param state:
    :return:
    """
    stack = [queue[0]] + stack
    queue = queue[1:]
    return stack, queue, state


def reduce(stack, queue, state):
    """
    Remove the first item from the stack
    :param stack:
    :param queue:
    :param state:
    :return:
    """
    return stack[1:], queue, state


def right_arc(stack, queue, state, deprel=False):
    """
    Creates an arc from the top of the stack to the first in the queue
    and shifts
    The deprel argument is either read from the manually-annotated corpus
    (deprel=False) or assigned by the parser. In this case, the deprel
    argument has a value
    :param stack:
    :param queue:
    :param state:
    :param deprel: either read from the manually-annotated corpus (value false)
    or assigned by the parser
    :return:
    """
    state['heads'][queue[0]['id']] = stack[0]['id']
    if deprel:
        state['deprels'][queue[0]['id']] = deprel
    else:
        state['deprels'][queue[0]['id']] = queue[0]['deprel']
    return shift(stack, queue, state)


def left_arc(stack, queue, state, deprel=False):
    """
    Creates an arc from the first in the queue to the top of the stack
    and reduces it.
    The deprel argument is either read from the manually-annotated corpus
    (deprel=False) or assigned by the parser. In this case, the deprel
    argument has a value
    :param stack:
    :param queue:
    :param state:
    :param deprel: either read from the manually-annotated corpus (value false)
    or assigned by the parser
    :return:
    """
    state['heads'][stack[0]['id']] = queue[0]['id']
    if deprel:
        state['deprels'][stack[0]['id']] = deprel
    else:
        state['deprels'][stack[0]['id']] = stack[0]['deprel']
    return reduce(stack, queue, state)


def can_reduce(stack, state):
    """
    Checks that the top of the stack has a head
    :param stack:
    :param state:
    :return:
    """
    if not stack:
        return False
    if stack[0]['id'] in state['heads']:
        return True
    else:
        return False


def can_leftarc(stack, state):
    """
    Checks that the top of the has no head
    :param stack:
    :param state:
    :return:
    """
    if not stack:
        return False
    if stack[0]['id'] in state['heads']:
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


def empty_stack(stack, state):
    """
    Pops the items in the stack. If they have no head, they are assigned
    a ROOT head
    :param stack:
    :param state:
    :return:
    """
    for word in stack:
        if word['id'] not in state['heads']:
            state['heads'][word['id']] = '0'
            state['deprels'][word['id']] = 'ROOT'
    stack = []
    return stack, state


def equal_graphs(sentence, state):
    """
    Checks that the state corresponds to the gold standard annotation of a sentence
    :param sentence:
    :param state:
    :return:
    """
    equal = True
    for word in sentence:
        if word['id'] in state['heads'] and word['head'] == state['heads'][word['id']]:
            pass
        else:
            print(word, flush=True)
            equal = False
    return equal


if __name__ == '__main__':
    pass
