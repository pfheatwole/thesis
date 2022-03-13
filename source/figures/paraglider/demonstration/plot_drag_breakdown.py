"""Compute the individual contributions to total drag."""

import matplotlib.pyplot as plt
import numpy as np
import pfh.glidersim as gsim

import util


def zero_Cd(s, ai, alpha, Re, clamp=False):
    shape = np.broadcast_shapes(
        np.shape(s),
        np.shape(ai),
        np.shape(alpha),
        np.shape(Re),
    )
    return np.zeros(shape=shape)


def paraglider_drag_components(glider, delta_a, delta_b, rho_air=1.225):
    glider_eq = glider.equilibrium_state(delta_a=delta_a, delta_b=delta_b)
    v_W2b = -glider_eq["v_RM2e"]
    C_w2b = gsim.orientation.euler_to_dcm([0, -glider_eq["alpha_b"], 0])
    C_e2b = gsim.orientation.euler_to_dcm(glider_eq["Theta_b2e"]).T

    # The canopy has viscous and inviscid components (profile and induced drag)
    dF, _, _ = glider.wing.aerodynamics(
        delta_a,
        delta_b,
        delta_b,
        v_W2b=v_W2b,
        rho_air=rho_air,
        reference_solution=None,
    )
    F = dF[:-2].sum(axis=0)  # FIXME: magic numbers to discard the line forces
    D_total = -(C_w2b @ F)[0]  # Drag is the force along -xhat
    Cd = glider.wing.canopy.sections.Cd  # Save the bound method
    glider.wing.canopy.sections.Cd = zero_Cd  # Disable viscous drag
    dF, _, _ = glider.wing.aerodynamics(
        delta_a,
        delta_b,
        delta_b,
        v_W2b=v_W2b,
        rho_air=rho_air,
        reference_solution=None,
    )
    F = dF[:-2].sum(axis=0)  # FIXME: magic numbers to discard the line forces
    D_inviscid = -(C_w2b @ F)[0]
    D_viscous = D_total - D_inviscid
    glider.wing.canopy.sections.Cd = Cd  # Reenable viscous drag

    dF, _ = glider.wing.lines.aerodynamics([v_W2b, v_W2b], rho_air)
    D_lines = -(C_w2b @ dF.sum(axis=0))[0]

    F, _ = glider.payload.resultant_force(0, v_W2b, rho_air, [0, 0, 0], [0, 0, 0])
    D_payload = -(C_w2b @ F)[0]

    return {
        "groundspeed": (C_e2b @ glider_eq["v_RM2e"])[0],
        "D_inviscid": D_inviscid,
        "D_viscous": D_viscous,
        "D_lines": D_lines,
        "D_payload": D_payload,
    }


##############################################################################

gliders = util.build_paragliders(verbose=False)
glider = gliders["6a_23"]

N = 31  # Number of points to sample for the brake and accelerator sequences
results = []
for delta_b in np.linspace(1, 0, N):
    results.append(paraglider_drag_components(glider, 0, delta_b))

for delta_a in np.linspace(0, 1, N)[1:]:
    results.append(paraglider_drag_components(glider, delta_a, 0))

Vx = [r["groundspeed"] for r in results]
D_inviscid = [r["D_inviscid"] for r in results]
D_viscous = [r["D_viscous"] for r in results]
D_lines = [r["D_lines"] for r in results]
D_payload = [r["D_payload"] for r in results]


def print_proportions(n, msg):
    total = sum((D_inviscid[n], D_viscous[n], D_lines[n], D_payload[n]))
    print(f" {msg}")
    print(f"  Inviscid: {D_inviscid[n]/total:.2g}")
    print(f"  Viscous:  {D_viscous[n]/total:.2g}")
    print(f"  Lines:    {D_lines[n]/total:.2g}")
    print(f"  Payload:  {D_payload[n]/total:.2g}")


print("Proportions:")
print_proportions(0, "Full brakes")
print_proportions(N, "Zero brakes")
print_proportions(-1, "Full speedbar")
print()

fig, ax = plt.subplots(figsize=(8, 4))
ax.axvline(
    Vx[N],
    0,
    0.6,
    color="k",
    linestyle="--",
    linewidth=1,
    label="Zero controls",
)
ax.stackplot(
    Vx,
    D_lines,
    D_payload,
    D_inviscid,
    D_viscous,
    labels=["Lines", "Payload", "Canopy inviscid", "Canopy viscous"],
)
ax.set_ylim(0, 150)
ax.set_xlabel("Groundspeed [m/s]")
ax.set_ylabel("Drag [N]")
handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels), loc="upper center")
fig.savefig("drag_breakdown.svg")
# plt.show()

# breakpoint()
