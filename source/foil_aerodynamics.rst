.. This chapter estimates a foil's aerodynamics using its geometry.


*****************
Foil aerodynamics
*****************

For the purposes of this chapter, *aerodynamics* describe the instantaneous
forces and moments produced when an object moves through air, and an
*aerodynamic model* encodes the aerodynamics of a foil over the range of
flight conditions. In a rigorous modeling process, an aerodynamic model is
measured experimentally, either in a wind tunnel or with flight tests.
Alternatively, theoretical methods allow a foil's aerodynamics to be predicted
from mathematical models that use the foil geometry to predict the surrounding
flow field. The previous chapter introduced a parametric foil geometry
explicitly because experimental methods are infeasible for this project;
experimental wing tests are time consuming and expensive, assuming a physical
parafoil could even be acquired. Instead, this project must rely on
theoretical methods.

This chapter selects a theoretical method suitable for flight reconstruction
of a paraglider under typical flight conditions. It refines the chosen method
to improve its performance in the context of flight simulation, and validates
its theoretical performance by comparing its predictions against wind tunnel
measurements from a representative parafoil model from literature.


Modeling requirements
=====================

.. Establish the performance criteria for this project. I need an aerodynamics
   method that can handle the unusual geometry of a paraglider canopy under
   expected flight conditions.


.. Introduce computational aerodynamics

Theoretical models are built by combining fundamental equations of fluid
behavior with an object's geometry to estimate the configuration of the
surrounding flow field and the forces it produces on the object. The variety
of models are built on different simplifying assumptions related to the
geometry and the characteristics of the flow field. [[Important
characteristics of the flow field include viscosity, compressibility,
rotational or irrotational, thermal conductivity, etc. Simplifications to the
flow field often appear as constraints on the flight conditions; for example,
linear models require small angles of attack.]]

Early theoretical aerodynamics predate the modern computing era, and were
forced to prioritize simplifying assumptions that would enable analytical
solutions of the governing equations. Those assumptions placed heavy
restrictions on what geometries could be analyzed and what characteristics of
the flow field must be neglected.

In contrast, modern *computational aerodynamics*
:cite:`cummings2015AppliedComputationalAerodynamics` rely on digital computers
to solve the equations numerically, relaxing the need for analytical
solutions. As a result, modern methods can analyze significantly more complex
foil geometries under the entire set of flow field characteristics.

There is a stunning array of different methods, each with its own set of
assumptions and limitations. Each design involves tradeoffs that limit their
applicability to different situations in exchange for ease of use and reduced
computational time.


[[FIXME: Now that I've declared the existence of a range of methods that can
handle a range of conditions, I need to say which conditions (in terms of
geometry, flow field characteristics, runtime, implementation availability,
etc) are important to this project so I can select a suitable method.

In practice a lot of these "requirements" turn out to be overkill, but **the
point is to VERIFY** which terms matter and which don't. I was fed up with
papers just assuming everything is linear, constant Reynolds number, etc etc,
without verification.]]


Geometry
--------

* Supports non-linear geometry

  [[For lifting-line methods, this means the model should not assume
  a straight lifting-line (allow both sweep and dihedral), should not assume
  the lifting-line follows a circular arc (ala `gonzalez1993`), etc]]

* Don't assume thin sections

  [[Relatively important for small angles of attack, but becomes more
  significant as alpha increases; in general, thicker airfoils have nicer
  stall characteristics)]]


Flow field
----------

.. Define "typical flight conditions" in the context of this paper. Wind
   gradients, wing rotation, etc: the aerodynamics method must be able to
   handle them.

