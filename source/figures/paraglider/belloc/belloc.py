"""
Recreates the paraglider analysis in "Wind Tunnel Investigation of a Rigid
Paraglider Reference Wing", H. Belloc, 2015

TODO:
* Why am I still significantly overestimating CL? Wrong airfoil data?
* The CM25% in the paper are positive? How? The section Cm are almost entirely
  negative until `alpha > 10`.
* Review my CM_G calculation; both it and CM25% look wrong (which make sense,
  since CM25% is computed directly from CM_G, while CM_CL and CM_CD look great.
* Review the force and moment calculations.
* Phillips needs "Picard iterations" to deal with stalled sections
* I need to fix how I calculate L and D when beta>0
   * Observe in my `CL vs CD`: CD decreases with beta? Nope, wrong
   * Also, in `CL vs alpha`, why does alpha_L0 increase with beta?
* Review the "effective AR" equation in Eq:6
"""


from IPython import embed

import matplotlib.pyplot as plt  # noqa: F401

import numpy as np

import pandas as pd

import pfh.glidersim as gsim

import scipy.interpolate
from scipy.interpolate import PchipInterpolator as Pchip


# ---------------------------------------------------------------------------
# Wing definition from the paper

# Table 1: the Full-scale wing dimensions converted into 1/8 model
h = 3 / 8  # Arch height (vertical deflection from wing root to tips) [m]
cc = 2.8 / 8  # The central chord [m]
b = 11.00 / 8  # The projected span [m]
S = 25.08 / (8**2)  # The projected area [m^2]
AR = 4.82  # The projected aspect ratio

b_flat = 13.64 / 8  # The flattened span [m]
S_flat = 28.56 / (8**2)  # The flattened area [m^2]
AR_flat = 6.52  # The flattened aspect ratio

# Table 2: Coordinates along the 0.6c line for the 1/8 model in [m]
xyz = np.array(
    [
        [0.000, -0.688,  0.000],
        [0.000, -0.664, -0.097],
        [0.000, -0.595, -0.188],
        [0.000, -0.486, -0.265],
        [0.000, -0.344, -0.325],
        [0.000, -0.178, -0.362],
        [0.000,  0.000, -0.375],
        [0.000,  0.178, -0.362],
        [0.000,  0.344, -0.325],
        [0.000,  0.486, -0.265],
        [0.000,  0.595, -0.188],
        [0.000,  0.664, -0.097],
        [0.000,  0.688,  0.000],
    ],
)

c = np.array([0.107, 0.137, 0.198, 0.259, 0.308, 0.339, 0.350,
              0.339, 0.308, 0.259, 0.198, 0.137, 0.107])  # chords [m]

theta = np.deg2rad([3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3])  # torsion [deg]

# Compute the section indices
L_segments = np.linalg.norm(np.diff(xyz, axis=0), axis=1)
s_xyz = np.cumsum(np.r_[0, L_segments]) / L_segments.sum() * 2 - 1

# Coordinates and chords are in meters, and must be normalized
fx = scipy.interpolate.interp1d(s_xyz, xyz.T[0] / (b_flat / 2))
fy = scipy.interpolate.interp1d(s_xyz, xyz.T[1] / (b_flat / 2))
fz = scipy.interpolate.interp1d(s_xyz, (xyz.T[2] - xyz[6, 2]) / (b_flat / 2))
fc = scipy.interpolate.interp1d(s_xyz, c / (b_flat / 2))
ftheta = scipy.interpolate.interp1d(s_xyz, theta)


# ---------------------------------------------------------------------------
# Build the canopy and wing

airfoil = gsim.airfoil.Airfoil(
    gsim.airfoil.XFLR5Coefficients("xflr5/airfoil_polars", flapped=False),
    gsim.airfoil.NACA(23015, convention="vertical")
)


class InterpolatedLobe:
    """Interface to use a PchipInterpolator for the lobe."""

    def __init__(self, s, y, z):
        y = np.asarray(y)
        z = np.asarray(z)

        assert y.ndim == 1 and z.ndim == 1

        self._f = scipy.interpolate.PchipInterpolator(s, np.c_[y, z])
        self._fd = self._f.derivative()

    def __call__(self, s):
        return self._f(s)

    def derivative(self, s):
        return self._fd(s)


