.. This chapter estimates a foil's aerodynamics using its geometry.


*****************
Foil aerodynamics
*****************

.. What are aerodynamics? Experimental and theoretical models

For the purposes of this chapter, an *aerodynamics model* provides the
instantaneous forces and moments produced on a foil when it moves relative to
air. In a rigorous modeling process the aerodynamic forces and moments would be
measured experimentally, either in a wind tunnel or with flight tests, but that
rigor is time consuming, expensive, and requires physical possession of the
wing. Instead, this paper is concerned with estimating the dynamics of
commercial paraglider wings from basic technical specifications, and so it must
rely on theoretical methods that predict the flow-field surrounding a foil by
combining fundamental equations of fluid behavior with the foil geometry.

.. Originally I was hoping to perform statistical flight reconstruction, and it
   would be infeasible to physically measure the aerodynamics of all paraglider
   wings that could have produced a flight track.

This chapter suggests performance criteria for simulating paraglider
aerodynamics, and selects a theoretical method capable of simulating those
dynamics under the [[target flight conditions]]. It presents a derivation of
the method, modifies the method to improve its behavior in the context of
flight simulation, and validates the modified method by comparing its
predictions against wind tunnel measurements of a representative parafoil model
from literature.

.. FIXME: ensure I have a definition for "target flight conditions" in the
   Introduction and link to it.


Aerodynamics models
===================

.. The aerodynamics method must be capable of modeling the flow field
   surrounding a paraglider canopy during "typical flight conditions". Define
   the selection criteria, review the avaible models, and choose an appropriate
   method.

.. Theoretical aerodynamics: analytical vs computational models.

   Both methods develop systems of equations to solve for the flow field using
   the governing equations of fluid flow.

Classical aerodynamics predate the modern computing era, and were forced to
prioritize simplifying assumptions that would enable analytical solutions of
the governing equations; those assumptions placed heavy restrictions on what
geometries could be analyzed and what characteristics of the flow-field must be
neglected. [[These simplifying assumption made the problems tractable in
a surprising variety of situations, but]] despite their elegance, such
analytical solutions are inadequate for analyzing the geometry and flight
conditions of a paraglider.

In contrast, modern *computational aerodynamics*
:cite:`cummings2015AppliedComputationalAerodynamics` solve the equations
numerically, relaxing the need for analytical solutions. As a result, modern
methods can analyze significantly more complex foil geometries over the entire
set of flow-field characteristics. [[However, even with modern computers]] the
fluid equations are too difficult to solve in the general case, so simplifying
assumptions are still required to produce a tractable system of equations. This
modeling process has led to a wide variety aerodynamic models built on
different simplifying assumptions regarding the geometry and the
characteristics of the flow-field.


Model requirements
------------------

.. Define the selection criteria

[[Each simplification restricts the physical scenarios that a model can
represent, so the first step in selecting a method is to establish what
characteristics of the foil geometry and flight conditions are relevant to
paraglider simulations.

Start with the geometry and flow-field since they establish the selection
criteria. Cover issues like nonlinear geometry, slow airspeed,
non-longitudinal, wind shear, high angle of attack, etc.]]


Model selection
---------------