* High angle of attack

  Related: require graceful degradation near stall

  [[When I talk about "graceful degradation", I should probably explain it in
  the sense of "the wing tips tend to start stalling first, but their
  contributions are relatively minor overall, so inaccuracies in the wing tip
  forces does not contribute a large error to the overall force estimate and
  should not preclude the method from providing functional, albeit degraded,
  accuracy."]]

* Viscous effects and empirical viscous corrections

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

* Variable Reynolds number (paraglider speeds are quite low and experience
  a relatively large change in range; the effect is even more significant due
  to taper, especially at such low airspeeds)

* Non-uniform wind. This is important for two reasons:

  1. Non-longitudinal (turning) maneuvers

  2. Wind gradients (shear, thermals, etc)


Implementation
--------------

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

* [[Must be open source]]


Model selection
===============

.. Survey the available models

[[Introduce LLT, VLM, panel methods, CFD, etc. Go through the requirements and
explain why they fail (LLT fails with non-linear geometry, VLM handles
non-linear geometry but assumes linear aerodynamics and neglects thickness,
which can be significant for parafoils, CFD is too slow). Only the NLLT met my
requirements.]]

* Good references:

  * :cite:`drela2014FlightVehicleAerodynamics`

  * :cite:`bertin2014AerodynamicsEngineers`

  * :cite:`anderson2017FundamentalsAerodynamics`

* [[Section profiles were covered in the previous chapter. The computational
  methods use the profiles either via their section coefficients, or via the
  surface geometry they generate.]]


* [[What simplifying assumptions do they make regarding the geometry? What
  simplifying assumptions do they make regarding the flow field (viscosity,
  compressibility, etc)?

  **Should I discuss these separately?** For example, does it make sense to
  declare that the LLT assumes the wing is straight without the context that
  it models the flow field using a variable-strength vortex filament? Not sure
  how to broach this discussion.]]


* [[What are their limitations? (spanwise flow, flow separation, linear
  coefficients, uniform wind, etc)]]


.. Critique the models according to my modeling requirements

* [[Some of these models are already being used in literature to estimate the
  performance of parafoils. Explain why methods that "work" for other papers
  do not meet the performance criteria for **this** project.]]


.. Select an appropriate model for this project

* Only the NLLT met my requirements (except no open source implementation was
  available at the time). It's an extension of LLT to account for the effects
  of a curved lifting-line. It's computationally efficient, handles non-linear
  geometry, uses proper airfoil data (does not assume constant or linear
  aerodynamic coefficients), allows for viscous corrections, and is relatively
  simple to implement.


Phillips' numerical lifting-line
================================

* Why am I choosing this method?

  * Supports nonlinear geometry (sweep, dihedral, twist, asymmetric geometry
    / brake deflections)

  * Could be adapted to support non-uniform wind vectors (non-uniform wind
    field, rotating wing maneuvers)

  * Uses actual airfoil coefficient data. I didn't want to just assume linear
    lift, I wanted to DEMONSTRATE linear lift. Parafoils use relatively thick
    airfoils, so assuming thin airfoils (ala the VLM) bothered me. It also
    allows the method to account (approximately) for viscous effects (changes
    the lift slope, induces stall, adds pressure drag due to flow separation,
    and enables viscous drag corrections)

  * Able to approximately model behavior near stall (though not deep stall).
    Inviscid methods cannot model flow separation, but paragliders often fly
    relatively close to the stall condition. That said, I'm not trying to
    accurately handle stall conditions, I just need graceful degradation.

  * Relatively simple to implement

  * Computationally fast

* Beware: there are two uses of the acronym NLLT: the `N` can either stand for
  "nonlinear" or "numerical". For example, Weissinger's "nonlinear LLT" versus
  Phillips "numerical LLT".


Derivation
----------

[[This derivation mostly uses the notation from this paper, with the exception
of velocity. Phillips uses a capital :math:`\vec{V}` for velocity, and
a lowercase :math:`\vec{v}` for the induced velocities. This derivation
retains that notation to avoid confusion with the original paper.

Oh, and he uses `r` a bit differently; they're still position vectors, but
implicitly wrt the origin. Also, `r0 = r2 - r1`.]]

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
   :label: local velocity (Phillips)

   \vec{V}_i = \vec{V}_{\infty} + \sum^N_{j=1} \Gamma_j \vec{v}_{ji}

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


[[Now solve for the circulation strengths by finding a zero of the residual
function. Given the circulation strengths, use the 3D vortex lifting law
:eq:`3D vortex lifting law` to compute the inviscid forces at each control
point. For the section drag and pitching moments, compute the angle of attack
then apply standard *strip theory* using the section drag and pitching
coefficients from the airfoil data.]]


Modifications
-------------

[[Changes and improvements on the original Phillips paper.]]


Control point distribution
^^^^^^^^^^^^^^^^^^^^^^^^^^

[[My method chooses control points that are spaced linearly in :math:`s`, the
section index. This keeps the spacing regular regardless of the shape of the
:math:`yz` design curve. This works well for parafoils, but other wing designs
may prefer either a different section index, or at least nonlinear spacing in
`s`.]]


Variable Reynolds numbers
^^^^^^^^^^^^^^^^^^^^^^^^^

Lifting-line methods like this one typically assume the section coefficient
data is a function of angle of attack :math:`\alpha`, and possibly some sort
of control deflection :math:`\delta`, but commonly neglect to make the
coefficient data an explicit function of Reynolds number. For relatively high
Reynolds regimes this is reasonable since the airfoil data is essentially
constant, but for for foils that operate in the low to transitional Reynolds
regimes the effect can be significant. For example, parafoil sections under
typical flight conditions experience Reynolds numbers in the range from
roughly 200,000 to 2,000,000. In that operating range the airfoil data cannot
be assumed constant, and should be an explicit function of Reynolds number.


Non-uniform upstream velocities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phillips' original derivation :cite:`phillips2000ModernAdaptationPrandtl`
assumes uniform flow, but :cite:`hunsaker2006LiftinglineApproachEstimating`
relaxes that assumption by replacing the uniform *freestream velocity*
:math:`V_{\infty}` with the relative *upstream velocity* :math:`V_{rel,i}`
that "may also have contributions from prop-wash or rotations of the lifting
surface about the aircraft center of gravity." (Compare Phillips Eq:5 to
Hunsaker-Snyder Eq:5.) The result is that :eq:`local velocity (Phillips)` is
replaced with:

.. math::
   :label: local velocity (Hunsaker)

   \vec{V}_i = \vec{V}_{rel,i} + \sum^N_{j=1} \Gamma_j \vec{v}_{ji}

In :cite:`hunsaker2006LiftinglineApproachEstimating` they are concerned with
accounting for propeller wash, but for a parafoil the upstream velocity is
simply the local wind velocity at control point :math:`i` combined with the
velocity produced by the control point :math:`CP,i` rotating about the glider
center of mass :math:`CM`:

.. math::
   :label: upstream velocity

   \vec{V}_{rel,i} =
     \vec{V}_{\infty,i}
     + \vec{r}_{CP,i/CG} \times \vec{\omega}_{b/e}

This change enables the method to approximately accommodate non-uniform wind
conditions, such as wind gradients, during turning maneuvers, etc. This
flexibility should be used with caution, however; see `Straight-wake
assumption`_ for a discussion.


Better solver
^^^^^^^^^^^^^

[[FIXME: section title]]

To solve for the circulation strengths :math:`\Gamma_i`, the Phillips paper
suggests using *Newtons' method*, which computes the zero of a function via
gradient descent. Gradient descent has several practical issues, but the most
important problem in this case is that it fails to converge if the gradient
goes to zero. For this application, the function under evaluation is the
residual error :eq:`horseshoe vortex strength optimization target`, and its
gradient :eq:`phillips jacobian` depends on derivatives of the section lift
coefficients. When a wing section reaches the angle of attack associated with
:math:`C_{L,max}` the section has stalled, its section lift slope is zero, and
gradient descent will fail to converge. Phillips suggests switching to Picard
iterations to deal with stalled sections, but it is unclear whether the target
function reliably produces fixed points; a simple prototype failed to
converge.

An alternative is to use a robust, hybrid root-finding algorithm that uses
gradient descent for speed but switches to a line-search algorithm when the
gradient goes to zero. The implementation for this project had great success
with a modified `Powell's method
<https://en.wikipedia.org/wiki/Powell%27s_method>`_, which "retains the fast
convergence of Newton's method but will also reduce the residual when Newton's
method is unreliable" (see the `GSL discussion
<https://www.gnu.org/software/gsl/doc/html/multiroots.html#c.gsl_multiroot_fdfsolver_hybridsj>`_
or MINPACK's `hybrj documentation
<https://www.math.utah.edu/software/minpack/minpack/hybrj.html>`_ for more
information). This method not only mitigates the convergence issues near
stall, but it is also significantly faster: it does not depend on fixed step
sizes (which must be inherently pessimistic to encourage convergence) and is
able to use approximate Jacobian updates instead of requiring full Jacobian
evaluations at each step.

