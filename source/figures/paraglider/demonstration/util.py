import time

import matplotlib.pyplot as plt
import pfh.glidersim as gsim
from pfh.glidersim.extras import simulation


###############################################################################
# Scenario-building utility functions


def zero_controls(T=5):
    """Scenario: zero_inputs."""
    return {}, T


def symmetric_brakes_fast_on(delta_b):
    """Scenario: zero_inputs."""
    t_warmup = 2
    t_rise = 0.5
    t_settle = 5
    braking = simulation.linear_control([(t_warmup, 0), (t_rise, delta_b)])
    inputs = {
        "delta_bl": braking,
        "delta_br": braking,
    }
    T = t_warmup + t_rise + t_settle
    return inputs, T


def symmetric_brakes_fast_off(delta_b):
    """Scenario: zero_inputs."""
    t_warmup = 2
    t_fall = 0.5
    t_settle = 5
    braking = simulation.linear_control([(0, delta_b), (t_warmup, None), (t_fall, 0)])
    inputs = {
        "delta_bl": braking,
        "delta_br": braking,
    }
    T = t_warmup + t_fall + t_settle
    return inputs, T


def symmetric_brakes_fast_on_off(delta_b):
    """Scenario: zero_inputs."""
    t_warmup = 2
    t_rise = 0.5
    t_hold = 2
    t_fall = 0.5
    t_settle = 5
    braking = simulation.linear_control(
        [(t_warmup, 0), (t_rise, delta_b), (t_hold, None), (t_fall, 0)],
    )
    inputs = {
        "delta_bl": braking,
        "delta_br": braking,
    }
    T = t_warmup + t_rise + t_hold + t_fall + t_settle
    return inputs, T


def short_right_turn(delta_br, delta_w):
    """Scenario: short right turn."""
    t_warmup = 2
    t_rise_b = 2
    t_rise_w = 1
    t_hold = 5
    t_fall = 1
    t_settle = 5
    inputs = {
        "delta_br": simulation.linear_control([
            (t_warmup + t_rise_w + t_hold, 0),
            (t_rise_b, delta_br),
            (t_hold, None),
            (t_fall, 0),
        ]),
        "delta_w": simulation.linear_control([
            (t_warmup, 0),
            (t_rise_w, delta_w),
            (t_hold + t_rise_b + t_hold, None),
            (t_fall, 0),
        ]),
    }
    T = t_warmup + t_rise_w + t_hold + + t_rise_b + t_hold + t_fall + t_settle
    return inputs, T


def continuous_right_turn(delta_w, delta_br):
    t_warmup = 2
    t_rise = 1
    t_hold = 5
    inputs = {
        "delta_br": simulation.linear_control(
            [(t_warmup + t_rise + t_hold, 0), (t_rise, delta_br)],
        ),
        "delta_w": simulation.linear_control([(t_warmup, 0), (t_rise, delta_w)]),
    }
    T = 60
    return inputs, T


def roll_right_then_left():
    """Scenario: smooth roll right then roll left."""
    inputs = {
        "delta_br": simulation.linear_control([(2, 0), (2, 0.75), (10, None), (2, 0)]),
        "delta_bl": simulation.linear_control([(16, 0), (3, 0.75)]),
    }
    T = 30
    return inputs, T


def roll_yaw_coupling_with_accelerator():
    """
    Scenario: roll-yaw coupling w/ accelerator.

    Purpose: observe how accelerator increases roll-yaw coupling when brakes
    are applied.

    Notes: not sure how representative this is of a real wing since a real wing
    experiences distorions (eg, profile flattening) when the accelerator is
    applied.
    """
    t_start = 2
    t_warmup = 5
    t_rise = 1.5
    t_hold = 3
    t_fall = 1.5
    inputs = {
        "delta_a": simulation.linear_control([(t_start, 0), (t_rise, 0.75)]),
        "delta_br": simulation.linear_control([
            (t_start + t_warmup, 0),
            (t_rise, 0.75),
            (t_hold, None),
            (t_fall, 0),
        ]),
    }
    T = t_start + t_warmup + t_hold + t_fall + 5
    return inputs, T


def figure_8s(N_cycles=2, duration=30, mag=0.75):
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


def ramping_headwind(t_rise=10, mag=-20):
    _mag = simulation.linear_control([(2, 0), (t_rise, mag)])

    def _headwind(t, r):
        v_W2e = np.zeros(
            (*gsim.util._broadcast_shapes(np.shape(t), np.shape(r)[:-1]), 3),
        )
        v_W2e[..., 0] = _mag(t)
        return v_W2e

    inputs = {
        "v_W2e": _headwind,
    }
    T = 20
    return inputs, T


