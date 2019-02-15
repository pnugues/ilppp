"""
Polynomial fit of the Salammbô A count/letter count
"""
__author__ = 'Pierre Nugues'

import matplotlib.pyplot as plt
import numpy as np

stat = open('../salammbo/salammbo_a_fr.tsv').read().strip().split('\n')
observations = np.array([list(map(float, obs.split())) for obs in stat])

# We plot the points: X is the predictor (feature) and y the response
x = observations[:, 0]
y = observations[:, 1]

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
