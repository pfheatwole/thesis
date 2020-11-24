***************
Canopy Geometry
***************

.. Meta:

   A paraglider dynamics model requires the aerodynamics and inertial
   properties of the canopy, which can be estimated from the canopy geometry.

   This chapter develops a parametric parafoil canopy geometry. It starts with
   *wing sections*, which are the starting point for parametrizing a wing
   geometry (airfoil curves capture the structure of the profiles). Using the
   airfoil to provide the points in a local (airfoil) coordinate system
   establishes a general equation for points on the wing surfaces (chords,
   camber lines, or profiles). The sections must then be scaled, positioned,
   and oriented. The rest of this chapter focuses on a reparametrization of
   the general equation that makes it easier to design non-linear wing
   geometries. The reparametrization (1) enables designing position using
   points other than the leading edge, and (2) decouples the scale, position,
   and orientation parameters so they can be designed independently.

   The reparametrization makes it easier to design the overall wing (since
   components are independent) and makes it easier to use simple analytical
   definitions based on a small number of *design parameters* that capture the
   structure of the shape. [[The designer can choose whatever reference points
   allow for the simplest design parameters; eg, maybe the trailing edge is
   a perfect circle, but the leading edge is complex.]]


* What is a canopy?

  * The essential component of gliding flight is the lifting surface.

  * [[Examples of lifting surfaces. Typically symmetric, etc. In this case,
    we're interested in parafoils, which are simply a way of producing
    a lifting surface by inflating nylon through the intakes.]]

    .. figure:: figures/paraglider/geometry/Wikimedia_Nova_X-Act.jpg
       :width: 75%

       Paraglider side view.

       `Photograph <https://www.flickr.com/photos/69401216@N00/2820146477/>`__ by
       Pascal Vuylsteker, distributed under a CC-BY-SA 2.0 license.

* Why does this project need a mathematical model of the canopy geometry?

  * Flight reconstruction requires a dynamics model of the paraglider that
    produced the flight data.

  * Paraglider dynamics depend on the aerodynamics and inertial properties of
    the canopy.

  * There are elegant models that estimate wing performance based on a small
    number of summary parameters (lift coefficient, efficiency factor, etc)
    instead of requiring a complete wing geometry, but they are insufficient
    for this project:

    * They only apply to wings with straight wings. (Their results do not
      apply to the highly non-linear geometry of parafoil canopies.)

    * They only estimate the longitudinal dynamics (straight flight), and
      cannot be used to simulate turning dynamics or the presence of
      a crosswind.

    * They rely on linear aerodynamics that assume small angles of attack.
      Although canopy behavior is unpredictable near stall due to wing
      collapse, flight reconstruction requires a dynamics model with graceful
      degradation at higher angles of attack.

    * They don't provide inertial properties.

  * Conclusion: the aerodynamics and inertial properties of a canopy must be
    estimated from a mathematical model of the canopy geometry.

* To support the variety of aerodynamic methods, the model must be able to
  returns points on the section surfaces (chords, camber lines, and profiles).

* The conventional parametric approach to wing design is to use *wing
  sections*, which require specifying the scale, position, orientation, and
  profile of cross-sectional areas along the wing span. For the non-linear
  geometry of a parafoil canopy, defining those parameters directly can be
  unwieldy. Instead, it can be more convenient to work with a set of *design
  parameters* (span, taper ratio, elliptical function parameters, etc) that
  capture the underlying structure of the model.

* This chapter introduces a novel set of design parameters, and the equations
  that define position and orientation in terms of those parameters. The
  result is a novel geometry based on wing sections that is both flexible and
  particularly intuitive for designing non-linear wing geometries such as
  paraglider canopies.


.. Roadmap

This chapter will proceed as follows:

* Discuss the canopy geometry and some of the modeling considerations.

* Briefly consider explicit geometries, highlight their limitations, and
  respond with the advantages of parametric geometries.

* Introduce the standard parametric approach for wing designs: *wing sections*

* Introduce the general equation for points on section surfaces

* Establish why it is inconvenient to design a parafoil canopy by defining the
  variables of the general surface equation directly, and why it can be more
  convenient to define them in terms of *design parameters* that capture the
  structure of the canopy.

