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

* Pilots who want to make use of wind patterns face two problems: *discovery*
  and *use*.

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

* [[Discuss existing methods: linearized thermals, circle method, etc]]

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


.. Response

Flight Reconstruction
---------------------

* [[We don't have a relationship to estimate the total wind field directly
  from a position sequence. We have to start by estimating **local** wind
  vectors using the **changes** in position.]]

* [[Define *flight reconstruction*?]]

* [[Describe some of the requirements for a "good" model. Foreshadow the
  overarching need for uncertainty management in all steps.]]


Roadmap
-------

* [[Summarize the contribution of this work]]


Flight reconstruction
=====================

[["Outline" moved into the chapter body]]


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

* Establish the model requirements

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

  * *Model-free* or *model-based* structure?

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
