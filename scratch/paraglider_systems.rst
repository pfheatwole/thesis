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

* [[Although flight simulators are commonly expected to be interactive
  programs with graphical outputs, the simulator defined in this chapter is
  only concerned with the numerical outputs, and the input sequences are
  strictly non-interactive. However, in practice the dynamics model is fast
  enough that interactive simulations should be possible.]]

* [[This paper does not solve the flight reconstruction problem; it only uses
  the simulator to generate test flights for validation. At first this is only
  helpful for superficial checks (do flights "look" correct?), but will
  eventually be necessary for physical flight validation.]]

* This paper is specifically about paragliding wings, but in terms of the
  aerodynamics it is closely related to *parafoil-payload systems* (primarily
  of interest to the military and aerospace organizations) and *kites* (kite
  boarding, airborne wind energy systems, etc)

* This paper requires a flight simulator because the *filtering equation*
  requires a transition function. For the purposes of flight reconstruction,
  the *state dynamics model* :math:`\dot{x} = f(x, u)` is the dynamics model
  provided by the flight simulator.

* "A *tangent-plane coordinate system* is aligned as a geographic system but
  has its origin fixed at a point of interest on the spheroid; this coordinate
  system is used with the *flat-Earth equations of motion*." (Stevens, pg27)

* I'm treating the Earth frame `F_e` as an inertial frame

* I'm not using Steven's *flat-Earth equations of motion*. Those use Euler
  angles, assume a constant `J_b/RM`, etc.