[[For this project, the `glidersim` implementation of Phillips' method uses
the `hybrj <https://www.math.utah.edu/software/minpack/minpack/hybrj.html>`_
routine from the `MINPACK` package via the Python interface provided by
`scipy's \`optimize\` module
<https://docs.scipy.org/doc/scipy/reference/optimize.root-hybr.html>`_.]]


Reference solutions
^^^^^^^^^^^^^^^^^^^

The root-finding algorithm that solves for the circulation strengths requires
an initial proposal for the circulation distribution :math:`\Gamma(s)`. Poor
proposals produce large residual errors that can push Newton iterations into
unrecoverable states, so it is preferable to use some sort of prior
information to guess the true distribution. The original paper suggested
solving a linearized version of the equations, but that choice only applies to
wings with no sweep or dihedral. Another common suggestion is to assume an
elliptical distribution; for most wings, an elliptical circulation
distribution is a reasonable guess during straight and steady flight, but it
is a poor proposal for scenarios that include non-uniform wind or asymmetric
control inputs, such as during flight maneuvers. It is clear that generating
suitable proposals for nonlinear geometries under variable flight conditions
requires a different approach.

[[This project chose a hybrid strategy.]]

For sequential problems, such as the sequence of states in a flight simulator
or the points of a polar curve, the simple answer is to reuse the solution
from the previous problem. Provided the time resolution of the simulation is
reasonably small then the state of the aircraft should be similar between each
timestep, so the proposal will be very close to the target. [[This also has
the added advantage of capturing hysteresis effects.
:cite:`owens1998WeissingerModelNonlinear`]]