* [[FIXME: Survey the methods and progressively eliminate them. Include
  citations with an overview of aerodynamic models, like Drela. Section
  profiles were covered in the previous chapter so that terminology is
  available.

* [[Survey the available models (LLT, VLM, panel methods, CFD, etc).

  What simplifying assumptions do they make regarding the geometry? What
  simplifying assumptions do they make regarding the flow-field (viscosity,
  compressibility, etc)?

  What are their limitations? (spanwise flow, flow separation, linear
  coefficients, uniform wind, etc)

  **Should I discuss these separately?** For example, does it make sense to
  declare that the LLT assumes the wing is straight without the context that
  it models the flow-field using a variable-strength vortex filament? Not sure
  how to broach this discussion.]]

* [[Some of these models are already being used in literature to estimate the
  performance of parafoils. Explain why methods that "work" for other papers do
  not meet the performance criteria for **this** project.]]


* Classical LLT fails with non-linear geometry, VLM handles non-linear geometry
  but assumes linear aerodynamics and neglects thickness, which can be
  significant for parafoils, CFD is too slow.

* Only Phillips' NLLT met my requirements (except no open source
  implementations were available at the time).


Phillips' numerical lifting-line
================================

.. What is this method? Why did I choose it?

Phillips' numerical lifting-line method (NLLT)
:cite:`phillips2000ModernAdaptationPrandtl` is an extension of Prandtl's
classic *lifting-line theory* (LLT) to account for the effects of a curved
lifting-line.

Unlike the classical LLT, this numerical approach supports the characteristic
nonlinear geometry of parafoils by decomposing the foil into discrete wing
segments, each with their own scale, position, orientation, and profile. It can
also be adapted to non-uniform wind vectors, allowing it to analyze
non-uniform, non-longitudinal scenarios involving wind shear and wing rotation.

Unlike pure potential flow solutions, such as traditional vortex lattice and
surface panel methods, it is able to approximately account for the effects of
viscosity through its use of section coefficients (critical for incorporating
viscous drag corrections and approximating flow behavior at high angles of
attack).

And unlike full CFD solvers, the implementation is relatively simple, requires
minimal manual configuration, and is computationally efficient (a critical
point when generating iterated solutions for flight simulation).


Derivation
----------

For the purposes of discussion, the derivation of Phillips' NLLT is briefly
repeated here using the notation of this paper. Note that to avoid confusion,
this derivation breaks the convention of this paper and instead uses Phillips'
convention of a capital :math:`\vec{V}` for velocity, and a lowercase
:math:`\vec{v}` for the induced velocities.

.. Also, he uses `r` a bit differently; they're still position vectors, but
   implicitly wrt the origin. Also, `r0 = r2 - r1`.

.. figure:: figures/paraglider/dynamics/phillips_scratch.*

   Wing sections for Phillips' method.

The goal is to establish a system of equations by equating two measures of the
aerodynamic force applied to discrete segments of a wing. One uses the 3D
vortex lifting law :eq:`section lift, 3D vortex lifting law` and the other uses
the local section lift coefficients :eq:`section lift, coefficients`:

.. math::
   :label: section lift, 3D vortex lifting law

   \vec{\mathrm{d}F}_i = \rho \Gamma_i \vec{V}_i \times \mathrm{d}\vec{l}_i

.. math::
   :label: section lift, coefficients

   \norm{\vec{\mathrm{d}F}_i} =
     \frac{1}{2}
     \rho_\textrm{air}
     \norm{\vec{V}_i}^2
     C_{L_i} \left( \alpha_i, \delta_i \right)
     A_i

[[FIXME: define *control point*]]

The net local velocity :math:`\vec{V}_i` at control point :math:`i` is the sum
of the freestream relative wind velocity :math:`\vec{V}_{\infty}` at the
control point and the induced velocities from all the other segments:

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
vortex :math:`i` is the difference between the two measures of section lift,
:eq:`section lift, 3D vortex lifting law` and :eq:`section lift, coefficients`:

.. math::
   :label: horseshoe vortex strength optimization target

   f_i \left( \Gamma_i \right) =
      2 \Gamma_i \norm{\vec{W}_i}
      - \norm{\vec{V}_i}^2 A_i C_{L,i} \left(\alpha_i, \delta_i \right)

where

.. math::
   :label: unlabeled1

   \vec{W}_i = \vec{V}_i \times \mathrm{d} \vec{l}_i

The set of residuals :math:`f_i \left( \Gamma_i \right)` represent a system of
nonlinear equations that can be solved numerically to produce an estimate of
the spanwise circulation :math:`\Gamma_i`. In order to solve the system,
Phillips suggests gradient descent using the system Jacobian :math:`J_{ij}
\defas \frac{\partial f_{i}}{\partial \Gamma_j}`, which expands to:

.. math::
   :label: phillips jacobian

   \begin{aligned}
   J_{ij} =\;
      &\delta_{ij}\, 2 \norm{\vec{W}_i}
      + 2\, \Gamma_i \frac {\vec{W}_i} {\norm{\vec{W}_i}}
          \cdot \left( \vec{v}_{ji} \times \mathrm{d} \vec{l}_i \right)\\
      &- \norm{\vec{V}_i}^2 A_i
         \frac
            {\partial C_{L,i}}
            {\partial \alpha_i}
         \frac
            {V_{a,i} \left( \vec{v}_{ji} \cdot \vec{u}_{n,i} \right)
            - V_{n,i} \left( \vec{v}_{ji} \cdot \vec{u}_{a,i} \right)}
            {V_{ai}^2 + V_{ni}^2}\\
      &- 2 A_i C_{L,i}(\alpha_i, \delta_i)(\vec{V}_i \cdot \vec{v}_{ji})
   \end{aligned}

with the effective wind speed in the normal and chordwise directions

.. math::
   :label: section axes

   \mat{C}_{f/s_i} =
      -\begin{bmatrix}
         | & | & | \\
         \vec{u}_{a,i} & \vec{u}_{s,i} & \vec{u}_{n,i} \\
         | & | & | \\
      \end{bmatrix}

.. FIXME: I hate that `s` refers to both section and spanwise here

.. math::
   :label: section wind speeds

   \begin{aligned}
      V_{a,i} &= \vec{V}_i \cdot \vec{u}_{a,i}\\
      V_{n,i} &= \vec{V}_i \cdot \vec{u}_{n,i}
   \end{aligned}

and the *effective local angle of attack* :math:`\alpha_i`

.. math::
   :label: effective local angle of attack

   \alpha_i = \arctan \left( \frac {V_{a,i}} {V_{n,i}} \right)

After solving for the circulation strengths, the 3D vortex lifting law
:eq:`section lift, 3D vortex lifting law` is used to compute the inviscid
forces at each control point, and the viscous drag and pitching moments are
computed as in standard *strip theory* using the effective angle of attack
:eq:`effective local angle of attack`:

.. math::
   :label: section moment

   \vec{\mathrm{d}M}_i =
     -\frac{1}{2}
     \rho_\textrm{air}
     \norm{\vec{V}_i}^2
     A_i
     c_i
     C_{M_i} \left( \alpha_i, \delta_i \right)
     \vec{u}_{s,i}


Modifications
-------------

.. Changes and improvements on the original Phillips paper

Although the original derivation is suitable for simple, static scenarios, it
is inadequate for simulating dynamic conditions that commonly occur during
paraglider flights. This section presents a small number of modifications to
improve the usability, functionality, and numerical stability of the method
that greatly extend its applicability.


Control point distribution
^^^^^^^^^^^^^^^^^^^^^^^^^^

The paper recommends placing the control points using a cosine distribution
over the 3D spanwise coordinate :math:`y`, but that recommendation assumes
a predominantly flat wing; cosine spacing generates a poor distribution when
the wing tips are nearly vertical, which is common with parafoils. Instead,
distributing the control points according to the *section index* :math:`s` will
maintain spacing along the foil's :math:`yz`-curve regardless of the arc. (Note
that although this works well for parafoils, other foil geometries may be
better suited to either a different section index, or some nonlinear spacing in
:math:`s`.)


