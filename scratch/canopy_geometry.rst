Overview
========

The goal of this chapter is to create a canopy model from very basic technical
specs. The approach is to augment the specs with educated guesses about the
missing structure. The section profiles are defined by airfoils; the section
scales, positions, and orientations are defined by parametric functions. The
parametric functions should incorporate the available specs to produce the
completed geometry.

There are existing wing modeling tools that use wing sections, but most of
them (XFLR5, AVL, etc) assume you know the geometry as a set of explicit
points and perform linear interpolation between them; such tools are not
suitable for **generating** a wing geometry. This project needs to generate
the points using parametric function. There are modeling tools that can use
parametric functions (MachUpX, more?), but they use fixed choices for the
section reference points; this lack of flexibility pushes the structural
complexity into the parametric functions which makes them unnecessarily
complicated. So, this chapter starts by developing a novel geometry that
decouples the design curves and allows for much simpler parametric functions.

Creating a canopy model from basic spec data is thus broken into two steps:

1. Design a generalized geometry (which defines the points on the section
   surfaces) that decouples section scale, position, and orientation

   [[I kept struggling with this part; my tendency is to say "design
   a geometry that allows arbitrary functions instead of explicit points", but
   that's irrelevant: you could just evaluate those arbitrary functions to get
   the explicit points, in which case AVL et al could model it just fine.

   **The whole point is here is that we don't know the explicit points, so we
   need to create parametric functions that encode our assumptions, and those
   parametric functions have MUCH simpler forms if they are all decoupled.**]]

2. Design a set of a parametric functions that encode the domain knowledge to
   define the scale, position, and orientation from basic technical data.


Rough outline
=============

* What is a parafoil canopy?

* Why does this project need a model of the canopy?

  To estimate the inertial properties and aerodynamics.

* Why not use existing wing modeling tools?

  Most of them assume the wing geometry is already available as a set of
  points. For parafoils, we don't know the geometry: we need to **create** it
  using parametric functions, so we need a wing geometry that accepts
  functions to specify the design.

* Why not use existing wing modeling tools that accept functions?

  Although there are existing tools that accept functions instead of points,
  they include some unfortunate limitations. In particular, they use fixed
  reference points, which has the effect of coupling the design curves.
  Coupling structure between curves means they have to be designed
  simultaneously; redesigning one requires redesigning the others.

* Conclusion: we need a generalized geometry that accepts decoupled *design
  curves* to specify the complete geometry. This chapter starts by developing
  a generalized geometry model that decouples the design curves, then it
  presents some parametric functions that can combine the basic spec data with
  structural assumptions that complete the geometry definition.


.. Parafoil canopies

* Review what we need to model: describe the physical system


.. General equation

* To make it easier to design the parametric functions, we start by creating
  a generalized geometry in terms of scale, position, and orientation.

* Introduce the general equation

* This is my general model with fully decoupled parameters

* It computes points anywhere in each section coordinate system (typically the
  points will be on the chord, camber line, or profile).


.. Available data

* Review what we know: the basic technical specs

* Consider what structure we don't know: we'll have to model that somehow


.. Design curves

* This section designs some parametric functions that define the position,
  scale, and orientation variables of the general equation. For simplicity,
  I'm them *design curves*.

* The *design curves* encode the structure of the canopy geometry.

* The basic specs are missing a lot of information, so this section needs to
  design parametric functions that can combine what little data we know with
  some educated guess to "fill in" the missing structure and produce
  a complete geometry.

* First, consider what data is available. There are several sources:

  1. Technical specs

  2. Pictures

  3. Physical measurements

  The design curves should make it easy to utilize these sources.

* Present some convenient definitions: elliptical chords, etc


.. Examples

* Show how the design curves produce completed canopies


Content
=======

* We need a model of the canopy geometry to determine the inertial properties
  and the aerodynamics (forces and moments)

  The *inertial properties* of a wing refer to quantities like the total mass
  (which determines the wing's translational accelerations), the distribution
  of mass (which determine the wing's angular accelerations), volume, etc.

  The *aerodynamics* describe the forces and moments that are exerted on the
  object when it interacts with moving air.


* For this project, an approximate geometry is sufficient. It is not intended
  for detailed wing design, so it does not (currently) model details such as
  internal structure, cells, etc. It is intended to maximize simplicity while
  still being "accurate enough".

* Why does this project need a **complete** mathematical model?

  * Although there are elegant aerodynamics models, such as Prandtl's *linear
    lifting-line theory*, that estimate wing performance based on simple summary
    parameters (lift coefficient, efficiency factor, etc) instead of requiring
    a complete wing geometry, they are insufficient for this project:

    * They only apply to wings with straight wings. (Their results do not
      apply to the highly non-linear geometry of parafoil canopies.)

    * They only estimate the longitudinal dynamics (straight flight), and
      cannot be used to simulate turning dynamics or the presence of
      a crosswind.

    * They rely on linear aerodynamics that assume small angles of attack.
      Although canopy behavior is unpredictable near stall due to wing
      collapse, flight reconstruction requires a dynamics model with graceful
      degradation at higher than average angles of attack.

    * They provide the aerodynamic forces, but not the inertial properties.

  * Conclusion: a complete mathematical model of the canopy geometry is required
    to estimate the aerodynamics and inertial properties of a paraglider.

* Calling into external aerodynamics programs is too slow; we will need to use
  a library. I didn't find a suitable aerodynamics library, so I was going to
  need to create my own. If I'm using my own aerodynamics code, I'll need
  a geometry model to query the shape. Most existing geometry implementations
  are built into specific programs

* The advantage of the generalized model are:

  1. It allows specifying position using points other than the leading edge.

  2. It decouples the scale, position, and orientation parameters, which
     allows them to be designed independently.

  3. Because the parameters are decoupled, the generalized model makes it
     easier to design simple parametric functions that can incorporate the
     available data.

* What are the limitations of existing wing modeling tools that accept
  functions to define the geometry?

  * MachUpX: requires position to be specified using the leading edge (I think),
    defines positions using lengths (not absolute coordinates, so you have to
    integrate), has a funky definition for orientation, etc. 

  * Paraglider Design Handbook: IIRC this accepts a reference point, but it's
    the same for all dimensions? (Besides, the source is not written to be used
    by external programs, so its Fortran is hard to understand and extend.)

  * Benedetti's dissertation: uses the quarter-chord (besides, his source isn't
    available anyway)


* What's cool about my *general equation* is how it parametrizes the surface.
  It doesn't require you to specify any particular point (leading edge,
  quarter chord, etc): you can define the sections using whatever is the most
  convenient. **Arbitrary reference points fully decouple the design curves;
  that's what makes this so cool.** Splitting out structure into the choice of
  reference point lets you choose much simpler design curves. Many realistic
  wings can be created using mostly constant design "curves"; that's really
  cool!]]

* The conventional parametric approach to wing design is to use *wing
  sections*, which require specifying the scale, position, orientation, and
  profile of cross-sectional areas along the wing span. For the non-linear
  geometry of a parafoil canopy, specifying the scale/position/orientation for
  each section explicitly is unwieldy. Instead, it is more convenient to work
  with a set of *design parameters* (span, taper ratio, elliptical function
  parameters, etc) that capture the underlying structure of the model.
