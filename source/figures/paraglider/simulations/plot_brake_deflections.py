import matplotlib.pyplot as plt
import numpy as np

import pfh.glidersim as gsim
from pfh.glidersim import orientation


def plot_deflections(wing, delta_bl, delta_br, save=False):
    figd, axd = plt.subplots()  # delta_d
    figTE, axTE = plt.subplots()  # trailing edge yz

    s = np.linspace(-1, 1, 150)

    delta_d = wing.lines.delta_d(s, delta_bl, delta_br)
    c = wing.canopy.chord_length(s)
    ai = delta_d / c  # Normalized deflection distances

    axd.plot(s, ai, linewidth=0.75, c="k")
    axd.set_ylim(ai.min() - 0.05 * ai.ptp(), ai.max() + 0.5 * ai.ptp())
    axd.set_xlabel("Section index $s$")
    axd.set_ylabel("Normalized deflection distance")
    axd.grid(True)

    TE0 = wing.canopy.surface_xyz(s, 0, 1, surface='upper')
    TE1 = wing.canopy.surface_xyz(s, ai, 1, surface='upper')
    axTE.plot(TE0.T[1], TE0.T[2], c='k', lw=0.75, linestyle='-')
    axTE.plot(TE1.T[1], TE1.T[2], c='k', lw=0.75, linestyle='--')
    axTE.invert_yaxis()  # Inverted `z` coordinates
    axTE.set_xlabel("y")
    axTE.set_ylabel("z")
    axTE.set_aspect("equal")

    plt.show()

    if save:
        figd.savefig(f"Hook3_deltad_{delta_bl:.2f}_{delta_br:.2f}.svg")
        figTE.savefig(f"Hook3_TE_{delta_bl:.2f}_{delta_br:.2f}.svg")


if __name__ == "__main__":
    wing = gsim.extras.wings.build_hook3(verbose=True)

    savefig = False
    plot_deflections(wing, 0.25, 0.50, save=savefig)
    plot_deflections(wing, 1.00, 1.00, save=savefig)
