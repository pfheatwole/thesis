.. This chapter defines two things:

   1. *system dynamics* combine the component models into a system model

   2. *state dynamics* choose a set of state variables and define their
      dynamics in terms of the *system dynamics*

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
trajectory*: a record of how the state of the aircraft evolved over time. This
chapter develops several state dynamics models suitable for paraglider flight
simulation. It starts by combining the individual :doc:`component models
<paraglider_components>` into composite *system dynamics* models. Then, for
each system model, it chooses a set of state variables :math:`\vec{x}` and
defines the *state dynamics* :math:`\dot{\vec{x}} = f(\vec{x}, \vec{u})` in
terms of the *system dynamics*. [[The state dynamics provide the *transition
function* :eq:`state-transition` that was motivated in :ref:`introduction
<introduction:Model the data-generating process>`.]]

[[This project requires a flight simulator because it is fundamental to
solving the flight reconstruction problem. An :ref:`introductory section
<introduction:Solve the inverse problem>` of this paper defined *flight
reconstruction* as an *inverse problem*: given a recorded flight trajectory,
the goal is to determine the flight conditions that produced that trajectory.
It also explained that *flight simulation* provides a way to estimate
a statistical distribution over the possible answers: simulate many possible
flight conditions, compare each simulated trajectory to the recorded
trajectory, and combine them into an estimate of which scenarios are probable
and which are not.]] [[FIXME: remove references to flight reconstruction?]]


System dynamics
===============

In this paper, a *system dynamics* model is any set of derivatives that
captures all the relevant motion of an aircraft in response to some set of
conditions. They are treated separately from the `State dynamics`_ because
they are independent of the representation of *state*; for example, they do
not depend on the aircraft's absolute position or orientation, or how those
vectors are encoded.

.. Why does this section develop its own sytem model?

[[Despite the variety of existing models in literature, none were adequate for
flight reconstruction.]]

[[Because this paper is dedicated to developing system models capable of
enabling :ref:`introduction:Flight reconstruction`, it must satisfy the needs
of that application. The concrete requirements of any particular flight
reconstruction method will depend on the statistical filtering architecture,
but in anticipation of those needs the introductory chapter established
baseline target :ref:`introduction:Functionality`.]]


[[Some of the functionality was handled in the component models. Some of it
needs to be handled in the system models: degrees of freedom, apparent mass,
etc. **Do I really need to explicitly call back to Functionality here?**]]


.. Developing a system dynamics model

The previous chapters developed a set of :doc:`component models
<paraglider_components>` for a paraglider, each with their own inertial
properties and dynamics equations. The system dynamics are a composite model
that connect all of those component models.

The first step is to define the nature of those connections. The simplest (and
most common) basis for parafoils is to start with a *rigid body* assumption:
the canopy and suspension lines are treated as a single, pseudo-rigid
component. The only deformations allowed are the ones produced by the control
inputs (brakes and accelerator).


.. Terminology: "body" and "payload" aircraft coordinate systems

[[The models in this chapter use nonstandard terminology.]] The paraglider
community typically refers to the combination of canopy and lines as
a *paraglider wing*, but in this chapter the group of components that includes
the canopy will be referred to as the paraglider *body*. Despite its
ambiguity, the "body" convention improves consistency with existing
parafoil-payload literature (which in turn inherited the term from
conventional aeronautics literature). Some texts prefer the term *parafoil*,
but having the same prefix :math:`p` for both *parafoil* and *payload* makes
subscripting the variables unnecessarily difficult. Similarly, using "wing"
would be preferred in this context, but subscripting with :math:`w` causes
conflicts when discussing wind vectors.

In models where the payload orientation is fixed, there is only the body
coordinate system. In models that allow relative motion, there are two
coordinate systems: one for the body, and one for the payload. The body
coordinate system is designated with :math:`b`, and the payload coordinate
system (if used) is designated with :math:`p`.

For all models, the body coordinate systems in this chapter are inherited
directly from the *canopy* coordinate system defined in the
:doc:`foil_geometry` chapter: a *front-right-down* (frd) system whose origin
is at the leading edge of the canopy's central section, the :math:`x`-axis is
directed along the central chord, and the :math:`y`-axis normal to the section
towards the right.


