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


