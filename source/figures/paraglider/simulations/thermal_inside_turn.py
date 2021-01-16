"""
Scenario: thermal on the inside wing tip during a constant right turn.

Includes some left brake so the turn is slower, allowing more time to interact
with the thermal.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import numpy as np
import pfh.glidersim as gsim
from pfh.glidersim.extras import simulation

import util


def right_turn(delta_b0, delta_br, delta_w, x, y, mag, radius5):
    t_warmup = 1
    t_rise = 2
    t_hold = 5
    inputs = {
        "delta_bl": simulation.linear_control(
            [(0, delta_b0),],
        ),
        "delta_br": simulation.linear_control(
            [(0, delta_b0), (t_warmup + t_rise + t_hold, None), (t_rise, delta_br)],
        ),
        "delta_w": simulation.linear_control([(t_warmup, 0), (t_rise, delta_w)]),
        "v_W2e": simulation.CircularThermal(
            px=x,
            py=y,
            mag=mag,
            radius5=radius5,
            t_enable=0,
        ),
    }
    T = 40
    return inputs, T


def main():
    testname = Path(__file__).stem
    print(f"\nRunning simulation '{testname}'\n")

    paragliders = util.build_paragliders(use_apparent_mass=True)

    # outside = True  # Thermal is outside the circle
    outside = False  # Thermal is inside the circle
    x = -65
    y = -122 + (-15 if outside else 15)
    mag = -3
    radius5 = 20

    # Simulate with mag=0 and plot `x vs y` to choose suitable px and py
    inputs, T = right_turn(
        delta_b0=0.5,  # Baseline symmetric brake
        delta_br=0.8,
        delta_w=0.5,
        x=x,
        y=y,
        mag=mag,
        radius5=radius5,
    )

    model = gsim.simulator.ParagliderModel6a(paragliders["6a"], **inputs)

    # Start facing south so a 180 turn will put the yaw angle at 0.
    state0 = model.starting_equilibrium()
    west = gsim.orientation.euler_to_quaternion([0, 0, -np.pi])
    state0["q_b2e"] = gsim.orientation.quaternion_product(west, state0["q_b2e"])
    state0["v_RM2e"] = gsim.orientation.quaternion_rotate(
        west * [-1, 1, 1, 1],
        state0["v_RM2e"],
    )

    times, states, states_dot = util.simulate(model, state0, dt=0.25, T=T)

    # Trim the output
    k = len(times) // 2
    times = times[k:]
    states = states[k:]
    states_dot = states_dot[k:]

    # -----------------------------------------------------------------------
    # Plots

    # 3D Plot: Position over time
    # points = gsim.extras.simulation.sample_paraglider_positions(model, states, times)
    # gsim.plots.plot_3d_simulation_path(**points, show=False)

    # xy-plot
    fig, ax = plt.subplots()
    util.plot_xy(states, ax=ax)
    ax.plot([y], [x], marker=".", c="k")
    ax.add_patch(Circle((y, x), radius5, fill=False, color="gray", linewidth=1))
    fig.savefig(f"{testname}_xy.svg")

    # Plot: orientation (note: `omega_b2e` != `Theta_b2e_dot`)
    Theta_b2e = gsim.orientation.quaternion_to_euler(states["q_b2e"])
    fig, ax = plt.subplots(3, figsize=(10, 10), sharex=True)
    ax[0].plot(times, np.rad2deg(Theta_b2e))
    ax[1].plot(times, np.rad2deg(states["omega_b2e"]))
    ax[2].plot(times, np.rad2deg(states_dot["omega_b2e"]))
    ax[0].set_ylabel("Theta_b2e [deg]")
    ax[1].set_ylabel("omega_b2e [deg]")
    ax[2].set_ylabel("alpha_b2e [deg]")
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    fig.savefig(f"{testname}_angular.svg")

    plt.show()

    breakpoint()


if __name__ == "__main__":
    main()
