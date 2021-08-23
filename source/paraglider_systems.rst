.. This chapter defines two things:

   1. Combines component models into a composite *system dynamics* model

   2. Chooses a set of state variables and defines the *state dynamics* in
      terms of the *system dynamics*

   The state dynamics represent the :math:`\dot{x} = f(x, u)` alluded
   to in :doc:`introduction`. (Flight reconstruction motivated the need for
   :math:`\dot{x} = f(x, u)`, and the bulk of this paper has been building to
   this point where it provides that function.)


************************
Paraglider system models
************************

.. How does flight simulation relate to the problem of flight reconstruction?
   (ie, why does this paper need a flight simulator?)

A *flight simulator* uses an aircraft's *state dynamics* to generate a *state
trajectory*: a record of how the *state* (position, orientation, etc) of the
aircraft evolved over time. This chapter develops several state dynamics
models suitable for paraglider flight simulation. It starts by combining the
individual :doc:`component models <paraglider_components>` into composite
*system dynamics* models. Then, for each system model, it chooses a set of
*state variables* :math:`\vec{x}` and defines the *state dynamics*
:math:`\dot{\vec{x}}` in terms of the *system dynamics*.


System dynamics
===============

In this paper, a *system dynamics* model is a set of derivatives that define
the translational and angular acceleration of each group of physical
components on an aircraft. They are treated separately from the :ref:`state
dynamics <paraglider_systems:State dynamics>` because they are independent of
the representation of state.

.. For example, the system dynamics don't care if orientation is being tracked
   with Euler angles or quaternions.


.. Developing a system dynamics model

The *system dynamics* are composite models built from a set of :doc:`component
models <paraglider_components>`. Developing a system model can be roughly
described as a sequence of steps:

1. Choose a set of components to represent the aircraft

#. Characterize their connections

#. Choose a dynamics reference point for the composite system

#. Develop the system of equations for the accelerations


Components
----------

The previous chapter defined component models for the canopy, suspension
lines, and harness. To simplify the dynamics equations, the individual
components are lumped into two quasi-rigid body components called the *body*
and the *payload*. The *body* of the wing is the combination of canopy and
suspension lines. The *payload* includes the harness, pilot, and their gear;
in this simplified model, the pilot and their gear are treated as additional
masses that are added to the mass of the harness.

These models are quasi-rigid because the dynamics equations will only consider
their instantaneous configurations when calculating their accelerations;
conservation of momentum requires accounting for redistributions of mass, but
doing so would require inertia derivatives as functions of time derivatives of
the control input (such as weight shift, accelerator, etc), which would
significantly complicate the model. Because the redistributions of mass are
relatively small for typical scenarios, these models assume the affect of
violating conservation of momentum is negligible.


.. Terminology: "body" and "payload" aircraft coordinate systems

It is important to note that the unfortunately ambiguous terminology of *body*
is deliberate. The paraglider community typically refers to the combination of
canopy and lines as a *paraglider wing*, but the "body" convention improves
consistency with existing *parafoil-payload* literature (which in turn
inherited the term from conventional aeronautics literature). Some texts
prefer the term *parafoil*, but having the same prefix :math:`p` for both
*parafoil* and *payload* makes subscripting the variables unnecessarily
difficult. Similarly, using "wing" would be preferred in this context, but
subscripting with :math:`w` causes conflicts when discussing wind vectors.
Referring to whatever group of components include the canopy as the *body* was
a compromise chosen for consistency.


.. FIXME: summarize the inputs to each lumped component?


Connections
-----------

.. Model the connection between the "lumped" components (body and payload)

Next, the system model must characterize the connection between the body and
payload. In literature, parafoil-payload models are commonly categorized by
their *degrees-of-freedom* (DoF): the total number of dimensions in which the
components of the system are free to move. The body has 3-DoF for
translational motion and another 3-DoF for rotational motion, and if the
payload is allowed to move or rotate relative to the body, those additional
DoF are added to the total DoF of the system model. For example, in a 6-DoF
model, the body and payload are connected as a single rigid body, with no
relative motion between them.

.. FIXME: Parafoil-payload literature typically define models with 6 to 10
   degrees of freedom. Discuss models from literature?


.. figure:: figures/paraglider/dynamics/paraglider_fbd_6dof.*
   :name: paraglider_fbd_6dof

   Diagram for a 6-DoF model.


.. 9-DoF model

For typical paragliding flight maneuvers, assuming a fixed payload orientation
is reasonably accurate, but with one significant failing: although the
relative roll and twist are typically negligible, relative pitch about the
riser connections is very common, even during static glides. Friction at the
riser carabiners (and aerodynamic drag, to a lesser extent) dampen pitching
oscillations, but the payload is otherwise free to pitch as necessary to
maintain equilibrium. Assuming a fixed relative pitch angle introduces
a fictitious pitching moment that disturbs the equilibrium conditions of the
wing and artificially dampens the pitching dynamics during maneuvers. To
mitigate that issue, the obvious solution is to add an additional DoF, but for
demonstration purposes it is simpler to define a full 9-DoF model, where the
body and payload are connected at the :ref:`riser midpoint
<paraglider_components:Accelerator>` :math:`RM`. The connection is modeled as
a spring-damper system, which produces an internal force :math:`\vec{F}_R` and
moment :math:`\vec{M}_R`:

.. FIXME: should be `f_RM` and `m_RM` or similar