# FIXME: move the resampling logic into `InterpolatedLobe`, and make that an
#        official helper class in `foil.py`. It should also use more intelligent
#        resampling (only needs two extra samples on either side of each point)
s = np.linspace(-1, 1, 1000)  # Resample so the cubic-fit stays linear
lobe = InterpolatedLobe(s, fy(s), fz(s))

chord_surface = gsim.foil.ChordSurface(
    x=0,
    r_x=0.6,
    yz=lobe,
    r_yz=0.6,
    chord_length=fc,
    torsion=ftheta,
)

sections = gsim.foil.FoilSections(
    airfoil=airfoil,
    intakes=None,
)

canopy = gsim.foil.SimpleFoil(
    chords=chord_surface,
    sections=sections,
    b_flat=b_flat,
)

print()
print("Finished defining the canopy. Checking fit...")
print(f"  Projected area> Expected: {S:.4f},   Actual: {canopy.S:.4f}")
print(f"  Flattened area> Expected: {S_flat:.4f},   Actual: {canopy.S_flat:.4f}")
print(f"    Projected AR> Expected: {AR:.4f},   Actual: {canopy.AR:.4f}")
print(f"    Flattened AR> Expected: {AR_flat:.4f},   Actual: {canopy.AR_flat:.4f}")
print()

wing = gsim.paraglider_wing.ParagliderWing(
    canopy=canopy,
    force_estimator=gsim.foil.Phillips(canopy, 40, K=31),
    brake_geo=gsim.brake_geometry.Cubic(0, 0.75, delta_max=0),  # unused
    d_riser=0.25,  # For the 1/8 model, d_riser = 0.0875 / 0.350 = 25%
    z_riser=1,  # The 1/8 scale model has the cg 1m below the central chord
    pA=0.08,  # unused
    pC=0.80,  # unused
    kappa_a=0,  # unused
    rho_upper=0,  # Neglect gravitational forces
    rho_lower=0,

    total_line_length=0,  # Neglect line drag
    average_line_diameter=0,
    line_drag_positions=[0, 0, 0],
    Cd_lines=0,
)

# print("\nFinished defining the complete wing. Pausing for review.\n")
# gsim.plots.plot_foil(canopy, N_sections=121)
# gsim.plots.plot_foil_topdown(canopy, N_sections=13)  # Belloc Fig:2
# embed()
# 1/0

# ---------------------------------------------------------------------------
# Testing

# The paper says the wind tunnel is being used at 40m/s to produce a Reynold's
# number of 920,000. It neglects to mention the air density during the test,
# but if the dynamic viscosity of the air is standard, then we can compute the
# density of the air.
Re = 0.92e6
v_mag = 40  # Wind tunnel airspeed [m/s]
L = 0.350  # central chord [m]
mu = 1.81e-5  # Standard dynamic viscosity of air
rho_air = Re * mu / (v_mag * L)
rho_air = 1.187  # Override: the true (mean) value from the wind tunnel data
print("rho_air:", rho_air)

# Full-range tests
Fs = {}  # Net force
Ms = {}  # Net moment at the "risers"
Mc4s = {}  # Net moment from all the section pitching moments
solutions = {}  # Solutions for Phillips' method
alphas = {}  # The converged angles-of-attack
betas = np.arange(16)
# betas = [0]

