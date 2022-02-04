.. This chapter chooses a set of state variables and defines the *state
   dynamics* in terms of the *system dynamics*.

   The state dynamics represent the :math:`\dot{x} = f(x, u)` alluded to in
   :doc:`introduction`. (Flight reconstruction motivated the need for
   :math:`\dot{x} = f(x, u)`, and the bulk of this paper has been building to
   this point where it provides that function.)


**************
State dynamics
**************

A *flight simulator* uses an aircraft's *state dynamics* to generate a *state
trajectory*: a record of how the *state* (position, orientation, etc) of the
aircraft evolved over time.

This chapter develops several state dynamics models suitable for paraglider
flight simulation. For each system model, it chooses a set of *state variables*
:math:`\vec{x}` and defines the *state dynamics* :math:`\dot{\vec{x}}` in terms
of the *system dynamics*.


The system dynamics defined the acceleration of the aircraft in terms of local
reference frames traveling with the aircraft. To track the global position and
orientation of the aircraft during a flight, its *state* must be recorded
relative to some global reference frame. The *state dynamics* define the
acceleration of the aircraft in that global frame, and are defined in terms of
the system dynamics. The exact relationship depends on the choice of state
variables, so implementing a flight simulator given a system dynamics model
involves several steps:


.. Define the state dynamics and integrate them over time to generate flight
   trajectories

1. Transform inputs from the global coordinate system into the local coordinate
   system

2. Choose a suitable set of state variables (including a global coordinate
   system)

3. Define the state derivatives in terms of the system derivatives


[[stuff this chapter should touch on:

* coordinate systems, reference frames
* equations of motion
* state variables, state derivatives

Elaborate that the choice of variables is one of the ways that the state
dynamics model provides the interface between the system dynamics and the
flight simulator.]]


State variables
===============

.. Position

To track the position of the glider, the state models must choose a reference
point on the glider. It does not have to be the same :ref:`reference point
<system_dynamics:Reference point>` used to calculate the system dynamics,
but it turns out the riser midpoint :math:`RM` is also good choice for
tracking the glider position. Because the riser midpoint is close to where
a pilot would likely mount their flight recorder, it is likely to be
representative of the data in a flight track, which makes it the most
convenient point for comparing real flight data to simulated data. Another
advantage is that the riser midpoint is typically very close to the glider
center of mass, which makes it easy to visualize the glider motion when
developing the models.

Next, the state model must choose a coordinate system for the position.
Typical of most GPS applications, paraglider flight records (IGC files) encode
position using the WGS-84 *geodetic datum*, which uses the geocentric
coordinates of latitude, longitude, and altitude. However, positioning on the
global spheroid is unnecessary for these simulations, so to avoid the
complexity involved with angular coordinates the state models here use
a *tangent-plane* approximation that records position as a linear displacement
from an arbitrary origin.


.. Orientation

For orientation, there are two common representations: *Euler angles* and
*quaternions*. Euler angles have the advantage of being easier to understand,
but they can experience an issue known as *Gimbal lock* which prevents their
use in situations where the aircraft rotates to extreme angles. Although the
limitations of the paraglider aerodynamics make it unlikely for the simulator
to create situations in which the glider is facing straight up or straight
down, the state models in this project chose quaternions for peace of mind and
a minor improvement in computational efficiency.

.. My implementations use the Hamilton convention
   (:cite:`sola2017QuaternionKinematicsErrorstate`, Tab:2).


.. Sets of state variables for each model

Given these choices, the state variables of the 6-DoF models are four vectors:

.. math::
   :label: model6a_state_variables

   \begin{aligned}
     {\vec{r}}_{RM/O} \qquad & \textrm{absolute position of the riser midpoint} \, RM \\
     {\vec{v}}_{RM/e} \qquad & \textrm{translational velocity of the riser midpoint} \, RM \\
     {\vec{q}}_{b/tp} \qquad & \textrm{orientation of the body to the tangent plane} \\
     {\vec{\omega}}_{b/e} \qquad & \textrm{angular velocity of the body} \\
   \end{aligned}


