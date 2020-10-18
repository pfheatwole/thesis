************
Introduction
************

.. Meta:

   Structure taken from `Exploration of Style
   <https://explorationsofstyle.com/2013/02/20/structuring-a-thesis-introduction/>`_.

   This chapter should establish:

   1. The problem: learn wind patterns from recorded flights

   2. The value: feedback helps pilot enjoy better flights

   3. The difficulty: not enough data

   4. The approach: introduce more information via flight dynamics

   5. The focus: building a dynamics model for the particle filter

   6. The outcomes: a fully parametric paraglider model


Intro to the Intro
==================

[[**FIXME: these paragraphs are outdated (and too long). Rewrite.**]]


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
the wind patterns as quickly as possible to minimize energy loss. [[Awkward;
I'm trying to say "time has an energy cost"]] Experienced pilots assess the
nearby air currents by observing vegetation, birds, or other pilots, but they
can also leverage knowledge gained from previous flights: although local wind
configurations are difficult to predict, they can exhibit recurring patterns.
By learning those patterns a pilot can assess the current wind conditions more
quickly and with better odds of success, and can prioritize flying to areas
that are likely to support their flight goals.


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



.. Context

   "Provides the full context in a way that flows from the opening."


Paragliding
===========

* What is paragliding?

  * Paragliding is a recreational flying activity that uses a lightweight,
    flexible wing for non-powered flight.

* What equipment is involved? (Describe the system.)

* What are the common goals of paragliding flights?


Wind Fields
===========

.. Discuss wind fields and their importance to paragliding pilots

* How do paragliders depend on the wind?

  * Because a paraglider is a non-powered aircraft its motion is entirely
    dictated by interactions with gravity and wind.

  * The aerodynamics of a paragliding wing are a function of the relative
    velocity between the wing and the air, which means a pilot is totally
    dependent on the local air currents to achieve their flight goals. If the
    air is ascending a pilot can slow their descent, or even gain altitude;
    conversely, sinking air will cause the wing to descend more quickly. The
    horizontal component of the wind dictates the ground speed of the glider
    in a given direction, which determines what regions of the air the pilot
    can access, and what landing zones they can reach.

* Why do pilots need to know the structure of the wind field?

  * A successful flight depends on the pilot's ability to recognize the
    structure of the local air currents and navigate them in order to achieve
    their flight goals, which may include optimizing for flight time,
    distance, or a particular route.

* What are some examples of structure in a wind field?

  * [[Describe the local wind field as a composite of basic features: shear,
    updrafts, and gusts. See :cite:`bencatel2013AtmosphericFlowField`

    Prioritize wind field information that is important to pilots. For
    example, house thermals, finding lift along a ridge, avoiding sink near
    a stream, etc.]]

* Why is it important to determine the structure as quickly as possible? Why
  is it important for a pilot to be able to **predict** the structure?

  * It takes a constant exchange of momentum between the wing and the air to
    keep the paraglider airborne, so time has an energy cost.

  * Efficient path planning minimizes energy expenditure.

  * Pilots with better path planning are more likely to achieve their flight
    goals.


.. Restatement of the problem (and significance)

   "Restate the problem and significance in light of the more thoroughly
   detailed context."

Predictive Modeling
===================

* How do pilots estimate the structure?

  * By exploration

  * By observing local features, such as dust, vegetation, and birds

  * By using heuristics (ridge orientation to the wind, thermal triggers, etc)

  * By previewing atmospheric structure through meteorological forecasts
    (weather forecasts, RASP), `soaringmeteoGFS
    <http://soaringmeteo.org/GFSw/googleMap.html>`_

  * By studying local *wind patterns*

    * Word of mouth, thermal hotspot maps, `Paragliding Thermal Maps
      <http://thermal.kk7.ch>`_ (**make sure to check the "Statistics and
      Developer Information" sidebar; lots of great links!**), `Paragliding
      Maps <http://www.paraglidingmaps.com>`_


.. Discuss wind patterns, their importance, and how they're learned

* What are *wind patterns*?

  * In this paper, a *wind pattern* is any recurring structure in a wind
    field.

    [[By "structure" I don't mean it needs to be follow some predetermined
    model "structure", like shear lines, ridge lift, thermal sources/sinks,
    etc. I simply mean subsets of the wind field with configurations that are
    predictable based on historical patterns.]]

* Why are wind patterns so **particularly** valuable?

  [[If a wind field has recurring structure, then pilots can use that to
  predict the structure before/without exploring that area.

  Consider both the vertical and horizontal components. Consider both
  pre-flight (flight planning) and in-flight scenarios.]]

* How do pilots learn wind patterns?

  * By flying in the same region repeatedly.

  * By talking to other pilots.

* What are problems with requiring pilots to memorize local patterns?

  * More complex sites have too many variables, so pilots can only remember
    the most dominant patterns, and must generalize the rest.

* Solution: use a computer to build a predictive model from flight data

* What are predictive models?

  * Predictive models encode predictable structure. Some wind field patterns
    can be predicted based on time of day/year, some can be predicted based on
    the values of other regions of the wind field, etc. This is the essence of
    "conditioning" our predictions.

  * Predictive models inform pilots of historical trends, which can help them
    recognize the current structure as early as possible; ideally, before they
    even fly into a new area. They can also improve the accuracy of a pilot's
    estimate of the current wind field.

  * [[**Computer** models that predict the structure of the wind field.]]

  * [[I'm leaving "pattern" vague, so this can include things like Paragliding
    Thermal Map, etc. Those tools only estimate simple point sources I'm still
    considering them "recurring structure".]]

* What is are the benefits of predictive models?

  * The primary goal is to help pilots determine the structure of wind fields
    *efficiently* (both in terms of time and energy) and *accurately*.  Pilots
    would be able to determine the wind field more efficiently and more
    accurately if they were able to compare it to previously observed wind
    fields. (ie, learn the patterns)

  * A secondary benefit would be to help pilots predict days with good flying
    conditions; imagine a website with a simple model that looks as prevailing
    winds and suggests the "most probable" wind field.

* What are the advantages of a predictive model that learns from recorded
  flights?

  * Automate pattern discovery [[Some trends may be subtle or infrequent.]]

  * Utilize all recorded flights from all pilots instead of requiring multiple
    flights by the same pilot. [[If a pilot only encountered a particular wind
    configuration a single time, they wouldn't recognize it as part of
    a recurring pattern.]]

  * Expand the set of detectable patterns: a single flight can only
    observe a small portion of the wind field. By merging multiple flights
    that occurred at the same time, you can build a more comprehensive
    observation of the field. With larger observations there are more
    opportunities for detecting useful patterns.

  * Quantifying/encoding the patterns in mathematical form would enable the
    creation of a *predictive model*.

    A statistical predictive model can provide confidence levels: it can
    quantify the variance in its predictions, since it knows how much evidence
    is present for a particular pattern. [[How does this compare to
    word-of-mouth knowledge? Pilots can be deceived/biased about their
    experiences; memories are faulty.]]

* What are the existing predictive models built from flight data?

  * Paragliding Thermal Map, etc

* What are the limitations of existing predictive models?

  * Existing models can only condition on crude measurements like the season
    or time of day, which can result in simplistic predictions that are simple
    "average" configurations averaged over arbitrary time intervals.

    [[Current predictive models have no estimate of the underlying wind field,
    so they **can't** use it to condition the model.]]

  * Predictions are better if you can condition them on current **conditions**
    (not just time).

    [[In a sense, the model is marginalizing over the unspecified inputs.
    Existing models don't take observations of the wind field into account, so
    they're effectively marginalizing over **all possible conditions** to
    produce an average. (Or something like that.)]]


.. Introduce the long-term objective: a wind field predictive model that
   conditions on observations of the wind field (as well as time/day).

* A predictive model that can condition on estimates of the wind field can
  predict the *actual* configuration instead of some *average* configuration
  (which is typically produced by averaging over some arbitrary time
  interval).

* This model would have advantages both for pre-flight and in-flight
  predictions.

  For in-flight predictions, it could produce estimates that are consistent
  with the observations of the current wind configuration (averages lump
  everything together).

  For pre-flight predictions, you could use global-scale wind forecasts as
  pseudo-observations to forecast details of the local wind field.

  [[Note: you don't have to use the same predictive model for both; for
  example, if you have wind forecasts on a grid of the surrounding area, you
  could train the model using the values of those predictor variables (which
  are **not** the same thing as observations of the wind field itself.]]

* Before you can build a predictive model over wind fields, you need the wind
  wind fields. To get the wind fields, you need the wind vectors. To get the
  wind vectors from position, you need to use the paraglider dynamics to infer
  the cause (the wind) based on the observed effect (the paraglider motion).

* The first step is to recover the actual wind vectors instead of using
  paraglider motion as a proxy for the wind vectors.

* What are the difficulties of recovering wind fields from a paragliding
  flight record? Is it even possible?

  * The flight tracks are position-only time series. No record of the
    paraglider model, pilot inputs, wind vectors, etc.


.. Restatement of the response

   "Leverage the detail presented in the full context to elaborate on the
   details of the response."

My Response Here
================

.. So, the goal is to build a predictive model that conditions on observations
   of the wind field. How does this paper respond to that challenge?


*  [[People are already predicting aspects of the wind field structure from
   data (eg, thermal maps). **This is to do is qualitatively different from
   conditioning on things like "month". This section must communicate that.**

   I must contrast my approach with existing methods that "learn from flight
   data", like the thermal maps. Those are *model-free* methods
   (kinematic-based filtering), I'm focusing on *model-based* methods.

   (Related: "data driven" vs "model driven", from "Probabilistic forecasting
   and Bayesian data assimilation" (Reich, Cotter; 2015). Also, page 549 of
   "Statistical Rethinking" (McElreath; 2020), which is discussing the problem
   of using noisy data to predict future data (like simple ARMA models do,
   thus propagating measurement error into the prediction.)

   Another difference: I think the flight-based maps average over all flights
   (possibly segmented by month/season). I'm interested in a predictive model
   that can condition the prediction based on current conditions; for that you
   need individual patterns, not a simple average.]]

* Decompose the "build a predictive model" into formalized subtasks

* The goals of this paper:

  #. Define the *flight reconstruction* subtask, and establish that it
     requires a parametric paraglider model

  #. Provide a parametric dynamics model suitable for recovering the wind
     vectors

  #. Survey the remaining work



SCRATCH: My Deliverables
------------------------

* Derivations are in an appendix

* Implementations of the paraglider geometry and dynamics are available in
  Python

* Everything is under open licensing: code is MIT, writeup is CC-BY


* Math

  * Parametric paraglider geometry

* Code

  * Paraglider dynamics models

  * Simple wind models (for testing the model and generating test flights)

  * A simulator

  * IGC parsing code

  * Rudimentary GMSPPF?  (Stretch goal!!!)

* Explain why I'm implementing everything in Python.

  * Approachable syntax

  * Good cross-domain language

  * Free (unlike matlab)

  * Numerical libraries (numpy, scipy)

  * Large library ecosystem (s2sphere, sklearn, databases, PyMC3, pandas, etc)

  * Easy integration into tools w/ native support (Blender, FreeCAD, QGIS)


Roadmap
=======

.. "Brief indication of how the thesis will proceed."

Upcoming chapters:

* Formalize the "restatement of the problem" in probabilistic terms. The math
  will produce a set of terms, each of which are their own topic. For example,
  the *underdetermined system* problem is the impetus for *simulation-based
  flight reconstruction*, which segues into particle filtering, which in turn
  will necessitate the parametric model. (The focus of this project.)

* Review the available data. Primary sources are IGC files, but could also
  suggest augmenting that with atmospheric equations, digital elevation
  models, radiosondes, RASP, etc. Those might fit well in my discussion about
  "adding information" to make up for the dearth of data; maybe put it under
  a "brain storm information we can add" prior to the mathematical
  formalization.

  Probably need to put this chapter earlier than the chapter on particle
  filtering. The limitations of the data is what motivates simulation-based
  filtering. Or maybe it's small enough to put this in the introduction?

  [[Update 2020-09-26: on second thought, maybe not. Start with the simplest
  possible problem statement: I have time-series of position, nothing more.
  I can dig into the data more later on when I'm discussing filter design.
  I'll already be discussing sensor noise, etc.]]


SCRATCH
=======

* My intermediate objective is *model-based* filtering to estimate the
  underlying wind field. (*Model-based* methods can dramatically outperform
  *model-free* methods such as kinematics-only Kalman filters).

  Model-free methods like "paragliding thermal map" tend to just show
  "pilots found lift near the ridge, and sink over bodies of water".
  Interesting, but ultimately **not very informative**, because that
  information is already encoded in heuristics that pilot's already know: lift
  along ridges, sink over bodies of water.

  Worse, they neglect the fact that a paraglider can be ascending in sink
  (under weird conditions), or descending in lift. This makes the "data" far
  noisy; you could fix this by averaging if you had a ton of observations, but
  you don't: each observation is precious.

* Interesting: you can think of the methods that are simple averages over
  a time interval as a prior for the wind field during that interval. I'm just
  wanting to take it further and condition that prior (to get the posterior).
  I think that's kinda what he means on page 171 (182) of "Probabilistic
  forecasting and Bayesian data assimilation" when he mentions "model-based
  forecast uncertainties taking the role of prior distributions"

* Existing predictive models (thermal maps) use the paraglider motion as
  a proxy for the wind vector. Because of ambiguity in the horizontal motion,
  they ignore it and only use the vertical component. The result is a map that
  simply shows the average vertical velocity, which doesn't necessarily
  correspond to the actual wind field. (I think "Paragliding Thermal Maps"
  tries to "locate" the thermal trigger, which might explain why it assumes
  ridges are always awesome.)


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

  The key frame of mind for this project is that the question is not "can you
  produce an estimate the wind from position-only data?", but rather "how
  **how good** of an estimate of wind is possible from position-only data?" An
  estimate doesn't need to be especially precise in order to be useful to
  a pilot who is trying to understand the local wind patterns.

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


My "Response" to this problem
-----------------------------

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
   (ie, it constrains the feasible set of filter designs).

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


Related Works
-------------

[[This seems too broad to put up front; I do love papers with these sections,
but I suspect it'd get unwieldy very fast if I put this discussion here.]]


* Wind estimation

  * Offline wind estimation / Learning from flight databases

    * :cite:`ultsch2010DataMiningDistinguish`

    * :cite:`vonkanel2010ParaglidingNetSensorNetwork`

  * Online wind estimation

    * :cite:`vonkanel2011IkarusLargescaleParticipatory`

    * :cite:`wirz2011RealtimeDetectionRecommendation`

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
