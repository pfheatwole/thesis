Remember: this paper, and every chapter in it, should **start with an
introduction that gives away the punchline**. Let the reader determine at
a glance what the chapter will discuss and the basic conclusions.



Introduction
============


.. Context

Paragliding
-----------

* Introduce paragliding as a sport


Wind fields
-----------

* Introduce wind fields

* Discuss the importance of wind to paragliding pilots

* Discuss how pilots benefit from knowledge of the structure of the wind

* Discuss global structure of the *atmospheric boundary layer*

  * Lapse rates, thermal convection, orographic lift, mountain waves, etc.

  * [[These combine with the topology to produce local structure?]]

* Discuss local structure in wind fields

  * Thermal lift and sink, orographic lift, shear (including venturi), etc


.. Problem and significance

Predictive modeling
-------------------

* How do pilots estimate the structure of the current wind field?

* Define *wind patterns* as "**recurring** structure"

* Discuss the importance of wind patterns to paragliding pilots

* How do pilots traditionally *discover* wind patterns?

* How do pilots traditionally *use* wind patterns?

* What are the difficulties of discovering and using wind patterns?

* Goal: discover patterns using flight data (to address the problems of
  discovery) and encode them in a predictive model (to address the problems of
  use)

* What are the advantages of discovering patterns using flight data?

* Define *predictive modeling*

* What are the advantages of encoding patterns in a predictive model?

* Unfortunately the available data does not contain any explicit information
  about the wind fields, so the first step towards building a predictive model
  is to estimate the wind field from the data of each recorded flight.


Wind field estimation
---------------------

* [[Explain the objective: estimating wind field structure from position-only
  data]]

* [[Discuss existing tools: linearized thermals, circle method, etc]]

* [[Explain the limitations of existing tools]]

  * They rely on *heuristics*: approximation methods that rely on the wind
    field containing features with some explicit structure that can be
    detected based on particular patterns of the paraglider motion.

    Thermal detectors may require a minimum sink rate, or total altitude
    gained; horizontal wind estimators may require that the glider was
    circling at a fixed airspeed, etc.

  * Each heuristic can only detect its explicit features. The rest of the data
    is discarded, which also discards valuable information.

  * To avoid false positives, heuristics typically introduce constraints on
    the motion such as minimum duration, minimum number of cycles, etc.

    Given the interval, the heuristic produces an output that is assumed to be
    a representative summary of the entire interval. The output is a sort of
    "averaged structure" that is assumed to be representative of the wind
    field over the entire interval.

    As a result, they tend to "smooth out" the regions they fit. Subtleties in
    the wind field are lost.

    [[FIXME: I don't like this phrasing, but it'll do for now.]]

* [[Conclusion: existing methods are inadequate. We need better estimators.]]


.. Now that we've seen how estimators can underperform we have more context for
   designing better ones in a principled way.

* [[Establish the performance criteria of a wind field estimator]]

  * Don't rely on specific motion patterns

  * Don't depend on explicit wind structure (ie, don't limit the estimator to
    structure that adheres to an explicit model, like a linearized thermal.
    You can *summarize* regions of the wind field using that sort of
    structure, but that should not be fundamental to *estimating* the wind
    field.)

  * Provide uncertainty quantification

* [[How can we produce such an estimator?]]

  * Existing models can't be easily extended to satisfy the criteria. Conclude
    that model-free methods are inadequate; model-based methods are required
    to produce "better" estimates of the wind field (ie, we need full *flight
    reconstruction*).

  * Heuristics are *model-free* methods, which rely on **coincidental**
    relationships between the particular motion sequence and the feature being
    detected. Using a *model-based* method enables introducing **causal**
    relationships: causal dynamics introduce "more" information and are able
    to extract more information from the data.


* [[MISC:

  * You can only predict what you can detect.

    You can only discover "recurring structure" involving structure you're
    capable of detecting that structure in the first place.

  * You can only condition predictions on structure you can detect (applies
    both to detecting structure from data and in-flight)

  * Accuracy is important both when estimating from data and in-flight. If
    you're trying to condition a prediction based on some variable, then your
    "from data" and "in-flight" estimates better agree or the predictions
    could be worse than an unconditional (marginalized) prediction.

  * Discuss uncertainty quantification?

  * Earlier I discussed aspect of wind field structure like thermals, sink,
    and shear, but don't those are sort of "summaries" of the wind field.
    Those are good targets for "feature detectors", but I'm arguing that
    better feature detectors can be created if they have access to the
    underlying wind field.

    I need to show how model-free methods are incapable of estimating those
    from the available data.

  ]]



