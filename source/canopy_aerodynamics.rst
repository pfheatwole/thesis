*******************
Canopy Aerodynamics
*******************

The paraglider dynamics are complicated enough on their own, so for now I'm
splitting the canopy aerodynamics into their own section.


The classic method for estimating the aerodynamic performance of a wing is
Prandtl's *lifting-line theory* (LLT). This deceptively simple model allowed
analytical solutions to the lift distribution.

For wings with significant sweep and/or dihedral, the classic LLT breaks down.
These more complex geometries require adaptations to account for the
non-linear behaviors, resulting in *non-linear lifting line* (NLLT) theories.
These are often also known as "numerical" lifting-line theories, since they
require numerical solutions.

Related work:

* :cite:`gonzalez1993PrandtlTheoryApplied`


Inviscid methods
================

* It'd be cool to show a purely inviscid analysis first. Those are more common
  in many analyses, and more commonly applied to unusual geometry. I can use
  its poor performance to motivation Phillips' method. It also gives me the
  chance to introduce the method (since I'll need to discuss it at some point
  anyway before I compare it with Phillips).

* Notice there are a variety of limitations to my chosen inviscid model: see
  https://www.xflr5.tech/docs/Part%20IV:%20Limitations.pdf. When I say
  "this is what inviscid methods produce", what I really mean is "this is the
  performance of the particular inviscid method I applied"


Viscous methods
===============

Lifting-line
------------

[[Describe the classic approach and its limitations.]]


Section Coefficients
--------------------

