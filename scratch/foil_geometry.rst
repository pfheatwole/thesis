* Wing origin offset: the chord surface uses it's own coordinate system,
  with its origin defined by the origins of the reference position curves.
  For the wing I'm defining origin as the leading edge of the central
  section. Thus, the chord surface positions an extra translation to get the
  coordinates in the wing's coordinate system. (If the central section has
  no geometric torsion then it's simply an x-offset `x(0) + r_x(0) * c(0)`,
  right?)

* The aerodynamics can be estimated using a variety of aerodynamics models
  that depend on different aspects of the shape, but in general they all use
  points from either the chord surface, the camber surface, or the profile
  surface; to support the variety of aerodynamic methods, the model should
  return points on any of the three surfaces.






.. Describe the visible characteristics/details of the canopy

   These details capture the visible structure of a parafoil, and thus are
   intuitive starting points for parametrizing a parafoil, but don't confuse
   the characteristic with its representation (eg, arc versus dihedral angle).

The most striking detail of a parafoil's shape is its characteristic spanwise
curvature, called the *arc* :cite:`lolies2019NumericalMethodsEfficient` (also
known as the *lobe* :cite:`casellasParagliderDesignHandbook`); the arc plays
a major role in wing stability, maneuverability, and efficiency. Another
important characteristic is the continuously variable tapering of the section
lengths from the center of the wing out to the tips, which impacts aerodynamic
efficiency, canopy weight, and stall behavior. A third important detail is how
the front ("leading") and rear ("trailing") edges are offset in the fore-aft
direction.

To manufacture a parafoil, nylon panels are stitched together to form upper
and lower surfaces, whose different curvature and length is fundamental for
generating aerodynamic lift. The panels are stitched to internal support
structures calls *ribs*, and the spaces between the ribs are visible as
a sequence of *cells*. The majority of the cells are open near their leading
edges, forming the *air intakes*. In addition to these fundamental details,
commercial wings employ a wide variety of techniques to improve wing
stability, performance, and reliability, such as partial ribs, diagonal ribs,
horizontal straps, structural reinforcement rods, etc. The deceptively simple
appearance of a parafoil belies a sophisticated aircraft dominated by subtle
details.





Introduction
============

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

* There are existing wing modeling tools that use wing sections, but most of
  them (XFLR5, AVL, etc) assume you know the geometry as a set of explicit
  points and perform linear interpolation between them; such tools are not
  suitable for **generating** a wing geometry. **This project needs to
  generate the points from the summary specs using parametric functions.**
  There are modeling tools that can use parametric functions (MachUpX, more?),
  but they use fixed choices for the section reference points; this lack of
  flexibility pushes the structural complexity into the parametric functions
  which makes them unnecessarily complicated. So, this chapter develops
  a novel geometry that decouples the design curves and allows for much
  simpler parametric functions.




Modeling requirements
=====================

* Review what we need to model: describe the physical system

* Review what we know: the basic technical specs

* Consider what structure we don't know: we'll have to model that somehow

* For this project, an approximate geometry is sufficient. It is not intended
  for detailed wing design, so it does not (currently) model details such as
  internal structure, cells, etc. It is intended to maximize simplicity while
  still being "accurate enough".

* I'm choosing to neglect cell distortions, which is technically
  a big deal, but developing an aerodynamic method that accounts for cell
  billowing is time prohibitive. Should I simply punt that discussion into the
  aerodynamics section? Like "this geometry neglects details such as cell
  distortions. See 'foil_aerodynamics:Limitations' for a discussion." ?



Parametric modeling with wing sections
======================================

.. Explicit vs parametric geometries

[[For wing models, explicit geometries are also less convenient to analyze,
since they are difficult to decompose.]]



.. Advantages of parametric geometries

Parametric models offer a variety of advantages:

* They can be generated small small amounts of data. [[This is the most
  important feature for this project, since I only have basic summary data.]]

* They are low-dimensional representations, which makes them more amenable to
  mathematical optimization methods. This is helpful for wing performance
  optimization and statistical parameter estimation.

* They make it much easier to place statistical priors over model
  configurations. [[You can probably build a metric for comparing explicit
  geometries, but it would be tough.]]

  It's important that I reduce the effort to model existing wings because
  I need a representative set of models to deal with model uncertainty.

  Flight reconstruction requires a model of the wing that produced the
  flight, but due to model uncertainty the estimate must use an entire
  distribution over possible wing configurations. [[You'll still probably
  need to use a "representative set" of models (parameter estimation is
  likely a pipedream given the available data), but at least parametric
  models make it MUCH easier to *create* that representative set from the
  limited available data on existing wings.]]



.. Define the functional goals of the canopy model parametrization

* [[Define *parametrization*]]

* [[Some parametrizations are better than others.]]

