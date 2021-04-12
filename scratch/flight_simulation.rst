* What is a *dynamic simulation*?

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

* What is required for flight simulation?

  A dynamics model, a suitable choice of state variables, and the time-series
  of inputs into that model.

  The choice of state variables determines the form of the *state dynamics
  model* :math:`\dot{x} = f(x, u)`.


* How do you choose the state variables? What makes a "good" choice?

  * The choice of state variables must be able to represent any state that can
    occur during a simulation.

  * They must make it possible (and preferably easy) to compare the simulated
    trajectory to an actual trajectory (so the state variables will ideally be
    the same variables as are provided in the flight records). (That's why
    I chose the riser midpoint to track the glider position; it's likely to
    agree with the location tracked by the pilot's GPS.)

  * It is preferable to keep the implementation details of the simulator (how
    input sequences are encoded, etc) separate from the dynamics models (that
    define the differential equations that depend on those inputs). For
    example, the aircraft dynamics should not care how the simulator is
    tracking its orientation.

  * For example, in this implementation the paraglider dynamics models are
    agnostic to orientation; they only consume the gravity vector `g`, and
    optionally a relative orientation between the payload and wing. The state
    variable for orientation can be Euler angles, quaternions, etc.
