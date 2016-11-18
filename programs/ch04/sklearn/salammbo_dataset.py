"""
Fitting a classifier with scikit learn for the Salammbo dataset
"""
__author__ = "Pierre Nugues"

import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn import linear_model
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score

# We load the dataset from a file with the svmlight format
X_train, y_train = load_svmlight_file('../salammbo/salammbo_a_binary.libsvm')
print(type(X_train))
print(X_train)
print(type(y_train))
print(y_train)

# Or we create it using numpy arrays
y_train = np.array(
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

X_train = np.array(
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
classifier = linear_model.LogisticRegression()
model = classifier.fit(X_train, y_train)
print(model)

# We predict the training set or observations
y_test_predicted = classifier.predict(X_train)
print(y_test_predicted)
print(classifier.predict([X_train[0]]))
print(classifier.predict(np.array([[35680, 2217]])))

# We evaluate the classifier with cross validation
scores = cross_val_score(classifier, X_train, y_train, cv=5,
                         scoring='accuracy')
print('Score', scores.mean())

print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(y_train, y_test_predicted)))

