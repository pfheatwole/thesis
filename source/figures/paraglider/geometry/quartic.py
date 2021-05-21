import matplotlib.pyplot as plt

import numpy as np


def quartic(p):
    A, B, C = 16, -32, 16
    return (
        A * p ** 4
        + B * p ** 3
        + C * p ** 2
    )


p0 = np.linspace(-0.1, 0, 10)
p1 = np.linspace(0, 1, 100)
p2 = np.linspace(1, 1.1, 10)

fig, ax = plt.subplots()
ax.plot(p0, quartic(p0), linewidth=1, color='grey', linestyle='--')
ax.plot(p0, np.zeros(10), linewidth=1.2, color='black')
ax.plot(p1, quartic(p1), linewidth=1.2, color='black')
ax.plot(p2, quartic(p2), linewidth=1, color='grey', linestyle='--')
ax.plot(p2, np.zeros(10), linewidth=1.2, color='black')
plt.grid()
plt.show()