[[The problem is how to bootstrap the "previous" solution. When no previous
solution is available the easiest target is to straight and steady flight with
zero control inputs. As mentioned earlier, an elliptical is a reasonable
proposal for most wings in that state. Given the solution to the "easy"
problem, try to solve the target. If the method does not converge, pick an
intermediate problem midway between the reference and target, solve for that,
then use its solution as the proposal for the target. Repeat subdividing the
problem until convergence is achieved.]]

[[Related: `Sensitive to initial proposal`_.]]


Limitations
-----------

Assumes minimal spanwise flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prandtl's classic lifting-line method assumes minimal spanwise flow
(:cite:`bertin2014AerodynamicsEngineers`, pg356)

  * "Weissinger's model of the nonlinear lifting-line method for aircraft
    design" (Owens; 1998)

    Regarding the swept wing: "The concern for the accuracy stems from the
    increase in spanwise flow as the sweep angle increases. This sweep causes
    a highly three-dimensional flow field which the method does not completely
    capture. Even so, the comparison in figure 15 shows very good agreement
    between experiment and computational predictions for the AOA range given."


In :cite:`phillips2000ModernAdaptationPrandtl` Phillips argues that
:cite:`saffman1992VortexDynamics` proves that fluid flow parallel to the bound
vorticity does not affect the relationship between section lift and section
circulation.


I may be wrong, but this does not seem to address the fact that **you still
need to compute the 2D coefficients in the presence of that same spanwise
flow**. I'm using coefficients computed under the assumption of zero spanwise
flow, so although applying the 3D vortex lifting law is probably fine, the
coefficients are probably not.


Straight-wake assumption
^^^^^^^^^^^^^^^^^^^^^^^^

Prandtl's classic lifting-line method assumed the trailing *wake vortex sheet*
streams straight back from the lifting-line. The strength of the vorticity
shed into the wake varies with the local variation of lift along the span. For
a discretized method, such as Phillips' or Weissinger's LLT
:cite:`weissinger1947LiftDistributionSweptback`, the vortex sheet is lumped
into a series of shed vortex filaments whose strength is equal to the
difference in local lift of neighboring segments.

