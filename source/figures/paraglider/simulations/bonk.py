"""
Demonstrates what happens when you use gradient descent and change the starting
point. Observe the `alpha_b2e` plot; those jumps happen when the model reverts
to the default reference solution.

TODO: review the `Gamma` before/after the bonk. Could be the `Gamma` have some
noise (especially at the wing tips) that's getting amplified and restarting
with the the default solution resets/eliminates it.

If so, I should probably be massaging that noise in the first place.
"""


import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import numpy as np
import pfh.glidersim as gsim
from pfh.glidersim.extras import simulation

import util


def right_turn(delta_b0, delta_br, delta_w, px, py, mag):
    # Simulate with mag=0 and plot `x vs y` to choose suitable px and py
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
            px=px,
            py=py,
            mag=mag,
            radius5=20,
            t_enable=0,
        ),
    }
    T = 23
    return inputs, T


def main():
    paragliders = util.build_paragliders(use_apparent_mass=True)

    inputs, T = right_turn(
        delta_b0=0.5,
        delta_br=0.95,
        delta_w=0.5,
        px=120 + 12,
        py=50,
        mag=-3,
    )

    model = gsim.simulator.ParagliderModel6a(paragliders["6a"], **inputs)

    print("\nPreparing the simulation...\n")
    state0 = model.starting_equilibrium()
    gsim.simulator.prettyprint_state(state0, "Initial state:", "")
    t_start = time.perf_counter()
    dt = 0.10  # Time step for the sequence of `states`
    times, states = gsim.simulator.simulate(model, state0, dt=dt, T=T)
    states_dot = gsim.simulator.recompute_derivatives(model, times, states)
    t_stop = time.perf_counter()
    print(f"\nTotal time: {t_stop - t_start:.2f}\n")
    gsim.simulator.prettyprint_state(states[-1], "Final state:", "")

    k = len(times) // 2
    times = times[k:]
    states = states[k:]
    states_dot = states_dot[k:]

    # -----------------------------------------------------------------------
    # Plots

    # 3D Plot: Position over time
    points = gsim.extras.simulation.sample_paraglider_positions(model, states, times)
    gsim.plots.plot_3d_simulation_path(**points, show=False)

    # Plot: orientation (note: `omega_b2e` != `Theta_b2e_dot`)
    Theta_b2e = gsim.orientation.quaternion_to_euler(states["q_b2e"])
    fig, ax = plt.subplots(3, figsize=(10, 10))
    ax[0].plot(times, np.rad2deg(Theta_b2e))
    ax[1].plot(times, np.rad2deg(states["omega_b2e"]))
    ax[2].plot(times, np.rad2deg(states_dot["omega_b2e"]))
    ax[0].set_ylabel("Theta_b2e [deg]")
    ax[1].set_ylabel("omega_b2e [deg]")
    ax[2].set_ylabel("alpha_b2e [deg]")
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()

    plt.show()

    breakpoint()


if __name__ == "__main__":
    main()
