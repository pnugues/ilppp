"""
Preprocessing functions for RNNs
__author__ = "Pierre Nugues"
"""
from keras.preprocessing.sequence import pad_sequences


def build_sequences(corpus_dict,
                    key_x='form',
                    key_y='pos',
                    tolower=True):
    """
    Creates prarallel sequences from a list of dictionaries
    :param corpus_dict:
    :param key_x:
    :param key_y:
    :return:
    """
    X = []
    Y = []
    for sentence in corpus_dict:
        x = [word[key_x] for word in sentence]
        y = [word[key_y] for word in sentence]
        if tolower:
            x = list(map(str.lower, x))
        X += [x]
        Y += [y]
    return X, Y


def to_index(X, idx, UKN_IDX=1):
    """
    Convert the word lists (or POS lists) to indexes
    :param X: List of word (or POS) lists
    :param idx: word to number dictionary
    :return:
    """
    X_idx = []
    for x in X:
        # We map the unknown symbols to one
        x_idx = list(map(lambda x: idx.get(x, UKN_IDX), x))
        X_idx += [x_idx]
    return X_idx


def to_char_index(X, idx, MAX_LEN_CHARS):
    """
    Convert the word lists (or POS lists) to char indexes
    :param X: List of word (or POS) lists
    :param idx: word to number dictionary
    :return:
    """
    X_idx = []
    for xl in X:
        # We map the unknown symbols to one
        x_idx = [list(map(lambda x: idx.get(x, 1), list(x))) for x in xl]
        x_idx = pad_sequences(x_idx, maxlen=MAX_LEN_CHARS)
        X_idx += [x_idx]
    return X_idx
