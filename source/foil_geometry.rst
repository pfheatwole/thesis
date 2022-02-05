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
estimated from its shape. In this project the foils of interest are the
canopies of commercial paraglider wings, which poses a major difficulty:
manufacturers do not provide detailed geometry data. At best, marketing
materials and user manuals provide basic summary specifications, which means
the majority of the geometry is unknown. Generating a surface model from
summary information requires making educated guesses about the missing
structure in order to generate a complete geometry. That assumed structure
takes the form of domain expertise encoded in parametric *design curves* which
augment the summary data to produce a fully specified model.


.. The Problem

   Why not use an existing foil geometry model? The geometry model chooses the
   variables, which in turn determines the structure of the functions that
   define those variables.

The problem with this approach is that the choice of variables in a geometry
model controls how a designer must specify the structure. More variables
increase model flexibility at the cost of increased complexity, so the goal is
to choose the smallest number of variables that provide the designer with
adequate flexibility. Existing foil models are inflexible, making strong
assumptions about how foils are most naturally defined, and that inflexibility
forces the remaining complexity into the design curves. This unnecessary
complication makes it difficult to describe a parafoil using simple parametric
functions: they must not only encode the fundamental structure, they must also
encode the translation of that structure into the variables that define the
model. Instead of the geometry model adapting to the needs of the design
curves, the design curves must adapt to the limitations of the model.


.. The Solution

The solution developed in this chapter is to reject the assumption that
predefined reference points are the most convenient way to position the
elements of a foil surface. The result is a novel foil geometry that fully
decouples the design curves, allowing each aspect of the foil to be designed
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
majority of the content in this chapter is not limited to parafoil canopies,
making "canopy" a poor choice.


.. Choose what geometry details to include and which to ignore

In addition, note that these are idealized geometry models, not detailed
structural models. Structural models include physical details that could be
used to simulate the interactions between the canopy surface deformations and
the surrounding flow field :cite:`lolies2019NumericalMethodsEfficient`.
Unfortunately, as discussed earlier, such details are not available for
commercial paraglider wings, and such analyses would be time prohibitive even
if they were. Instead, this design will model only those details of the shape
that can be approximated from the available data. It does not model internal
structures, in-flight deformations, or surface deviations from that idealized
shape (such as internal ribs, cell billowing, or surface material creases).

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


Parametric modeling with wing sections
======================================

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


.. Advantages of parametric geometries

   FIXME?


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

1. Specify the airfoil at each section

2. Specify the scale, position, and orientation of each section

.. figure:: figures/paraglider/geometry/wing_sections2.svg

   Wing section profiles.

   Note that section profiles are not the same thing as the ribs of a parafoil.
   Parafoil ribs are the internal structure that produce the desired section
   profile at specific points along the span.

In some literature :cite:`gudmundsson2014GeneralAviationAircraft` these two
steps are described as designing the *profile* and the *planform*, but this
description is problematic due to inconsistent uses of the term *planform*
across literature. Specifically, in some cases the planform is the complete
surface produced by the section chords, and in others "planform" refers to
a projected-view of the chord surface onto the :math:`xy`-plane. Due to this
ambiguity, this paper avoids the term *planform* in preference of explicit
references such as *chord surface*, *mean camber surface*, or *profile
surface*.


Section index
-------------

Wing sections are convenient for generating a foil geometry mesh, but they are
also convenient for querying properties of a model; for example, aerodynamic
methods that rely on section coefficients must be able to query the scale,
position, and orientation of individual sections. To support queries involving
discrete wing sections, each section must be assigned a unique identifier,
which this paper refers to as a *section index* :math:`s`.

This term is deliberately generic. Some aeronautics literature use the term
*spanwise station*, but *spanwise* is ambiguous; some papers use "spanwise" to
refer to the absolute :math:`y`-coordinate of some reference point embedded in
the section, while others refer to a linear distance along some curve tangent
to the section :math:`y`-axes (the "local spanwise axis", as it were). The
term *section index* generalizes these concepts and provides an arbitrary
reference to any choice of unique identifier over the set of sections.


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

Although the primary purpose of a section index is as an independent variable
to query the geometry, it may also be used to define the geometry. Conversely,
it is commonly defined by the geometry; for example, a common convention is to
refer to sections by the :math:`y`-coordinate of some point embedded in the
section, or the linear distance of some curve that runs through points
embedded in the sections. It is a feature of this generality that provides
models the flexibility to choose a definition that is convenient for each
application.


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


Scale
-----

.. Wing sections are built from scale models