Variable Reynolds numbers
^^^^^^^^^^^^^^^^^^^^^^^^^

Lifting-line methods typically assume the section coefficient data is an
explicit function of angle of attack :math:`\alpha`, and possibly some sort of
control deflection :math:`\delta`, but assume the coefficients are constant
with respect to Reynolds number. For relatively high Reynolds regimes this is
reasonable since the airfoil data is essentially constant, but parafoil
sections under typical flight conditions experience Reynolds numbers in the
range from roughly 150,000 to 3,000,000, spanning the transitional regime where
viscous effects can be significant. To verify whether section-local Reynolds
numbers have a significant effect on parafoil aerodynamics, the coefficients
should be an explicit function of Reynolds number.


Non-uniform upstream velocities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phillips' original derivation :cite:`phillips2000ModernAdaptationPrandtl`
assumes uniform flow, but :cite:`hunsaker2006LiftinglineApproachEstimating`
relaxes that assumption by replacing the uniform *freestream velocity*
:math:`V_{\infty}` with the relative *upstream velocity* :math:`V_{rel,i}` that
"may also have contributions from prop-wash or rotations of the lifting surface
about the aircraft center of gravity." (Compare Phillips Eq:5 to
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
     + \vec{r}_{CP,i/CM} \times \vec{\omega}_{b/e}

This change enables the method to approximately accommodate non-uniform wind
conditions, such as from wind shear, turning maneuvers, etc. This flexibility
should be used with caution, however; see `Straight-wake assumption`_ for
a discussion.


Better solver
^^^^^^^^^^^^^

.. FIXME: section title

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
function reliably produces fixed points; a simple prototype failed to converge.

An alternative is to use a robust, hybrid root-finding algorithm that uses
gradient descent for speed but switches to a line-search method when the
gradient goes to zero. The implementation for this project had great success
with a modified `Powell's method
<https://en.wikipedia.org/wiki/Powell%27s_method>`__, which "retains the fast
convergence of Newton's method but will also reduce the residual when Newton's
method is unreliable" (see the `GSL discussion
<https://www.gnu.org/software/gsl/doc/html/multiroots.html#c.gsl_multiroot_fdfsolver_hybridsj>`__
or MINPACK's `hybrj documentation
<https://www.math.utah.edu/software/minpack/minpack/hybrj.html>`__ for more
information). This method not only mitigates the convergence issues near stall,
but it is also significantly faster: it does not depend on fixed step sizes
(which must be inherently pessimistic to encourage convergence) and is able to
use approximate Jacobian updates instead of requiring full Jacobian evaluations
at each step.

.. For this project, the `glidersim` implementation of Phillips' method uses
   the `hybrj
   <https://www.math.utah.edu/software/minpack/minpack/hybrj.html>`_ routine
   from the `MINPACK` package via the Python interface provided by `scipy's
   \`optimize\` module
   <https://docs.scipy.org/doc/scipy/reference/optimize.root-hybr.html>`_.


