"""Plot the wing response to rapidly releasing the accelerator."""

import matplotlib.pyplot as plt
import numpy as np
import pfh.glidersim as gsim

import util


def accelerator_fast_off(delta_a, t_warmup, t_fall, t_settle):
    """Scenario: rapidly release accelerator."""
    accelerate = gsim.extras.simulation.linear_control(
        [(t_warmup, delta_a), (t_fall, 0)]
    )
    inputs = {
        "delta_a": accelerate,
    }
    T = t_warmup + t_fall + t_settle
    return inputs, T


sim_parameters = {  # Default scenario
    "delta_a": 0.0,
    "delta_bl": 0.0,
    "delta_br": 0.0,
    "delta_w": 0.0,
    "rho_air": 1.225,
    "v_W2e": (0, 0, 0),
}
inputs, T = accelerator_fast_off(  # Custom scenario
    delta_a=1,
    t_warmup=2,
    t_fall=0.3,
    t_settle=10,
)
sim_parameters.update(inputs)

gliders = util.build_paragliders(verbose=False)
glider = gliders["6a_23"]
model = gsim.simulator.ParagliderStateDynamics6a(glider, **sim_parameters)

dt = 0.25
state0 = model.starting_equilibrium()
times, states, states_dot = util.simulate(model=model, state0=state0, dt=dt, T=T)

points = gsim.extras.simulation.sample_paraglider_positions(model, states, times)
# gsim.extras.plots.plot_3d_simulation_path(**points, show=True)

# Plot a side view
fig, ax = plt.subplots(figsize=(6, 3))
util.plot_path_sideview(points["r_RM2O"], points["r_C02O"], points["r_P2O"], ax)
ax.set_aspect("equal")
ax.invert_yaxis()
ax.set_xlabel("x [m]")
ax.set_ylabel("z [m]")
ax.legend()

# Plot: orientation (note: `omega_b2e` != `Theta_b2e_dot`)
Theta_b2e = gsim.orientation.quaternion_to_euler(states["q_b2e"])

fig, ax = plt.subplots(figsize=(6,3))
ax.plot(times, np.rad2deg(Theta_b2e.T[1]), c="k", lw=0.75)
ax.grid()
ax.set_xlabel("Time [sec]")
ax.set_ylabel("Pitch angle [deg]")

plt.show()
