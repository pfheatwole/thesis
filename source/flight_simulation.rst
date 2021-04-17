*****************
Flight Simulation
*****************

* What is *dynamic simulation*?

  From Wikipedia: "*Dynamic simulation* (or dynamic system simulation) is the
  use of a computer program to model the time-varying behavior of a dynamical
  system. The systems are typically described by ordinary differential
  equations or partial differential equations. A simulation run solves the
  state-equation system to find the behavior of the state variables over
  a specified period of time. The equation is solved through numerical
  integration methods to produce the transient behavior of the state
  variables. Simulation of dynamic systems predicts the values of model-system
  state variables, as they are determined the past state values. This
  relationship is found by creating a model of the system."

.. What is a flight simulator?

A flight simulator uses aircraft dynamics to record how a set of state
variables change over time in response to a sequence of control inputs and
wind vectors.

[[Although flight simulators are commonly expected to be interactive programs
with graphical outputs, the simulator defined in this chapter is only
concerned with the numerical outputs, and the input sequences are strictly
non-interactive. However, in practice the dynamics model is fast enough that
interactive simulations should be possible.]]


.. How does flight simulation relate to the problem of flight reconstruction?
   (ie, why does this paper need a flight simulator?)

[[This paper defines a flight simulator because the *filtering equation* needs
a transition function. For the purposes of flight reconstruction, the *state
dynamics model* :math:`\dot{x} = f(x, u)` is the dynamics model provided by
the flight simulator.]]

The introductory section of this paper, :ref:`introduction:Solve the inverse
problem`, defined *flight reconstruction* as an *inverse problem*: given
a recorded flight trajectory, we are interested in determining the flight
conditions that produced that trajectory. It also explained that *flight
simulation* provides a means to estimating a distribution that is likely to
contain the answer: by simulating many possible flight conditions, it is
possible to compare those possible outcomes against the actual outcome.

A paraglider dynamics model makes it possible to simulate and record the
motion of that paraglider in different flight scenarios.

The flight simulator is the link between the paraglider dynamics model and the
flight trajectories.

* [[This paper uses the simulator to generate test flights for validation. At
  first this is only helpful for superficial checks (do flights "look"
  correct?), but will eventually be necessary for physical flight
  validation.]]


.. Roadmap

This chapter proceeds as follows:

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


Implementation
==============

Inputs
------

FIXME


State variables
---------------

* [[Define the state variables, representations of orientation, etc]]

* [[The dynamics functions expect `g` and `v_W2e` to already be in canopy frd,
  so no explicit angles are required (it doesn't force any particular
  representation). That choice is convenient since the simulator is free to
  use whatever orientation encoding it wants for storing the orientation state
  (Euler angles, quaternions, etc).]]

  :cite:`sola2017QuaternionKinematicsErrorstate`


State dynamics
--------------

[[Need to relate the state dynamics to the paraglider model dynamics. Review
`Dynamics6a` and `Dynamics9a` from `glidersim`; they choose their own sets of
state variables and link their derivatives to the `glider.accelerations`.]]


Integration
-----------

[[ie, "solving" the differential equation, given the state dynamics, initial
state, and inputs]]


Example flight scenarios
========================

[[Should these go in "case study"? Each scenario needs a wing, so I'd either
have to move `demonstration` before this chapter or else forward reference it
here. I'm leaning towards making `demonstration` an end-to-end demonstration
from technical specs to geometry to aerodynamics to flight scenarios.]]


MISC
====

* This simulator assumes the wind and controls are available as a function of
  time. That's not the case for flight reconstruction, where you **pass** the
  wind and control vectors at each timestep instead of letting the `dynamics`
  function **query** them.

* [[Should I highlight that the dynamics implementations are stateless? Makes
  development easier, you can use a single instance for all the particles,
  etc. Should probably go in a discussion of the implementation itself.]]