Reference solutions
^^^^^^^^^^^^^^^^^^^

The root-finding algorithm that solves for the circulation strengths requires
an initial proposal for the *circulation distribution* :math:`\Gamma(s)`. Poor
proposals produce large residual errors that can push Newton iterations into
unrecoverable states, so it is preferable to use prior information to predict
the true distribution. The original paper suggested solving a linearized
version of the equations, but that choice is only suitable for foils with no
sweep or dihedral. Another common suggestion from related methods is to assume
an elliptical distribution; for most foils, an elliptical circulation
distribution is a reasonable guess during straight and steady flight, but it is
a poor proposal for scenarios that include non-uniform wind or asymmetric
control inputs, such as during flight maneuvers. It is clear that generating
suitable proposals for nonlinear geometries under variable flight conditions
requires a different approach.

For sequential problems, such as the sequence of states in a flight simulator
or the points of a polar curve, an effective solution is to use the solution
from the previous iteration as the proposal. Provided the time resolution of
the simulation is reasonably small then the state of the aircraft should be
similar between each timestep, so the proposal will be very close to the
target. An added advantage of using a prior solution is an ability to capture
hysteresis effects :cite:`owens1998WeissingerModelNonlinear`.

.. FIXME: There is a remaining problem is how to bootstrap the "previous"
   solution. When no previous solution is available the easiest target is to
   straight and steady flight with zero control inputs. As mentioned earlier,
   an elliptical is a reasonable proposal for most wings in that state. Given
   the solution to the "easy" problem, try to solve the target. If the method
   does not converge, pick an intermediate problem midway between the
   reference and target, solve for that, then use its solution as the proposal
   for the target. Repeat subdividing the problem until convergence is
   achieved.

   Related: `Sensitive to initial proposal`_.


Clamping section coefficients
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One significant issue with the method is a tendency to produce fictitious
"infinite" induced velocities, causing convergence to fail. This tendency
increases as the grid resolution is refined, and is most commonly observed at
the wing tips, especially during turning maneuvers. The cause is apparent in
equation :eq:`induced velocities`, where the induced velocities between bound
segments increases as the inverse of their separation distance; as the
separation distance goes to zero, the induced velocity goes to infinity. In
most cases, the induced velocities from the left and right neighbors of
a segment mostly cancel, but if the foil has discontinuities (such as at the
wingtips, where the outer segment has only an inboard neighbor) then
cancellation may be incomplete, leaving a large imbalance. It can also occur
due to numerical issues at very fine grid resolutions.

.. For a related problem, see also `Unstable at high resolution`_.

For parafoils the most significant discontinuities are at the wingtips, where
the effect of the induced velocity spike is to dramatically overestimate the
effective angle of attack. The NLLT relies on accurate section coefficient
data, and if that coefficient data is unavailable (such as at high angles of
attack) then the numerical routine cannot continue, causing convergence to
fail.

Clearly the lack of coefficient data is not a valid reason to abort, since the
large induced angle of attack is fictitious. To mitigate the issue when it
occurs at the wingtips, assume the true :math:`\alpha` is less than or equal to
the maximum :math:`\alpha` supported by the coefficient data, and clamp
:math:`C_L` to its value at that maximum :math:`\alpha`. In the case where the
high :math:`\alpha` is fictitious, the :math:`C_L` will be incorrect but will
at least remain relatively close to the true value, and will allow the
simulation to continue. In the case where :math:`\alpha` is genuinely large,
then the unclamped inboard segments will also lack coefficient data and the
method will correctly fail.

It is important to note that this is a practical mitigation, not
a theoretically-justified solution. The point is not to "fix" the method, the
point is to limit the magnitude of the error and allow the simulation to
continue with reasonable accuracy. However, despite lacking a theoretical
basis, there are several strong justifications:

#. If the outer segment is small, then its contribution to the error is
   expected to be small. For example, if the outer segment represents the last
   5% of the wing span means then the error from much less than 5% of the total
   aerodynamic contributions (since the area of that wingtip segment is very
   small).

#. If the outer segment is small, you wouldn't expect a significant change in
   alpha from the wingtip to its neighbor, so if the inboard neighbor is in the
   valid range you can expect that the wingtip alpha is (relatively) close to
   the valid range.

   [[The :math:`C_L` curve stays (relatively) flat for significant range of
   :math:`\alpha` post-stall, so the true value of :math:`C_L` should be
   relatively close to the clamped value, so even if :math:`\alpha_\textrm{true}
   > \alpha_\textrm{max}`, it's unlikely for :math:`C_L(\alpha_\textrm{max})`
   to be wildly inaccurate (provided the section coefficient data covers
   a reasonably high :math:`\alpha`).]]


