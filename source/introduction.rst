************
Introduction
************

Following the advice from `Exploration of Style
<https://explorationsofstyle.com/2013/02/20/structuring-a-thesis-introduction/>`_.


Intro to the Intro
==================

.. Establishing a research territory (Context):

* Paragliding is a recreational flying activity that uses a lightweight,
  flexible wing called a *paraglider*.

* Because a paraglider is a non-motorized aircraft, its motion is entirely
  dictated by gravity and wind. Paragliding pilots are totally dependent on
  the local air currents to achieve their flight goals.

* A lifting component to the wind counteracts the effect of gravity, allowing
  the pilot to slow their descent or even gain altitude; a sinking vertical
  component has the opposite effect. The horizontal component of the wind
  determines the direction and distance the glider can fly.

* A successful flight depends on the pilot's ability to recognize and navigate
  the current wind configuration in order to achieve their flight goals, which
  may include optimizing for flight time, distance, or a particular route.

* Because a glider is constantly exchanging potential energy to counteract
  gravity, the pilot must recognize the wind patterns as quickly as possible.
  One way to improve the odds of success is to learn from previous flights:
  although local wind configurations are difficult to predict, they can
  exhibit recurring patterns. By learning those patterns a pilot can assess
  the current wind conditions more quickly and with better odds of success,
  and can prioritize flying to areas that are likely to support their flight
  goals.


.. Establishing a niche (Problem and Significance):

* Traditionally, wind patterns are discovered by pilots with a large amount of
  flight time in a given area, and are shared directly from one pilot to
  another. For the pilot community to learn reliable patterns, individual
  pilots must first recognize them and then be able to communicate them with
  precision.

* An appealing alternative would be to aggregate recorded flight data from
  many pilots over many flights, detect the wind patterns automatically from
  those flights, and build a graphical map to communicate the features of the
  wind field visually instead of relying on verbal descriptions.

* In support of this idea, there already exist huge databases with millions of
  recorded flights spanning several decades. Pilots continue to record and
  share their flights for personal and competition purposes.

* The difficulty with this option is that common flight devices only record
  a tiny amount of the information available to a pilot: the average flight
  track can only be expected to include a time series of positions. There is
  typically no information regarding the orientation, velocity, acceleration,
  pilot control inputs (brakes, accelerator, etc), or the weather conditions.
  Even the details of the aircraft are unknown. The question then becomes
  whether there is enough information in position-only time series data to
  recover the wind vectors that were present during a flight.


.. Occupying the niche (Response):

* This thesis investigates the procedures necessary to produce a regression
  model over wind fields using position-only time series flight data for
  a paraglider. It contributes a parametric paraglider dynamics model for
  simulating paraglider flight tracks for a given wind field and pilot control
  sequence. It discusses how to use the dynamics model with simulation-based
  filtering methods to perform statistical flight reconstruction, and
  usability requirements for a flight track to be suitable for flight
  reconstruction. Lastly, it discusses the requirements for assembling
  a predictive model suitable for in-flight wind field estimation.


Context
=======

* Paragliding

  * Paragliding as a sport

  * The equipment: wing and harness

  * The dependency on the wind field. Discuss how pilots rely on wind (both
    vertical and horizontal).

  Paragliding is a non-motorized form of flight, which means it requires wind
  power for sustained flight. Pilots rely on their ability to find regions of
  rising air in order to gain altitude. They must also determine the direction
  and magnitude of the wind in order to determine what regions of the air they
  can access/explore, and to calculate suitable landing zones. [[ie, pilots
  are totally dependent on the local wind pattern]]


* Wind fields

  * Composites of different features (shear, updrafts, gusts)

  * Exhibit patterns that depend on the time of year, latitude, topography,
    etc.

  * [[Prioritize wind field information that is important to pilots. For
    example, house thermals, finding lift along a ridge, avoiding sink near
    a stream, etc.]]


* Pilots must learn to understand and predict the wind field

  * It is important for a pilot to determine the wind conditions as soon as
    possible. [[Elaborate why; pilots do this both pre-flight and
    mid-flight.]]

  * Exploring the wind field for information comes at a cost; exploration
    requires time, which costs energy (since the wing is always sinking).


* Knowing historical trends improve the accuracy of a pilot's estimates of the
  current conditions, and lets them make better predictions with less
  information. 