for kb, beta_deg in enumerate(betas):
    Fs[beta_deg] = []
    Ms[beta_deg] = []
    Mc4s[beta_deg] = []
    solutions[beta_deg] = []
    cp_wing = wing.control_points(0)  # Section control points

    alphas_down = np.deg2rad(np.linspace(2, -5, 30))[1:]
    alphas_up = np.deg2rad(np.linspace(2, 22, 75))

    # First with decreasing alpha
    ref = None
    for ka, alpha in enumerate(alphas_down):
        print(f"\rTest: alpha: {np.rad2deg(alpha): 6.2f}, beta: {beta_deg}", end="")
        beta = np.deg2rad(beta_deg)
        v_W2b = np.asarray(
            [np.cos(alpha) * np.cos(beta), np.sin(beta), np.sin(alpha) * np.cos(beta)],
        )
        v_W2b *= -v_mag  # The Reynolds numbers are a function of the magnitude

        try:
            dF, dM, ref = wing.forces_and_moments(
                0, 0, v_W2b=v_W2b, rho_air=rho_air, reference_solution=ref,
            )
        except gsim.foil.ForceEstimator.ConvergenceError:
            ka -= 1  # FIXME: messing with the index!
            break
            # FIXME: continue, or break? Maybe try the solution from a previous
            #        `beta`? eg: ref = solutions[betas[kb - 1]][ka]

        F = dF.sum(axis=0)
        M = dM.sum(axis=0)  # Moment due to section `Cm`
        M += np.cross(cp_wing, dF).sum(axis=0)  # Add the moment due to forces

        Fs[beta_deg].append(F)
        Ms[beta_deg].append(M)
        Mc4s[beta_deg].append(dM.sum(axis=0))
        solutions[beta_deg].append(ref)

    alphas_down = alphas_down[:ka+1]  # Truncate when convergence failed

    # Reverse the order
    Fs[beta_deg] = Fs[beta_deg][::-1]
    Ms[beta_deg] = Ms[beta_deg][::-1]
    Mc4s[beta_deg] = Mc4s[beta_deg][::-1]
    solutions[beta_deg] = solutions[beta_deg][::-1]
    alphas_down = alphas_down[::-1]

    # Continue with increasing alpha
    ref = None
    for ka, alpha in enumerate(alphas_up):
        print(f"\rTest: alpha: {np.rad2deg(alpha): 6.2f}, beta: {beta_deg}", end="")
        beta = np.deg2rad(beta_deg)
        v_W2b = np.asarray(
            [np.cos(alpha) * np.cos(beta), np.sin(beta), np.sin(alpha) * np.cos(beta)],
        )
        v_W2b *= -v_mag  # The Reynolds numbers are a function of the magnitude

        try:
            dF, dM, ref = wing.forces_and_moments(
                0, 0, v_W2b=v_W2b, rho_air=rho_air, reference_solution=ref,
            )
        except gsim.foil.ForceEstimator.ConvergenceError:
            ka -= 1  # FIXME: messing with the index!
            break
            # FIXME: continue, or break? Maybe try the solution from a previous
            #        `beta`? eg: ref = solutions[betas[kb - 1]][ka]

        F = dF.sum(axis=0)
        M = dM.sum(axis=0)  # Moment due to section `Cm`
        M += np.cross(cp_wing, dF).sum(axis=0)  # Add the moment due to forces

        Fs[beta_deg].append(F)
        Ms[beta_deg].append(M)
        Mc4s[beta_deg].append(dM.sum(axis=0))
        solutions[beta_deg].append(ref)

    alphas_up = alphas_up[:ka+1]  # Truncate when convergence failed

    alphas[beta_deg] = np.r_[alphas_down, alphas_up]  # Stitch them together

    print()

for beta in betas:
    Fs[beta] = np.asarray(Fs[beta])
    Ms[beta] = np.asarray(Ms[beta])
    Mc4s[beta] = np.asarray(Mc4s[beta])

# ---------------------------------------------------------------------------
# Compute the aerodynamic coefficients
#
# Uses the flattened wing area as the reference, as per the Belloc paper.

S = canopy.S_flat
q = 0.5 * rho_air * v_mag**2