.. FIXME:

   * The section coefficients assume minimal spanwise flow, which is already
     massively violated, which means I already expect the wing tip values to be
     borderline useless anyway.

   * A caveat of my implementation is that it only clamps `alpha_max`, assuming
     the fictitious alpha are always POSITIVE at the wing tips. For a rigid
     wing at a very negative alpha the fictitious alpha would be negative, but
     I'm neglecting that scenario since such a negative alpha would induced
     a frontal collapse anyway, at which point the model would already be
     totally broken.

   * Clamping seems to have eliminated the need for "relaxed" solutions? Should
     I retain that section? Not sure I ever trigger it anymore.


Limitations
-----------


Assumes minimal spanwise flow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method argues that the derivation of the 3D vortex lifting law in
:cite:`saffman1992VortexDynamics` proves that "the relationship between section
lift and section circulation is not affected by flow parallel to the bound
vorticity." In other words, it relies on the fact that the 3D vortex lifting
law holds even in the presence of spanwise flow. What this does not account
for, however, is the effect of spanwise flow on the section coefficients. Wing
analysis using section coefficients relies on the assumption that each wing
segment acts as a finite segment of an infinite wing, provided the spanwise
flow is negligible (:cite:`bertin2014AerodynamicsEngineers`, p. 356). Although
the 3D vortex law holds in the presence of spanwise flow, solving for the
circulation strengths using section coefficients does not.

A similar discussion can be found in :cite:`owens1998WeissingerModelNonlinear`,
who apply a similar NLLT to a flat wing with 45° sweep. They acknowledge that
although the sweep introduces significant 3D flow-field effects, the method
"shows very good agreement" versus experimental measurements. Their success
offers some confidence that the effects of spanwise flow may indeed be
negligible, but it is unclear whether the effect has more significance once
continuous arc anhedral is involved.

[[FIXME: good place to cite `goates2021`? He talks about swept wings.]]


Straight-wake assumption
^^^^^^^^^^^^^^^^^^^^^^^^

A common aerodynamic modeling approximation is to assume that vorticity is shed
into the wake as a trailing *vortex sheet*; the strength of the shed vorticity
varies with the local variation of lift along the span. In a rigorous analysis,
the trailing vorticity should follow a curved path
(:cite:`bertin2014AerodynamicsEngineers`, p. 390), but this produces an
intractable nonlinear system of equations. Instead, models apply a further
simplification known as the *straight-wake assumption*: that the trailing *wake
vortex sheet* streams straight back from the lifting-line. The straight-wake
assumption is an important step in linearizing the system of equations to allow
mathematically tractable solutions.

For a discretized method, such as Phillips' or Weissinger's LLT
:cite:`weissinger1947LiftDistributionSweptback`, the vortex sheet is lumped
into a series of shed vortex filaments whose strength is proportional to the
difference in local lift of neighboring segments. Under the straight-wake
assumption, the trailing legs of all horseshoe vortices extend from the nodes
in straight lines parallel to some *freestream velocity* direction
:math:`\vec{u}_{\infty}` (see :eq:`induced velocities`). This is clearly
invalid for a rotating wing where a freestream velocity is ambiguous.

Despite this limitation, this project assumes that as long as the rotation
rates remain small enough that relative flow angles remain small the method
still provides useful approximations. This assumption is made without
theoretical justification; instead, this paper relies on the superior
aerodynamics knowledge of its sources. First, the use of this method with
non-zero rotation is explicitly mentioned in
:cite:`hunsaker2006LiftinglineApproachEstimating`. Also, this assumption is
shared with the vortex-lattice model used in `AVL
<https://web.mit.edu/drela/Public/web/avl/>`_, although in that method the
trailing legs are aligned with the foil :math:`x`-axis, regardless of
freestream flow. In Phillips' method the trailing are aligned to the
freestream, which for this work is defined as the local upstream velocity
:math:`\vec{u}_{\infty,0}` of the central section under the assumption that it
minimizes average deviation.

For a related technical discussion that incorporates rotation rates into
a vortex lattice method, refer to :cite:`drela2014FlightVehicleAerodynamics`
Sec. 6.5; in particular, Eq. 6.33 for aligning the trailing legs with the
:math:`x`-axis and Eq. 6.39 for incorporating the rotation rates into the
aerodynamic influence coefficients matrix.


Reliance on section coefficients
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A significant limitation of aerodynamic methods based on the theory of *wing
sections* their assumption that the section coefficient data is accurate and
representative of the flow conditions during a flight. In practice, section
coefficient data is notoriously optimistic, relying on idealized geometry,
negligible spanwise flow, a uniform flow-field across the segment, steady-state
conditions, etc. These assumptions are strong to begin with, and become
particularly questionable near stall, especially when using simulated airfoil
data.

