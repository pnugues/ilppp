"""
Predicting the Salammbô dataset with a logistic function
Scaling is very significant
Author: Pierre Nugues
"""

from keras import models
from keras import layers
from sklearn.preprocessing import StandardScaler, Normalizer
import numpy as np

simple_model = True
verbose = False

# The Data
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

y = np.array(
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

print('Standardizing the data')
mean = np.mean(X[:, 1])
std = np.std(X[:, 1])
print('Mean A:', mean, 'Std A:', std)
print('Original:', X[15, 1], 'Standardized:', (X[15, 1] - mean) / std)
X_norm = Normalizer().fit_transform(X)
X_scaled = StandardScaler().fit_transform(X_norm)

# The network
np.random.seed(0)
model = models.Sequential()

if simple_model:
    model.add(layers.Dense(1, input_dim=2, activation='sigmoid'))
else:
    model.add(layers.Dense(10, input_dim=2, activation='relu'))
    # model.add(layers.Dropout(0.5))
    model.add(layers.Dense(1, activation='sigmoid'))

# Fitting the network
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.fit(X_scaled, y, epochs=10, batch_size=1)

y_predicted = model.predict(X_scaled)
print(y_predicted)

# evaluate the model
scores = model.evaluate(X_scaled, y)
print(scores)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

if verbose:
    print(model.get_weights())