Misc:

* The dynamics functions expect `g` and `v_W2e` to already be in canopy frd,
  so no explicit orientation is required (it doesn't force any particular
  representation). The state dynamics models are free to encode orientation
  however they want (Euler angles, quaternions, etc).


System inputs
-------------

The inputs :math:`\vec{u}` to the system model are the control inputs for each
component, the [[set of]] of wind velocities :math:`\vec{v}_{W/e}` for each
control point, and the gravity vector :math:`\vec{g}`.

.. math::
   :label: system inputs

   \vec{u} =
     \left\{
       \delta_a,
       \delta_{bl},
       \delta_{br},
       \delta_w,
       \vec{v}_{W/e},
       \vec{g},
     \right\}

Note that the deflection distances :math:`\delta_d(s)` used by the
:ref:`canopy model <paraglider_components:Canopy>` are computed internally by
the system model; they are not system inputs.

[[FIXME: should `v_W/e` be a matrix? It's an array of vectors, one for each
aerodynamic control point.]]


Reference point
---------------

Each dynamics model must choose a reference point about which the moments and
angular inertia are calculated. A common choice for conventional aircraft is
the center of real mass because it decouples the translational and angular
dynamics of isolated objects. For a paraglider, however, this is not possible:
paragliders are sensitive to apparent mass, which depends on the direction of
motion, so there is no "center" that decouples the translational and
rotational terms of the apparent inertia matrix. Because the system matrix
cannot be diagonalized there is no advantage in choosing the center of real
mass. Instead, the reference point can be chosen such that it simplifies other
calculations.

.. Note that the reference point for the dynamics can be different from the
   point for tracking the glider position

The :ref:`method <paraglider_components:Apparent mass>` to calculate the
apparent inertia matrix requires that the reference point lies in the
:math:`xz`-plane of the canopy. Two natural choices in that plane are the
leading edge of the central section, or the midpoint between the two risers.
The models in this paper use the :ref:`riser midpoint
<paraglider_components:Riser position>` :math:`RM` for all dynamics equations
because the body and payload can calculate its position in their own
coordinate systems without depending on the relative position or orientation
of the payload with respect to the body. (This choice simplifies the equations
for the :ref:`9-DoF model <derivations:Model 9a>` while maintaining
consistency with the :ref:`6-DoF model <derivations:Model 9a>`.)


Degrees-of-freedom
------------------

Arguably the most obvious differentiator between system models is how they
characterize the connection between the risers and the payload. Allowances for
relative rotation and translation between the body and payload are typically
referred to as the *degrees-of-freedom* (DoF) of the model. Models that do not
allow the payload to move relative to the body have 6-DoF: three
translational, and three rotational. Each dimension of relative translation or
rotation add an extra degree of freedom. Parafoil-payload literature provide
models from 6 to 10 degrees of freedom.


.. 6-DoF model

* In the 6-DoF models, the body and payload are connected as a single rigid
  body, with no relative motion between them.

* [[The canopy and suspension line models are already treated as rigid bodies
  (with the exception of canopy trailing edge deflections).]]

.. figure:: figures/paraglider/dynamics/paraglider_fbd_6dof.*
   :name: paraglider_fbd_6dof

   Diagram for a 6-DoF model.

* The :ref:`appendix <derivations:Paraglider Models>` includes several 6-DoF
  models. The most complete is :ref:`derivations:Model 6a` which accounts for
  the effects of apparent mass, while :ref:`derivations:Model 6b` and
  :ref:`derivations:Model 6c` have the advantage of simplicity.


[[ref: :eq:`model6a_complete_system`]]

The outputs of the 6-DoF dynamics model are two vector derivatives describing
the motion of the body relative to the earth frame :math:`\mathcal{F}_e` taken
with respect to the body frame :math:`\mathcal{F}_b`:

.. math::
   :label: model6a_system_derivatives

   \begin{aligned}
     {^b \dot{\vec{v}}_{RM/e}} \qquad & \textrm{translational acceleration of the riser midpoint} \, RM \\
     {^b \dot{\vec{\omega}}_{b/e}} \qquad & \textrm{angular acceleration of the body} \\
   \end{aligned}

