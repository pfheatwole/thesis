.. This chapter generalizes the typical foil geometry equation to allow
   arbitrary reference points, relaxing the constraint that the geometry is
   specified in terms of the leading edge. This additional flexibility allows
   complex geometries to be described using simple parametric design curves.
   The parametric design curves encode domain expertise (reasonable
   assumptions about typical foil design), thus enabling complete parafoil
   geometries to be specified using only summary technical specifications.



* FIXME: Combine the "Foil specifications" and "Parametric modeling" into
  "Modeling requirements"? Seems like that section should work through what
  I'm trying to model and how the model is specified (parametrically).



*************
Foil geometry
*************

.. What is a foil?

The essential component of any flying object is the lifting surface.
A *lifting surface* is any part of an aircraft that produces *lift* when it
interacts with the air. By redirecting the airflow downward, the lifting
surface exchanges momentum with the air and produces the lifting force that
allows the aircraft to fly.

This paper refers to an arbitrary lifting surface as a *foil* instead of the
conventional *wing* or *canopy*. This unconventional term was chosen to avoid
two generalization issues. First, although *wing* is the conventional term for
the lifting surfaces of non-rotary aircraft, the paragliding community uses
the term *paraglider wing* to include not only the lifting surface but also
the supporting structure connected to it, such as suspension lines, risers,
etc. Second, although *canopy* is the term for the lifting surface of
a parafoil, the geometry developed in this chapter is not limited to parafoil
canopies.


.. Why does this project need to model the foil geometry?

An aerodynamics model requires the inertial properties and aerodynamics of the
foil, which can be estimated from the foil's shape.


.. Why not use existing wing modeling tools?

[[Short answer: this project is particularly interested in paraglider
dynamics, so it needs a foil geometry that allows me to specify a wing using
basic technical specs; the way to do that is with parametric functions, so **I
need a foil geometry that makes it easy to design parametric functions to
describe a parafoil geometry.** **I need a foil geometry that enables creating
complex foil geometries using simple parametric functions.** Existing tools
are inflexible, so nonlinear geometries like parafoil canopies cannot be
described using simple parametric functions.]]

An accurate model of a foil requires a complete set of specifications, but
those are unavailable for commercial paraglider wings. User manuals provide
valuable summary information, but the majority of the wing structure is
unspecified. Generating an approximate foil geometry from basic technical
specs requires making educated assumptions about the unknown structure. Those
assumptions are encoded in parametric functions that combine domain expertise
with the technical data to produce a fully specified model.

The trouble with existing methods lies in how the design of the parametric
functions depend on the variables they are defining; the general geometry
chooses the variables, which in turn determines the structure of the functions
that define those variables. Existing foil modeling tools impose unnecessary
constraints on how the geometry is specified, which forces unnecessary
complexity into the design curves (the rigidity forces the parametric
functions to adapt instead of letting the model adapt to the needs of the
parametric functions).

This chapter develops a generalized foil geometry that relaxes those
constraints by allowing arbitrary section reference points, which:

1. It decouples the design curves (so you can change them independently)

2. It lets the designer choose whatever local reference point is the most
   convenient.

The result is a novel geometry based on wing sections that is both flexible
and particularly intuitive for designing non-linear wing geometries such as
paraglider canopies. In particular, it satisfies the need for creating
parametric parafoil canopy models from basic technical specifications.


**The key thing about this generalized geometry is that it lets you use SIMPLE
design curves. Saying "arbitrary" suggests that allowing complex curves is
what's cool, but that's wrong: it's the fact that you can use simple functions
(constants, linear functions, ellipticals, etc) compose complex (highly
nonlinear) wings.**



