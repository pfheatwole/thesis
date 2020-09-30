Introduction
============

Outline:

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
     are inadequate. Conclude they that we need a model-driven method.

   * Solution: we need more information

     * Specifically, we must introduce more information via flight dynamics

     * Build intuition for the model-based method by giving a "conversational"
       walkthrough of how a pilot might estimate the wind by watching
       a glider. They're using domain knowledge; the program should do the
       same.

   * The new goal is to quantify a pilot's "intuitive" knowledge in
     a mathematical form. The mathematical form enables statistical filtering
     methods that can combine the knowledge with our data to get what we want.

#. Summarize the contribution of this work

   * This paper is in two parts: the first part is a concrete implementation
     of a parametric paraglider dynamics model (the basis for step 1); the
     second part is a survey of the remaining subtasks and their
     considerations.

   * Derivations are in an appendix

   * Implementations available in Python

   * Code is MIT licensed, writeup is CC-BY


Probabilistic flight reconstruction
===================================

* [[**This chapter is responsible for convincing the reader that there exists
  some path towards solving the informal problem statement, and that path
  requires the dynamics. It will accomplish this by translating the informal
  problem statement from the introduction into a formal, probabilistic
  equation that explicitly motivates the dynamics model.**]]

  * Its job is to motivate the dynamics while hiding the statistics from
    readers that only care about the dynamics.

  * Arguing "if you're going to solve it, you'll need the dynamics" is easier
    than arguing "if you had the dynamics, you could solve it". This chapter
    only deals with the first part; nevertheless, connecting the informal
    discussion to the filtering equation adds a sense of legitimacy to the
    objective; like "if you give me the dynamics, here's the name of the
    theory you can use to apply it."

    That said, this chapter should avoid discussions of how you might
    **solve** the filtering equation; leave any discussion of filtering
    architectures until future chapters.


* The first step to learning wind patterns is to estimate the wind vectors
  from individual flights. (Although the wind vectors could be estimated
  concurrently with a wind field regression model, for simplicity this chapter
  assumes these steps are separate.)

* The flight data doesn't explicitly record the wind vectors, and we can't
  compute them directly from the positions. To estimate the wind vectors we
  must introduce more information; specifically, we require a relationship
  between the sequence of positions and the sequence of wind vectors.

* The relationship between the wind vectors and the motion of the aircraft is
  given by the canopy aerodynamics.

* Using the canopy aerodynamics to determine the wind vectors is an *inverse
  problem*: given the effects, we wish to determine the causes.

* But this inverse problem isn't deterministic: it's stochastic. There is
  uncertainty in the data, wind, controls, and model, so a complete solution
  should provide *uncertainty quantification*.

* Estimating the values of a stochastic process is the domain of *statistical
  filtering*.

* Statistical filtering problems involving values that evolve over time can be
  modeled with the *recursive filtering equation*.

* The recursive filtering equation requires a transition function, prior
  distributions, and a likelihood function.

* The focus of this work is on the dynamics model.



Canopy geometry
===============

* The easiest way to design a parametric dynamics model is to start with
  a parametric geometry.

* This chapter chooses a target level-of-detail, then presents an intuitive
  parametrization to enable creating models at that level of detail.


Outline:

1. Introduction

   #. What is a canopy?

   #. Why does this project need a mathematical model of canopy geometry?

   #. What are the important aspects of the canopy geometry?

   #. What are **MY** performance requirements for a mathematical model?

   #. How do you design a mathematical model that achieves those requirements?

   #. What is the rest of the chapter about?

#. Chord Surface

   #. Review existing parametrizations of the chord surface?

   #. Introduce my general parametrization of a chord surface. Discuss the
      section index, and how to specify scale, position, and orientation.

   #. Refine/optimize/simplify the general parametrization for parafoils (this is
      where I choose a definition of the section index, set `r_y = r_z = r_yz`,
      parametrize `C_w/s` using Euler angles, etc. **My examples use six design
      functions; I need to get there somehow**)

   #. Discuss parametric design functions? (eg, an elliptical arc)

   #. Present examples of parametric chord surfaces

#. Section profiles

   #. Discuss section profiles (airfoils)

   #. Discuss how the airfoil affects wing performance?

   #. Discuss how they can vary along the span?

   #. Discuss distortions due to billowing, braking, etc?

   [[This isn't meant to be an exhaustive discussion of parafoil design!]]

#. Examples of complete parametric canopies

#. Advantages and limitations


Canopy aerodynamics
===================

* This is my link between position and the wind.


Paraglider geometry
===================

* The paraglider is a system composed of wing and harness.


Paraglider dynamics
===================

* This is what we use to drive the flight simulator


Case study
==========

* Walk through a simple design example for a paraglider. This should view the
  problem from the standpoint of a user trying to approximate an existing wing
  from technical specs and an on-hand wing. (ie, show how to use what I've
  created)


Flight simulation
=================

* The filtering equation needs a transition function


Future work
===========

* Survey the remaining steps

  * Summarize the tidbits I've learned and open questions I know about?

* Maybe call these *resources*; they're incomplete, but still useful.


Model optimization
------------------

* The NLLT is probably too slow to use with a particle filter. It'd be great
  to pre-process the solutions; maybe train a neural network?


Data considerations
-------------------

* Need to characterize sensor noise for a wide range of tracks

* Estimate the atmospheric parameters (air density)

* Consider supplementary sources like topography (eg, a DEM), meteorology (eg,
  RASP), related fields (drainage networks), etc


Filter architecture
-------------------

* Need to "solve" the filtering/smoothing equations for the posterior

  * Are wind vectors independent, or do you try to fit the wind field
    regression model "on-line", and use that to inform the priors? (This would
    probably make any smoothing equations a lot more difficult.)

* Priors

  * Multivariate GP for the control inputs?

  * Wind field models and/or turbulence models for wind vectors?

  * Empirical database for glider parameters?

* Likelihood function (observation model)


Wind field regression
---------------------

* Given an individual track, estimate the underlying wind field.

* Assume constant mean over a fixed time interval?


Pattern detection
-----------------

* Points or areas? Grids or polygons?


Predictive modeling
-------------------

* How do you encode the patterns such that a mobile device can query them?
