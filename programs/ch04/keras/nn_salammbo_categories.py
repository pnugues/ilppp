"""
Predicting the Salammbô dataset with categories and softmax
Scaling is very significant
Author: Pierre Nugues
"""
from keras import models
from keras import layers
from sklearn.preprocessing import StandardScaler, Normalizer
import numpy as np
import keras.utils

simple_model = True
standardize = True
optimizer = 'sgd'
verbose = True

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

"""
X = np.array(
    [[35680, 2217, 1], [42514, 2761, 1], [15162, 990, 1], [35298, 2274, 1],
     [29800, 1865, 1], [40255, 2606, 1], [74532, 4805, 1], [37464, 2396, 1],
     [31030, 1993, 1], [24843, 1627, 1], [36172, 2375, 1], [39552, 2560, 1],
     [72545, 4597, 1], [75352, 4871, 1], [18031, 1119, 1], [36961, 2503, 1],
     [43621, 2992, 1], [15694, 1042, 1], [36231, 2487, 1], [29945, 2014, 1],
     [40588, 2805, 1], [75255, 5062, 1], [37709, 2643, 1], [30899, 2126, 1],
     [25486, 1784, 1], [37497, 2641, 1], [40398, 2766, 1], [74105, 5047, 1],
     [76725, 5312, 1], [18317, 1215, 1]
     ])

"""

y = np.array(
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
y_one_hot_labels = keras.utils.to_categorical(y, num_classes=2)
print(y_one_hot_labels)

if standardize:
    print('Standardizing the data')
    mean = np.mean(X[:, 1])
    std = np.std(X[:, 1])
    print('Mean A:', mean, 'Std A:', std)
    print('Original:', X[15, 1], 'Standardized:', (X[15, 1] - mean) / std)
    X_norm = Normalizer().fit_transform(X)
    X_scaled = StandardScaler().fit_transform(X_norm)
else:
    X_scaled = X

# The network
np.random.seed(0)
model = models.Sequential()

if simple_model:
    model.add(layers.Dense(2, input_dim=2, activation='softmax'))
else:
    model.add(layers.Dense(10, input_dim=2, activation='relu'))
    # model.add(Dropout(0.5))
    model.add(layers.Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer=optimizer,
              metrics=['accuracy'])

model.fit(X_scaled, y_one_hot_labels, epochs=30, batch_size=1)

y_predicted = model.predict(X_scaled)
print(y_predicted)

# evaluate the model
metrics = model.evaluate(X_scaled, y_one_hot_labels)
print('Metrics:', metrics)
print("\n%s: %.2f%%" % (model.metrics_names[1], metrics[1] * 100))

if verbose:
    print(model.get_weights())