By convention, airfoils are normalized to a unit chord length. Similarly, the
aerodynamic coefficients associated with an airfoil are also dimensionless. To
generate the geometry and compute the aerodynamic forces associated with a wing
segment, both the airfoil and its aerodynamic coefficients must be scaled in
units appropriate to the model.


.. What is determined by the scale distribution?

Although conceptually simple, section scale plays a large role in controlling
the aerodynamic behavior of a wing segment; in fact, all but the most basic
foils vary the chord length along the span. The only fundamental requirement of
scale is that the sections collectively produce enough aerodynamic lift to
support the aircraft, but spanwise variation allows a foil designer to control
behavior such as:

* Spanwise loading (the chord lengths are one factor, along with choice of
  section profile and orientation/twist, that can be used to encourage an
  elliptical load distribution, thus minimizing induced drag)

* Weight distribution

* Relative importance of wing segments (if the wingtips are smaller then they
  contribute less to the loading, making the loading is less sensitive to
  wingtip stalls, leading to "gentler" stall characteristics)

.. [[Keeping scale as an independent parameter instead of hard-baking it into
   the airfoil and its coefficients means a foil designer can use general
   coefficient data an adjust the results on demand.]]


Position
--------

To layout a 3D foil, each section must be positioned by specifying a vector in
foil coordinates of some *reference point* in the section's local coordinate
system. For example, the most common choice of reference point is the leading
edge of the section profile; by convention the section leading edge will
coincide with the origin of the airfoil coordinate system, which means no
additional translations are required to position the profile. Section
positions are fundamental to controlling important foil characteristics such
as *span*, *sweep*, and *arc* :cite:`gudmundsson2014GeneralAviationAircraft`.


.. Misc:

   * Span (span together with the chord distribution determine the aspect ratio,
     and thus directly impact aerodynamic efficiency)

   * Sweep (important for controlling the spanwise flow, especially in
     supersonic regimes?)

   * Arc (affects aerodynamic and structural stability)

     Rigid foils such as traditional wings are often designed to produce
     in-flight *dihedral* to increase aerodynamic roll stability.

     For parafoils, creating an arc *anhedral* is essential to developing the
     spanwise load on the suspension lines.


Orientation
-----------

[[FIXME: finish]]


* [[Section pitch/roll/yaw. Dihedral/anhedral. Geometric torsion.]]

* Section roll helps keep the sections oriented parallel to each other


Section orientation can be used to control characteristics such as:

* Zero-lift angle (optimize the wing for its target/intended flight
  conditions)

* Stability

* Spanwise loading

* Stall profile (how stall conditions develop across the span)

* Roll-yaw coupling


Basic model
===========

Choosing to model a foil using *wing sections* means that the surfaces are
defined by 2D airfoils. The 2D airfoil curves must be converted into a 3D
section-local coordinate system, then scaled, positioned, and oriented relative
to the foil coordinate system.

First, let :math:`P` represent any point in a wing section (such as points on
the chord, mean camber line, or profile), and :math:`LE` be the leading edge of
that section. It is conventional to share the origin between the airfoil and
section coordinate systems, and specify the section position using the section
leading edge, so using the `notation <_common_notation>`_ of this paper,
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

Because airfoil curves are defined in the 2D airfoil-local coordinate system,
another transformation is required to convert them into 3D section-local
coordinates. The convention for airfoil coordinates places the origin at the
leading edge, with the :math:`x`-axis pointing from the leading edge towards
the trailing edge, and the :math:`y`-axis oriented towards the upper surface.
This paper uses a front-right-down convention for all 3D coordinate systems, so
the conversion can be written with a matrix transformation:

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


The basic model is adequate to represent wings composed of airfoils, but its
inflexibility forced incidental complexity into the design curves. The expanded
model provides additional flexibility, but it's generality can make it
difficult for a designer to identify which aspects of the foil structure result
in a simple parametric representation. This section identifies several
simplifying assumptions that provide a foundation for a particularly concise
representation of many foils (parafoils in particular). The result is an
intuitive, partially-parametrized foil geometry model that decouples the design
curves and allows a parafoil to be rapidly approximated using only minimal
available data, even if that data was obtained from a flattened version of the
parafoil.

[[To make it clear how this parametrization is valuable for designing parafoils
from basic data it will repeatedly consider the fact that a lot of that basic
data from from measurements taken from a flattened parafoil. Choosing
a parametrization that allows you to use data from a flattened version of the
wing is REALLY helpful here.]]


.. FIXME: link to the "available data" discussion in `Demonstration`?

