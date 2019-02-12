"""
Preprocessing functions for RNNs
__author__ = "Pierre Nugues"
"""


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


def to_char_index(X, idx, UKN_IDX=1):
    """
    Convert the word lists (or POS lists) to char indexes
    :param X: List of word (or POS) lists
    :param idx: char to number dictionary
    :return: A list of x, where x is a list of char lists
    """
    X_idx = []
    for xl in X:
        # We map the unknown symbols to one
        x_idx = [list(map(lambda x: idx.get(x, UKN_IDX), list(x))) for x in xl]
        X_idx += [x_idx]
    return X_idx


if __name__ == '__main__':
    X = [['the', 'big', 'cat'],
         ['a', 'small', 'mouse']]
    words = [w for l in X for w in l]
    characters = []
    for word in words:
        characters.extend(word)
    characters = sorted(list(set(characters)))
    idx2char = dict(enumerate(characters, start=1))
    char2idx = {v: k for k, v in idx2char.items()}
    print(idx2char)
    print(char2idx)
    print(to_char_index(X, char2idx))