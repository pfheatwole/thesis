.. This chapter generalizes the typical foil geometry equation to allow
   arbitrary reference points for position, relaxing the constraint that the
   geometry is specified in terms of the leading edge. This additional
   flexibility allows complex geometries to be described using simple
   parametric design curves. The parametric design curves encode domain
   expertise (reasonable assumptions about typical foil design), thus enabling
   complete parafoil geometries to be specified using only summary technical
   specifications.


*************
Foil geometry
*************

.. What is a foil? Why does this project need to model the foil geometry?

The essential components of any flying object are the lifting surfaces, or
*foils*: by redirecting airflow, a foil exchanges momentum with the air,
producing a lifting force that allows the object to fly. The dynamics of a foil
depend on its inertial properties and its aerodynamics, both of which can be
estimated from its shape.

A foil geometry model describes the shape of a foil by defining the positions
of all the points on the foil's surfaces. Although those positions can be
defined as an explicit set of points (with interpolation in between), it is
much more convenient to decompose them into a set of variables that represent
distinct characteristics of the foil's shape. Similarly, those variables may be
defined using explicit values, but it is much more convenient to define them
using *design curves*: parametric functions that encode that underlying
structure of the foil with a small number of intuitive parameters.

This decomposition is essential to this project, because the foils of interest
are commercial paraglider wings, and manufacturers do not provide explicit
geometry data; at best, marketing materials and user manuals provide basic
summary specifications, which means the majority of the geometry is unknown.
Generating a surface model from summary information requires making educated
guesses about the missing structure in order to generate a complete geometry.
That assumed structure takes the form of domain expertise encoded in the design
curves, which augment the summary data to produce a fully specified model.


.. The Problem

   Why not use an existing foil geometry model? The geometry model chooses the
   variables, which in turn determines the structure of the functions that
   define those variables.

The difficulty with this approach is that the choice of variables in a geometry
model controls how a designer must specify the structure. More variables
increase model flexibility at the cost of increased complexity, so the goal is
to choose the smallest number of variables that provide the designer with
adequate flexibility. Existing foil models are inflexible, making strong
assumptions about how foils are most naturally defined, and that inflexibility
forces the remaining complexity into the design curves. This unnecessary
complication makes it difficult to describe a parafoil using simple parametric
functions: they must not only encode the fundamental structure, they must also
translate that structure into the variables that define the model. Instead of
the geometry model adapting to the needs of the design curves, the design
curves must adapt to the inflexibility of the model.


.. The Solution

The solution developed in this chapter is to reject the assumption that
predefined reference points are the most convenient way to position the
elements of a foil surface. The result is a novel foil geometry that fully
decouples the design curves, allowing each variable to be designed
independently. It also presents a simplified model that eliminates most of the
additional complexity of the expanded model. The simplified model is both
flexible and intuitive for designing highly nonlinear foil geometries (such as
paraglider canopies) using simple parametric functions.


.. Notes on notation

But first, a remark on notation: in this chapter, the lifting surface of an
aircraft is referred to as a *foil* instead of using the conventional terms
*wing* or *canopy* (for traditional aircraft or parafoils, respectively). This
unconventional term was chosen to avoid two generalization issues. First,
although *wing* is the conventional term for the primary lifting surfaces of
non-rotary aircraft, the paragliding community already uses the term
*paraglider wing* to reference not only the lifting surface but also the
supporting structure connected to it, such as suspension lines, risers, etc.
Second, although this project is primarily concerned with parafoils, the
content in this chapter is not limited to parafoil canopies, making "canopy"
a poor choice.


.. Choose what geometry details to include and which to ignore

In addition, note that these are idealized geometry models, not detailed
structural models. Structural models include physical details that can be used
to simulate effects such as internal forces and wing deformations
:cite:`lolies2019NumericalMethodsEfficient`. Unfortunately, as discussed
earlier, such details are not available for commercial paraglider wings, and
such analyses would be time prohibitive even if they were. Instead, this design
will model only those details of the shape that can be approximated from the
available data. It does not model internal structures, in-flight deformations,
or surface deviations from the idealized design target.

.. For statistical filtering this imprecision would simply be another source of
   model uncertainty.




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


Modeling with wing sections
===========================

.. Introduce designing a wing using "wing sections". They're the conventional
   starting point for parametrizing a wing geometry (airfoil curves capture
   the structure of the section profiles), and lead to the basic model.

.. Explicit vs parametric geometries

At its most basic, a foil geometry is the surface of a volume. Points on the
surface can be defined with explicit coordinates, or they can be generated
using functions that encode aspects of the surface's structure. Explicit
geometries are extremely flexible (since they can encode arbitrary amounts of
detail), but refining an explicit mesh can be very time consuming (in addition
to requiring highly detailed geometry data). Conversely, parametric geometries
model the surface mesh indirectly using parametric functions which encode
structural knowledge of the shape. In effect, the parameters summarize the
structure: a structural parameter communicates more information than an
explicit coordinate, which means less work (and less data) is required to
specify a design.


