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

* Define *flight simulation* (for the purposes of this paper)

  For the purposes of this paper, a *flight simulator* is a computer program
  that uses a model of the flight dynamics to determine the state of the
  flight over a sequence of time. It 

* Why does this paper need a flight simulator?

  * To generate test flights for validation. At first this is only helpful for
    superficial checks (do flights "look" correct?), but will eventually be
    necessary for physical flight validation.

  * The filtering equation needs a transition function


.. Roadmap

This chapter proceeds as follows:

* Establish the functionality of the simulator [["requirements" seems
  unnecessary here: integrating the DE seems pretty clear-cut]]

* Discuss the implementation of the simulator (the dynamics solver)

  * Form of the differential equation (the model dynamics)

  * Inputs to the system (wind and control inputs)

  * Choice of state variables

  * Method of integration

* Provide examples of dynamic simulations, and compare to test cases if
  possible.

  * Simulated inputs (wind and controls)

  * Interesting scenarios


Implementation
==============

* Define the state variables, representations of orientation, etc

* Review `test_sim.py:Dynamics6a` and `test_sim.py:Dynamics9a` from
  `glidersim`. Provides the derivatives for use with scipy's RK4 integrator in
  `model.dynamics`. Each model chooses a set of state variables and call
  signature to `glider.accelerations`.

* Most of the state dynamics come directly from `glider.accelerations`, except
  for `q_b2e` (the orientation quaternion), which uses a formula from Stevens
  for the quaternion derivative based on `omega`.

* This simulator assumes the wind and controls are available as a function of
  time. That's not the case for flight reconstruction, where you **pass** the
  wind and control vectors at each timestep instead of letting the `dynamics`
  function **query** them.

* [[The dynamics functions expect `g` and `v_W2e` to already be in canopy frd,
  so no explicit angles are required (it doesn't force any particular
  representation). That choice is convenient since the simulator is free to
  use whatever orientation encoding it wants for storing the orientation state
  (Euler angles, quaternions, etc).]]

* [[Should I highlight that the dynamics implementations are stateless? Makes
  development easier, you can use a single instance for all the particles,
  etc. Should probably go in a discussion of the implementation itself.]]


Demonstrations
==============

* [[I need a wing for this, so I'll probably introduce my Hook3ish in
  `paraglider_dynamics:Case Study` (or whatever I call it). That section will
  provide the wing polars (*static*, steady-state analysis) and show some
  *dynamic* simulations here to further critique the model performance.]]


Input sequences
---------------

* Need to discuss my example, deterministic, wind and control functions
  (`LateralGust`, `linear_control`, etc), then show some example sequences and
  the resulting paraglider track.


Test cases
----------

* :cite:`slegers2003AspectsControlParafoil`: "roll steering" vs "skid
  steering"
