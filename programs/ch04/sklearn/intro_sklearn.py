from sklearn import datasets
from sklearn import svm

iris = datasets.load_iris()
digits = datasets.load_digits()

print(digits.data)
print(digits.target)
print(digits.images[0])

print(digits)

clf = svm.SVC(gamma=0.001, C=100.)
model = clf.fit(digits.data[:-1], digits.target[:-1])
print(clf)
print(model)
clf.predict(digits.data[-1:])

from sklearn import svm
from sklearn import datasets

clf = svm.SVC()
iris = datasets.load_iris()
X, y = iris.data, iris.target
model = clf.fit(X, y)

import pickle

s = pickle.dumps(clf)
clf2 = pickle.loads(s)
print(clf2.predict(X[0:1]))
print(y[0])

from sklearn.externals import joblib

joblib.dump(clf, 'filename.pkl')
clf3 = joblib.load('filename.pkl')
print(clf3.predict(X[0:1]))
print(y[0])
