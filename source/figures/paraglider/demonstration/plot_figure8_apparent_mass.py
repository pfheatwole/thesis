"""Plot two partial figure-8s w/ and w/o apparent mass."""

import matplotlib.pyplot as plt
import numpy as np
import pfh.glidersim as gsim
from pfh.glidersim.extras import simulation

import util


def figure_8s(N_cycles=2, duration=30, mag=1):
    """
    Scenario: multiple figure-8s.

    Parameters
    ----------
    N_cycles : int
        How many cycles of left+right braking.
    duration : int [sec]
        Seconds per half-cycle.
    mag : float
        Magnitude of braking applied.
    """
    on = [(2.0, mag), (duration - 2.0, None)]  # Braking on
    off = [(1.0, 0), (duration - 1.0, None)]  # Braking off
    inputs = {
        "delta_br": simulation.linear_control([(2, 0), *([*on, *off] * N_cycles)]),
        "delta_bl": simulation.linear_control([(2, 0), *([*off, *on] * N_cycles)]),
    }
    T = N_cycles * duration * 2
    return inputs, T


inputs, _ = figure_8s()
T = 60

sim_parameters = {  # Default scenario
    "delta_a": 0.0,
    "delta_bl": 0.0,
    "delta_br": 0.0,
    "delta_w": 0.0,
    "rho_air": 1.225,
    "v_W2e": (0, 0, 0),
}
sim_parameters.update(inputs)

gliders1 = util.build_paragliders(use_apparent_mass=True, verbose=False)
gliders2 = util.build_paragliders(use_apparent_mass=False, verbose=False)

glider1 = gliders1["6a_23"]
glider2 = gliders2["6a_23"]

model1 = gsim.simulator.ParagliderStateDynamics6a(glider1, **sim_parameters)
model2 = gsim.simulator.ParagliderStateDynamics6a(glider2, **sim_parameters)

dt = 0.25

state0 = model1.starting_equilibrium()
times, states, states_dot = util.simulate(model=model1, state0=state0, dt=dt, T=T)
points1 = gsim.extras.simulation.sample_paraglider_positions(model1, states, times)

state0 = model2.starting_equilibrium()
times, states, states_dot = util.simulate(model=model2, state0=state0, dt=dt, T=T)
points2 = gsim.extras.simulation.sample_paraglider_positions(model2, states, times)

fig, ax = gsim.extras.plots._create_3d_axes()
ax.view_init(azim=20, elev=25)
alpha = 0.75
gsim.extras.plots.plot_3d_simulation_path(**points1, ax=ax, alpha=alpha)
gsim.extras.plots.plot_3d_simulation_path(**points2, ax=ax, alpha=alpha)

handles, labels = ax.get_legend_handles_labels()
handles = [handles[1], handles[4]]
labels = ["With apparent mass", "Without apparent mass"]
ax.legend(handles, labels)
plt.show()