def centered_thermal(delta_a=0, delta_b=0, py=0, mag=-3, radius5=10):
    """
    Place a thermal in the path of a glider.

    The default is that the wing will hit the thermal dead-center, but `py`
    can be used to shift the thermal and create an indirect hit.

    Parameters
    ----------
    delta_a : float [percentage]
        The amount of accelerator.
    delta_b : float [percentage]
        The amount of symmetric brake.
    py : float [m]
        The y-axis (easterly) offset of the thermal
    mag : float [m/s]
        The strength of the thermal core.
    radius5 : float [m]
        The distance at which the thermal strength has reduced to 5%.
    """
    inputs = {
        "delta_a": delta_a,
        "delta_bl": delta_b,
        "delta_br": delta_b,
        "v_W2e": simulation.CircularThermal(
            px=10 * 10,  # At 10m/s, roughly 10 seconds in
            py=py,
            mag=mag,
            radius5=radius5,
            t_enable=0,
        ),
    }
    T = 20
    return inputs, T


def horizontal_shear(delta_a=0, delta_b=0):
    inputs = {
        "delta_a": delta_a,
        "delta_bl": delta_b,
        "delta_br": delta_b,
        "v_W2e": simulation.HorizontalShear(
            x_start=10 * 10,
            mag=-4,
            smooth=25,
            t_enable=0,
        ),
    }
    T = 20
    return inputs, T


def lateral_gust(delta_a=0, delta_b=0):
    mag = 10  # [mph]
    inputs = {
        "delta_a": delta_a,
        "delta_bl": delta_b,
        "delta_br": delta_b,
        "v_W2e": simulation.LateralGust(
            t_start=2,
            t_ramp=3,
            t_duration=3,
            mag=mag * 1.6 / 3.6,  # [m/s]
        ),
    }
    T = 15
    return inputs, T


###############################################################################
# Model and simulation utlity functions


def build_paragliders(
    use_apparent_mass=True,
    kappa_RM=(-100, 0, -10),  # Coefficients for Theta_p2b
    kappa_RM_dot=(-50, -5, -50),  # Coefficients for dot{Theta_p2b}
):
    """
    Build a set of glider models.

    The size 23 uses a normal "upright" harness, the 25 and 27 use pod-style
    harnesses (to match specs from flight tests by thermik.at and Parapente).
    """

    ###########################################################################
    # Build the wings and appropriate payloads

    # size=23 using an upright harness like mine
    wing23 = gsim.extras.wings.niviuk_hook3(size=23, verbose=True)
    harness23 = gsim.paraglider_harness.Spherical(
        mass=75,
        z_riser=0.5,
        S=0.55,
        CD=0.8,
        kappa_w=0.15,
    )

    # size=25 using a pod harness as in `Hook 3 Parapente Mag 148.pdf`
    wing25 = gsim.extras.wings.niviuk_hook3(size=25, verbose=True)
    harness25 = gsim.paraglider_harness.Spherical(
        mass=94,
        z_riser=0.5,
        S=0.65,
        CD=0.4,
        kappa_w=0.15,
    )

    # size=27 using a pod harness as in `hook_3_perfils.pdf`
    wing27 = gsim.extras.wings.niviuk_hook3(size=27, verbose=True)
    harness27 = gsim.paraglider_harness.Spherical(
        mass=115,
        z_riser=0.5,
        S=0.70,
        CD=0.4,
        kappa_w=0.15,
    )

    ###########################################################################
    # Build the paraglider system models

    # 6 DoF models
    paraglider6a_23 = gsim.paraglider.ParagliderSystemDynamics6a(
        wing23,
        harness23,
        use_apparent_mass=use_apparent_mass,
    )
    paraglider6b_23 = gsim.paraglider.ParagliderSystemDynamics6b(
        wing23,
        harness23,
        # No apparent mass
    )
    paraglider6c_23 = gsim.paraglider.ParagliderSystemDynamics6c(
        wing23,
        harness23,
        # No apparent mass
    )

    paraglider6a_25 = gsim.paraglider.ParagliderSystemDynamics6a(
        wing25,
        harness25,
        use_apparent_mass=use_apparent_mass,
    )
    paraglider6b_25 = gsim.paraglider.ParagliderSystemDynamics6b(
        wing25,
        harness25,
        # No apparent mass
    )
    paraglider6c_25 = gsim.paraglider.ParagliderSystemDynamics6c(
        wing25,
        harness25,
        # No apparent mass
    )

    paraglider6a_27 = gsim.paraglider.ParagliderSystemDynamics6a(
        wing27,
        harness27,
        use_apparent_mass=use_apparent_mass,
    )
    paraglider6b_27 = gsim.paraglider.ParagliderSystemDynamics6b(
        wing27,
        harness27,
        # No apparent mass
    )
    paraglider6c_27 = gsim.paraglider.ParagliderSystemDynamics6c(
        wing27,
        harness27,
        # No apparent mass
    )

    # 9 DoF models
    paraglider9a_23 = gsim.paraglider.ParagliderSystemDynamics9a(
        wing23,
        harness23,
        kappa_RM=kappa_RM,
        kappa_RM_dot=kappa_RM_dot,
        use_apparent_mass=use_apparent_mass,
    )
    paraglider9a_25 = gsim.paraglider.ParagliderSystemDynamics9a(
        wing25,
        harness25,
        kappa_RM=kappa_RM,
        kappa_RM_dot=kappa_RM_dot,
        use_apparent_mass=use_apparent_mass,
    )
    paraglider9a_27 = gsim.paraglider.ParagliderSystemDynamics9a(
        wing27,
        harness27,
        kappa_RM=kappa_RM,
        kappa_RM_dot=kappa_RM_dot,
        use_apparent_mass=use_apparent_mass,
    )

    paraglider9b_23 = gsim.paraglider.ParagliderSystemDynamics9b(
        wing23,
        harness23,
        kappa_RM=kappa_RM,
        kappa_RM_dot=kappa_RM_dot,
        # No apparent mass
    )
    paraglider9b_25 = gsim.paraglider.ParagliderSystemDynamics9b(
        wing25,
        harness25,
        kappa_RM=kappa_RM,
        kappa_RM_dot=kappa_RM_dot,
        # No apparent mass
    )
    paraglider9b_27 = gsim.paraglider.ParagliderSystemDynamics9b(
        wing27,
        harness27,
        kappa_RM=kappa_RM,
        kappa_RM_dot=kappa_RM_dot,
        # No apparent mass
    )

    paraglider9c_23 = gsim.paraglider.ParagliderSystemDynamics9c(
        wing23,
        harness23,
        kappa_RM=kappa_RM,
        kappa_RM_dot=kappa_RM_dot,
        use_apparent_mass=use_apparent_mass,
    )
    paraglider9c_25 = gsim.paraglider.ParagliderSystemDynamics9c(
        wing25,
        harness25,
        kappa_RM=kappa_RM,
        kappa_RM_dot=kappa_RM_dot,
        use_apparent_mass=use_apparent_mass,
    )
    paraglider9c_27 = gsim.paraglider.ParagliderSystemDynamics9c(
        wing27,
        harness27,
        kappa_RM=kappa_RM,
        kappa_RM_dot=kappa_RM_dot,
        use_apparent_mass=use_apparent_mass,
    )

    return {
        "6a_23": paraglider6a_23,
        "6a_25": paraglider6a_25,
        "6a_27": paraglider6a_27,
        "6b_23": paraglider6b_23,
        "6b_25": paraglider6b_25,
        "6b_27": paraglider6b_27,
        "6c_23": paraglider6c_23,
        "6c_25": paraglider6c_25,
        "6c_27": paraglider6c_27,

        "9a_23": paraglider9a_23,
        "9a_25": paraglider9a_25,
        "9a_27": paraglider9a_27,
        "9b_23": paraglider9b_23,
        "9b_25": paraglider9b_25,
        "9b_27": paraglider9b_27,
        "9c_23": paraglider9c_23,
        "9c_25": paraglider9c_25,
        "9c_27": paraglider9c_27,
    }