* Parametric designs try to balance simplicity and expressibility. A good
  parametrization lets you focus on high-level design without forcing you
  into simplistic designs. **The goal is to find a set of simple parametric
  functions that combine to capture the complex structure of the wing.**

* [[The choice of parametrization affects how useable it is. What would make
  a good parametrization?]]

  * Some goals of a parametrization:

    * Capable of capturing the most important details (as simple as possible,
      but no simpler)

    * Intuitive

    * Preferably map easily onto the most readily-available summary values
      (like span). It needs to make it easy to work with available wing data
      (technical specs, measurable quantities like flat span, etc).

  * When I say a good parametrization should be *intuitive*, I mean that it
    should match what you notice when you glance at a wing. The arc, the
    width, and the way the leading edge sweeps backwards are probably the most
    obvious. Or maybe you notice the trailing edge more; whatever you notice
    is what I mean by "intuitive".

  * The choice of parametrization is influence by what details you want to be
    able to represent / capture. The final model will be an approximation of
    the real wing, so you need to decide up from what details you want to
    capture (and thus what details you're happy to lose).

  * You should be able to specify the design target directly. If you want
    to position a particular part of the wing at a particular position, you
    should be able to say that explicitly without needing to translate (eg, if
    you want to position the trailing edge you shouldn't be required to
    describe it in terms of the chord length, orientation, and leading edge
    position).

  * Design parameters should be independent. You shouldn't need to change one
    to satisfy another. This is directly related to the idea of "specifying
    each target directly". How you position a section should be independent of
    the chord length or how you orient that section.


.. Wing sections

[[In addition to design convenience, building a wing from 2D cross-sections
also provides computational benefits for estimating the aerodynamic
performance of the 3D wing, as discussed in :ref:`foil_aerodynamics:Section
Coefficients`.]]

Advantages of designing with *wing sections*:

1. They hide a lot of the geometric complexity.

2. They enable analyzing the 2D sections independently from the 3D wing. It's
   not a perfect match, but you have a lot of control over the final 3D
   aerodynamics by choosing the 2D profiles.

3. You can precompute the section coefficients, thus saving a ton of time when
   solving the 3D flow field (especially if viscous effects are included).



Basic model
===========

* The conventional parametric approach to wing design is to use *wing
  sections*, which require specifying the scale, position, orientation, and
  profile of cross-sectional areas along the wing span. For the non-linear
  geometry of a parafoil canopy, specifying the scale/position/orientation for
  each section explicitly is unwieldy. Instead, it is more convenient to work
  with a set of *design parameters* (span, taper ratio, elliptical function
  parameters, etc) that capture the underlying structure of the model.



Expanded model
==============

* The advantage of the expanded model are:

  1. It allows specifying position using points other than the leading edge.

  2. It decouples the scale, position, and orientation parameters, which
     allows them to be designed independently.

  3. Because the parameters are decoupled, the generalized model makes it
     easier to design simple parametric functions that can incorporate the
     available data.

* What's cool about my *general equation* is how it parametrizes the surface.
  It doesn't require you to specify any particular point (leading edge,
  quarter chord, etc): you can define the sections using whatever is the most
  convenient. **Arbitrary reference points fully decouple the design curves;
  that's what makes this so cool.** Splitting out structure into the choice of
  reference point lets you choose much simpler design curves. Many realistic
  wings can be created using mostly constant design "curves"; that's really
  cool!]]



Simplified model
================



Design curves
=============

* This section designs some parametric functions that define the position,
  scale, and orientation variables of the general equation..

* The *design curves* encode the structure of the canopy geometry.

* First, consider what data is available. There are several sources:

  1. Technical specs

  2. Technical reviews

  3. Pictures and video

  4. Physical measurements

  The design curves must make it easy to utilize these sources.

* Present some convenient definitions: elliptical chords, etc

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


Examples
========

* Show how the design curves produce completed canopies

* Should I provide the parameters of the design curves? Might be nice to
  highlight their simplicity.



MISC
====

* The *inertial properties* of a wing refer to quantities like the total mass
  (which determines the wing's translational accelerations), the distribution
  of mass (which determine the wing's angular accelerations), volume, etc.

  The *aerodynamics* describe the forces and moments that are exerted on the
  object when it interacts with moving air.

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


Foil design
-----------

* Washin and washout have multiple purposes:

  * Control the spanwise tension (lateral) and loading (vertical)

  * Allow the designer to encourage more favorable stall patterns.
    (Specifically, a paraglider should start stalling the wing tip first.)

* "Wing tapering reduces the wing-root bending moments, since the inboard
  portion of the wing carries more of the wing's lift than the tip."

* You can affect the circulation distribution (and thus the induced drag) by
  manipulating the wing twist.


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
