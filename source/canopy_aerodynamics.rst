*******************
Canopy Aerodynamics
*******************

.. The previous chapter produced an approximate canopy geometry model from the
   basic technical specs. This chapter needs to use that geometry to estimate
   the canopy aerodynamics.


.. What are *aerodynamics*?

Aerodynamics describe the forces and moments produced when an object moves
through air.


.. Why does this project need the canopy aerodynamics?

[[The paraglider dynamics model needs all the forces and moments of the
glider, which come from Earth's gravity and the air.]]


.. How do you determine the canopy aerodynamics?

* [[Theoretical (predict) vs experimental (measure) approaches to determining
  wing performance.]]

  Ideally you'd just measure them experimentally, but for this project we have
  to use theoretical methods.

* *Computational aerodynamics* produce numerical solutions to the governing
  equations. They combine a model of the wing geometry with a set of boundary
  conditions to solve for the flow field around the wing.

* There are many different methods. Each one comes with a different set of
  assumptions. Their designs involve tradeoffs that limit their applicability
  to different situations.

* Conclusion: we need to choose a suitable aerodynamics method and acquire an
  implementation.

* [[There are existing methods in literature, but I need to define my
  performance criteria before claiming they are inadequate. This might be
  a good spot to acknowledge their existence, but defer their discussion.]]


.. Roadmap:

This chapter will proceed as follows:

* Introduce computational aerodynamics

* Establish the modeling requirements in the context of flight reconstruction

* Discuss the different categories of aerodynamics models in the context of
  the requirements and make a selection (Phillips' NLLT)

* Discuss the selected aerodynamic method 

* Present tests using the selected method

* Discussion


Modeling requirements
=====================

.. Establish the performance criteria for this project. I need an aerodynamics
   method that can handle the unusual geometry of a paraglider canopy under
   expected flight conditions.

* [[Define the variety of "typical flight conditions" in the context of this
  paper. Wind gradients, wing rotation, etc: the aerodynamics method must be
  able to handle it.]]

* [[What modeling fidelity do I need?]]

  * Supports arbitrary non-linear geometry

    * Do not assume a straight lifting-line (allow both sweep and dihedral)

    * Do not assume a circular arc (ala `gonzalez1993`)

  * Supports non-linear lift

    * Do not assume a constant lift-slope (applies to both the complete and
      the individual section coefficients)

    * Do not assume brake deflections simply shift the section lift curves

    * Do not assume a constant Reynolds number (these vary quite a lot due to
      taper, especially at such low airspeeds)

    * Require graceful degradation near stall

      [[When I talk about "graceful degradation", I should probably explain it
      in the sense of "the wing tips tend to start stalling first, but their
      contributions are relatively minor overall, so inaccuracies in the wing
      tip forces does not contribute a large error to the overall force
      estimate and should not preclude the method from providing functional,
      albeit degraded, accuracy."]]

    * [[Non-linearities come from a variety of sources: the geometry
      (particularly the arc?), viscosity (boundary layer effects are
      significant for parafoils), non-uniform wind (turning, wind gradients,
      etc)

      **Don't just assume linear aerodynamics; confirm it.**]]

    * I'm already using a rigid body assumption, so I'm committed to an
      imperfect model. I accept that I can't handle stall conditions (so
      flight reconstruction is limited to "average" flight conditions), but
      the simulator does need graceful degradation when approaching stall
      conditions.

  * Supports non-uniform wind (turning maneuvers, wind gradients)

  * Supports viscous effects and empirical adjustments (mostly viscous drag
    correction factors)

    [[These exist in literature. I want to be able to use them. Can
    incorporate them either by adding them directly to the drag coefficient
    (as I do for Phillips method), or via strip theory.

    Sources:

    * :cite:`kulhanek2019IdentificationDegradationAerodynamic`: the purpose of
      the paper is to "quantify the amount of aerodynamic drag related to the
      flexible nature of the wing.

      Uses a coefficient `C_d,f` which "takes into account all the effects
      related to the flexible nature of the wing, such as deformation of the
      leading edge, cell opening, skin wrinkling, airfoil and trailing edge
      thickening, etc." See Fig:12 in particular. **I should review my choices
      of viscous adjustments.**

    * "Aerodynamic Research of the Airfoils for the Paragliders" (Pohl, 2011):
      linked by Kulhanek, but I can't find a copy of this one

    * :cite:`ware1969WindtunnelInvestigationRamair`: Provides an estimate of
      drag due to "surface characteristics". Also provides an estimate of the
      "air intake drag coefficient", but that's superseded by `babinsky1999`.

    * :cite:`lingard1986AerodynamicsGlidingParachutes`

    * :cite:`babinsky1999AerodynamicPerformanceParagliders`: I'm using his
      estimate for "air drag due to air intakes".

    ]]

  * Computationally efficient/fast

    * The underlying goal of this paper is flight reconstruction, and
      a particle filter would need to generate a huge number of simulations,
      so the aerodynamics must be fast.

    * Ultimately this method is likely to be replaced with an approximation,
      but it's still nice to work with the "full" model whenever possible.

  * Nice to have: avoid external dependencies

    * I'm trying to keep this self-contained, since I wanted to understand
      what's happening end-to-end. Also let me design it just how I wanted,
      which also enabled simplified interfaces.

    * Side effect: needs to be feasible to implement given my time constraints

[[In practice a lot of these are overkill, but **the whole point is to
VERIFY** which terms matter and which don't. I was fed up with papers just
assuming everything is linear, constant Reynolds number, etc etc, without
verification.]]


Aerodynamics models
===================

.. Survey the available models and the tradeoffs they involve.

* [[What categories of aerodynamics methods are available?

  Introduce LLT, VLM, CFD, etc. Go through the requirements and explain why
  they fail (LLT fails with non-linear geometry, VLM handles non-linear
  geometry but assumes linear aerodynamics (and neglects thickness, which can
  be significant for parafoils), CFD is too complicated to implement and too
  slow). Only the NLLT met my requirements.

  [[For the theoretical approaches, compare analytical vs numerical
  (computational) solutions to the governing equations.
  :cite:`cummings2015AppliedComputationalAerodynamics`]]

  Also, a great reference: :cite:`drela2014FlightVehicleAerodynamics`]]

* [[What kinds of assumptions do they make? (viscosity, spanwise flow, flow
  separation, linear coefficients, uniform wind, etc)]]

* [[Section profiles were covered in the previous chapter. The computational
  methods use the profiles either via their section coefficients, or via the
  surface geometry they generate.]]


.. Critique the models in the context of this project

* [[Some of these are used in literature to estimate the performance of
  parafoils. Explain why methods that work for other papers do not meet the
  performance criteria for **this** project.]]


.. Select an appropriate model for this project

* Only the NLLT met my requirements. It's an extension of LLT to account for
  3D effects. It's computationally efficient, handles non-linear geometry,
  does not assume constant or linear aerodynamic coefficients, allows for
  viscous corrections, and is relatively simple to implement (so I can
  implement my own instead of relying on external dependencies).


Phillips' numerical lifting-line
================================

.. Explain the method, review its design, describe my improvements, and
   discuss my implementation.

* **Phillips' original derivation assumes uniform flow** for Eq:5, but I'm
  using the non-uniform version from Hunsaker-Snyder Eq:5. Hunsaker mentions
  that this *local upstream velocity* `V_rel,i` "differs from the global
  freestream velocity `V_inf` in that it may also have contributions from
  prop-wash **or rotations of the lifting surface about the aircraft center of
  gravity.**" Is he implying that Phillips' method is useable as-is during
  rotations?

* "The lifting-line theory of Phillips and Snyder (2000) is in reality the
  vortex-lattice method applied using only a single lattice element in the
  chordwise direction for each spanwise subdivision of the wing."
  (Aerodynamics for Engineers, pg 383).

  Interesting: useful to keep in mind when validating an implementation by
  comparing it to a full lattice method.

* Why am I choosing this method? It provides a reasonable tradeoff between
  accuracy and computational efficiency, it seemed easier to implement than
  other methods, it allowed me to incorporate viscous effects, and the fact
  that it only needs the quarter-chord means it's easy to use with simple
  geometry definitions (I wanted the geometry as simple as possible).

  I needed a method that can handle **non-linear geometry** (sweep, dihedral,
  twist, asymmetric geometry / brake deflections, asymmetric wind / turning),
  as well as **non-linear lift coefficients** (inviscid methods neglect any
  notion of flow separation; I'm not trying to accurately handle stall
  conditions, I just want graceful degradation).

  I want to be able to use section data that accounts (at least approximately)
  for **thickness** and **viscosity** (which changes the lift slope, induces
  stall, adds pressure drag due to flow separation, and enables viscous drag
  corrections)

* I like this comment in Belloc's paper: "Theoretical analysis of arched wings
  is scarce in the literature, partly because the Prandtl lifting line theory
  is not applicable to arched wings", then in his conclusion, "using a 3D
  potential flow code like panel method, vortex lattices method or an adapted
  numerical lifting line seems to be a sufficient solution to obtain the
  characteristics of a given wing."

  I hadn't thought about the NLLT as a "3D potential flow code".


Derivation
----------

.. figure:: figures/paraglider/dynamics/phillips_scratch.*

   Wing sections for Phillips' method.

.. math::
   :label: 3D vortex lifting law

   \vec{\mathrm{d}F} = \rho \Gamma \vec{V} \times \mathrm{d}\vec{l}

.. math::
   :label: differential lifting force

   dF_i =
     \frac{1}{2}
     \rho
     V_i^2
     C_{L_i}
     \left( \alpha_i, \delta_i \right)
     A_i

Alternative form using explicit norms of vectors instead of using scalars as
the implicit norms:

.. math::
   :label: differential lifting force 2

   \left\| \vec{\mathrm{d}F}_i \right\| =
     \frac{1}{2}
     \rho
     \left\| \vec{V}_i \right\| ^2
     C_{L_i} \left( \alpha_i, \delta_i \right)
     A_i

The net local velocity at control point :math:`i` is the sum of the freestream
relative wind at the control point and the induced velocities from all the
other segments:

.. math::
   :label: local velocity

   \vec{V}_i = \vec{V}_{rel,i} + \sum^N_{j=1} \Gamma_j \vec{v}_{ji}

where :math:`\vec{v}_{ji}` are the velocities induced at control point
:math:`i` by horseshoe vortex :math:`j`:

.. math::
   :label: induced velocities

   \vec{v}_{ji} =
     \frac{1}{4\pi}
     \left[
       \frac
         {\vec{u}_{\infty} \times \vec{r}_{j_2i}}
         {r_{j_2i} \left( r_{j_2i} - \vec{u}_{\infty} \cdot \vec{r}_{j_2i} \right)}
       + (1 - \delta_{ji}) \frac
         {(r_{j_1i} + r_{j_2i})(\vec{r}_{j_1i} \times \vec{r}_{j_2i})}
         {r_{j_1i}r_{j_2i}(r_{j_1i}r_{j_2i} + \vec{r}_{j_1i} \cdot \vec{r}_{j_2i})}
       - \frac
         {\vec{u}_{\infty} \times \vec{r}_{j_1i}}
         {r_{j_1i} \left( r_{j_1i} - \vec{u}_{\infty} \cdot \vec{r}_{j_1i} \right)}
     \right]

and :math:`\delta_{ji}` is the Kronecker delta function:

.. math::
   :label: kronecker_delta

   \delta_{ji} \defas
     \begin{cases}
       1\quad &i = j \\
       0\quad &i \neq j
     \end{cases}

Solving for the vector of circulation strengths can be approached as
a multi-dimensional root-finding problem over :math:`f`, where :math:`f` is
a vector-valued function of residuals, and the residual for each horseshoe
vortex :math:`i` is given by:

.. math::
   :label: horseshoe vortex strength optimization target

   f_i \left( \Gamma_i \right) =
      2 \Gamma_i \left\| \vec{W}_i \right\|
      - \left\| \vec{V}_i \right\|^2 A_i C_{L,i} \left(\alpha_i, \delta_i \right)

where

.. math::
   :label: unlabeled1

   \vec{W}_i = \vec{V}_i \times \mathrm{d} \vec{l}_i

The Jacobian :math:`J_{ij} \defas \frac{\partial f_{i}}{\partial \Gamma_j}`
expands to:

.. math::
   :label: phillips jacobian

   \begin{aligned}
   J_{ij} =\;
      &\delta_{ij}\, 2 \left\| \vec{W}_i \right\|
      + 2\, \Gamma_i \frac {\vec{W}_i} {\left\| \vec{W}_i \right\|}
          \cdot \left( \vec{v}_{ji} \times \mathrm{d} \vec{l}_i \right)\\
      &- \left\| \vec{V}_i \right\|^2 A_i
         \frac
            {\partial C_{L,i}}
            {\partial \alpha_i}
         \frac
            {V_{a,i} \left( \vec{v}_{ji} \cdot \vec{u}_{n,i} \right)
            - V_{n,i} \left( \vec{v}_{ji} \cdot \vec{u}_{a,i} \right)}
            {V_{ai}^2 + V_{ni}^2}\\
      &- 2 A_i C_{L,i}(\alpha_i, \delta_i)(\vec{V}_i \cdot \vec{v}_{ji})
   \end{aligned}

with the normal and chordwise wind speeds

.. math::
   :label: section wind speeds

   \begin{aligned}
      V_{a,i} &= \vec{V}_i \cdot \vec{u}_{a,i}\\
      V_{n,i} &= \vec{V}_i \cdot \vec{u}_{n,i}
   \end{aligned}

* The fundamental idea of the method is to use solve for the circulation by
  finding a root of :math:`f`. Phillips recommends simple Newton iterations,
  but as a purely gradient method this becomes unreliable when sections of the
  wing reach their stall condition (when the lift-slope goes to zero).
  Phillips suggests using Picard iterations to deal with stalled sections, but
  it is unclear whether the target function reliably produces fixed points;
  a quick implementation failed to reliably converge.

  An alternative is to replace Newton's method with an alternative
  root-finding algorithm. I had great success with a modified `Powell's method
  <https://en.wikipedia.org/wiki/Powell%27s_method>`_, which "retains the fast
  convergence of Newton's method but will also reduce the residual when
  Newton's method is unreliable" (see the `GSL discussion
  <https://www.gnu.org/software/gsl/doc/html/multiroots.html#c.gsl_multiroot_fdfsolver_hybridsj>`_
  for more information). This method also reduces computational cost by
  reducing the number of Jacobian evaluations.

  This modified Powell's method is implemented using MINPACK's implementation
  `hybrj <https://www.math.utah.edu/software/minpack/minpack/hybrj.html>`_,
  which is easily accessible in Python via `scipy's \`optimize\` module
  <https://docs.scipy.org/doc/scipy/reference/optimize.root-hybr.html>`_.


Improvements
------------

* The original derivation suggesting using *Newton's method*, which computes
  the zero of a function (the residual error, in this case) via gradient
  descent. The problem with gradient descent is that it fails if the gradient
  goes to zero (as it does when section lift coefficients go to zero at their
  stall points). I replaced the gradient descent method with a hybrid method
  that uses Newton's method for large steps, and a line search when using the
  gradient is unreliable. This can be faster (it doesn't rely on fixed step
  sizes), and it naturally handles conditions near stall.

* [[Use a reference solution for sequential estimates. If the reference fails,
  solve a different, more relaxed, problem somewhere between the target
  conditions (with an unknown solution) and the reference conditions (with
  a known solution), and solve for that; if the analysis succeeds, use that
  solution as the new reference.

  As with all methods based on gradient descent, the Newton iterations require
  a starting point. In this case, the method requires an initial value for the
  circulation distribution :math:`\Gamma(s)`. The original paper suggested
  solving a linearized version of the equations, but only when analyzing wings
  with no sweep or dihedral. For the geometry of a typical parafoil, the
  non-linear equations must be used.

  In general, if no other information is available, a reasonable starting
  point is to assume an elliptical distribution. However, an elliptical
  circulation is a poor approximation as the wind deviates from uniform,
  head-on freestream. During the course of a typical flight, it is common to
  encounter significant angles of attack and sideslip, making an elliptical
  distribution a poor starting point. Suboptimal starting points produce large
  residual errors that tend to push naive Newton iterations to jump into
  unrecoverable states. At best, poor starting points require very small step
  sizes to avoid diverging, and if using fixed step sizes this will cause all
  solutions to be unnecessarily slow.

  FIXME: finish this discussion]]

* [[Lifting-line methods typically use a single Reynolds number for all
  sections based on a single profile, but for wings with significant taper the
  wing tips can be at significantly lower Reynolds numbers than the wing root.
  My implementation uses Reynolds numbers when looking up the section
  coefficients.]]

* My method chooses control points that are spaced linearly in :math:`s`, the
  section index. This keeps the spacing regular regardless of the shape of the
  :math:`yz` design curve.


Limitations
-----------

* Implications of using section coefficients

  * Assumes the section coefficient data is accurate and representative of the
    flow conditions during a flight. This is particularly questionable near
    stall, especially when using simulated airfoil data.

  * Assumes the sections will behave independently, as predicted by their
    individual coefficients (which is almost definitely wrong, since the
    sections interact). Part of the interaction can be captured by the induced
    velocities, but it seems very likely that in many common scenarios things
    like turbulence and separation bubbles will dramatically influence
    neighboring cells.

  * Unlike the section profiles, these are external data. They must be
    measured in a wind tunnel or computed with an external tool, like XFOIL.

    The coefficients must be estimated for every variation of the profile and
    flight conditions. Dealing with Reynolds numbers and section deformations
    quickly becomes unwieldy. Reynolds numbers are more straightforward, since
    many tools support batch analyses over a range of Reynolds numbers, but
    profile deformations, like braking or billowing, are more problematic. The
    distorted profiles must be precomputed and their aerodynamics estimated
    individually. This precludes continuous deformations, so interpolation is
    required.

    [[This doesn't seem like a major problem, to be honest, since the
    flowfield around billowing cells seems very unlikely to be nicely
    summarized by 2D coefficient data. You'll have all sorts of separation
    bubbles going on. For the same reason, I doubt surface panel methods would
    work for paragliders either; I doubt boundary conditions like flow
    tangency are reasonable models down in the valleys between billowing
    cells. My gut says you should pursue NLLT solutions for initial design
    work then switch to *fluid-structure interactions* (see
    :cite:`lolies2019NumericalMethodsEfficient`) to refine the design.]]

  * They ignore cross-flow effects. I'm sure the arc of the wing has
    a significant effect on the boundary layer, which we're assuming is
    constant over the entire section.

  * Precomputed 2D section coefficients introduce a steady-state assumption.

    [[In the conclusion of "Specialized System Identification for Parafoil and
    Payload Systems" (Ward, Costello; 2012), they note that "the simulation is
    created entirely from steady-state data". This is one of my major
    assumptions as well. This will effect accuracy during turns and wind
    fluctuations, and ignores hysteresis effects (boundary layers exhibit
    "memory" in a sense; the same wind vector can produce a separation bubble
    or not depending on how that state was achieved).]]

    [[ref: "Flight Vehicle Aerodynamics", Ch:7]]

    [[I am accounting for **some** of the unsteady effects by introducing
    *apparent mass*.]]

  * Section coefficients are optimistic. They are for idealized geometric
    shapes (they ignore surface imperfections), and computational methods for
    estimating them tend to struggle at high angles of attack (where flow
    separation quickly depends on complicated viscous effects).

    [[I'm using airfoil data from XFOIL, which is unreliable post-stall, but
    I'm including significant post-stall coefficient data anyway to observe
    how Phillips' method behaves in those regions. It's useful to understand
    how the method behaves in post-stall regions in the event you have
    accurate post-stall airfoil data. (ignoring the fact that the 3D wing
    basically shoots that to heck anyway)]]

* It uses the *Kutta-Joukowski theorem* for the section lift. Does the KJ
  theorem hold for a section beyond `Cl_max`?

* Can't model a spin (backwards airflow on one wingtip)

* Places the control points on the lifting-line, which causes issues as the
  number of control points is increased (the grid is refined). Recall the
  **very** informative discussion in Sec:8.2.3 from "Understanding
  Aerodynamics" (McLeanauth; 2013): "a curved lifting-line has infinite
  self-induced velocity" and "locating the control points away from the bound
  vortex is still the only way to have a general formulation that doesn't
  behave badly as the discretization is refined".

  See also :cite:`chreim2018ChangesModernLiftingLine`, pg3: long discussion of
  the PBC, and later on he notes "the circulation distribution becomes
  unstable and leads to divergence as the mesh is refined". **Worth
  revisiting: that paper proposes alternate horseshoe vortex geometries**.

  See also: :cite:`reid2020GeneralApproachLiftingLine`, where they mention:

    Previous attempts have been made to extend lifting-line theory to wings
    with sweep. One commonly used method moves the control pints off the locus
    of aerodynamic centers to the three-quarter chord line. This method then
    constrains the total velocity at each control point to be tangential to
    the wing camber line. **The downside of this approach is that it is no
    longer possible to use arbitrary section properties that account for
    thickness or contain viscous corrections to the lift slope.**

  Most of those papers are discussing problems for wings with sweep, but it
  seems like it'd also apply to wings with dihedral. Why wouldn't it? Oh, note
  to self: big difference between a wing with dihedral versus **a wing with
  sweep is that the wing with sweep will (probably?) experience significant
  spanwise flow.** Also, for a swept wing the set of bound vortices are not
  planar, which (I think) would mean they will induce velocities experienced
  at each other (whereas if they are planar then it's just the trailing
  vortices that influence the neighbors?)


* Doesn't lifting-line theory assume minimal spanwise flow?

  * "Aerodynamics for Engineers" (Bertin, Cummings; 2014; pg356)

  * "Weissinger's model of the nonlinear lifting-line method for aircraft
    design" (Owens; 1998)

  In :cite:`phillips2000ModernAdaptationPrandtl` he argues that
  :cite:`saffman1992VortexDynamics` proves that flow parallel to the bound
  vorticity does not affect the relationship between section lift and section
  circulation (ie, the *Kutta-Joukowski theorem* holds in the presence of
  spanwise flow?). I may be wrong, but this does not seem to address the fact
  that **you still need to compute the 2D coefficients in the presence of that
  same spanwise flow**. I'm using coefficients computed under the assumption
  of zero spanwise flow, so although applying the 3D vortex lifting law is
  probably fine, the coefficients are probably not.

* Modeling of turns is highly suspect. Phillips' method uses the
  *straight-wake assumption* where all trailing vortices are parallel to
  a single **uniform** freestream velocity, but freestream is ambiguous in the
  case of a turning wing. I chosen to use the freestream velocity of the
  central section under the assumption that 1) it minimizes the average
  deviation, and 2) sections on the left and the right have minimal impact on
  each other.

  Related: :cite:`bertin2014AerodynamicsEngineers` pg390: "In a **rigorous**
  theoretical analysis, the vortex lattice panels are located on the mean
  camber surface of the wing, and, **when the trailing vortices leave the
  wing, they follow a curved path.**" The *straight-wake assumption* is one of
  the linearizations used by most vortex lattice methods (of which Phillips
  can be considered to belong).

  One difference between Phillips and common vortex lattice methods is many
  (most?) common VLM implementations align the trailing legs with the wing
  central chord, whereas Phillips aligns it with freestream (Phillips
  acknowledges the error is only about 1%, but it's simple to do so why not?).

* The NLLT is essentially a VLM, which is a solution to the *lifting-surface
  theory* problem, which is "an extension of thin-airfoil theory to 3D". *Thin
  airfoil theory* assumes the airfoil is "thin", but I'm trying to use airfoils
  with 15% and 18% thickness! According to "Aerodynamics for Engineers"
  (pg308), airfoil sections "typically have a maximum thickness of
  approximately 12% of the chord and a maximum mean camber of approximately 2%
  of the chord". (I know a NACA 24018 has an 18% thickness, not sure about
  maximum mean camber; probably more than 2% though.) Makes sense that *surface
  panel methods* (that have no restriction on thickness) might have some
  advantages.

* Flow separation is a viscous effect, so you typically need to go to CFD for
  good approximations of that. In my case, I'm using the viscous-inviscid
  coupling method from XFOIL to predict small amounts of flow separation in
  the section coefficients and assume it is representative of flow separation
  on the 3D wing.

* This is a steady-state (non-accelerated) solution; in particular, it doesn't
  include corrections for apparent mass. (See :ref:`paraglider_components:Apparent
  Mass`).


Case study
==========

.. Validate the performance of Phillips' method for analyzing a parafoil
   canopy in steady-state conditions.

[[Introduce Belloc's wind tunnel data]]

* Introduce the test (the model, the test setup, and the data)

* Why is this a good test?

  * In terms of aerodynamics: good representation of the unusual geometry of
    a paraglider; completely known geometry (including airfoil); extensive
    data for a range of wind conditions; internal wood structure maintains
    the shape, eliminating uncertainty due to distortions

  * It also provides a good demonstration of how to use my geometry.

* Discuss the results

]]

Every new tool should be validated, and for aerodynamic codes validation often
involves comparing theoretical models to wind tunnel measurements. For the
tools proposed in this paper, validation should include demonstrating the
flexibility of the geometry definition proposed in :doc:`canopy_geometry` and
the performance of the aerodynamics code proposed in `Phillips' numerical
lifting-line`_.

An excellent test case for the geometry and aerodynamics is available from
:cite:`belloc2015WindTunnelInvestigation`, which provides both point-wise
geometry data and wind tunnel performance.


Aerodynamics
------------

[[Compare the wind tunnel data against the NLLT, a traditional *vortex lattice
method* (VLM) in AVL, and an experimental VLM in XFLR5 (which tilts the
geometry to mitigate the "small angles" approximation for alpha and beta). I'm
frustrated that the lift curve for all methods is so high compared to the wind
tunnel data, but at least the NLLT matches AVL, XFLR5, and MachUpX, so I'm
pretty confident I've implemented it correctly. I need to make a list of
explanations for the discrepancies though: unmodeled viscous effects in
particular, but there's still the chance of an issues with the `CZa` or
`Alphac` values in the wind tunnel data. I'm also not including any "wind
tunnel corrections", as in :cite:`barlow1999LowSpeedWindTunnel` or
:cite:`drela2014FlightVehicleAerodynamics` Sec:10.3

Also, maybe it's not such a terrible result overall? It is a pretty low aspect
ratio wing, after all. See Fig:7.22 of :cite:`bertin2014AerodynamicsEngineers`
shows theoretical vs experimental CL for a wing with AR=5.3; the theoretical
estimate significantly overestimates (IMHO) the lift coefficient, but the
author calls it a "reasonable" estimate.

Possibly related to the lift discrepancy:

* "Aerodynamics for Engineers", pg326, he discusses the effects of
  a "separated wake", although that's in the context of airfoils. Still it
  does have the same look as my data.

* In https://www.xflr5.tech/docs/Part%20IV:%20Limitations.pdf, pg29, he
  mentions that the "flat wake" assumption (no wake roll-up) causes an
  overestimation of the vortex strengths (and thus the lift), and that the
  error can be in the order of 1% to 10% for the lift and induced drag.

]]

Some results:

.. figure:: figures/paraglider/belloc/CL_vs_alpha.*

   Lift coefficient vs angle of attack.

.. figure:: figures/paraglider/belloc/CD_vs_alpha.*

   Drag coefficient vs angle of attack.

.. figure:: figures/paraglider/belloc/Cm_vs_alpha.*

   Pitching coefficient vs angle of attack.

This is the global pitching coefficient, which includes contributions from
both the section pitching coefficients and the aerodynamic forces. The VLM
estimate appears to be using the wrong reference point, but it isn't clear
from the program documentation what the error might be. The results are left
here for completeness and to highlight the uncertainty in how the VLM was
applied.

.. figure:: figures/paraglider/belloc/CL_vs_CD_pseudoinviscid.*

   Pseudo-inviscid lift coefficient vs drag coefficient.

[[Demonstrates how well the NLLT lift matches XLFR5's "Tilted Geometry" method
over the lower range of alpha. Once alpha approaches stall, the NLLT diverges
since it's not a true inviscid method; it's using the viscous lift
coefficients to determine the circulation distribution.]]

.. figure:: figures/paraglider/belloc/CL_vs_CD.*

   Lift coefficient vs drag coefficient.

.. figure:: figures/paraglider/belloc/CL_vs_Cm.*

   Lift coefficient vs global pitching coefficient.


It's also informative to consider the effect of sideslip.

.. figure:: figures/paraglider/belloc/CY_vs_beta.*

   Lateral force coefficient vs sideslip.

.. figure:: figures/paraglider/belloc/Cl_vs_beta.*

   Rolling coefficient vs sideslip.

.. figure:: figures/paraglider/belloc/Cn_vs_beta.*

   Yawing coefficient vs sideslip.


Comments
^^^^^^^^

* The inviscid solutions agree with the NLLT quite well for small angles of
  attack. I think the deviation occurs when the "thin boundary layer"
  assumption starts to break down; for the 2D lift coefficient, the BL really
  starts to thicken around alpha=12, so when you consider the **effective**
  angle of attack it happens around alpha=9? Seems about right. I'm not sure
  if flow separation is involved, but I don't think that tends to happen until
  after a section exceeds `Cl_max`?

* The VLM and NLLT disagree on the zero-lift angle of attack? Hm. That seems
  to suggest bad airfoil coefficients, doesn't it? I would think you'd have
  the least amount of flow separation at that alpha; is that intuition
  correct? Or maybe BL thickness is already significant at that angle;
  I should check the overall spanwise alphas.

* The wind tunnel data is only testing the **uniform** flow field case. In my
  simulations I'm using this method for **asymmetric** flows (spanwise
  variation in speed and/or direction). That's definitely questionable
  (similar to what I mention about assuming the trailing wake is aligned to
  the central freestream: highly questionable).

  Not a big deal though; I just need to be clear that the point isn't to claim
  this is a great model; I just need something useful for testing the geometry
  and "good enough" for simulations.

  **This was always meant to be used in an uncertain environment (stochastic
  simulations). As long as the choice of aerodynamic method is not the
  dominant source of error, I'm fine with it.**


Discussion
==========

* Phillips' method uses steady-state coefficients and uses a straight-wake
  assumption. Both are cause for concern when trying to apply this method to
  unsteady or non-uniform flow conditions (such as turning).

* [[Acknowledge but defer the discussion of unsteady effects until
  :ref:`paraglider_components:Discussion`? I'll have already discussed apparent
  mass by that point.]]
