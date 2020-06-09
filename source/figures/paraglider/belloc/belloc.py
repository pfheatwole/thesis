"""
Recreates the paraglider analysis in "Wind Tunnel Investigation of a Rigid
Paraglider Reference Wing", H. Belloc, 2015
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

# Table 1: the full-scale wing dimensions converted into 1/8 model
h = 3 / 8  # Arch height (vertical deflection from wing root to tips) [m]
cc = 2.8 / 8  # Central chord [m]
b = 11.00 / 8  # Projected span [m]
S = 25.08 / (8**2)  # Projected area [m^2]
AR = 4.82  # Projected aspect ratio

b_flat = 13.64 / 8  # Flattened span [m]
S_flat = 28.56 / (8**2)  # Flattened area [m^2]
AR_flat = 6.52  # Flattened aspect ratio

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

chords = gsim.foil.ChordSurface(
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
    chords=chords,
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
    force_estimator=gsim.foil.Phillips(canopy, 40, K=11),
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
# Simulate the wind tunnel tests
#
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
betas = np.arange(-15, 16)
# betas = [0, 5, 10, 15]

for kb, beta_deg in enumerate(betas):
    Fs[beta_deg] = []
    Ms[beta_deg] = []
    Mc4s[beta_deg] = []
    solutions[beta_deg] = []
    cp_wing = wing.control_points(0)  # Section control points

    # Some figures assume samples at alpha = [0, 5, 10, 15], so make sure to
    # include those test points.
    alphas_down = np.deg2rad(np.linspace(4, -5, 37))[1:]
    alphas_up = np.deg2rad(np.linspace(4, 22, 73))

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
            ka -= 1
            break

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
            ka -= 1
            break

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

    # Transform body -> wind axes. (See "Flight Vehicle Aerodynamics", Drela,
    # 2014, Eq:6.7, page 125). Notice that Drela uses back-right-up instead of
    # front-right-down coordinates, so the CX and CZ terms are negated.
    beta_rad = np.deg2rad(beta)
    sa, sb = np.sin(alphas[beta]), np.full(len(alphas[beta]), np.sin(beta_rad))
    ca, cb = np.cos(alphas[beta]), np.full(len(alphas[beta]), np.cos(beta_rad))
    C_w2b = np.array([
        [-ca * cb, -sb, -sa * cb],
        [-ca * sb, cb, -sa * sb],
        [sa, np.zeros_like(alphas[beta]), -ca]
    ])

    # Body axes
    CX, CY, CZ = Fs[beta].T / (q * S)
    Cl, Cm, Cn = Ms[beta].T / (q * S * cc)

    # Wind axes
    CXa, CYa, CZa = np.einsum("ijk,kj->ik", C_w2b, Fs[beta] / (q * S))
    Cla, Cma, Cna = np.einsum("ijk,kj->ik", C_w2b, Ms[beta] / (q * S * cc))

    Cm_c4 = Mc4s[beta].T[1] / (q * S * cc)  # FIXME: useful?

    nllt[beta] = {
        "CX": CX,
        "CY": CY,
        "CZ": CZ,
        "Cl": Cl,
        "Cm": Cm,
        "Cn": Cn,
        "CXa": CXa,
        "CYa": CYa,
        "CZa": CZa,
        "Cla": Cla,
        "Cma": Cma,
        "Cna": Cna,

        "Cm_c4": Cm_c4
    }


# ---------------------------------------------------------------------------
# Recreate Belloc figures 5..8

plotted_betas = {0, 5, 10, 15}  # The betas present in Belloc's plots
axes_indices = {0: (0, 0), 5: (0, 1), 10: (1, 0), 15: (1, 1)}  # Subplot axes

# Load the VLM and wind tunnel data
belloc = {}  # Coefficients from the wind tunnel, keyed  by beta [deg]
vlm = {}  # Coefficients from the VLM method, keyed by beta [deg]
for beta in sorted(plotted_betas.intersection(betas)):
    belloc[beta] = pd.read_csv(f"windtunnel/beta{beta:02}.csv")  # Belloc's raw wind tunnel data
    names = ("alpha", "CZa", "CXa", "Cm")
    vlm[beta] = np.loadtxt(  # Inviscid solution using VLM from XLFR5
        f"xflr5/wing_polars/Belloc_VLM2-b{beta:02}.txt",
        dtype=np.dtype({"names": names, "formats": [float] * 4}),
        skiprows=8,
        usecols=(0, 2, 5, 8),
    )

belloc_args = {"c": "k", "linestyle": "-", "linewidth": 0.5, "label": "Wind tunnel"}
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
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CZa"], **belloc_args)
    ax.plot(np.rad2deg(alphas[beta]), nllt[beta]["CZa"], **nllt_args)
    ax.plot(vlm[beta]["alpha"], vlm[beta]["CZa"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="lower right")
fig.tight_layout()
fig.savefig(f"CL_vs_alpha.svg", dpi=96)

# Plot: CD vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "$\mathrm{C_D}$", xlim=(-10, 25), ylim=(0.0, 0.2))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CXa"], **belloc_args)
    ax.plot(np.rad2deg(alphas[beta]), nllt[beta]["CXa"], **nllt_args)
    ax.plot(vlm[beta]["alpha"], vlm[beta]["CXa"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="upper left")
fig.tight_layout()
fig.savefig(f"CD_vs_alpha.svg", dpi=96)

# Plot: CM vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "$\mathrm{C_{M,G}}$", xlim=(-10, 25), ylim=(-0.5, 0.1))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CMT1"], **belloc_args)
    ax.plot(np.rad2deg(alphas[beta]), nllt[beta]["Cm"], **nllt_args)
    ax.plot(vlm[beta]["alpha"], vlm[beta]["Cm"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="lower left")
fig.tight_layout()
fig.savefig(f"CM_vs_alpha.svg", dpi=96)

# Plot: CL vs CD
fig, axes = plot4x4("$\mathrm{C_D}$", "$\mathrm{C_L}$", xlim=(0, 0.2), ylim=(-0.6, 1.25))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["CXa"], belloc[beta]["CZa"], **belloc_args)
    ax.plot(nllt[beta]["CXa"], nllt[beta]["CZa"], **nllt_args)
    ax.plot(vlm[beta]["CXa"], vlm[beta]["CZa"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="lower right")
fig.tight_layout()
fig.savefig(f"CL_vs_CD.svg", dpi=96)

# Plot: CL vs CM
fig, axes = plot4x4("$\mathrm{C_{M,G}}$", "$\mathrm{C_L}$", xlim=(-0.5, 0.1), ylim=(-0.6, 1.25))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["CMT1"][:42], belloc[beta]["CZa"][:42], **belloc_args)
    ax.plot(nllt[beta]["Cm"], nllt[beta]["CZa"], **nllt_args)
    ax.plot(vlm[beta]["Cm"], vlm[beta]["CZa"], **vlm_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[1, 1].legend(loc="lower left")
fig.tight_layout()
fig.savefig(f"CL_vs_CM.svg", dpi=96)

# ---------------------------------------------------------------------------

# Build sets of coefficients over `betas`, keyed by alpha
Cy = {alpha: [] for alpha in [0, 5, 10, 15]}
Cl = {alpha: [] for alpha in [0, 5, 10, 15]}
Cn = {alpha: [] for alpha in [0, 5, 10, 15]}
for beta in betas:
    for alpha in [0, 5, 10, 15]:
        ix = np.nonzero(np.isclose(np.rad2deg(alphas[beta]), alpha))
        if ix[0].shape[0]:
            Cy[alpha].append(nllt[beta]["CYa"][ix][0])
            Cl[alpha].append(nllt[beta]["Cl"][ix][0])
            Cn[alpha].append(nllt[beta]["Cn"][ix][0])
        else:  # pad to keep the sequences the same length as `betas`
            Cy[alpha].append(np.nan)
            Cl[alpha].append(np.nan)
            Cn[alpha].append(np.nan)

belloc2 = {a: pd.read_csv(f"windtunnel/alpha{a:02}v40.csv") for a in [0, 5, 10, 15]}

# Plot: Cy vs beta
fig, axes = plot4x4(r"$\beta$", r"$\mathrm{Cy_G}$", (-20, 20), (-0.3, 0.3))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CY"], **belloc_args)
    ax.plot(betas, Cy[alpha], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[1, 1].legend()
fig.tight_layout()
fig.savefig(f"CY_vs_beta.svg", dpi=96)

# Plot: Cl (wing rolling coefficient) vs beta
fig, axes = plot4x4(r"$\beta$", r"$\mathrm{Cl_G}$", (-20, 20), (-0.2, 0.2))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CLT1"], **belloc_args)
    ax.plot(betas, Cl[alpha], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[1, 1].legend()
fig.tight_layout()
fig.savefig(f"Cl_vs_beta.svg", dpi=96)

# Plot: Cn (wing yawing coefficient) vs beta
fig, axes = plot4x4(r"$\beta$", r"$\mathrm{Cn_G}$", (-20, 20), (-0.2, 0.2))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CNT1"], **belloc_args)
    ax.plot(betas, Cn[alpha], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[1, 1].legend()
fig.tight_layout()
fig.savefig(f"Cn_vs_beta.svg", dpi=96)

plt.show()

embed()
