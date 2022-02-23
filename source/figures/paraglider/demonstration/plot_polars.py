"""Plot polar curves for Niviuk Hook 3 and annotate them with flight data."""

import matplotlib.pyplot as plt
import numpy as np
import pfh.glidersim as gsim

import util


gliders = util.build_paragliders()

savefig = False
# savefig = True

###############################################################################
# Wing test: Parapente Mag (French), size=25 with a pod harness
# (`Hook 3 Parapente Mag 148.pdf`)

accelerating, braking = gsim.extras.compute_polars.compute_polar_data(gliders["6a_25"])
deltas_a = accelerating["delta"]
deltas_b = braking["delta"]
thetas_a = accelerating["theta_b"]
thetas_b = braking["theta_b"]
v_RM2e_a = accelerating["v_RM2e"]
v_RM2e_b = braking["v_RM2e"]

# Polar curve: vertical versus horizontal airspeed
fig, ax = plt.subplots(figsize=(10, 5))
speeds = np.array([24, 33.12, 38, 52])  # stall, min sink, trim, max [km/h]
ax.vlines(speeds / 3.6, 0.5, 3, colors="k", linestyles="dashed", linewidth=1)
ax.plot(v_RM2e_a.T[0], v_RM2e_a.T[2], "g")
ax.plot(v_RM2e_b.T[0], v_RM2e_b.T[2], "r")
ax.plot([9.22], [1.05], "k.")
ax.set_aspect("equal")
ax.set_xlim(0, 20)
ax.set_ylim(0, 3.5)
ax.invert_yaxis()
ax.set_xlabel("Horizontal airspeed [m/s]")
ax.set_ylabel("Sink rate [m/s]")
ax.set_title("Niviuk Hook 3, size 25")
ax.grid(which="both")
# ax.minorticks_on()
if savefig:
    fig.savefig("equilibrium_airspeed.svg")


###############################################################################
# Wing test: Parapente (Spanish), size=27 with a pod harness
# (`Hook 3 perfils.pdf`)

accelerating, braking = gsim.extras.compute_polars.compute_polar_data(gliders["6a_27"])
deltas_a = accelerating["delta"]
deltas_b = braking["delta"]
thetas_a = accelerating["theta_b"]
thetas_b = braking["theta_b"]
v_RM2e_a = accelerating["v_RM2e"]
v_RM2e_b = braking["v_RM2e"]

# Polar curve: vertical versus horizontal airspeed
fig, ax = plt.subplots(figsize=(10, 5))
speeds = np.array([24, 35, 40, 54])  # stall, min sink, trim, max [km/h]
ax.vlines(speeds / 3.6, 0.5, 3, colors="k", linestyles="dashed", linewidth=1)
ax.plot(v_RM2e_a.T[0], v_RM2e_a.T[2], "g")
ax.plot(v_RM2e_b.T[0], v_RM2e_b.T[2], "r")
ax.plot([9.72], [1.15], "k.")
ax.set_aspect("equal")
ax.set_xlim(0, 20)
ax.set_ylim(0, 3.5)
ax.invert_yaxis()
ax.set_xlabel("Horizontal airspeed [m/s]")
ax.set_ylabel("Sink rate [m/s]")
ax.set_title("Niviuk Hook 3, size 27")
ax.grid(which="both")
# ax.minorticks_on()
if savefig:
    fig.savefig("equilibrium_airspeed_27.svg")

plt.show()
