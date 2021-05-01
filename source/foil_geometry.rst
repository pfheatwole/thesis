.. This chapter generalizes the typical foil geometry equation to allow
   arbitrary reference points, relaxing the constraint that the geometry is
   specified in terms of the leading edge. This additional flexibility allows
   complex geometries to be described using simple parametric design curves.
   The parametric design curves encode domain expertise (reasonable
   assumptions about typical foil design), thus enabling complete parafoil
   geometries to be specified using only summary technical specifications.


*************
Foil geometry
*************

.. What is a foil?

The essential components of any flying object are the *lifting surfaces*. By
redirecting airflow downward, a lifting surface exchanges momentum with the
air and produces the lifting force that allows the object to fly.

In this chapter, the lifting surface of an aircraft will be referred to as
a *foil* instead of using the conventional terms *wing* or *canopy* (for
traditional aircraft or parafoils, respectively). This unconventional term was
chosen to avoid two generalization issues. First, although *wing* is the
conventional term for the primary lifting surfaces of non-rotary aircraft, the
paragliding community uses the term *paraglider wing* to reference not only
the lifting surface but also the supporting structure connected to it, such as
suspension lines, risers, etc. Second, although this project is primarily
concerned with parafoils, the model developed in this chapter is not limited
to parafoil canopies.


.. Why does this project need to model the foil geometry?

This chapter is motivated by the need to develop dynamics models for
commercially manufactured paraglider wings. Two key components of the dynamics
are the inertial properties and aerodynamics of the canopy, which can be
estimated from the foil's shape.


.. Why not use an existing foil geometry model?

An accurate model of a foil's shape requires a detailed set of specifications,
but those are unavailable for commercial paraglider wings. User manuals
provide valuable summary information in the form of basic technical
specifications, but the majority of the foil structure is unspecified, so
completing a model requires making educated assumptions about that unknown
structure. Those assumptions are encoded in parametric *design curves* that
extend the technical data with domain expertise to produce a fully specified
model.


.. The geometry model chooses the variables, which in turn determines the
   structure of the functions that define those variables.

Parafoil canopies have fundamental complexity that must be captured, either in
the model structure or in the design curves. Unfortunately, existing foil
geometry models are inflexible, making strong assumptions about how the foil
is most conveniently defined. The inflexibility of a simplistic geometry model
forces the remaining complexity into the design curves. This unnecessary
complexity makes it difficult to describe a parafoil using simple design
curves: they must not only encode the fundamental structure, they must also
convert that structure into the variables that define the geometry model.
Instead of the geometry model adapting to the needs of the design curves, the
design curves must adapt to the limitations of the geometry model.

The solution developed in this chapter is to reject the assumption that
predefined reference points are the most convenient way to position the
elements of a parafoil surface. The result is a novel foil geometry that fully
decouples the design curves, allowing each aspect of the foil geometry to be
designed independently, plus a simplified geometry model that eliminates most
of the additional complexity of the expanded model. The simplified model is
both flexible and intuitive for designing highly nonlinear foil geometries
such as paraglider canopies. In particular, it [[solves]] the problem of
creating parafoil canopy models from basic technical specifications.


.. Roadmap

   1. Discuss the physical system being modeled and its important details

   2. Review the incomplete geometry information from the readily available
      sources like technical specs, physical wing measurements, and pictures

   3. Consider how to create a complete geometry from the incomplete
      information by encoding domain expertise in parametric functions.

   4. Introduce parametric modeling using *wing sections*.

   5. Develop the direct (basic) implementation of a foil geometry based on
      wing sections (that uses the leading edge as the fixed reference point),
      and review the limitations produced by fixed reference points.

   6. Expand the basic equation to allow arbitrary reference points.

   7. Simplify the expanded model to eliminate the extra complexity (make
      reasonable assumptions about typical foil structure, such as defining
      the reference points using positions on the section chords, assuming the
      sections are perpendicular to the yz-curve, etc)

   8. Show some examples using the new geometry model using *design curves*:
      parametric functions that encode the underlying structure of parafoil
      canopies using basic parameters that can be estimated from the available
      information (or from reasonable assumptions)

   9. Demonstrate using the model to recreate a parafoil from literature.

   10. Discussion



Modeling requirements
=====================

[[These are the modeling requirements of **THIS PROJECT**. Explain what I'm
trying to model, typical specifications of such a geometry, the missing
structure I need to encode in parametric functions. Those needs drive the
requirements for the geometry model.]]

The geometry that results happens to be pleasantly general, and useful in
other contexts, but this section is explicitly interesting in establishing
what tool we need to create foil geometry models of parafoils.]]


Foil specifications
-------------------

.. This section must:

   1. Draw attention to the important details of the foil geometry that must
      be modeled (chord distribution, arc, etc)

   2. Introduce the available specification data (span, flat span, area, etc).

   3. Highlight the missing information (what we need to model versus what we
      know) and consider what is required to produce a complete model from
      this minimal data?


.. Describe the system we need to model

A parafoil canopy is a type of *ram-air parachute*. It uses air intakes at the
front of the wing to inflate a partially-open nylon casing. Although a small
amount of air does flow through the canopy's surface, the majority of the air
flows around the canopy's volume. [[FIXME: reword]]

.. figure:: figures/paraglider/geometry/Wikimedia_Nova_X-Act.jpg
   :width: 75%

   Paraglider side view.

   `Photograph <https://www.flickr.com/photos/69401216@N00/2820146477/>`__ by
   Pascal Vuylsteker, distributed under a CC-BY-SA 2.0 license.

Manufactured from flexible materials such as ripstop nylon, they rely on
internal structures to control the shape of the inflated volume, and
variable-length suspension lines to control the shape of the arc.


