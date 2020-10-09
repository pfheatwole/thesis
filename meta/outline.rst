Introduction
============

1. Introduce paragliding

#. Discuss wind fields and their importance to paragliding pilots

#. Discuss wind patterns, their importance, and how they're learned

#. Introduce the objective: wind field predictive modeling

   * Can we learn them from existing data?

   * What are the advantages?

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

#. Summarize the contribution of this work


Flight reconstruction
=====================

.. Meta:

   * This chapter is responsible for arguing that there exists some path
     towards solving the informal problem statement (turning sequences of
     positions into sequences of wind vectors), and that path requires the
     dynamics. It will accomplish this by translating the informal problem
     statement from the introduction into a formal, probabilistic equation
     that explicitly motivates the dynamics model.

   * It should motivate the dynamics while hiding most of the statistics from
     readers that only care about the dynamics.

   * Arguing "if you're going to solve it, you'll need the dynamics" is easier
     than proving "if you had the dynamics, you **definitely can** solve it".
     This chapter only deals with the first part (arguing that the dynamics are
     necessary); nevertheless, connecting the informal discussion to the
     filtering equation adds a sense of legitimacy to the objective; like "if you
     give me the dynamics, here's the name of the theory you can use to
     **possibly** solve it."

     That said, this chapter should avoid discussions of how you might
     **solve** the filtering equation; leave any discussion of filtering
     architectures until future chapters.


* The first step to learning wind patterns is to reconstruct the wind vectors
  from individual flights.

  [[Although a filtering architecture could estimate the wind vectors
  concurrently with the wind field regression model, for simplicity this
  chapter assumes these steps are separate. In particular, it models the
  sequence of wind vectors as a Markov process, so it can't incorporate the
  wind field regression model into the prior for each wind vector.]]

* The flight data doesn't explicitly record the wind vectors, and we can't
  compute them directly from the positions. To estimate the wind vectors we
  must introduce more information; specifically, we require a relationship
  between the sequence of positions and the sequence of wind vectors at those
  positions.

* The relationship between the wind vectors and the motion of the aircraft is
  given by the canopy aerodynamics.

* [[The aerodynamics model adds new variables, like air density and control
  inputs. Maybe introduce those here by using an intuitive "derivation" that
  predicts/assumes their existence.]]

* Using the canopy aerodynamics to determine the wind vectors is an *inverse
  problem*: given the effects, we wish to determine the causes. We need to
  invert the dynamics.

* But this inverse problem isn't deterministic: it's stochastic. There is
  uncertainty in the data, wind, controls, and model, so a complete solution
  should provide *uncertainty quantification*. Instead of providing an exact
  answer, there will be ranges of answers and their estimated probabilities.

* Estimating the values of a stochastic process is the domain of *statistical
  filtering*.

* [[Define the joint probability distribution over state, inputs, and
  observations. Maybe define conditional probability here too.]]

* Estimating the joint probability directly is intractable, but the Markov
  property allows the problem to be rewritten in a tractable form: the
  *recursive filtering equation*.

  [[Old phrasing: "Statistical filtering problems involving values that evolve
  over time can be modeled with the *recursive filtering equation*."]]

* The recursive filtering equation is composed from a set of priors
  (probabilities before seeing any data), a transition function (a dynamics
  model), and a likelihood function (an observation model).

* The transition function is how we "introduce more information" into the
  problem (via the aerodynamics).

* Writing the wind vector estimation task in terms of the recursive filtering
  equation also reveals that there are several subtasks:

  1. State estimation

  2. Parameter estimation (aka model estimation)

  3. Input estimation (the wind vectors live in this subtask)

* "Solving" the filtering problem simply means "estimate the joint probability
  distribution", then *marginalize* the "nuisance" variables (control inputs,
  model parameters, etc) to compute the joint distribution over the position
  and wind vectors. (*Nuisance variables* aren't interesting by themselves,
  but they must be accounted for: the targets depend on the nuisance
  variables, and so the uncertainty of the nuisance variables must be
  incorporated into the uncertainty of the target variables.)

* This paper will not discuss filtering architectures for solving the
  filtering problem. **The focus of this work is on the dynamics model, which
  provides the transition function.**


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