Restatement of the problem (and significance)
=============================================

[[Remember: **the problem is "learning the wind patterns, and why wind
patterns are important to pilots", not why the wind is important in
general**.]]


* How do pilots learn wind patterns?

   * Learning wind patterns by personal experience and word of mouth

   * Learning wind patterns from recorded flights


* What are the advantages of learning from recorded flights?

  * Automate pattern discovery [[Some trends may be subtle or infrequent.]]

  * Utilize all flights from all pilots instead of requiring multiple
    flights by the same pilot. [[If a pilot only encountered a particular
    wind configuration a single time, they wouldn't recognize it as part of
    a recurring pattern.]]

  * Expand the set of detectable patterns: a single flight can only
    observe a small portion of the wind field. By merging multiple flights
    that occurred at the same time, you can build a more comprehensive
    observation of the field. With larger observations there are more
    opportunities for detecting useful patterns.

  * A statistical predictive model can provide confidence levels: it can
    quantify the variance in its predictions, since it knows how much evidence
    is present for a particular pattern. [[How does this compare to
    word-of-mouth knowledge? Pilots can be deceived/biased about their
    experiences; memories are faulty.]]


* What flight data is available?

  * Position-only data

  * Approximate air density

  * [[It's important to discuss the available data *first* since it sets up
    the set of possible solutions.]]

* What are the difficulties of learning wind patterns from the available data?

  * No observations of the wind vectors, pilot inputs, or topography. No
    knowledge of wing parameters or sensor characteristics.

    [[Because the wing behavior relies on not only the wind vectors, but also
    on the wing dynamics, orientation, and pilot controls, this *inverse
    problem* must deal with a highly underdetermined system of equations.]]

* How do the difficulties affect the solution?

  * Because such an underdetermined system cannot be solved exactly, the
    objective is to compute the *distribution* over all possible solutions.

  * The fact that the solution involves a distribution over all possible
    solutions highlights the fact that the question is not "can I produce an
    estimate of the wind vectors?" to "can I produce a **useful** estimate of
    the wind vectors?"

    For example, if no information at all is given, a wind speed estimate of
    "between 0 and 150 mph" is likely to be correct, but it is not useful. If
    a pilot is told that a paraglider is currently flying, then with no
    further information they can still make reasonable assumptions about the
    maximum wind speed, since paragliding wings have relatively small
    operating ranges. If you told them the pilot's position at two points
    close in time, they can make an even better guess of the wind speed and
    a very rough guess about the wind direction. Intuitively, this is an
    "eliminate the impossible" approach: by assuming some reasonable limits on
    the wind speed and wing performance you can improve the precision of the
    estimate.

    The key frame of mind for this project is that the question is not "can
    you estimate the wind from position-only data?", but rather "how **how
    good** of an estimate of wind is possible from position-only data?" An
    estimate doesn't need to be especially precise in order to be useful to
    a pilot who is trying to understand the local wind patterns.


Restatement of the response
===========================

* The goal of estimating the wind vector using incomplete and noisy
  observations of the system is referred to as a *filtering problem*.

  [[This term comes from the field of *stochastic processes*, which is the
  study of processes that are partly predictable and partly random.]]

* Preparing observations from the raw flight data

  * The first step to using filtering methods is to establish exactly what
    information is available since this will determine the filter design.

  * The raw data is stored in IGC files, which must be parsed and sanitized.
    Parsing is straightforward, since the data follows a well-defined format.
    Sanitizing the data is more difficult: erratic timestamps, pressure
    altitude biases, and unknown sensor characteristics all present their own
    sets of concerns. Due to time constraints, data parsing and sanitization
    will not be handled in this thesis.