.. Wing sections

The standard first step towards parametrizing a foil geometry is to define it
in terms of *wing sections* (:cite:`abbott1959TheoryWingSections`;
:cite:`bertin2014AerodynamicsEngineers`, Sec. 5.2). The foil is modeled as
a sequence of *sections* (typically arranged spanwise, left to right) over some
continuous *section index* :math:`s`. Each section is assigned a 2D
cross-sectional profile, called an *airfoil*, which lies perpendicular to the
local spanwise axis. Each airfoil is scaled, positioned, and oriented to
produce the *section profile*. Together, the section profiles produce
a continuous surface that defines the complete 3D volume.

Wing design using airfoils is thus decomposed into two steps:

1. Specify the scale, position, and orientation of each section

2. Specify the airfoil at each section

.. figure:: figures/paraglider/geometry/wing_sections2.svg

   Wing section profiles.

   Note that section profiles are not the same thing as the ribs of a parafoil.
   Parafoil ribs are the internal structure that produce the desired section
   profile at specific points along the span.

In some literature :cite:`gudmundsson2014GeneralAviationAircraft` these two
steps are described as designing the *planform* and the *profile*, but this
description is problematic due to inconsistent uses of the term *planform*
across literature. Specifically, in some cases the planform is the complete
surface produced by the section chords, and in others "planform" refers to
a projected-view of the chord surface onto the :math:`xy`-plane. Due to this
ambiguity, this paper avoids the term *planform* in preference of explicit
references such as *chord surface*, *mean camber surface*, or *profile
surface*.


Section index
-------------

In order to generate a foil from discrete wing sections (and to support queries
about their individual properties) each section must be assigned a unique
identifier which this paper refers to as a *section index* :math:`s`. This term
is deliberately generic. Some aeronautics literature use the term *spanwise
station*, but "spanwise" is ambiguous: some papers use "spanwise" to refer to
the absolute :math:`y`-coordinate of some reference point embedded in each
section, while others refer to the linear distance along the curve through
those reference points. The term *section index* generalizes these concepts and
provides an arbitrary reference to any choice of unique identifier over the set
of sections.

However, avoiding ambiguity is the not the primary purpose of this generality.
The real goal is to avoid unnecessary coupling of the design curves that define
the geometry. Instead of committing to a definition immediately, delaying the
choice of section index allows a designer the freedom to define the section
index in terms of the geometry, or the geometry in terms of the section index,
or a even a mixture of the two. This freedom will be used later by the
:ref:`foil_geometry:Simplified model` to enable particularly simple parametric
design curves.


.. Why do I refer to an explicit, abstract section index?

   It allows each model to choose whatever definition of section index is most
   convenient (for example, the models in this chapter use this flexibility to
   decouple the design curves from any particular aspect of the geometry).

   It also highlights that models shouldn't need to know what `s` represents.
   For example, it allows for generalized aerodynamics methods that work with
   `s` instead of, say, `y`. Don't lock designers into choices like `s = y`;
   they're free to do `x(s) = y(s)^2` if they want, but don't require that.
   (ie, functions of `s` are more general than functions of `y`)


.. Defining the section index

   Don't confuse how you generate the geometry with how you index a section.


.. Other considerations:

   * Is it useful to **define** the design curves?

   * Does it need physical significance?

   * Does it provide some useful relation, like `s = 0.5` is the "midpoint" of
     something of interest?


.. Start with the airfoil, since it defines important terminology.

Airfoil
-------

.. Define airfoil terminology

The building block of each section is its dimensionless cross-sectional
profile, called an *airfoil*. The volume of the wing is generated by the
continuum of neighboring airfoils, so the choice of 2D airfoils is vital to
designing the flow field characteristics over the 3D wing. The choice involves
trade-offs specific to the application (for example, thicker airfoils tend to
offer more gentle stall characteristics in exchange for a small increase in
drag); as a result, the variety of airfoil designs is very diverse.

.. figure:: figures/paraglider/geometry/airfoil/airfoil_examples.*

   Airfoils.

Airfoils are conventionally described using terms that assume the airfoil can
be divided into upper and lower surfaces. The upper and lower surfaces are
separated by two points defined by a straight *chord line* that runs from the
rounded leading edge back to the sharp trailing edge. The curve created by the
midpoints between the upper and lower surface curves is the *mean camber line*.

.. figure:: figures/paraglider/geometry/airfoil/airfoil_diagram.*
   :name: airfoil_diagram
   :scale: 80%

   Components of an airfoil.

Another standard design parameter for an airfoil is its *thickness
distribution*. Unfortunately, the mean camber line and thickness distribution
are not universally defined, because there are two conventions for measuring
the airfoil thickness: perpendicular to the chord line (sometimes referred to
as the "British" convention), or perpendicular to the mean camber line (the
"American" convention). The thickness convention also determines what point is
designated the *leading edge*. For the "British" convention the leading edge is
the point where the curve is perpendicular to a line from the trailing edge.
For the "American" convention, the leading edge is the "leftmost" point with
the smallest radius (greatest curvature).