.. figure:: figures/paraglider/dynamics/paraglider_fbd_9dof.*
   :name: paraglider_fbd_9dof

   Diagram for a 9-DoF model with internal forces.


Reference point
---------------

Each dynamics model must choose a reference point about which the moments and
angular inertia are calculated. A common choice for conventional aircraft is
the center of real mass because it decouples the translational and angular
dynamics of isolated objects. For a paraglider, however, this is not possible:
paragliders are sensitive to apparent mass, which depends on the direction of
motion, so there is no "center" that decouples the translational and
rotational terms of the apparent inertia matrix
:cite:`barrows2002ApparentMassParafoils`. Because the system matrix cannot be
diagonalized there is no advantage in choosing the center of real mass.
Instead, the reference point can be chosen such that it simplifies other
calculations.

.. Note that the reference point for the dynamics can be different from the
   point for tracking the glider position

In particular, the :ref:`method <paraglider_components:Apparent mass>` to
estimate the apparent inertia matrix requires that the reference point lies in
the :math:`xz`-plane of the canopy. Two natural choices in that plane are the
leading edge of the central section, or the midpoint between the two risers.
The :ref:`riser midpoint <paraglider_systems:Connections>` :math:`RM` has the
advantage that is a fixed point in both the body and payload coordinate
systems, which means it does not depend on the relative position or
orientation of the payload with respect to the body. (This choice simplifies
the equations for the :ref:`9-DoF model <derivations:Model 9a>` while
maintaining consistency with the :ref:`6-DoF model <derivations:Model 9a>`.)

.. 6a and 9a use `RM`, but the others don't


Equations of motion
-------------------

The equations of motion are developed by solving for the derivatives of
translational momentum :math:`{^e \dot{\vec{p}}} = \sum{\vec{F}}
= m \dot{\vec{v}}` and angular momentum :math:`{^e \dot{\vec{h}}} = \sum
\vec{M} = \mat{J} \dot{\vec{\omega}}` for each group of components
:cite:`hughes2004SpacecraftAttitudeDynamics`. In addition to requiring the
forces, moments, and inertia matrices for each component, each system model
must choose a dynamics reference point and whether to account for the affects
of *apparent mass*. The :ref:`appendix <derivations:Paraglider Models>`
includes derivations demonstrating different choices for several each model.


.. 6-DoF model

For the 6-DoF model, the most complete is :ref:`derivations:Model 6a` which
accounts for the effects of apparent mass, while :ref:`derivations:Model 6b`
and :ref:`derivations:Model 6c` have the advantage of simplicity (making them
easier to implement and useful for validating implementations of more complex
models). The derivation produces a system of equations
:eq:`model6a_complete_system` that can be solved for the two vector
derivatives that describe the accelerations of the body relative to the earth
frame :math:`\mathcal{F}_e` taken with respect to the body frame
:math:`\mathcal{F}_b`:

.. math::
   :label: model6a_system_derivatives

   \begin{aligned}
     {^b \dot{\vec{v}}_{RM/e}} \qquad & \textrm{translational acceleration of the riser midpoint} \, RM \\
     {^b \dot{\vec{\omega}}_{b/e}} \qquad & \textrm{angular acceleration of the body} \\
   \end{aligned}

.. [[Notice, the current values of the variables are the :math:`\vec{x}
   = \left\{\vec{v}_{RM/e}, \vec{\omega}_{b/e} \right\}`]]


.. 9-DoF

Similarly, for the 9-DoF model, :ref:`derivations:Model 9a` also develops
a complete system of equations :eq:`model9a_complete_system` that account for
apparent mass of the canopy, but with the addition of a separate angular
acceleration for the payload with respect to the payload frame
:math:`\mathcal{F}_p`:

.. math::
   :label: model9a_system_derivatives

   \begin{aligned}
     {^b \dot{\vec{v}}_{RM/e}} \qquad &\textrm{translational acceleration of the riser midpoint} \, RM \\
     {^b \dot{\vec{\omega}}_{b/e}} \qquad & \textrm{angular acceleration of the body} \\
     {^p \dot{\vec{\omega}}_{p/e}} \qquad & \textrm{angular acceleration of the payload} \\
   \end{aligned}


State dynamics
==============

The system dynamics defined the acceleration of the aircraft in terms of local
reference frames traveling with the aircraft. To track the global position and
orientation of the aircraft during a flight, its *state* must be measured
relative to some global reference frame. The *state dynamics* define the
acceleration of the aircraft in that global frame, and are defined in terms of
the system dynamics. The exact relationship depends on the choice of state
variables, so implementing a flight simulator given a system dynamics model
involves several steps:


.. Define the state dynamics and integrate them over time to generate flight
   trajectories

1. Choose a suitable set of state variables (including a global coordinate
   system)

2. Transform inputs from the global coordinate system into the embedded
   coordinate system

3. Define the state derivatives in terms of the system derivatives


State variables
---------------

.. Position

To track the position of the glider, the state models must choose a reference
point on the glider. It does not have to be the same :ref:`reference point
<paraglider_systems:Reference point>` used to calculate the system dynamics,
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
   (:cite:`sola2017QuaternionKinematicsErrorstate`, Table:2).


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
----------------

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
-----------------

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
Coriolis* to calculate the state derivatives in the inertial frame:

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
the coordinate system attached to that object (:math:`\vec{\omega}_{b/e}^b`
for the body, or :math:`\vec{\omega}_{p/e}^p` for the payload) (:cite:`stevens2015AircraftControlSimulation`, Eq:1.8-15):

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