nllt = {}  # Coefficients from the NLLT, keyed by beta [deg]
for beta in betas:
    CX, CY, CZ = Fs[beta].T / (q * S)
    CN = -CZ
    CM = Ms[beta].T[1] / (q * S * cc)  # The paper uses the central chord
    CM_c4 = Mc4s[beta].T[1] / (q * S * cc)

    # From Stevens, "Aircraft Control and Simulation", pg 90 (104)
    beta_rad = np.deg2rad(beta)
    CD = (
        -np.cos(alphas[beta]) * np.cos(beta_rad) * CX
        - np.sin(beta_rad) * CY
        + np.sin(alphas[beta]) * np.cos(beta_rad) * CN
    )
    CL = np.sin(alphas[beta]) * CX + np.cos(alphas[beta]) * CN

    # Alternative form using a transformation matrix: body -> wind axes
    # See: https://www.mathworks.com/help/aeroblks/aerodynamicforcesandmoments.html
    # sa, sb = np.sin(alphas[beta]), np.sin(beta_rad)
    # ca, cb = np.cos(alphas[beta]), np.cos(beta_rad)
    # C_w2b = np.array([
    #     [ca * cb, sb, sa * cb],
    #     [-ca * sb, cb, -sa * sb],
    #     [-sa, 0, ca]
    # ])
    # (CD, CC, CL) = C_w2b @ [-CX, -CY, -CZ]

    nllt[beta] = {"CL": CL, "CD": CD, "CM": CM, "CM_c4": CM_c4}


# ---------------------------------------------------------------------------
# Recreate Belloc figures 5..8

plotted_betas = {0, 5, 10, 15}  # The betas present in Belloc's plots
beta_names = {0: "00", 5: "05", 10: "10", 15: "15"}  # For filenames
beta_ax = {0: (0, 0), 5: (0, 1), 10: (1, 0), 15: (1, 1)}  # Subplot axes

# Load the VLM and wind tunnel data
belloc = {}  # Coefficients from the wind tunnel, keyed  by beta [deg]
vlm = {}  # Coefficients from the VLM method, keyed by beta [deg]
for beta in sorted(plotted_betas.intersection(betas)):
    b = beta_names[beta]
    belloc[beta] = pd.read_csv(f"windtunnel/beta{b}.csv")  # Belloc's raw wind tunnel data
    names = ("alpha", "CL", "CD", "CM")
    vlm[beta] = np.loadtxt(  # Inviscid solution using VLM from XLFR5
        f"xflr5/wing_polars/Belloc_VLM2-b{b}.txt",
        dtype=np.dtype({"names": names, "formats": [float] * 4}),
        skiprows=8,
        usecols=(0, 2, 5, 8),
    )

belloc_args = {"c": "k", "linestyle": "--", "linewidth": 1, "label": "Wind tunnel"}
nllt_args = {"c": "b", "linestyle": "--", "linewidth": 1, "label": "NLLT"}
vlm_args = {"c": "r", "linestyle": "--", "linewidth": 1, "label": "VLM"}

def plot4x4(xlabel, ylabel, xlim=None, ylim=None):
    args = {
        "nrows": 2,
        "ncols": 2,
        "sharex": True,
        "sharey": True,
        "figsize": (6, 6),
    }

    fig, axes = plt.subplots(**args)
    if xlim:
        axes[0, 0].set_xlim(*xlim)
    if ylim:
        axes[0, 0].set_ylim(*ylim)
    axes[1, 0].set_xlabel(xlabel)
    axes[1, 1].set_xlabel(xlabel)
    axes[0, 0].set_ylabel(ylabel)
    axes[1, 0].set_ylabel(ylabel)
    axes[0, 0].grid(c='lightgrey', linestyle="--")
    axes[0, 1].grid(c='lightgrey', linestyle="--")
    axes[1, 0].grid(c='lightgrey', linestyle="--")
    axes[1, 1].grid(c='lightgrey', linestyle="--")
    return fig, axes


