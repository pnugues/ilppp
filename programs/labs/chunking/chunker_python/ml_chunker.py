"""
Machine learning chunker for CoNLL 2000
"""
__author__ = "Pierre Nugues"

import time
import conll_reader
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn import linear_model
from sklearn import metrics
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV


def extract_features(sentences, w_size, feature_names):
    """
    Builds X matrix and y vector
    X is a list of dictionaries and y is a list
    :param sentences:
    :param w_size:
    :return:
    """
    X_l = []
    y_l = []
    for sentence in sentences:
        X, y = extract_features_sent(sentence, w_size, feature_names)
        X_l.extend(X)
        y_l.extend(y)
    return X_l, y_l


def extract_features_sent(sentence, w_size, feature_names):
    """
    Extract the features from one sentence
    returns X and y, where X is a list of dictionaries and
    y is a list of symbols
    :param sentence: string containing the CoNLL structure of a sentence
    :param w_size:
    :return:
    """

    # We pad the sentence to extract the context window more easily
    start = "BOS BOS BOS\n"
    end = "\nEOS EOS EOS"
    start *= w_size
    end *= w_size
    sentence = start + sentence
    sentence += end

    # Each sentence is a list of rows
    sentence = sentence.splitlines()
    padded_sentence = list()
    for line in sentence:
        line = line.split()
        padded_sentence.append(line)
    # print(padded_sentence)

    # We extract the features and the classes
    # X contains is a list of features, where each feature vector is a dictionary
    # y is the list of classes
    X = list()
    y = list()
    for i in range(len(padded_sentence) - 2 * w_size):
        # x is a row of X
        x = list()
        # The words in lower case
        for j in range(2 * w_size + 1):
            x.append(padded_sentence[i + j][0].lower())
        # The POS
        for j in range(2 * w_size + 1):
            x.append(padded_sentence[i + j][1])
        # The chunks (Up to the word)
        """
        for j in range(w_size):
            feature_line.append(padded_sentence[i + j][2])
        """
        # We represent the feature vector as a dictionary
        X.append(dict(zip(feature_names, x)))
        # The classes are stored in a list
        y.append(padded_sentence[i + w_size][2])
    return X, y


def predict(test_sentences, feature_names, f_out):
    for test_sentence in test_sentences:
        X_test_dict, y_test = extract_features_sent(test_sentence, w_size, feature_names)
        # Vectorize the test sentence and one hot encoding
        X_test = vec.transform(X_test_dict)
        # Predicts the chunks and returns numbers
        y_test_predicted = classifier.predict(X_test)
        # Appends the predicted chunks as a last column and saves the rows
        rows = test_sentence.splitlines()
        rows = [rows[i] + ' ' + y_test_predicted[i] for i in range(len(rows))]
        for row in rows:
            f_out.write(row + '\n')
        f_out.write('\n')
    f_out.close()


if __name__ == '__main__':
    start_time = time.clock()
    train_corpus = '../../../corpus/conll2000/train.txt'
    test_corpus = '../../../corpus/conll2000/test.txt'
    w_size = 2  # The size of the context window to the left and right of the word
    feature_names = ['word_n2', 'word_n1', 'word', 'word_p1', 'word_p2',
                     'pos_n2', 'pos_n1', 'pos', 'pos_p1', 'pos_p2']

    train_sentences = conll_reader.read_sentences(train_corpus)

    print("Extracting the features...")
    X_dict, y = extract_features(train_sentences, w_size, feature_names)

    print("Encoding the features...")
    # Vectorize the feature matrix and carry out a one-hot encoding
    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(X_dict)
    # The statement below will swallow a considerable memory
    # X = vec.fit_transform(X_dict).toarray()
    # print(vec.get_feature_names())

    training_start_time = time.clock()
    print("Training the model...")
    classifier = linear_model.LogisticRegression(penalty='l2', dual=True, solver='liblinear')
    model = classifier.fit(X, y)
    print(model)

    test_start_time = time.clock()
    # We apply the model to the test set
    test_sentences = list(conll_reader.read_sentences(test_corpus))

    # Here we carry out a chunk tag prediction and we report the per tag error
    # This is done for the whole corpus without regard for the sentence structure
    print("Predicting the chunks in the test set...")
    X_test_dict, y_test = extract_features(test_sentences, w_size, feature_names)
    # Vectorize the test set and one-hot encoding
    X_test = vec.transform(X_test_dict)  # Possible to add: .toarray()
    y_test_predicted = classifier.predict(X_test)
    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(y_test, y_test_predicted)))

    # Here we tag the test set and we save it.
    # This prediction is redundant with the piece of code above,
    # but we need to predict one sentence at a time to have the same
    # corpus structure
    print("Predicting the test set...")
    f_out = open('out', 'w')
    predict(test_sentences, feature_names, f_out)

    end_time = time.clock()
    print("Training time:", (test_start_time - training_start_time) / 60)
    print("Test time:", (end_time - test_start_time) / 60)
