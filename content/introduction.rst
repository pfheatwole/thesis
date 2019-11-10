************
Introduction
************

Introduction to the paper
=========================

Following the advice from `Exploration of Style
<https://explorationsofstyle.com/2013/02/20/structuring-a-thesis-introduction/>`_.


Intro to the Intro
------------------

.. Establishing a research territory (Context):

* A paraglider is a non-motorized aircraft, which means paragliding pilots are
  totally dependent on the local wind field.

* [[Discuss basic wind features before discussing their importance/impact?]]

* The vertical wind component is essential for sustained flight, while the
  horizontal wind components determine the direction and distance the glider
  can fly.

* The success of a flight depends on the pilot's ability to recognize the
  current wind configuration so that they can choose a flight path that allows
  them to achieve their flight goals. [[Because a gliding aircraft is
  constantly descending relative to the local air, it is vital that a pilot
  can locate regions of rising air as soon as possible.]]

* Although local wind configurations are difficult to predict, they do exhibit
  recurring patterns. By learning those patterns , a pilot can assess the
  current wind conditions more quickly [[than they would without prior
  knowledge of the patterns]].


.. Establishing a niche (Problem and Significance):

* Traditionally, wind patterns are discovered by pilots with a large amount of
  flight time in a given area, and are shared directly from one pilot to
  another. For the pilot community to learn reliable patterns, individual
  pilots must first detect them and then be able to communicate them with
  precision.

* An alternative [[to pilots manually detecting and communicating the
  patterns]] could be to aggregate recorded flight data from many pilots over
  many flights, learn the wind patterns from those flights, then build
  a graphical map to visually communicate the features of the wind field.

* The difficulty with this option is that GPS devices only record a tiny
  amount of the information available to a pilot: there is typically no
  information regarding the orientation, velocity, acceleration, pilot control
  inputs (brakes, accelerator, etc), or the weather conditions. Even the
  details of the aircraft performance are unknown. The question then becomes
  whether there is enough information in position-only data to recover the
  wind vectors present during a flight.


.. Occupying the niche (Response):

* This thesis investigates the procedures necessary to produce a regression
  model over wind fields using position-only paraglider flight data. It
  contributes a parametric paraglider dynamics model for simulating paraglider
  flight tracks for a given wind field and pilot control sequence. It
  discusses how to use the dynamics model with simulation-based filtering
  methods to perform statistical flight reconstruction. Lastly, it discusses
  the requirements for assembling a predictive model suitable for in-flight
  wind field estimation. [[FIXME: review these topics, liable to change]]


Context
-------

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
---------------------------------------------

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
---------------------------

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
-------------------------