.. FIXME: add a reference for British and American conventions?

.. The choice of convention is irrelevant. The only thing that matters is that
   you manufacture the wing with the sections scaled and oriented in exactly
   the same way as they were defined. For example, you could define the chord
   with any two points on the surface; it would be confusing, and you could
   end up with a usable range of alpha from, like, 53 to 70 degrees, but as
   long as you mount the section oriented correctly it's irrelevant. The
   convention does two things: (1) it disambiguates the orientation of the
   profile relative to freestream associated with the coefficients, and (2)
   standardizes the orientation so you can easily swap out different profile
   definitions.

.. figure:: figures/paraglider/geometry/airfoil/NACA-6412-thickness-conventions.*
   :name: airfoil_thickness
   :scale: 80%

   Airfoil thickness conventions.

As a result, the exact value of the mean camber line and thickness depends on
the thickness convention, but in general the mean camber line will lie halfway
between an upper and lower surface whose separation distance is specified by
the thickness distribution. Fortunately, this ambiguity is irrelevant except
when comparing airfoil design parameters.

.. FIXME: when **does** it matter? It affects the mean camber line so it would
   affect the placement of aerodynamic control points on the mean camber
   surface; it would change the thickness for inertia calculations (as in
   Barrows method for computing apparent mass); more?


Scale
-----

.. Wing sections are built from scale models

By convention, airfoils are normalized to a unit chord length. Similarly, the
aerodynamic coefficients associated with an airfoil are also dimensionless. To
generate the geometry and compute the aerodynamic forces associated with a wing
segment, both the airfoil and its aerodynamic coefficients must be scaled in
units appropriate to the model.

.. FIXME: unit analysis to verify the coefficients are dimensionless


.. What is determined by the scale distribution?

Although conceptually simple, section scale plays a large role in controlling
the aerodynamic behavior of a wing segment; in fact, all but the most basic
foils have variable section chord lengths. The only fundamental requirement is
that the sections collectively produce enough aerodynamic lift to support the
aircraft, but beyond that a foil designer is free to use use spanwise variation
to control behavior such as:

* Spanwise loading (the chord lengths are one factor, along with choice of
  section profile and orientation/twist, that can be used to encourage an
  elliptical load distribution, thus minimizing induced drag)

* Weight distribution

* Relative importance of wing segments (if the wingtips are smaller then they
  contribute less to the loading, making the loading is less sensitive to
  wingtip stalls, leading to "gentler" stall characteristics)

.. Bonus: keeping scale as an independent parameter instead of hard-baking it
   into the airfoil and its coefficients means a foil designer can use general
   coefficient data an adjust the results on demand.


Position
--------

The relative position of the sections is fundamental to controlling important
foil characteristics such as *span*, *sweep*, and *arc*
:cite:`gudmundsson2014GeneralAviationAircraft`. Span (the width of the wing,
roughly speaking) together with the chord distribution determines the *aspect
ratio* of a foil, which impacts characteristics such as aerodynamic efficiency
and maneuverability. Sweep (the fore-aft relative positioning of the sections)
is important for controlling spanwise airflow. Arc (the vertical relative
positioning of the sections, roughly speaking) is primarily used to increase
the roll stability of conventional wings, although for parafoils the *arc
anhedral* is essential to designing the spanwise loading across the suspension
lines.

To define their layout, each section must be positioned by specifying a vector
in foil coordinates of some *reference point* in the section's local coordinate
system. For example, the most common choice of reference point is the leading
edge of the section profile; by convention the section leading edge will
coincide with the origin of the airfoil coordinate system, which means no
additional translations are required to position the profile. This conventional
but inflexible choice is demonstrated by the :ref:`foil_geometry:Basic model`,
then relaxed by the :ref:`foil_geometry:Expanded model`, and made convenient by
the :ref:`foil_geometry:Simplified model`.

.. FIXME: this paragraph feels awkward. What's its point?


Orientation
-----------

The last degree of freedom for a wing section is its orientation. Instead of
pointing straight ahead, the can roll and twist to change their angle of attack
in different flight conditions. Changing the wind angles affects both their
aerodynamic coefficients as well as the direction of the force and moment
produced by that section. Controlling the strength, magnitude, and orientation
of the section forces can be used to control characteristics such as the
zero-lift angle of the wing, spanwise loading (the lift distribution, which
also affects the induced drag of the wing), stall profile (how stall conditions
develop across the span), and dynamic stability (such as the roll-yaw coupling
exhibited by wings with arc anhedral).


Basic model
===========

Choosing to model a foil using *wing sections* means that the surfaces are
defined by 2D airfoils. The 2D airfoil curves must be converted into a 3D
section-local coordinate system, then scaled, positioned, and oriented relative
to the foil coordinate system. This "basic" model describes how that is done by
conventional wing modeling tools, which position the sections by their leading
edge.

