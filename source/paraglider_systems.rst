.. This chapter defines two things:

   1. *system dynamics* combine the component models into a system model

   2. *state dynamics* choose a set of state variables and define their
      dynamics in terms of the *system dynamics*

   The state dynamics represent the :math:`\dot{x} = f(x, u)` alluded
   to in :doc:`introduction`. (Flight reconstruction motivated the need for
   :math:`\dot{x} = f(x, u)`, and the bulk of this paper has been building to
   this point where it provides that function.)

* [[This chapter combines the component models from
  :doc:`paraglider_components` to create a dynamics model of the complete
  paraglider system.]]

* [[Although flight simulators are commonly expected to be interactive
  programs with graphical outputs, the simulator defined in this chapter is
  only concerned with the numerical outputs, and the input sequences are
  strictly non-interactive. However, in practice the dynamics model is fast
  enough that interactive simulations should be possible.]]

* [[This paper does not solve the flight reconstruction problem; it only uses
  the simulator to generate test flights for validation. At first this is only
  helpful for superficial checks (do flights "look" correct?), but will
  eventually be necessary for physical flight validation.]]


************************
Paraglider system models
************************

.. What are dynamics? What are paraglider dynamics used for?

A *dynamics model* describes how a set of variables change over time.
A *flight simulator* uses aircraft dynamics to generate a *flight trajectory*:
a sequence that records how the state of the aircraft evolves over time in
response to a sequence of control inputs and wind vectors.

.. How does flight simulation relate to the problem of flight reconstruction?
   (ie, why does this paper need a flight simulator?)

This paper requires a flight simulator because it is fundamental to solving
the flight reconstruction problem. The introductory section of this paper,
:ref:`introduction:Solve the inverse problem`, defined *flight reconstruction*
as an *inverse problem*: given a recorded flight trajectory, we are interested
in determining the flight conditions that produced that trajectory. It also
explained that *flight simulation* provides a means to estimating
a distribution that is likely to contain the answer: by simulating many
possible flight conditions, it is possible to compare those simulated
trajectories outcomes against the recorded trajectory.


[[This chapter needs to start by defining several *system dynamics* models for
the composite paraglider system, using all of its component models. Then, it
needs to choose sets of state variables and define the *state dynamics* in
terms of the *system dynamics*.]]

[[This paper requires a flight simulator because the *filtering equation*
requires a transition function. For the purposes of flight reconstruction, the
*state dynamics model* :math:`\dot{x} = f(x, u)` is the dynamics model
provided by the flight simulator.]]



.. Roadmap

This chapter proceeds as follows:

* Discuss existing paraglider models from literature?

* Composite system dynamics

  [[Degrees-of-freedom, connection model, etc?]]


* Establish the functionality of the simulator [["requirements" seems
  unnecessary here: integrating the DE seems pretty clear-cut]]

* Discuss the implementation of the simulator (the dynamics solver)

  * Inputs to the system (wind and control inputs)

  * Choice of state variables

  * Form of the differential equation (the model dynamics)

  * Method of integration

* Provide examples of dynamic simulations, and compare to test cases if
  possible.

  * Simulated inputs (wind and controls)

  * Interesting scenarios



System dynamics
===============

.. These provide the system dynamics needed to define the state dynamics

[[Models of the composite system]]


Reference point
---------------

One of the first steps in developing an aircraft dynamics model is to choose
a reference point for the translational dynamics. A common choice is the
system center of mass because it decouples the translational and angular
dynamics. For paragliders, however, the center of mass is not a fixed point
because it is not a strictly rigid body system: weight shift, accelerator, and
atmospheric air density all effect the location of the paraglider center of
mass. Also, paragliders are sensitive to apparent mass, which don't have
a single "center"; that is, there is no point that minimizes all of the terms
in the apparent inertia matrix, and there is no point that decouples the
translational and rotational terms of the apparent inertia matrix. Because the
system matrix cannot be diagonalized there is no advantage in choosing the
center of mass. Instead, the reference point can be chosen such that it
simplifies other calculations.

.. Note that the point you use for computing the dynamics can be different
   from the point you use for tracking the glider trajectory over the Earth.

As mentioned in :ref:`paraglider_components:Apparent mass`, estimating the
apparent mass of the canopy is simplified if the reference point lies in the
xz-plane of the wing. The most natural choices in that plane are the leading
edge of the central section, or the midpoint between the two risers
connections, which is constant regardless of the width the riser chest strap.

