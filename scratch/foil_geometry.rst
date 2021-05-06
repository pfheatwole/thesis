* Although a small amount of air does flow through the canopy's surface, the
  majority of the air flows around the canopy's volume.

* I'm choosing to neglect cell distortions, which is technically
  a big deal, but developing an aerodynamic method that accounts for cell
  billowing is time prohibitive. Should I simply punt that discussion into the
  aerodynamics section? Like "this geometry neglects details such as cell
  distortions. See 'foil_aerodynamics:Limitations' for a discussion." ?

* Do I like using "O" for the wing origin? It's basically the origin for the
  entire wing; my only gripe is that I don't like using "O" in math since it
  looks like a zero. Also, do I need a name for the origin of the chord
  surface?

* Wing origin offset: the chord surface uses it's own coordinate system,
  with its origin defined by the origins of the reference position curves.
  For the wing I'm defining origin as the leading edge of the central
  section. Thus, the chord surface positions an extra translation to get the
  coordinates in the wing's coordinate system. (If the central section has
  no geometric torsion then it's simply an x-offset `x(0) + r_x(0) * c(0)`,
  right?)

* Washin and washout have multiple purposes:

  * Control the spanwise tension (lateral) and loading (vertical)

  * Allow the designer to encourage more favorable stall patterns.
    (Specifically, a paraglider should start stalling the wing tip first.)

* "Wing tapering reduces the wing-root bending moments, since the inboard
  portion of the wing carries more of the wing's lift than the tip."

* You can affect the circulation distribution (and thus the induced drag) by
  manipulating the wing twist.


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


Overview 2 (2021-04-15)
=======================

This project needs a mathematical model of the canopy geometry in order to
estimate the canopy aerodynamics. The problem is that complete specifications
of commercial paraglider canopies are not available; manufacturers only
provide summary specs. To create approximate models from the summary specs
must be combined with domain expertise to "fill in the blanks" with reasonable
guesses of the missing information. The domain expertise is encoded in
parametric functions; the parameters are either the summary specs or other
relatively available information, and the function encodes the assumed
structure.

So, we need a geometry model that accepts parametric functions. This is
a problem because although there are wing modeling tools expect the wing
geometry to be specified in unnecessarily constrained ways. Those constrains
force unnecessary complexity into the parametric functions and make it
difficult to create clean design curves.

To that end, this chapter has two goal. First, it will develop a generalized
wing model that places fewer constraints on how the wing is specified; this
flexibility allows significantly simpler parametric design curves. Second, it
will provide several convenient design curves that capture most of the missing
structure using reasonable assumptions based on typical canopy design.


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


Geometry specification
----------------------

* [[There are also a variety of standard terms I will avoid due to ambiguity:
  *planform*, *mean aerodynamic chord*, maybe more? For *planform*, most texts
  assume the wing is flat and so the projected area is essentially equal to
  the flat area, and thus differentiating the two is largely neglected in
  standard aerodynamic works. The mean aerodynamic chord is a convenient
  metric for comparing flat wings and for simplifying some equations, but for
  wings with significant arc anhedral I'm not sure how beneficial this term
  really is; it's a mistake to compare wings based on the MAC alone, so I'd
  rather avoid any mistaken comparisons.]]

* Technically, for flat wings curvature in the yz-plane is is described as
  *dihedral* or *anhedral*: not sure how to define this for a wing. If the
  wing is straight, then it's traditionally defined as `arctan(z/y)` of the
  section position, but that's pretty unhelpful for a paraglider. It also
  doesn't differentiate between `arctan(z/y)` and `arctan(dz/dy)` of
  a section. Still, discussing curvature leads nicely into a discussion of the
  *arc*, so whatever.


Points on chords
----------------

[[I've kept this because it tickles my brain in a pleasant way, but should
probably be removed.]]

Points on the section chords have particularly simple equations. For some
point :math:`P` at some ratio :math:`0 \le r \le 1` along the section chord:

.. math::

   \begin{aligned}
   \vec{r}_{P/O}^f
     &= \vec{r}_{LE/O}^f + \vec{r}_{P/LE}^f\\
     &= \vec{r}_{LE/O}^f - \vec{r}_{LE/P}^f\\
     &=
        \left(
          \vec{r}_{\mathrm{RP}/\mathrm{O}}^f
            + \mat{R} \mat{C}_{f/s} c\, \hat{x}^s_s
        \right)
        - r\, \mat{C}_{f/s} c\, \hat{x}^s_s\\
   \end{aligned}

Which simplifies to:

.. math::
   :label: chord_points

   \vec{r}_{P/O}^f =
      \vec{r}_{\mathrm{RP}/\mathrm{O}}^f
      + \left(\mat{R} - r\right) \mat{C}_{f/s} c\, \hat{x}^s_s

All the notational baggage can make this equation look more complicated than
it really is. Suppose the points on the chord are simply :math:`\left\langle
x, y, z \right\rangle` in canopy coordinates, the reference points in canopy
coordinates are :math:`\vec{r}_{RP/O} = \left\langle x_r, y_r, z_r
\right\rangle`, and :math:`\mat{K} = \left(\mat{R} - r\right) c`, then the
structure is easier to see:

.. math::
   :label: simplifed_chord_points

   \left\langle x, y, z \right\rangle =
      \left\langle x_r, y_r, z_r \right\rangle
      + \mat{K} \hat{x}_s^f

Or, using separate equations instead of matrix math:

.. math::

   \begin{aligned}
   x &= x_r + (r_x - r) \hat{x}^f_x\\
   y &= y_r + (r_y - r) \hat{x}^f_y\\
   z &= z_r + (r_z - r) \hat{x}^f_z
   \end{aligned}