.. Response

Flight Reconstruction
---------------------

* [[Build intuition for the model-based method by giving a "conversational"
  walk-through of how a pilot might estimate the wind by watching a glider.
  They're using domain knowledge; the program should do the same.

  In essence, that "intuitive" solution is simulating flights. They're doing
  flight reconstruction in their head.

  The new goal is to quantify a pilot's "intuitive" knowledge in mathematical
  form. The mathematical form enables statistical filtering methods that can
  combine the knowledge with our data to get what we want.]]

* [[Define *flight reconstruction*?]]

* [[Describe some of the requirements for a "good" model. Foreshadow the
  overarching need for uncertainty management in all steps.]]


Roadmap
-------

* [[Summarize the contribution of this work]]


Flight reconstruction
=====================

.. Informal overview (conversational definition of the problem)

* Recap: the objective that motivates this paper is to estimate wind fields
  from flight data so the fields can analyzed for patterns.

* Paraglider flight data is limited to position and time, with no direct
  observations of the wind field (making this an *inverse problem*), but we
  can use the knowledge that a paraglider's change in position depends on the
  *wind vectors*, the value of the wind field, at that position. This
  relationship introduces a statistical dependence that can be used to infer
  information about the wind vectors from the position sequence.

  [[Whether the strength of this relationship is sufficient for usefully
  precise estimates is another question.]]

* [[Introduce *inverse problems*: we don't have any direct observations of the
  wind field, so we have to rely on its relationship to the data. In this
  case, we have observed an effect, and wish to determine the cause. Solving
  this inverse problem requires using the paraglider dynamics.]]

* Estimating the wind fields becomes a problem of estimating the wind vectors
  that were encountered during the flight.

* Although our target is the wind vectors, the dynamics also depend on other
  variables, such as pilot controls, and on the paraglider design itself.
  These additional *nuisance variables* must be jointly estimated as part of
  the "complete state" of the flight.

* This chapter describes how to build a statistical model of a paraglider
  flight, how to use it to estimate the full joint probability from the
  sequence of positions, and how to use the joint probability distribution to
  compute the estimate of the sequence of wind vectors.


.. Solving for unknown variables (general review)

Inverse problems
----------------

* Simple example of solving an equation, and a system of equations

* Define *underdetermined system*

* You can "fix" an underdetermined system by adding more information: more
  data, or more relationships (equations)

* What if you still don't have enough information? What does it mean to
  "solve" an underdetermined system?

  We have to rely on statistical inference: instead of "solving" the problem,
  we infer properties of the distribution over what the solution might be.

* Define *inverse problem*

* We are trying to estimate the wind vectors using observations of position.
  We don't observe the wind vectors directly, so wind vector estimation from
  the available data is an *inverse problem*.

* Underdetermined systems cannot be solved exactly, they can only be solved
  approximately. Instead of seeking the single "true" value, the problem
  becomes one of estimating a distribution over all possible values.


* [[The goal is to use statistics to gain information about some target based
  in information gained from some observed data. Conditioning one variable on
  another requires a **statistical dependency** between the them. The
  relationship can be direct or indirect.

  The natural starting place for any data analysis problem is to define
  a model of the data-generating process. If the target is not a member of the
  data-generating process you must be able to extend the model with new
  relationships to induce the dependency. Otherwise, the observed data is not
  informative about the value of the target.]]


Filtering problems
------------------

* A common example of an underdetermined system is a measurement corrupted by
  noise.

* [[Sometimes observations are produced in a sequential fashion]]

* [[Introduce sequential processes]]

* [[Sequential estimation has a special mathematical form]]

* Define *filtering problem*

* Solving a *filtering problem* requires a model of the *data-generating
  process*

* [[*State-space models* of sequential data-generating processes]]

* [[Converting a state-space model to a statistical model]]

* [[Using the full statistical model to solve the filtering problem]]


Flight reconstruction as a filtering problem
--------------------------------------------

.. Could also model this as a *state-estimation problem* if you consider
   the unknown inputs as "state".

* Define a state-space model of the paraglider position

* Review the components of the state-space model

