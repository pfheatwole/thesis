************
Introduction
************

The goal of this chapter should establish:

1. The problem: learn wind patterns from recorded flights

2. The value: feedback helps pilot enjoy better flights

3. The difficulty: not enough good data

4. The approach: simulate flights and weight them

5. The focus: building a dynamics model for the particle filter

6. The outcomes: a fully parametric paraglider model


Structure of this Introduction
==============================

Following the advice from `Exploration of Style
<https://explorationsofstyle.com/2013/02/20/structuring-a-thesis-introduction/>`_.


Intro to the Intro
------------------

.. Establishing a research territory (Context):

* Paragliding is a recreational flying activity that uses a lightweight,
  flexible wing called a *paraglider*.

* Because a paraglider is a non-motorized aircraft, its motion is entirely
  dictated by interactions with gravity and wind. Paragliding pilots are
  totally dependent on the local air currents to achieve their flight goals.

* The aerodynamic forces on the wing are the product of the relative velocity
  between the wing and the air. If the air is ascending it allows the pilot to
  slow their descent, or even gain altitude; conversely, sinking air will
  cause the wing to descend more quickly. The horizontal component of the wind
  determines the direction and distance the glider can fly.

* A successful flight depends on the pilot's ability to recognize the
  structure of the local air currents and navigate them in order to achieve
  their flight goals, which may include optimizing for flight time, distance,
  or a particular route.

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
  flight time in a particular area, and are shared directly from one pilot to
  another. For the pilot community to learn reliable patterns, individual
  pilots must first recognize them and then be able to communicate them with
  precision.

* An appealing alternative would be to aggregate recorded flight data from
  many pilots over many flights, detect the wind patterns automatically from
  those flights, and build a graphical map to communicate the features of the
  wind field visually instead of relying on verbal descriptions.

* In support of this idea, there already exist large databases with millions
  of recorded flights spanning several decades. These databases continue to
  grow as pilots record and share their flights for personal and competition
  purposes.

* The difficulty with this option is that common flight devices only record
  a tiny amount of the information available to a pilot: the average flight
  record can only be expected to include a time series of positions. There is
  typically no information regarding the orientation, velocity, acceleration,
  pilot control inputs (brakes, accelerator, etc), or the weather conditions.
  Even the details of the aircraft are unknown. The question then becomes
  whether there is enough information in position-only time series data to
  recover the wind vectors that were present during a flight.


.. Occupying the niche (Response):

* This thesis investigates the procedures necessary to produce a regression
  model over wind fields using position-only time series flight data for
  a paraglider. Its primary contribution is a parametric paraglider dynamics
  model for simulating paraglider flight tracks for a given wind field and
  pilot control sequence. It discusses how the dynamics model enables
  simulation-based filtering methods to perform statistical flight
  reconstruction, and the requirements for a flight recording to be suitable
  for flight reconstruction. Lastly, it discusses the requirements for
  assembling a predictive model suitable for in-flight wind field estimation.


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
-------

[["Brief indication of how the thesis will proceed."]]


Task Overview
=============

I'd like to develop a motivational roadmap for flight reconstruction: what is
it, why would it be useful, and what's involved in performing it? This section
should decompose the big picture task of "turning flight data into
a predictive model suitable for in-flight feedback" into a collection of
subtasks.


1. What is flight reconstruction?

   * Reconstructing the wind for an individual flight

2. Why do it?

   What are the applications? Make a list of related literature of tasks that
   would benefit from solving the problem of paraglider flight reconstruction.

  * Wind estimation

  * Path planning algorithms (strategies to help pilots utilize the predictive
    model while accounting for the predictive uncertainty)

3. What would be required for reconstructing individual flights?

  * Probabilistic simulation that needs dynamics models for all the
    components, priors for all the variables, etc

4. What would be required for the applications of flight reconstruction?

  * Building regression models from individual flights

  * Aggregating/merging regression models from combined flights (flights at
    the same location at the same time)

  * Aggregating regression models over multiple days to build a predictive
    model

  * Pattern detection/extraction (finding reliable patterns in the set of
    regression models)

  * Encoding the patterns into a predictive model


