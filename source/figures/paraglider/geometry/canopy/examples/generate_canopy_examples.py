from IPython import embed  # noqa: F401

from cycler import cycler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401; for `projection='3d'`
from matplotlib.collections import PolyCollection

import numpy as np

import scipy

import pfh.glidersim as gsim
from pfh.glidersim.airfoil import Airfoil, NACA  # noqa: F401
from pfh.glidersim.foil import (  # noqa: F401
    FlatYZ,
    SimpleFoil,
    PolynomialTorsion as PT,
    elliptical_chord,
    elliptical_arc,
)


# Style for the 2D curves
rc = {
    # "axes.linewidth":
    "axes.spines.top": False,
    "axes.spines.right": False,

    "xtick.direction": "inout",
    "ytick.direction": "inout",

    "xtick.major.size": 8,
    "ytick.major.size": 8,

    "xtick.labelsize": 14,
    "ytick.labelsize": 14,

    # "xtick.bottom": False,
    # "xtick.labelbottom": False,
    # "ytick.left": False,
    # "ytick.labelleft": False,

    "axes.prop_cycle": cycler(color=["k"]),

    "axes.linewidth": 0.8,  # In points
    "lines.linewidth": 1.5,  # In points

    "text.usetex": True,
}


def configure_2d_axes(ax, xlabel, ylabel, invert_x=False, invert_y=False):
    # Apply the common style, add axes arrows and labels, set the limits, etc.
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-.2, 1.2)
    ax.xaxis.set_ticks([-1, 1])
    ax.yaxis.set_ticks([])

    if invert_y:
        ax.invert_yaxis()

    # Add axes arrow markers: https://stackoverflow.com/a/58410781
    xmarker = ">" if not invert_x else "<"
    ymarker = "^" if not invert_y else "v"
    xpos = 1 if not invert_x else 0
    ypos = 1 if not invert_y else 0
    ax.plot((xpos), (0), ls="", marker=xmarker, ms=5, color="k",
            transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot((0), (ypos), ls="", marker=ymarker, ms=5, color="k",
            transform=ax.get_xaxis_transform(), clip_on=False)

    # Add axes labels
    xpos = 1.3 if not invert_x else -0.3
    ypos = 1.5 if not invert_y else -0.5
    ax.text(xpos, 0, xlabel, fontsize=15, verticalalignment="center")
    ax.text(0, ypos, ylabel, fontsize=15, horizontalalignment="center", verticalalignment="center")


def _plot_foil(foil, N_sections=21, N_points=50, flatten=False, ax=None):
    """Plot a FoilGeometry in 3D."""
    if ax is None:
        fig, ax = _create_3d_axes()
        ax.set_proj_type('ortho')  # FIXME: better for this application?
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

    # Plot projections of the quarter-chord
    xlim = ax.get_xlim3d()
    zlim = ax.get_zlim3d()

    # Outline and quarter-chord projection onto the xy-pane (`z` held fixed)
    z = 0.75
    vertices = np.vstack((LE[0:2].T, TE[0:2].T[::-1]))  # shape: (2 * N_sections, 2)
    poly = PolyCollection([vertices], facecolors=['k'], alpha=0.25)
    ax.add_collection3d(poly, zs=[z], zdir='z')
    ax.plot(c4[0], c4[1], z, "g--", lw=0.8)

    # `x` reference curve projection onto the xy-pane
    xyz = foil.chord_xyz(s, foil._chords.r_x(s))
    x, y = xyz[..., 0], xyz[..., 1]
    ax.plot(x, y, z, 'r--', lw=0.8, label="reference lines")

    # Quarter-chord projection onto the yz-pane (`x` held fixed)
    x = np.full(*c4[1].shape, -1.25)
    ax.plot(x, c4[1], c4[2], "g--", lw=0.8, label="quarter-chord")

    # `yz` reference curve projection onto the yz-pane
    xyz = foil.chord_xyz(s, foil._chords.r_yz(s))
    y, z = xyz[..., 1], xyz[..., 2]
    ax.plot(x, y, z, 'r--', lw=0.8)


def plot_3d_foil(foil):
    # Make it big; removing the whitespace greatly reduces the final size
    fig, ax = gsim.plots._create_3d_axes(figsize=(10, 10), dpi=96)
    # ax.view_init(elev=90 - np.rad2deg(np.arctan(np.sqrt(2))), azim=-135)
    # gsim.plots.plot_foil(foil, N_sections=31, flatten=False, ax=ax)
    ax.view_init(elev=90 - np.rad2deg(np.arctan(np.sqrt(2))), azim=45)
    _plot_foil(foil, N_sections=31, flatten=False, ax=ax)

    # Hide the panes, grids, ticks, and ticklabels
    ax.set_axis_off()

    # Hide the pane but leave the grid
    # ax.xaxis.pane.set_visible(False)
    # ax.yaxis.pane.set_visible(False)
    # ax.zaxis.pane.set_visible(False)

    # Hide the ticklabels
    # ax.set_xticklabels([])
    # ax.set_yticklabels([])
    # ax.set_zticklabels([])

    # Remove the legend
    # ax.legend().remove()

    # FIXME: this still leaves a lot of useless space in the graph. What if I
    # hid the gridlines, panes, ticks, etc, but drew some faux-panes on the xy
    # and yz planes to highlight the fact that the reference curves are
    # projections onto planes? That'd let me move them closer to the wing and
    # simplify the clutter. I would sort of miss the gridlines though; they're
    # helpful for orienting the view in 3D.

    # Add faux xy and yz panes
    # vx, vz = 0.6, 0.5
    # xy_verts = np.array([[0.25, -1], [0.25, 1], [-vx, 1], [-vx, -1]])
    # yz_verts = np.array([[-1, vz], [1, vz], [1, -vz], [-1, -vz]])
    # xy_poly = PolyCollection([xy_verts], facecolors=['k'], alpha=0.10)
    # yz_poly = PolyCollection([yz_verts], facecolors=['k'], alpha=0.10)
    # ax.add_collection3d(xy_poly, zs=vz, zdir='z')
    # ax.add_collection3d(yz_poly, zs=-vx, zdir='x')

    # Add a faux grid
    xx = np.linspace(-1.25, 0.25, 7)
    yy = np.linspace(-1.25, 1.25, 11)
    zz = np.linspace(-0.5, 0.75, 6)
    style = {"c": "lightgray", "lw": 0.8, "zorder": -1}
    for x in xx:
        ax.plot([x, x], [-1.25, 1.25], [zz.max(), zz.max()], **style)

    for y in yy:
        ax.plot([xx.min(), xx.max()], [y, y], [zz.max(), zz.max()], **style)
        ax.plot([xx.min(), xx.min()], [y, y], [zz.min(), zz.max()], **style)

    for z in zz[:-1]:
        ax.plot([xx.min(), xx.min()], [-1.25, 1.25], [z, z], **style)

    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(1.25, -1.25)
    ax.set_zlim(1.25, -1.25)


    fig.tight_layout(pad=0)
    return fig


if __name__ == "__main__":

    examples = {}

    # Flat, no taper, no twist
    examples["flat1"] = {
        "r_x": 0,
        "x": 0,
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": 0.5,
        "torsion": 0,
    }

    # Flat, straight taper, no twist
    examples["flat2"] = {
        "r_x": 1,
        "x": 0,
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": lambda s: 0.5 - 0.25 * abs(s),
        "torsion": 0,
    }

    # Flat, elliptical taper, no twist
    examples["flat3"] = {
        "r_x": 1,
        "x": 0,
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": gsim.foil.elliptical_chord(root=0.5, tip=0.2),
        "torsion": 0,
    }

    # Flat, no taper, twist
    examples["flat4"] = {
        "r_x": 1,
        "x": 0,
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": 0.25,
        "torsion": lambda s: np.deg2rad(25) * s**4,
    }

    # Manta rays!
    #
    # Adding 1e-3 prevents zero-length sections, which are a pain because they
    # 
    examples["manta1"] = {
        "r_x": 0,
        "x": lambda s: 0.5 * (1 - s**2),
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": lambda s: 0.5 * (1 - abs(s)) + 1e-3,
        "torsion": 0,
    }
    examples["manta2"] = {
        "r_x": 0.5,
        "x": lambda s: 0.5 * (1 - s**2),
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": lambda s: 0.5 * (1 - abs(s)) + 1e-3,
        "torsion": 0,
    }
    examples["manta3"] = {
        "r_x": 1, 
        "x": lambda s: 0.5 * (1 - s**2),
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": lambda s: 0.5 * (1 - abs(s)) + 1e-3,
        "torsion": 0,
    }

    # Elliptical arc
    examples["elliptical1"] = {
        "r_x": 0.75,
        "x": 0,
        "r_yz": 1.00,
        "yz": gsim.foil.elliptical_arc(mean_anhedral=33, tip_anhedral=67),
        "chord_length": gsim.foil.elliptical_chord(root=0.5, tip=0.2),
        "torsion": 0,
    }

    examples["elliptical2"] = {
        "r_x": 0.75,
        "x": 0,
        "r_yz": 1.00,
        "yz": gsim.foil.elliptical_arc(mean_anhedral=44, tip_anhedral=89),
        "chord_length": gsim.foil.elliptical_chord(root=0.5, tip=0.2),
        "torsion": 0,
    }

    examples["elliptical3"] = {
        "r_x": 0.75,
        "x": 0,
        "r_yz": 1.00,
        "yz": gsim.foil.elliptical_arc(mean_anhedral=20, tip_anhedral=89),
        "chord_length": gsim.foil.elliptical_chord(root=0.5, tip=0.2),
        "torsion": 0,
    }

    # -----------------------------------------------------------------------
    # Build the reference wing from Belloc's paper

    h = 3 / 8  # Arch height (vertical deflection from wing root to tips) [m]
    cc = 2.8 / 8  # The central chord [m]
    b = 11.00 / 8  # The projected span [m]
    S = 25.08 / (8**2)  # The projected area [m^2]
    AR = 4.82  # The projected aspect ratio
    b_flat = 13.64 / 8  # The flattened span [m]
    S_flat = 28.56 / (8**2)  # The flattened area [m^2]
    AR_flat = 6.52  # The flattened aspect ratio

    # Use Eq:1 and Eq:2 for xyz and c
    i = np.arange(13)[::-1]  # Reverse the order to move left->right
    thetas = i * np.pi / 12
    xyz = np.c_[np.zeros(13), b / 2 * np.cos(thetas), -h * np.sin(thetas)]
    k = 1.05
    c = cc * np.sqrt(1 - (xyz.T[1] / (k * b / 2)) ** 2)  # Corrected Eq:2
    theta = np.deg2rad([3, 3, *([0] * 9), 3, 3])

    # Compute the section indices
    L_segments = np.linalg.norm(np.diff(xyz, axis=0), axis=1)
    s_xyz = np.cumsum(np.r_[0, L_segments]) / L_segments.sum() * 2 - 1

    # Coordinates and chords are in meters, and must be normalized
    fx = scipy.interpolate.interp1d(s_xyz, xyz.T[0] / (b_flat / 2))
    fy = scipy.interpolate.interp1d(s_xyz, xyz.T[1] / (b_flat / 2))
    fz = scipy.interpolate.interp1d(s_xyz, (xyz.T[2] - xyz[6, 2]) / (b_flat / 2))
    fc = scipy.interpolate.interp1d(s_xyz, c / (b_flat / 2))
    ftheta = scipy.interpolate.interp1d(s_xyz, theta)

    class PchipInterpolatedArc:
        def __init__(self, s, y, z):
            self._f = scipy.interpolate.PchipInterpolator(s, np.c_[y, z])
            self._fd = self._f.derivative()

        def __call__(self, s):
            return self._f(s)

        def derivative(self, s):
            return self._fd(s)

    s = np.linspace(-1, 1, 1000)  # Resample so the cubic-fit stays linear
    arc = PchipInterpolatedArc(s, fy(s), fz(s))

    examples["belloc"] = {
        "r_x": 0.6,
        "x": 0,
        "r_yz": 0.6,
        "yz": arc,
        "chord_length": fc,
        "torsion": ftheta,
    }

    # -----------------------------------------------------------------------

    # Use a common airfoil
    airfoil = gsim.airfoil.Airfoil(None, gsim.airfoil.NACA(23015))

    savefig = True  # Save the images to SVG files
    # savefig = False

    plot_2d = True  # Show the 2D curves
    # plot_2d = False  # Disable the 2D plots

    plot_3d = True  # Show the 3D wireframe view
    # plot_3d = False  # Disable the 3D view

    for name, parameters in examples.items():
        print("Current example:", name)
        chords = gsim.foil.ChordSurface(**parameters)
        foil = gsim.foil.SimpleFoil(airfoil=airfoil, chords=chords, b_flat=2)

        if plot_2d:
            s = np.linspace(-1, 1, 21)
            with plt.rc_context(rc):
                fig, axes = plt.subplots(2, 3, figsize=(7, 3), dpi=96)

                configure_2d_axes(axes[0, 0], "$s$", "$c$")
                axes[0, 0].plot(s, chords._chord_length(s)),

                configure_2d_axes(axes[0, 1], "$s$", "$r_{xy}$")
                axes[0, 1].set_yticks([1])
                axes[0, 1].plot(s, chords.r_x(s))

                configure_2d_axes(axes[0, 2], "$s$", "$r_{yz}$")
                axes[0, 2].set_yticks([1])
                axes[0, 2].plot(s, chords.r_yz(s))

                # FIXME: show yticks? These are radians.
                configure_2d_axes(axes[1, 0], "$s$", r"$\theta$")
                axes[1, 0].plot(s, chords.torsion(s))

                configure_2d_axes(axes[1, 1], "$s$", "$x$")
                axes[1, 1].plot(s, chords.x(s))

                configure_2d_axes(axes[1, 2], "$y$", "$z$", invert_y=True)
                axes[1, 2].set_xticklabels([])  # Avoid confusion between s and y
                axes[1, 2].plot(*chords.yz(s).T)

                fig.tight_layout()
                fig.subplots_adjust(hspace=1.0, wspace=0.3)

                if savefig:
                    fig.savefig(name + "_curves.svg")

        if plot_3d:
            fig = plot_3d_foil(foil)

            if savefig:
                fig.savefig(name + "_canopy.svg")

        if not savefig:
            plt.show()
