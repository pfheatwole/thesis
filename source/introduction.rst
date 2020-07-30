************
Introduction
************

Structure taken from `Exploration of Style
<https://explorationsofstyle.com/2013/02/20/structuring-a-thesis-introduction/>`_.


This chapter should establish:

1. The problem: learn wind patterns from recorded flights

2. The value: feedback helps pilot enjoy better flights

3. The difficulty: not enough good data

4. The approach: simulate flights and weight them

5. The focus: building a dynamics model for the particle filter

6. The outcomes: a fully parametric paraglider model


Intro to the Intro
==================

[[**FIXME: these paragraphs are too long? Move some detail to the full
sections.**]]


.. Establishing a research territory (Context):

Paragliding is a recreational flying activity that uses a lightweight,
flexible wing for non-powered flight. Because a paraglider is a non-powered
aircraft its motion is entirely dictated by interactions with gravity and
wind, which means paragliding pilots are totally dependent on the local air
currents to achieve their flight goals. As with all lifting surfaces, the
aerodynamics of a paragliding wing depend on the relative velocity between the
wing and the air, not the relative velocity between the wing and the ground.
If the air is ascending it allows the pilot to slow their descent, or even
gain altitude; conversely, sinking air will cause the wing to descend more
quickly. The horizontal component of the wind determines the speed the glider
can fly in a given direction. A successful flight depends on the pilot's
ability to recognize the structure of the local air currents and navigate them
in order to achieve their flight goals, which may include optimizing for
flight time, distance, or a particular route. Because a glider is constantly
spending energy to counteract the force of gravity, the pilot must recognize
the wind patterns as quickly as possible to minimize energy loss. Experienced
pilots assess the nearby air currents by observing vegetation, birds, or other
pilots, but they can also leverage knowledge gained from previous flights:
although local wind configurations are difficult to predict, they can exhibit
recurring patterns. By learning those patterns a pilot can assess the current
wind conditions more quickly and with better odds of success, and can
prioritize flying to areas that are likely to support their flight goals.


.. Establishing a niche (Problem and Significance):

Traditionally, wind patterns are discovered by pilots with a large amount of
flight time in a particular area, and are shared directly from one pilot to
another. For the pilot community to learn reliable patterns, individual pilots
must first recognize them and then be able to communicate them with precision.
An appealing alternative would be to aggregate recorded flight data from many
pilots over many flights, detect the wind patterns automatically from those
flights, and build a graphical map to communicate the features of the wind
field visually instead of relying on verbal descriptions. In support of this
idea, there already exist large databases with millions of recorded flights
spanning several decades. These databases continue to grow as pilots record
and share their flights for personal and competition purposes. The difficulty
with this option is that common flight devices only record a tiny amount of
the information available to a pilot: in fact, the average flight record can
only be expected to include a time series of positions. There is typically no
information regarding the orientation, velocity, acceleration, pilot control
inputs (brakes, accelerator, etc), or the weather conditions. Even the details
of the aircraft are unknown. The question then becomes whether there is enough
information in position-only time series data to recover the wind vectors that
were present during a flight.


.. Occupying the niche (Response):

This thesis investigates the procedures necessary to produce a predictive
model for wind fields using position-only time series flight data from
a paraglider. The primary contribution of this project is a parametric
paraglider dynamics model for simulating paraglider flight tracks for a given
wind field and pilot control sequence. It discusses how the dynamics model
enables simulation-based filtering methods to perform statistical flight
reconstruction, and the requirements for a flight recording to be suitable for
flight reconstruction. Lastly, it discusses the requirements for assembling
a predictive model suitable for in-flight wind field estimation.


Context
=======

.. "Provides the full context in a way that flows from the opening."

Paragliding
-----------

* Paragliding as a sport

* What are the tasks of a paragliding pilot?

  Paragliding is a non-motorized form of flight, which means it requires wind
  power for sustained flight. Pilots rely on their ability to find regions of
  rising air in order to gain altitude. They must also determine the direction
  and magnitude of the wind in order to determine what regions of the air they
  can access/explore, and to calculate suitable landing zones. [[ie, pilots
  are totally dependent on the local wind pattern]]

* What equipment is involved? (Describe the system.)


Wind fields
-----------

* Describe the wind field as a composite of features (shear, updrafts, gusts)

  Prioritize wind field information that is important to pilots. For
  example, house thermals, finding lift along a ridge, avoiding sink near
  a stream, etc.

* Describe the causes of a wind field.

* Describe how the patterns depend on the time of year, latitude, topography,
  etc.


Restatement of the problem (and significance)
=============================================

.. "Restate the problem and significance in light of the more thoroughly
   detailed context."

[[Remember: **the problem is "learning the wind patterns, and why wind
patterns are important to pilots", not why the wind is important in
general**.]]


* How do pilots depend on the wind field?

  * Consider both the vertical and horizontal components. Consider both
    pre-flight (flight planning) and mid-flight scenarios.

* Why is it important to figure out what's happening as quickly as possible?

