"""
Polynomial fit of the Salammbô A count/letter count
"""
__author__ = 'Pierre Nugues'

import matplotlib.pyplot as plt
import numpy as np

# The data set: _Salammbô_ in French with the counts of characters, counts of _a_ and _e_
dataset = np.array([[36961, 2503, 4312],
                    [43621, 2992, 4993],
                    [15694, 1042, 1785],
                    [36231, 2487, 4158],
                    [29945, 2014, 3394],
                    [40588, 2805, 4535],
                    [75255, 5062, 8512],
                    [37709, 2643, 4229],
                    [30899, 2126, 3599],
                    [25486, 1784, 3002],
                    [37497, 2641, 4306],
                    [40398, 2766, 4618],
                    [74105, 5047, 8678],
                    [76725, 5312, 8870],
                    [18317, 1215, 2195]])

# We plot the points: X is the predictor (feature) and y the response
x = dataset[:, 0]
y = dataset[:, 1]

# The polynomial degrees we will test and their color
degrees_col = [(1, 'r-'), (8, 'b-'), (9, 'g-')]

f, axes = plt.subplots(len(degrees_col), sharex=True, sharey=True)
x_vals = np.linspace(min(x), max(x), 1000)

for idx, (degree, color) in enumerate(degrees_col):
    axes[idx].scatter(x, y)
    # We find the fitting coefficients
    z = np.polyfit(x, y, degree)
    # We use them to create a polynomial
    p = np.poly1d(z)
    legend = axes[idx].plot(x_vals, p(x_vals), color)
plt.show()
