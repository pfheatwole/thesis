import pfh.glidersim as gsim
import numpy as np
import matplotlib.pyplot as plt

wing = gsim.extras.wings.niviuk_hook3(size=23)
r = np.linspace(0, 1, 300)
pu = wing.canopy.surface_xyz(0, 0, r, surface="upper")
pl = wing.canopy.surface_xyz(0, 0, r, surface="lower")

fig, ax = plt.subplots()
ax.plot(pu.T[0], -pu.T[2])
ax.plot(pl.T[0], -pl.T[2])
ax.set_aspect("equal")
plt.show()