.. Roadmap

   1. Discuss the physical system being modeled and its important details

   2. Review the incomplete geometry information from the readily available
      sources like technical specs, physical wing measurements, and pictures

   3. Consider how to create a complete geometry from the incomplete
      information by encoding domain expertise in parametric functions.

   4. Introduce parametric modeling using *wing sections*.

   5. Review the limitations of existing wing modeling tools (stemming from
      how they specify position and orientation)

   6. Develop a more flexible geometry model

      1. Derive a general equation equation that mitigates the limitations.

         The limitations of existing methods are due to constraints that
         appear by assuming specific wing shapes. Generalizing the geometry
         eliminates the constraints and adds extra flexibility that makes it
         a lot easier to specify the geometry using simple design curves.

      2. Parametrize the general equation.

         Explicitly defining the variables in the raw equation is unwieldy;
         parametrizing the pieces, such as assuming the sections are
         perpendicular to the yz-curve and that the geometric torsion is
         a simple scalar function of section index

      3. Define the parameters with *design curves*: parametric functions that
         encode the underlying structure of parafoil canopies using basic
         parameters that can be estimated from the available information (or
         from reasonable assumptions).

         These functions rely on domain expertise to "fill in the gaps" of the
         sparse technical data. For example, an elliptical chord distribution
         that only requires the root and tip lengths, or an elliptical
         yz-curve that only needs two (or even one) parameter by assuming an
         elliptical (or circular) arc.

   7. Show some examples using the new geometry model

   8. Demonstrate using the model to recreate a parafoil from literature.

   9. Discussion


Foil specifications
===================

.. This section elaborates on the details we need to model (chord
   distribution, etc), what data we know (span, area, etc), and what is
   required to produce a complete model from that minimal data.


.. The introduction explained that I don't have complete specifications for
   existing wings, and thus need to "fill in the blanks" with parametric
   design curves that use what little information I do know. I also claimed
   that existing tools make it difficult to use intuitive/efficient design
   curves, so I have to start by creating a more flexible geometry. So this
   chapter is about two things: 1) creating a flexible geometry so that 2)
   I can produce good design curves that make it easy to use the minimally
   available data.

   So this section should explain/detail that missing geometry information?

   Does this chapter introduce the design curves? I guess it must since I have
   example chord surfaces.

.. This section must:

   1. Draw attention to the geometry that must be modeled

   2. Introduce the most readily available specification data

   3. Establish that 

   1. Explain the complexity of parafoils that warrants a new geometry model

   2. Explain how design curves allow domain expertise to supplement the data


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
    "lobe" :cite:`casellasParagliderDesignHandbook`)

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


Modeling requirements
=====================

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


Design using sections
======================

.. Introduce designing a wing using "wing sections". They're the conventional
   starting point for parametrizing a wing geometry (airfoil curves capture the
   structure of the section profiles). Choosing to define the surfaces using
   points in the wing sections establishes the general form of the parametric
   model.

.. See `notes-2020w47:Canopy parametrizations` for a discussion


[[The premise of *wing sections* is that a 3D wing can be described using 2D
cross-sections. Each section is assigned a *profile* which is scaled,
positioned, and oriented, and together the 2D profiles produce the 3D wing
surfaces.]]


A foil geometry model defines the shape of a foil as a collection of surfaces:
the chord surface, the mean camber surface, and the profile surface. [[FIXME:
not sure I agree with this statement. Unclear. A shape is just a shape.
Granted, a foil geometry must PROVIDE those surfaces.]]

* [[We should have already established that we want a parametric model.]]

* [[There is already a standard parametric method for wings: *wing sections*]]

