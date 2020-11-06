Remember: this paper, and every chapter in it, should **start with an
introduction that gives away the punchline**. Let the reader determine at
a glance what the chapter will discuss and the basic conclusions.



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