[[Notice, the current values of the variables are the :math:`\vec{x}
= \left\{\vec{v}_{RM/e}, \vec{\omega}_{b/e} \right\}`]]


.. 9-DoF model

The 6-DoF models constrain the relative payload orientation to a fixed
position. This is reasonably accurate for average flight maneuvers, but it has
one significant failing: although the relative roll and twist are typically
[[negligible]], relative pitch about the riser connections is very common,
even during static glides. Friction at the riser carabiners [[and aerodynamic
drag]] dampen pitching oscillations, but the harness is free to pitch as
necessary to maintain equilibrium. Assuming a fixed pitch angle introduces
a nonexistent pitching moment that disturbs the equilibrium conditions of the
wing and artificially dampens the pitching dynamics during maneuvers.

To mitigate that issue, models with higher degrees of freedom break the system
into two components, a body and a payload, and permit relative orientations
between the two components. The body includes the lines, canopy, and enclosed
air. The payload includes the harness and pilot.

[[FIXME: **I argue that relative roll and pitch are unimportant, but then I go
and derivate a 9-DoF anyway?** Rework. I'm not using this model for much
anyway; maybe present it as a starting framework for implementing other
models?]]

[[Discuss the 7-, 8-, and 9-DoF models from literature?]]

This section develops a model with nine degrees of freedom: six for the
orientations of the body and payload, and three for the velocity of the
connection point shared by the body and payload. The body and payload are
modeled as two rigid bodies connected at the riser midpoint :math:`RM`, with
the connection modeled as a spring-damper system.

.. figure:: figures/paraglider/dynamics/paraglider_fbd_9dof.*
   :name: paraglider_fbd_9dof

   Diagram for a 9-DoF model with internal forces.

* The equations of motion are developed by solving for the translational
  momentum :math:`{^e \dot{\vec{p}}} = \sum{\vec{F}}` and angular momentum
  :math:`{^e \dot{\vec{h}}} = \sum \vec{M}` for both bodies. [[FIXME: who
  cares? Put this in the derivation.]]

* For the derivation of the mathematical model, see :ref:`derivations:Model
  9a`.

* [[The rotation coefficients should probably be modeled as a function of the
  harness chest strap width (ie, the riser separation distance), but this
  model is already rubbish anyway. Besides, I'm ignoring canopy deformations
  due to weight shift anyway.]]

* In addition to the derivatives provided by the 6-DoF models, the 9-DoF
  models add the angular acceleration of the payload

[[ref: :eq:`model9a_complete_system`]]

The outputs of the 9-DoF dynamics model are two vector derivatives taken with
respect to the body frame :math:`\mathcal{F}_b`, and one with respect to the
payload frame :math:`\mathcal{F}_p`:

.. math::
   :label: model9a_system_derivatives

   \begin{aligned}
     {^b \dot{\vec{v}}_{RM/e}} \qquad &\textrm{translational acceleration of the riser midpoint} \, RM \\
     {^b \dot{\vec{\omega}}_{b/e}} \qquad & \textrm{angular acceleration of the body} \\
     {^p \dot{\vec{\omega}}_{p/e}} \qquad & \textrm{angular acceleration of the payload} \\
   \end{aligned}


State dynamics
==============

.. Define the state dynamics and integrate them over time to generate flight
   trajectories

* Discuss the implementation of the simulator (the dynamics solver)

  * Inputs to the system (wind and control inputs)

  * Choice of state variables

  * Form of the differential equation (the model dynamics)

  * Method of integration


[[FIXME: where do I explain the tangent plane coordinate system?]]


Inputs
------

[[FIXME: explain how the simulator queries the wind and control inputs]]


State variables
---------------

.. Choose the state information (what we need to track) and how to encode it

The 6-DoF models record four vectors: the position and translational velocity
vectors of a reference point, and the orientation and angular velocity of the
body. The 9-DoF models include two additional vectors for the orientation and
angular velocity of the payload.


.. Position

