# coding=utf-8
"""
Feature extractors.
"""
__author__ = "Pierre Nugues"

import sys
import os
from sklearn.feature_extraction import DictVectorizer
from sklearn import linear_model
import time
import datasets
from context_dictorizer import ContextDictorizer, evaluate

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))

from ch06.python.conll_dictorizer import CoNLLDictorizer


def predict(test_sentence, context_dictorizer, dict_vectorizer):
    """
    Prediction using the words (lexical values)
    :param test_sentence:
    :return:
    """
    X_dict, y = context_dictorizer.transform([test_sentence], training_step=False)
    y_pred_vec = []
    for x_dict in X_dict:
        # Vectorize the feature dict
        x_vec = dict_vectorizer.transform(x_dict)
        y_pred = classifier.predict(x_vec)
        y_pred_vec.append(y_pred[0])
    # print('X', X_test_dict)
    rows = test_sentence
    # We add the predictions in the ppos column
    for row, y_pred in zip(rows, y_pred_vec):
        row['ppos'] = y_pred
    return test_sentence


if __name__ == '__main__':
    # Universal dependencies otherwise, Penn Treebank
    UD = True
    start_time = time.clock()

    if UD:
        train_sentences, dev_sentences, test_sentences, column_names = datasets.load_internet_ud_en_ewt()
    else:
        train_sentences, dev_sentences, test_sentences, column_names = datasets.load_conll2009_pos()

    conll_dict = CoNLLDictorizer(column_names, col_sep='\t')
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])

    if UD:
        context_dictorizer = ContextDictorizer(output='upos')
    else:
        context_dictorizer = ContextDictorizer()
    context_dictorizer.fit(train_dict)

    # We print the features to check they match Table 8.1 in my book (second edition)
    # We use the training step extraction with the dynamic features
    context_dictorizer.print_example(train_dict)

    # Feature and response extraction
    X_dict, y = context_dictorizer.transform(train_dict)
    print(X_dict[0])
    print(y[0])

    # We transform the symbols into numbers
    print('Vectorizing the features...')
    dict_vectorizer = DictVectorizer(sparse=True)
    X = dict_vectorizer.fit_transform(X_dict)

    print('Fitting the model...')
    classifier = linear_model.LogisticRegression(dual=True)
    model = classifier.fit(X, y)
    print(model)

    # Prediction
    test_dict = conll_dict.transform(test_sentences)
    print(train_dict[0])

    print("Predicting the test set...")
    for test_sentence in test_dict:
        test_sentence = predict(test_sentence, context_dictorizer, dict_vectorizer)

    if UD:
        good, bad = evaluate(test_dict, 'upos', 'ppos')
    else:
        good, bad = evaluate(test_dict, 'pos', 'ppos')
    print('Accuracy, lexical model:', good / (good + bad))
    print('Elapsed time:', time.clock() - start_time)

    """
    Penn Treebank
    Accuracy, lexical model (dual):
    width 1: 0.950690061724114
    width 2: 0.9549726055898468 *
    width 3: 0.954296414453152
    width 4: 0.9529960468825854
    
    UD en_ewt
    width 1: 0.8973980953898872
    width 2: 0.9012630991752002 *
    width 3: 0.8984340757859505
    width 4: 0.8973184045901901
    """