This paper chooses the midpoint between the two riser connections, designated
:math:`RM`, for all dynamics equations because it is also the most natural
choice for the vehicle velocity state variable in the simulator. The reason is
that because the riser midpoint is likely to be near to where a pilot would
place their flight device, it is also the most representative of the data
measured by flight recorders, making it the most convenient point for
comparing real flight data to simulated data.

Another advantage is that the riser midpoint is typically very close to the
glider center of mass, which makes it easy to visualize the glider motion when
developing the models.


Control inputs
--------------

[[FIXME: should these have been specified earlier when I was defining the
component models? Or do the component models forward reference this section?]]


A six degrees-of-freedom model
------------------------------

In these models, the paraglider is approximated as a single rigid body.
With all the components held in a fixed position, the dynamics can be
described by solving the system of equations produced by equating the
derivatives of translational and angular momentum to the sum of forces and
moments on the rigid body.

[[FIXME: the six and nine DoF introductions should have parallel structure.
Write one of them, then adapt it for the other so they develop in the same
way.]]

.. figure:: figures/paraglider/dynamics/paraglider_fbd_6dof.*
   :name: paraglider_fbd_6dof

   Diagram for a 6-DoF model.

For the derivation of the mathematical model, see :ref:`derivations:Model 6a`.


A nine degrees-of-freedom model
-------------------------------

The 6-DoF models constrain the relative payload orientation to a fixed
position. This is reasonably accurate for average flight maneuvers, but it has
one significant failing: although the relative roll and twist are typically
[[negligible]], relative pitch about the riser connections is very common.
Friction at the riser carabiners adds a damping effect to pitching
oscillations, but in general the harness is free to pitch as necessary to
maintain equilibrium. Assuming a fixed pitch angle introduces a incorrect
pitching moment that disturbs the equilibrium conditions of the wing and
artificially dampens the pitching dynamics during maneuvers.

To mitigate that issue, models with higher degrees of freedom break the system
into two components, a body and a payload, and permit relative orientations
between the two components. The body includes the lines, canopy, and enclosed
air. The payload includes the harness and pilot.

[[Discuss the 7-, 8-, and 9-DoF models from literature?]]

This section develops a model with nine degrees of freedom: six for the
orientations of the body and payload, and three for the velocity of the
connection point shared by the body and payload. The body and payload are
modeled as two rigid bodies connected at the riser midpoint :math:`RM`, with
the connection modeled as a spring-damper system.

.. figure:: figures/paraglider/dynamics/paraglider_fbd_9dof.*
   :name: paraglider_fbd_9dof

   Diagram for a 9-DoF model with internal forces.

The equations of motion are developed by solving for the translational
momentum :math:`^e \dot{\vec{p}} = \sum{\vec{F}}` and angular momentum
:math:`^e \dot{\vec{h}} = \sum \vec{M}` for both bodies.

For the derivation of the mathematical model, see :ref:`derivations:Model 9a`.


State dynamics
==============

.. Define the state dynamics and integrate them over time to generate flight
   trajectories


State variables
---------------

* [[Define the state variables, representations of orientation, etc]]

* [[The dynamics functions expect `g` and `v_W2e` to already be in canopy frd,
  so no explicit angles are required (it doesn't force any particular
  representation). That choice is convenient since the simulator is free to
  use whatever orientation encoding it wants for storing the orientation state
  (Euler angles, quaternions, etc).]]

  :cite:`sola2017QuaternionKinematicsErrorstate`


State derivatives
-----------------

[[Need to relate the state dynamics to the paraglider model dynamics. Review
`Dynamics6a` and `Dynamics9a` from `glidersim`; they choose their own sets of
state variables and link their derivatives to the `glider.accelerations`.]]


Integration
-----------

[[ie, "solving" the differential equation, given the state dynamics, initial
state, and inputs]]


Discussion
==========

* [[Refer to `demonstration` for examples of different flight scenarios.]]

* This simulator assumes the wind and controls are available as a function of
  time. That's not the case for flight reconstruction, where you **pass** the
  wind and control vectors at each timestep instead of letting the `dynamics`
  function **query** them.

* [[Should I highlight that the dynamics implementations are stateless? Makes
  development easier, you can use a single instance for all the particles,
  etc. Should probably go in a discussion of the implementation itself.]]
