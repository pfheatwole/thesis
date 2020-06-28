from IPython import embed  # noqa: F401

from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401; for `projection='3d'`

import numpy as np

import pfh.glidersim as gsim
from pfh.glidersim.airfoil import Airfoil, NACA  # noqa: F401
from pfh.glidersim.foil import (  # noqa: F401
    FlatYZ,
    SimpleFoil,
    PolynomialTorsion as PT,
    elliptical_chord,
    elliptical_arc,
)

airfoil = gsim.airfoil.Airfoil(
    None,
    gsim.airfoil.NACA(24018, convention='vertical'),
)


# Flat, no taper
chords1 = gsim.foil.ChordSurface(
    r_x=1,
    x=0,
    r_yz=0,
    yz=FlatYZ(),
    chord_length=lambda s: 0.5 - 0.25 * abs(s),
    torsion=0,
)

chordsX = gsim.foil.ChordSurface(
    r_x=0.75,
    x=0,
    r_yz=1.00,
    yz=gsim.foil.elliptical_arc(mean_anhedral=33, max_anhedral=67),
    chord_length=gsim.foil.elliptical_chord(root=0.5, tip=0.2),
    torsion=0,
)

foil1 = gsim.foil.SimpleFoil(
    airfoil=airfoil,
    chords=chords1,
    b_flat=2,
)

fig, ax = gsim.plots._create_3d_axes(figsize=(6, 6), dpi=96)
gsim.plots.plot_foil(foil1, N_sections=31, flatten=False, ax=ax)
ax.xaxis.pane.set_visible(False)
ax.yaxis.pane.set_visible(False)
ax.zaxis.pane.set_visible(False)
fig.tight_layout()
plt.show()


# What if I hide the gridlines, panes, ticks, etc, but draw some pseudo-panes
# on the xy and yz planes to highlight the fact that the reference curves
# are projections onto planes? That'd let me move them closer to the wing and
# simplify the clutter.
