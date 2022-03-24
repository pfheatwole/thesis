"""
Recreate the paraglider analysis in [1]_ using multiple aerodynamics models.

0. Raw wind tunnel data

1. AVL (VLM)

2. XFLR5 (VLM)

3. `pfh.glidersim` (Phillips' nonlinear lifting-line model [2]_)

.. [1] Hervé Belloc, "Wind Tunnel Investigation of a Rigid Paraglider Reference
       Wing", 2015

.. [2] W. F. Phillips and D. O. Snyder, "Modern adaptation of Prandtl's classic
       lifting-line theory", 2000
"""

import time

import matplotlib.pyplot as plt
import numpy as np
import pfh.glidersim as gsim
import scipy.interpolate


###############################################################################
# Wing specifications from the paper

# Table 1: the full-scale wing dimensions converted into 1/8 model
h = 3 / 8  # Arch height (vertical deflection from wing root to tips) [m]
cc = 2.8 / 8  # Central chord [m]
b = 11.00 / 8  # Projected span [m]
S = 25.08 / (8 ** 2)  # Projected area [m^2]
AR = 4.82  # Projected aspect ratio

b_flat = 13.64 / 8  # Flattened span [m]
S_flat = 28.56 / (8 ** 2)  # Flattened area [m^2]
AR_flat = 6.52  # Flattened aspect ratio