First, let :math:`P` represent any point in a wing section (such as points on
the chord, mean camber line, or profile), and :math:`LE` be the leading edge of
that section. It is conventional to share the origin between the airfoil and
section coordinate systems, and specify the section position using the section
leading edge, so using the :ref:`notation <common_notation>` of this paper,
a general equation for the position of that point :math:`P` with respect to the
foil origin :math:`O`, written in terms of the foil coordinate system
:math:`f`, is:

.. Unparametrized (explicit geometry?) equation

.. math::
   :label: conventional position layout

   \vec{r}_{P/O}^f = \vec{r}_{P/LE}^f + \vec{r}_{LE/O}^f

Assuming the foil geometry is symmetric, designate the central section the
foil *root*, and let the 3D foil inherit the 3D coordinate system defined by
the root section. Points in section (local) coordinate systems :math:`s` must
be rotated into the foil (global) coordinate system :math:`f`. Given the
*direction cosine matrix* :math:`\mat{C}_{f/s}` between the section and foil
coordinate systems, position vectors in foil coordinates can be written in
terms of section coordinates:

.. math::
   :label: profile points

   \vec{r}_{P/LE}^f = \mat{C}_{f/s} \vec{r}_{P/LE}^s

Because airfoil curves are defined in the 2D airfoil-local coordinate system
:math:`a`, another transformation is required to convert them into the 3D
section-local coordinate system :math:`s`. The convention for airfoil
coordinates places the origin at the leading edge, with the :math:`x`-axis
pointing from the leading edge towards the trailing edge, and the
:math:`y`-axis oriented towards the upper surface. This paper uses
a front-right-down convention for all 3D coordinate systems, so the conversion
from 2D airfoil coordinates :math:`a` to 3D section coordinates :math:`s` can
be written as a matrix transformation:

.. math::
   :label: T_s2a

   \mat{T}_{s/a} \defas \begin{bmatrix}
      -1 & 0 \\
      0 & 0\\
      0 & -1
   \end{bmatrix}

Next, the airfoil must be scaled. By convention, airfoil geometries are
normalized to a unit chord, so the section geometry defined by the airfoil must
be scaled by the section chord :math:`c`. Writing the points in terms of
relative position vectors defined in the foil coordinate system produces:

.. math::
   :label: profile points in airfoil coordinates

   \vec{r}_{P/LE}^f = \mat{C}_{f/s} \mat{T}_{s/a} \, c \, \vec{r}_{P/LE}^a

.. This is the suboptimal "general" parametrization

The complete general equation for arbitrary points :math:`P` in each section
:math:`s` is then:

.. math::
   :label: basic-equation

   \vec{r}_{P/O}^f(s) =
     \mat{C}_{f/s}(s) \mat{T}_{s/a} \, c(s) \, \vec{r}_{P/LE}^a(s)
     + \vec{r}_{LE/O}^f(s)

In this form it is clear that a complete geometry definition requires four
*design curves* that define the variables for every section:

.. math::
   :label: basic foil geometry variables

   \begin{aligned}
     c(s) \qquad & \textrm{Scale} \\
     \vec{r}_{LE/O}^f(s) \qquad & \textrm{Position} \\
     \mat{C}_{f/s}(s) \qquad & \textrm{Orientation} \\
     \vec{r}_{P/LE}^a(s) \qquad & \textrm{Airfoil} \\
   \end{aligned}


Expanded model
==============

.. Generalize the basic equation by decomposing `r_LE/O = r_LE/RP + r_RP/O`

The basic equation :eq:`basic-equation` is an explicit mathematical equivalent
of the approach used by most freely available wing modeling tools. However,
although it is technically sufficient to describe arbitrary foils composed of
airfoils, its inflexibility can introduce incidental complexity into what
should be fundamentally simple design curves.

.. Elaborate on why requiring position to be specified in terms of the leading
   edge is suboptimal. **The key problems are that 1) you can't specify the
   geometry in the simplest way, and 2) it couples the design curves.**
   (Coupled curves means they have to be designed simultaneously; redesigning
   one requires redesigning the others.) This is where I make my stand that
   existing tools are suboptimal, which is why it gets its own section.]]

For example, consider a delta wing with a straight trailing edge:

.. figure:: figures/paraglider/geometry/Wing_ogival_delta.*

   Ogival delta wing planform.

   `Figure <https://en.wikipedia.org/wiki/File:Wing_ogival_delta.svg>`__  by
   Wikimedia contributor "Steelpillow", distributed under a CC-BY-SA 3.0 license.

The wing geometry is fundamentally simple. Its specification should be equally
simple, but defining this wing with a model that is only capable of
positioning sections by their leading edge makes that impossible. Instead, the
position curve must be just as complex as the scale function (chord length) in
order to achieve the straight trailing edge. The simplicity of the model has
forced an artificial coupling between the design curves.

The problem becomes much more severe when section section chords no longer lie
in the :math:`xy`-plane, because the trailing edge position is no longer
a simple :math:`x`-coordinate offset; instead, all of the scale, position, and
orientation design curves are coupled together, making design iterations
incredibly tedious. Whether the adjustments are performed manually or with the
development of additional tooling, the fact is the extra work is unnecessary.

