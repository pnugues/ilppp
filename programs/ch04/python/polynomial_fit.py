"""
Polynomial fit of the Salammbô A count/letter count
"""
__author__ = 'Pierre Nugues'

import numpy as np
import matplotlib.pyplot as plt

stat = open('../salammbo/salammbo_a_fr.tsv').read().strip().split('\n')
observations = np.array([list(map(float, obs.split())) for obs in stat])

# We plot the points: x is the predictor (feature) and y the response
x = observations[:, 0]
y = observations[:, 1]

f, axes = plt.subplots(3, sharex=True, sharey=True)
axes[0].scatter(x, y)
axes[1].scatter(x, y)
axes[2].scatter(x, y)

r = np.linspace(min(x), max(x), 1000)

degree = 1
# We find the fitting coefficients
z = np.polyfit(x, y, degree)
# We use them to create a polynomial
p = np.poly1d(z)
legend1 = axes[0].plot(r, p(r), 'r-')

degree = 8
z = np.polyfit(x, y, degree)
p = np.poly1d(z)
legend2 = axes[1].plot(r, p(r), 'b-')


degree = 9
z = np.polyfit(x, y, degree)
p = np.poly1d(z)
legend3 = axes[2].plot(r, p(r), 'g-')


plt.show()