Similarly, the 9-DoF models use the same four vectors, plus an additional
quaternion and angular acceleration vector for the payload:

.. math::
   :label: model9a_state_variables

   \begin{aligned}
     {\vec{r}}_{RM/O} \qquad & \textrm{absolute position of the riser midpoint} \, RM \\
     {\vec{v}}_{RM/e} \qquad & \textrm{translational velocity of the riser midpoint} \, RM \\
     {\vec{q}}_{b/tp} \qquad & \textrm{orientation of the body to the tangent plane} \\
     {\vec{q}}_{p/tp} \qquad & \textrm{orientation of the payload to the tangent plane} \\
     {\vec{\omega}}_{b/e} \qquad & \textrm{angular velocity of the body} \\
     {\vec{\omega}}_{p/e} \qquad & \textrm{angular velocity of the payload} \\
   \end{aligned}


Simulator inputs
================

.. FIXME: explain how the simulator queries the wind and control inputs

The state dynamics model must pass whatever inputs are required by the system
dynamics model. The inputs :math:`\vec{u}` to the system model are the control
inputs for each component, the wind velocity :math:`\vec{v}_{W/e}`, and the
gravity vector :math:`\vec{g}`.

.. math::
   :label: system inputs

   \vec{u} =
     \left\{
       \delta_a,
       \delta_{bl},
       \delta_{br},
       \delta_w,
       \vec{v}_{W/e}^b,
       \vec{g}^b,
     \right\}

Here the wind field is assumed to be uniform so the wind velocity at every
control point is defined by a single, constant vector, but for non-uniform
wind fields there will be a unique wind vector for each aerodynamic control
point. Also, note that the deflection distances :math:`\delta_d(s)` used by
the :ref:`canopy model <paraglider_components:Canopy>` are computed internally
by the system model; they are not system inputs.


.. FIXME: discussion:

   * `v_W/e` could be written as a matrix (an array of vectors)

   * These are functions of time, not standalone/"instantaneous" variables.

   * All inputs to the simulator are defined in `tp` coordinates.

   * I've decided to have the state dynamics models transform all the vectors
     into body coordinates so the system models don't have to. For the 9-DoF,
     I'm passing `Theta_p2b` to allow transforming the wind vectors for the
     payload control points into payload coordinates; they need `C_p2b`
     anyway, so that's not a big deal, and passing them as Euler angles allows
     them to be used for the restoring moments.]]


State derivatives
=================

.. Define the derivatives of the state variables in terms of the current state
   and the system derivatives.

A flight simulator generates a state trajectory by integrating the state
derivatives over time. Although the state derivatives are functions of the
system derivatives (and the current state), the two must not be conflated; the
system dynamics do provide a set of derivatives that describe the motion of
the aircraft, but they are not necessarily equal to the state derivatives. For
example, the state variable for position may track a different reference point
than was used for calculating the system dynamics, the derivatives may be
taken with respect to a different reference frame, etc.

.. Position: in this case we ARE using the same reference point.

.. Reference frame

For example, the derivatives calculated by the system dynamics models were
taken in the body and payload reference frames, :math:`\mathcal{F}_b` and
:math:`\mathcal{F}_p`, but tracking the position and orientation of the
aircraft relative to the tangent plane requires derivatives taken with respect
to the inertial frame :math:`\mathcal{F}_e`. To provide the simulator with the
proper derivatives, the state dynamics models must use the *equation of
Coriolis* [[FIXME: add reference to Stevens]] to calculate the state
derivatives taken with respect to the inertial frame:

.. math::

   \begin{aligned}
     {^e \dot{\vec{v}}_{RM/e}^{tp}} &=
       \mat{C}_{tp/b} \cdot \left(
         {^b \dot{\vec{v}}_{RM/e}^b}
         + \vec{\omega}_{b/e}^b \times \vec{v}_{RM/e}^b
       \right)
     \\
     {^e \dot{\vec{\omega}}_{b/e}^b} &= {^b \dot{\vec{\omega}}_{b/e}^b}
     \\
     {^e \dot{\vec{\omega}}_{p/e}^p} &= {^p \dot{\vec{\omega}}_{p/e}^p}
   \end{aligned}