def simulate(model, state0, dt, T):
    gsim.simulator.prettyprint_state(state0, "Initial state:", "")
    t_start = time.perf_counter()
    dt = 0.25  # Time step for the sequence of `states`
    times, states = gsim.simulator.simulate(model, state0, dt=dt, T=T)
    states_dot = gsim.simulator.recompute_derivatives(model, times, states)
    t_stop = time.perf_counter()
    print(f"\nTotal time: {t_stop - t_start:.2f}\n")
    gsim.simulator.prettyprint_state(states[-1], "Final state:", "")

    return times, states, states_dot


def plot_inputs(model, T):
    # FIXME: plot the v_W2e?
    # FIXME: hide the y-axis `0` on `delta_w` (fix the ylabel x-offset)
    fig, ax = plt.subplots(4, figsize=(8, 8), sharex=True)
    style = {"lw": 2.00, "c": "k"}
    t = np.arange(0, T + 0.1, 0.1)
    ax[0].plot(t, model.delta_a(t), **style)
    ax[1].plot(t, model.delta_bl(t), **style)
    ax[2].plot(t, model.delta_br(t), **style)
    ax[3].plot(t, model.delta_w(t), **style)
    ax[3].set_xlabel("time [sec]")
    ax[0].set_ylabel(r"$\delta_a$")
    ax[1].set_ylabel(r"$\delta_{bl}$")
    ax[2].set_ylabel(r"$\delta_{br}$")
    ax[3].set_ylabel(r"$\delta_w$")
    ax[0].set_ylim(-0.1, 1.1)
    ax[1].set_ylim(-0.1, 1.1)
    ax[2].set_ylim(-0.1, 1.1)
    ax[3].set_ylim(-1.1, 1.1)
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()
    ax[3].grid()
    fig.tight_layout()


def plot_xy(states, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    x, y, _ = states["r_RM2O"].T
    ax.plot(y, x, c="k", lw=1)
    ax.set_xlabel("y")
    ax.set_ylabel("x")
    ax.set_aspect("equal")
    return ax