# Table 2: geometry for the 1/8 model, left-to-right
# fmt: off
xyz = np.array(  # Coordinates along the 0.6c line [m]
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
# fmt: on

theta = np.deg2rad([3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3])  # torsion [deg]


###############################################################################
# Build the canopy and wing models


class InterpolatedArc:
    """Interface to use point-definitions for the arc.

    FIXME: resample+Pchip is kludgy; do a proper piecewise-linear implementation
    """

    def __init__(self, s, y, z):
        sr = np.linspace(-1, 1, 1000)  # Resample so the cubic-fit stays linear
        fy = scipy.interpolate.interp1d(s, y)
        fz = scipy.interpolate.interp1d(s, z)
        self._f = scipy.interpolate.PchipInterpolator(sr, np.c_[fy(sr), fz(sr)])
        self._fd = self._f.derivative()

    def __call__(self, s):
        return self._f(s)

    def derivative(self, s):
        return self._fd(s)


# Section indices are the normalized distances from the central section along
# the length of the `yz` curve (so s=±1 for the right/left wingtips, and s=0
# for the central section).
L_segments = np.linalg.norm(np.diff(xyz.T[1:]), axis=0)
s = np.cumsum(np.r_[0, L_segments]) / L_segments.sum() * 2 - 1
s = s.clip(-1, 1)  # Floating-point error means `s` might slightly exceed ±1

# The FoilLayout uses lengths normalized by the semispan since it makes it
# easier to define parametric representations, so raw coordinates must be
# normalized first.

# Option 1: use the piecewise-linear physical geometry (sampled ellipse):
arc = InterpolatedArc(
    s,
    y=xyz.T[1] / (b_flat / 2),
    z=(xyz.T[2] - xyz[6, 2]) / (b_flat / 2),  # Central section at `z = 0`
)

# Option 2: use the analytical geometry (true ellipse)
# arc = gsim.foil_layout.EllipticalArc(np.rad2deg(np.arctan(0.375 / 0.688)), 89)

layout = gsim.foil_layout.FoilLayout(
    x=0,
    r_x=0.6,
    yz=arc,
    r_yz=0.6,
    c=scipy.interpolate.interp1d(s, c / (b_flat / 2)),
    theta=scipy.interpolate.interp1d(s, theta),
)

airfoil = gsim.airfoil.NACA(23015, convention="vertical")
sections = gsim.foil_sections.FoilSections(
    profiles=gsim.airfoil.AirfoilGeometryInterpolator({0: airfoil}),
    coefficients=gsim.airfoil.XFLR5Coefficients("../xflr5/airfoil_polars", flapped=False),
    # Cd_surface=0.004,  # ref: ware1969WindtunnelInvestigationRamair
)

# Pseudo-inviscid mode
# sections.Cd = lambda s, ai, alpha, Re, clamp: 0


canopy = gsim.foil.SimpleFoil(
    layout=layout,
    sections=sections,
    b_flat=b_flat,
    aerodynamics_method=gsim.foil_aerodynamics.Phillips,
    aerodynamics_config={
        "v_ref_mag": 40,
        "alpha_ref": 5,
        "s_nodes": s,
        # "s_clamp": s_nodes[-1],  # Not supported by XFLR5Coefficients
    },
)

print()
print("Finished defining the canopy. Checking fit...")
print(f"  Projected area> Expected: {S:.4f},   Actual: {canopy.S:.4f}")
print(f"  Flattened area> Expected: {S_flat:.4f},   Actual: {canopy.S_flat:.4f}")
print(f"    Projected AR> Expected: {AR:.4f},   Actual: {canopy.AR:.4f}")
print(f"    Flattened AR> Expected: {AR_flat:.4f},   Actual: {canopy.AR_flat:.4f}")
print()

# This model is overkill for this simulation, but it allows the ParagliderWing
# to to calculate the moments about the reference point.
lines = gsim.paraglider_wing.SimpleLineGeometry(
    kappa_x=0.0875,  # Reference point is 25% back from the leading edge
    kappa_z=1.0,  # Reference point is 1m below the central chord
    kappa_A=0,  # unused
    kappa_C=1,  # unused
    kappa_a=0,  # unused
    total_line_length=0,  # unused
    average_line_diameter=0,  # unused
    r_L2LE=[0, 0, 0],  # unused
    Cd_lines=0,  # unused
    s_delta_start0=0,  # unused
    s_delta_start1=0,  # unused
    s_delta_stop0=1,  # unused
    s_delta_stop1=1,  # unused
    kappa_b=0,  # unused
)

wing = gsim.paraglider_wing.ParagliderWing(
    lines=lines,
    canopy=canopy,
    rho_upper=1,  # unused
    rho_lower=1,  # unused
)

# print("\nFinished defining the complete wing. Pausing for review.\n")
# gsim.plots.plot_foil(canopy, N_sections=121)
# gsim.plots.plot_foil_topdown(canopy, N_sections=13)  # Belloc Fig:2
# breakpoint()
# 1/0


###############################################################################
# Simulate the wind tunnel tests using the NLLT aerodynamics model

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

print("\nRunning simulations...")
betas = np.arange(-15, 16)
nllt: dict[int, dict] = {}  # Results for Phillips' NLLT, keyed by `beta` [deg]
t_start = time.perf_counter()
for _kb, beta in enumerate(betas):
    dFs, dMs, Fs, Ms, Mc4s, solutions = [], [], [], [], [], []
    r_LE2RM = -wing.r_RM2LE(0)
    r_CP2LE = wing.r_CP2LE(0)
    r_CP2RM = r_CP2LE + r_LE2RM

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
        v_W2b = np.asfarray([ca * cb, sb, sa * cb])
        v_W2b *= -v_mag  # The Reynolds numbers are a function of the magnitude

        try:
            dF, dM, ref = wing.aerodynamics(
                0, 0, 0, v_W2b=v_W2b, rho_air=rho_air, reference_solution=ref
            )
        except gsim.foil_aerodynamics.ConvergenceError:
            ka -= 1
            break

        F = dF.sum(axis=0)
        M = dM.sum(axis=0)  # Moment due to section `Cm`
        M += np.cross(r_CP2RM, dF).sum(axis=0)  # Add the moment due to forces

        dFs.append(dF)
        dMs.append(dM)
        Fs.append(F)
        Ms.append(M)
        Mc4s.append(dM.sum(axis=0))
        solutions.append(ref)

    alphas_down = alphas_down[: ka + 1]  # Truncate when convergence failed

    # Continue with increasing alpha
    dFs.reverse()
    dMs.reverse()
    Fs.reverse()
    Ms.reverse()
    Mc4s.reverse()
    solutions.reverse()
    alphas_down = alphas_down[::-1]
    ref = None
    for ka, alpha in enumerate(alphas_up):
        print(f"\rTest: alpha: {alpha:6.2f}, beta: {beta}", end="")
        alpha_rad = np.deg2rad(alpha)
        beta_rad = np.deg2rad(beta)
        sa, sb = np.sin(alpha_rad), np.sin(beta_rad)
        ca, cb = np.cos(alpha_rad), np.cos(beta_rad)
        v_W2b = np.asfarray([ca * cb, sb, sa * cb])
        v_W2b *= -v_mag  # The Reynolds numbers are a function of the magnitude

        try:
            dF, dM, ref = wing.aerodynamics(
                0, 0, 0, v_W2b=v_W2b, rho_air=rho_air, reference_solution=ref
            )
        except gsim.foil_aerodynamics.ConvergenceError:
            ka -= 1
            break

        F = dF.sum(axis=0)
        M = dM.sum(axis=0)  # Moment due to section `Cm`
        M += np.cross(r_CP2RM, dF).sum(axis=0)  # Add the moment due to forces

        dFs.append(dF)
        dMs.append(dM)
        Fs.append(F)
        Ms.append(M)
        Mc4s.append(dM.sum(axis=0))
        solutions.append(ref)

    alphas_up = alphas_up[: ka + 1]  # Truncate when convergence failed

    nllt[beta] = {
        "alpha": np.r_[alphas_down, alphas_up],  # Converged `alpha`
        "dF": np.asfarray(dFs),  # Individual section forces
        "dM": np.asfarray(dMs),  # Individual section moments
        "F": np.asfarray(Fs),  # Net forces
        "M": np.asfarray(Ms),  # Net moments
        "Mc4": np.asfarray(Mc4s),  # Net moments from section pitching moments
        "solutions": solutions,  # Solutions for Phillips' method
    }
    print()

t_stop = time.perf_counter()
print(f"Finished in {t_stop - t_start:0.2f} seconds\n")


###############################################################################
# Load or compute the aerodynamic coefficients

plotted_betas = {0, 5, 10, 15}  # The betas present in Belloc's plots

# Dataset: wind tunnel
belloc: dict[int, dict] = {}  # Keyed by `beta` [deg]
for beta in plotted_betas:
    belloc[beta] = np.genfromtxt(
        f"../windtunnel/beta{beta:02}.csv",
        names=True,
        delimiter=",",
    )

# Dataset: XFLR5
xflr5: dict[int, dict] = {}  # Keyed by `beta` [deg]
for beta in plotted_betas:
    xflr5[beta] = np.genfromtxt(
        f"../xflr5/wing_polars/Belloc_VLM2-b{beta:02}-Inviscid.txt",
        skip_header=7,
        names=True,
    )

# Dataset: AVL
avl: dict[int, dict] = {}  # Keyed by `beta` [deg]
for beta in betas:
    data = np.genfromtxt(f"../avl/polars/beta{beta:02}.txt", names=True)
    avl[beta] = {field: data[field] for field in data.dtype.fields}
    euler = np.stack(np.broadcast_arrays(0, -data["alpha"], beta), axis=-1)
    CXa, CYa, CZa = np.einsum(  # Force coefficients in wind axes
        "ijk,ik->ij",
        gsim.orientation.euler_to_dcm(np.deg2rad(euler), intrinsic=False),  # C_w2b
        np.c_[avl[beta]["CX"], avl[beta]["CY"], avl[beta]["CZ"]],
    ).T
    avl[beta].update({"CXa": CXa, "CYa": CYa, "CZa": CZa})

# Dataset: NLLT
S = canopy.S_flat  # Flattened wing as the reference area
q = 0.5 * rho_air * v_mag ** 2
for beta in betas:
    if len(nllt[beta]["alpha"]) == 0:
        # Pad to keep the sequences the same length as `betas`
        nllt[beta].update(
            {
                "CX": np.array([]),
                "CY": np.array([]),
                "CZ": np.array([]),
                "Cl": np.array([]),
                "Cm": np.array([]),
                "Cn": np.array([]),
                "CXa": np.array([]),
                "CYa": np.array([]),
                "CZa": np.array([]),
                "Cla": np.array([]),
                "Cma": np.array([]),
                "Cna": np.array([]),
                "Cm_c4": np.array([]),
            }
        )
        continue

    # Body axes
    CX, CY, CZ = nllt[beta]["F"].T / (q * S)
    Cl, Cm, Cn = nllt[beta]["M"].T / (q * S * cc)
    Cm_c4 = nllt[beta]["Mc4"].T[1] / (q * S * cc)  # FIXME: useful?

    # Wind axes
    euler = np.stack(np.broadcast_arrays(0, -nllt[beta]["alpha"], beta), axis=-1)
    C_w2b = gsim.orientation.euler_to_dcm(np.deg2rad(euler), intrinsic=False)
    CXa, CYa, CZa = np.einsum("ijk,ik->ij", C_w2b, nllt[beta]["F"] / (q * S)).T
    Cla, Cma, Cna = np.einsum("ijk,ik->ij", C_w2b, nllt[beta]["M"] / (q * S * cc)).T

    nllt[beta].update(
        {
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
            "Cm_c4": Cm_c4,
        }
    )

# ----------------------------------------------------------------------------
# Build alternate groupings of coefficients over `betas`, keyed by `alpha`

belloc2: dict[float, dict] = {}
for alpha in [0, 5, 10, 15]:
    filename = f"../windtunnel/alpha{alpha:02}v40.csv"
    belloc2[alpha] = np.genfromtxt(filename, names=True, delimiter=",")

avl2: dict[float, dict] = {}
for alpha in [0, 5, 10, 15]:
    CXa, CYa, CZa, Cl, Cm, Cn = [], [], [], [], [], []
    for beta in betas:
        alpha_rad = np.deg2rad(avl[beta]["alpha"])
        ix = np.nonzero(np.isclose(avl[beta]["alpha"], alpha))
        CXa.append(avl[beta]["CXa"][ix][0])
        CYa.append(avl[beta]["CYa"][ix][0])
        CZa.append(avl[beta]["CZa"][ix][0])
        Cl.append(avl[beta]["Cl"][ix][0])
        Cm.append(avl[beta]["Cm"][ix][0])
        Cn.append(avl[beta]["Cn"][ix][0])
    avl2[alpha] = {
        "CXa": np.asfarray(CXa),
        "CYa": np.asfarray(CYa),
        "CZa": np.asfarray(CZa),
        "Cl": np.asfarray(Cl),
        "Cm": np.asfarray(Cm),
        "Cn": np.asfarray(Cn),
    }

nllt2: dict[float, dict] = {}
for alpha in [0, 5, 10, 15]:
    CXa, CYa, CZa, Cl, Cm, Cn = [], [], [], [], [], []
    for beta in betas:
        ix = np.nonzero(np.isclose(nllt[beta]["alpha"], alpha))
        if ix[0].shape[0]:
            CXa.append(nllt[beta]["CXa"][ix][0])
            CYa.append(nllt[beta]["CYa"][ix][0])
            CZa.append(nllt[beta]["CZa"][ix][0])
            Cl.append(nllt[beta]["Cl"][ix][0])
            Cm.append(nllt[beta]["Cm"][ix][0])
            Cn.append(nllt[beta]["Cn"][ix][0])
        else:  # pad to keep the sequences the same length as `betas`
            CXa.append(np.nan)
            CYa.append(np.nan)
            CZa.append(np.nan)
            Cl.append(np.nan)
            Cm.append(np.nan)
            Cn.append(np.nan)
    nllt2[alpha] = {
        "CXa": np.asfarray(CXa),
        "CYa": np.asfarray(CYa),
        "CZa": np.asfarray(CZa),
        "Cl": np.asfarray(Cl),
        "Cm": np.asfarray(Cm),
        "Cn": np.asfarray(Cn),
    }


###############################################################################
# Plot the coefficients using the wind axes (front-right-down coordinates where
# the x-axis points directly into the oncoming wind)
#
# Belloc and XFLR5 use back-right-up coordinate axes (which is convenient since
# `CL = CZa`), but AVL and NLLT use front-right-down so their X and Z
# components (CXa, CZa, Cla, Cna) must be negated.


def plot2x2(xlabel, ylabel, xlim=None, ylim=None):
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
    axes[0, 0].grid(c="lightgrey", linestyle="--")
    axes[0, 1].grid(c="lightgrey", linestyle="--")
    axes[1, 0].grid(c="lightgrey", linestyle="--")
    axes[1, 1].grid(c="lightgrey", linestyle="--")
    return fig, axes


belloc_args = {"c": "k", "linestyle": "-", "linewidth": 0.75, "label": "Tunnel"}
avl_args = {"c": "b", "linestyle": "--", "linewidth": 0.75, "label": "AVL"}
xflr5_args = {"c": "g", "linestyle": "--", "linewidth": 1, "label": "XFLR5"}
nllt_args = {"c": "r", "linestyle": "--", "linewidth": 1, "label": "NLLT"}
axes_indices = {0: (0, 0), 5: (0, 1), 10: (1, 0), 15: (1, 1)}  # Subplot axes
pad_args = {"h_pad": 1.75, "w_pad": 1}

plot_avl = True
plot_xflr5 = True
savefig = False  # Export the figures as SVG files


# Plot: CL vs alpha
fig, axes = plot2x2("$\\alpha$ [deg]", "CL", xlim=(-10, 25), ylim=(-0.35, 1.4))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CZa"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], -avl[beta]["CZa"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["alpha"], xflr5[beta]["CL"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], -nllt[beta]["CZa"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("CL_vs_alpha.svg", dpi=96)

# Plot: CD vs alpha
fig, axes = plot2x2("$\\alpha$ [deg]", "CD", xlim=(-10, 25), ylim=(-0.01, 0.18))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CXa"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], -avl[beta]["CXa"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["alpha"], xflr5[beta]["CD"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], -nllt[beta]["CXa"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("CD_vs_alpha.svg", dpi=96)

# Plot: CY vs alpha
fig, axes = plot2x2("$\\alpha$ [deg]", "CY", xlim=(-10, 25), ylim=(-0.20, 0.05))
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
if savefig:
    fig.savefig("CY_vs_alpha.svg", dpi=96)

# Plot: CL vs CD
fig, axes = plot2x2("CD", "CL", xlim=(-0.01, 0.18), ylim=(-0.35, 1.4))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["CXa"], belloc[beta]["CZa"], **belloc_args)
    if plot_avl:
        ax.plot(-avl[beta]["CXa"], -avl[beta]["CZa"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["CD"], xflr5[beta]["CL"], **xflr5_args)
    ax.plot(-nllt[beta]["CXa"], -nllt[beta]["CZa"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="lower right")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("CL_vs_CD.svg", dpi=96)

# Plot: CL vs Cm
fig, axes = plot2x2("Cm", "CL", xlim=(-0.6, 0.08), ylim=(-0.35, 1.0))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["CMT1"][:42], belloc[beta]["CZa"][:42], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["Cm"], -avl[beta]["CZa"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["Cm"], xflr5[beta]["CL"], **xflr5_args)
    ax.plot(nllt[beta]["Cm"], -nllt[beta]["CZa"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("CL_vs_Cm.svg", dpi=96)

# Plot: Cl vs alpha
fig, axes = plot2x2("$\\alpha$ [deg]", "Cl", xlim=(-10, 25), ylim=(-0.21, 0.035))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CLT1"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], avl[beta]["Cl"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["alpha"], xflr5[beta]["Cl"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], nllt[beta]["Cl"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("Cl_vs_alpha.svg", dpi=96)

# Plot: Cm vs alpha
fig, axes = plot2x2("$\\alpha$ [deg]", "Cm", xlim=(-10, 25), ylim=(-1.25, 0.25))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CMT1"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], avl[beta]["Cm"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["alpha"], xflr5[beta]["Cm"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], nllt[beta]["Cm"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("Cm_vs_alpha.svg", dpi=96)

# Plot: Cn vs alpha
fig, axes = plot2x2("$\\alpha$ [deg]", "Cn", xlim=(-10, 25), ylim=(-0.04, 0.24))
for beta in sorted(plotted_betas.intersection(betas)):
    ax = axes[axes_indices[beta]]
    ax.plot(belloc[beta]["Alphac"], belloc[beta]["CNT1"], **belloc_args)
    if plot_avl:
        ax.plot(avl[beta]["alpha"], avl[beta]["Cn"], **avl_args)
    if plot_xflr5:
        ax.plot(xflr5[beta]["alpha"], xflr5[beta]["Cn"], **xflr5_args)
    ax.plot(nllt[beta]["alpha"], nllt[beta]["Cn"], **nllt_args)
    ax.set_title(f"$\\beta$={beta}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("Cn_vs_alpha.svg", dpi=96)

# Plot: CD vs beta
fig, axes = plot2x2(r"$\beta$ [deg]", "CD", (-17, 17), (-0.01, 0.18))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CXa"], **belloc_args)
    if plot_avl:
        ax.plot(betas, -avl2[alpha]["CXa"], **avl_args)
    ax.plot(betas, -nllt2[alpha]["CXa"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("CD_vs_beta.svg", dpi=96)

# Plot: CY vs beta
fig, axes = plot2x2(r"$\beta$ [deg]", r"CY", (-17, 17), (-0.23, 0.23))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CYa"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["CYa"], **avl_args)
    ax.plot(betas, nllt2[alpha]["CYa"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("CY_vs_beta.svg", dpi=96)

# Plot: CL vs beta
fig, axes = plot2x2(r"$\beta$ [deg]", "CL", (-17, 17), (-0.01, 1.05))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CZa"], **belloc_args)
    if plot_avl:
        ax.plot(betas, -avl2[alpha]["CZa"], **avl_args)
    ax.plot(betas, -nllt2[alpha]["CZa"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("CL_vs_beta.svg", dpi=96)

# Plot: Cl (wing rolling coefficient) vs beta
fig, axes = plot2x2(r"$\beta$ [deg]", "Cl", (-17, 17), (-0.2, 0.2))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CLT1"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["Cl"], **avl_args)
    ax.plot(betas, nllt2[alpha]["Cl"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("Cl_vs_beta.svg", dpi=96)

# Plot: Cm (wing pitching coefficient) vs beta
fig, axes = plot2x2(r"$\beta$ [deg]", "Cm", (-17, 17), (-0.65, 0.1))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CMT1"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["Cm"], **avl_args)
    ax.plot(betas, nllt2[alpha]["Cm"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="lower left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("Cm_vs_beta.svg", dpi=96)

# Plot: Cn (wing yawing coefficient) vs beta
fig, axes = plot2x2(r"$\beta$ [deg]", "Cn", (-17, 17), (-0.2, 0.2))
for alpha in [0, 5, 10, 15]:
    ax = axes[axes_indices[alpha]]
    ax.plot(belloc2[alpha]["Beta"], belloc2[alpha]["CNT1"], **belloc_args)
    if plot_avl:
        ax.plot(betas, avl2[alpha]["Cn"], **avl_args)
    ax.plot(betas, nllt2[alpha]["Cn"], **nllt_args)
    ax.set_title(f"$\\alpha$={alpha}°")
axes[0, 0].legend(loc="upper left")
fig.tight_layout(**pad_args)
if savefig:
    fig.savefig("Cn_vs_beta.svg", dpi=96)

plt.show()

# breakpoint()