**Which aspects of these tasks are the focus of my paper?** I'm focused on
building components for probabilistic flight simulation.

**Note to self**: I like this idea of laying out a roadmap then highlighting
how each chapter of my paper fits into that roadmap


The goal is to estimate the local wind field that was present during
a paragliding flight, but the only data we have is measurements of the
paraglider position. To use this data, we need a relationship between the
paraglider movement and the wind. The mathematical description of how
a paraglider's movement changes with the wind is given by the set of
differential equations that define the glider dynamics. Thus, in addition to
the position data, we also need knowledge of its dynamics.

However, the dynamics depend on more than just the wind. They also depend on
the paraglider wing design, the harness, the weight of the pilot, the control
inputs from the pilot, and the current atmospheric conditions. So in order to
use the dynamics equations, we need to choose values for these other unknowns
variables.


Related topics for discussion:

* Flight reconstruction as a *state estimation* problem. State estimation
  might mean improving an estimate of an observed quantity, or it could mean
  producing an original estimate of an unobserved quantity.

* Performing *parameter estimation* implies that you have a parametric model
  in the first place.

* In most aerodynamic literature, when they talk about *parameter estimation*
  they typically have access to the aircraft in question and can execute
  a specific set of maneuvers to learn the behavior of the system. I have no
  access to the wing, no knowledge of the control inputs, and the maneuvers are
  assumed unsteady (not the result of the control inputs alone).

* Priors over the control inputs, wing parameters, and atmospheric conditions

* Managing uncertainty using *Bayesian filtering* methods


Some comments:

* Flight path reconstruction

  * The term *flight path reconstruction* seems to have a particular meaning
    in some portions of the aerospace community, where it is used to indicate
    kinematics-based state estimation as a component in model validation and
    calibration. (For a good survey on this topic, see
    :cite:`mulder1999NonlinearAircraftFlight`.) As a kinematics-based method,
    the models are built around *specific forces* and angular rates instead of
    aerodynamic forces and moments. As such, it is more concerned with
    **what** an aircraft will do, now and moments **why**.

    In my project, the **why** is the most important aspect. I can't use
    kinematics-only filtering because it neglects the very thing I'm
    interested in: why the wing moves a particular way (ie, it depends on the
    wind).

  * I'm calling my efforts in this paper "flight reconstruction" because it's
    not just the path of the wing I'm interested in.


I'd like to decompose this project into a collection of subtasks, then discuss
related work in the context of those subtasks:

* Paraglider model identification (finding a suitable dynamics model)

* State estimation (estimating the states of all components, including the
  wing, control inputs, and wind)

* Parameter estimation (the parameters of the dynamics model)

* Input estimation (control inputs and wind vectors)

* Spatial regression (for the wind field), etc.

* Wind field modelling (*model-free* proposals vs *model-based* proposals)

* The fundamental idea of this project is to augment a tiny amount of flight
  data with a large amount of system knowledge. Related to this idea is
  *model-free* vs *model-based* methods: if you have information about the
  target, use it. This project has many components, and each component needs
  a model; conceptually you can start with *model-free* methods for everything
  and replace them with *model-based* ones. (I'm not sure if kinematics-only
  models would fall under model-free or not...)

  From :cite:`li2003SurveyManeuveringTarget`: "a good *model-based* tracking
  algorithm will greatly outperform any *model-free* tracking algorithm if the
  underlying model turns out to be a good one". (See also
  :cite:`li2005SurveyManeuveringTarget` for more discussion of this notion?)


* An interesting paper for flight planning with environmental estimates is
  :cite:`menezes2018EvaluationStochasticModeldependent`. Might have some
  useful overlap for how I frame the tasks of this paper.

* I need to rethink the name of my paper. I'm not actually **performing**
  flight reconstruction, I'm just talking about it / building towards it.
  I may also discuss topics like flight planning concepts, which I may add
  after I publish the original paper. Maybe the name of the paper should be
  more general, since my discussions are more general, plus it'd make it more
  natural to extend the content later on.


Brief technical development
===========================

