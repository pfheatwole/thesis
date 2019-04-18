****************
Style and Layout
****************


Latex
=====


Memoir
------

These are some scratch notes regarding the `memoir` LaTeX class.

* It can produce **glossaries** and **lists of symbols**

  Excellent for all the math I'll be doing

* It doesn't work with the standard **hyperref** package

   * You must use **memhfixc** after using *hyperref*
   * Recent versions of **hyperref** apply this automatically

* Provides its own flavor of some packages

   * **fancyhdr**, **geometry**, **crop**, etc
   * Probably want to disable **fancyhdr** in Sphinx?


Terminology
^^^^^^^^^^^

 * **recto** page: odd pages, front of the leaf
 * **verso** page: even pages, (back of the leaf
 * **folio**: page number
 * **pagination**: pages with *folios*
 * **preamble**: the region between the `\documentclass` and the start of the
   `document` environment



*******
Content
*******


Trouble Words
=============

* "paraglider wing" vs "paragliding wing"

* accelerator, speedbar/speed-bar/speed bar

* debias, de-bias (when to hyphenate)

* timestep, time-step, time step

* vario, variometer (allowable abbreviations)


Useful Reminders
================

* Use ReST comments to document structural peculiarities (eg, in my HTML
  versus LaTeX sources)

* Signposting is a useful way for the writer to layout their work. It's a way
  of telling yourself what you're going to work on next. Also, you can look
  back and see how your expected path has diverged.

* Signposting *what* you're going to do isn't as helpful as first
  communicating *why* the *what* is necessary.

  Consider "I will discuss particle filtering." versus "Recreating the flight
  requires filling in missing pieces; this type of artificial data generation
  is known as simulation-based filtering. One such method is the particle
  filter."


Abstracts
=========

The most fundamental four statements (not necessarily sentences) of an
abstract for a paper:

1. State the problem

2. State the consequences of the problem

3. State your solution

4. State the consequences of your solution


How do these correspond to blog posts that don't necessarily introduce a novel
solution? They can still establish that a topic exists (the problem) and why
it's worth studying (the consequences), the solution (the knowledge of methods
discussed by the post for dealing with that problem), and the consequences of
that solution (what you should learn by reading this post)


Some examples
-------------

Topic: Encoding Rotations with a Quaternion

1. In engineering, you frequently need to describe how something is rotated
   relative to a starting position.

2. In three dimensions, a rotation must describe a rotation relative to all
   three axes. The most intuitive solution is to describe three independent,
   sequential rotations, but this is computationally expensive and introduces
   a failure called "gimbal lock".

3. Instead of describing three separate rotations, an alternative is to encode
   a new axis, and a rotation around that axis.

4. A compact and numerically efficient way to encode an axis-angle
   representation of a 3D rotation is to use a set of four numbers called
   a "quaternion".


Introduction
============


Intro to the Intro
------------------

The introduction to the introduction is important to my project since the
scope is so broad. Trying to establish the entire context in detail before
getting to a description of what my thesis offers will make the reader wait
a long time before they learn about my contribution. You need to **put the
contribution of the paper front and center; the reader should know ASAP what
they will gain by reading it.**

John Swales' model for "Creating a Research Space" consists of three "moves":

1. Establishing a research territory
 
2. Establishing a niche
 
3. Occupying the niche

 
(An alternative is "Context", "Problem and Significance", and "Response".)

According to Explorations of Style, "An Introduction to the introduction [...]
will be a short version of the three moves, often in as little as three
paragraphs, ending with some sort of transition to the next section where the
full context will be provided."

In my case, I will first set the context (my research territory: paragliding
dependencies on wind patterns), then introduce my motivating goal (my niche:
learning wind patterns from flight data), then introduce how I've made
progress towards goal (how I've occupied the niche: by building the flight
reconstruction portion of the model).


Filtering
=========


Simulation-based Filtering
--------------------------

* Introduce particle filtering

* Highlight how system dynamics and weather limitations enable simulation

Remember: ask "is this content self-contained? Can this chapter be read by
itself and still understood?


Data Assimilation
-----------------

In :cite:`fearnhead2018ParticleFiltersData` he marries *filtering* (an
engineering term) with *data assimilation* (filtering's geophysics analog).

I should try to phrase my problem in terms of both, or however makes sense to
tie in the geophysics realm. There's probably a bunch of good literature to
cite.