* How do pilots (currently) predict and estimate the wind field mid-flight?

  * Exploring the wind field for information comes at a cost; exploration
    requires time, which costs energy (since the wing is always sinking).

* How does learning wind patterns help a pilot make better choices?

  Knowing historical trends improve the accuracy of a pilot's estimates of the
  current conditions, and lets them make better predictions with less
  information. 

* How do pilots learn wind patterns (so they make better estimates)?

  * Currently, through personal experience and word of mouth

* What would be the advantages of learning from recorded flights?

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


Restatement of the response
===========================

.. Recap:

   * The problem: estimating wind information from flight tracks. (This is the
     big picture problem, not the detailed problems of the response.)

   * The significance: help pilots learn wind patterns

   * The response: use model dynamics to estimate the wind field


1. Develop an informal intuition of how this would work. Start by painting
   a picture of a pilot watching another glider in the sky. Discuss how they
   use their intuition of wing performance to guess the wind condition. If
   a human can approximate the wind from position-only data, then
   a mathematical model could too.

#. Establish the requirements of the solution in order for it to be considered
   a success.

   * How to communicate uncertainty of the solution. Point-estimates by
     themselves are worthless; just because the model produces a number
     doesn't mean you should trust it.

#. Discuss the available data. This determines the set of possible solutions
   (ie, it constraints the feasible set of filter designs).

   * Time series of position, approximate air density?

   * The raw data is stored in IGC files, which must be parsed and sanitized.
     Parsing is straightforward, since the data follows a well-defined format.
     Sanitizing the data is more difficult: erratic timestamps, pressure
     altitude biases, and unknown sensor characteristics all present their own
     sets of concerns. Due to time constraints, data parsing and sanitization
     will not be handled in this thesis.

#. Discuss the difficulties of learning wind patterns from the available data.
   Don't discuss how to mitigate them yet; just refine the requirements of the
   response.

   * Observations of position are noisy.

   * No observations of the wind vectors, pilot inputs, or topography.

   * No knowledge of wing parameters or sensor characteristics.