The solution is to decouple all of the design curves by allowing section
position to be specified using arbitrary reference points in the section
coordinate systems. This can be accomplished by decomposing their positions
into two vectors: one from the section *leading edge* :math:`LE` to some
arbitrary *reference point* :math:`RP`, and one from the reference point to
the *foil origin* :math:`O`:

.. math::
   :label: decomposed leading edge

   \vec{r}_{LE/O}^f = \vec{r}_{LE/RP}^f + \vec{r}_{RP/O}^f

.. The major point here is that the reference point can be anywhere in the
   section's 3D coordinate system; it is not constrained to the section x-axis.

Although this decomposition increases model complexity, the additional
flexibility allows a designer to choose whichever point in each section's
coordinate system will produce the simplest geometry specification. The basic
model :eq:`basic-equation` is replaced by an expanded equation with a new set
of design curves:

.. Note that the leading edges remain the section origins.

.. FIXME: What about the foil origin? I need a `-xyz(s = 0)` sort of term to
   translate the canopy origin to the central leading edge. I'm not requiring
   that the design curves satisfy `xyz(s = 0) = <0, 0, 0>`.

.. math::
   :label: expanded-equation

   \vec{r}_{P/O}^f(s) =
     \mat{C}_{f/s}(s) \mat{T}_{s/a} \, c(s) \, \vec{r}_{P/LE}^a(s)
     + \vec{r}_{LE/RP}^f(s) + \vec{r}_{RP/O}^f(s)

.. math::
   :label: expanded foil geometry variables

   \begin{aligned}
     c(s) \qquad & \textrm{Scale} \\
     \vec{r}_{RP/O}^f(s) \qquad & \textrm{Position} \\
     \mat{C}_{f/s}(s) \qquad & \textrm{Orientation} \\
     \vec{r}_{P/LE}^a(s) \qquad & \textrm{Airfoil} \\
     \vec{r}_{LE/RP}^f(s) \qquad & \textrm{Reference point} \\
   \end{aligned}


Simplified model
================

.. The expanded model added flexibility to the basic model, but it's too
   complex to use directly since it doesn't encode any structure. We want both
   flexibility AND simplicity, so the goal is to decompose the wing in such
   a way that it enables simple design curves with parametric representations.
   In this section I provide a few carefully considered simplifications that
   replace the fully explicit "Expanded model" with simple parametrizations of
   `C_f/s` and `r_LE/RP` that are easier to specify with parametric curves.


The `Basic model`_ is adequate to represent wings arbitrary foils composed of
airfoils, but its inflexibility forced incidental complexity into the design
curves. The `Expanded model`_ provides additional flexibility, but it's
generality can make it difficult for a designer to identify which aspects of
the foil structure result in a simple parametric representation. This section
identifies several simplifying assumptions that provide a foundation for
a particularly concise representation of many foils (parafoils in particular).
The result is an intuitive, partially-parametrized foil geometry model that
decouples the design curves and allows a parafoil to be rapidly approximated
using only minimal available data, even if that data was obtained from
a flattened version of the parafoil.


.. To make it clear how this parametrization is valuable for designing
   parafoils from basic data it will repeatedly consider the fact that a lot of
   that basic data from from measurements taken from a flattened parafoil.
   Choosing a parametrization that allows you to use data from a flattened
   version of the wing is REALLY helpful here.

.. FIXME: link to the "available data" discussion in `Demonstration`?

.. FIXME: should I explicitly acknowledge that these parametrizations were
   tailored for specifying parafoils? The "perpendicular to yz" constraint
   does make it incompatible with stuff with vertically-sheared sections like
   fighter jet delta wings, etc. Earlier in the chapter I claimed that nothing
   in this chapter is specific to parafoil canopies, but this chapter violates
   that claim.


.. _simplified model section index:

Section index
-------------

.. This section defines the section index as a dependent variable of `yz(s)`

   Key idea: the choice of section index should help identify simple
   parametric representations that can easily incorporate available data.
   For parafoils, a lot of that data is acquired by flattening the wing.


.. What are the common choices?

Although most tools do not explicitly announce to their choice of section
index, there are two conventions in common use: the most common is to use the
reference point :math:`y`-coordinate (:math:`s = y`, or its normalized version
:math:`s = \frac{y}{b/2}`). Although simple and intuitive for flat wings,
defining a nonlinear geometry in terms of :math:`y` can become unwieldy, so
another common choice is to use the linear distance along the locus of
reference points :math:`\vec{r}_{RP/O}` (or its normalized version that ranges
±1). Unfortunately, both are problematic for modeling a paraglider canopy using
the most readily-available data.

