"""
Recreates the paraglider analysis in "Wind Tunnel Investigation of a Rigid
Paraglider Reference Wing", H. Belloc, 2015
"""

import time

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
    gsim.airfoil.NACA(23015, convention="vertical"),
)


class InterpolatedArc:
    """Interface to use a PchipInterpolator for the arc."""

    def __init__(self, s, y, z):
        self._f = scipy.interpolate.PchipInterpolator(s, np.c_[y, z])
        self._fd = self._f.derivative()

    def __call__(self, s):
        return self._f(s)

    def derivative(self, s):
        return self._fd(s)


# FIXME: move the resampling logic into `InterpolatedArc`, and make that an
#        official helper class in `foil.py`. It should also use more intelligent
#        resampling (only needs two extra samples on either side of each point)
s = np.linspace(-1, 1, 1000)  # Resample so the cubic-fit stays linear
arc = InterpolatedArc(s, fy(s), fz(s))

# Alternatively, use the analytical (non-sampled, smooth curvature) form
# arc = gsim.foil.elliptical_arc(np.rad2deg(np.arctan(.375/.688)), 89)

chords = gsim.foil.ChordSurface(
    x=0,
    r_x=0.6,
    yz=arc,
    r_yz=0.6,
    c=fc,
    theta=ftheta,
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

lines = gsim.line_geometry.SimpleLineGeometry(
    kappa_x=0.0875 / 0.350,  # 25% back from the leading edge
    kappa_z=1.0 / 0.350,  # 1m below the central chord
    kappa_A=0.08,  # unused
    kappa_C=0.80,  # unused
    kappa_a=0,  # unused
    total_line_length=0,  # Neglect line drag
    average_line_diameter=0,
    line_drag_positions=[0, 0, 0],
    Cd_lines=0,
    s_delta_start=0,  # unused
    s_delta_max=0.75,  # unused
    delta_max=0,  # unused
)

wing = gsim.paraglider_wing.ParagliderWing(
    lines=lines,
    canopy=canopy,
    rho_upper=0,  # Neglect gravitational forces
    rho_lower=0,
    force_estimator=gsim.foil.Phillips(canopy, 40, K=11),
)

# print("\nFinished defining the complete wing. Pausing for review.\n")
# gsim.plots.plot_foil(canopy, N_sections=121)
# gsim.plots.plot_foil_topdown(canopy, N_sections=13)  # Belloc Fig:2
# embed()
# 1/0

# ---------------------------------------------------------------------------
# Simulate the wind tunnel tests
#
# The paper says the wind tunnel is being used at 40m/s to produce a Reynolds
# number of 920,000. It neglects to mention the air density during the test,
# but if the dynamic viscosity of the air is standard, then we can compute the
# density of the air.
Re = 0.92e6  # Reynolds number
v_mag = 40  # Wind tunnel airspeed [m/s]
L = 0.350  # central chord [m]
mu = 1.81e-5  # Standard dynamic viscosity of air
rho_air = Re * mu / (v_mag * L)
rho_air = 1.187  # Override: the true (mean) value from the wind tunnel data
print("rho_air:", rho_air)

# Full-range tests
betas = np.arange(-15, 16)
# betas = [0, 5, 10, 15]
nllt = {}  # Coefficients for Phillips' NLLT, keyed by `beta`

print("\nRunning tests...")
t_start = time.perf_counter()

for kb, beta in enumerate(betas):
    dFs, dMs, Fs, Ms, Mc4s, solutions = [], [], [], [], [], []
    cp_wing = wing.control_points(0)  # Section control points

    # Some figures will look for samples at alpha = [0, 5, 10, 15], so make
    # sure to include those test points.
    alphas_down = np.linspace(4, -5, 19)[1:]
    alphas_up = np.linspace(4, 22, 37)

    # First with decreasing alpha
    ref = None
    for ka, alpha in enumerate(alphas_down):
        print(f"\rTest: alpha: {alpha:6.2f}, beta: {beta}", end="")
        alpha_rad = np.deg2rad(alpha)
        beta_rad = np.deg2rad(beta)
        sa, sb = np.sin(alpha_rad), np.sin(beta_rad)
        ca, cb = np.cos(alpha_rad), np.cos(beta_rad)
        v_W2b = np.asarray([ca * cb, sb, sa * cb])
        v_W2b *= -v_mag  # The Reynolds numbers are a function of the magnitude

        try:
            dF, dM, ref = wing.forces_and_moments(
                0, 0, 0, v_W2b=v_W2b, rho_air=rho_air, reference_solution=ref,
            )
        except gsim.foil.ForceEstimator.ConvergenceError:
            ka -= 1
            break

        F = dF.sum(axis=0)
        M = dM.sum(axis=0)  # Moment due to section `Cm`
        M += np.cross(cp_wing, dF).sum(axis=0)  # Add the moment due to forces

        dFs.append(dF)
        dMs.append(dM)
        Fs.append(F)
        Ms.append(M)
        Mc4s.append(dM.sum(axis=0))
        solutions.append(ref)

    alphas_down = alphas_down[:ka+1]  # Truncate when convergence failed

    # Reverse the order
    dFs = dFs[::-1]
    dMs = dMs[::-1]
    Fs = Fs[::-1]
    Ms = Ms[::-1]
    Mc4s = Mc4s[::-1]
    solutions = solutions[::-1]
    alphas_down = alphas_down[::-1]

    # Continue with increasing alpha
    ref = None
    for ka, alpha in enumerate(alphas_up):
        print(f"\rTest: alpha: {alpha:6.2f}, beta: {beta}", end="")
        alpha_rad = np.deg2rad(alpha)
        beta_rad = np.deg2rad(beta)
        sa, sb = np.sin(alpha_rad), np.sin(beta_rad)
        ca, cb = np.cos(alpha_rad), np.cos(beta_rad)
        v_W2b = np.asarray([ca * cb, sb, sa * cb])
        v_W2b *= -v_mag  # The Reynolds numbers are a function of the magnitude

        try:
            dF, dM, ref = wing.forces_and_moments(
                0, 0, 0, v_W2b=v_W2b, rho_air=rho_air, reference_solution=ref,
            )
        except gsim.foil.ForceEstimator.ConvergenceError:
            ka -= 1
            break

        F = dF.sum(axis=0)
        M = dM.sum(axis=0)  # Moment due to section `Cm`
        M += np.cross(cp_wing, dF).sum(axis=0)  # Add the moment due to forces

        dFs.append(dF)
        dMs.append(dM)
        Fs.append(F)
        Ms.append(M)
        Mc4s.append(dM.sum(axis=0))
        solutions.append(ref)

    alphas_up = alphas_up[:ka+1]  # Truncate when convergence failed

    nllt[beta] = {
        "alpha": np.r_[alphas_down, alphas_up],  # Converged `alpha`
        "dF": np.asarray(dFs),  # Section forces
        "dM": np.asarray(dMs),  # Net section moments
        "F": np.asarray(Fs),  # Net forces
        "M": np.asarray(Ms),  # Net moments
        "Mc4": np.asarray(Mc4s),  # Section pitching moments
        "solutions": solutions,  # Solutions for Phillips' method
    }
    print()

t_stop = time.perf_counter()
print(f"Finished in {t_stop - t_start:0.2f} seconds\n")

# ---------------------------------------------------------------------------
# Load or compute the aerodynamic coefficients

plotted_betas = {0, 5, 10, 15}  # The betas present in Belloc's plots

# Load the aerodynamic coefficients from other datasets, keyed by beta [deg]
belloc = {}  # Wind tunnel measurements
avl = {}  # AVL's VLM method
xflr5 = {}  # XFLR5's VLM2 method

for beta in betas:
    avl[beta] = np.genfromtxt(f"avl/polars/beta{beta:02}.txt", names=True)
    avl[beta] = {field: avl[beta][field] for field in avl[beta].dtype.fields}

for beta in sorted(plotted_betas.intersection(betas)):
    belloc[beta] = pd.read_csv(f"windtunnel/beta{beta:02}.csv")  # Belloc's raw wind tunnel data
    xflr5[beta] = np.genfromtxt(
        f"xflr5/wing_polars/Belloc_VLM2-b{beta:02}-Inviscid.txt",
        skip_header=7,
        names=True,
    )

# Compute the force coefficients in wind axes for the AVL dataset
for beta in betas:
    # Transform body -> wind axes. (See "Flight Vehicle Aerodynamics", Drela,
    # 2014, Eq:6.7, page 125). Notice that Drela uses back-right-up instead of
    # front-right-down coordinates, so the CX and CZ terms are negated.
    alpha_rad = np.deg2rad(avl[beta]["alpha"])
    beta_rad = np.deg2rad(beta)
    k = len(avl[beta]["alpha"])
    sa, sb = np.sin(alpha_rad), np.full(k, np.sin(beta_rad))
    ca, cb = np.cos(alpha_rad), np.full(k, np.cos(beta_rad))
    C_w2b = np.array([
        [-ca * cb, -sb, -sa * cb],
        [-ca * sb, cb, -sa * sb],
        [sa, np.zeros(k), -ca]
    ])
    CXa, CYa, CZa = np.einsum(
        "ijk,kj->ik",
        C_w2b,
        np.c_[avl[0]["CX"], avl[0]["CY"], avl[0]["CZ"]]
    )
    avl[beta].update({"CXa": CXa, "CYa": CYa, "CZa": CZa})

# Compute the aerodynamic coefficients from the NLLT simulations. Uses the
# flattened wing area as the reference, as per the paper.
S = canopy.S_flat
q = 0.5 * rho_air * v_mag**2
for beta in betas:

    # Transform body -> wind axes. (See "Flight Vehicle Aerodynamics", Drela,
    # 2014, Eq:6.7, page 125). Notice that Drela uses back-right-up instead of
    # front-right-down coordinates, so the CX and CZ terms are negated.
    alpha_rad = np.deg2rad(nllt[beta]["alpha"])
    beta_rad = np.deg2rad(beta)
    k = len(nllt[beta]["alpha"])
    sa, sb = np.sin(alpha_rad), np.full(k, np.sin(beta_rad))
    ca, cb = np.cos(alpha_rad), np.full(k, np.cos(beta_rad))
    C_w2b = np.array([
        [-ca * cb, -sb, -sa * cb],
        [-ca * sb, cb, -sa * sb],
        [sa, np.zeros(k), -ca]
    ])

    # Body axes
    CX, CY, CZ = nllt[beta]["F"].T / (q * S)
    Cl, Cm, Cn = nllt[beta]["M"].T / (q * S * cc)

    # Wind axes
    CXa, CYa, CZa = np.einsum("ijk,kj->ik", C_w2b, nllt[beta]["F"] / (q * S))
    Cla, Cma, Cna = np.einsum("ijk,kj->ik", C_w2b, nllt[beta]["M"] / (q * S * cc))

    Cm_c4 = nllt[beta]["Mc4"].T[1] / (q * S * cc)  # FIXME: useful?

    nllt[beta].update({
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
    })


# ---------------------------------------------------------------------------
# Coefficient plots

axes_indices = {0: (0, 0), 5: (0, 1), 10: (1, 0), 15: (1, 1)}  # Subplot axes

belloc_args = {"c": "k", "linestyle": "-", "linewidth": 0.75, "label": "Tunnel"}
nllt_args = {"c": "r", "linestyle": "--", "linewidth": 1, "label": "NLLT"}
avl_args = {"c": "b", "linestyle": "--", "linewidth": 0.75, "label": "AVL"}
xflr5_args = {"c": "g", "linestyle": "--", "linewidth": 1, "label": "XFLR5"}
pad_args = {"h_pad": 1.75, "w_pad": 1}

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


plot_avl = True
plot_xflr5 = True

# Plot: CL vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "CL", xlim=(-10, 25), ylim=(-0.35, 1.4))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CZa"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], avl[beta]["CZa"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["alpha"], xflr5[beta]["CL"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], nllt[beta]["CZa"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
fig.savefig(f"CL_vs_alpha.svg", dpi=96)

# Plot: CD vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "CD", xlim=(-10, 25), ylim=(-0.01, 0.18))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CXa"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], avl[beta]["CXa"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["alpha"], xflr5[beta]["CD"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], nllt[beta]["CXa"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
fig.savefig(f"CD_vs_alpha.svg", dpi=96)

# Plot: CY vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "CY", xlim=(-10, 25), ylim=(-0.20, 0.05))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CYa"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], avl[beta]["CYa"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["alpha"], xflr5[beta]["CY"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], nllt[beta]["CYa"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
fig.savefig(f"CY_vs_alpha.svg", dpi=96)

# Plot: CL vs CD
fig, axes = plot4x4("CD", "CL", xlim=(-0.01, 0.18), ylim=(-0.35, 1.4))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["CXa"], belloc[beta]["CZa"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["CXa"], avl[beta]["CZa"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["CD"], xflr5[beta]["CL"], **xflr5_args)
    ax.plot(nllt[beta]["CXa"], nllt[beta]["CZa"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="lower right")
fig.tight_layout(**pad_args)
fig.savefig(f"CL_vs_CD.svg", dpi=96)

# Plot: CL vs Cm
fig, axes = plot4x4("Cm", "CL", xlim=(-0.6, 0.08), ylim=(-0.35, 1.0))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["CMT1"][:42], belloc[beta]["CZa"][:42], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["Cm"], avl[beta]["CZa"], **avl_args)
    # if plot_xflr5:
    #     ax.plot(xflr5[beta]["Cm"], xflr5[beta]["CL"], **xflr5_args)
    ax.plot(nllt[beta]["Cm"], nllt[beta]["CZa"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
fig.savefig(f"CL_vs_Cm.svg", dpi=96)

# Plot: Cl vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "Cl", xlim=(-10, 25), ylim=(-0.21, 0.035))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CLT1"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], avl[beta]["Cl"], **avl_args)
    # if plot_xflr5:
    #     ax.plot(xflr5[beta]["alpha"], xflr5[beta]["Cl"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], nllt[beta]["Cl"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
fig.savefig(f"Cl_vs_alpha.svg", dpi=96)

# Plot: Cm vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "Cm", xlim=(-10, 25), ylim=(-1.25, 0.25))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CMT1"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], avl[beta]["Cm"], **avl_args)
    # if plot_xflr5:
    #     ax.plot(xflr5[beta]["alpha"], xflr5[beta]["Cm"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], nllt[beta]["Cm"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
fig.savefig(f"Cm_vs_alpha.svg", dpi=96)

# Plot: Cn vs alpha
fig, axes = plot4x4("$\\alpha$ [deg]", "Cn", xlim=(-10, 25), ylim=(-0.04, 0.24))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CNT1"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], avl[beta]["Cn"], **avl_args)
    # if plot_xflr5:
    #     ax.plot(xflr5[beta]["alpha"], xflr5[beta]["Cn"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], nllt[beta]["Cn"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
fig.savefig(f"Cn_vs_alpha.svg", dpi=96)

# ---------------------------------------------------------------------------

# Build sets of coefficients over `betas`, keyed by alpha
nllt2 = {
    alpha: {
        "Cy": [],
        "Cl": [],
        "Cm": [],
        "Cn": [],
        "CXa": [],
        "CYa": [],
        "CZa": [],
    } for alpha in [0, 5, 10, 15]
}
for beta in betas:
    for alpha in [0, 5, 10, 15]:
        ix = np.nonzero(np.isclose(nllt[beta]["alpha"], alpha))
        if ix[0].shape[0]:
            nllt2[alpha]["CXa"].append(nllt[beta]["CXa"][ix][0])
            nllt2[alpha]["CYa"].append(nllt[beta]["CYa"][ix][0])
            nllt2[alpha]["CZa"].append(nllt[beta]["CZa"][ix][0])
            nllt2[alpha]["Cl"].append(nllt[beta]["Cl"][ix][0])
            nllt2[alpha]["Cm"].append(nllt[beta]["Cm"][ix][0])
            nllt2[alpha]["Cn"].append(nllt[beta]["Cn"][ix][0])
        else:  # pad to keep the sequences the same length as `betas`
            nllt2[alpha]["CXa"].append(np.nan)
            nllt2[alpha]["CYa"].append(np.nan)
            nllt2[alpha]["CZa"].append(np.nan)
            nllt2[alpha]["Cl"].append(np.nan)
            nllt2[alpha]["Cm"].append(np.nan)
            nllt2[alpha]["Cn"].append(np.nan)

avl2 = {
    alpha: {
        "CXa": [],
        "CYa": [],
        "CZa": [],
        "Cl": [],
        "Cm": [],
        "Cn": [],
    } for alpha in [0, 5, 10, 15]
}
for beta in betas:
    alpha_rad = np.deg2rad(avl[beta]["alpha"])
    for alpha in [0, 5, 10, 15]:
        ix = np.nonzero(np.isclose(avl[beta]["alpha"], alpha))
        avl2[alpha]["CXa"].append(avl[beta]["CXa"][ix][0])
        avl2[alpha]["CYa"].append(avl[beta]["CYa"][ix][0])
        avl2[alpha]["CZa"].append(avl[beta]["CZa"][ix][0])
        avl2[alpha]["Cl"].append(avl[beta]["Cl"][ix][0])
        avl2[alpha]["Cm"].append(avl[beta]["Cm"][ix][0])
        avl2[alpha]["Cn"].append(avl[beta]["Cn"][ix][0])

belloc2 = {a: pd.read_csv(f"windtunnel/alpha{a:02}v40.csv") for a in [0, 5, 10, 15]}

# Plot: CD vs beta
fig, axes = plot4x4(r"$\beta$ [deg]", "CD", (-17, 17), (-0.01, 0.18))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CXa"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["CXa"], **avl_args)
    ax.plot(betas, nllt2[alpha]["CXa"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
fig.savefig(f"CD_vs_beta.svg", dpi=96)

# Plot: CY vs beta
fig, axes = plot4x4(r"$\beta$ [deg]", r"CY", (-17, 17), (-0.23, 0.23))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CYa"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["CYa"], **avl_args)
    ax.plot(betas, nllt2[alpha]["CYa"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
fig.savefig(f"CY_vs_beta.svg", dpi=96)

# Plot: CL vs beta
fig, axes = plot4x4(r"$\beta$ [deg]", "CL", (-17, 17), (-0.01, 1.05))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CZa"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["CZa"], **avl_args)
    ax.plot(betas, nllt2[alpha]["CZa"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
fig.savefig(f"CL_vs_beta.svg", dpi=96)

# Plot: Cl (wing rolling coefficient) vs beta
fig, axes = plot4x4(r"$\beta$ [deg]", "Cl", (-17, 17), (-0.2, 0.2))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CLT1"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["Cl"], **avl_args)
    ax.plot(betas, nllt2[alpha]["Cl"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
fig.savefig(f"Cl_vs_beta.svg", dpi=96)

# Plot: Cm (wing pitching coefficient) vs beta
fig, axes = plot4x4(r"$\beta$ [deg]", "Cm", (-17, 17), (-0.65, 0.1))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CMT1"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["Cm"], **avl_args)
    ax.plot(betas, nllt2[alpha]["Cm"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
fig.savefig(f"Cm_vs_beta.svg", dpi=96)

# Plot: Cn (wing yawing coefficient) vs beta
fig, axes = plot4x4(r"$\beta$ [deg]", "Cn", (-17, 17), (-0.2, 0.2))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CNT1"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["Cn"], **avl_args)
    ax.plot(betas, nllt2[alpha]["Cn"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
fig.savefig(f"Cn_vs_beta.svg", dpi=96)

plt.show()

embed()