[[FIXME: I'm not sure where this content goes]]

* Defining the problem (yes, this is a contribution! But I'd have to be
  thoughtful about how I'd word that; can't just pat myself on the back for
  coming up with an idea.)

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
-------

[["Brief indication of how the thesis will proceed."]]


Flight Data
===========

What are my data? These are the raw measurements for the Bayesian model, which
is to say: these are the only observed random variables.

* Discuss the raw data available in IGC tracks


Data sanitation
---------------

Key Points:

* In order to perform flight reconstruction on actual flights, you need to
  parse, clean, and transform the IGC data into the format required by the
  dynamics model.

* The output from this stage is the only parts of the flight that were
  observed; everything else must be simulated. The extreme limitations of this
  data establishes the constraints for the flight reconstruction stage.


* The fact that older tracks were inaccurate shouldn't mean we can't prepare
  for the continuing collection of new tracks! Newer GPS devices are getting
  very accurate; why not start designing for them?


Example tasks:

* Sanitize the timestamps

* Check the GPS noise model (Chi^2 test)

* Debias the variometer data (via dynamic time warping or similar)

* Estimate atmospheric conditions (air density in particular)


Probabilistic Methods
=====================

This entire project is a set of questions with the general form: "what is the
value of this thing given the value of that other thing?" That is, these
questions involve relationships between variables, where dependent variables
take on values conditional on the values of the independent variables. And,
since there is uncertainty in all the variables, it doesn't make sense to ask
for for specific numbers, but the distributions that cover the plausible
values.

We need to transform these questions into mathematical equivalents in order to
find the answers. The mathematical framework for reasoning through conditional
probability is the realm of *Bayesian statistics*. This section provides
a Bayesian formulation of the goals of this project.


The Bayesian Formulation
------------------------

Before we can look for recurring patterns in the wind fields, we need to
estimate the individual wind fields from each flight. We want to know
:math:`\vec{w}_{1:T}`, but we only have :math:`\vec{p}_{1:T}`, so our first
step is to learn :math:`p(\vec{w}_{1:T} \mid \vec{p}_{1:T})`. To do that we
need a relationship between the sequence of flight positions and the wind
vectors. That relationship is given by the paraglider aerodynamics model
:math:`f({\cdot\,} ; M)`, which is parametrized by the wing model :math:`M`.

If we knew :math:`M`, we might try to target :math:`p(\vec{w}_{1:T} \mid
\vec{p}_{1:T}, M)`, but the aerodynamics model also requires the pilot inputs
:math:`\vec{\delta}_{1:T}`, so we are forced to target :math:`p(\vec{w}_{1:T}
\mid \vec{p}_{1:T}, \vec{\delta}_{1:T}, M)`. The problem is that we still have
no function that can describe this distribution in closed-form. Because there
is no analytical solution that we can solve directly, we are forced to use
Monte Carlo methods, which approximate the target by generating samples from
this intractable distribution. It is important to note that we also don't know
the true :math:`\vec{\delta}` or :math:`M`, so we need to generate
a representative set of samples for those as well.

The ultimate goal is to generate representative sets of samples for each of
the unknowns, input those samples into aerodynamic functions of the wing to
explore the set of possible flights, called *trajectories*, then score (or
*weight*) each possible flight based on how plausibly it could have created
the observed flight path. That set of weighted trajectories is the Monte Carlo
approximation of that intractable target, :math:`p(\vec{w}_{1:T} \mid
\vec{p}_{1:T}, \vec{\delta}_{1:T}, M)`.

.. math::

   p(\vec{w}_{1:T} \mid \vec{p}_{1:T}, \vec{\delta}_{1:T}, M) = \frac{ p(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M)}{p(\vec{p}_{1:T}, \vec{\delta}_{1:T}, M)} \
                                                              = \frac{ p\left(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M\right)}{\int p\left(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right) \mathrm{d} \vec{w}_{1:T}}

.. ::

   An alternative, two-line version of the above

   .. math::

      p(\vec{w}_{1:T} \mid \vec{p}_{1:T}, \vec{\delta}_{1:T}, M) &= \frac{ p(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M)}{p(\vec{p}_{1:T}, \vec{\delta}_{1:T}, M)} \\
                                                                 &= \frac{ p\left(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M\right)}{\int p\left(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right) \mathrm{d} \vec{w}_{1:T}}


Computing the target requires knowing the joint probability
:math:`p(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M)`, which is
unknown. Instead, we will use the chain rule of probability to rewrite the
joint distribution as the product of several conditional distributions which
we can estimate.

.. math::

   p(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M) = p(\vec{p}_{1:T} \mid \vec{w}_{1:T}, \vec{\delta}_{1:T}, M) p(\vec{w}_{1:T}, \vec{\delta}_{1:T}, M)


Or, using ``\left`` and ``\right``:

.. math::

   p\left(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M\right) = p\left(\vec{p}_{1:T} \mid \vec{w}_{1:T}, \vec{\delta}_{1:T}, M\right) p\left(\vec{w}_{1:T}, \vec{\delta}_{1:T}, M\right)


We can use SMC and MCMC methods to produce samples from the joint
distribution, then average over the wind components of each particle to
estimate our ultimate target: the distribution over the wind vectors
present during the flight.


Extra Notes
===========

* Is it correct to say that the control inputs and the wind vectors are
  marginally *independent* (in the absence of the pose), but conditionally
  dependent given the pose of the wing? A gut check says yes: if you asked
  me to guess a pilot controls in the blind, I'd have to be vague, but if you
  told me they were banking to the right with a gust coming from the left,
  I'd be much more inclined to believe they were applying right brakes (and
  in the middle of a turn).

  It might help to draw the model graph for the two scenarios. Wind doesn't
  *directly* influence the controls, it does it *indirectly*, through the
  pilot's objective/strategy. The pilot's decision making process takes in
  the wind, post, and objective, and produces the control output as a
  response, but if you delete that strategy from the model graph then
  there isn't a dependency between the wind and controls; they're only
  related by their common effect: the trajectory.

  This question probably belongs together with the discussion on *maneuvering
  target tracking*.