When trying to create a model of a flexible wing like a paraglider canopy, it
is much easier to take measurements when the wing is stretched out flat. When
the canopy is flat it is possible to measure :math:`c(s)` and :math:`x(s)`
directly, whether from the physical wing or from photos (such as are found in
user manuals). Also, it is trivial to measure the flattened span compared to
trying to measure the span of an in-flight canopy. The solution is to use the
normalized section :math:`y`-coordinates from the flattened foil:

.. math::
   :label: yz-distance section index

   s = \frac{y_{flat}}{b_{flat}/2}

Not only does this choice make the section index easy to measure from
a flattened paraglider canopy, but with a careful choice of reference points it
also decouples the :math:`yz`-coordinates of the reference positions
(:math:`yz(s)`) from all the other design curves, which is a key aspect of this
model's ability to define complex nonlinear foils using simple parametric
functions. The next section explains the process in detail, but the key idea
(and why this choice of section index is so important) is that using this
definition of :math:`s` and choosing the same chord position for the :math:`y`
and :math:`z` components of the reference point you can simply "wrap" the
flattened paraglider canopy around :math:`yz(s)` to produce the final geometry.
It becomes possible design the flattened foil geometry before designing its
arc, a natural process that enables the direct use of the most readily
available measurements for commercial paraglider canopies.


Reference point
---------------

.. This section defines `r_LE/RP` using points on section chords

The `Basic model`_ positions each section using the section origins (the
leading edges). The `Expanded model`_ allows the sections to be positioned
using arbitrary reference points anywhere in the 3D section coordinate systems.
Although flexible, the freedom of the expanded model does not address the
problem of choosing good reference points.

One intuitive choice is to use points on the section chords, in which case the
reference point is a function of a chord ratio :math:`0 \le r \le 1`. The chord
lies on the negative section :math:`x`-axis, so a reference point at some
fraction :math:`r` along the chord is given by :math:`\vec{r}_{RP/LE}^s = -r\,
c\, \hat{x}^s_s` (where :math:`\hat{x}^s_s \defas \left[1 \, 0 \;
0 \right]^T`, the :math:`x`-axis of section :math:`s` in that section's local
coordinate system). Substituting :math:`\vec{r}_{LE/RP} = -\vec{r}_{RP/LE}`
into :eq:`expanded-equation` produces:

.. math::

   \vec{r}_{LE/O}^f =
         \mat{C}_{f/s}\, r\, c\, \hat{x}^s_s
         + \vec{r}_{RP/O}^f

Simple and intuitive, this parametrization captures the choices used by every
foil modelling tool reviewed for this project. Models that position sections by
their leading edge (XFLR5, AVL, MachUpX) are equivalent to setting :math:`r
= 0`. Another (less common :cite:`benedetti2012ParaglidersFlightDynamics`)
choice is to use the quarter-chord positions, in which case :math:`r = 0.25`.
The problem with the constraint that reference points lie on the section chords
is that it couples the position functions for all three dimensions. For many
foil geometries it can be significantly more convenient to use different chord
positions for different dimensions.

.. Using a fixed scalar `r` is equivalent to requiring that the reference
   point is **ON** the chord. What I'm going to do now is define it **RELATIVE
   TO** points at (potentially different) positions along the chord, but
   without the constraint that it's on the chord.

For example, suppose an engineer is designing a foil with an elliptical chord
distribution and geometric twist, and they wish to place the leading edge in
the plane :math:`x = 0` and the trailing edge in the plane :math:`z = 0`.
Although the intuitive specification of this foil would be :math:`{x(s) = 0,
z(s) = 0}`, it cannot be used because it needs to position different points on
each section chord: the :math:`x(s) = 0` design requires :math:`r = 0`, but the
:math:`z(s) = 0` design requires :math:`r = 1`. One of the position curves must
be changed, introducing unnecessary complexity to make up for this
inflexibility.

For another example, a foil designer may want to arc an elliptical planform
such that the :math:`y`- and :math:`z`-coordinates of the quarter-chord
(:math:`r = 0.25`) follow a circular arc while the :math:`x`-coordinate of the
trailing edge (:math:`r = 1`) is a constant. Because of the elliptical chord
distribution, the :math:`x`-coordinates of the quarter-chord that would produce
a straight trailing edge are distinctly non-constant; if geometric twist is
present the issue becomes even more severe. What should be a simple :math:`x(s)
= 0` to specify the straight trailing edge must become a complex function with
no simple analytical representation.

The underlying problem is that the designer cannot specify their design
directly using a shared reference point that lies directly on the chord;
instead, they must translate their design into an alternative specification
using positions that accommodate the shared reference point.

The solution is that instead of using a shared reference point directly on the
chord for all dimensions, allow each dimension to choose independent reference
points along the chord, and associate each dimension of the position design
curve with that dimension's coordinate of that dimension's reference point.
The :math:`x(s)` design curve specifies the :math:`x`-coordinate of the
reference point for the :math:`x`-dimension, etc.