Not only do these methods assume the section coefficient data is accurate for
each individual section in isolation, they also assume the flow conditions of
each section will have a negligible impact on the coefficients of neighboring
sections. In reality, development of 3D flow-field conditions such as
separation bubbles is significantly impacted by such neighboring sections. Part
of the interaction can be captured by the induced velocities, but section
coefficients are ultimately incapable of modeling effects such as turbulence,
3D separation bubbles, significant spanwise (or "cross") flow, etc. Such
effects seem likely to be even more prominent given the significant arc of
a parafoil.

.. "The greatest compromise in using lifting-line theory into the stall
   angle-of-attack range and beyond is the use of data for the two-dimensional
   flow around an airfoil. The actual flow for this configuration is a complex,
   three-dimensional flow with separation."
   (:cite:`bertin2014AerodynamicsEngineers`, p.384, last paragraph)


No unsteady effects
^^^^^^^^^^^^^^^^^^^

This method produces a steady-state (non-accelerated) solution. It does not
include unsteady (time-varying) effects, such as
(:cite:`drela2014FlightVehicleAerodynamics`, p. 149):

* Unsteady foil motion

* Unsteady foil deformation

* Spatially-varying or unsteady atmospheric velocity field

Thankfully, the (arguably) most important unsteady effect for the purposes of
paraglider simulation under typical flight conditions can be accounted for by
the simulator itself; see :ref:`paraglider_components:Apparent mass`.


Non-unique solutions
^^^^^^^^^^^^^^^^^^^^

Gradient descent will find a zero of the residual, but it is not guaranteed to
be unique, especially given that the numerical solver relies on tolerances
instead of exact solutions. Depending on the initial conditions, the solver may
converge to different circulation distributions.

.. See `demonstration:Bonk`_.


.. Unstable at high resolution
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^

   [[**FIXME**: finish writing]]

   This method places the control points on the lifting-line, which causes
   issues as the number of control points is increased (the grid is refined).
   Recall the **very** informative discussion in Sec:8.2.3 from "Understanding
   Aerodynamics" (McLeanauth; 2013): "a curved lifting-line has infinite
   self-induced velocity" and "locating the control points away from the bound
   vortex is still the only way to have a general formulation that doesn't
   behave badly as the discretization is refined".

   [[The reason the effect becomes more significant as the number of segments
   is increased can be seen in :eq:`induced velocities`. As distance between
   the segments is reduced, the denominators decrease, the induced velocities,
   and the "imbalance" at the wing tip increases. (I think.)]]

   See also :cite:`chreim2018ChangesModernLiftingLine`, p. 3: long discussion
   of the PBC, and later on he notes "the circulation distribution becomes
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

   [[Most of those papers are discussing problems for wings with sweep, but it
   seems like it'd also apply to wings with dihedral. Why wouldn't it? Oh, note
   to self: big difference between a wing with dihedral versus **a wing with
   sweep is that the wing with sweep will (probably?) experience significant
   spanwise flow.** Also, for a swept wing the set of bound vortices are not
   planar, which (I think) would mean they will induce velocities experienced
   at each other (whereas if they are planar then it's just the trailing
   vortices that influence the neighbors?)]]


Sensitive to initial proposal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This method relies on a good proposal (an initial "guess" of the circulation
distribution) to encourage convergence while minimizing optimization runtime.
The root-finding problem uses the residual error :eq:`horseshoe vortex strength
optimization target` which is likely a non-convex function, in which case
a global optimization method such as gradient descent is not guaranteed to find
the global minimum for a non-convex function, so the solution is sensitive to
the starting point (the initial proposal). In practice this issue is not
a major problem when the intended use is flight simulation; solutions are
generated iteratively, in which case the previous solution is a natural choice
for minimizing the initial residual error (see `Reference solutions`). As an
added bonus, using the previous solution adds the capability of capturing
hysteresis effects :cite:`owens1998WeissingerModelNonlinear`; for example, in
:cite:`anderson1980NumericalLiftingLine` they discuss a wing that demonstrates
hysteresis depending on whether data were generated with increasing versus
decreasing alpha. Nevertheless, the fact that the method has a tendency to
produce different solutions for different proposals mean the method will
exhibit hysteresis effects which may or may not be physically accurate.

.. That said, if the reference (previous) solution for the circulation gets
   messy (due to numerical issues) and needs to be "reset" to a clean
   elliptical distribution, discontinuities can appear in the state dynamics
   trajectory. Thankfully the alternative solutions tend to be minor, plus
   section clamping tends to avoid the issue. See `demonstration/bonk.py`


Unreliable near stall
^^^^^^^^^^^^^^^^^^^^^

.. FIXME: section title? "Unreliable" is true, but sounds overly pessimistic