In this model, the trailing legs of all horseshoe vortices extend from the
nodes in straight lines parallel to some *freestream velocity* direction
:math:`u_{\infty}` (see :eq:`induced velocities`). This is clearly invalid for
a rotating wing where a freestream velocity is ambiguous.

Despite this limitation, this project assumes that as long as the rotation
rates remain small enough that relative flow angles remain small the method
still provides useful approximations.

This assumption is made without theoretical justification; instead, it relies
on the superior aerodynamics knowledge of its sources. First, the use of this
method with non-zero rotation is explicitly mentioned in
:cite:`hunsaker2006LiftinglineApproachEstimating`. Also, this assumption is
shared with the vortex-lattice model used in `AVL
<https://web.mit.edu/drela/Public/web/avl/>`_; in that method, the trailing
legs are aligned with the foil :math:`x`-axis, regardless of freestream flow.
In Phillips' method the trailing are aligned to the freestream; this
implementation of Phillips' model uses the local upstream velocity of the
central section for the conceptual :math:`u_{\infty}`.

For a related technical discussion that incorporates rotation rates into
a vortex lattice method, refer to :cite:`drela2014FlightVehicleAerodynamics`
Sec:6.5; in particular, Eq:6.33 for aligning the trailing legs with the
:math:`x`-axis and Eq:6.39 for incorporating the rotation rates into the
aerodynamic influence coefficients matrix.




"quasi-steady flow", ala Drela; see also Drela pg133 where he's setting up the
AIC matrix; he includes rotation rates there, so I'm going to claim that this
method is similar: technically wrong, but reasonably accurate within the
limits of the "quasi-steady state" assumption. Also, this is probably more
stable because Drela aligns the trailing vortices with x-hat (See Eq:6.33,
pg132), whereas I'm at least aligning it with the central freestream, so...
yay?




Modeling of turns is highly suspect. Phillips' method uses the *straight-wake
assumption* where all trailing vortices are parallel to a single **uniform**
freestream velocity, but freestream is ambiguous in the case of a turning
wing. I chose to use the freestream velocity of the central section under the
assumption that 1) it minimizes the average deviation, and 2) sections on the
left and the right have minimal impact on each other.

Related: :cite:`bertin2014AerodynamicsEngineers` pg390: "In a **rigorous**
theoretical analysis, the vortex lattice panels are located on the mean camber
surface of the wing, and, **when the trailing vortices leave the wing, they
follow a curved path.**" The *straight-wake assumption* is one of the
linearizations used by most vortex lattice methods (of which Phillips can be
considered to belong).