#. Preview the strategies for overcoming the difficulties (preferably in the
   same order they were presented, if possible)

   * Managing uncertainty through Bayesian statistics

     *Bayesian statistics* is a theoretical framework that interprets
     statements of *probability* as statements of ignorance; probability
     represents the *degree of belief* in some outcome. It uses the rules of
     probability to relate uncertain quantities and to quantify the "state of
     ignorance" of the result.

     You don't produce "best guess" point-estimates, you produce an entire
     distribution over all possible values. The question is not "can I produce
     **an** estimate?" but rather "can I produce a **useful** estimate?" You
     can always produce an answer, but it's only useful if the probability
     mass is spread over a useably small range of outcomes.

   * Dealing with the underdetermined system via simulation-based methods

     * Producing the distribution over possible outcomes requires first
       producing the set of possible outcomes and then assigning weights
       (probabilities) to each outcomes. Generating the outcomes requires
       a relationship between the data (the flight track) and the outcomes
       (the wind vectors). The relationship between the paraglider position
       and the wind is provided by the paraglider dynamics.

     * A difficulty with this approach is that the paraglider dynamics rely on
       not only the wind vectors, but also on the wing dynamics, orientation,
       and pilot controls. Because those values were not recorded, they are
       not present in the observational data, which means this *inverse
       problem* must deal with a highly underdetermined system of equations.
       In the terminology of statistics, this means the wind vectors are not
       *identifiable*: there are many different flight scenarios that could
       explain the observed data. The wind cannot be determined without
       knowledge the wing behavior and control inputs, which means that
       *simulation-based filtering* methods are required.

       [[What about PVA approaches that ignore the relative wind, such as
       Michael von Kaenel's thesis?]]

       [[Useful paragraph, but it doesn't explain how you solve it. This is
       basically arguing (again) that you need a distribution over outcomes,
       but that wasn't suppose to be the point of this paragraph. It was
       supposed to be about highlight the fact that you utilize the
       relationship between the flight track and the wind vectors you need
       more information, and that information comes from simulations. You
       don't care about the simulations themselves (they're nuisance
       parameters), you just care about getting that sweet distribution over
       the wind vectors.]]

     * The essence of simulation-based methods is to explore the possible true
       state by utilizing a large set of guesses, called *proposals*. Each
       proposal is a possible value of the current state, and each proposal
       receives a score, called a *weight*, according to how well they explain
       the observations. Although there is no closed form probability
       distribution for these guesses, by making a large number of guesses you
       can arrive at an empirical probability distribution over solutions of
       the system state at each point in time. The precise state of the system
       is still unknown, but the set of possible solutions may be bounded
       enough to be useful.

     * Given a complete set of dynamics (for the wing, pilot controls, and
       wind), you can generate simulated flight trajectories.

   * Approximating the missing dynamics through a parametric model (enables
     parameter estimation or empirical approximations of wing models)

     * The great difficulty with model simulations is that they require
       equations that encode the model dynamics. Aerodynamics are non-trivial
       in even the most simple applications, and paragliders are particularly
       challenging aircraft to analyze due to their curvature and flexibility.
       In addition to the aerodynamics, the paraglider models themselves are
       uncertain, since the wing specifications are generally unknown for any
       given recorded flight; instead of a single, exactly-defined model, you
       need a parametric model that can be configured to match the unknown
       wing. Because the wing configuration is unknown, this estimation
       problem must be applied to not only the system state, but to the model
       parameters as well (also known as a *dual estimation problem*).

#. Discuss the contributions of my paper

   * Math

     * Parametric paraglider geometry

   * Code

     * Paraglider dynamics model

     * Reference wind models (for testing the model and generating test flights)

     * A simulator

     * IGC parsing code

     * Rudimentary GMSPPF?  (Stretch goal!!!)

   * Explain why I'm implementing everything in Python.

     * Approachable syntax

     * Free (unlike matlab)

     * Numerical libraries (numpy, scipy)

     * Large library ecosystem (s2sphere, sklearn, databases, PyMC3, pandas, etc)

#. Things I'd like to discuss but not finish

   * Parameter estimation for the sensor noise?

   * Paraglider model identification (parameter estimation for the wing)

   * Turbulence models, etc, for the wind dynamics?

   * Control inputs

     * Given a parametric paraglider model and a method for evaluating the
       aerodynamic forces that arise from a given set of wind conditions and
       control inputs, you can design a set of state dynamics equations for
       the total system. Those state dynamics are the basis of generating
       predictions as part of the particle filter time update step.

     * Gaussian processes for the proposal distribution?

   * Digital elevation models for the topography?

   * Wind field regression

     * Each flight is a set of observations. They need to be merged (if
       there are multiple overlapping flights) and used in a kriging process
       to build a regression model for the wind field at the time+place of
       the flight.

     * Consider *model-free* proposals vs *model-based* proposals

     * Gaussian processes for wind field regression? (need to turn the wind
       velocity time series into a spatial model).

   * Predictive model

     * Given a set of wind field regression models, needs to find regions
       with overlapping observations, then look for correlations in those
       co-observed regions.

     * Regional correlations must be encoded into a predictive model that
       can be queried (ie, if part of the wind field is (noisily) observed,
       and they have known correlations, the predictive model should produce
       estimates of unobserved regions)

     * Ultimately, this predictive model will be useable in-flight, so as
       the pilot samples the wind field, the predictive model can suggest
       regions with desirable wind patterns.

     * How to combine the set of wind field regression models into
       a spatiotemporal predictive model?


SNIPPETS
========

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

* Flight path reconstruction

  * The term *flight path reconstruction* seems to have a particular meaning
    in some portions of the aerospace community, where it is used to indicate
    kinematics-based state estimation as a component in model validation and
    calibration. (For a good survey on this topic, see
    :cite:`mulder1999NonlinearAircraftFlight`.) As a kinematics-based method,
    the models are built around *specific forces* and angular rates instead of
    aerodynamic forces and moments. As such, it is more concerned with
    **describing** and aircraft's motion instead of **explaining** its motion.

    In my project, the explanation is the most important aspect: the aircraft
    motion is the result of interactions with the wind. That interaction is
    the key relationship between what we know (position) and what we want
    (wind), which is why I can't use kinematics-only filtering.

  * I'm calling my efforts in this paper "flight reconstruction" because it's
    not just the path of the wing I'm interested in. I'm also reconstruction
    the environment of the flight (the wind and control inputs).

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


Detailed tasks list
-------------------

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


Flight Reconstruction
---------------------

Flight reconstruction: what is it, why would it be useful, and what's involved
in performing it? This section should decompose the big picture task of
"turning flight data into a predictive model suitable for in-flight feedback"
into a collection of subtasks.

1. What is flight reconstruction?

   * Reconstructing the flight conditions for an individual flight

   * More than simply recreating the flight track (the physical trajectory of
     the wing), simulation-based filtering is a method for generating
     estimates of unobserved variables from otherwise highly *underdetermined*
     systems.

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


Roadmap
=======

.. "Brief indication of how the thesis will proceed."

Upcoming chapters:

* Formalize the "restatement of the problem" in probabilistic terms. The math
  will produce a set of terms, each of which are their own topic. For example,
  the "underdetermined system" problem is the impetus for "simulation-based
  flight reconstruction", which segues into particle filtering, which in turn
  will necessitate the parametric model. (The focus of this project.)

* Review the available data. Primary sources are IGC files, but could also
  suggest augmenting that with atmospheric equations, digital elevation
  models, radiosondes, RASP, etc.

  Probably need to put this chapter earlier than the chapter on particle
  filtering. The limitations of the data is what motivates simulation-based
  filtering. Or maybe it's small enough to put this in the introduction?


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

    * :cite:`menezes2018EvaluationStochasticModeldependent`: flight planning
      with environmental estimates. Might have some useful overlap for how
      I frame the tasks of this paper.

    * :cite:`lawrance2011PathPlanningAutonomous`

    * :cite:`lawrance2011AutonomousExplorationWind`

    * :cite:`lawrance2009WindEnergyBased`

  * Input estimation

    * :cite:`kampoon2014WindFieldEstimation`