* Briefly consider existing parametrizations (particularly of position and
  orientation) and highlight their limitations.

* Introduce my novel parametrization.

* Provide examples of parafoil designs using my parametrization.

* Discussion


Paraglider canopies
===================

.. Describe the physical system (geometry, structure, materials, etc)

* What are the important aspects of a canopy geometry?

  * [[These details are important because they are the basis for recognizing
    the underlying structure of the wing, and thus they are the basis for
    parametric representations. The goal of a "good" parametrization is to let
    you use these "aspects" to produce a mathematical model.]]

  * [[What details of a canopy's shape are required (or at least useful) for
    defining a model that satisfies the needs of this project?

    These are not necessarily the variables you would choose to parametrize
    the geometry; they might simply be helpful for discussing/understanding
    the shape of a canopy. For example, anhedral is ambiguous, so I'm using
    Euler roll angles for section "anhedral". These are here to establish the
    details of the shape and thus the flexibility required by the
    parametrization.

    Related: "General aviation aircraft design" (Gudmundsson; 2013),
    chapter 9: "Anatomy of a wing"]]

  * *flat* versus *projected* values

  * *flat span*, *flat area*, *flat aspect ratio*

  * *projected span*, *projected area*, *projected aspect ratio*

  * There are also a variety of standard terms I will avoid due to ambiguity:
    *planform*, *mean aerodynamic chord*, maybe more? For *planform*, most
    texts assume the wing is flat and so the projected area is essentially
    equal to the flat area, and thus differentiating the two is largely
    neglected in standard aerodynamic works. The mean aerodynamic chord is
    a convenient metric for comparing flat wings and for simplifying some
    equations, but for wings with significant arc anhedral I'm not sure how
    beneficial this term really is; it's a mistake to compare wings based on
    the MAC alone, so I'd rather avoid any mistaken comparisons.

  * *dihedral*, *anhedral*: not sure how to define this for a wing. It's
    traditionally defined for flat wings, as `arctan(z/y)` of the section
    position, but that's pretty unhelpful for a paraglider. It also doesn't
    differentiate between `arctan(z/y)` and `arctan(dz/dy)` of a section. Still,
    discussing curvature leads nicely into a discussion of the *arc*, so
    whatever.

  * *arc* (Bruce Goldsmith calls it the "arc", the "Paraglider Design
    Handbook" calls it the "lobe")

  * *geometric torsion*: relative pitch angle of a section

    .. figure:: figures/paraglider/geometry/airfoil/geometric_torsion.*

       Geometric torsion.

       Note that this refers to the angle, and is the same regardless of any
       particular rotation point.

* [[Highlight why canopy geometries are tricky to model?]]


Modeling considerations
=======================


Functionality
-------------

.. Define the functional goals of the canopy model

* [[Model objectives v1]]:

  1. Be capable of capturing the relevant details of existing wings.

  2. Make it easy for users to describe existing wings.

  3. Support the queries necessary to use the geometry in aerodynamic methods.

     In particular, it should return the positions of points on the canopy
     surfaces: the chord surface, the mean camber surface, and the profile
     surface.

     [[The main requirement is that it does not lock the user into one
     specific method, like LLT, but don't focus on that here. I want to avoid
     any discussion of aerodynamics if possible.]]

* [[Model objectives v2]]:

  * [[The general requirement is that it enables estimating the inertial
    properties and aerodynamics, but the additional goals are that it should
    be: expressive, intuitive, able to use existing data, minimize the number
    of parameters (when reasonable), general enough to accommodate
    deformations (billowing, braking, accelerator, etc.

    There are existing parametrizations I could have used, so this is really
    about my extra demands that made the existing choices come up short.
    Driving that home will require some careful examples to establish the
    limitations of existing parametrizations.

    I think the biggest difference is that I chose to increase the complexity
    by adding the "reference point" parameters. I decided to pay the
    "simplicity" cost because of the "intuitive" gain; for elliptical chord
    lengths it was easier to adjust `r_x` than to find a parametric `x(s)`
    that shifted the chords into a reasonable approximation of real wings. In
    particular, most wings have a mostly-straight trailing edge that were
    a pain to encode using leading-edge reference points.]]

  * Makes it easy to specify a target design

    * Each design parameter should be intuitive and capture the target
      property directly (avoiding intermediate translations)

    * Makes it easy to incorporate existing design data. There are three main
      sources of information for the geometry of a paragliding canopy:

      1. Technical specifications (from researchers or a manufacturer)

      2. Pictures

      3. The wing itself

    * Support mixed-design between the flattened and inflated geometries.

      Parafoils only produce an arched geometry when they are inflated. It
      can be convenient to specify some values in terms of the non-inflated
      wing.

      [[A good choice of section index is key here. I should be able to
      define `c(s)` and `x(s)` by spreading a wing out on the grass and
      simply **measuring** the chord lengths and `x` positions of an edge.]]

    * Able to express continuous deformations [[from braking, C-riser
      piloting, accelerator flattening, weight shift, cell billowing, etc.]]

  * Minimizes the number of design parameters

    [[Should this be in the list of general goals? I already list "easy to
    use", but this goal is specifically targeted at simplifying statistical
    analysis. The structural knowledge of each parameter also tends to make
    them more amenable to statistical summarization.

    One long-term goal of this geometry is to allow people to encode
    approximations of existing wings. Once you've built up a database of
    models of physical wings you can generate a distribution over the wing
    parameters.

    Another "blue skies" goal is to produce a model that is amenable to
    statistical parameter estimation. This implies that as few parameters
    as possible should be used (to reduce the dimensionality). Also
    advantageous to decompose the parameters to maximize the variance of
    each parameter (ala principal component analysis); the choice of
    parameterization determines the parameter distributions, and it might
    be helpful to "eliminate" some of the variance by using stronger priors
    over some of the parameters. Like, instead of some complicated `X` you
    decompose into simpler `Y` and `Z`, then place a strong prior over `Z` or
    even treat `Z` as constant, so the only variance remaining is that in
    `Y`, which makes the parameter estimation easier.]]

  * [[Segue into "you can simplify both the specification and the analysis of
    a wing by decomposing it into a set of design parameters. The traditional
    way to do that is *wing sections*.]]


  * Supports the most common [broad-strokes] design parameters of
    a paraglider: airfoil, chord length, taper, geometric torsion, etc. (air
    intakes?)

  * Flexible enough that users can approximate existing designs (the choice of
    parametrization factors into this)

  * As simple as possible (intuitive to use, "frugal" in number of parameters)


Usability
---------

.. Parameters are how you specify the design. Motivate parametric models (as
   opposed to explicit geometries), define "parametrization", and establish
   the importance of choosing a good parametrization.

* [[To define a geometry, you can either use an explicit set of points or
  a set of parametric functions that generate the points.]]

* [[Define *explicit geometry*]]

  [[In a sense, explicit geometries are "infinite parametric" since you can
  add as much detail to the mesh as you want. Individual "parameters" (the
  points) don't capture any structure by themselves.]]

* [[Modeling with explicit geometries is too expensive (time consuming to
  produce, require too much information about the wing, difficult to analyze
  with simple aerodynamics, etc)]]

* [[Define *parametric geometry*]]

* [[Advantages of parametric geometries]]

  * Parametric designs try to balance simplicity and expressibility.
    Parameters "summarize" the structure. A good parametrization lets you
    focus on high-level design without forcing you into simplistic designs.
    [[I'm interested in "easy to create, good enough" approximations of real
    wings, not physically-realistic simulations.]]

  * Parametric models let you standardize so you can compared models.

  * Parametric models make it much easier to place priors over model
    configurations. (You can probably build a metric for explicit geometries,
    but it would be tough.)

  * Parametric models use fewer parameters, which makes them more amenable to
    mathematical optimization methods. This is helpful for statistical
    parameter estimation, or wing performance optimization.


.. Define the functional goals of the canopy model parametrization

* [[The choice of parametrization affects how useable it is. What would make
  a good parametrization?]]

  * Some goals of a parametrization:

    * Capable of capturing the most important details (as simple as possible,
      but no simpler)

    * Intuitive

    * Preferably map easily onto the most readily-available summary values
      (like span). It needs to make it easy to work with technical specs.

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


Designing with wing sections
============================

.. Introduce designing a wing using "wing sections"

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
  "planform" matches my idea of a chord surface.]]


.. figure:: figures/paraglider/geometry/wing_sections2.svg

   Wing section profiles.

   Note that section profiles are not the same thing as the ribs of a parafoil.
   Parafoil ribs are the internal structure that produce the desired section
   profile at specific points along the span.


Scale
-----

* The *scale* of a section is the scaling factor to produce the section
  profile from a normalized airfoil curve.

* How do you specify scale?

  * What is a chord?

    The *chord* of a section is the line connecting the leading edge to the
    trailing edge. The scale of a wing section is determined by the length of
    the chord.

  * The airfoils are scaled such that the camber line starts at the leading
    edge and terminates at the trailing edge of the section. (In other words,
    an airfoil is the section profile normalized by the chord length.)


Position
--------

* How do you specify position?

  * The position of a section is the vector from the wing origin to some
    reference point in the section-local coordinate system.

  * The leading edge of a wing section is the most common section-local origin
    because airfoils are traditionally defined with the leading edge as the
    origin. This choice is convenient since the wing section and the airfoil can
    share a coordinate system.

  * The most common reference point for the position is the leading edge, but
    other choices are possible.


Orientation
-----------

* How do you specify orientation?

  * The orientation of a section is the orientation of the section's local
    coordinate system relative to the wing's.

  * Can specify it explicitly using angles, or implicitly by specifying the
    shape of the position curves.

* [[From PDH: "washin promotes spanwise tension and stability, preventing the
  wing tips fold unexpectedly".

  It also encourages the wing to stall from the wing tips first; unlike plane
  wings, you want the middle of the wing to be the last to stall so you don't
  "taco" the canopy.]]


Profile
-------

[[Should I write a separate chapter about airfoils? Their purpose, geometry,
coefficients, behavior, etc. I don't like separating those topics, but I also
don't want to discuss section coefficients in this chapter. I do need some
geometry terminology here though, like *chord*, *camber line*, etc.]]

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


The section scale, position, and orientation define the *chord surface* of the
wing. [[**FIXME**: is a *chord surface* the same thing as a traditional
*planform*?]] The final step of defining the 3D wing shape is to assign each
section a cross-sectional profile called an *airfoil*.

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
*angle of attack*.

.. figure:: figures/paraglider/geometry/airfoil/NACA-6412-thickness-conventions.*
   :name: airfoil_thickness

   Airfoil thickness conventions.


General equation of a wing geometry
===================================

.. See `notes-2020w47:Canopy parametrizations` for a discussion

.. Introduce the general equation of points on the section surfaces

[[FIXME: define *surface* and their role in aerodynamics here?]]

A *canopy geometry* defines all the surfaces that describe the shape of the
canopy: the chord surface, the mean camber surface, and the profile surface.
In general, let any point `P` on any of those surfaces, given with respect to
the canopy origin `O`, be called :math:`r_{P/O}`.

The *general surface equation* for points :math:`P` on the section surfaces
(could be the chords, camber lines, or section profiles):

.. math::
   :label: general_surface_equation

   \begin{aligned}
   \vec{r}_{P/O}^c &= \vec{r}_{P/LE}^c + \vec{r}_{LE/O}^c\\
   \vec{r}_{P/LE}^c &= \mat{C}_{c/s} \mat{C}_{s/a} \vec{r}_{P/LE}^a\\
   \vec{r}_{LE/O}^c &= \;???
   \end{aligned}

Where :math:`\vec{r}_{P/LE}^a` is some point in the airfoil coordinate system
(most likely a point on the chord, on the mean camber line, or on the
profile), :math:`\mat{C}_{c/s}` is the *direction cosine matrix* that
transforms coordinates from the section (local) coordinate system to the
canopy (global) coordinate system, and :math:`\mat{C}_{s/a}` transforms
coordinates from the 2D airfoil coordinate system into the 3D section
coordinate system (Both `c` and `s` use `frd` coordinates).

[[FIXME: I'm calling this the general **surface** equation, but the points
don't have to lie on a surface: they're points **anywhere** in the airfoil
coordinate system (the xz-plane of the section).]]

[[The general equation is the result of designing via wing sections. The whole
point is that you start by defining the section profiles, then position them
relative to the canopy origin to produce the final wing. Splitting `r_P/O`
into `r_P/LE` and `r_LE/O` is the natural (general) result of designing with
wing sections; I suppose it's sort of a parametrization of the surfaces, but
that's not the "parametrization" I'll be talking about later. **I need to give
a more complete definition of the airfoil geometry in terms of `r_P/LE` before
I introduce the general equation to make it more obvious what those two
components mean.**]]

.. math::

   \mat{C}_{s/a} \defas \begin{bmatrix}
      -1 & 0 \\
      0 & 0\\
      0 & -1
   \end{bmatrix}


* The general equation is very expressive, but a bit of a pain to work with
  directly. It's easier to define the variables in terms of more convenient
  *design parameters*.


Existing parametrizations
=========================

.. There are already tools for designing wings using wing sections. Briefly
   discuss existing parametrizations and why they're not ideal for designing
   parafoil canopy geometries.

* Problems with the general surface equation

  * It's **too** flexible: it allows design layouts that can't be (reasonably)
    analyzed using section coefficient data, so a designer has to waste time
    being careful.

  * It's inconvenient: requiring the designer to specify the leading edge
    isn't always ideal (maybe you're trying to position the quarter-chord, the
    trailing edge, etc).

* Thankfully, those problems can be mitigated with a better parametrization.

* What do I mean by "parametrize the general equation"?

  [[I'm essentially saying "that set of design parameters is awkward, I want
  to choose a better set."]]

  The general parameters are able to represent any structure, but they don't
  encode enough structure. This is a problem because it pushes the work onto
  the designer. If you can assume more underlying structure you can save the
  designer from needing to provide that structure themselves. A good choice of
  parameters lets them focus on the important details.

  The purpose of a parametric surface is to decompose a complicated surface
  geometry into a set of simple design functions. The purpose of "parametric"
  functions (like an elliptical arc) is the **capture the structure** of the
  function, preferably with as few parameters as possible.

  (I feel like "parametric function" is poorly named, unless that's
  a conventional way to say "specify the values of a function through
  functions of some parameters instead of specifying the values directly".)


.. People are already designing wings using sections. Why don't I just use
   those tools?

* What are some existing parametrizations of the general equation?

  * [[Mostly how they define position and orientation. Assume scale is always
    an explicit chord length. Not sure about the section index.]]

  * [[PDH, Benedetti, MachUpX, XFLR5, AVL, etc. Present them as
    parametrizations of the general equation.]]

* What are the limitations of existing parametrizations?

  * [[The mathematical model is supposed to be flexible and easy to use. I'm
    developing a new parametrization which suggests the conventional choices
    fail somehow. Section profiles and scale already have standardized
    parametrizations, but there are a variety of ways to specify position and
    orientation. They typically use the projected section `y` coordinate for
    the section index, define fixed reference points for position, fixed
    rotation points (usually the leading edge), etc.]]

  * Some parametrizations only allow the designer to specify `y`, but for
    arched wings like parafoils it can be easier to specify `y_flat`

  * MachUpX specifies `x` via a `sweep` angle. That's not so bad, but it
    **only** supports that way of specifying `x`. It'd be nice if it supported
    other forms of `x(s)` (or `x(y)`, actually, since it uses `s = y` with
    a normalized span).

  * Fixed reference points dictate design specification.

    For example, a designer may want to design the trailing edge but the
    parametrization requires the design to be specified in terms of the
    leading edge. Forcing the user to specify their design using leading edge
    coordinates requires the designer to manually convert their design target
    into leading edge coordinates.

  * Tight coupling between the different dimensions of the design.

    Explicit rotation points are an indirect way of producing a desired
    design. The design goal is to specify two independent parameters, position
    and orientation, but because the choice of rotation point affects the
    final position of points on the chords it means that position is coupled
    to rotation.

    Similarly, if the reference points are at fixed locations on the chord,
    and the goal is to position some other point on the chord, then position
    is coupled to the chord length. Scale should not be coupled to position.


Optimized parametrization
=========================

.. Introduces a novel parametrization of the general equation that makes it
   easier to design parafoil canopies. Start by describing and "ideal"
   design workflow, and demonstrate the convenience of this result.

   Chooses a definition of the section index; defines independent reference
   points for x, y, and z; sets `r_y = r_z`; defines the section DCM using
   `dz/dy` and `\theta` (so you design `theta(s)` and `yz(s)` instead of
   specifying the section DCM directly).

.. Introduce my simplified parametrization for parafoils

It's annoying to design the section leading edges directly. Instead, define it
using more convenient design parameters:

.. math::

   \vec{r}_{LE/O}^c = \vec{r}_{RP/O}^c + \vec{r}_{LE/RP}^c

Where `RP` are as-yet nebulous "reference points" and :math:`\vec{r}_{RP/O}^c`
are the design curves (`x(s)` and `yz(s)`, in my case). This lets you choose
reference points other than the leading edges, and position those points
explicitly in the wing coordinate system. (Note that the leading edges remain
the origin of the section coordinate systems.)

In my case I chose to define the reference points using positions on the
section chords:

.. math::

   \vec{r}_{LE/RP}^c = \mat{R} \mat{C}_{c/s} c\, \hat{x}^s_s

.. math::

   \mat{R} \defas \begin{bmatrix}
      r_x & 0 & 0\\
      0 & r_{yz} & 0\\
      0 & 0 & r_{yz}
   \end{bmatrix}

* Some advantages of my parametrization:

  1. Make it particularly easy to capture the important details of a parafoil
     canopy

  2. Makes it easier to design in mixed flat and inflated geometries

  3. Supports aerodynamic analysis via section coefficient data (partly by
     keeping the y-axes in the yz-plane).


Examples of chord surfaces
==========================

.. Chord surface of designs made using the "optimized" parametrization.


Example 1
---------

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat1_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat1_canopy_chords.*


Example 2
---------

Words here.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat2_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat2_canopy_chords.*


Example 3
---------

Words here.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat3_canopy_chords.*


Example 4
---------

Words here.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_canopy_chords.*


Example 5
---------

[[FIXME: describe the "anhedral" correctly]]

A circular arc with a mean anhedral of 33 degrees:

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical1_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical1_canopy_chords.*


Example 6
---------

[[FIXME: describe the "anhedral" correctly]]

A circular arc with a mean anhedral of 44 degrees:

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical2_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical2_canopy_chords.*

Example 7
---------

[[FIXME: describe the "anhedral" correctly]]

An elliptical arc with a mean anhedral of 30 degrees and a wingtip anhedral of
89 degrees:

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_canopy_chords.*


Example: The Manta
------------------

The "manta ray" is a great demo for `r_x`.

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta1_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta1_canopy_chords.*

   "Manta ray" with :math:`r_x = 0`


.. figure:: figures/paraglider/geometry/canopy/examples/build/manta2_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta2_canopy_chords.*

   "Manta ray" with :math:`r_x = 0.5`


.. figure:: figures/paraglider/geometry/canopy/examples/build/manta3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/manta3_canopy_chords.*

   "Manta ray" with :math:`r_x = 1.0`



Examples of completed wings
===========================

Assigning a NACA 23015 airfoil to some of the previous examples:

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_canopy_airfoils.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical1_canopy_airfoils.*

Building a wing from 2D cross-sections also provides computational benefits
for estimating the aerodynamic performance of the 3D wing, as discussed in
:ref:`canopy_aerodynamics:Section Coefficients`.

[[Maybe link forward to :ref:`canopy_aerodynamics:Case Study`, where
I implement Belloc's wing using this geometry.]]


Discussion
==========

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

* I haven't described how to implement cells using parametric functions.

* Doesn't model structure like internal ribs


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
