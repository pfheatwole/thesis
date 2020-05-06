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
    elliptical_lobe,
)


def plot_foil(foil, N_sections=21, N_points=50, flatten=False, ax=None):
    """Plot a FoilGeometry in 3D."""
    if ax is None:
        fig, ax = _create_3d_axes()
        independent_plot = True
    else:
        independent_plot = False

    sa = 1 - np.cos(np.linspace(np.pi / 2, 0, N_points))
    for s in np.linspace(-1, 1, N_sections):
        coords = foil.surface_xyz(s, sa, "lower", flatten=flatten).T
        ax.plot(coords[0], coords[1], coords[2], c="r", zorder=0.9, lw=0.25)
        coords = foil.surface_xyz(s, sa, "upper", flatten=flatten).T
        ax.plot(coords[0], coords[1], coords[2], c="b", lw=0.25)

    s = np.linspace(-1, 1, N_sections)
    LE = foil.chord_xyz(s, 0, flatten=flatten).T
    c4 = foil.chord_xyz(s, 0.25, flatten=flatten).T
    TE = foil.chord_xyz(s, 1, flatten=flatten).T
    ax.plot(LE[0], LE[1], LE[2], "k--", lw=0.8)
    ax.plot(c4[0], c4[1], c4[2], "g--", lw=0.8)
    ax.plot(TE[0], TE[1], TE[2], "k--", lw=0.8)

    gsim.plots._set_axes_equal(ax)
    ax.set_proj_type('ortho')  # FIXME: better for this application?

    # Plot projections of the quarter-chord
    xlim = ax.get_xlim3d()
    zlim = ax.get_zlim3d()

    # Outline and quarter-chord projection onto the xy-pane (`z` held fixed)
    z = max(zlim)
    z *= 1.035  # Fix the distortion due to small distance from the xy-pane
    vertices = np.vstack((LE[0:2].T, TE[0:2].T[::-1]))  # shape: (2 * N_sections, 2)
    poly = PolyCollection([vertices], facecolors=['k'], alpha=0.25)
    ax.add_collection3d(poly, zs=[z], zdir='z')
    ax.plot(c4[0], c4[1], z, "g--", lw=0.8)

    # `x` reference curve projection onto the xy-pane
    xyz = foil.chord_xyz(s, foil._chords.r_x(s))
    x, y = xyz[..., 0], xyz[..., 1]
    ax.plot(x, y, z, 'r--', lw=0.8, label="reference lines")

    # Quarter-chord projection onto the yz-pane (`x` held fixed)
    x = np.full(*c4[1].shape, min(xlim))
    x *= 1.035  # Fix distortion due to small distance from the yz-pane
    ax.plot(x, c4[1], c4[2], "g--", lw=0.8, label="quarter-chord")

    # `yz` reference curve projection onto the yz-pane
    xyz = foil.chord_xyz(s, foil._chords.r_yz(s))
    y, z = xyz[..., 1], xyz[..., 2]
    ax.plot(x, y, z, 'r--', lw=0.8)
    ax.legend()
    ax.axis("off")


airfoil = gsim.airfoil.Airfoil(
    None,
    gsim.airfoil.NACA(24018, convention='vertical'),
)


chords1 = gsim.foil.ChordSurface(
    r_x=0.75,
    x=0,
    r_yz=1.00,
    yz=gsim.foil.elliptical_lobe(mean_anhedral=33, max_anhedral=67),
    chord_length=gsim.foil.elliptical_chord(root=0.5, tip=0.2),
    torsion=0,
)

foil1 = gsim.foil.SimpleFoil(
    airfoil=airfoil,
    chords=chords1,
    b_flat=2,
)

fig, ax = gsim.plots._create_3d_axes(figsize=(6, 6), dpi=96)
plot_foil(foil1, N_sections=31, flatten=False, ax=ax)
fig.tight_layout()
plt.show()