* [[Call attention to the important details:

  * *arc* :cite:`lolies2019NumericalMethodsEfficient` (also known as the
    *lobe* :cite:`casellasParagliderDesignHandbook`)

  * Nonlinear leading edge (the wings are not straight)

  * Variable chord lengths

  * *geometric torsion*: relative pitch angle of a section

    .. figure:: figures/paraglider/geometry/airfoil/geometric_torsion.*

       Geometric torsion.

       Note that this refers to the angle, and is the same regardless of any
       particular rotation point.

  * Cells

* [[These details are important because they are the basis for recognizing the
  underlying structure of the wing, and thus they are intuitive starting
  points for parametrizing representations. However, don't confuse these these
  characteristics with how you **represent** them (eg, arc versus dihedral
  angle).]]


.. Describe the quantitative information we can reasonably attain

* [[Parafoil canopies are typically described using terminology from classical
  wing design: surface area, span, and aspect ratio.

  Define the difference between *flat* and *projected* values.]]


.. Discuss the difficulty of modeling a parafoil from such limited data

* [[The user manual for a wing usually includes basic properties such as the
  total mass of the wing, the areal densities of its surface materials, etc,
  but not the mass and volume distributions, aerodynamics, etc.]]


* [[These specifications are are structural summaries, and are not sufficient
  to create a wing model. Creating a model from such sparse information will
  rely on many simplifications. Explain which details are important to this
  paper, and which will be ignored. **The rest of this chapter is interested in
  using what little we know to build the approximate model.**

  These are not necessarily the variables you would choose to parametrize the
  geometry; they might simply be helpful for discussing/understanding the shape
  of a canopy. For example, "anhedral" is ambiguous, so I'm using Euler roll
  angles for section "anhedral". These are here to establish the details of the
  shape and thus the flexibility required by the parametrization.

  Related: "General aviation aircraft design" (Gudmundsson; 2013), chapter 9:
  "Anatomy of a wing"]]


Foil model
----------

.. This section must:

   1. Establish which aspects of the geometry must be captured (and which will
      be ignored).

   2. Establish the functionality of the geometry model (ie, what queries must
      it suport for computing inertial properties and aerodynamics)

   3. Establish the need to augment the foil specification data with domain
      expertise via parametric functions (so the model must allow "good"
      design curves).


.. Choose what geometry details to include and which to ignore

* [[This section must establish which aspects of the geometry are worth
  modeling (what parts of the canopy will be modeled and which will be
  ignored). Unfortunately that question is tied to the aerodynamics method.

  For example, I'm choosing to neglect cell distortions, which is technically
  a big deal, but developing an aerodynamic method that accounts for cell
  billowing is time prohibitive. Should I simply punt that discussion into the
  aerodynamics section? Like "this geometry neglects details such as cell
  distortions. See 'foil_aerodynamics:Limitations' for a discussion." ?]]


.. Functionality

* A geometry model is necessary to estimate the inertial properties and
  aerodynamics of the wing.

* The inertial properties depend on the distribution of mass. For a parafoil,
  the masses are the *solid mass*, from the structural materials, the *air
  mass*, from the air enclosed in the wing, and the *apparent mass*, from the
  acceleration of the wing relative to the surrounding air.

  This chapter does not deal with how to compute the masses and their
  inertias, but to support their calculation the model must return points on
  the profile surface.

  [[**FIXME**: I haven't defined *surface* yet.]]

* Different aerodynamic codes use different aspects of the shape, but in
  general they all use points from either the chord surface, the camber
  surface, or the profile surface.

  To support the variety of aerodynamic methods, the model should return
  points on any of the three surfaces.


.. Parametrization

* [[The primary motivation of a parametric model is the need to "fill in the
  gaps" of the available technical specs using domain expertise. The secondary
  motivation is to reduce the degrees of freedom, making it (1) easier for an
  end user to specify a design, and (2) to (theoretically) enable
  optimizations methods (either for design optimization or statistical model
  identification).]]

* The model is intended to assist in reconstructing flights recoded by real
  wings, so it must be able to represent existing wings with sufficient
  accuracy. [[The primary purpose of the model is "useable accuracy with
  minimal effort"; it's not intended as a detailed wing design tool, so no
  ribs, distortions, etc.]]


* Parafoil canopies are relatively complex shapes, and can be time consuming
  to describe in detail. To reduce design effort, the model should provide
  a concise set of *design parameters* (span, taper ratio, etc) that directly
  capture the fundamental structure of the wing. [[the *design curves* are the
  parametric functions; should define those clearly somewhere]]

  One goal of this geometry is to make it as easy as possible to produce
  models of existing wings, which means the choice of parameters should allow
  a designer to use existing available data (technical specifications,
  pictures, and physical measurements) as directly as possible. [[This
  includes supporting mixed flat/inflated design; it can be more convenient to
  specify some structure in terms of the non-inflated wing.]]

  [[Secondary reason for minimizing the number of parameters: a lower
  dimensional representation of the wing has advantages for mathematical wing
  optimization and statistical parameter estimation.]]

* [[Nice to have: flexible enough to handle deformations (cell billowing,
  braking, weight shifting, accelerator flattening, C-riser piloting, etc)]]

* [[I might want to informally describe an "ideal" design workflow, and refer
  to that workflow when critiquing geometry model parametrizations.]]


Parametric modeling
===================

.. Parameters are how you specify the design. Motivate parametric models (as
   opposed to explicit geometries), define "parametrization", and establish
   the importance of choosing a good parametrization.

* [[To define a geometry, you either specify a set of points explicitly or you
  specify the parameters of parametric functions that generate the points.]]

* [[Define *explicit geometry*: specifying variable values directly]]

* [[Modeling with explicit geometries is too expensive (time consuming to
  specify, require too much information about the wing, difficult to analyze
  with simple aerodynamics, etc)]]

* [[Define *parametric geometry*: specifying variables values using parametric
  functions which are defined in terms of *design parameters*]]

* [[Advantages of parametric geometries]]

  * Parametric equations are designed to capture the structural knowledge of
    the shape. If a complex shape can be represented with parametric
    equations, then the parameters "summarize" the structure. Each parameter
    communicates more information than an explicit coordinate, so fewer
    parameters are required, and less work is required to specify a design.

    Parametric designs try to balance simplicity and expressibility. A good
    parametrization lets you focus on high-level design without forcing you
    into simplistic designs. **The goal is to find a set of simple parametric
    functions that combine to capture the complex structure of the wing.**
    [[I'm interested in "easy to create, good enough" approximations of real
    wings, not physically-realistic simulations.]]

  * Parametric models let you standardize so you can compare models.

  * Parametric models are low-dimensional representations, which makes them
    more amenable to mathematical optimization methods. This is helpful for
    statistical parameter estimation, or wing performance optimization.

  * Parametric models make it much easier to place priors over model
    configurations. (You can probably build a metric for comparing explicit
    geometries, but it would be tough.)

    It's important that I reduce the effort to model existing wings because
    I need a representative set of models to deal with model uncertainty.

    Flight reconstruction requires a model of the wing that produced the
    flight, but due to model uncertainty the estimate must use an entire
    distribution over possible wing configurations. [[You'll still probably
    need to use a "representative set" of models (parameter estimation is
    likely a pipedream given the available data), but at least parametric
    models make it MUCH easier to *create* that representative set from the
    limited available data on existing wings.]]

  * Building a wing from 2D cross-sections also provides computational
    benefits for estimating the aerodynamic performance of the 3D wing, as
    discussed in :ref:`foil_aerodynamics:Section Coefficients`.

    [[Maybe link forward to :ref:`foil_aerodynamics:Case Study`, where
    I implement Belloc's wing using this parametric geometry.]]


.. Define the functional goals of the canopy model parametrization

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


Basic model
===========


Wing sections
-------------

.. Introduce designing a wing using "wing sections". They're the conventional
   starting point for parametrizing a wing geometry (airfoil curves capture the
   structure of the section profiles). Choosing to define the surfaces using
   points in the wing sections establishes the general form of the parametric
   model.

.. See `notes-2020w47:Canopy parametrizations` for a discussion

[[The standard way to parametrize a foil geometry is to describe it in terms
of *wing sections*. Each section is assigned a 2D cross-sectional profile,
called an *airfoil*, which is scaled, positioned and oriented to produce the
*section profile*. Together, the set of section profiles produce a continuous
surface that defines the complete 3D volume.

Related work:

* :cite:`abbott1959TheoryWingSections`

* :cite:`bertin2014AerodynamicsEngineers`, Sec:5.2


.. Define the relevant details of airfoils

[[Before I can refer to terms like "chord surface", "mean camber surface",
etc, I need to define "chord, "mean camber line", etc. Define the airfoil
geometry: leading edge, trailing edge, chord, mean camber line, thickness
distribution, thickness convention, etc.]]

.. figure:: figures/paraglider/geometry/airfoil/airfoil_examples.*

   Airfoils examples.

An airfoil is defined by a camber line, a thickness function, and a thickness
convention. [[FIXME: This is just one specific way to defining the profile
curve; you could just as easily provide an explicit set of points.]]

Here's a diagram of the basic airfoil geometric properties:

.. figure:: figures/paraglider/geometry/airfoil/airfoil_diagram.*
   :name: airfoil_diagram

   Components of an airfoil.

There are two conventions measuring the airfoil thickness; this convention
also determines what point is designated the *leading edge*. The leading and
trailing edge of a wing section are arbitrary points that define the *chord*;
the chord is used to nondimensionalize the airfoil geometry and define the
local *angle of attack*.

.. figure:: figures/paraglider/geometry/airfoil/NACA-6412-thickness-conventions.*
   :name: airfoil_thickness

   Airfoil thickness conventions.


[[**The choice of convention is irrelevant. The only thing that matters is
that you manufacture the wing with the sections scaled and oriented in exactly
the same way as they were defined.** For example, you could define the chord
with any two points on the surface; it would be confusing, and you could end
up with a usable range of alpha from, like, 53 to 70 degrees, but as long as
you mount the section oriented correctly it's irrelevant. The convention does
two things: (1) it disambiguates the orientation of the profile relative to
freestream associated with the coefficients, and (2) standardizes the
orientation so you can easily swap out different profile definitions.]]



The wing design process is thus decomposed into two steps:

1. Specify the scale, position, and orientation of each section

2. Specify the airfoils at each section to define the section profiles, which
   define the three surfaces: the *chord surface*, the *mean camber surface*,
   and the *profile surface*.

[[Gudmundsson says wing design is about designing two 2D components: the
*planform* and the *profile*, so his idea of "planform" matches my idea of
a chord surface, except that my "chord surface" is more like a 2D manifold in
3D (it's not restricted to a plane), plus it doesn't provide orientation.]]

.. figure:: figures/paraglider/geometry/wing_sections2.svg

   Wing section profiles.

   Note that section profiles are not the same thing as the ribs of a parafoil.
   Parafoil ribs are the internal structure that produce the desired section
   profile at specific points along the span.

Advantages of designing with *wing sections*:

1. They hide a lot of the geometric complexity.

2. They enable analyzing the 2D sections independently from the 3D wing. It's
   not a perfect match, but you have a lot of control over the final 3D
   aerodynamics by choosing the 2D profiles.

3. You can precompute the section coefficients, thus saving a ton of time when
   solving the 3D flow field (especially if viscous effects are included).


Basic equation
--------------

.. Introduce the basic equation that uses `r_LE/O`

Choosing to model a foil using *wing sections* means that the wing surfaces
are defined by 2D airfoils.

By convention, airfoil coordinates are defined in an airfoil-local coordinate
system whose origin is at the leading edge. To create the section profile, the
airfoil coordinates must be converted into a section-local coordinate system,
scaled, positioned, and oriented. The natural choice is to share the origin
between the airfoil and section coordinate systems, and specify the section's
position using the leading edge.

First, let :math:`\mathrm{P}` represent any point in a wing section (such as
points on the section chords, mean camber lines, or profiles), and
:math:`\mathrm{LE}` be the leading edge of that section. In the `notation
<_common_notation>`_ of this paper, a general equation for the position of
that point :math:`\mathrm{P}` with respect to the foil origin
:math:`\mathrm{O}`, written in terms of the foil coordinate system :math:`f`,
is:

.. Unparametrized (explicit geometry?) equation

.. math::

   \vec{r}_{\mathrm{P}/\mathrm{O}}^f = \vec{r}_{P/LE}^f + \vec{r}_{LE/O}^f

In this chapter, foil geometries are expected to be symmetric, with the
central section designated the foil *root*. The foil inherits the coordinate
system defined by the root section. Points in section (local) coordinate
systems :math:`s` must be rotated into the foil (global) coordinate system.
Given the *direction cosine matrix* :math:`\mat{C}_{f/s}` between the section
and foil coordinate systems, position vectors in foil coordinates can be
written in terms of section coordinates:

.. math::

   \vec{r}_{P/LE}^f = \mat{C}_{f/s} \vec{r}_{P/LE}^s

Because airfoil curves are defined in airfoil coordinates, another
transformation is required, from airfoil coordinates to section coordinates.
The convention for airfoil coordinates places the origin at the leading edge,
with the x-axis pointing from the leading edge to the trailing edge, and the
y-axis oriented towards the upper surface. This paper uses a front-right-down
convention for the 3D section coordinates, so the 2D airfoil coordinates can
be transformed into 3D section coordinates with a matrix transformation:

.. math::

   \mat{T}_{s/a} \defas \begin{bmatrix}
      -1 & 0 \\
      0 & 0\\
      0 & -1
   \end{bmatrix}

Next, the airfoil must be scaled. By convention, airfoil geometries are
normalized to a unit chord, so the section geometry defined by the airfoil
must be scaled by the section chord :math:`c`. Writing the points in terms of
scaled airfoil coordinates:

.. math::

   \vec{r}_{P/LE}^f = \mat{C}_{f/s} \mat{T}_{s/a} \, c \, \vec{r}_{P/LE}^a

.. This is the suboptimal "general" parametrization

The complete general equation is then:

.. math::

   \vec{r}_{\mathrm{P}/\mathrm{O}}^f =
     \mat{C}_{f/s} \mat{T}_{s/a} \, c \, \vec{r}_{P/LE}^a
     + \vec{r}_{LE/O}^f

In this form it is clear that a complete geometry definition requires
definitions of four variables:

1. Scale: :math:`c`

2. Position: :math:`\vec{r}_{LE/O}^f`

3. Orientation: :math:`\mat{C}_{f/s}`

4. Profile: :math:`\vec{r}_{P/LE}^a`


Expanded model
==============

.. Generalize the basic equation by decomposing `r_LE/O = r_LE/RP + r_RP/O`

[[Although the basic equation is enough to describe any wing composed of
continuous design curves (I think), its simplicity means the complexity is
pushed into the design curves. A dramatic improvement is to allow each section
to be positioned using arbitrary reference points instead of the section
leading edges. This extra flexibility allows much simpler parametric forms.]]

[[The "basic equation" is an explicit, mathematical representation of the
standard approach to wing modeling used by most tools. (Well, sort of: most
tools use a parametrized version of it; for example, you can usually specify
twist as an Euler angle.) It is general but unwieldy, since the model must be
specified in terms of the leading edge. The real magic happens when `r_LE/O`
is decomposed so it can be specified using an arbitrary reference point;
that's the part that introduces the flexibility that enables simplified
parametric functions.]]



[[Elaborate on why requiring the position to be specified in terms of the
leading edge is suboptimal. **The key problems are that 1) you can't specify
the geometry in the simplest way, and 2) it couples the design curves.** This
is where I make my stand that existing tools are suboptimal, which is why it
gets its own section.]]


Instead of requiring section positions to be specified in terms of section
leading edges, decompose them into two vectors: one from the section origin
(the section leading edge) to some arbitrary *reference point* :math:`RP`, and
one from the reference point to the foil origin:

.. math::
   :label: expanded-model-equation

   \vec{r}_{LE/O}^f = \vec{r}_{LE/RP}^f + \vec{r}_{RP/O}^f

Where `RP` are as-yet nebulous "reference points" and :math:`\vec{r}_{RP/O}^f`
is defined by the *design curves* (`x(s)` and `yz(s)`, in my case). This lets
you choose reference points other than the leading edges, and position those
points explicitly in the wing coordinate system. (Note that the leading edges
remain the origin of the section coordinate systems.)




Simplified model
================

.. The expanded model has the necessary flexibility, but it's too difficult
   too use because it has too many parameters: scale (1), reference point (3),
   position (3), and orientation (3).

   This section applies some reasonable assumptions to simplify defining all
   those parameters. It goes from 10 free parameters (not counting choice of
   airfoil) down to 7. Equally as important, it provides a clever parametric
   reference point that decouples the design curves.

.. Chooses a definition of the section index; defines independent reference
   points for x, y, and z; sets `r_y = r_z`; defines the section DCM using
   `dz/dy` and `\theta` (so you design `theta(s)` and `yz(s)` instead of
   specifying the section DCM directly).


[[FIXME: should I explicitly acknowledge that this "simplified" model was
tailored for specifying parafoils? The "perpendicular to yz" does make it
incompatible with stuff like fighter jet delta wings, etc. Earlier in the
chapter I claimed that nothing in this chapter is specific to parafoil
canopies, but this chapter violates that claim.]]


[[Remember, the goal of designing this model was to enable simple parametric
design curves to complete the model from basic technical specs. The airfoil
curves parametrize the surface points, now I need to parametrize the layout
(scale, position, and orientation).]]


[[The final step to making a foil geometry model that is both flexible and
convenient is to simplify the equation by making reasonable assumptions about
the foil structure.]]


.. math::

   \vec{r}_{LE/RP}^f = \mat{R} \mat{C}_{f/s} c\, \hat{x}^s_s

.. math::

   \mat{R} \defas \begin{bmatrix}
      r_x & 0 & 0\\
      0 & r_{yz} & 0\\
      0 & 0 & r_{yz}
   \end{bmatrix}

Where:

* `xhat = [1, 0, 0]^T` (the chord lies along `xhat`)

* `0 <= r_x, r_y, r_z <= 1` (proportions of the chord)

[[FIXME: explain, in general, the `R = diag(r_x, r_y, r_z)`]]

[[The simplified equation given these choices is then:

.. math::

   \begin{aligned}
   r_{P/O}^f
     &= r_{P/LE}^f
        + r_{LE/RP}^f
        + r_{RP/O}^f \\
     &= \mat{C}_{f/s} \mat{T}_{s/a} \vec{r}_{P/LE}^a
        + \mat{R} \mat{C}_{f/s} c\, \hat{x}^s_s
        + \vec{r}_{RP/O}^f
   \end{aligned}


To design a wing, specify: `c`, `C_f/s`, `r_P/LE`, `R`, and `r_RP/O`. **This
is almost exactly the same amount of work as before, you only need to add
`R`.** Minimal extra effort for a lot of convenience.]]

[[FIXME: define `C_f/s` here? I think I need to. Hrm, or actually, I should
finish the general equation without simplifying it too much, so keep things
like `R = diag(r_x, r_y, r_z)`. Choosing `r_y = r_z` should be explained
together with choosing to use `arctan(dz/dy)` to define the section roll
angle. **Avoid premature simplification. Finish the GENERAL equation, and then
make choices that make it more convenient for defining parafoils.**


Designing a chord surface with these equations requires five steps:

1. Define a *section index* :math:`s`

2. Define a scalar-valued function for the section scaling factors
   :math:`c(s)`

3. Choose the reference point positions on the chords :math:`\left\{ r_x(s),
   r_y(s), r_z(s) \right\}`.

4. Define a 3-vector valued function for the section reference point positions
   in wing coordinates :math:`\vec{r}_{RP/O}^f(s) = \left\langle x(s), y(s),
   z(s) \right\rangle`

5. Define the section orientation matrices :math:`\mat{C}_{f/s}(s)`



Namely, some choices that work well for parafoils:

* Let `r_y = r_z`

* Parametrize `C_f/s` using intrinsic Euler angles:

  * Section roll: defined "automatically via `arctan(dz/dy)` (where `dz/dy`
    comes from `r_RP/O`)

  * Section pitch: defined with an explicit design curve

  * Section yaw: fixed at zero [[FIXME: I remember that maintaining zero-yaw
    was significant, but I forget why?]]

To specify a parafoil you just need to design: `c`, `r_x`, `r_yz`, `r_RP/O`,
`theta`, and the section airfoils.

**FIXME**: write the final version using the actual functions (of section
index, fractions of the chord, etc) instead of this generalized notation ("any
point P" is not particularly clear)]]

Some advantages of this parametrization:

1. It makes it particularly easy to capture the important details of a foil

2. It makes it easier to design in mixed flat and inflated geometries

3. It's compatible with aerodynamic analysis via section coefficient data
   (partly by keeping the y-axes in the yz-plane).

* **Oh hey, I just figured out how my choice of reference point works!** Think
  of `c * C_f/s @ xhat` as a vector of derivatives: how much you would change
  in x, y, and z as you moved one chord length from the LE to the TE. The
  vector `c * C_f/s @ xhat` is essentially `<dx/dr, dy/dr, dz/dr>` (where `0
  <= r <= 1` is the parameter for choosing points along the chord). Applying
  `diag(r_x, r_y, r_z)` just scales them.

  Another way to get the intuition: imagine the trailing edge. You know that
  by definition it is `c * xhat` from the leading edge. Now imagine a point at
  `0.5 * c * xhat`. It's some delta-x, delta-y, delta-z away from the LE.
  These `r_x` etc are just scaling those deltas.



Section index
-------------

[[Choosing `s = y_flat / (b_flat / 2)` is convenient because you can flatten
a wing and use its width to determine `s`, without knowing `yz(s)`. The
**result** is that `s` corresponds to the linear distance along `yz(s)`.
Choosing `r_y = r_z` was something that allows you to maintain proportional
scaling of `yz(s)` in case you want to define them together (like with
a single parametric ellipse, for example).]]

[[FIXME: explain that this assumes the foil is symmetric]]


The position, scale, orientation, and choice of airfoil must be defined for
each section. They can either be defined pointwise, relying on interpolation
between each point, or they can be functions of some explicit parameter, the
*section index*.


[[Blind-writing:

Every foil section must have a unique identifier (I think); after all, how
else could you sample points on the surface? Well, then again I guess a 3D
mesh in a modeling program doesn't need section indices. Oh, so that's the
key: it's because you're generating an entire mesh from sections.



* The variables of the basic (or expanded) model must be defined for every
  section of the foil, which means they are (implicitly or explicitly)
  functions of some variable that uniquely identifies each section.

* If the variables are defined pointwise, with linear interpolation between
  each point, then section index is implicit, and equivalent to the linear
  distance along the section positions.

  Wait: what about variable definitions like `x = sqrt(1 - y^2)`, in which
  case I guess `s = y`? Ah, not necessarily: **don't confuse the difference
  between defining the variable functions versus querying the geometry**


* Many aeronautics papers refer to this variable as the *spanwise station*,
  but *spanwise* is ambiguous; some papers use it to refer to the absolute
  y-coordinate of the section, and others use it to refer to a linear distance
  along some curve tangent to the section y-axes (the "local spanwise axis",
  as it were).

  Instead, this paper uses the term *section index* because it is an
  unambiguous reference to a unique identifier over the set of sections.


* Many modeling tools do not explicitly declare their choice of section index.
  (MachUpX refers to "span location", which I think is equivalent to distance
  along `xyz(s)`).


* A traditional choice is to use the spanwise coordinate :math:`y`. Although
  simple and intuitive for flat wings, defining a nonlinear geometry in terms
  of :math:`y` quickly becomes unwieldy.

* Another common choice is the linear distance along :math:`r_RP/O` (possibly
  normalized such that a section index of `1` refers to a wing tip).
  This choice is common among foil modeling tools that expect the variables to
  be defined pointwise, relying on linear interpolation for the intermediate
  values.

* Instead, this chapter uses the normalized linear distances of only the `y`
  and `z` components of `r_RP/O`.

  Hrm, well, sort of: what I'm really using is `s = y_flat/(b_flat/2)`, and
  then should be explaining why that's useful when working with flattened
  geometry specs.


  Advantages:

  * The section indices don't depend on `x`, which means changes to `x` do not
    change the section index.

  * When the wing is flattened, you lose `y` and `z`, yet you can still
    determine `s`, which makes it easier to use the specs for a flattened
    wing. This means you can define `x(s)`, `r_x(s)`, `c(s)`, etc, in
    parametric forms independently of information about about `yz(s)`.

  * You don't need to know the total length of `r_RP/O` to determine the
    section indices.


* Unless `x = constant`, linear spacing along `yz` will not produce linear
  spacing along `xyz`.

]]



Reference point
---------------

.. Define `r_LE/RP` relative to points on section chords using `R`

The basic model positions each section using the section origins (the leading
edges). The expanded model allows the sections to be positioned using
arbitrary reference points anywhere in the 3-dimensional section coordinate
systems. Although flexible, the freedom of the expanded model does not address
the problem of choosing good reference points.

One intuitive choice is to use points on the section chords, in which case the
reference point is a function of a chord ratio :math:`0 \le r \le 1`. The
chord lies on the negative section x-axis, so a reference point at some
fraction :math:`r` along the chord is given by :math:`\vec{r}_{RP/LE}^s = -r\,
c\, \hat{x}^s_s` (where :math:`\hat{x}^s_s = \begin{bmatrix}1
& 0 & 0\end{bmatrix}^T`, the section x-axis in the section coordinate system).

Substituting :math:`\vec{r}_{LE/RP} = -\vec{r}_{RP/LE}` into
:eq:`expanded-model-equation` produces:

.. math::

   \vec{r}_{\mathrm{LE}/\mathrm{O}}^f =
         \mat{C}_{f/s}\, r\, c\, \hat{x}^s_s
         + \vec{r}_{\mathrm{RP}/\mathrm{O}}^f

Simple and intuitive, this parametrization is used by every foil modelling
tool reviewed for this project. Models that position sections by their leading
edge are equivalent to setting :math:`r = 0`. Another, less common, choice is
to use the quarter-chord positions, in which case :math:`r = 0.25`.

.. Using a fixed scalar `r` is equivalent to requiring that the reference
   point is **ON** the chord. What I'm going to do now is define it **RELATIVE
   TO** points at (potentially different) positions along the chord, but
   without the constraint that it's on the chord.

The problem with the constraint that reference points lie on the section
chords is that it couples the position functions for all three dimensions. For
many foil geometries it can be significantly more convenient to use different
chord positions for each dimension.

For example, suppose an engineer is designing an elliptical foil with
geometric twist, and they wish to place the leading edge along the line
:math:`x = 0` and the trailing edge along the line :math:`z = 0`. Although the
intuitive specification of this foil is simply :math:`{x(s) = 0, z(s) = 0}`,
these position curves cannot be used because they are trying to position
different points on the section chords: the simple form of :math:`x(s) = 0`
requires :math:`r = 0`, and :math:`z(s) = 0` requires :math:`r = 1`. One of
the position curves must be changed, introducing unnecessary complexity to
make up for this inflexibility.

For another example, a foil designer may want to curve an elliptical planform
such that the :math:`y` and :math:`z` coordinates of the quarter-chord
(:math:`r = 0.25`) follow a circular arc and the :math:`x` coordinate of the
trailing edge (:math:`r = 1`) is constant. Because of the elliptical chord
distribution, the :math:`x` coordinates of the quarter-chord what would
produce a straight trailing edge are distinctly non-constant; if geometric
twist is present the issue becomes even more severe. What should be a simple
:math:`x(s) = 0` to specify the straight trailing edge must become
a significantly complex function with no simple analytical representation.

The underlying problem is that the designer cannot specify their design
directly using a shared reference point. Instead, they must translate their
design into an alternative specification into positions that would produce
their target design using that shared reference point. A good geometry model
should allow a designer to express their intent directly, without
modification; instead, the simplicity of a scalar :math:`r` forces unnecessary
complexity onto the designer.

The solution is that instead of the geometry model requiring the designer to
specify their entire design in terms of a single position along the chord, it
should allow each of the three coordinates of the reference point to be
defined relative to independent positions along the chord.

Fortunately, this flexibility is easier to implement and use than it is to
describe. Instead of a single :math:`r` for all three dimension, allow each
dimension of the reference point to choose a different :math:`r`:

.. math::

   \mat{R} \defas \begin{bmatrix}
      r_x & 0 & 0\\
      0 & r_y & 0\\
      0 & 0 & r_z
   \end{bmatrix}

The coordinates of the leading edge relative to the reference point is simply
the relative displacement of the section origin relative to the :math:`x`,
:math:`y`, and :math:`z` components of the :math:`r_x`, :math:`r_y`, and
:math:`r_z` positions along the chord. The resulting equation, which allows
completely decoupled positioning for each dimension, is surprisingly simple:

.. math::

   \vec{r}_{\mathrm{LE}/\mathrm{O}}^f =
     \mat{R} \mat{C}_{f/s} c\, \hat{x}^s_s
     + \vec{r}_{\mathrm{RP}/\mathrm{O}}^f

This choice of reference point makes the earlier examples trivial to
implement. For the first, which was struggling with the fact that geometric
twist has coupled the :math:`x` and :math:`z` positions is solved with
:math:`\{r_x = 0, r_z = 1\}` (because the foil is flat, :math:`r_y` is a free
parameter). The second example, which was struggling to define an `x(s)` to
achieve a straight trailing edge, the answer is simply :math:`\{ r_x = 1, r_y
= 0.25, r_z = 0.25 \}`. In both cases, the designer is able to specify their
target directly, using simple design curves, with no translation necessary.

[[Now discuss how to simplify the choice for parafoils by making `r_y = r_z`.
Notably, setting `r_y = r_z` maintains proportional scaling of the `yz` curve;
you can curve and it won't get distorted on the final foil.]]


Orientation
-----------

[[Specifying orientation using Euler angles, choosing phi, theta, and gamma,
etc]]

[[Defend these choices:

* `phi = 0`

* `theta(s)`

* `gamma = arctan(dz/dy)`

It's nice because now you only have one free parameter instead of three.]]


Simplified equation
-------------------

[[Repeat the simplified equation, but now include variable definitions in
terms of the section index. This summary should be complete and standalone,
matching my implementation.]]



EXTRA
-----

* Problems with the general surface equation

  * It's too flexible: it doesn't impose any restrictions on the values of the
    variables, meaning it allows design layouts that can't be (reasonably)
    analyzed using section coefficient data. It forces all the responsibility
    on the designer to produce a useable foil definition.

  * It's not flexible enough: it requires the designer to use the section
    leading edges to position the sections. In many cases it is more
    convenient to position with other points, such as the quarter-chord,
    trailing edge, etc. [[If a designer wants to define a foil using some
    other reference point they cannot do it directly; they must specify the
    shape indirectly by manually calculating the corresponding leading edge
    position.]]

* [[The general equation is the result of designing via wing sections. The
  whole point is that you start by defining the section profiles, then
  position them relative to the foil origin to produce the final foil.
  Splitting `r_P/O` into `r_P/LE` and `r_LE/O` is the natural (general) result
  of designing with wing sections; I suppose it's sort of a parametrization of
  the surfaces, but that's not the "parametrization" I'll be talking about
  later. **I need to give a more complete definition of the airfoil geometry
  in terms of `r_P/LE` before I introduce the general equation to make it more
  obvious what those two components mean.**]]

* Should I introduce scale, position, etc **before** the general equation, or
  should I define the general equation as part of the "design with wing
  sections" section, and naturally segue from "what the math produced" into
  a discussion of those four parameters?

  That'd work nicely if I can **clearly** motivate each step of the derivation
  of the general equation.

* The origin of the chord surface is defined by the origins of the position
  functions. Let the user of the chord surface (eg, a `ParagliderWing`)
  position and orient the chord surface as they like; don't pollute this
  definition with constraints like "the origin is the central leading edge".

* Note that I've dropped the section index parameter for notational simplicity

* :math:`\mat{C}_{f/s}` is the directed cosine matrix (DCM) of the foil
  reference frame :math:`\mathcal{F}_w` with respect to the section reference
  frame :math:`\mathcal{F}_s`.


EXTRA 2: points on chords
-------------------------

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


Examples
========

.. This section highlights the elegance of the "optimized" parametrization.

These examples are composed from a small collection of simple design
curves, such as constant functions, polynomials, and parametric functions.
See :ref:`derivations:Parametric design curves` for a derivation of some
parametric curves; for usage information of their implementations, see the
`glidersim` documentation, such as :py:class:`documentation
<glidersim:pfh.glidersim.foil.EllipticalArc>`.

All examples are generated programmatically. For details of the parameters
used in each example, the source is available in [[FIXME: link to
source]].

For the profile surfaces, all examples are using a NACA 23015 airfoil.

[[**FIXME**: embed the video in the HTML build]]


Delta wing
----------

Straight wing with a linear chord distribution and no twist.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat2_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat2_canopy_chords.*

   Chord surface of a delta wing planform.


Elliptical wing
---------------

Straight wing with an elliptical chord distribution and no twist.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat3_canopy_chords.*

   Chord surface of an elliptical wing planform.


Twisted wing
------------

Wings with geometric torsion (or "twist") typically use relatively small
angles that can be difficult to visualize. Exaggerating the angles with
extreme torsion makes it easier to see the relationship.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_canopy_chords.*

   Chord surface of a wing with geometric twist.


Manta ray
----------

The effect of changing the reference positions can be surprising. A great
example is a "manta ray" inspired design that changes nothing but the constant
value of :math:`r_x`.

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta1_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta1_canopy_chords.*

   "Manta ray" with :math:`r_x = 0`


.. figure:: figures/paraglider/geometry/canopy/examples/build/manta2_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta2_canopy_chords.*

   "Manta ray" with :math:`r_x = 0.5`


.. figure:: figures/paraglider/geometry/canopy/examples/build/manta3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta3_canopy_chords.*

   "Manta ray" with :math:`r_x = 1.0`

These examples clearly demonstrate the power of wing design using extremely
simple parametric curves. Four of the six design "curves" are merely constants,
and yet they enable significantly nonlinear designs in an intuitive way.


Parafoil
--------

[[This example should be a complete description, explaining the design curves
and the plots. The other examples can be less detailed; the curves and result
should suffice.]]

[[FIXME: describe the "anhedral" correctly]]

An elliptical arc with a mean anhedral of 30 degrees and a wingtip anhedral of
89 degrees:

.. math::

   \begin{aligned}
   c(s) &= \mathrm{elliptical\_chord}(root=0.5, tip=0.2)\\
   \theta(s) &= 0\\
   r_x(s) &= 0.75\\
   x(s) &= 0\\
   r_{yz}(s) &= 1\\
   yz(s) &= \mathrm{elliptical\_arc}(mean\_anhedral=30, tip\_roll=89)\\
   \end{aligned}


.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_canopy_chords.*

   Chord surface of a simple parafoil.

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_canopy_airfoils.*

   Profile surface of a simple parafoil.

[[**FIXME**: need to explain the diagrams. The dashed green and red lines in
particular.]]

[[**FIXME**: good time to explain that if `x` is constant then it's irrelevant.
One of the more confusing aspects of this geometry is that no matter what you
define, the central leading edge is always at the origin. Is it accurate to say
that the `x` and `yz` curves are all about **RELATIVE** positioning? They're
not exactly displacement vectors, because the final positions depend on all the
other variables. On the bright side, you don't have to care.]]

The code does have the option of letting the design curves use absolute
positioning, but I'm not sure I want to discuss that here.]]


Case study
==========

.. Introduce Belloc's reference wing geometry. There are two points here:

   1. Show how easy it is to implement specs from actual papers

   2. Prepare for the wind tunnel test in the next chapter

[[The point is to make it easy to produce target geometries. In particular,
how well does this geometry map onto actual wings from literature? Introduce
Belloc's wing, and show how to translate his specs into this parametrization.
Thankfully, he's using simple linear relationships, so the design curves are
simple constants and linear interpolators.]]

.. list-table:: Full-scale wing dimensions
   :header-rows: 1

   * - Property
     - Value
     - Unit
   * - Arch height
     - 3.00
     - m
   * - Central chord
     - 2.80
     - m
   * - Projected area
     - 25.08
     - m\ :sup:`2`
   * - Projected span
     - 11.00
     - m
   * - Projected aspect ratio
     - 4.82
     - --
   * - Flat area
     - 28.56
     - m\ :sup:`2`
   * - Flat span
     - 13.64
     - m
   * - Flat aspect ratio
     - 6.52
     - --

The physical model was built at a quarter-scale. Physical dimensions and
positions were provided for the physical model.

.. csv-table:: Model wing geometry data at panel’s ends
   :header: :math:`i`, :math:`y` [m], :math:`z` [m], :math:`c` [m], :math:`r_x`, :math:`r_{yz}`, :math:`\\theta` [deg]

   0, -0.688,  0.000, 0.107, 0.6, 0.6, 3
   1, -0.664, -0.097, 0.137, 0.6, 0.6, 3
   2, -0.595, -0.188, 0.198, 0.6, 0.6, 0
   3, -0.486, -0.265, 0.259, 0.6, 0.6, 0
   4, -0.344, -0.325, 0.308, 0.6, 0.6, 0
   5, -0.178, -0.362, 0.339, 0.6, 0.6, 0
   6,  0.000, -0.375, 0.350, 0.6, 0.6, 0
   7,  0.178, -0.362, 0.339, 0.6, 0.6, 0
   8,  0.344, -0.325, 0.308, 0.6, 0.6, 0
   9,  0.486, -0.265, 0.259, 0.6, 0.6, 0
   10, 0.595, -0.188, 0.198, 0.6, 0.6, 0
   11,  0.664, -0.097, 0.137, 0.6, 0.6, 3
   12,  0.688,  0.000, 0.107, 0.6, 0.6, 3

It is important to notice the difference between the section numbers used here
and the section indices used in the parafoil canopy geometry.

Also, the reference data is defined with the wing tips at :math:`z = 0`,
whereas the chord surface convention places the canopy origin at the leading
edge of the central section. This is easily accommodated by the chord surface
implementation, which simply shifts the origin to suit the final geometry.

.. TODO:: Should I use these tables or just give the explicit equations?
   They're messy, bu I do like the fact that they highlight the fact that you
   **can** use pointwise data.

For the section profiles, the model uses a NACA 23015 airfoil.

.. figure:: figures/paraglider/geometry/airfoil/NACA-23015.*

   NACA 23015

Inputting the values to the parametric foil geometry produces:

.. raw:: latex

   \newpage

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_canopy_chords.*

   Chord surface for Belloc's reference paraglider wing.

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_canopy_airfoils.*

   Profile surface for Belloc's reference paraglider wing.


Discussion
==========

* This project requires a parametric geometry that could model complex wing
  shapes using simple design parameters. The parametrization must make it
  convenient to approximate existing paraglider canopies using the limited
  available data.

  [[If you had highly detailed geometry data you could use that, but since we
  don't we need to use simple functional forms to approximate that detail.]]

* There are two aspects to a geometry model:

  1. The choice of variables that combine to describe the wing. The choice of
     variables is the language the designer must use to describe the wing.

  2. Assigning values to those variables

* This chapter started with *wing sections* to derive a general equation
  typical of existing geometry models. It decompose the position variable to
  allow positioning via an arbitrary reference point. The decomposition
  decoupled all the variables, making it easier to design parametric functions
  for each of them. I concluded with my choice of parametrization, and some
  examples of canopies using that parametrization.

* Reference the :ref:`foil_aerodynamics:Case study` (Belloc's wing) and
  :doc:`demonstration` (my Hook3ish)


Advantages
----------

[[Is this a discussion of my parametrization of the chord surface, or of
parametric functions, or...?]]

* Using arbitrary reference points is great because (1) they decouple the
  parameters (so you can change one without needing to modify the others) and
  (2) they allow the designer to directly target the aspects of the design
  they're interested in (eg, you don't have to specify rotation points)

* The equations are simple, so implementation is simple.

* No constraints on the form of the design parameters. You can use (mostly)
  arbitrary functions for the curves, like linear interpolators or Bezier
  curves. This makes it easy to design custom curve shapes, and it makes it
  easy to recreate a geometry that was specified in points (like in Belloc).
  You can use Bezier curves if you want. [[This probably isn't unique to this
  parametrization.]]

* As a generative model, it's easy to integrate into a CAD or 3D modeling
  program that can choose how to sample from the surface. [[Again, this isn't
  unique to this parametrization.]]

* Parametric design functions have significant advantages over explicit
  functions (ie, specifying a set of points and using linear interpolation):

  * Parametric functions are amenable to mathematical optimization routines,
    such as exploring performance behaviors or performing statistical parameter
    estimation (fitting a model to flight data).

  * Explicit (as opposed to parametric) representations make it difficult to
    incorporate deformations. There are a variety of interesting situations that
    deform a paraglider wing: trailing edge deflections due to braking, C-riser
    piloting, accelerator flattening, weight shift, cell billowing, etc.

  * [[These statements are true, but again: not unique to this
    parametrization?]]

* Parametric design parameters can be parametrized to produce cells,
  billowing, weight shift deformations, etc? [[Again: not unique.]]


Limitations
-----------

* This geometry does not impose any constraints on self-intersections.
  Self-intersections can occur if the chord surface is excessively curved (so
  the surface intersects itself), or if the thickness of an airfoil causes the
  inner surface of a radius to overlap. [[These are limitations of the general
  equation that are inherited by this parametrization. If I allowed section
  yaw then you'd have this issue for that too.]]

  I've accepted this limitation with the understanding that the equations are
  intended to be as simple as possible, and reasonable wing designs are
  unlikely to be impacted. If these geometric constraints are important for
  a design then the geometry can be validated as an additional post-processing
  step instead of polluting these equations.

* I'm explicitly disallowing section-yaw (so no wedge-shaped segments), and
  assume that the section y-axes are all parallel to the body y-axis when the
  wing is flat. I'm not sure how accurate that is.

* Doesn't model internal structure (ribs, straps), and thus cannot model
  cells, cell distortions, and cannot account for the mass of the internal
  structure.

  Conceptually the abstracted section indices should enable a relatively
  simple mapping between inflated and deflated sections, but I never developed
  a suitable transformation to the section profiles.

* [[My choice of section index assumes a symmetric foil.]]


EXTRA
=====

* Using a chord surface to define a wing:

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
