*****************
Flight Simulation
*****************

* Define *flight simulation* (for the purposes of this paper)

* Why does this paper need a flight simulator?

  * To generate test flights for validation. At first this is only helpful for
    superficial checks (do flights "look" correct?), but will eventually be
    necessary for physical flight validation.

  * The filtering equation needs a transition function

* Define the state variables, representations of orientation, etc

* Highlight that the dynamics so far are stateless. The dynamics take Euler
  angles as inputs, but the simulator is free to use whatever orientation
  encoding it wants for storing the orientation state (Euler angles,
  quaternions, etc).

* Show some examples, and compare to test cases if possible.


Test Cases
==========

* :cite:`slegers2003AspectsControlParafoil`: "roll steering" vs "skid
  steering"
