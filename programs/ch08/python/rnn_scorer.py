"""
Scoring functions for RNNs
__author__ = "Pierre Nugues"
"""


def eval(X_test_cat, Y_test_cat, Y_test_pred, word2idx):
    total, correct, total_ukn, correct_ukn = 0, 0, 0, 0
    for id_s, x_test_cat in enumerate(X_test_cat):
        for id_w, word in enumerate(x_test_cat):
            total += 1
            if Y_test_pred[id_s][id_w] == Y_test_cat[id_s][id_w]:
                correct += 1
            # The word is not in the dictionary
            if word not in word2idx:
                total_ukn += 1
                if Y_test_pred[id_s][id_w] == Y_test_cat[id_s][id_w]:
                    correct_ukn += 1
    return total, correct, total_ukn, correct_ukn