# Plot: CL vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "$\mathrm{C_L}$", xlim=(-10, 25), ylim=(-0.6, 1.25))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[beta_ax[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CZa"], **belloc_args)
    ax.plot(np.rad2deg(alphas[beta]), nllt[beta]["CL"], **nllt_args)
    ax.plot(vlm[beta]["alpha"], vlm[beta]["CL"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="lower right")
fig.tight_layout()
fig.savefig(f"CL_vs_alpha.svg", dpi=96)

# Plot: CD vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "$\mathrm{C_D}$", xlim=(-10, 25), ylim=(0.0, 0.2))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[beta_ax[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CXa"], **belloc_args)
    ax.plot(np.rad2deg(alphas[beta]), nllt[beta]["CD"], **nllt_args)
    ax.plot(vlm[beta]["alpha"], vlm[beta]["CD"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="upper left")
fig.tight_layout()
fig.savefig(f"CD_vs_alpha.svg", dpi=96)

# Plot: CM vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "$\mathrm{C_{M,G}}$", xlim=(-10, 25), ylim=(-0.5, 0.1))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[beta_ax[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CMT1"], **belloc_args)
    ax.plot(np.rad2deg(alphas[beta]), nllt[beta]["CM"], **nllt_args)
    ax.plot(vlm[beta]["alpha"], vlm[beta]["CM"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="lower left")
fig.tight_layout()
fig.savefig(f"CM_vs_alpha.svg", dpi=96)

# Plot: CL vs CD
fig, axes = plot4x4("$\mathrm{C_D}$", "$\mathrm{C_L}$", xlim=(0, 0.2), ylim=(-0.6, 1.25))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[beta_ax[beta]]
    ax.plot(belloc[beta]["CXa"], belloc[beta]["CZa"], **belloc_args)
    ax.plot(nllt[beta]["CD"], nllt[beta]["CL"], **nllt_args)
    ax.plot(vlm[beta]["CD"], vlm[beta]["CL"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="lower right")
fig.tight_layout()
fig.savefig(f"CL_vs_CD.svg", dpi=96)

# Plot: CL vs CM
fig, axes = plot4x4("$\mathrm{C_{M,G}}$", "$\mathrm{C_L}$", xlim=(-0.5, 0.1), ylim=(-0.6, 1.25))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[beta_ax[beta]]
    ax.plot(belloc[beta]["CMT1"][:42], belloc[beta]["CZa"][:42], **belloc_args)
    ax.plot(nllt[beta]["CM"], nllt[beta]["CL"], **nllt_args)
    ax.plot(vlm[beta]["CM"], vlm[beta]["CL"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="lower right")
fig.tight_layout()
fig.savefig(f"CL_vs_CM.svg", dpi=96)

plt.show()

embed()
1/0


# Compute the pitching moment coefficients:
#
# CM_CD : due to the drag force applied to the wing
# CM_CL : due to the lift force applied to the wing
# CM_c4 : due to the wing shape
# CM_G: the total pitching moment = CM_CD + CM_CL + CM_c4
CL = nllt[0]["CL"]
CM_G = nllt[0]["CM"]
CM_CD = nllt[0]["CD"] * np.cos(alphas[0]) / cc  # Eq: 8
CM_CL = -nllt[0]["CL"] * np.sin(alphas[0]) / cc  # Eq: 9
CM_c4 = CM_G - CM_CL - CM_CD  # Eq: 7

ax[0, 1].plot(CM_G, CL, label="CM_G", marker=m)
ax[0, 1].plot(CM_CL, CL, label="CM_CL", marker=m)
ax[0, 1].plot(CM_CD, CL, label="CM_CD", marker=m)
ax[0, 1].plot(CM_c4, CL, label="CM_25%", marker=m)
ax[0, 1].plot(nllt[0]["CM_c4"], CL, 'r--', label="Other CM_25%", marker=m)
ax[0, 1].set_xlabel("CM")
ax[0, 1].set_ylabel("CL")
ax[0, 1].legend()
ax[0, 1].grid()
ax[0, 1].set_xlim(-0.5, 0.2)
ax[0, 1].set_ylim(-0.4, 1.0)

ax[1, 1].set_xlabel("CM_G")
ax[1, 1].set_ylabel("CL")
ax[1, 1].set_xlim(-0.5, 0.1)
ax[1, 1].set_ylim(-0.4, 1.0)
ax[1, 1].legend()
ax[1, 1].grid()


# Figures 9, 11, and 12
Cy_a0, Cy_a5, Cy_a10, Cy_a15 = [], [], [], []
Cl_a0, Cl_a5, Cl_a10, Cl_a15 = [], [], [], []
Cn_a0, Cn_a5, Cn_a10, Cn_a15 = [], [], [], []
for beta in betas:
    # Find the indices nearest each alpha in {0, 5, 10, 15}
    ix_a0 = np.argmin(np.abs(np.rad2deg(alphas[beta]) - 0))
    ix_a5 = np.argmin(np.abs(np.rad2deg(alphas[beta]) - 5))
    ix_a10 = np.argmin(np.abs(np.rad2deg(alphas[beta]) - 10))
    ix_a15 = np.argmin(np.abs(np.rad2deg(alphas[beta]) - 15))

    # Lateral force
    Cy_a0.append(Fs[beta].T[1][ix_a0] / (q * S))
    Cy_a5.append(Fs[beta].T[1][ix_a5] / (q * S))
    Cy_a10.append(Fs[beta].T[1][ix_a10] / (q * S))
    Cy_a15.append(Fs[beta].T[1][ix_a15] / (q * S))

    # Rolling moment coefficients
    Cl_a0.append(Ms[beta].T[0][ix_a0] / (q * S * cc))
    Cl_a5.append(Ms[beta].T[0][ix_a5] / (q * S * cc))
    Cl_a10.append(Ms[beta].T[0][ix_a10] / (q * S * cc))
    Cl_a15.append(Ms[beta].T[0][ix_a15] / (q * S * cc))

    # Yawing moment coeficients
    Cn_a0.append(Ms[beta].T[2][ix_a0] / (q * S * cc))
    Cn_a5.append(Ms[beta].T[2][ix_a5] / (q * S * cc))
    Cn_a10.append(Ms[beta].T[2][ix_a10] / (q * S * cc))
    Cn_a15.append(Ms[beta].T[2][ix_a15] / (q * S * cc))

fig9, ax9 = plt.subplots()
ax9.plot(betas, Cy_a0, label=r"$\alpha$=0°")
ax9.plot(betas, Cy_a5, label=r"$\alpha$=5°")
ax9.plot(betas, Cy_a10, label=r"$\alpha$=10°")
ax9.plot(betas, Cy_a15, label=r"$\alpha$=15°")
ax9.set_xlim(-20, 20)
ax9.set_ylim(-0.3, 0.3)
ax9.set_title("Figure 9: The effect of sideslip on the lateral force")
ax9.set_xlabel(r"$\beta$")
ax9.set_ylabel(r"$\mathrm{C_y}$")
ax9.legend()
ax9.grid()

fig11, ax11 = plt.subplots()
ax11.plot(betas, Cl_a0, label=r"$\alpha$=0°")
ax11.plot(betas, Cl_a5, label=r"$\alpha$=5°")
ax11.plot(betas, Cl_a10, label=r"$\alpha$=10°")
ax11.plot(betas, Cl_a15, label=r"$\alpha$=15°")
ax11.set_xlim(-20, 20)
ax9.set_ylim(-0.2, 0.2)
ax11.set_title("Figure 11: The effect of sideslip on the rolling moment")
ax11.set_xlabel(r"$\beta$")
ax11.set_ylabel(r"$\mathrm{Cl_G}$")
ax11.legend()
ax11.grid()

fig12, ax12 = plt.subplots()
ax12.plot(betas, Cn_a0, label=r"$\alpha$=0°")
ax12.plot(betas, Cn_a5, label=r"$\alpha$=5°")
ax12.plot(betas, Cn_a10, label=r"$\alpha$=10°")
ax12.plot(betas, Cn_a15, label=r"$\alpha$=15°")
ax12.set_xlim(-20, 20)
ax12.set_ylim(-0.1, 0.1)
ax12.set_title("Figure 12: The effect of sideslip on the yawing moment")
ax12.set_xlabel(r"$\beta$")
ax12.set_ylabel(r"$\mathrm{Cn_G}$")
ax12.legend()
ax12.grid()

plt.show()

embed()
