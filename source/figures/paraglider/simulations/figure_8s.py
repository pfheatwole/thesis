"""Scratch file for developing simulator-related code."""

import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import numpy as np
import pfh.glidersim as gsim

import util


def main():
    paragliders1 = util.build_paragliders()
    paragliders2 = util.build_paragliders(
        kappa_RM=(0, 0, 0),
        kappa_RM_dot=(0, 0, 0),
    )
    inputs, T = util.figure_8s()
    model6a = gsim.simulator.ParagliderModel6a(paragliders1["6a"], **inputs)
    model9a1 = gsim.simulator.ParagliderModel9a(paragliders1["9a"], **inputs)
    model9a2 = gsim.simulator.ParagliderModel9a(paragliders2["9a"], **inputs)
    models = {
        "model6a": model6a,
        "model9a1": model9a1,
        "model9a2": model9a2,
    }

    style = {"lw": 1}
    fig, ax = plt.subplots()

    for m in models:
        model = models[m]
        state0 = model.starting_equilibrium()
        times, states = gsim.simulator.simulate(model, state0, dt=0.25, T=T)
        rx, ry, rz = states["r_RM2O"].T
        ax.plot(ry, rx, label=m, **style)

    ax.legend()
    plt.show()

    # breakpoint()


if __name__ == "__main__":
    main()
