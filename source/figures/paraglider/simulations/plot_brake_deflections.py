import matplotlib.pyplot as plt
import numpy as np

import pfh.glidersim as gsim
from pfh.glidersim import orientation


class ProfileInterpolator:
    """Linear interpolator over section profiles as a function of delta_f.

    FIXME: nasty hack just to create some diagrams
    """

    def __init__(self, profiles):
        """
        profiles : dict
            A dictionary of {delta_f: {name, AirfoilGeometry}}
        """
        self.profiles = profiles
        self.delta_fs = np.array(sorted(profiles.keys()))

    def _interpolate(self, r, delta_f, surface):
        df = np.rad2deg(delta_f)
        if df > max(self.delta_fs):
            raise ValueError("delta_f exceeds the maximum in the profile set")
        d1 = self.delta_fs[np.argwhere(self.delta_fs <= df).max()]
        d2 = self.delta_fs[np.argwhere(self.delta_fs >= df).min()]

        if surface == "profile":
            xz1 = self.profiles[d1]["airfoil"].profile_curve(r)
            xz2 = self.profiles[d2]["airfoil"].profile_curve(r)
        elif surface == "camber":
            xz1 = self.profiles[d1]["airfoil"].camber_curve(r)
            xz2 = self.profiles[d2]["airfoil"].camber_curve(r)
        else:
            raise ValueError("profile must be 'profile' or 'surface'")

        p = 0 if d2 == d1 else (df - d1) / (d2 - d1)
        return (1 - p) * xz1 + p * xz2

    def profile_curve(self, r, delta_f):
        return self._interpolate(r, delta_f, "profile")

    def camber_curve(self, r, delta_f):
        return self._interpolate(r, delta_f, "camber")


if __name__ == "__main__":
    wing = gsim.extras.wings.build_hook3(verbose=True)

    airfoils = gsim.extras.airfoils.load_datfile_set(
        "braking_NACA24018_Xtr0.25",
    )
    interp = ProfileInterpolator(airfoils)

    N = 91
    s = np.linspace(-1, 1, N)
    xyz = wing.canopy.surface_xyz(s, 0, surface="chord")  # Section origins
    c = wing.canopy.chord_length(s)
    T = wing.canopy.section_orientation(s)  # Section DCMs

    def plot_deflections(delta_bl, delta_br, save=False):
        figd, axd = plt.subplots()  # delta_d
        figf, axf = plt.subplots()  # delta_f
        figTE, axTE = plt.subplots()  # trailing edge yz

        delta_d = wing.lines.delta_d(s, delta_bl, delta_br)
        delta_d /= max(delta_d)  # Normalize the magnitudes
        axd.plot(s, delta_d, linewidth=0.75, c="k")
        axd.set_ylim(-0.08, 1.08)
        axd.set_xlabel("Section index $s$")
        axd.set_ylabel("Normalized deflection distance")
        axd.grid(True)

        delta_f = np.zeros(N)
        points = []
        for d in delta_f:
            points.append(interp.profile_curve(1, d))
        p = np.asarray(points)
        p2 = c[:, None] * np.array([-p[:, 0], np.zeros(N), -p[:, 1]]).T
        p3 = np.einsum("ijk,ik->ij", T, p2)
        p4 = xyz + p3
        axTE.plot(
            p4.T[1], p4.T[2], linestyle="--", linewidth=0.75, c="k", alpha=0.5,
        )

        delta_f = wing.delta_f(s, delta_bl, delta_br)
        points = []
        for d in delta_f:
            points.append(interp.camber_curve(1, d))
        p = np.asarray(points)
        p2 = c[:, None] * np.array([-p[:, 0], np.zeros(N), -p[:, 1]]).T
        p3 = np.einsum("ijk,ik->ij", T, p2)
        p4 = xyz + p3
        axTE.plot(p4.T[1], p4.T[2], linestyle="--", linewidth=0.75, c="k")
        axTE.set_aspect("equal")
        axTE.invert_yaxis()

        axf.plot(s, np.rad2deg(delta_f), linewidth=0.75, c='k')
        axf.set_ylim(-1, 14)
        axf.set_xlabel("Section index $s$")
        axf.set_ylabel(r"Deflection angle $\delta_f$ [deg]")
        axf.grid(True)

        plt.show()

        if save:
            figd.savefig(f"Hook3_deltad_{delta_bl:.2f}_{delta_br:.2f}.svg")
            figf.savefig(f"Hook3_deltaf_{delta_bl:.2f}_{delta_br:.2f}.svg")
            figTE.savefig(f"Hook3_TE_{delta_bl:.2f}_{delta_br:.2f}.svg")

    savefig = False
    plot_deflections(0.25, 0.50, save=savefig)
    plot_deflections(1.00, 1.00, save=savefig)