* Define *nuisance variable*

* [[Unlike unpredictable noise terms, these nuisance variables have structured
  dynamics that capture essential information.]]

* Nevertheless, evaluating the paraglider dynamics requires concrete values
  for all of its parameters. Where do those values come from?

* Define *simulation-based filtering*

  [[Essentially, you draw "guesses" for the unobserved variables from
  a proposal distribution, then use the rules of probability to compute the
  posterior probability of the target while accounting for the uncertainty in
  those unobserved variables.]]

  **I should probably stop using the phrase "simulation-based filtering".
  Every filtering architecture that uses a transition function is "simulating"
  the dynamics. I sure highlight the need to simulate the unknown data, but
  stop using this term: it's not informative.**

* [[Flight reconstruction (as we'll be doing it) is many problems in one:
  state-estimation, input-estimation, and parameter-estimation. In the end we
  will marginalize over the nuisance variables to get just the posterior
  distributions of the wind vectors.]]


.. Conclusion

* In this paper, the term *flight reconstruction* refers to this process
  of estimating the full joint probability distribution over all the variables
  in the state-space model for the entire flight sequence.

* The focus of this paper is to provide a parametric paraglider model suitable
  for flight reconstruction of average, non-acrobatic paragliding flights.


Canopy geometry
===============

.. Meta:

   The easiest way to design a parametric dynamics model is to start with
   a parametric geometry. This chapter chooses a target level-of-detail, then
   presents an intuitive parametrization to enable creating models at that
   level of detail.


* What is a canopy?

* Why does this project need a mathematical model of the canopy?

  To enable calculating the aerodynamics and inertial properties.

* Describe the physical system

* Choose the model requirements

  * What are the important aspects of a canopy geometry?

  * What sorts of queries should the model answer? [[Points on the chords,
    points on the surfaces, inertial properties, etc.]]

* How do users specify a design?

  * Explicit vs parametric geometries

* What are the goals of a parametrization? (What makes a good one?)

* How do you design a parametrization that achieves those goals?

  Decompose the model into sets of parameters:

  1. *Chord surface*: section scale, position and orientation

  2. *Foil surface*: section profiles

* What is the rest of the chapter about?


Chord Surface
-------------

* What is a chord surface? (Scale, position, and orientation)

* What are the conventional parametrizations of a chord surface?

* What are the limitations of conventional parametrizations?

* Introduce my **general** parametrization of a chord surface.

  Define the *section index*, and how to specify scale, position, and
  orientation.

* Introduce my **simplified** parametrization for parafoils.

  This is where I choose a definition of the section index, set `r_y = r_z
  = r_yz`, parametrize `C_w/s` using Euler angles, etc. **My examples use
  six design functions; I need to get there somehow**)

* Discuss parametric design functions?

  The chord surface is parametrized by functions, those functions can
  themselves be parametric (eg, an elliptical arc)

* Present examples of parametric chord surfaces


Foil surface
------------

* What is a *section profile*?

* How does the choice of airfoil effect wing performance?

* How does the profile vary along the span?

* How does the profile behave in-flight?

  Distortions due to billowing, braking, etc. (We're ignoring these, but
  you can use the section indices to deal with them.)

* [[This should not be an exhaustive discussion of parafoil design!]]


Examples
--------

* Examples of complete parametric canopies


Discussion
----------

* Discussion, pros/cons


Canopy aerodynamics
===================

.. Meta:

   This is the link between position and the wind.


* What are aerodynamics?

* What are the modeling requirements?

  * Physical model

    * Non-linear geometry (straight lifting-line is unacceptable)

    * Non-linear coefficients (don't **start** with a simplistic model; this
      should provide a baseline for judging simplified models)

    * Enables empirical adjustments to viscous drag (existing literature on
      paragliders often provide empirical values that I wanted to incorporate)

    * Non-uniform wind (what happens during a turn, when the wingtip enters
      a thermal, etc)

    * Relaxes the "small AoA" restriction (graceful degradation near stall)

  * Practicalities

    * Simple (relatively easy to implement, no dependence on external tools)

    * Computationally fast (think of this as a rapid prototyping phase)

* [[Section profiles were covered in the previous chapter. The computational
  methods use the profiles either via their section coefficients, or via the
  surface geometry they generate.]]

* Phillips' NLLT

