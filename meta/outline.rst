Remember: this paper, and every chapter in it, should **start with an
introduction that gives away the punchline**. Let the reader determine at
a glance what the chapter will discuss and the basic conclusions.



Introduction
============

.. Context

1. Introduce paragliding

#. Discuss wind fields and their importance to paragliding pilots

#. Discuss wind patterns, their importance, and how they're learned


.. Problem and significance

#. Introduce the objective: wind field predictive modeling

   * Can we learn them from existing data?

   * What are the advantages?


.. Response

#. Decompose the problem into subtasks

   1. Turn a sequence of positions into a sequence of wind vectors

   #. Turn a sequence of wind vectors into a wind field

   #. Turn a set of wind fields into a set of patterns

   #. Turn a set of patterns into a predictive model

#. Foreshadow the overarching need for uncertainty management in all steps

#. Explicitly focus on the first step

   * Describe the available data (briefly)

   * Consider the relationship between what we know and what we want

   * Consider model-free (data-driven methods) and give examples of why they
     are inadequate.

   * Solution: we need more information

     * Specifically, we must introduce more information via flight dynamics

     * Estimation methods that incorporate knowledge of the underlying system
       dynamics are called *model-based* methods.

     * Build intuition for the model-based method by giving a "conversational"
       walkthrough of how a pilot might estimate the wind by watching
       a glider. They're using domain knowledge; the program should do the
       same.

   * The new goal is to quantify a pilot's "intuitive" knowledge in
     a mathematical form. The mathematical form enables statistical filtering
     methods that can combine the knowledge with our data to get what we want.


.. Roadmap

#. Summarize the contribution of this work


Flight reconstruction
=====================

.. Informal overview (conversational definition of the problem)

* Recap: the objective that motivates this paper is to estimate wind fields
  from flight data so the fields can analyzed for patterns. Estimating the
  wind fields requires knowledge of the wind vectors that were encountered
  during a flight.

* Paraglider flight data is limited to position and time, but a paraglider's
  change in position depends on the wind. This relationship introduces
  a statistical dependence that can be used to infer information about the
  wind vectors from the position sequence.

  [[Whether the strength of this relationship is sufficient for usefully
  precise estimates is another question.]]

* [[Introduce *inverse problems*:  we observe the effect, and wish to
  determine the cause. Solving this inverse problem requires using the
  paraglider dynamics.]]

* Although our target is the wind vectors, the dynamics also depend on other
  variables, such as pilot controls, and on the paraglider design itself.
  These additional *nuisance variables* must be jointly estimated as part of
  the "complete state" of the flight.

* This chapter describes how to build a statistical model of a paraglider
  flight; how to use it to estimate the full joint probability from the
  sequence of positions, and how to use the joint probability distribution to
  compute the estimate of the sequence of wind vectors.


.. Solving for unknown variables (general review)

* Simple example of solving an equation, and a system of equations

* Define *underdetermined system*

* "Fixing" an underdetermined system by adding more information: more data, or
  more relationships

* What if you still don't have enough information? What does it mean to
  "solve" an underdetermined system?

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


.. Filtering problems

* A common example of an underdetermined system is a measurement corrupted by
  noise.

* Define *filtering problem*

* Solving a *filtering problem* requires a model of the *data-generating
  process*

* [[Introduce sequential processes]]

* [[State-space models of sequential data-generating processes]]

* [[Converting a state-space model to a statistical model]]

* [[Using the full statistical model to solve the filtering problem]]


.. Flight reconstruction

* Flight reconstruction as a filtering problem

* Define a state-space model of the paraglider position

* Review the components of the state-space model

* Define *nuisance variable*

* [[Unlike unpredictable noise terms, these nuisance variables have structured
  dynamics that capture essential information. They should not ]]

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


1. Introduction

   #. What is a canopy?

   #. Why does this project need a mathematical model of the canopy?

      To enable calculating the aerodynamics and inertial properties.

   #. What are the important aspects of a canopy geometry?

   #. What sorts of queries should the model answer? [[Points on the chords,
      points on the surfaces, inertial properties, etc.]]

   #. How do you specify a design?

      * Explicit vs parametric geometries

   #. What are the goals of a parametrization? (What makes a good one?)

   #. How do you design a parametrization that achieves those goals?

      Decompose the model into sets of parameters:

      1. Section scale, position and orientation (chord surface)

      2. Section profiles (foil surface)

   #. What is the rest of the chapter about?

#. Chord Surface

   #. What is a chord surface? (Scale, position, and orientation)

   #. What are the conventional parametrizations of a chord surface?

   #. What are the limitations of conventional parametrizations?

   #. Introduce my **general** parametrization of a chord surface.

      Define the *section index*, and how to specify scale, position, and
      orientation.

   #. Introduce my **simplified** parametrization for parafoils.

      This is where I choose a definition of the section index, set `r_y = r_z
      = r_yz`, parametrize `C_w/s` using Euler angles, etc. **My examples use
      six design functions; I need to get there somehow**)

   #. Discuss parametric design functions?

      The chord surface is parametrized by functions, those functions can
      themselves be parametric (eg, an elliptical arc)

   #. Present examples of parametric chord surfaces

#. Foil surface

   * What is a *section profile*?

   * How does the choice of airfoil effect wing performance?

   * How does the profile vary along the span?

   * How does the profile behave in-flight?

     Distortions due to billowing, braking, etc. (We're ignoring these, but
     you can use the section indices to deal with them.)

   * [[This should not be an exhaustive discussion of parafoil design!]]

#. Examples of complete parametric canopies

#. Discussion, pros/cons


Canopy aerodynamics
===================

.. Meta:

   This is the link between position and the wind.


Outline:

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

#. Phillips' NLLT

#. Case study: Barrows' model

   * Describe the model and wind tunnel dataset

   * Compare the raw data to the VLM and the NLLT

#. Discussion, pros/cons


Paraglider geometry
===================

* The paraglider is a system composed of wing (canopy+lines) and payload
  (harness+pilot).

* [[Introduce my chosen specification for a paraglider wing, positioning the
  payload, etc.]]

* [[Provide an example? Like my Hook 3 model.]]


Paraglider dynamics
===================

#. This provides the dynamics model for generating flight trajectories

#. Discussion, pros/cons


Flight simulation
=================

* The filtering equation needs a transition function

* [[Talk about choosing a state representation? Quaternions, etc?]]

* [[Show some demo flights?]]


Future work
===========

* Survey the remaining steps

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

  * Topography (eg, a DEM), meteorology (eg, RASP), related fields (drainage
    networks), etc


Filter architecture
-------------------

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