.. FIXME: should I explicitly acknowledge that these parametrizations were
   tailored for specifying parafoils? The "perpendicular to yz" constraint
   does make it incompatible with stuff with vertically-sheared sections like
   fighter jet delta wings, etc. Earlier in the chapter I claimed that nothing
   in this chapter is specific to parafoil canopies, but this chapter violates
   that claim.


Section index
-------------

[[FIXME: finish]]


.. This section defines the section index as a dependent variable of `yz(s)`

   Key idea: the choice of section index should help identify simple
   parametric representations that can easily incorporate available data.
   For parafoils, a lot of that data is acquired by flattening the wing.


.. What are the common choices?

Although most tools do not explicitly refer to their choice of section index,
there are two conventions in common use: one is to use the section
:math:`y`-coordinate, and the other is the linear distance along the position
curve :math:`\vec{r}_{RP/O}`.

Unfortunately, both are problematic for modeling a parafoil from the most
readily-available data. 


**You can measure c(s) and x(s) directly from the flattened foil. You don't
know the final position, so using position is a bad idea. You only know
y_flat, so use y_flat to define the section index. The effect of using y_flat
is that s is defined as the linear distance along the yz curve (or in this
case, the normalized y_flat equates to the normalized yz distance). You should
be able to layout the flattened planform and finalize those design curves;
they shouldn't change when you change the yz-curve.**


* The section index connects all of the design curves.

* Models should choose a definition that encourages simple parametric forms of
  the design curves. Decoupling the curves as much as possible gives them the
  freedom to choose simple parametric forms (that's why the expanded model
  decomposed position).

* [[Another issue arises when modeling an existing wing from technical
  specifications and physical measurements.

  You should choose a scheme that makes it easy to determine the index of each
  section, and thus the index associate with each measurement.]]



.. What are the common choices?

A traditional choice of section index is the section :math:`y`-coordinate,
sometimes normalized by the span of the wing to produce an index between ±1
(so :math:`s = \frac{y}{b/2}`). Although simple and intuitive for flat wings,
defining a nonlinear geometry in terms of :math:`y` can become unwieldy, so
another common choice is to use the linear distance along the position curve
:math:`\vec{r}_{RP/O}`; again, this distance is sometimes normalized to ±1.


.. What is my choice? What is the advantage of my choice?

