from IPython import embed  # noqa: F401

from cycler import cycler
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
    ax.yaxis.set_ticks([1])

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
    xpos = 1.4 if not invert_x else -0.4
    ypos = 1.4 if not invert_y else -0.4
    ax.text(xpos, 0, xlabel, fontsize=15, verticalalignment="center")
    ax.text(0, ypos, ylabel, fontsize=15, horizontalalignment="center", verticalalignment="center")


def plot_3d_foil(foil):
    fig, ax = gsim.plots._create_3d_axes(figsize=(8, 8), dpi=96)
    ax.view_init(elev=90 - np.rad2deg(np.arctan(np.sqrt(2))), azim=-135)
    gsim.plots.plot_foil(foil, N_sections=31, flatten=False, ax=ax)

    # Hide the panes, grids, ticks, and ticklabels
    # ax.set_axis_off()

    # Hide the pane but leave the grid
    ax.xaxis.pane.set_visible(False)
    ax.yaxis.pane.set_visible(False)
    ax.zaxis.pane.set_visible(False)

    # Hide the ticklabels
    # ax.set_xticklabels([])
    # ax.set_yticklabels([])
    # ax.set_zticklabels([])

    # Remove the legend
    ax.legend().remove()

    # FIXME: this still leaves a lot of useless space in the graph. What if I
    # hid the gridlines, panes, ticks, etc, but drew some faux-panes on the xy
    # and yz planes to highlight the fact that the reference curves are
    # projections onto planes? That'd let me move them closer to the wing and
    # simplify the clutter. I would sort of miss the gridlines though; they're
    # helpful for orienting the view in 3D.

    fig.tight_layout(pad=0)
    return fig


if __name__ == "__main__":

    examples = {}

    # Flat, no taper, no twist
    examples["flat1"] = {
        "r_x": 1,
        "x": 0,
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": 0.25,
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
        "torsion": lambda s: np.deg2rad(25) * s**3,
    }

    # Manta rays!
    examples["manta1"] = {
        "r_x": 0,
        "x": lambda s: 0.5 * (1 - s**2),
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": lambda s: 0.5 * (1 - abs(s)),
        "torsion": 0,
    }
    examples["manta2"] = {
        "r_x": 0.5,
        "x": lambda s: 0.5 * (1 - s**2),
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": lambda s: 0.5 * (1 - abs(s)),
        "torsion": 0,
    }
    examples["manta3"] = {
        "r_x": 1, 
        "x": lambda s: 0.5 * (1 - s**2),
        "r_yz": 0,
        "yz": FlatYZ(),
        "chord_length": lambda s: 0.5 * (1 - abs(s)),
        "torsion": 0,
    }

    # Elliptical lobe
    examples["elliptical1"] = {
        "r_x": 0.75,
        "x": 0,
        "r_yz": 1.00,
        "yz": gsim.foil.elliptical_lobe(mean_anhedral=33, max_anhedral=67),
        "chord_length": gsim.foil.elliptical_chord(root=0.5, tip=0.2),
        "torsion": 0,
    }

    examples["elliptical2"] = {
        "r_x": 0.75,
        "x": 0,
        "r_yz": 1.00,
        "yz": gsim.foil.elliptical_lobe(mean_anhedral=44, max_anhedral=89),
        "chord_length": gsim.foil.elliptical_chord(root=0.5, tip=0.2),
        "torsion": 0,
    }

    examples["elliptical3"] = {
        "r_x": 0.75,
        "x": 0,
        "r_yz": 1.00,
        "yz": gsim.foil.elliptical_lobe(mean_anhedral=20, max_anhedral=89),
        "chord_length": gsim.foil.elliptical_chord(root=0.5, tip=0.2),
        "torsion": 0,
    }

    # Use a common airfoil
    airfoil = gsim.airfoil.Airfoil(None, gsim.airfoil.NACA(24018))

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
                axes[0, 1].plot(s, chords.r_x(s))

                configure_2d_axes(axes[0, 2], "$s$", "$r_{yz}$")
                axes[0, 2].plot(s, chords.r_yz(s))

                # FIXME: show yticks? These are radians.
                configure_2d_axes(axes[1, 0], "$s$", r"$\theta$")
                axes[1, 0].set_yticks([])
                axes[1, 0].plot(s, chords.torsion(s))

                configure_2d_axes(axes[1, 1], "$s$", "$x$")
                axes[1, 1].plot(s, chords.x(s))

                configure_2d_axes(axes[1, 2], "$y$", "$z$", invert_y=True)
                axes[1, 2].set_xticks([])  # Avoid confusion between s and y
                axes[1, 2].plot(*chords.yz(s).T)

                fig.tight_layout()

                if savefig:
                    fig.savefig(name + "_curves.svg")

        if plot_3d:
            fig = plot_3d_foil(foil)

            if savefig:
                fig.savefig(name + "_canopy.svg")

        if not savefig:
            plt.show()
