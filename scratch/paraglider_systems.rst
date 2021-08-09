* This project requires a flight simulator because it is fundamental to
  solving the flight reconstruction problem. An :ref:`introductory section
  <introduction:Solve the inverse problem>` of this paper defined *flight
  reconstruction* as an *inverse problem*: given a recorded flight trajectory,
  the goal is to determine the flight conditions that produced that
  trajectory. It also explained that *flight simulation* provides a way to
  estimate a statistical distribution over the possible answers: simulate many
  possible flight conditions, compare each simulated trajectory to the
  recorded trajectory, and combine them into an estimate of which scenarios
  are probable and which are not. [[FIXME: remove references to flight
  reconstruction?

  The state dynamics provide the *transition function* :eq:`state-transition`
  that was motivated in :ref:`introduction <introduction:Model the
  data-generating process>`.

* Why did I need to develop my own system model?

  Despite the variety of existing models in literature, none were adequate for
  flight reconstruction. Why? To answer this I'd need to first setup the
  requirements for flight reconstruction, review existing models, then show
  why existing models fail to meet those requirements.

* My models violate conservation of momentum since they doesn't account for
  accelerations due to redistributions of mass (due weight shift and the
  accelerator). I think that to do that properly you'd need rates of motion
  relative to rates of control inputs, which I'm not interested in modeling.


Misc:

* The system inputs is the set of component inputs.

* Each component has its own inertial properties and dynamics equations.

* "Degrees-of-freedom" is a characterization of the connection between the
  wing and the canopy.

* Is the set of system inputs fully determined by the inputs of individual
  components? Are there any inputs that only work for the composite model? If
  not, I probably shouldn't have a section on `System inputs`. It's too short,
  and should get moved closer to where they're used.


* In models where the payload orientation is fixed, there is only the body
  coordinate system. In models that allow relative motion, there are two
  coordinate systems: one for the body, and one for the payload. The body
  coordinate system is designated with :math:`b`, and the payload coordinate
  system (if used) is designated with :math:`p`.

* For all models, the body coordinate systems in this chapter are inherited
  directly from the *canopy* coordinate system defined in the
  :doc:`foil_geometry` chapter: a *front-right-down* (frd) system whose origin
  is at the leading edge of the canopy's central section, the :math:`x`-axis
  is directed along the central chord, and the :math:`y`-axis normal to the
  section towards the right.

* For model 9a, the rotation coefficients should probably be modeled as
  a function of the harness chest strap width (ie, the riser separation
  distance), but that model is already rubbish anyway. Besides, I'm ignoring
  canopy deformations due to weight shift anyway.

* OUTLINE FREEWRITE:

  * This chapter defines *state dynamics* in terms of *system dynamics*

  * The system dynamics are a composite model using the component models.

  * Common setup for all models:

     * Review the list the basic components

     * Define the system inputs

     * Define *reference point*?

  * Characterize the connections between components

    * Define *body* and *payload* (this chapter uses non-standard terminology
      since "wing" has a different meaning in the paragliding community)

    * All models use a rigid body assumption the *body*

    * The connection between body and payload leads to "degrees of freedom"


System dynamics
===============

* This paper is specifically about paragliding wings, but in terms of the
  aerodynamics it is closely related to *parafoil-payload systems* (primarily
  of interest to the military and aerospace organizations) and *kites* (kite
  boarding, airborne wind energy systems, etc)

* Because this paper is dedicated to developing system models capable of
  enabling :ref:`introduction:Flight reconstruction`, it must satisfy the
  needs of that application. The concrete requirements of any particular
  flight reconstruction method will depend on the statistical filtering
  architecture, but in anticipation of those needs the introductory chapter
  established baseline target :ref:`introduction:Functionality`.

  Some of the functionality was handled in the component models. Some of it
  needs to be handled in the system models: degrees of freedom, apparent mass,
  etc. **Do I really need to explicitly call back to Functionality here?**]]


Existing models
---------------

Most existing parafoil-payload models focus on the *system dynamics*: the
dynamics of the final composite system.

This is a problem for me, because:

1. They model the aerodynamics with simplistic models

   Of course, I could have simply replaced that piece of a model with a better
   aerodynamics method. But that brings me to other issues:

2. They have different component models:

   * Instead of an accelerator they use canopy pitch angles

   * They don't incorporate apparent mass. Incorporating apparent mass
     requires a specific choice of reference point. (**But wait**: if they
     were using the system center of mass, wouldn't that have been in the
     xz-plane anyway? Probably. Hrm.)

   * Weight shift? I could swear one of them offered lateral payload control.

My system model is very similar to :cite:`slegers2003AspectsControlParafoil`.

That's okay, just don't overstate the amount of work I spent creating the
system model. Just acknowledge that Sleger's is close. My derivation uses my
notation though.

Why didn't I use his derivation?

1. The derivation skip steps, so it wasn't clear if it was correct.

2. The derivation was NOT correct, such as taking derivatives wrt `b` not `e`

3. The derivation mixed the real and apparent matrices, making it inconvenient
   to replace Lissaman's method with Barrows method. I tidied and reordered
   the matrices to dramatically simplify the system.

4. The derivation used implicit vector notation


State dynamics
==============

* I'm not using Steven's *flat-Earth equations of motion* (Eq:1.7-18, pg42).
  Those assume you're tracking orientation using Euler angles, assume
  a constant inertia matrix about the body center of mass, etc.

* "A *tangent-plane coordinate system* is aligned as a geographic system but
  has its origin fixed at a point of interest on the spheroid; this coordinate
  system is used with the *flat-Earth equations of motion*." (Stevens, pg27)


State derivatives:

* position, velocity, orientation, and angular velocity

* :eq:`model6a_state_variables`

* :eq:`model9a_state_variables`



Flight simulation
=================

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

* This paper requires a flight simulator because the *filtering equation*
  requires a transition function. For the purposes of flight reconstruction,
  the *state dynamics model* :math:`\dot{x} = f(x, u)` is integrated by the
  flight simulator to produce the *transition function* :math:`\vec{x}_{k+1}
  = f(\vec{x}_k, \vec{u}_k)`.

* I'm treating the Earth frame `F_e` as an inertial frame



FREEWRITE
=========

What does this chapter need to cover?

* What are system dynamics?

* What are state dynamics?

* Choice of state variables

* Coordinate systems

* Degrees-of-freedom


* Define *simulation*: calculating the state derivatives using the system
  dynamics, then integrate them numerically using a method like Runge-Kutta.
  We're interesting in keeping the intermediate states, so we step forward
  through the simulation in discrete time steps, and record the states at each
  timestep to produce a *state trajectory*.

* How do you provide the inputs to the simulation? I'm using hand-crafted
  control and wind vector "scenarios", but that's not essential to defining
  the simulator. I just need to explain the interface to the simulator, and
  say "these are the values it needs".


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