[[One difference between Phillips and common vortex lattice methods is many
(most?) common VLM implementations align the trailing legs with the wing
central chord, whereas Phillips aligns it with freestream (Phillips
acknowledges the error is only about 1%, but it's simple to do so why not?).]]

[[Related: the wind vectors might not be parallel either. Technically any
gradient with a rotational component would mean each control point should
expect a different "straight-wake" direction, even if the wing was flying
straight.]]

[[Related but minor issue: it that Can't model a spin (backwards airflow on
one wingtip).]]

[[Is this the same thing as assuming the trailing sheet is flat? The XFLR5
docs mention inaccuracy due to ignoring sheet roll-up. I imagine that applies
here too.]]

[[I think this is closely related to the `No unsteady effects`_  limitation.
In `avl_doc.txt` they discuss unsteady flow in the same paragraph as the need
for rotation rates to be small enough that relative flow angles are small.

Consider how **Phillips derivation assumes all the trailing vortices are
aligned with `u_inf`**. Now imagine what would happen if you tried to replace
`u_inf` with the local flow directions `u_rel,i`. The two trailing legs
emanating from each shared node would point in different directions, meaning
there would be a dramatic discontinuity in the underlying vortex sheet (I
think); I suspect that would be a nonsense physical model.

What if the trailing legs were aligned with the wind vectors at the nodes? The
trailing legs of each horseshoe vortex would not (in general) be parallel.
What happens if the trailing legs of a horseshoe vortex are not parallel?
Well, (I think) non-parallel trailing legs imply force exist **inside** the
flow field, which (I think) means there are accelerations inside the flow
field (momentum exchange between parcels of air) which (I think) violates the
whole "steady-state flow field" assumption. --- Oh, and another point: 

Also, consider the trajectory of those straight trailing legs back towards
their notion of "infinity"; conceptually, the global flow field is the result
of the "local flow field" interactions, but I have no idea how non-aligned
trailing vortices would work. I suspect that straight trailing legs are simply
bad models for the shed vorticity from a rotating wing.]]


Requires accurate section coefficients
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

* Viscous effects such as flow separation and viscous drag are notoriously
  difficult to model accurately. In my case, I'm using the viscous-inviscid
  coupling method from XFOIL and assuming its estimates are representative of
  the flow field surrounding the 3D wing segments. In practice, XFOIL is only
  able to predict small amounts of flow separation, and tends to be produce
  optimistic estimates of the viscous drag.


No unsteady effects
^^^^^^^^^^^^^^^^^^^

This is a steady-state (non-accelerated) solution. It does not include
time-varying effects.

Some common sources of unsteady effects
(:cite:`drela2014FlightVehicleAerodynamics`, Ch:7, pg149):

  1. Unsteady body motion

  2. Unsteady body deformation

  3. Spatially-varying or unsteady atmospheric velocity field

  **lol, a rigorous paraglider simulator should acccount for all of those**

One important unsteady effect is *apparent mass*. Thankfully that can be
accounted for that manually; see :ref:`paraglider_components:Apparent mass`.


Non-unique solutions
^^^^^^^^^^^^^^^^^^^^

Gradient descent will find a zero of the residual, but it is not guaranteed to
be unique, especially given that the numerical solver relies on tolerances
instead of exact solutions. Depending on the initial conditions, the solver
may converge to different circulation distributions. See
`demonstration:Bonk`_.


Unstable at high resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method places the control points on the lifting-line, which causes issues
as the number of control points is increased (the grid is refined). Recall the
**very** informative discussion in Sec:8.2.3 from "Understanding Aerodynamics"
(McLeanauth; 2013): "a curved lifting-line has infinite self-induced velocity"
and "locating the control points away from the bound vortex is still the only
way to have a general formulation that doesn't behave badly as the
discretization is refined".

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


Sensitive to initial proposal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* This implementation is intended for flight simulation, generating solutions
  iteratively, so reusing the previous solution as the proposal is a natural
  choice for minimizing the initial residual error. Good proposals encourage
  convergence while minimizing optimization runtime.

* As an added bonus, using the previous solution adds the capability of
  capturing hysteresis effects :cite:`owens1998WeissingerModelNonlinear`.

* For example, in :cite:`anderson1980NumericalLiftingLine` they discuss a wing
  that demonstrates hysteresis depending on whether data were generated with
  increasing versus decreasing alpha.

* True hysteresis effects can be significant, so the ability to capture them
  can be beneficial.

* Unfortunately, the method can also demonstrate a fictitious dependence on
  the proposal.

* The root-finding problem uses the residual error :eq:`horseshoe vortex
  strength optimization target` which is likely a non-convex function.
  A global optimization method such as gradient descent is not guaranteed to
  find the global minimum for a non-convex function, so the solution is
  sensitive to the starting point (the initial proposal).

* The conclusion is that ability to produce different solutions for different
  proposals mean the method will exhibit hysteresis effects which may or may
  not be physically accurate.

* [[Extra]]: Alternative solutions can create discontinuities/jumps in the
  solutions. I chose to ignore this issue in favor of robustness; aborting
  a simulation is not ideal, and in practice the discontinuities do not create
  significant deviations in the overall trajectory.

  See `demonstration:Bonk` for an example.


Unreliable near stall
^^^^^^^^^^^^^^^^^^^^^

[[FIXME: section title. "Unreliable" is true, but sounds overly pessimistic.]]

* Phillips mentions that it can be used up to stall "with caution"

* Weissingers NLL :cite:`owens1998WeissingerModelNonlinear`, which is
  conceptually very similar, notes that their model "does not predict the high
  angle-of-attack aerodynamics for wings that produce a LE vortex. In other
  words, this method limited to wings with moderate to thick airfoils and
  moderate sweep." I presume the same applies to Phillips'.


Case study
==========

.. Validate the performance of Phillips' method for analyzing a parafoil
   canopy in steady-state conditions.

This section considers the ability of Phillips' NLLT to predict the
aerodynamics of a typical paraglider geometry. It continues the discussion in
:ref:`foil_geometry:Case study` by comparing the theoretical predictions of
several aerodynamics models against experimental wind tunnel data.


* Introduce the test (the model, the test setup, and the data)

* Why is this a good test?

  * In terms of aerodynamics: good representation of the unusual geometry of
    a paraglider; completely known geometry (including airfoil); extensive
    data for a range of wind conditions; internal wood structure maintains
    the shape, eliminating uncertainty due to distortions

  * It also provides a good demonstration of how to use my geometry.

* Discuss the results


Wind tunnel data
----------------

Wind tunnel measurements were taken over a range of angle of attack and
sideslip. The angle of attack ranged from -5 to 20 degrees, suitable for
capturing the longitudinal performance of the wing post-stall. The sideslip
angles range from 0 to 15 degrees, which is useful for considering the impact
of the `Straight-wake assumption`_ for a non-rotating wing.

For best accuracy, wind tunnel data measurement must be corrected for wall
interactions with the flow (:cite:`barlow1999LowSpeedWindTunnel`, or
:cite:`drela2014FlightVehicleAerodynamics` Sec:10.3). However, because
classical wind tunnel wall corrections assume a flat wing, the data for the
arched parafoil are uncorrected for wall effects.


Aerodynamics models
-------------------

[[Introduce the aerodynamic models I'll be comparing against the NLLT:
a traditional *vortex lattice method* (VLM) in `AVL
<https://web.mit.edu/drela/Public/web/avl/>`_ , and an experimental VLM in
`XFLR5 <https://www.xflr5.tech/xflr5.htm>` (which tilts the geometry to
mitigate the "small angles" approximation for alpha and beta).]]


Model performance
-----------------

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


Comments:

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


* Did Belloc account for hysteresis? In
  :cite:`anderson1980NumericalLiftingLine` they plots how both the
  experimental and numerical data were strongly affected by increasing vs
  decreasing alpha.

  TODO: run the numerical solutions forward and backwards in alpha!

* I'm frustrated that the lift curve for all methods is so high compared to
  the wind tunnel data, but at least the NLLT matches AVL, XFLR5, and MachUpX,
  so I'm pretty confident I've implemented it correctly. I need to make a list
  of explanations for the discrepancies though: unmodeled viscous effects in
  particular, but there's still the chance of an issues with the `CZa` or
  `Alphac` values in the wind tunnel data.

  Also, maybe it's not such a terrible result overall? It is a pretty low
  aspect ratio wing, after all. See Fig:7.22 of
  :cite:`bertin2014AerodynamicsEngineers` shows theoretical vs experimental CL
  for a wing with AR=5.3; the theoretical estimate significantly overestimates
  (IMHO) the lift coefficient, but the author calls it a "reasonable"
  estimate.


Possibly related to the lift discrepancy:

* "Aerodynamics for Engineers", pg326, he discusses the effects of
  a "separated wake", although that's in the context of airfoils. Still it
  does have the same look as my data.

* In https://www.xflr5.tech/docs/Part%20IV:%20Limitations.pdf, pg29, he
  mentions that the "flat wake" assumption (no wake roll-up) causes an
  overestimation of the vortex strengths (and thus the lift), and that the
  error can be in the order of 1% to 10% for the lift and induced drag.


Discussion
==========

* Phillips' method uses steady-state coefficients and uses a straight-wake
  assumption. Both are cause for concern when trying to apply this method to
  unsteady or non-uniform flow conditions (such as turning).

  Should I Acknowledge but defer the discussion of unsteady effects until
  :ref:`paraglider_components:Discussion`? I'll have already discussed
  apparent mass by that point.
