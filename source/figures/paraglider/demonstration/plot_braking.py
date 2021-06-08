import matplotlib.pyplot as plt
import numpy as np
import pfh.glidersim as gsim

airfoils = gsim.extras.airfoils.load_datfile_set('braking_NACA24018_Xtr0.25')

r = np.linspace(-1, 1, 250)

fig, ax = plt.subplots(figsize=(6,3))

for d in airfoils:
    ax.plot(
        *airfoils[d]['airfoil'].profile_curve(r).T,
        linewidth='1',
        c='k',
    )

ax.set_ylim(-0.25, 0.15)
ax.set_aspect('equal')
plt.show()

# fig.savefig("braking_NACA24018.svg")
