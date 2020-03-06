"""
Fitting a classifier with scikit learn for the Salammbo dataset
"""
__author__ = "Pierre Nugues"

import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import cross_val_score, LeaveOneOut

# We load the dataset from a file with the svmlight format
X, y = load_svmlight_file('../salammbo/salammbo_a_binary.libsvm')
print(type(X))
print(X)
print(type(y))
print(y)

# Or we create it using numpy arrays
y = np.array(
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

X = np.array(
    [[35680, 2217], [42514, 2761], [15162, 990], [35298, 2274],
     [29800, 1865], [40255, 2606], [74532, 4805], [37464, 2396],
     [31030, 1993], [24843, 1627], [36172, 2375], [39552, 2560],
     [72545, 4597], [75352, 4871], [18031, 1119], [36961, 2503],
     [43621, 2992], [15694, 1042], [36231, 2487], [29945, 2014],
     [40588, 2805], [75255, 5062], [37709, 2643], [30899, 2126],
     [25486, 1784], [37497, 2641], [40398, 2766], [74105, 5047],
     [76725, 5312], [18317, 1215]
     ])

# We create a classifier and learn a model
classifier = LogisticRegression()
model = classifier.fit(X, y)
print('Model:', model)

# We predict the training set
# As classes
y_hat = classifier.predict(X)
print('Class predictions:', y_hat)

# With probabilities
y_predicted = classifier.predict_proba(X)
print('Class predictions with probabilities:\n', y_predicted)

print('Model weights:', classifier.intercept_, classifier.coef_)

print('Prediction of the last observation: {},\n class: {}'.format(
    [X[-1]],
    classifier.predict([X[0]])[0]))
print('Prediction of the observation: {},\n class: {}'.format(
    [35680, 2217],
    classifier.predict(np.array([[35680, 2217]]))[0]))

# We evaluate the model on the training set
print("Classification report for classifier on the training set:\n",
      metrics.classification_report(y, y_hat))

# We evaluate the classifier with cross validation
scores = cross_val_score(classifier, X, y, cv=5,
                         scoring='accuracy')
print('Five-fold crossvalidation accuracy:', scores.mean())

# We evaluate the classifier with leave-one-out cross validation
loo = LeaveOneOut()
predictions = 0
correct_predictions = 0
for train_index, test_index in loo.split(X):
    predictions += 1
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    classifier.fit(X_train, y_train)
    if classifier.predict(X_test)[0] == y_test:
        correct_predictions += 1
print('Leave-one-out crossvalidation accuracy:', correct_predictions / predictions)
