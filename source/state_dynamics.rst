.. This chapter chooses a set of state variables and defines the *state
   dynamics* in terms of the *system dynamics*.

   The state dynamics represent the :math:`\dot{x} = f(x, u)` alluded to in
   :doc:`introduction`. (Flight reconstruction motivated the need for
   :math:`\dot{x} = f(x, u)`, and the bulk of this paper has been building to
   this point where it provides that function.)


**************
State dynamics
**************

.. What is *state*? What are *state dynamics*?

The :doc:`system_dynamics` defined the instantaneous accelerations of the
aircraft in terms of local reference frames traveling with the aircraft. To
record the behavior of an aircraft over time, a set of variables must be chosen
to encode the *state* of the system relative to some global reference frame.
The *state dynamics* — time derivatives of the state variables — encode the
dynamic behavior of the aircraft in that global frame. A flight simulator
integrates the state dynamics to generate a *state trajectory*: a record of how
the state of the aircraft evolved over time.


.. Roadmap for the chapter

This chapter develops state dynamics models for the paraglider system models.
For each system model, it chooses a global coordinate system, defines a set of
*state variables* :math:`\vec{x}` in terms of that global coordinate system,
and defines the *state dynamics* :math:`\dot{\vec{x}}` in terms of the system
dynamics.



State variables
===============

.. A subtlety is that a state dynamics model may choose to involve a state
   derivative that is that is the same as a derivative calculated by the system
   model. For example, suppose the system dynamics choose to derive its
   equations of motion with respect to some point `R`; if the velocity of `R`
   is be chosen as a state variable, then the state derivative will be
   identical to the system derivative. However, it's not required that they are
   equal. For example, a different state model might choose to encode position
   using latitude and longitude, in which case they're different.


.. Position

To track the position of the glider, the state models must choose a reference
point in the glider's local coordinate system. It does not have to be the same
:ref:`reference point <system_dynamics:Reference point>` used to calculate the
system dynamics, but it turns out the riser midpoint :math:`RM` is also good
choice for tracking the glider position. Because the riser midpoint is close to
where a pilot would likely mount their flight recorder, it is likely to be
representative of the data in a flight track, which makes it the most
convenient point for comparing real flight data to simulated data. Another
advantage is that the riser midpoint is typically very close to the glider
center of mass, which makes the position data easier to understand when
developing the models.

Next, the state model must choose a coordinate system for the position. Most
GPS applications, including paraglider flight records (IGC files), encode
position using the WGS-84 *geodetic datum*, which uses the geocentric
coordinates of latitude, longitude, and altitude. However, positioning on the
global spheroid is overkill for these simulations, so to avoid the complexity
involved with angular coordinates the state models here use a *tangent-plane*
(:math:`tp`) approximation (:cite:`stevens2015AircraftControlSimulation`, p.
27) that records position as a linear displacement from an arbitrary origin.


.. Orientation

For orientation, there are two common representations: *Euler angles* and
*quaternions*. Euler angles have the advantage of being easier to understand,
but they can experience an issue known as *Gimbal lock* which prevents their
use in situations where the aircraft rotates to extreme angles. Although the
limitations of the paraglider aerodynamics make it unlikely for the simulator
to encounter situations in which the glider is facing straight up or straight
down, quaternions provide peace of mind and a minor improvement in
computational efficiency.

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


State derivatives
=================

.. Define the derivatives of the state variables in terms of the current state
   and the system derivatives.

Next, define the derivatives of the state variables in terms of the current
state and the system derivatives. The derivative of state variable for position
is straightforward since it uses the same reference point as dynamics. The only
modification is that the derivatives calculated by the system dynamics models
were taken in the body and payload reference frames, :math:`\mathcal{F}_b` and
:math:`\mathcal{F}_p`, but tracking the position and orientation of the
aircraft relative to the tangent plane requires derivatives taken with respect
to the inertial frame :math:`\mathcal{F}_e`. To provide the simulator with the
proper derivatives, the state dynamics models must use the *equation of
Coriolis* (:cite:`stevens2015AircraftControlSimulation`, Eq.
1.4-2) to calculate the derivative of velocity taken with respect to the
inertial frame:

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

For the orientation state variable, the time derivative of a quaternion
:math:`\vec{q}` that is tracking the orientation of an object can be calculated
using the object's angular velocity vector :math:`\vec{\omega} = \{ p, q, r \}`
in the coordinate system attached to that object (:math:`\vec{\omega}_{b/e}^b`
for the body, or :math:`\vec{\omega}_{p/e}^p` for the payload)
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
a standard 4th order `Runge-Kutta
<https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods>`__ method.


.. Tip to remember

   How are state dynamics different from system dynamics?

   At this point it can be easy to confuse the system and state dynamics. For
   example, they both offer variables such as translational velocity, so it's
   easy to forget why there is a distinction. The key thing to remember is that
   the system behavior is independent of the representation of state.

   Consider if the state variable for position was defined using latitude and
   longitude instead of linear distance. The system dynamics do not deal with
   angles; they deal with meters. That choice would clearly reveal why the
   state dynamics are separate from the system dynamics: the role of the state
   dynamics is to serve as the interface between the system dynamics and the
   flight simulator.