[[Do these have any application to inviscid methods? I think Prandtl's
lifting-line is a *potential flow* method, but it also uses the section
coefficients, so I'm confused.]]


Related work:

* :cite:`abbott1959TheoryWingSections`

Instead of solving the boundary layer conditions for the full 3D wing, it is
common to treat the lifting surface as a collection of finite segments taken
from theoretical infinite-length wings. The infinite length assumption
eliminates 3D effects and allows the wing sections to be analyzed using 2D
geometry. The 3D flow of the physical wing can then be approximated using the
2D aerodynamic coefficients.

Limitations:

* This method assumes straight, uniformly shaped wing segments. For
  a continuously curved wing, this approximation will never be correct,
  although the approximation improves as the number of segments increases.

* It assumes the finite segments are well approximated by the flow over the
  infinite wing. This neglects spanwise variation in boundary layers, etc.

* It is difficult to model cell distortions (due to billowing, etc) using
  predetermined 2D geometry. It is technically possibly to estimate the final
  cell shapes and measure the section profiles, but the "infinite wing"
  approximation is unlikely to remain valid. If the aerodynamic effects of
  cell distortions are of interest, they are best treated either
  approximately, using averaged coefficient effects, or using full
  computational fluid dynamics methods. This current work neglects the effects
  of cell distortions and assumes all wing segments match the idealized 2D
  airfoils.


Phillips' numerical lifting-line
================================

* In Phillips' original derivation they assumes uniform flow for Eq:5, but I'm
  using the non-uniform version from Hunsaker-Snyder Eq:5. Hunsaker mentions
  that this *local upstream velocity* `V_rel,i` "differs from the global
  freestream velocity `V_inf` in that it may also have contributions from
  prop-wash **or rotations of the lifting surface about the aircraft center of
  gravity.**" Is he implying that Phillips' method is useable as-is during
  rotations?

* I'm using airfoil data from XFOIL, which is unreliable post-stall, but I'm
  including significant post-stall coefficient data anyway to observe how
  Phillips' method behaves in those regions. It's useful to understand how the
  method behaves in post-stall regions in the event you have accurate
  post-stall airfoil data. (ignoring the fact that the 3D wing basically
  shoots that to heck anyway)

* By using section coefficient data, I'm ignoring cross-flow effects. I'm sure
  the arc of the wing has a significant effect on the boundary layer, which
  we're assuming is constant over the entire section.

* Why am I choosing this method? It provides a reasonable tradeoff between
  accuracy and computational efficiency, it seemed easier to implement than
  other methods, it allowed me to incorporate viscous effects, and the fact
  that it only needs the quarter-chord means it's easy to use with simple
  geometry definitions (I wanted the geometry as simple as possible).

  I needed a method that can handle sweep, dihedral, twist, asymmetric
  geometry (brake deflections), asymmetric wind (turning), non-linear lift
  coefficients.


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
      \left(\alpha_i, \delta_i \right)
      A_i

Alternative form using explicit norms of vectors instead of using scalars as
the implicit norms:

.. math::
   :label: differential lifting force 2

   \left\| \vec{\mathrm{d}F}_i \right\| =
      \frac{1}{2}
      \rho
      \left\|\vec{V}_i\right\|^2
      C_{L_i} \left(\alpha_i, \delta_i \right)
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

   \vec{v}_{ji} = \frac{1}{4\pi}
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

   \delta_{ji}=
   \begin{cases}
      1\quad &i = j\\
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

The Jacobian :math:`J_{ij} = \frac{\partial f_{i}}{\partial \Gamma_j}` expands
to:

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


Limitations
-----------

* Treats the wing as a composite of segments from infinitely long wings (ie,
  it assumes 2D coefficients are accurate representations of the 3D segments).
  This assumption implies steady state conditions, uniform boundary layers
  across the segments, no cross-flow, etc. The 2D coefficients also make an
  assumption about the center of pressure, so I'm guessing it'll affect the
  segment pitching moments.

* It uses the Kutta-Joukowski theorem for the section lift. I think the KJ
  theorem assumes uniform fluid velocity, steady-state, and unseparated? Is
  the KJ assuming inviscid flow, ie it's a potential flow solution?

* Can't model a spin (backwards airflow on one wingtip)


Case Study
==========

(This is where I'll introduce Belloc's reference wing and wind tunnel data.
I can refer to it when I'm showing examples of the chord surface geometries as
an real-world application of the chord surface concept.)

Every new tool should be validated, and for aerodynamic codes validation often
involves comparing theoretical models to wind tunnel measurements. For the
tools proposed in this paper, validation should include demonstrating the
flexibility of the geometry definition proposed in :doc:`canopy_geometry` and
the performance of the aerodynamics code proposed in `Phillips' numerical
lifting-line`_.

An excellent test case for the geometry and aerodynamics is available from
:cite:`belloc2015WindTunnelInvestigation`, which provides both point-wise
geometry data and wind tunnel performance.


Geometry
--------

Chord Surface
^^^^^^^^^^^^^

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

Inputting the values to the canopy geometry produces:

.. raw:: latex

   \newpage

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_curves.*

   ChordSurface curves for Belloc's reference paraglider wing.

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_canopy_chords.*

   3D chords for Belloc's reference paraglider wing.

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_canopy_airfoils.*

   3D airfoils for Belloc's reference paraglider wing.


Airfoils
^^^^^^^^

It uses a NACA 23015.

.. figure:: figures/paraglider/geometry/airfoil/NACA-23015.*

   NACA 23015


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
tunnel corrections", as in :cite:`barlow1999LowSpeedWindTunnel`.]]

Some results:

.. figure:: figures/paraglider/belloc/CL_vs_alpha.*

   Lift coefficient vs angle of attack.

.. figure:: figures/paraglider/belloc/CD_vs_alpha.*

   Drag coefficient vs angle of attack.

.. figure:: figures/paraglider/belloc/Cm_vs_alpha.*

   Global pitching coefficient vs angle of attack.

This is the global pitching coefficient, which includes contributions from
both the section pitching coefficients and the aerodynamic forces. The VLM
estimate appears to be using the wrong reference point, but it isn't clear
from the program documentation what the error might be. The results are left
here for completeness and to highlight the uncertainty in how the VLM was
applied.

.. figure:: figures/paraglider/belloc/CL_vs_CD_pseudoinviscid.*

   Pseudo-inviscid lift coefficient vs drag coefficient.

[[Demonstrates how well the NLLT lift matches XLFR5's "Tilted Geometry" method
over the lower rnage of alpha. Once alpha approaches stall, the NLLT diverges
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

* The inviscid solution (from the VLM) agrees with the NLLT quite well up to
  the alpha where flow separation becomes significant (for the 2D lift
  coefficient, separation seems to ramp up around alpha=12, so when you
  consider the effective angle of attack it happens around alpha=9? Seems
  about right.

* The VLM and NLLT disagree on the zero-lift angle of attack? Hm. That seems
  to suggest bad airfoil coefficients, doesn't it? I would think you'd have
  the least amount of flow separation at that alpha; is that intuition
  correct?
