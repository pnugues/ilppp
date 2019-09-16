# coding=utf-8
"""
A simple POS tagger using a context of five words and logistic regression.
To run the POS tagger, just type
python lr_pos_tagger_simple.py
"""
__author__ = "Pierre Nugues"

import sys
import os
import time
from sklearn.feature_extraction import DictVectorizer
from sklearn import linear_model
import datasets
from context_dictorizer import ContextDictorizer, evaluate

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))

from ch06.python.conll_dictorizer import CoNLLDictorizer

CORPUS = 'EWT'  # or 'PTB'


def predict_sentence(sentence, model,
                     context_dictorizer,
                     dict_vectorizer):
    """
    Prediction using the words (lexical values)
    :param sentence:
    :return:
    """
    X_dict, y = context_dictorizer.transform([sentence],
                                             training_step=False)
    y_pred_vec = []
    for x_dict in X_dict:
        # Vectorize the feature dict
        x_vec = dict_vectorizer.transform(x_dict)
        y_pred = model.predict(x_vec)
        y_pred_vec.append(y_pred[0])

    # We add the predictions in the ppos column
    for row, y_pred in zip(sentence, y_pred_vec):
        row['ppos'] = y_pred
    return sentence


def sentence_to_conll(sentence):
    """
    Convert a sentence to a CoNLL dict
    :param sentence:
    :return:
    """
    column_names = ['id', 'form']
    sentence = list(enumerate(sentence.split(), start=1))
    conll_cols = ''
    for tuple in sentence:
        conll_cols += str(tuple[0]) + '\t' + tuple[1] + '\n'

    conll_dict = CoNLLDictorizer(column_names)
    sent_dict = conll_dict.transform(conll_cols)
    return sent_dict[0]


if __name__ == '__main__':
    start_time = time.perf_counter()
    if CORPUS == 'EWT':
        train_sentences, dev_sentences, test_sentences, column_names = datasets.load_ud_en_ewt()
    else:
        train_sentences, dev_sentences, test_sentences, column_names = datasets.load_conll2009_pos()

    conll_dict = CoNLLDictorizer(column_names)
    train_dict = conll_dict.transform(train_sentences)
    print(train_dict[0])

    context_dictorizer = ContextDictorizer(w_size=2)
    context_dictorizer.fit(train_dict)
    # Feature and response extraction
    X_dict, y = context_dictorizer.transform(train_dict)
    print(X_dict[0])
    print(y[0])

    # We print the features to check they match Table 8.1 in my book (second edition)
    # We use the training step extraction with the dynamic features
    context_dictorizer.print_example(train_dict)

    # We transform the symbols into numbers
    print('Vectorizing the features...')
    dict_vectorizer = DictVectorizer()
    X = dict_vectorizer.fit_transform(X_dict)

    print('Fitting the model...')
    classifier = linear_model.LogisticRegression(multi_class='auto',
                                                 solver='lbfgs')
    model = classifier.fit(X, y)
    print(model)

    # Prediction
    test_dict = conll_dict.transform(test_sentences)
    print(train_dict[0])

    print("Predicting the test set...")
    for sentence in test_dict:
        sentence = predict_sentence(sentence,
                                    model,
                                    context_dictorizer,
                                    dict_vectorizer)

    good, bad = evaluate(test_dict, 'pos', 'ppos')
    print('Accuracy, lexical model:', good / (good + bad))

    # Tag sentences
    sentences = ['That round table might collapse .',
                 'The man can learn well .',
                 'The man can swim .',
                 'The man can simwo .',
                 'that round table might collapsex']
    for sentence in sentences:
        sentence = sentence_to_conll(sentence.lower())
        y_test_pred_cat = predict_sentence(sentence,
                                           model,
                                           context_dictorizer,
                                           dict_vectorizer)
        print([y['form'] for y in y_test_pred_cat])
        print([y['ppos'] for y in y_test_pred_cat])

    print('Elapsed time:', time.perf_counter() - start_time)

    """
    Results:
    Penn Treebank
    Accuracy, lexical model (dual):         (lbfgs)
    width 1: 0.950690061724114              0.9416915181357931
    width 2: 0.9549726055898468 **          0.9462688119841876
    width 3: 0.954296414453152              0.9464942090297525 *
    width 4: 0.9529960468825854             0.9453845620362022             
    
    UD en_ewt (liblinear, dual)             (lbfgs)
    width 1: 0.8973980953898872             0.8968004143921584
    width 2: 0.9012630991752002 *           0.9033749053671754 **     
    width 3: 0.8984340757859505             0.8994700561820138
    width 4: 0.8973184045901901             0.8987129935848907
    """
