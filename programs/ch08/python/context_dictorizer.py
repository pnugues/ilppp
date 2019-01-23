# coding=utf-8
"""
CoNLL context dictorizers for the parts of speech that creates word windows of a certain size
"""
__author__ = "Pierre Nugues"
import sys
import os
import math
import datasets

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))

# sys.path.append('/Users/pierre/Documents/Cours/EDAN20/programs/')

from ch06.python.conll_dictorizer import CoNLLDictorizer, Token


class ContextDictorizer():
    """
    Extract contexts of words in a sequence
    Contexts are of w_size to the left and to the right
    Builds an X matrix in the form of a dictionary
    and possibly extracts the output, y, if not in the test step
    If the test_step is True, returns y = []
    """

    def __init__(self, input='form', output='pos', w_size=2, tolower=True):
        self.BOS_symbol = '__BOS__'
        self.EOS_symbol = '__EOS__'
        self.input = input
        self.output = output
        self.w_size = w_size
        self.tolower = tolower
        # To be sure the names are ordered
        zeros = math.ceil(math.log10(2 * w_size + 1))
        self.feature_names = [input + '_' + str(i).zfill(zeros) for i in range(2 * w_size + 1)]

    def fit(self, sentences):
        """
        Build the padding rows
        :param sentences:
        :return:
        """
        self.column_names = sentences[0][0].keys()
        start = [self.BOS_symbol] * len(self.column_names)
        end = [self.EOS_symbol] * len(self.column_names)
        start_token = Token(dict(zip(self.column_names, start)))
        end_token = Token(dict(zip(self.column_names, end)))
        self.start_rows = [start_token] * self.w_size
        self.end_rows = [end_token] * self.w_size

    def transform(self, sentences, training_step=True):
        X_corpus = []
        y_corpus = []
        for sentence in sentences:
            X, y = self._transform_sentence(sentence, training_step)
            X_corpus += X
            if training_step:
                y_corpus += y
        return X_corpus, y_corpus

    def fit_transform(self, sentences):
        self.fit(sentences)
        return self.transform(sentences)

    def _transform_sentence(self, sentence, training_step=True):
        # We extract y
        if training_step:
            y = [row[self.output] for row in sentence]
        else:
            y = None

        # We pad the sentence
        sentence = self.start_rows + sentence + self.end_rows

        # We extract the features
        X = list()
        for i in range(len(sentence) - 2 * self.w_size):
            # x is a row of X
            x = list()
            # The words in lower case
            for j in range(2 * self.w_size + 1):
                if self.tolower:
                    x.append(sentence[i + j][self.input].lower())
                else:
                    x.append(sentence[i + j][self.input])
            # We represent the feature vector as a dictionary
            X.append(dict(zip(self.feature_names, x)))
        return X, y

    def print_example(self, sentences, id=1968):
        """
        :param corpus:
        :param id:
        :return:
        """
        # We print the features to check they match Table 8.1 in my book (second edition)
        # We use the training step extraction with the dynamic features
        Xs, ys = self._transform_sentence(sentences[id])
        print('X for sentence #', id, Xs)
        print('y for sentence #', id, ys)


def evaluate(sentences, gold, system):
    """
    Computes the accuracy
    :param sentences:
    :param gold:
    :param system:
    :return:
    """
    bad = 0
    good = 0
    for sentence in sentences:
        for word in sentence:
            if word[gold] == word[system]:
                good += 1
            else:
                bad += 1
    return good, bad


if __name__ == '__main__':
    train_sentences, dev_sentences, test_sentences, column_names = datasets.load_conll2009_pos()

    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])

    good, bad = evaluate(train_dict, 'pos', 'ppos')
    print('Accuracy:', good / (good + bad))

    context_dictorizer = ContextDictorizer()
    context_dictorizer.fit(train_dict)
    X_dict, y = context_dictorizer.transform(train_dict)

    print(X_dict[0])
    print(y[0])
    context_dictorizer.print_example(train_dict)

    test_file2 = 'simple_pos_test.txt'
    test2 = open(test_file2).read().strip()
    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(test2)
    print(train_dict[0])

    context_dictorizer = ContextDictorizer()
    context_dictorizer.fit(train_dict)
    X_dict, y = context_dictorizer.transform(train_dict)

    print(X_dict[0])
    print(y[0])

    train_sentences, dev_sentences, test_sentences, column_names = datasets.load_internet_ud_en_ewt()

    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])

    context_dictorizer = ContextDictorizer(input='form', output='upos')
    context_dictorizer.fit(train_dict)
    X_dict, y = context_dictorizer.transform(train_dict)

    print(X_dict[0])
    print(y[0])
    context_dictorizer.print_example(train_dict)
