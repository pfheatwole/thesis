***************
Canopy Geometry
***************

1. What is a canopy?

   * The essential component of gliding flight is the lifting surface.

   * [[Examples of lifting surfaces. Typically symmetric, etc. In this case,
     we're interested in parafoils, which are simply a way of producing
     a lifting surface by inflating nylon through the intakes.]]

     .. figure:: figures/paraglider/geometry/Wikimedia_Nova_X-Act.jpg
        :width: 75%

        Paraglider side view.

        `Photograph <https://www.flickr.com/photos/69401216@N00/2820146477/>`_ by
        Pascal Vuylsteker, distributed under a CC-BY-SA 2.0 license.

#. Why does this project need a canopy geometry?

   * [[To estimate the inertial properties and aerodynamics]]

   * Paraglider dynamics depend on canopy aerodynamics and inertial
     properties. I'm generating new wing geometries, so these are unknown. If
     the aerodynamics and inertial properties of a canopy are unknown, they
     must be estimated from the geometry itself. [[In particular I plan to
     utilize the section coefficient data, but you could also use CFD, etc.]]

   * For straight wings there are elegant aerodynamics models that work well
     for small angles of attack, but those simple methods are based on linear
     relationships that do not hold for the highly non-linear geometry of
     a typical parafoil.

     [[Discuss how the discrepancy between linear theories and actual
     performance becomes more pronounced as alpha/beta increase. They also
     can't handle asymmetric wind, such as when the wing is turning.]]

#. What are the important aspects of a canopy geometry?

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
     *planform*, *mean aerodynamic chord*, maybe more? For *planform*, most texts
     assume the wing is flat and so the projected area is essentially the flat
     area, and thus differentiating the two is largely neglected in standard
     aerodynamic works. The mean aerodynamic chord is a convenient metric for
     comparing flat wings and for some simplifying equations, but for wings with
     significant arc anhedral I'm not sure how beneficial this term really is;
     it's a mistake to compare wings based on the MAC alone, so I'd rather avoid
     any mistaken comparisons.

   * *dihedral*, *anhedral*: not sure how to define this for a wing. It's
     traditionally defined for flat wings, as `arctan(z/y)` of the section
     position, but that's pretty unhelpful for a paraglider. It also doesn't
     differentiate between `arctan(z/y)` and `arctan(dz/dy)` of a section. Still,
     discussing curvature leads nicely into a discussion of the *arc*, so
     whatever.

   * *arc*

   * *geometric torsion*: relative pitch angle of a section

     .. figure:: figures/paraglider/geometry/airfoil/geometric_torsion.*

        Geometric torsion.

        Note that this refers to the angle, and is the same regardless of any
        particular rotation point.

#. Explicit vs parametric parametrizations.

   * Parametric designs try to balance simplicity and flexibility. A good
     parametrization lets you focus on high-level design without forcing you
     into simplistic designs. [[I'm interested in "easy to create, good
     enough" approximations of real wings, not physically-realistic
     simulations.]]

   * It's much easier to place a prior for parameters than for explicit
     geometries. (You'd have to invent parameters you can compute for an
     explicit geometry just so you can compare two canopies.)

#. What are **MY** requirements for a parametric model?

   * [[The general requirement is that it enables estimating the inertial
     properties and aerodynamics, but the additional goals are that it should
     be: expressive, intuitive, able to use existing data, minimize
     parameters, general enough to accommodate deformations (billowing,
     braking, accelerator, etc.

     There already exist parametrizations I could have used, so this is really
     about my extra demands that made the existing methods come up short.
     Driving that home will require some careful examples to establish the
     limitations of existing methods.

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


#. How do you design a mathematical model that achieves those requirements?

   * [[Through careful decomposition and parametrization. Introduce "wing
     sections" and how they simplify wing design using a two step process
     (specify the scale, position, and orientation of sections, then assign
     section profiles). Introduce the concept of section chords and the chord
     surface.]]

   * The shape of a parafoil canopy can be defined in many ways. The simplest
     way is to specify a set of points over the surface to produce an explicit
     representation of the shape. The issue is that the intricate, non-linear
     geometry of a parafoil requires a large number of points.

   * Instead of defining the shape with an explicit set of points, the complex
     shapes of parafoil canopies can usually be decomposed into a simpler set
     of parametric equations.

   * If a complex shape can be represented with simple parametric equations,
     then each parameter of the parametric equations tend to be better at
     capturing structural knowledge than the explicit set of points.

   * Because each parameter communicates more information than an explicit
     coordinate, fewer parameters are required, which tends to mean much less
     work is required to specify a design target.

   * The conventional way to decompose a wing is to use *wing sections*. Wing
     sections make a wing easier to design and easier to analyze.

     [[Discuss designing with chords + profiles versus designing the surfaces
     directly.]]

   * Instead of designing the 3D shape of a wing directly (ie, as a large set
     of points), simple wings are traditionally decomposed into 2D wing
     *sections* :cite:`abbott1959TheoryWingSections` distributed along the
     span.

     [[I don't like this phrasing: what does "directly" mean? Probably better
     to talk in terms of **structure**, since I'm thinking in terms of
     structured vs unstructured shapes; maybe use those terms?]]

   * [[What the advantages of designing with wing sections as opposed to
     designing arbitrary wing geometries? ie, what are the benefits of the
     structured approach of "design by wing sections"?]]

   * Designing the wing is then broken into two steps:

     1. Specify the scale, position, and orientation of each section.

     2. Assign a 2D profile to each section, called an *airfoil*, which
        defines the upper and lower surfaces of the section.

   * There are a variety of conventions for the first step. [[This is where
     you specify the chord surface. By "variety of conventions" what I mean is
     "variety of parametrizations", but they're all relatively similar.]]

.. figure:: figures/paraglider/geometry/wing_sections2.svg

   Wing section profiles.

   Note that section profiles are not the same thing as the ribs of a parafoil.
   Parafoil ribs are the internal structure that produce the desired section
   profile at specific points along the span.

#. What is the rest of the chapter about?


Related Work
============

* What are some examples of chord surface parametrizations?

  * **My design is very closely related** to the one in "Paraglider Design
    Handbook", except he requires explicit rotation points and he doesn't
    appear to allow different reference points for `x` and `yz`.

  * Benedetti :cite:`benedetti2012ParaglidersFlightDynamics` uses fixed `r_x
    = r_yz = 0.25`.


* What are some examples of parametric design parameters?

  * "Paraglider Design Handbook", :cite:`casellasParagliderDesignHandbook`

  * :cite:`lingard1995RamairParachuteDesign` [[Is this correct? Where/what are
    his design curves?]]


[[Also, "design by wing sections" is closely related to common 3D modelling
methods. It is similar to *lofting* in the sense that you are generating
a solid by interpolating between profiles at each section. It is similar to
*sweeping* a profile along a curve, except that the profile (the shape being
"swept") can change size (if the wing uses a non-constant chord), shape (if
the wing uses a non-uniform profile), and orientation (rotation of the profile
about the curve if there is geometric twist).

Another big difference is the use of separate curves for designing in the `x`
and `yz` planes, but you could probably convert this definition into a single
curve (eg, compute the final leading edge) and scaling factor (the chord
lengths scale the profiles). **This geometry should be straightforward to use
as an input to a 3D modeling program.** In fact, FreeCAD and Blender already
have Python API's, so this should be pretty easy to use this as a backend for
parametric geometries in those programs.]]


Chord Surface
=============

[[This section introduces a novel parametrization of the chord surface (the
"general equation"). Discuss conventional parametrizations (previous methods
of defining the chords), and the limitations of those old methods. Then
describe what "would" be a convenient workflow, and demonstrate the
convenience of this choice. In other words, introduce the general equation,
then introduce definitions of its parameters that make it easy to use to
define parafoils.]]

The first step of designing a wing using sections is to specify the scale,
position, and orientation of the sections.



* How do you specify scale?

  * What is a chord?

    The *chord* of a section is the line connecting the leading edge to the
    trailing edge. The scale of a wing section is determined by the length of
    the chord.

  * The section profiles are scaled such that the camber line starts at the
    leading edge and terminates at the trailing edge of the section. (In other
    words, section profiles are normalized by the chord length. An airfoil is
    the profile determined by the camber line, thickness function, and
    thickness convention; nothing more.)

* How do you specify position?

  * The position of a section is the vector from the wing origin to some
    reference point in the section-local coordinate system.

  * The leading edge of a wing section is the most common section-local origin
    because airfoils are traditionally defined with the leading edge as the
    origin. This choice is convenient since the wing section and the airfoil can
    share a coordinate system.

  * The most common reference point for the position is the leading edge, but
    other choices are possible.

* How do you specify orientation?

  * The orientation of a section is the orientation of the section's local
    coordinate system relative to the wing's.

  * Can specify it explicitly using angles, or implicitly by specifying the
    shape of the position curves.





* What is a chord surface?

  * Geometrically, a chord surface is the flat surface produced by all the
    section chords.

  * Mathematically, it is a function that returns points on the section
    chords.

  * It encodes the scale, position, and orientation of the wing sections.

  * The first step of designing a wing using wing sections is to specify the
    section chords.

* What are the conventional parametrizations of a chord surface?

  * The purpose of a parametric surface is to decompose the complicated
    surface into simple design functions. The purpose of "parametric"
    functions (like an elliptical arc) is the **capture the structure** of the
    function in as few parameters as possible.

    Note: I feel like "parametric function" is poorly named, unless that's
    a conventional way to say "specify the values of a function through
    functions of some parameters instead of specifying the values directly".

  * Discuss the common ways to describe a chord surface (eg, the section index
    is typically the section `y` coordinate, fixed reference points, explicit
    rotation points, etc)

* What are the limitations of conventional parametrizations?

  * [[The mathematical model is supposed to be flexible and easy to use. I'm
    developing a new parametrization which suggests the conventional choices
    fail somehow.]]

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

* How can those limitations be eliminated?

  * Present the general form of the leading edge derived in
    :ref:`derivations:General parametrization of a chord surface`

    [[Call out that parametric surfaces usually use `u` and `v` for the
    parameters?]]

  * Explain how the general equation establishes a standard set of parameters
    and design functions. The choice of parameters and design functions is
    intended to make it easy for a designer to communicate their design.

  * Discuss the parameters (`-1 <= s <= 1` and `0 <= r <= 1`; at least,
    I think those are the parameters? They are the arguments of the design
    functions.)

  * Discuss the design functions (`x(s)`, `C_w2s(s)`, etc)

    Those parameters can themselves be parametric functions of some
    (arbitrary) choice of section index. Discuss explicit vs parametric design
    curves (expressiveness versus number of parameters, essentially).

    Explain that some "functions" can be scalars, like `r_x(s) = 0`

    Note that at this point that although the design curves are parametrized
    by the section index it has only been defined as an arbitrary parameter
    that uniquely identifies a section (ie, the general form of the equation
    acknowledges that some index must exist, but leaves its definition
    unspecified).

  * Show how the general equation eliminates the limitations of the
    conventional definitions. (Able to specify design targets directly, able
    to design each dimension independently, etc.)



[[After establishing that the general equation can eliminate the limitations
of the general methods, I should be leading into "**how** can the general
equation be used to define parafoil geometries?" The general equation doesn't
say how to design those parameters


Choosing a parametrization
--------------------------

[[Title okay? This section is about choosing a **specific** parametrization of
the general equation that works well for defining parafoil canopies.]]

[[This chapter started by outlining the important details of a canopy
geometry. I then introduced a general parametrization which uses a set of
functions which make it intuitive to specify those important details. **The
problem is, it's TOO general**: it's possible to design layouts that you can't
reasonably analyze using section coefficient data. Thankfully, you can avoid
that problem by constraining/simplifying the parametrization a bit, which
leaves the designer with six "design functions". They're still general
functions, possibly with their own parameters, and so could be constants or
linear interpolators or whatever. Finish by showing some examples of section
layouts using those six functions.]]


[[I've been getting bogged down with this section, trying to decide how to
order the content. For example, do I list the constraints implied by the
desire to use coefficient data up front then refer back to it later, or do
I mention it while I'm choosing the orientation parameters?

Maybe I should try just saying up front what it's about: "Here's a generalized
set of parametric equations that describe the chord surface. They provide the
flexibility we need, but we can choose a specific parametrization that makes
it easier to work with while preventing some design mistakes."]]




* What are the constraints on wing design if the wing needs to be analyzed
  using section coefficient data?

  [[Are these relevant? Seems like the only thing I care about is the
  orientation. Maybe I should mention this when I'm parametrizing the DCMs?]]

  Segments must be able to be well-approximated as a single profile given
  a width. Things that cause this constraint be violated include:

  * Non-uniform profiles

  * Non-uniform torsion

  * Section y-axes are not parallel to each other (eg, wedge-shaped
    segments)

  * Section y-axes are not parallel to the segment quarter-chord (eg,
    "sheared" sections, like with swept wings or vertical sections with
    non-flat yz-curves)

* How do these "section coefficients analysis" constraints affect the choice
  of parametrization?

  * To keep the sections perpendicular to the segment span I set `r_y = `r_z`
    and use the derivatives of `yz` to define the section roll angle. (Not
    sure I'm actually required to set `r_y = r_z` for this to work, but it's
    more intuitive, and I prefer simpler designs.) [[**Does this belong
    here?** Or should it go in the "Orientation" subsection when I'm choosing
    the parametrization of the DCM?]]

* [[Should be left with the six "design functions" at this point. The 


Section index
^^^^^^^^^^^^^

[[I need to motivate my choice of section index, choosing `r_y = r_z` (to make
designing `yz` more intuitive), and using a roll-pitch Tait-Bryan sequence (or
a pitch-roll "proper" Euler angle sequence?) for the DCMs.]]

* *section index*: a unique identifier for each section.

* What I'm calling a "section index" is often called a "spanwise station" in
  literature. See "General Aviation Aircraft Design", Eq:9-36 (pg 319/325).
  I'll probably stick with this since it's more explicit (it's an index, so
  I'm going to call it that) plus I don't want any mixups between the classic
  definition of `spanwise station = 2y/b` (especially since that name doesn't
  say **which** span). Kinda nice that "station" and "section" both start with
  `s` though.

* My definition of the section index is similar to something used by Abbott,
  except he used `s = 2 * y / b` whereas I'm using the flat versions.

* Flat coordinates are useful since they can be measured from a wing lying on
  the ground.

* The arched versions are less convenient when sampling points along the
  span (as is done in Phillips).

* The traditional choices are the y-coordinate (so :math:`s \defas y`) or the
  normalized span coordinate (so :math:`s \defas 2 \frac{y}{b}`), but those
  become unwieldy for non-linear wings. (They are also non-constant if the
  wing is subject to deformations which change the section y-coordinates.) For
  parafoil design it's much more convenient to use the flat spanwise
  coordinate (this simplifies mixed design between the flattened and inflated
  wing shapes).

  Assuming the semispans are symmetric (reasonable for a parafoil), define:

  .. math::

     s \defas \, 2 \, \frac{y_\mathrm{flat}}{b_\mathrm{flat}}

* I'm using :math:`b_\mathrm{flat} = \mathrm{length}(yz(s))` even though the
  :math:`yz(s)` might not define the "true" physical span. (The reference
  points might not be the maximum y-coordinates.)


Scale
^^^^^

[[Interesting stuff about chord lengths goes here. This is about how you
specify the chord distribution, and not a discussion about wing design (taper,
aspect ratios, etc).]]

* You can specify chords as either a position and length, or as two
  positions (typically the leading and trailing edges). `FreeCAD` and
  `SingleSkin` do it that way; probably more?

  I suspect that the position+length representation lends itself to simpler
  equations, but it'd be interesting to check. For example, suppose
  a straight `0.7c` with an elliptical chord; what do the leading and
  trailing edge functions look like? Do they lose that nice,
  analytical-function look?

  Of course, the difference is a bit moot: if you have `LE(s)` and `TE(s)`,
  just set `r_x = 0` and `c(s) = norm(LE(s) - TE(s))`.


Position
^^^^^^^^

[[Interesting stuff on positioning sections goes here. Leading edge, trailing
edge, quarter-chord, whatever.]]

* What is :math:`yz(s)`? In short, for each section of the wing, pick the
  point at :math:`r_{yz} \, c` back from the leading edge. Project that
  point onto the yz-plane. Do this for all sections to produce a curve. The
  :math:`s` is the normalized length along that curve. The length of that
  curve also defines :math:`b_\mathrm{flat}`, since it would be the span of
  the reference line if you "unrolled" the wing so all the z-coordinates are
  zero.

* Point out that although the "leading edge" and "trailing edge" of the
  airfoil is defined by the camber line (which in turn defines the chord
  line), the chord line of the airfoil is ultimately just a way of
  positioning the profile onto the chord surface. You could choose any
  arbitrary line, you just need to make sure that whatever line you use to
  generate the coefficients matches the orientation and scale of the profile
  you assign to the final wing.


Orientation
^^^^^^^^^^^

* The general equation of the chord surface requires the section DCMs to
  determine the section x-axes, thus wing design requires DCM design.

* Section DCMs can be decomposed into intuitive design parameters by defining
  the section orientations as Euler angles. The decomposition also facilitates
  mixed-design of the flattened and inflated wing geometries. [[How?]]

* Euler angles can be encoded using "intrinsic" or "extrinsic" axes: intrinsic
  rotations are rotations about the body-fixed axes, extrinsic rotations are
  about the axes that are fixed in the object being rotated. Intrinsic
  (body-fixed) rotations are referred to as "proper Euler" angles; extrinsic
  (object-fixed) rotations are referred to as "Tait-Bryan" angles.

* I've chosen to parametrize the section orientations as an intrinsic
  pitch-roll sequence, so :math:`\phi` for section dihedral and :math:`\theta`
  for section torsion.

  Note that this breaks with my earlier work that refers to "section dihedral"
  as :math:`\Gamma`. I decided to abandon :math:`\Gamma` as the parametrization
  (how you **specify** section orientation) for several reason:

  1. Section dihedral is a pain to define in an unambiguous way for wings with
     geometric torsion: do you use the angle between the body y-axis and (a) the
     section y-axis or (b) the projection of the section y-axis onto the
     yz-plane?

  2. :math:`\Gamma` already has a conventional definition as **wing** dihedral
     (overloading it to refer to section dihedral is not ideal)

  3. I've been trying to always use right-handed rotations for everything, but
     the conventional definition of a positive dihedral angle corresponds to
     a negative right-handed rotation about the +x-axis.

  4. Euler angles already have well established conventions for the angle
     variables (phi, theta, gamma).

  In short, a formal definition of section dihedral angles might be an
  interesting concept from the perspective of wing analysis, but for wing
  design it's not very helpful.

* The way I've designed section roll and pitch correspond to either an
  intrinsic pitch-roll sequence or an extrinsic roll-pitch sequence. (How do
  the matrices compare? So far my definition has been using intrinsic angles;
  should I stick with that? What does the extrinsic pitching rotation matrix
  look like? Keep in mind, I want to define the roll matrix using `dz/ds` and
  `dy/ds`.) One advantage is conceptual: assuming the wing starts out flat,
  you can think of the section torsion as happening first, so pitch-roll is
  intuitive.

* This DCM parametrization keeps the section y-axes in the yz-plane (ie, it
  ignores `dx/ds`). Positioning with `x(s)` simply shifts the sections
  ("shears the chords") into position with no rotation with no rotation about
  the z-axis. (I'm pretty sure this is a reasonable constraint for most wing
  designs? Using wing section coefficient data assumes the wing segment can be
  described by taking a uniform section profile and stretching it by some
  width; if the sections in the segment have section yaw, then then segment
  would be a wedge, and the "linear segment" approximation falls apart.)

  Related: https://www.youtube.com/watch?v=w1AuPn_oBnU. I suspect that they
  aren't reorienting the profiles but are simply reorienting the ribs to
  minimize cross-flow. Simple concept, you just need to compute the
  "typical" airflow for a point on the wing and slice the wing along that
  airfoil (so the ribs won't match the section profiles anymore).

* Using `yz` to define `phi` keeps the sections perpendicular to the segment
  spans, plus it reduces the number of parameters.


[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

* Might be good to define washin, washout, angle of incidence, mounting angle,
  etc. There's quite a bit of confusion around those terms, so I'm explicitly
  trying to avoid using them at all. I'm using the angle relative to the
  central chord, that's it.

* *geometric torsion*: the section orientation angle produced by
  a right-handed rotation about the wing y-axis

  Or, the angle from the wing x-axis to the section x-axis, as produced by
  a right-handed rotation about the wing y-axis

  .. math::
     :label: section_torsion

     \Theta \defas
        \arctan \left(
           \frac
              {\vec{\hat{x}}_\mathrm{wing} \times \vec{\hat{x}}_\mathrm{section}}
              {\vec{\hat{x}}_\mathrm{wing} \cdot \vec{\hat{x}}_\mathrm{section}}
           \cdot \vec{\hat{y}}_\mathrm{wing}
        \right)

  From the definition of the torsion angle :math:`\Theta` in
  :eq:`section_torsion` you have the rotation matrices for geometric torsion:

  .. math::
     :label: section_torsion_matrix

     \mat{\Theta} &\defas \begin{bmatrix}
        \cos(\theta) & 0 & \sin(\theta)\\
        0 & 1 & 0\\
        -\sin(\theta) & 0 & \cos(\theta)
     \end{bmatrix}

* *section anhedral*: the angle from the wing y-axis to the section y-axis, as
  produced by a right-handed rotation about the wing x-axis.

  Note that this mathematical definition of the anhedral angle is different
  from the conventional definition of dihedral angle. The convention for wing
  dihedral is that the angle is measured as the positive "upwards" angle of
  the wing. That definition is ambiguous, so this definition uses signed
  angles and standard right-hand rules.

  [[FIXME: **I need to choose** a standard term: dihedral or anhedral. I think
  I prefer dihedral simply because it's more common, and if I use `\Gamma` I'd
  like it to agree with convention. There is the downside that it's
  a **negated** right-hand rotation about the +x-axis, but if I'm not using
  `Gamma` to define the section orientations it probably doesn't matter.]]

  .. math::
     :label: section_dihedral

     \Gamma \defas
        \arctan \left(
           \frac
              {\vec{\hat{y}}_\mathrm{wing} \times \vec{\hat{y}}_\mathrm{section}}
              {\vec{\hat{y}}_\mathrm{wing} \cdot \vec{\hat{y}}_\mathrm{section}}
           \cdot \vec{\hat{x}}_\mathrm{wing}
        \right)

  To use the airfoil data you need the spanwise axis of the wing segments to
  be parallel to the wing sections that comprise the segment. (At least,
  I think that's the case: I doubt the airfoil coefficients would be accurate
  if the sections were slanted relative to the segment span.) You can enforce
  this parallel alignment by constraining the section dihedral to stay
  orthogonal to the yz-curve, which is why I define the dihedral with the
  derivatives of `yz`. If you didn't do that you'd have a sort of shearing of
  the sections along the segment.

  Oh, I bet this is also related to why lifting-line methods fail for swept
  wings; part of that is because of spanwise flow, but you also have sections
  y-axes that don't align with the segment!]]

  From the definition of the dihedral angle :math:`\Gamma` in
  :eq:`section_dihedral` you have the rotation matrices for section dihedral:

  .. math::
     :label: section_dihedral_matrix

     \mat{\Gamma} &\defas \begin{bmatrix}
        1 & 0 & 0\\
        0 & \cos(\Gamma) & -\sin(\Gamma)\\
        0 & \sin(\Gamma) & \cos(\Gamma)
     \end{bmatrix}

  The disadvantage of :eq:`section_dihedral_matrix` is its dependence on the
  arctangent function in :eq:`section_dihedral`, which is undefined for wing
  sections that achieve a 90° section dihedral. To avoid the divide by zero,
  the matrix can be computed using the derivatives of the arc reference
  curves:

  .. math::
     :label: section_dihedral_alternative

     \Gamma = \arctan \left( \frac{dz}{dy} \right)

  .. math::

     \begin{aligned}
     K &= \frac{1}{\sqrt{\left(dy/ds\right)^2 + \left(dz/ds\right)^2}}\\
     \\
     \mat{\Gamma} &= \frac{1}{K} \begin{bmatrix}
        K & 0 & 0\\
        0 & dy/ds & -dz/ds\\
        0 & dz/ds & dy/ds
     \end{bmatrix}
     \end{aligned}

* Section direction-cosine matrix (DCM):

  .. math::
     :label: section_DCM

     \mat{C}_{w/s} = \mat{\Gamma} \mat{\Theta}

* Section :math:`x`-axis:

  .. math::

     \vec{\hat{x}} = \mat{\Gamma} \mat{\Theta} \begin{bmatrix}1\\0\\0\end{bmatrix}

* I think this design happened because I wanted the arc (yz-curve) to define
  the section orientation. The wing starts flat, then the lines pull various
  sections downwards (and inwards), which is why I start with a flat wing and
  then rotate it about the global x-axis (not the section x-axes): it was
  simply easier for me to reason about. Oh, and **to compute the final angle
  of a section you don't have to integrate over all the section-local
  angles.** 

  Consider what would happen if the yz-curve did not define the section
  orientation: you would have section profiles sheared along the curve, their
  y-axes not parallel to the segment span. You are going to get some funky
  cross-flow due to spanwise pressure gradients (section coefficients assume
  uniform pressure distributions along the segment span) so the section
  coefficients are unlikely to be representative of the actual behavior.

  (Hm, **how does this work with wing sweep?** I'm not allowing section yaw,
  but if the wing is swept then the section y-axes are not parallel to the
  quarter-chord segment.)

  **If I state up front that I want a simple geometry that's amenable to
  analysis by wing coefficients, then these choices are well motivated.** Of
  course, I can't yet define or analyze billowing cells but ah well.

  Aah, okay, I get it now: you start by designing the flat wing. I'm assuming
  that when the wing is flat the only thing you design is `c(s)`, `x(s)`, and
  `theta(s)`: the wing is flat, so that rotation is naturally about the wing
  (global) y-axis. You then use the line geometry to pull down on the sections,
  and I assume that pulling down will produce a bending, not a shearing, of the
  wing segments; also, the lines don't know (or care) about the section x-axes,
  they which is why dihedral is rotation about the global x-axis. It's all
  about the sequence of events.

* The choice of parametrization of the section orientation arises from the
  intuitive sequence of wing design. You start by laying out the wing sections
  of the flat wing; the section y-axes start parallel to the body y-axis, and
  geometric torsion leaves them that way. You then use the line geometry to
  pull down on the sections to produce the yz-curve; the lines are assumed to
  pull straight down without distorting the section profiles, which means
  bending the cells, not shearing them.

  These assumptions are probably a bit strong for "real" wing design. In
  particular, the assumption that the section y-axes all start parallel to the
  body y-axis. Assuming no relative yaw is also suspect; just because it makes
  analysis with section coefficients more difficult doesn't mean wing
  designers don't do it.


EXTRA NOTES
-----------

* General

  * I didn't invent this notion of a chord surface: I merely gave it a name.
    And my contribution isn't a "new parametric geometry": I'm contributing
    a general equation for the surface, and a particular choice of section
    index and design function parametrization (the DCM is parametrized by
    Euler angles, section roll being defined by `yz(s)`) for that equation
    that make it easy to (1) capture the important details of a parafoil
    canopy, (2) design in mixed flat and inflated geometries, and (3) analyze
    the aerodynamics using section coefficient data (partly by keeping the
    y-axes in the yz-plane).

  * For notational simplicity, I'm going to drop the explicit section index
    parameter :math:`s`, so  :math:`LE(s) \to LE`, :math:`r_x(s) \to r_x`,
    etc.


Examples
--------


Example 1
^^^^^^^^^

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat1_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat1_canopy_chords.*


Example 2
^^^^^^^^^

Words here.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat2_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat2_canopy_chords.*


Example 3
^^^^^^^^^

Words here.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat3_canopy_chords.*


Example 4
^^^^^^^^^

Words here.

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_canopy_chords.*


Example 5
^^^^^^^^^

A circular arc with a mean anhedral of 33 degrees:

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical1_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical1_canopy_chords.*


Example 6
^^^^^^^^^

A circular arc with a mean anhedral of 44 degrees:

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical2_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical2_canopy_chords.*

Example 7
^^^^^^^^^

An elliptical arc with a mean anhedral of 30 degrees and a wingtip anhedral of
89 degrees:

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical3_canopy_chords.*


Example: The Manta
^^^^^^^^^^^^^^^^^^

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


Foil Surface
============

The chord surface is the flat surface produced by all the section chord. To
produce the 3D canopy, each section must be assigned an airfoil.


Outline:

* Describe section profiles (airfoils)

* Show how assigning section profiles to a chord surface generates the upper
  and lower surfaces.

* Derive (or simply present) the function that returns points on the upper and
  lower surfaces given a chord surface and section profiles

* Show some examples of completed canopies.


Airfoils
--------

Related work:

* :cite:`abbott1959TheoryWingSections`

[[**Key terms and concepts to define in this section**: upper surface, lower
surface, leading edge, trailing edge, chord line, mean camber line, thickness,
thickness convention, 2D aerodynamic coefficients.]]

After designing the section chords, the chord surface will produce a 3D wing
by assigning each section a cross-sectional geometry called an *airfoil*.

.. figure:: figures/paraglider/geometry/airfoil/airfoil_examples.*

   Airfoils examples.

An airfoil is a 2D profile defined by a camber line, a thickness function, and
a thickness convention.

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


Examples
--------

Assigning a NACA 23015 airfoil to some of the previous examples:

.. figure:: figures/paraglider/geometry/canopy/examples/build/flat4_canopy_airfoils.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/elliptical1_canopy_airfoils.*

Building a wing from 2D cross-sections also provides computational benefits
for estimating the aerodynamic performance of the 3D wing, as discussed in
:ref:`canopy_aerodynamics:Section Coefficients`.

[[Maybe link forward to :ref:`canopy_aerodynamics:Case Study`, where
I implement Belloc's wing using this geometry.]]


Distortions
-----------

**FIXME**: should I discuss cells, billowing, distortion, etc? I'm not working
on / implementing these, so they can probably go in the "Limitations" section
(whatever that turns out to be)

References:

* Babinksy (:cite:`babinsky1999AerodynamicPerformanceParagliders`) discusses
  the effect of billowing on flow separation, and
  :cite:`babinsky1999AerodynamicImprovementsParaglider` discusses using
  stiffeners to reduce the impact

* Kulhanek (:cite:`kulhanek2019IdentificationDegradationAerodynamic`) has
  brief discussion of these impacts

* Belloc (:cite:`belloc2016InfluenceAirInlet`) discusses the effects of air
  intakes, and suggests some modeling choices

* There are a bunch of papers on *fluid-structure interaction* modelling.

* Altmann (:cite:`altmann2009NumericalSimulationParafoil`) discusses the
  overall impact of cell billowing on glide performance, and has a great
  discussion of how design choices (cell structure, ribs, etc) can mitigate
  the problem; in future papers
  (:cite:`altmann2015FluidStructureInteractionAnalysis`,
  :cite:`altmann2019FluidStructureInteractionAnalysis`) he discusses
  implementation details. Fogell
  (:cite:`fogell2014FluidstructureInteractionSimulations`,
  :cite:`fogell2017FluidStructureInteractionSimulation`,
  :cite:`fogell2017FluidStructureInteractionSimulations`) has a lot to say
  on FSI, including some critique of the applicability of Altmann's method
  to parachutes.

  Another recent paper well worth reviewing (good discussions and great
  references list) is :cite:`lolies2019NumericalMethodsEfficient`, which is
  co-authored by Bruce Goldsmith! Neat. One of their big ideas seems to be
  using "mass-spring systems" from computer animation applications for
  paraglider cloth simulations.


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
