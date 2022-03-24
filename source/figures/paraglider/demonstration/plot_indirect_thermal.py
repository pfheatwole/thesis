"""Compute steady-state turn data."""

import matplotlib.pyplot as plt
import numpy as np
import pfh.glidersim as gsim

import util


inputs, T = util.centered_thermal(
    delta_a=0,
    delta_b=0.75,
    py=15,
    mag=-3,
    radius5=15,
)

sim_parameters = {  # Default scenario
    "delta_a": 0.0,
    "delta_bl": 0.0,
    "delta_br": 0.0,
    "delta_w": 0.0,
    "rho_air": 1.225,
    "v_W2e": (0, 0, 0),
}
sim_parameters.update(inputs)

gliders = util.build_paragliders(verbose=False)
glider = gliders["6a_23"]
model = gsim.simulator.ParagliderStateDynamics6a(glider, **sim_parameters)

dt = 0.05
state0 = model.starting_equilibrium()
times, states, states_dot = util.simulate(model=model, state0=state0, dt=dt, T=T)


# Plot: orientation (note: `omega_b2e` != `Theta_b2e_dot`)
Theta_b2e = gsim.orientation.quaternion_to_euler(states["q_b2e"])
Theta_b2e_dot = gsim.extras.simulation.compute_euler_derivatives(
    Theta_b2e,
    states["omega_b2e"],
)

fig, ax = plt.subplots(3, figsize=(10, 6), sharex=True)
ax[0].plot(times, np.rad2deg(Theta_b2e))
ax[1].plot(times, np.rad2deg(states["omega_b2e"]))
ax[2].plot(times, np.rad2deg(states_dot["omega_b2e"]), label=["Roll", "Pitch", "Yaw"])
ax[0].set_ylabel("Theta_b2e [°]")
ax[1].set_ylabel("omega_b2e [°/s]")
ax[2].set_ylabel("alpha_b2e [°/s²]")
ax[0].grid()
ax[1].grid()
ax[2].grid()
ax[2].legend(loc="upper right")
plt.show()


C_e2b = gsim.orientation.quaternion_to_dcm(states["q_b2e"][-1]).T
print("In Earth (tangent-plane) coordinates:")
print(f"   v_RM2e = {states['v_RM2e'][-1].round(2)}")
print(f"omega_b2e = {np.rad2deg(C_e2b @ states['omega_b2e'][-1]).round(2)}")

breakpoint()