* Case study: Barrows' model

  * Describe the model and wind tunnel dataset

  * Compare the raw data to the VLM and the NLLT

* Discussion, pros/cons


Paraglider geometry
===================

* The paraglider is a system composed of wing (canopy+lines) and payload
  (harness+pilot).

* [[Introduce my chosen specification for a paraglider wing, positioning the
  payload, etc.]]

* [[Provide an example? Like my Hook 3 model.]]


Paraglider dynamics
===================

* Define the canopy dynamics

  * What are they? What are they used for?

  * Provides the dynamics model for generating flight trajectories

* Modeling requirements

* Survey the common options

* Phillips' NLLT

* Case study: wind tunnel test data

  * Introduce the test (the model, the test setup, and the data)

  * Why is this a good test?

    * In terms of aerodynamics: good representation of the unusual geometry of
      a paraglider; completely known geometry (including airfoil); extensive
      data for a range of wind conditions; internal wood structure maintains
      the shape, eliminating uncertainty due to distortions

    * It also provides a good demonstration of how to use my geometry.

  * Discuss the results

* Discussion


Flight simulation
=================

* Define *flight simulation* for the purposes of this paper

* Why does this paper need a flight simulator?

  * To generate test flights for validation. At first this is only helpful for
    superficial checks (do flights "look" correct?), but will eventually be
    necessary for physical flight validation.

  * The filtering equation needs a transition function

* [[Talk about choosing a state representation? Quaternions, etc?]]

* [[Show some demo flights?]]


Future work
===========

.. Review the steps (from data generating to the predictive model) and survey
   the open questions / remaining work for each step.

   * Summarize the tidbits I've learned and open questions I know about?

   * Maybe call these *resources*; they're incomplete, but still useful.


Paraglider model
----------------

* Computational improvements for the dynamics model: Even if the NLLT gives
  reasonable results, it's probably too slow to use with a particle filter.
  It'd be great to pre-process the solutions; maybe train a neural network?

* Distortions (mainly cell billowing)

* Riser-control


Data
----

* Characterizing sensor noise (GPS, variometer)

  * Not sure how to generalize over such a wide range of tracks.

* Atmospheric parameters (air density)

* Supplementary sources

  * Topography (eg, a DEM), meteorology (eg, RASP, TherMap), related fields
    (drainage networks, flowfield tools for wind farms), etc


Flight reconstruction
---------------------

* Need to "solve" the filtering/smoothing equations for the posterior

  * Are wind vectors independent, or do you try to fit the wind field
    regression model "on-line", and use that to inform the priors? (This would
    probably make any smoothing equations a lot more difficult.)

* Priors

  * Multivariate GP for the control inputs?

  * Wind field models and/or turbulence models for wind vectors?

  * Paraglider model identification (model parameter estimation). Use an
    empirical database for glider parameters?

* Likelihood function (observation model)


Filter architecture
^^^^^^^^^^^^^^^^^^^

* Suggest the GMSPPF?


Wind field regression
---------------------

* Estimate the underlying wind field of individual tracks (eg, fit a kriging
  model)

* Combine flights that overlap in time + space?

* Model-free or model-based?

* Constraints

  * Assume constant mean over a fixed time interval?


Wind patterns
-------------

* Choice of modeling target

  * Separate the horizontal and vertical components?

  * *Model-free*  or *model-based*?

    Are patterns *data-driven* (using unstructured wind velocities), or do you
    try to detect and fit explicit thermal models, shear models, etc?

* Representation (Points, lines, areas, volumes? Grids or polygons?)


Predictive modeling
-------------------

* Given a set of wind field regression models, you need to find regions with
  overlapping observations, then look for correlations in those co-observed
  regions.

* Regional correlations must be encoded into a predictive model that can be
  queried (ie, if part of the wind field is (noisily) observed, and they have
  known correlations, the predictive model should produce estimates of
  unobserved regions)

* Ultimately, this predictive model will be useable in-flight, so as the pilot
  samples the wind field, the predictive model can suggest regions with
  desirable wind patterns.

* How to combine the set of wind field regression models into a spatiotemporal
  predictive model?

* How do you encode the patterns such that a mobile device can query them?


Discussion
==========

* Highlight what's been achieved: a parametric geometry and a dynamics model
  in Python

* [[Assume an impatient reader will jump here. This is your last chance to
  convince them the paper is worth reading.]]