Phillips suggests that this method can be used up to stall "with caution".
Closely related to the issues of spanwise flow, the development of stall
conditions along a wing has a high likelihood of violating the assumptions used
to generate the section coefficients. Worse, the flexible nature of a parafoil
will exacerbate the effects of section stall, which cause the profiles to
deform and wrinkle even more than normal. Nevertheless, this project attempts
to apply the method to "near stall" conditions under the belief that, for the
purposes of flight reconstruction, it is preferable to get a low-quality
estimate as opposed to no estimate at all. It is vital, however, for the
filtering architecture to model the increased uncertainty as sections approach
stall conditions.

.. A related discussion in :cite:`owens1998WeissingerModelNonlinear`
   acknowledges that their NLLT "does not predict the high angle-of-attack
   aerodynamics for wings that produce a LE vortex. In other words, this method
   limited to wings with moderate to thick airfoils and moderate sweep." It is
   plausible presume the same applies to Phillips'.


Case study
==========

.. Validate the performance of Phillips' method for analyzing a parafoil canopy
   in steady-state conditions.

This section considers the ability of Phillips' NLLT to predict the
aerodynamics of a typical paraglider geometry. It continues the discussion from
:ref:`Foil Geometry:Case Study <foil_geometry:Case study>` by comparing the
theoretical predictions of several aerodynamics models against experimental
wind tunnel data.


Wind tunnel data
----------------

.. Describe the test setup and the data

As explained in :cite:`belloc2015WindTunnelInvestigation`, a 1/8th-scale model
was fabricated from wood and [[material]], mounted on a 1 meter rod connected
to force sensors, and placed in a wind tunnel configured for 40 m/s airspeed.
Measurements were taken with the angle of attack and sideslip ranging over
:math:`-5 < \alpha < 22` and :math:`-15 < \beta < 15`.

.. This range of alpha is suitable for capturing longitudinal performance
   post-stall.

For better accuracy, wind tunnel measurements should be corrected for wall
interactions with the flow (:cite:`barlow1999LowSpeedWindTunnel`;
:cite:`drela2014FlightVehicleAerodynamics`, Sec. 10.3). However, because
classical wind tunnel wall corrections assume a flat wing, the data for the
arched parafoil are uncorrected for wall effects.


Aerodynamics models
-------------------

[[Introduce the aerodynamic models I'll be comparing against the NLLT:
a traditional *vortex lattice method* (VLM) in `AVL
<https://web.mit.edu/drela/Public/web/avl/>`_ , and an experimental VLM in
`XFLR5 <https://www.xflr5.tech/xflr5.htm>`_ (which tilts the geometry to
mitigate the "small angles" approximation for alpha and beta).]]


Experimental vs theoretical results
-----------------------------------

.. FIXME: I removed the VLM results from XFLR5 for the moment coefficients
   because they were VERY wrong; looks like they were using the wrong reference
   point somehow, but it's not clear from the documentation what's wrong.


Coefficients vs angle of attack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

[[Coefficients versus angle of attack :math:`\alpha`, measured at four
different angles of sideslip :math:`\beta`]]

.. figure:: figures/paraglider/belloc/CL_vs_alpha.*
   :name: Belloc_CL_vs_alpha

   Lift coefficient vs angle of attack.

.. figure:: figures/paraglider/belloc/CD_vs_alpha.*
   :name: Belloc_CD_vs_alpha

   Drag coefficient vs angle of attack.

.. figure:: figures/paraglider/belloc/Cm_vs_alpha.*
   :name: Belloc_Cm_vs_alpha

   Pitching coefficient vs angle of attack.

[[This is the global pitching coefficient, which includes contributions from
both the section pitching coefficients and the aerodynamic forces. These
coefficients are computed using the riser midpoint `RM`.]]


Coefficients vs sideslip
^^^^^^^^^^^^^^^^^^^^^^^^

[[Coefficients versus angle of sideslip :math:`\beta`, measured at four
different angles of attack :math:`\alpha`]]

.. figure:: figures/paraglider/belloc/CY_vs_beta.*
   :name: Belloc_CY_vs_beta

   Lateral force coefficient vs sideslip.

.. figure:: figures/paraglider/belloc/Cl_vs_beta.*
   :name: Belloc_Cl_vs_beta

   Rolling coefficient vs sideslip.

.. figure:: figures/paraglider/belloc/Cn_vs_beta.*
   :name: Belloc_Cn_vs_beta

   Yawing coefficient vs sideslip.


Coefficients vs each other
^^^^^^^^^^^^^^^^^^^^^^^^^^

[[This is the classic way to consider the overall performance of a wing.]]