To track the position of the glider, the state models must choose a reference
point. It does not have to be the same :ref:`reference point
<paraglider_systems:Reference point>` used to calculate the system dynamics,
but as it turns out, the riser midpoint :math:`RM` is also good choice for
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
coordinates of latitude, longitude, and altitude. However, global positioning
is unnecessary for these simulations, so to avoid the complexity involved with
angular coordinates, these state models use a *tangent-plane* approximation
that records position as a linear displacement from an arbitrary origin.

[[All units are in metric.]]

[[The wind field must be defined using the same tangent-plane coordinates.]]

[[Flight reconstruction can simply convert the flight track into a local
tangent-plane.]]


.. Orientation

For orientation, there are two common representations: *Euler angles* and
*quaternions*. Euler angles have the advantage of being easier to understand,
but they can experience an issue known as *Gimbal lock* which prevents their
use in situations where the aircraft rotates to extreme angles. Although the
limitations of the paraglider aerodynamics make it unlikely for the simulator
to create situations in which the glider is facing straight up or straight
down, the state models in this project chose quaternions for peace of mind and
a minor improvement in computational efficiency. [[My implementations use the
Hamilton convention (:cite:`sola2017QuaternionKinematicsErrorstate`,
Table:2).]]


.. Summary

The 6-DoF models record the trajectory of four vectors:

.. math::
   :label: model6a_state_variables

   \begin{aligned}
     {\vec{r}}_{RM/O} \qquad & \textrm{absolute position of the riser midpoint} \, RM \\
     {\vec{v}}_{RM/e} \qquad & \textrm{translational velocity of the riser midpoint} \, RM \\
     {\vec{q}}_{b/tp} \qquad & \textrm{orientation of the body to the tangent plane} \\
     {\vec{\omega}}_{b/e} \qquad & \textrm{angular velocity of the body} \\
   \end{aligned}


The 9-DoF models record two additional vectors for the payload:

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


State derivatives
-----------------

.. Define the derivatives of the state variables in terms of the current state
   and the system derivatives.

[[The state dynamics must combine the derivatives from the system dynamics
with the current state to compute the derivatives of the state variables.]]


.. Position

The derivatives calculated by the system dynamics models were taken in the
body and payload reference frames, :math:`\mathcal{F}_b` and
:math:`\mathcal{F}_p`, respectively. The simulator requires derivatives taken
with respect to the inertial frame :math:`\mathcal{F}_e` in order to integrate
the changes the paraglider position and orientation over time with respect to
the tangent plane. So, the state dynamics models must calculate the correct
derivatives as necessary. [[FIXME: verify this explanation]]

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

The time derivative of some quaternion :math:`\vec{q}` that is tracking the
orientation of an object relative to a reference frame can be calculated using
the object's angular velocity vector :math:`\vec{\omega} = \{ p, q, r \}` in
the coordinate system attached to that object (:math:`\vec{\omega}_{b/e}^b`
for the body, or :math:`\vec{\omega}_{p/e}^p` for the payload):

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
:eq:`model6a_state_variables` :

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


The complete set of state dynamics equation for the 9-DoF models in terms of
the system derivatives :eq:`model9a_system_derivatives` and state variables
:eq:`model9a_state_variables` :

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


Integration
-----------

.. Explain how to "solve" the differential equation given the state dynamics,
   initial state, and inputs

FIXME: necessary? Can't I just say "use Runge-Kutta"?


Discussion
==========

* [[Refer to `demonstration` for examples of different flight scenarios.]]

* This simulator assumes the wind and controls are available as a function of
  time. That's not the case for flight reconstruction, where you **push** the
  wind and control vectors at each timestep instead of letting the `dynamics`
  function **pull/query** them.

* [[Should I highlight that the dynamics implementations are stateless? Makes
  development easier, you can use a single instance for all the particles,
  etc. Should probably go in a discussion of the implementation itself.]]

* For the 9-DoF state dynamics, I'm pretty sure it would be preferable to
  track `omega_p2b` instead of `omega_p2e` (I suspect it would reduce
  accumulated integration error), but I forget why I didn't do that.

* If flight reconstruction is feasible, it is probably limited to "average"
  flight conditions, and under average flight conditions there is relatively
  insignificant relative motion of the harness, so a 6-DoF model is likely to
  be adequate.