.. Another way to think of this is to consider \hat{x} as the derivatives
   {dx/dr, dy/dr, dz/dr}. Now think of `c * \mat{C}_{f/s} @ \hat{\vec{x}}` as
   a vector of derivatives: how much you would change in x, y, and z as you
   moved one chord length from the LE to the TE. The vector `c * C_f/s @ xhat`
   is essentially `<dx/dr, dy/dr, dz/dr>` (where `0 <= r <= 1` is the
   parameter for choosing points along the chord). Applying `diag(r_x, r_y,
   r_z)` just scales them.

   Or another way to get the intuition: imagine the trailing edge. You know
   that by definition it is `c * xhat` from the leading edge. Now imagine
   a point at `0.5 * c * xhat`. It's some delta-x, delta-y, delta-z away from
   the LE. These `r_x` etc are just scaling those deltas.

Fortunately, providing this flexibility is easier to implement and use than it
is to describe. Instead of a shared :math:`r` for all three dimension, allow an
independent :math:`r` for each dimension of the reference point:

.. math::

   \mat{R} \defas \begin{bmatrix}
      r_x & 0 & 0\\
      0 & r_y & 0\\
      0 & 0 & r_z
   \end{bmatrix}

where :math:`0 \le r_x, r_y, r_z \le 1` are proportions of the chord, as
before. The coordinates of the leading edge relative to the reference point are
now the displacement of the section origin relative to the :math:`\left\{ x, y,
z \right\}` components of the :math:`\left\{ r_x, r_y, r_z \right\}` positions
along the chord. The resulting equation, which allows completely decoupled
positioning for each dimension, is surprisingly simple:

.. math::

   \vec{r}_{LE/O}^f =
     \mat{R} \mat{C}_{f/s} c\, \hat{x}^s_s
     + \vec{r}_{RP/O}^f

This choice of reference point makes the earlier examples trivial to implement.
For the first, which was struggling with the fact that geometric twist has
coupled the :math:`x` and :math:`z` positions is solved with :math:`\{r_x = 0,
r_z = 1\}` (because the foil is flat, every choice of :math:`r_y` is
equivalent). The second example, which was struggling to define an :math:`x(s)`
to achieve a straight trailing edge, the answer is simply :math:`\{ r_x = 1,
r_y = 0.25, r_z = 0.25 \}`. In both cases, the designer is able to specify
their target directly, using simple design curves, with no translation
necessary. The reason is that :eq:`yz-distance section index` combined with
:math:`r_y = r_z` means that changing :math:`yz(s)` does not change the section
index; having designed the orientation and fore-aft position :math:`x(s)` of
a section, changing :math:`yz(s)` will not affect that design. The curves have
been decoupled.

.. math::
   :label: simplified model reference point vector

   \vec{r}_{LE/RP}^f = \mat{R} \mat{C}_{f/s} c\, \hat{x}^s_s

.. math::
   :label: simplified model reference point matrix

   \mat{R} \defas \begin{bmatrix}
      r_x & 0 & 0\\
      0 & r_{yz} & 0\\
      0 & 0 & r_{yz}
   \end{bmatrix}


Orientation
-----------

.. This section defines `C_f/s` using `dz/dy` and `theta`

The expanded model :eq:`expanded-equation` uses a *direction cosine matrix*
(DCM) to define the orientation of each section; the problem is how to define
that matrix. A natural parametrization of a DCM is a set of three Euler angles
:math:`\left< \phi, \theta, \gamma \right>`, corresponding to roll, pitch, and
yaw. The Euler parametrization replaces the :math:`\mathbb{R}^{3 \times 3}`
matrix with a 3-vector — three parameters — but the structure of typical
parafoils can provide further simplifications.

In particular, observe that when a parafoil is flattened out on the ground, the
sections are (essentially) vertical, with no relative roll or yaw. Inflating
the parafoil and using the suspension lines to form the arc will naturally roll
the sections without affecting the section yaw. These observations reveal that
the section orientation produced by inflating a parafoil is well approximated
by a single degree of freedom, resulting in a minimal parametrization with
a single design variable for section pitch :math:`\theta(s)`.


.. The default orientation of each section is parallel to the central section.
   Real wings may want to pitch (geometric torsion) or roll (local "dihedral",
   sort of). Need a way to specify that orientation.

For the section roll :math:`\phi(s)`, observe that inflating the foil to
produce the arc does not produce a shearing effect between sections; instead,
the sections roll jointly with the arc. This relationship can be encoded using
the derivatives of the :math:`\left< y(s), z(s) \right>` components of the
position curve :math:`\vec{r}_{RP/O}(s)`:

.. math::
   :label: section roll from position

   \phi = \mathrm{arctan} \left( \frac{dz}{dy} \right)

For the section yaw :math:`\gamma(s)`, inflating the parafoil to produce the
arc anhedral will roll the sections in the foil's :math:`yz`-plane and does not
affect the section yaw, which remains zero:

.. math::
   :label: section yaw constant zero

   \gamma = 0

.. FIXME: I remember that maintaining zero-yaw was significant, but why? The
   section y-axes are all parallel to the yz-plane, so forward motion does not
   produce spanwise flow?