* Simulation-based filtering

  * Because the observations provide minimal information, the system is highly
    *underdetermined*; or, in the terminology of statistics, the wind vectors
    are not *identifiable*, which simply means that there are many different
    flight scenarios that could explain the observed data. The wind cannot be
    determined without knowledge the wing behavior and control inputs, which
    means that *simulation-based filtering* methods are required.

    [[What about PVA approaches that ignore the relative wind, such as Michael
    von Kaenel's thesis?]]

  * The essence of simulation-based methods is to explore the possible true
    state by utilizing a large set of guesses, called *proposals*. Each
    proposal is a possible value of the current state, and each proposal
    receives a score, called a *weight*, according to how well they explain
    the observations. Although there is no closed form probability
    distribution for these guesses, by making a large number of guesses you
    can arrive at an empirical probability distribution over solutions of the
    system state at each point in time. The precise state of the system is
    still unknown, but the set of possible solutions may be bounded enough to
    be useful.

* Parametric paraglider dynamics model

  * The great difficulty with model simulations is that they require equations
    that encode the model dynamics. Aerodynamics are non-trivial in even the
    most simple applications, and paragliders are particularly challenging
    aircraft to analyze due to their curvature and flexibility. In addition to
    the aerodynamics, the paraglider models themselves are uncertain, since
    the wing specifications are generally unknown for any given recorded
    flight; instead of a single, exactly-defined model, you need a parametric
    model that can be configured to match the unknown wing. Because the wing
    configuration is unknown, this estimation problem must be applied to not
    only the system state, but to the model parameters as well (also known as
    a *dual estimation problem*).

* Pilot controls and wind dynamics

  * Given a parametric paraglider model and a method for evaluating the
    aerodynamic forces that arise from a given set of wind conditions and
    control inputs, you can design a set of state dynamics equations for the
    total system. Those state dynamics are the basis of generating predictions
    as part of the particle filter time update step.


* Flight simulation

  * Given a complete set of dynamics (for the wing, pilot controls, and wind),
    you can generate simulated flight trajectories.

  * [[**Does this go before or after the dynamics model? The simulator
    establishes the need for the dynamics model.**]]

* Flight reconstruction

  * How simulation-based filtering deals with the underdetermined system

  * Running the particle filter over a specific flight produces a set of
    observations over points in the wind field at a specific time

* Wind field regression

  * Each flight is a set of observations. They need to be merged (if there are
    multiple overlapping flights) and used in a kriging process to build
    a regression model for the wind field at the time+place of the flight.

* Predictive model

  * Given a set of wind field regression models, needs to find regions with
    overlapping observations, then look for correlations in those co-observed
    regions.

  * Regional correlations must be encoded into a predictive model that can be
    queried (ie, if part of the wind field is (noisily) observed, and they
    have known correlations, the predictive model should produce estimates of
    unobserved regions)

  * Ultimately, this predictive model will be useable in-flight, so as the
    pilot samples the wind field, the predictive model can suggest regions
    with desirable wind patterns.


[[

So, given the wisdom of hindsight, what is the progression for solving this
problem?

1. Define a parametric paraglider model

#. Implement paraglider dynamics

#. Create test environments (wind conditions and control inputs)

#. Implement a paragliding flight simulator

#. Generate test flights using a known paraglider parameters

#. Define system-wide state transition equations for the GMSPPF

   These equations say how each state component is changing in time. The
   paraglider model uses the aerodynamics *given* the wind and control
   inputs.

#. Implement a UKF+GMSPPF framework

#. Use the GMSPPF to produce trajectory distributions for each of the test
   flights using the *known* paraglider model parameters

#. Expand the method to deal with *unknown* paraglider model parameters by
   embedding the GMSPFF (which use proposed model parameters) into a particle
   Metropolis-Hastings method or similar (use MCMC to propose model
   parameters, then use SMC to propose trajectories using those
   parameters)

]]


Contributions of my paper
=========================

[[FIXME: I'm not sure where this content goes]]

* Defining the problem (yes, this is a contribution! But I'd have to be
  thoughtful about how I'd word that; can't just pat myself on the back for
  coming up with an idea.)

  * Clearly developing and motivating the ultimate question, identifying the
    intermediate targets, the different forms of each targets (different
    models), the interdependencies of the targets, pros/cons of the different
    solutions, summarizing existing work and providing references, etc

* Code

  * Paraglider dynamics model

  * Reference wind models (for testing the model and generating test flights)

  * A simulator

  * IGC parsing code

  * Rudimentary GMSPPF?  (Stretch goal!!!)


* I'm implementing everything in Python. Explain why.

  * Approachable syntax

  * Free (unlike matlab)

  * Numerical libraries (numpy, scipy)

  * Large library ecosystem (s2sphere, sklearn, databases, PyMC3, pandas, etc)


My efforts are centered on sketching a possible path forward. This is the
problem I'd like to solve, these are the available resources, this is how
those resources might make a solution possible.


Roadmap
=======

[["Brief indication of how the thesis will proceed."]]