[[This section is as much for myself as anything. I would like to start with
the kernel of the idea and iteratively refine the details, expanding the
question complexity while converting the details into mathematical form. The
goal is to walk the reader through the development of the idea and how the
math motivates the design path.]]


The long-term objective of this project is to learn wind patterns from
recorded flights, but the more fundamental problem is how to estimate the wind
field from an individual flight. Each step of the process follows the same
formula: how can we use relationships to things we know to estimate
something we don't know? This section develops these questions by rewriting
them in mathematical terms, letting the needs of the math guide the process.

To begin, our initial problem statement is to "estimate the wind field present
during a paraglider flight". In mathematical form, we want to know the value
of the wind field:

.. math::

   \mathcal{W}

Because precise knowledge is impossible, we must be content with an estimate.
To quantify the inherent uncertainty in our estimate we must invoke the
language of probability, so our new objective is to "estimate the probability
distribution over the wind field:

.. math::

   p \left( \mathcal{W} \right)

The next task is to develop relationships between what we know and what we
want. At the beginning, the only thing we know is the sequence of the
paraglider's position over time. To put this into mathematical terms, we start
by defining the time as :math:`t` and the paraglider position as
:math:`\vec{r}`. Because the flight is recorded as a sequence of position over
time, this means everything we know is encoded in :math:`\vec{r}(t)`.

However, because the position was recorded using a GPS device it will be
subject to sensor noise. To account for the sensor noise we need the language
of probability to formalize the uncertainty. To simplify the notation, start
by defining :math:`\vec{r}_t \defas \vec{r}(t)`. The mathematical form of what
we know is then given by the probability distribution over the position is
then :math:`p(\vec{r}_t)`.

Given these new terms, our original objective can be defined as "estimate the
wind field given a sequence of positions from a paraglider flight".
Mathematically, our objective has now become:

.. math::

   p\left(\mathcal{W}\right) =
      \int_{\vec{r}_t}
         p \left( \mathcal{W} \given \vec{r}_t \right)
         p \left( \vec{r}_t \right)
         \mathrm{d}\vec{r}_t

Because there is no direct relationship between the global wind field and the
positions over time, we must decompose the problem definition into
intermediate steps. For instance, although the ultimate objective is to
estimate the entire wind field, our relationship between the wind and the
paraglider position comes in the form of the paraglider aerodynamics, which
only depend on the instantaneous wind velocities :math:`\vec{w}_t`. This
expanded goal is then:

.. math::

   p \left( \mathcal{W} \given \vec{w}_t, \vec{r}_t \right)
      p \left( \vec{w}_t \given \vec{r}_t \right)
      p \left( \vec{r}_t \right)


Some progress can be made by expanding the term :math:`p \left( \vec{w}_t
\given \vec{r}_t \right)`. We know that the position of the paraglider depends
on the wind velocity. An application of Bayes formula produces:

.. math::

   p \left( \vec{w}_t \given \vec{r}_t \right) =
      \frac
         {p \left( \vec{r}_t \given \vec{w}_t \right) p \left( \vec{w}_t \right)}
         {p \left( \vec{r}_t \right)}


Using the terms to rewrite our objective:

.. math::

   p \left( \mathcal{W} \given \vec{w}_t, \vec{r}_t \right)
      p \left( \vec{r}_t \given \vec{w}_t \right)
      p \left( \vec{w}_t \right)


Note that the relationship given by :math:`p \left( \vec{r}_t \given \vec{w}_t
\right)` is ultimately one of the model dynamics. Unfortunately we don't have
any explicit relationship between the position of a paraglider given the wind
field; we do, however, anticipate having a dynamics model that describes the
relationship between a paraglider's movement and the wind if we also know the
paraglider model :math:`\mathcal{M}` and the pilot control inputs
:math:`\vec{u}_t`. By the rules of probability we expand:

.. math::

   p \left( \vec{r}_t \given \vec{w}_t \right) =
      p \left( \vec{r}_t \given \vec{w}_t, \vec{u}_t, \mathcal{M} \right)
      p \left( \vec{u}_t, \mathcal{M} \right)