* Instead of designing the 3D shape directly, the wing is sliced into 2D
  cross-sections and the wing design process is decomposed into two steps:

  1. Specify the scale, position, and orientation of each section

  2. Specify the profile at each section, which defines the upper and lower
     surfaces.

  [[**Why are these just two steps? Why not four? Why not one?** They're all
  linked together, after all. If I'm not defining a "chord surface" then it's
  not clear that "scale, position, orientation" are fundamentally a group.
  **Counterpoint**: Gudmundsson says wing design is about designing two 2D
  components: the *planform* and the *profile*, so I guess his idea of
  "planform" sort of matches my idea of a chord surface, except that the chord
  surface is more like a 2D manifold in 3D (it's not restricted to a plane).]]

.. figure:: figures/paraglider/geometry/wing_sections2.svg

   Wing section profiles.

   Note that section profiles are not the same thing as the ribs of a parafoil.
   Parafoil ribs are the internal structure that produce the desired section
   profile at specific points along the span.

* The big idea behind using section profiles is that:

  1. They hide a lot of the geometric complexity. It's much MUCH easier to
     just say "NACA 24018" versus specifying the entire set of points.

  2. They enable analyzing the 2D sections independently from the 3D wing.
     It's not a perfect match, but you have a lot of control over the final 3D
     aerodynamics by choosing the 2D profiles.

  3. You can precompute the section coefficients, thus saving a ton of time
     when solving the 3D flow field (especially if viscous effects are
     included).


Section profiles
----------------

[[I feel like I should discuss these first since they define some of the
terminology I need, like *chord*. **FIXME**: can you define the geometry
without defining airfoils yet? Is it better that way?]]

[[Should I write a separate chapter about airfoils? (ed: **NO.**) Their
purpose, geometry, coefficients, behavior, etc. I don't like separating those
topics, but I also don't want to discuss section coefficients in this chapter.
I do need some geometry terminology here though, like *chord*, *camber line*,
etc.]]

[[**Key terms and concepts to define in this section**: upper surface, lower
surface, leading edge, trailing edge, chord line, mean camber line, thickness,
thickness convention, 2D aerodynamic coefficients.]]

Related work:

* :cite:`abbott1959TheoryWingSections`

* :cite:`bertin2014AerodynamicsEngineers`, Sec:5.2


.. Outline

   * Define *section profile* (airfoil)

   * Show how airfoils generate the upper and lower surfaces.

   * Discuss how the choice of airfoil effects wing performance

   * Discuss how the profile can vary along the span

   * Discuss how the profile behaves/changes in-flight

     Distortions due to billowing, braking, etc. (We will be ignoring these,
     but you can use the section indices to deal with them.)

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


General equation
----------------

Choosing to model a wing using wing sections means that the wing surfaces are
defined by airfoils, which are 2D curves that lie in the section-local
coordinate systems. By convention, points in the wing sections are defined
relative to the section leading edges, so all of the foil surfaces are
naturally defined in terms of points relative to the section leading edges.
[[FIXME: wording.]]

Let :math:`\mathrm{P}` represent any point in a wing section (such as points
on the section chords, mean camber lines, or profiles), and
:math:`\mathrm{LE}` be the leading edge of that section. In the `notation
<_common_notation>`_ of this paper, a general equation for the position of
that point :math:`\mathrm{P}` with respect to the foil origin
:math:`\mathrm{O}`, written in terms of the foil coordinate system :math:`c`,
is:

.. Unparametrized (explicit geometry?) equation

.. math::

   \vec{r}_{\mathrm{P}/\mathrm{O}}^c = \vec{r}_{P/LE}^c + \vec{r}_{LE/O}^c

In this paper, the foil coordinate system is defined by the foil *root* (the
central section). [[The foil coordinate system uses the coordinate system of
the central section for the xz-plane, and adds a y-axis according to the
right-hand rule.]] Points in section (local) coordinate systems :math:`s` must
be rotated into the foil (global) coordinate system. Given the *direction
cosine matrix* :math:`\mat{C}_{c/s}` between the section and foil coordinate
systems, the general equation for points relative to the foil origin can be
written in terms of points in section coordinates:

.. math::

   \vec{r}_{P/LE}^c = \mat{C}_{c/s} \vec{r}_{P/LE}^s

Furthermore, because an airfoil is defined in a 2D airfoil coordinate system,
another transformation is required, from airfoil coordinates to section
coordinates. The convention for airfoil coordinates places the origin at the
leading edge, with the x-axis pointing from the leading edge to the trailing
edge, and the y-axis oriented towards the upper surface. This paper uses
a front-right-down convention for the 3D section coordinates, so the 2D
airfoil coordinates can be transformed into 3D section coordinates with
a matrix transformation:

.. math::

   \mat{T}_{s/a} \defas \begin{bmatrix}
      -1 & 0 \\
      0 & 0\\
      0 & -1
   \end{bmatrix}

Lastly, by convention, airfoil geometries are normalized to a unit chord, so
the section geometry defined by the airfoil must be scaled by the section
chord :math:`c`. Writing the points in terms of scaled airfoil coordinates:

.. math::

   \vec{r}_{P/LE}^c = \mat{C}_{c/s} \mat{T}_{s/a} \, c \, \vec{r}_{P/LE}^a

.. This is the suboptimal "general" parametrization

The complete general equation is then:

.. math::

   \vec{r}_{\mathrm{P}/\mathrm{O}}^c =
     \mat{C}_{c/s} \mat{T}_{s/a} \, c \, \vec{r}_{P/LE}^a
     + \vec{r}_{LE/O}^c

In this form it is clear that a complete geometry definition requires
definitions of four variables:

1. Scale: :math:`c`

2. Position: :math:`\vec{r}_{LE/O}^c`

3. Orientation: :math:`\mat{C}_{c/s}`

4. Profile: :math:`\vec{r}_{P/LE}^a`

This general equation is very expressive, but a bit of a pain to work with
directly. It's often more convenient to define the variables in terms of
functions of simple *design parameters* that encode the significant structure
of the wing.


[[This "general equation" is an explicit, mathematical representation of the
basic/standard approach to wing modeling used by most tools. It's general, but
unwieldy. The real magic happens when I decompose `r_LE/O` so it can be
specified using an arbitrary reference point; that's the part that introduces
the flexibility that enables simplified parametric functions.

Important to recognize that my parametrization is simply a convenient way to
define these general variables; you could use my parametrization in existing
tools.]]


Parametric design
-----------------

.. Introduces a novel parametrization of the general equation that makes it
   easier to design parafoil canopies. Start by describing an "ideal" design
   workflow, and demonstrate how this result makes that possible.

   Chooses a definition of the section index; defines independent reference
   points for x, y, and z; sets `r_y = r_z`; defines the section DCM using
   `dz/dy` and `\theta` (so you design `theta(s)` and `yz(s)` instead of
   specifying the section DCM directly).


[[FIXME: I think I need two sections: "General equation" and "simplified
equation". The "general" equation keeps `R = diag(r_x, r_y, r_z)`, doesn't say
how to specify `C_c/s`, etc. The "simplified" version does things like setting
`r_y = r_z`, defining `C_c/s` using Euler angles, setting yaw=0,
roll=arctan(dz/dy), etc. The variables that must be defined to use the
simplified equation are more convenient for parafoils; that's when this new
geometry becomes amenable to parametric equations.]]


[[By this point I've introduced wing sections (the conventional starting point
for parametrizing a wing geometry) which naturally resulted in a general
equation that specifies the points on the wing surfaces (chords, camber lines,
or profiles) in terms of points in the section coordinate systems. The general
equation is defined in terms of four variables: scale, position, orientation,
and points. Each variable must be defined. Defining each variable explicitly
is a pain, so we want parametric functions of simple *design parameters* that
define the variables. The airfoil geometry already parametrized the points,
now I need to parametrize the others.]]


.. Introduce my simplified parametrization for parafoils

It's annoying to design the section leading edges directly. Instead, decompose
it into two separate vectors: one from the section origin (the section leading
edge) to some arbitrary *reference point* :math:`RP`, and one from the
reference point to the foil origin:

.. math::

   \vec{r}_{LE/O}^c = \vec{r}_{LE/RP}^c + \vec{r}_{RP/O}^c

Where `RP` are as-yet nebulous "reference points" and :math:`\vec{r}_{RP/O}^c`
is defined by the *design curves* (`x(s)` and `yz(s)`, in my case). This lets
you choose reference points other than the leading edges, and position those
points explicitly in the wing coordinate system. (Note that the leading edges
remain the origin of the section coordinate systems.)

[[Although the reference point can be any point in the section's coordinate
system, it is convenient to constrain it to be a point on the section chord,
in which case the reference point is a function of the chord ratio :math:`r`
such that :math:`\vec{r}_{\mathrm{LE}/\mathrm{RP}}^s = r\, c\, \hat{x}^s_s`,
where :math:`\hat{x}^s_s = \begin{bmatrix}1 & 0 & 0\end{bmatrix}^T` is the
section x-axis in the section coordinate system.

.. math::

   \vec{r}_{\mathrm{LE}/\mathrm{O}}^c =
         \vec{r}_{\mathrm{RP}/\mathrm{O}}^c
         + r\, \mat{C}_{c/s} c\, \hat{x}^s_s

This equation covers the majority of the choices for chord surface
parametrizations in common use. Designs that position the chords by specifying
their leading edge are equivalent to setting :math:`r = 0` and
:math:`\vec{r}_{\mathrm{RP}/\mathrm{O}}^c
= \vec{r}_{\mathrm{LE}/\mathrm{O}}^c`. Other designs use the quarter-chord
positions for the reference points, in which case :math:`r = 0.25`.

The problem with these fixed parametrizations is that they only support
a single reference point for design in all three dimensions. If a designer
wants to position the quarter-chord (:math:`r = 0.25`) along a circular arch
and the trailing edge (:math:`r = 1`) along a straight line, then they must
manually calculate the positions that would achieve that design for a given
reference point. It is much easier to allow different reference points for
each dimension.

Define:

.. math::

   \mat{R} \defas \begin{bmatrix}
      r_x & 0 & 0\\
      0 & r_y & 0\\
      0 & 0 & r_z
   \end{bmatrix}

The final form of the generalized equation for the leading edge, allowing
independent design curves and reference point for each of the position
dimensions, is then:

.. math::

   \vec{r}_{\mathrm{LE}/\mathrm{O}}^c =
     \vec{r}_{\mathrm{RP}/\mathrm{O}}^c
     + \mat{R} \mat{C}_{c/s} c\, \hat{x}^s_s

]]

The downside to a simple scalar `r` is that you have to use the same point
for specifying the section position in in all three dimensions. It is often
more convenient to use different reference points for different dimensions of
the position:

.. math::

   \vec{r}_{LE/RP}^c = \mat{R} \mat{C}_{c/s} c\, \hat{x}^s_s

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

[[The general equation given these choices is then:

.. math::

   \begin{aligned}
   r_{P/O}^c
     &= r_{P/LE}^c
        + r_{LE/RP}^c
        + r_{RP/O}^c \\
     &= \mat{C}_{c/s} \mat{T}_{s/a} \vec{r}_{P/LE}^a
        + \mat{R} \mat{C}_{c/s} c\, \hat{x}^s_s
        + \vec{r}_{RP/O}^c
   \end{aligned}


I say "general" because it'd be a reasonable target for code that implements
a general geometry defined in terms of wing sections. Parafoils et al could
reasonably defined using this form, using their own internal choices to define
these parameters. It'd be nice not to lock a model into a particular
parametrization of orientation, or reference point, or whatever. (Then again,
it does force the user into using a reference point on the chord, so "general"
is probably the wrong name. Also, the second form isn't immediately usable by
parametrizations that specify section scale/pitch/yaw by defining the LE and
TE as two points.)

To design a wing, specify: `c`, `C_c/s`, `r_P/LE`, `R`, and `r_RP/O`. **This
is almost exactly the same amount of work as before, you only need to add
`R`.** Minimal extra effort for a lot of convenience.]]

[[FIXME: define `C_c/s` here? I think I need to. Hrm, or actually, I should
finish the general equation without simplifying it too much, so keep things
like `R = diag(r_x, r_y, r_z)`. Choosing `r_y = r_z` should be explained
together with choosing to use `arctan(dz/dy)` to define the section roll
angle. **Avoid premature simplification. Finish the GENERAL equation, and then
make choices that make it more convenient for defining parafoils.**


Designing a chord surface with these equations requires five steps:

1. Define the *section index* :math:`s`

2. Define a scalar-valued function for the section scaling factors
   :math:`c(s)`

3. Choose the reference point positions on the chords :math:`\left\{ r_x(s),
   r_y(s), r_z(s) \right\}`.

4. Define a 3-vector valued function for the section reference point positions
   in wing coordinates :math:`\vec{r}_{RP/O}^c(s) = \left\langle x(s), y(s),
   z(s) \right\rangle`

5. Define the section orientation matrices :math:`\mat{C}_{c/s}(s)`



Namely, some choices that work well for parafoils:

* Let `r_y = r_z`

* Parametrize `C_c/s` using intrinsic Euler angles:

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
  of `c * C_c/s @ xhat` as a vector of derivatives: how much you would change
  in x, y, and z as you moved one chord length from the LE to the TE. The
  vector `c * C_c/s @ xhat` is essentially `<dx/dr, dy/dr, dz/dr>` (where `0
  <= r <= 1` is the parameter for choosing points along the chord). Applying
  `diag(r_x, r_y, r_z)` just scales them.

  Another way to get the intuition: imagine the trailing edge. You know that
  by definition it is `c * xhat` from the leading edge. Now imagine a point at
  `0.5 * c * xhat`. It's some delta-x, delta-y, delta-z away from the LE.
  These `r_x` etc are just scaling those deltas.


EXTRA
-----

* Problems with the general surface equation

  * It's too flexible: it doesn't impose any restrictions on the values of the
    variables, meaning it allows design layouts that can't be (reasonably)
    analyzed using section coefficient data. It forces all the responsibility
    on the designer to produce a useable wing definition.

  * It's not flexible enough: it requires the designer to use the section
    leading edges to position the sections. In many cases it is more
    convenient to position with other points, such as the quarter-chord,
    trailing edge, etc. [[If a designer wants to define a wing using some
    other reference point they cannot do it directly; they must specify the
    shape indirectly by manually calculating the corresponding leading edge
    position.]]

* [[The general equation is the result of designing via wing sections. The
  whole point is that you start by defining the section profiles, then
  position them relative to the foil origin to produce the final wing.
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

* :math:`\mat{C}_{c/s}` is the directed cosine matrix (DCM) of the wing
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
   \vec{r}_{P/O}^c
     &= \vec{r}_{LE/O}^c + \vec{r}_{P/LE}^c\\
     &= \vec{r}_{LE/O}^c - \vec{r}_{LE/P}^c\\
     &=
        \left(
          \vec{r}_{\mathrm{RP}/\mathrm{O}}^c
            + \mat{R} \mat{C}_{c/s} c\, \hat{x}^s_s
        \right)
        - r\, \mat{C}_{c/s} c\, \hat{x}^s_s\\
   \end{aligned}

Which simplifies to:

.. math::
   :label: chord_points

   \vec{r}_{P/O}^c =
      \vec{r}_{\mathrm{RP}/\mathrm{O}}^c
      + \left(\mat{R} - r\right) \mat{C}_{c/s} c\, \hat{x}^s_s

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
      + \mat{K} \hat{x}_s^c

Or, using separate equations instead of matrix math:

.. math::

   \begin{aligned}
   x &= x_r + (r_x - r) \hat{x}^c_x\\
   y &= y_r + (r_y - r) \hat{x}^c_y\\
   z &= z_r + (r_z - r) \hat{x}^c_z
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
