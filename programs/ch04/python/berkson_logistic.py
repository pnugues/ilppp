"""
Data set from the original paper on logistic regression:
Joseph Berkson, Application of the Logistic Function to Bio-Assay. Journal of the American Statistical Association (1944).
"""
from math import log10, sqrt, exp
import matplotlib.pyplot as plt
import numpy as np


def logistic(x):
    try:
        return 1 / (1 + exp(-x))
    except:
        return 0


def line(m, b, x):
    return m * x + b


dose = [40, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300]
exposed = [462, 500, 467, 515, 561, 469, 550, 542, 479, 497, 453]
mortality = [109, 199, 298, 370, 459, 400, 495, 499, 450, 476, 442]

log_dose = [log10(dose[i]) for i in range(0, len(dose))]
mortality_rate = [mortality[i] / exposed[i] for i in range(0, len(dose))]
plt.scatter(log_dose, mortality_rate, color='red', marker='^')

# Fitting parameters from Berkson (p. 363)
m, b = 5.659746, -10.329884
x_l = np.linspace(min(log_dose) - 1.5, max(log_dose) + 1.5, 1000)
y_l = [logistic(line(m, b, x_l[i])) for i in range(0, len(x_l))]
plt.plot(x_l, y_l)
plt.show()