.. Pseudo-inviscid results; requires setting `Cd = 0`

   .. figure:: figures/paraglider/belloc/CL_vs_CD_pseudoinviscid.*
      :name: Belloc_CL_vs_CD_pseudoinviscid

      Pseudo-inviscid lift coefficient vs drag coefficient.

   [[Demonstrates how well the NLLT lift matches XLFR5's "Tilted Geometry"
   method over the lower range of alpha. Once alpha approaches stall, the NLLT
   diverges since it's not a true inviscid method; it's using the viscous lift
   coefficients to determine the circulation distribution.]]

.. figure:: figures/paraglider/belloc/CL_vs_CD.*
   :name: Belloc_CL_vs_CD

   Lift coefficient vs drag coefficient.

.. figure:: figures/paraglider/belloc/CL_vs_Cm.*
   :name: Belloc_CL_vs_Cm

   Lift coefficient vs global pitching coefficient.


Discussion
----------

.. FIXME: create an outline. There are two aspects to this discussion:

   1. Performance in general (does the model agree with the wind tunnel data?)

   2. Performance relative to the *model selection* criteria (how well do
      I expect the model to work for dynamic paraglider simulations?)

* Does the NLLT include the empirical viscous drag corrections?

* The inviscid solutions agree with the NLLT quite well for small angles of
  attack. I think the deviation occurs when the "thin boundary layer"
  assumption starts to break down; for the 2D lift coefficient, the BL really
  starts to thicken around alpha=12, so when you consider the **effective**
  angle of attack it happens around alpha=9? Seems about right. I'm not sure if
  flow separation is involved, but I don't think that tends to happen until
  after a section exceeds `Cl_max`?

* The VLM and NLLT disagree on the zero-lift angle of attack? Hm. That seems to
  suggest bad airfoil coefficients, doesn't it? I would think you'd have the
  least amount of flow separation at that alpha; is that intuition correct? Or
  maybe BL thickness is already significant at that angle; I should check the
  overall spanwise alphas.

* The wind tunnel data is only testing the **uniform** flow-field case. In my
  simulations I'm using this method for **asymmetric** flows (spanwise
  variation in speed and/or direction). That's definitely questionable (similar
  to what I mention about assuming the trailing wake is aligned to the central
  freestream: highly questionable).

  Not a big deal though; I just need to be clear that the point isn't to claim
  this is a great model; I just need something useful for testing the geometry
  and "good enough" for simulations.

  **This was always meant to be used in an uncertain environment (stochastic
  simulations). As long as the choice of aerodynamic method is not the dominant
  source of error, I'm fine with it.**


* Did Belloc account for hysteresis? In
  :cite:`anderson1980NumericalLiftingLine` they plots how both the experimental
  and numerical data were strongly affected by increasing vs decreasing alpha.

  TODO: run the numerical solutions forward and backwards in alpha!

* I'm frustrated that the lift curve for all methods is so high compared to the
  wind tunnel data, but at least the NLLT matches AVL, XFLR5, and MachUpX, so
  I'm pretty confident I've implemented it correctly. I need to make a list of
  explanations for the discrepancies though: unmodeled viscous effects in
  particular, but there's still the chance of an issues with the `CZa` or
  `Alphac` values in the wind tunnel data.

  Also, maybe it's not such a terrible result overall? It is a pretty low
  aspect ratio wing, after all. See Fig:7.22 of
  :cite:`bertin2014AerodynamicsEngineers` shows theoretical vs experimental CL
  for a wing with AR=5.3; the theoretical estimate significantly overestimates
  (IMHO) the lift coefficient, but the author calls it a "reasonable" estimate.

  Possibly related to the lift discrepancy:

  * "Aerodynamics for Engineers", p. 326, he discusses the effects of
    a "separated wake", although that's in the context of airfoils. Still it
    does have the same look as my data.

  * In https://www.xflr5.tech/docs/Part%20IV:%20Limitations.pdf, p. 29, he
    mentions that the "flat wake" assumption (no wake roll-up) causes an
    overestimation of the vortex strengths (and thus the lift), and that the
    error can be in the order of 1% to 10% for the lift and induced drag.

* Why is this a good/useful test?

  * The range of angle of attack is suitable for capturing the longitudinal
    performance of the wing post-stall

  * The range of sideslip angles is useful for considering the impact of the
    `Straight-wake assumption`_ for a non-rotating wing.

    FIXME: how is the straight-wake assumption under question for
    a non-rotating wing? It's important for aerodynamic models that assume the
    wind is head on, I think; isn't that the issue that the experimental VLM2
    in XFLR5 is meant to address? Like, doesn't AVL "assume" the wind is head
    on then make corrections instead of modeling the wind directly?

  * In terms of aerodynamics: good representation of the unusual geometry of
    a paraglider; completely known geometry (including airfoil); extensive data
    for a range of wind conditions; internal wood structure maintains the
    shape, eliminating uncertainty due to distortions

  * It also provides a good demonstration of how to use my geometry.