.. Orientation

Also, the state derivatives require an additional equation to define the
quaternion derivatives in terms of the angular velocity state variables. The
time derivative of some quaternion :math:`\vec{q}` that is tracking the
orientation of an object relative to a reference frame can be calculated using
the object's angular velocity vector :math:`\vec{\omega} = \{ p, q, r \}` in
the coordinate system attached to that object (:math:`\vec{\omega}_{b/e}^b` for
the body, or :math:`\vec{\omega}_{p/e}^p` for the payload)
(:cite:`stevens2015AircraftControlSimulation`, Eq. 1.8-15):

.. math::

   \mat{\Omega} \defas
     \begin{bmatrix}
       0 & -p & -q & -r \\
       p & 0 & r & -q \\
       q & -r & 0 & p \\
       r & q & -p & 0
     \end{bmatrix}

.. math::

   \dot{\vec{q}} = \frac{1}{2} \mat{\Omega} \cdot \vec{q}


The complete set of state dynamics equation for the 6-DoF models in terms of
the system derivatives :eq:`model6a_system_derivatives` and state variables
:eq:`model6a_state_variables` are then:

.. math::
   :label: 6dof_state_dynamics

   \begin{aligned}
     {^e \dot{\vec{r}}_{RM/O}^{tp}} &= {\vec{v}_{RM/e}^{tp}}
     \\
     {^e \dot{\vec{v}}_{RM/e}^{tp}} &=
       \mat{C}_{tp/b} \cdot \left(
         {^b \dot{\vec{v}}_{RM/e}^b} + \vec{\omega}_{b/e}^b \times {\vec{v}_{RM/e}^b}
       \right)
     \\
     {^e \dot{\vec{q}}_{b/tp}} &= \frac{1}{2} \mat{\Omega}_{b/tp} \cdot \vec{q}_{b/tp}
     \\
     {^e \dot{\vec{\omega}}_{b/e}^b} &= {^b \dot{\vec{\omega}}_{b/e}}
   \end{aligned}


Similarly, the complete set of state dynamics equation for the 9-DoF models in
terms of the system derivatives :eq:`model9a_system_derivatives` and state
variables :eq:`model9a_state_variables`:

.. math::
   :label: 9dof_state_dynamics

   \begin{aligned}
     {^e \dot{\vec{r}}_{RM/O}^{tp}} &= {\vec{v}_{RM/e}^{tp}}
     \\
     {^e \dot{\vec{v}}_{RM/e}^{tp}} &=
       \mat{C}_{tp/b} \cdot \left(
         {^b \dot{\vec{v}}_{RM/e}^b} + \vec{\omega}_{b/e}^b \times {\vec{v}_{RM/e}^b}
       \right)
     \\
     {^e \dot{\vec{q}}_{b/tp}} &= \frac{1}{2} \mat{\Omega}_{b/tp} \cdot \vec{q}_{b/tp}
     \\
     {^e \dot{\vec{q}}_{p/tp}} &= \frac{1}{2} \mat{\Omega}_{p/tp} \cdot \vec{q}_{p/tp}
     \\
     {^e \dot{\vec{\omega}}_{b/e}^b} &= {^b \dot{\vec{\omega}}_{b/e}^b}
     \\
     {^e \dot{\vec{\omega}}_{p/e}^p} &= {^p \dot{\vec{\omega}}_{p/e}^p}
   \end{aligned}


.. Explain how to "solve" the differential equation given the state dynamics,
   initial state, and inputs

The state dynamics models in :eq:`6dof_state_dynamics` and
:eq:`9dof_state_dynamics` are ready to be used with a suitable numerical
integration method to generate the state trajectories. Due to the significant
nonlinear behavior of the dynamics, the implementation for this project uses
a standard 4th order Runge-Kutta method.
