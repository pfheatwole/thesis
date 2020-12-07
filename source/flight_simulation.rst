*****************
Flight Simulation
*****************

* Define *flight simulation* (for the purposes of this paper)

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


Demonstrations
==============

* [[What wing am I planning to use for the demonstrations? My Hook3 is the
  only fully specified wing. I should probably introduce that first, then use
  it to demonstrate the flight simulator and critique the model performance?


Input sequences
---------------

* Need to discuss my example, deterministic, wind and control functions
  (`LateralGust`, `linear_control`, etc), then show some example sequences and
  the resulting paraglider track.


Test cases
----------

* :cite:`slegers2003AspectsControlParafoil`: "roll steering" vs "skid
  steering"