The remaining degree of freedom is the rotation about each sections
:math:`y`-axis. This pitch angle :math:`\theta(s)`, conventionally known as
*geometric torsion*, is produced when the wing is manufactured, and is not
affected when the flattened wing is shaped into its final arched form.

.. figure:: figures/paraglider/geometry/airfoil/geometric_torsion.*

   Geometric torsion.

   Note that this refers to the angle, and is the same regardless of any
   particular rotation point.

.. FIXME: Defend these choices

.. FIXME: define :math:`\mat{C}_{f/s}` using the Euler angles?


Summary
-------

In conclusion, the simplifications identified by this model not only reduced
the number of parameters of the expanded model :eq:`expanded foil geometry
variables`, it also replaced the arbitrary and unwieldy 3D reference points
with simple ratios of the section chords. It allows rapid and intuitive
conversion of measurements from a flattened paraglider canopy to a foil
geometry, and decoupled the design curves to allow the design of each variable
to be manipulated without affect the others. In short, it provides the
flexibility of the expanded model but without its complexity.

.. math::
   :label: simplified foil geometry variables

   \begin{aligned}
     c(s) \qquad & \textrm{Scale} \\
     r_x(s) \qquad & \textrm{Chord ratio for positioning} \ RP_x \\
     r_{yz}(s) \qquad & \textrm{Chord ratio for positioning} \ RP_y \ \textrm{and} \ RP_z \\
     \vec{r}_{RP/O}^f(s) \qquad & \textrm{Position} \\
     \theta(s) \qquad & \textrm{Pitch} \\
     \vec{r}_{P/LE}^a(s) \qquad & \textrm{Airfoil} \\
   \end{aligned}


Examples
========


.. This section highlights the elegance of the "simplified" parametrization.

These examples demonstrate how the simplified model makes it easy to represent
nonlinear foil geometries using simple parametric functions, such as constants,
absolute functions, ellipticals, and polynomials. For a discussion of the
elliptical functions for the arc and chord distributions, see
:ref:`derivations:Parametric design curves`.

All examples show a wireframe view of the chord surface because it is easier to
visualize the foil layout. The green dashed lines are projections of the
section quarter-chord positions (shown because of their use in analyzing
aerodynamics). The red dashed lines are the projections of the :math:`r_x` and
:math:`r_{yz}` chord positions.

.. FIXME: that's a mighty terse explanation of the lines

.. FIXME: link to the source?

.. FIXME: embed the video in the HTML build?


.. raw:: latex

   \newpage

Delta wing
----------

A delta with with a linear chord distribution and straight trailing edge can be
defined with :math:`r_x = 1` and a piecewise-linear :math:`c(s)`. Unlike
conventional wing modeling tools, because the trailing edge is used directly
for position in the :math:`x`-direction, the :math:`x(s)` curve does not need
to be coupled to :math:`c(s)` to compute offsets for the leading edge.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat2_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat2_canopy_chords.*

   Chord surface of a delta wing planform.


.. raw:: latex

   \newpage

Elliptical wing
---------------

Similarly, a flat wing with an elliptical chord distribution and fore-aft
symmetric is trivial to define using :math:`r_x = 0.5` and an elliptical chord
function.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat3_canopy_chords.*

   Chord surface of an elliptical wing planform.


.. raw:: latex

   \newpage

Twisted wing
------------

Wings with twist typically use relatively small
angles that can be difficult to visualize. Exaggerating the angles with
extreme torsion makes it easier to see the relationship.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_canopy_chords.*

   Chord surface of a wing with geometric twist.


.. raw:: latex

   \newpage

Manta ray
----------

The effect of changing the reference positions can be surprising. A great
example is a "manta ray" inspired design: each model uses the same
piecewise-linear chord distribution and circular :math:`x(s)`, changing only
the constant value of :math:`r_x`. These examples clearly demonstrate the
flexibility of the `Simplified model`_: four of the six design "curves" are
merely constants, and yet they enable significantly nonlinear designs in an
intuitive way.

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta1_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta1_canopy_chords.*

   "Manta ray" with :math:`r_x = 0`


.. raw:: latex

   \newpage

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta2_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta2_canopy_chords.*

   "Manta ray" with :math:`r_x = 0.5`


.. raw:: latex

   \newpage

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta3_canopy_chords.*

   "Manta ray" with :math:`r_x = 1.0`



.. raw:: latex

   \newpage

Parafoil
--------

Lastly, as this project is primarily focused on paragliders, these examples
would not be complete without showing how the `Simplified model`_ allows two
simple elliptical functions and :math:`r_x = 0.75` to easily produce an
accurate generalization of a paraglider canopy.

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_canopy_chords.*

   Chord surface of a simple parafoil.


.. raw:: latex

   \newpage

In addition to the surface produced by the section chords, it may be helpful to
see the upper and lower profile surfaces produced after assigned every section
an airfoil (NACA 23015):

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_canopy_airfoils.*

   Profile surface of a simple parafoil.