Paragliding
===========

.. figure:: figures/paraglider/paraglider_diagram.*
   :name: paraglider_diagram
   :width: 50%

   A Paraglider. I hate this diagram.


Wind Fields
===========

[[Describe the things I'm trying to find.]]


Managing Uncertainty
====================

Flight reconstruction must deal with many sources of uncertainty: the input
data, the dynamics, the control inputs, and the atmospheric data are either
imprecise or entirely unknown. Reconstruction accuracy demands careful
management and quantification of that uncertainty. We need to manage and
quantify our uncertainty.

A single point estimate cannot communicate any information regarding the
possible error.

*Bayesian statistics* is a philosophical framework that interprets statements
of *probability* as statements of ignorance. It uses the rules of probability
to relate uncertain quantities and to quantify the "state of ignorance" of the
result.

Bayesian filtering requires knowledge of the model, which means we need
a dynamics model for the system: the paraglider wing, the pilot inputs, and
the wind.


Predictive Modeling
===================

[[On a track-by-track basis, I'm trying to estimate, or "learn", the wind
velocity field as a function of position. But more than that, I am proposing
that the wind field has regular patterns that depend on the time of day, day
of the year, and weather conditions. Conceivably there is a useable set of
wind field models that capture recurring elements. If you know the historical
patterns then if you can figure out the likely current configurations then you
should be able to predict the unobserved parts of the wind field.]]

You want to use observations to predict the current state. (Not sure "predict"
is the right word here though; it's more like "estimation", except that
estimation in statistics means "estimating the true value of the observed
thing", whereas I'm trying to estimate the value of the **unobserved** thing.)

* Given a model, you would like to predict the value you would observe at
  other points in the wind field.

* Static models that simply summarize historical averages or rates aren't
  useless, but they are pretty boring; for example, in Michael von Kaenel's
  thesis the conclusion was simply "stay along the ridge", which pilots
  already know.

  Instead, we want a probabilistic model that gives answers that have been
  **conditioned** on some *set of observations* :math:`\mathcal{O}
  = \left\{x\right\}`. But there are multiple levels to this: a simple kriging
  model can use just the current observations to try and build a regression
  model over the current state, but conceptually the trained model is
  essentially using the historical data as "pseudo-observations". You're not
  just conditioning the answer based on current observations, but on the
  historical observations as well. Mathematically, we say that the historical
  data is encoded in a *model* :math:`\mathcal{M}`, so the distribution
  becomes :math:`\vec{x} \sim p \left(\vec{x} \given \mathcal{O}, \mathcal{M}
  \right)`.

  This distinction is obvious to data science practitioners, but it's probably
  helpful to make the idea explicit for the less mathematically inclined
  reader.


Flight Reconstruction
=====================

[[What is flight reconstruction? How does it related to wind field
estimation?]]


Related Works
=============

* Wind estimation

  * Offline wind estimation / Learning from flight databases

    * :cite:`ultsch2010DataMiningDistinguish`

    * :cite:`vonkanel2010ParaglidingNetSensorNetwork`

  * Online wind estimation

    * :cite:`vonkanel2011IkarusLargescaleParticipatory`

    * :cite:`wirz2011RealtimeDetectionRecommendation`

* Wind estimation

  * :cite:`kampoon2014WindFieldEstimation`

* State estimation

  * :cite:`mulder1999NonlinearAircraftFlight`

* Applications of a predictive wind model

  * Flight reconstruction

    * Malaysian Airlines Flight 370, "Bayesian Methods in the search for
      MH370" (:cite:`davey2016BayesianMethodsSearch`)

    * Flight reconstruction of a tethered glider:
      :cite:`borobia2018FlightPathReconstructionFlight` (is this actually
      flight **path** reconstruction?)

  * Path planning during a flight

    * :cite:`lawrance2011PathPlanningAutonomous`

    * :cite:`lawrance2011AutonomousExplorationWind`

    * :cite:`lawrance2009WindEnergyBased`

  * Input estimation

    * :cite:`kampoon2014WindFieldEstimation`