[[I chose the linear distance along the :math:`yz` curve (that is, only the
:math:`y` and :math:`z` components of :math:`r_{RP/O}(s)`). This choice has
the distinct advantage that section indices can be determined even when the
parafoil is flattened out on the ground, which means it is equivalent to

.. math::
   :label: yz-distance section index

   s = \frac{y_{flat}}{b_{flat}/2}

[[Very useful when some data comes from measurements of a flattened foil. You
can determine `s` directly from the flattened wing and measure `r_x(s)`,
`x(s)`, and `c(s)` without knowing :math:`yz(s)`. Importantly, **manipulating
`yz(s)` doesn't change `s`.**]]

[[Caveat: unless `x = constant`, linear spacing along `yz` will not produce
linear spacing along `xyz`. That can be surprising, but easy to understand if
you always visualize the wing from directly behind it.]]


Reference point
---------------

.. This section defines `r_LE/RP` using points on section chords

The basic model positions each section using the section origins (the leading
edges). The expanded model allows the sections to be positioned using arbitrary
reference points anywhere in the 3D section coordinate systems. Although
flexible, the freedom of the expanded model does not address the problem of
choosing good reference points.

One intuitive choice is to use points on the section chords, in which case the
reference point is a function of a chord ratio :math:`0 \le r \le 1`. The
chord lies on the negative section :math:`x`-axis, so a reference point at
some fraction :math:`r` along the chord is given by :math:`\vec{r}_{RP/LE}^s
= -r\, c\, \hat{x}^s_s` (where :math:`\hat{x}^s_s \defas \begin{bmatrix}1
& 0 & 0\end{bmatrix}^T`, the :math:`x`-axis of section :math:`s` in that
section's local coordinate system).

Substituting :math:`\vec{r}_{LE/RP} = -\vec{r}_{RP/LE}` into
:eq:`expanded-equation` produces:

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
is to describe. Instead of a shared :math:`r` for all three dimension, allow
each dimension of the reference point to choose an independent :math:`r`:

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

This choice of reference point makes the earlier examples trivial to
implement. For the first, which was struggling with the fact that geometric
twist has coupled the :math:`x` and :math:`z` positions is solved with
:math:`\{r_x = 0, r_z = 1\}` (because the foil is flat, every choice of
:math:`r_y` is equivalent). The second example, which was struggling to define
an :math:`x(s)` to achieve a straight trailing edge, the answer is simply
:math:`\{ r_x = 1, r_y = 0.25, r_z = 0.25 \}`. In both cases, the designer is
able to specify their target directly, using simple design curves, with no
translation necessary.


[[FIXME: explain how choosing `r_y = r_z` simplifies the design by maintaining
the proportional scaling of the `y` and `z` curves; you can design a joint
`yz` curve and it won't get distorted on the final foil. Useful for defining
`yz(s)` as a single vector-valued parametric function.]]


.. math::

   \vec{r}_{LE/RP}^f = \mat{R} \mat{C}_{f/s} c\, \hat{x}^s_s

.. math::

   \mat{R} \defas \begin{bmatrix}
      r_x & 0 & 0\\
      0 & r_{yz} & 0\\
      0 & 0 & r_{yz}
   \end{bmatrix}



Orientation
-----------

.. This section defines `C_f/s` using `dz/dy` and `theta`

The expanded model :eq:`expanded-equation` uses a *direction cosine matrix*
(DCM) to define the orientation of each section. A natural parametrization of
a DCM is a set of three Euler angles :math:`\left< \phi, \theta, \gamma
\right>`, corresponding to roll, pitch, and yaw. The Euler parametrization
replaces the :math:`\mathbb{R}^{3 \times 3}` matrix with a 3-vector, but the
structure of typical parafoils can provide further simplifications.

In particular, observe that when a parafoil is flattened out on the ground, the
sections are (essentially) vertical, with no relative roll or yaw. Inflating
the parafoil and using the suspension lines to form the arc will produce
a natural section roll without affecting the section yaw. These observations
reveal that the section orientation produced by inflating a parafoil is well
approximated by a single degree of freedom, resulting in a minimal
parametrization with a single design variable for section pitch
:math:`\theta(s)`.

.. The default orientation of each section is parallel to the central section.
   Real wings may want to pitch (geometric torsion) or roll (local "dihedral",
   sort of). Need a way to specify that orientation.

For the section roll :math:`\phi(s)`, observe that inflating the foil to
produce the arc does not produce a shearing effect between sections; instead,
the sections roll together with the arc. This relationship can be encoded using
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

Lastly, although inflating a parafoil will not cause the sections to rotate
about their spanwise axes, the relative section pitch :math:`\theta(s)`
produced during manufacturing is an important design variable, referred to as
*geometric torsion*.

.. figure:: figures/paraglider/geometry/airfoil/geometric_torsion.*

   Geometric torsion.

   Note that this refers to the angle, and is the same regardless of any
   particular rotation point.

.. FIXME: Defend these choices

.. FIXME: define :math:`\mat{C}_{f/s}` using the Euler angles?


Summary
-------

[[List the design variables as in the Basic and Expanded model subsections.]]

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

[[FIXME: finish]]


.. This section highlights the elegance of the "simplified" parametrization.

These examples demonstrate how the expanded model makes it easy to represent
nonlinear foil geometries using simple parametric functions, such as constants,
absolute functions, ellipticals, and polynomials.

[[All examples use a NACA 23015 airfoil for the section profiles. For
a discussion of the elliptical functions for the arc and chord distribution,
see :ref:`derivations:Parametric design curves`; for their implementations, see
the :external+glidersim:doc:`glidersim documentation <reference>`, such as
:external+glidersim:py:class:`EllipticalArc
<pfh.glidersim.foil_layout.EllipticalArc>`. The source code to generate each
example is available at [[FIXME: link to source]], making them useful starting
points for working with the model.]]

[[**FIXME**: need to explain the diagrams. The dashed green and red lines in
particular.]]

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

The purpose of the `Expanded model`_ is to increase the freedom of how a foil
is specified. The examples demonstrated how this freedom can be used to design
complex foil geometries using simple design curves. Another benefit of this
freedom is that it is more adaptable to the variety of foil specifications
used in literature.

Parafoil canopies in particular are not convenient to design using the leading
edge. The geometry from a 2015 parafoil wind tunnel test
:cite:`belloc2015WindTunnelInvestigation` makes an excellent case study of
a foil specification from literature that positions the sections using
alternative reference points on the section chords. Moreover, the geometry
satisfies the assumptions of the `Simplified model`_, making an implementation
of the geometry almost trivial.

First, the paper describes the geometry of the full-scale canopy they wish to
study:

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

For the wind tunnel test, a physical model was built at a quarter-scale.
Physical dimensions and positions were provided for the physical model as
pointwise data with linear interpolation between each point.

.. FIXME: Should I use these tables or just give the explicit equations?
   They're messy, but I do like the fact that they highlight the fact that you
   **can** use pointwise data in a linear interpolator just as easily.

.. csv-table:: Wind tunnel wing geometry data at panel’s ends
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

It is important to notice the difference between the section numbers :math:`i`
used in the paper and the section indices :math:`s` used in the simplified
model. The section indices are easily calculated using the normalized linear
distance along the :math:`\left< y, z \right>` points.

Another important point is that the reference data is defined with the wing
tips at :math:`z = 0`, whereas the convention of this paper places the canopy
origin at the leading edge of the central section. This is easily accommodated
by subtracting the central :math:`z = -0.375` from all :math:`z`-coordinates.
(The implementation of the simplified model in ``glidersim`` shifts the origin
automatically.) [[This is the same issue as for normal parametric functions;
the origin of the parametric functions is arbitrary; the origin of the canopy
is a predetermined point.]]

For the section profiles, the model uses a NACA 23015 airfoil.

.. figure:: figures/paraglider/geometry/airfoil/NACA-23015.*

   NACA 23015

Calculating the section indices for each point and building a linear
interpolator for each component as a function of the section index produces
a set of piecewise-linear design curves:

.. raw:: latex

   \newpage

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_canopy_chords.*

   Chord surface for Belloc's reference paraglider wing.

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_canopy_airfoils.*

   Profile surface for Belloc's reference paraglider wing.

[[FIXME: compute the summary specs and compare; area, span, etc]]


Discussion
==========

[[FIXME: finish]]


* This project requires a parametric geometry that could model complex wing
  shapes using simple, parametric design functions. The parametrization must
  make it convenient to model existing paraglider canopies using the limited
  available data.

* There are two aspects to a geometry model:

  1. The choice of variables that combine to describe the wing. The choice of
     variables is the language the designer must use to describe the wing.

  2. Assigning values to those variables

* This chapter started with *wing sections* to derive a general equation
  typical of existing geometry models. It decomposed the position variable to
  allow positioning via an arbitrary reference point. The decomposition
  allowed each design variable to be decoupled, making it easier to design
  them using simple parametric functions. I concluded with a simplified model
  that eliminated most of the extra complexity of the expanded model, and
  showed some examples of canopies using that parametrization.

* Reference the :ref:`foil_aerodynamics:Case study` (Belloc's wing) and
  :doc:`demonstration` (my Hook3ish)


Advantages
----------

* Using arbitrary reference points is great because (1) they decouple the
  parameters (so you can change one without needing to modify the others) and
  (2) they allow the designer to directly target the aspects of the design
  they're interested in (eg, you don't have to specify rotation points)

* The equations are simple, so implementation is simple.

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

* Problems with the general surface equation

  * It's too flexible: it doesn't impose any restrictions on the values of the
    variables, meaning it allows design layouts that can't be (reasonably)
    analyzed using section coefficient data. It forces all the responsibility
    on the designer to produce a usable foil definition. [[This isn't a valid
    criticism; if someone abused it like that then that's their fault.]]

    It also doesn't impose any constraints on self-intersections.
    Self-intersections can occur if the chord surface is excessively curved
    (so the surface intersects itself), or if the thickness of an airfoil
    causes the inner surface of a radius to overlap. [[These are limitations
    of the general equation that are inherited by this parametrization. If
    I allowed section yaw then you'd have this issue for that too.]] I've
    accepted this limitation with the understanding that the equations are
    intended to be as simple as possible, and reasonable wing designs are
    unlikely to be impacted. If these geometric constraints are important for
    a design then the geometry can be validated as an additional
    post-processing step instead of polluting these equations.

  * It's not flexible enough: it requires the designer to use the section
    leading edges to position the sections. In many cases it is more
    convenient to position with other points, such as the quarter-chord,
    trailing edge, etc. [[If a designer wants to define a foil using some
    other reference point they cannot do it directly; they must specify the
    shape indirectly by manually calculating the corresponding leading edge
    position.]]

* I'm explicitly disallowing section-yaw (so no wedge-shaped segments), and
  assume that the section y-axes are all parallel to the body y-axis when the
  wing is flat. I'm not sure how accurate that is.

* Doesn't model internal structure (ribs, straps), and thus cannot model
  cells, cell distortions, and cannot account for the mass of the internal
  structure.

  Conceptually the abstracted section indices should enable a relatively
  simple mapping between inflated and deflated sections, but I never developed
  a suitable transformation to the section profiles.

* My choice of section index assumes a symmetric foil.
