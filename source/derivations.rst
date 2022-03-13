***********
Derivations
***********


Parametric design curves
========================

The :ref:`"simplified" foil geometry <foil_geometry:Simplified model>` chose
a set of variables :eq:`simplified foil geometry variables` that describe
different aspects of the shape. This section provides definitions for several
of those variables using parametric functions that can approximate the
structure of a typical parafoil using a small number of simple parameters.


Elliptical chord
----------------

A :doc:`foil_geometry` requires a chord distribution :math:`c(s)`. For
parafoils, the chords lengths are most commonly defined by a truncated
elliptical function of section index, in which case the distribution is
a function of two design parameters. The typical choices are either the root
and wingtip chord lengths, or the root length and a taper ratio. Choosing the
root and wingtip chord lengths, a truncated elliptical function over the
section index :math:`-1 \le s \le 1` is then:

.. math::
   :label: elliptical chord

   \begin{aligned}
     a &= \frac{1}{\sqrt{1 - \left(\frac{c_\textrm{tip}}{c_\textrm{root}}\right)^2}} \\
     b &= c_\textrm{root} \\
     c(s) &= b \sqrt{1 - \left( \frac{s}{a} \right)^2}
   \end{aligned}

Refer to :external+glidersim:py:class:`EllipticalChord
<pfh.glidersim.foil_layout.EllipticalChord>` in ``glidersim`` for an
implementation.


Elliptical arc
--------------

In this paper the *arc* of a parafoil is the vector-valued function of
:math:`\left< y, z \right>` coordinates that position the section reference
points. For parafoils, the arc is typically defined by an elliptical function.

.. Explain arc anhedral and section roll. FIXME: draw a diagram

A centered elliptical curve can be defined as a function of four parameters,
but the symmetry of the wing reduces that to three free design parameters, and
normalizing the arc length reduces it to just two. There are several possible
parametrizations, but an intuitive choice is the mean anhedral angle
:math:`\Gamma_\textrm{tip}` and the section roll angle
:math:`\phi_\textrm{tip}` of the wing tips
:cite:`benedetti2012ParaglidersFlightDynamics`. Choosing those parameters to
define an elliptical function that is proportional to the desired
:math:`yz`-curve produces an intermediate result:

.. math::

   \begin{aligned}
     k_1        &= 1 - \frac{\tan(\Gamma_\textrm{tip})}{\tan(\phi_\textrm{tip})} \\
     k_2        &= 1 - \frac{2 \tan(\Gamma_\textrm{tip})}{\tan(\phi_\textrm{tip})} \\
     A          &= \frac{k_1}{\sqrt{k_2}} \\
     B          &= \frac{k_1}{k_2} \tan(\Gamma_\textrm{tip}) \\
     \vec{f}(t) &= \left< A \cos(t), B \sin(t) \right>
   \end{aligned}

.. FIXME: this really needs a diagram

This design requires that :math:`\phi_\textrm{tip} > 2 \Gamma_\textrm{tip}` (so
the wing must be wider than it is tall and the wing tip roll cannot exceed 90°)
and is valid over :math:`t_{min} \le t \le \pi - t_{min}`, where :math:`t_{min}
= \arccos \left( \frac{1}{A} \right)`.

Next although the shape produced by this intermediate result is proportional to
the desired curve, it is not directly usable by the :doc:`foil_geometry`. It
needs two modifications:

1. Make the arc a function of the chosen section index :math:`s`

2. Scale the arc to a total curve length of :math:`b_\textrm{flat}`

Both can be achieved by normalizing the elliptical function to a curve length
of 2. First, scale the axes to produce a new semi-ellipse with a total curve
length of 1:

.. math::

   \begin{aligned}
     L(t)             &= \int_{\frac{\pi}{2}}^{t_{min}} \norm{\vec{f}(t)} dt \\
     k_3              &= L(t_{min}) \\
     \bar{\vec{f}}(t) &= \left< \frac{A}{k_3} \cos(t), \frac{B}{k_3} \sin(t) \right> \\
   \end{aligned}

The fact that the simplified foil geometry chose to define the :ref:`section
index <simplified model section index>` :math:`s` as the linear distance along
the :math:`yz`-curve enables a convenient conversion over :math:`\frac{\pi}{2}
\le t \le t_{min}` and :math:`0 \le s \le 1`:

.. math::

   \begin{aligned}
     \bar{L}(t) &= \int_{\frac{\pi}{2}}^{t_{min}} \norm{\bar{\vec{f}}(t)} dt = s(t) \\
     t(s)       &= s^{-1}(t)
   \end{aligned}

Thus the complete parametric function for the :math:`yz`-curve of the arc is
thus :math:`\left< y, z \right>(s) = \bar{\vec{f}}(t(\left|s\right|))`. The
integrals and inverse functions are not available analytically, but are trivial
to compute numerically. Refer to :external+glidersim:py:class:`EllipticalArc
<pfh.glidersim.foil_layout.EllipticalArc>` in ``glidersim`` for an
implementation.

.. Bonus: you can calculate `\Gamma_\textrm{tip}` directly if you know the
   position coordinates of the wingtip: `\Gamma = arctan(z/y)`


Polynomial torsion
------------------

Like most wings, parafoils use section-relative pitch :math:`\theta(s)`
(conventionally referred to as *geometric torsion*) to fine-tune wing behavior.
The exact distribution of geometric torsion along a wing can be difficult to
measure, but they are frequently described using simple polynomials or
piecewise-linear functions. For idealized models of nonlinear geometries such
as those developed here, a piecewise-polynomial function is assumed to be
adequate.

Assuming a symmetric wing, define three parameters:

* :math:`T`: the maximum torsion (in radians) at the wingtips

* :math:`s_{start}`: the section index where the torsion begins (where :math:`0
  \le s_{start} < 1`)

* :math:`\beta`: the degree of the polynomial (for example, :math:`\beta = 1`
  is linear, :math:`\beta = 2` is quadratic, etc.)

.. math::

   \begin{aligned}
     p(s) &= \frac{|s| - s_{start}}{1 - s_{start}} \\
     \theta(s) & =
       \begin{cases}
         0 & |s| < s_{start} \\
         T p^\beta & |s| \ge s_{start}
       \end{cases}
   \end{aligned}

Refer to :external+glidersim:py:class:`PolynomialTorsion
<pfh.glidersim.foil_layout.PolynomialTorsion>` in ``glidersim`` for an
implementation.


Area and Volume of a Mesh
=========================

The paraglider dynamics require the inertial properties of the canopy surface
areas and volume. These include the magnitudes (total mass or volume),
centroids, and inertia tensors. All of these quantities can be computed using
a triangular surface mesh over the canopy surfaces.

What follows is a reproduction of the procedure developed in
:cite:`blow2004HowFindInertia`, which is a functionally equivalent to the
procedure from :cite:`zhang2001EfficientFeatureExtraction` but with a more
intuitive interpretation and complete equations for the inertia tensors.


Area
----

To compute the mass distribution of the upper and lower surfaces, start by
computing the dimensionless inertia tensor of the areas then scale them by the
surface material areal densities. [[FIXME: what? Reword: we want the total
area, total area centroid, and dimensionless inertia matrices. We can scale
those by the upper and lower surface densities to get the actual values.]]

First, for each of the upper and lower surfaces, cover the surface with
a triangulated mesh so it is represented by a set of :math:`N` triangles. Each
triangle is defined by three points :math:`\left\{ \mathrm{P1}, \mathrm{P2},
\mathrm{P3} \right\}_n` in canopy coordinates. For convenience, define position
vectors for each of the three points of the nth triangle: :math:`\vec{r}_{i,n}
\defas \vec{r}_{Pi/O,n}`.

The area of each triangle is easily computed using the vector cross-product of
two legs of the triangle:

.. math::

   a_n =
      \frac{1}{2}
      \rho
      \norm{
        \left( \vec{r}_{2,n} - \vec{r}_{1,n} \right)
        \times
        \left( \vec{r}_{3,n} - \vec{r}_{2,n} \right)
      }

The total area of the surface is the sum of the triangle areas:

.. I wasn't crazy about the notation `a = sum(a_n)`, but it is clean  and it
   matches Hughes (eg, see Eq:9 on page 44 (53), where `p = sum(p_n)`)

.. math::

   a = \sum^N_{n=1} a_n

The area centroid of each triangle:

.. math::

   \overline{\vec{a}}_n \defas
     \frac{1}{3} \left( \vec{r}_{1,n} + \vec{r}_{2,n} + \vec{r}_{3,n} \right)

And the centroid :math:`\mathrm{A}` of the total surface area with respect to
the canopy origin :math:`\mathrm{O}`:

.. math::

   \vec{r}_{\mathrm{A}/\mathrm{O}} = \frac{1}{a} \sum^N_{n=1} a_n \overline{\vec{a}}_n

The covariance matrix of the total surface area:

.. math::

   \mat{\Sigma}_a = \sum^N_{n=1} a_n \overline{\vec{a}}_n \overline{\vec{a}}_n^T

The inertia tensor of the total surface area :math:`a` about the canopy origin
:math:`\mathrm{O}`:

.. math::

   \mat{J}_{a/\mathrm{O}} = \mathrm{trace} \left( \mat{\Sigma}_a \right) \vec{I}_3 - \mat{\Sigma}_a

And tada, we've computed the three relevant properties for each surface area:
the total area :math:`a`, the area centroid
:math:`\vec{r}_{\mathrm{A}/\mathrm{O}}`, and the inertia tensor
:math:`\mat{J}_{a/\mathrm{O}}`.


Volume
------

Now for the volume. For the purposes of computing the inertia properties of the
enclosed air, it is convenient to neglect the air intakes and treat the canopy
as a closed volume. Given this simplifying assumption, build another triangular
mesh that covers the entire canopy surface as well as the left and right wing
tip sections. For this derivation, it is essential that the points on each
triangle are ordered such that a right-handed traversal produces a normal
vector pointing out of the volume. It is also essential that the complete mesh
does not contain any holes, or the volume may be miscounted. Given a surface
triangulation over the closed canopy geometry using :math:`N` triangles, the
volume can be computed as follows.

First, treat each triangle as the face of a tetrahedron that includes the
origin. The signed volume of the tetrahedron formed by each triangle is given
by:

.. math::

   v_n =
      \frac{1}{6}
      \left(
         \vec{r}_{1,n} \times \vec{r}_{2,n}
      \right)
      \cdot \vec{r}_{3,n}

Given that the vertices of each triangle were oriented such that they satisfy
a right-hand rule, the sign of each volume will be positive if the normal
vector for each triangular face points away from the origin, and negative if
it points towards the origin. In essence the tetrahedrons "overcount" the
volume for triangles pointing away from the origin, then the triangles facing
the origin subtract away the excess volume. The final volume of the canopy is
the simple sum:

.. math::

   v = \sum^N_{n=1} v_n

For the volume centroid of each tetrahedron:

.. Divide by 4 since this implicitly includes the origin at <0,0,0>

.. math::

   \overline{\vec{v}}_n \defas \frac{1}{4} \sum^3_{i=1} \vec{r}_{i,n}

And the centroid :math:`\mathrm{V}` of the total volume with respect to the
canopy origin :math:`\mathrm{O}`:

.. math::

   \vec{r}_{\mathrm{V}/\mathrm{O}} = \frac{1}{v} \sum^N_{n=1} v_n \overline{\vec{v}}_n

Lastly, calculating the inertia tensor of the volume can be simplified by
computing the inertia tensor of a prototypical or "canonical" tetrahedron and
applying an affine transformation to produce the inertia tensor of each
individual volume.

First, given the covariance matrix of the "canonical" tetrahedron:

.. math::

   \mat{\hat{\Sigma}} \defas \begin{bmatrix}
      \frac{1}{60} & \frac{1}{120} & \frac{1}{120}\\
      \frac{1}{120} & \frac{1}{60} & \frac{1}{120}\\
      \frac{1}{120} & \frac{1}{120} & \frac{1}{60}
   \end{bmatrix}


Use the points in each triangle to define:

.. math::

   \mat{T}_n \defas
      \begin{bmatrix}
         | & | & | \\
         \vec{r}_{1,n} & \vec{r}_{2,n} & \vec{r}_{3,n}\\
         | & | & | \\
      \end{bmatrix}

The covariance of each tetrahedron volume is then:

.. math::

   \mat{\Sigma}_n = \left| \mat{T}_n \right| \mat{T}_n^T \mat{\hat{\Sigma}} \mat{T}_n

And the covariance matrix of the complete volume:

.. math::

   \mat{\Sigma}_v = \sum^N_{n=1} \mat{\Sigma}_n

And at last, the inertia tensor of the volume about the origin :math:`O` can
be computed directly from the covariance matrix:

.. math::

   \mat{J}_{v/O} = \mathrm{trace} \left( \mat{\Sigma}_v \right) \vec{I}_3 - \mat{\Sigma}_v

.. FIXME: make a table showing the six variables and their names. Well, nine
   variables? There are upper and lower surfaces.


Apparent mass of a parafoil
===========================

This section presents Barrows' method :cite:`barrows2002ApparentMassParafoils`
for estimating the apparent mass matrix of a wing with circular arc anhedral.
(For a discussion of apparent mass effects, see
:ref:`paraglider_components:Apparent Mass`.) The equations have been adapted
to use the standard notation of this paper.

The purpose of the equations is estimate several terms that allow the
paraglider system dynamics model to calculate the apparent inertia matrix with
respect to the dynamics reference point, so the apparent mass can be taken
into account when calculating the canopy acceleration. The necessary terms
are:

* :math:`\mat{A}_{a/R}`: apparent inertia matrix with respect to some
  *reference point* :math:`R`. This matrix is comprised of a translational
  inertia part :math:`\mat{M}_a` and a rotational inertia part
  :math:`\mat{J}_{a/R}`.

* :math:`\vec{r}_{RC/R}`: roll center with respect to :math:`R`

* :math:`\vec{r}_{PC/RC}`: pitch center with respect to the *roll center*
  :math:`RC`

Some notes about Barrows' development:

* It assumes the foil is symmetric about the :math:`xz`-plane (left-right
  symmetry) and about the :math:`yz`-plane (fore-aft symmetry).

* It requires that the dynamics reference point :math:`R` lies in the
  :math:`xz`-plane

* It assumes the canopy arc is circular.

* It assumes a constant chord length over the entire span.

* It assumes constant thickness over the entire span.

* It assumes no chordwise camber.

* It assumes the chords are all parallel to the x-axis (which also means no
  geometric twist). This mostly isn't a problem since our coordinate system is
  defined by the central chord, the geometric torsion angles tend to be quite
  small, and twist tends to occur over segments which represent negligible
  volume compared to the bulk of the wing.

.. figure:: figures/paraglider/dynamics/barrows.*
   :name: barrows_diagram

   Geometry for Barrow's apparent mass equations.

Some initial definitions:

.. math::

   \begin{aligned}
     t   &= \text{Airfoil thickness.} \\
     h^* &= \frac{h}{b} \\
   \end{aligned}

First, the apparent mass terms for a flat wing of a similar volume, from
Barrows' equations 34-39:

.. math::

   \begin{aligned}
     m_{f11} &= k_A \pi \left( t^2 b / 4 \right) \\
     m_{f22} &= k_B \pi \left( t^2 c / 4 \right) \\
     m_{f33} &= \left[ \mathrm{AR} / \left( 1 + \mathrm{AR} \right) \right] \pi \left( c^2 b / 4 \right) \\
     \\
     I_{f11} &= 0.055 \left[ \mathrm{AR} / \left( 1 + \mathrm{AR} \right) \right] b S^2 \\
     I_{f22} &= 0.0308 \left[ \mathrm{AR} / \left( 1 + \mathrm{AR} \right) \right] c^3 S \\
     I_{f33} &= 0.055 b^3 t^2
   \end{aligned}

Where :math:`k_A` and :math:`k_B` are the "correction factors for
three-dimensional effects":

.. math::

   \begin{aligned}
     k_A &= 0.85 \\
     k_B &= 1.0
   \end{aligned}

Assuming the parafoil arc is circular and with no chordwise camber, use Barrows
equations 44 and 50 to compute the *pitch center* :math:`PC` and *roll center*
:math:`RC` as points directly above the *confluence point* :math:`C` of the
arc:

.. math::

   \begin{aligned}
     z_{PC/C}  &= -\frac{r \sin \left( \Theta \right)}{\Theta} \\
     z_{RC/C}  &= -\frac{z_{PC/C} \; m_{f22}}{m_{f22} + I_{f11}/r^2} \\
     z_{PC/RC} &= z_{PC/C} - z_{RC/C}
   \end{aligned}

Modifying the apparent mass terms from the flat wing to approximate the terms
for the arched wing, Barrows equations 51-55:

.. math::

   \begin{aligned}
     m_{11} &= k_A \left[ 1 + \left(\frac{8}{3}\right){h^*}^2 \right] \pi \left( t^2 b / 4 \right) \\
     m_{22} &= \frac{r^2 m_{f22} + I_{f11}}{z^2_{PC/C}} \\
     m_{33} &= m_{f33} \\
     \\
     I_{11} &= \frac{z^2_{PC/RC}}{z^2_{PC/C}} r^2 m_{f22} + \frac{z^2_{RC/C}}{z^2_{PC/C}} I_{f11} \\
     I_{22} &= I_{f22} \\
     I_{33} &= 0.055 \left( 1 + 8 {h^*}^2 \right) b^3 t^2
   \end{aligned}

The apparent mass and apparent moment of inertia matrices are then defined in
Barrows equations 1 and 17:

.. math::
   :label: apparent_mass_matrix

   \mat{M}_a \defas
     \begin{bmatrix}
       m_{11} & 0      & 0 \\
       0      & m_{22} & 0 \\
       0      & 0      & m_{33}
     \end{bmatrix}

.. math::
   :label: apparent_moment_of_inertia_matrix

   \mat{I}_a \defas
     \begin{bmatrix}
       I_{11} & 0      & 0 \\
       0      & I_{22} & 0 \\
       0      & 0      & I_{33}
     \end{bmatrix}

Define two helper matrices:

.. math::

   \mat{S}_2 \defas
     \begin{bmatrix}
       0 & 0 & 0 \\
       0 & 1 & 0 \\
       0 & 0 & 0
     \end{bmatrix}

.. math::

   \mat{Q} = \mat{S}_2 \crossmat{\vec{r}_{PC/RC}} \mat{M}_a \crossmat{\vec{r}_{RC/R}}

Where :math:`\crossmat{\vec{x}}` is the :ref:`cross-product matrix operator
<crossmat>`.

Using the helper matrices, use Barrows equation 25 to write the rotational
part of the apparent inertia matrix:

.. math::

   \mat{J}_{a/R} \defas
      \mat{I}
      - \crossmat{\vec{r}_{RC/R}} \mat{M}_a \crossmat{\vec{r}_{RC/R}}
      - \crossmat{\vec{r}_{PC/RC}} \mat{M}_a \crossmat{\vec{r}_{PC/RC}} \mat{S}_2
      - \mat{Q}
      - \mat{Q}^T

And the corresponding angular momentum of the apparent mass about :math:`R`,
using Barrows equation 24:

.. math::

   \vec{h}_{a/R} =
      \left(
         \mat{S}_2 \crossmat{\vec{r}_{PC/RC}} + \crossmat{\vec{r}_{RC/R}}
      \right) \mat{M}_a \vec{v}_{R/e} + \mat{J}_{a/R} \omega

And finally, the completed apparent inertia matrix with respect to the
reference point :math:`R`, from Barrows equation 27:

.. math::
   :label: apparent_inertia_matrix

   \mat{A}_{a/R} =
     \begin{bmatrix}
       \mat{M}_a & -\mat{M}_a \left( \crossmat{\vec{r}_{RC/R}} + \crossmat{\vec{r}_{PC/RC}} \mat{S}_2 \right) \\
       \left( \mat{S}_2 \crossmat{\vec{r}_{PC/RC}} + \crossmat{\vec{r}_{RC/R}} \right) \mat{M}_a & \mat{J}_{a/R}
   \end{bmatrix}

Plus the vectors necessary to incorporate :math:`\mat{J}_{a/R}` into the
final dynamics:

.. math::

   \vec{r}_{PC/RC} = \begin{bmatrix} 0 & 0 & z_{PC/RC}\end{bmatrix}

Linear momentum of the apparent mass:

.. math::
   :label: apparent_linear_momentum

   \vec{p}_{a/e} =
     \mat{M}_a \cdot \left(
       \vec{v}_{R/e}
       - \crossmat{\vec{r}_{RC/R}} \omega_{b/e}
       - \crossmat{\vec{r}_{PC/RC}} \mat{S}_2 \cdot \omega_{b/e}
     \right)

Angular momentum of the apparent mass about :math:`R`:

.. math::
   :label: apparent_angular_momentum

   \vec{h}_{a/R} =
     \left(
       \mat{S}_2 \cdot \crossmat{\vec{r}_{PC/RC}} + \crossmat{\vec{r}_{RC/R}}
     \right) \cdot \mat{M}_a \cdot \vec{v}_{R/e}
     + \mat{J}_{a/R} \cdot \omega_{b/e}

Refer to :external+glidersim:py:class:`ParagliderWing
<pfh.glidersim.paraglider_wing.ParagliderWing>` in ``glidersim`` for an
implementation.

.. Notes to self

   * If :ref:`paraglider_systems:Reference point` said this section gives
     reasons that `R` should be in the xz-plane, then make sure this section
     covers that.

   * Doesn't Barrows use the *principal axes*? See my comment at the end of
     the "Introduction" to Barrows' paper about the coordinate axes needing to
     be parallel to the principal axes. I think the fact that I'm assuming the
     wing has fore-aft and later symmetry is what allows me to use the canopy
     axes.

   * I'm not crazy about the notation `\mat{A}_{a/R}`, but this matrix isn't
     like anything else in my paper so for now I'll leave it.


Paraglider system models
========================

[[**FIXME**: preview the models. Model `6a` is the most complete, and accounts
for apparent mass. Models `6b` and `6c` are simpler but require computing the
body center of mass :math:`r_{B/RM}` before computing :math:`A_{a/B}` (plus
:math:`B` is not strictly a fixed point since air density changes); they are
mostly useful for verifying the implementations.]]


Model 6a
--------

This section describe a paraglider dynamics model with 6 degrees of freedom.
It uses a rigid-body assumption, and incorporates the effects of apparent
mass. The dynamics are computed with respect to the riser midpoint :math:`RM`
instead of the wing center of mass :math:`B` because it avoids needing to
recompute the apparent inertia matrix whenever `B` changes. In this derivation
all vectors are in the canopy coordinate system :math:`c`, so the vector
coordinate systems are implicit in the notation.

The derivation develops the equations of motion by starting with derivatives
of linear and angular momentum. The derivation is largely based on the
excellent :cite:`hughes2004SpacecraftAttitudeDynamics`, although this section
uses this paper's version of Stevens' notation (see :ref:`notation:Notation and
Symbols`).

An implementation of this model is available as
:external+glidersim:py:class:`Paraglider6a
<pfh.glidersim.paraglider.ParagliderSystemDynamics6a>` in the ``glidersim``
package. The ``glidersim`` package also includes
:external+glidersim:py:class:`Paraglider6b
<pfh.glidersim.paraglider.ParagliderSystemDynamics6b>` and
:external+glidersim:py:class:`Paraglider6c
<pfh.glidersim.paraglider.ParagliderSystemDynamics6c>`, which decouple the
translational and angular equations of motion by choosing the glider center of
gravity for the dynamics reference point, but do not incorporate the apparent
mass matrix.


Real mass only
^^^^^^^^^^^^^^

Start with the equations for the translational and angular momentum of the
body :math:`b` about the reference point :math:`RM` as observed by the
inertial reference frame :math:`e`:

.. math::
   :label: model6a_p

   \begin{aligned}
     {\vec{p}_{b/e}}
       &= m_b \, \vec{v}_{B/e} \\
       &= m_b \left(
            {\vec{v}_{RM/e}} + {\vec{\omega}_{b/e}} \times {\vec{r}_{B/RM}}
          \right)
   \end{aligned}

.. ref: Stevens Eq:1.7-3 (pg36)

.. math::
   :label: model6a_h

   \vec{h}_{b/RM} =
     m_b \, \vec{r}_{B/RM} \times \vec{v}_{RM/e}
     + \mat{J}_{b/RM} \cdot \vec{\omega}_{b/e}

Compute the momentum derivatives in the inertial frame :math:`\mathcal{F}_e`
in terms of derivatives in the body frame :math:`\mathcal{F}_b`:

.. math::
   :label: model6a_momentum_derivatives1

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}}
       &= {^b \dot{\vec{p}}_{b/e}}
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e}

       &= m_b \left(
            {^b \dot{\vec{v}}_{RM/e}}
            + {^b\dot{\vec{\omega}}_{b/e}} \times {\vec{r}_{B/RM}}
            + {\vec{\omega}}_{b/e} \times {\cancelto{0}{^b \dot{\vec{r}_{B/RM}}}}
          \right)
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e}

       &= m_b \left(
            {^b \dot{\vec{v}}_{RM/e}}
            + {^b\dot{\vec{\omega}}_{b/e}} \times {\vec{r}_{B/RM}}
          \right)
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e}

     \\

     {^e \dot{\vec{h}}_{b/RM}}
       &= {^b\dot{\vec{h}}_{b/RM}} + {\vec{\omega}_{b/e} \times \vec{h}_{b/RM}}

       &= m_b \left(
            {\cancelto{0}{^b \dot{\vec{r}_{B/RM}}}} \times \vec{v}_{RM/e}
            + \vec{r}_{B/RM} \times {^b \dot{\vec{v}_{RM/e}}}
          \right)
          + {\mat{J}_{b/RM} \cdot {^b \dot{\vec{\omega}}_{b/e}}}
          + {\vec{\omega}_{b/e} \times \vec{h}_{b/RM}}

       &= m_b \, \vec{r}_{B/RM} \times {^b \dot{\vec{v}_{RM/e}}}
          + {\mat{J}_{b/RM} \cdot {^b \dot{\vec{\omega}}_{b/e}}}
          + {\vec{\omega}_{b/e} \times \vec{h}_{b/RM}}

   \end{aligned}

Relate the derivatives of momentum with respect to the inertial frame to the
net force on the body :math:`\vec{f}_b` and the net moment on the body about
the reference point :math:`\vec{g}_{b/RM}`:

.. For angular momentum, see Stevens Eq:1.7-1 (pg35)

.. math::
   :label: model6a_momentum_derivatives2

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}} &=
       \mat{f}_b \\
     {^e \dot{\vec{h}}_{b/RM}} + \vec{v}_{RM/e} \times \vec{p}_{b/e} &=
       \mat{g}_{b/RM}
   \end{aligned}

Where

.. math::

   \begin{aligned}
     \vec{f}_b &=
       {\vec{f}_{b,\textrm{aero}}}
       + {\vec{f}_{b,\textrm{weight}}} \\
     \vec{g}_{b/RM} &=
       {\vec{g}_{b,\textrm{aero}}}
       + {\vec{r}_{B/RM} \times {\vec{f}_{b,\textrm{weight}}}}
   \end{aligned}

Combining :eq:`model6a_momentum_derivatives1` and
:eq:`model6a_momentum_derivatives2` gives the final equations for the dynamics
of the real mass (solid mass plus the enclosed air) in terms of :math:`^b
\dot{\vec{v}}_{RM/e}` and :math:`^b \dot{\vec{\omega}}_{b/e}`.

.. math::
   :label: model6a_dynamics_equations

   \begin{aligned}
      m_b \, {^b \dot{\vec{v}}_{RM/e}}
      + m_b \, {^b \dot{\vec{\omega}}_{b/e}} \times \vec{r}_{B/RM}
      &= \vec{f}_b
         - \vec{\omega}_{b/e} \times \vec{p}_{b/e}

      m_b \, \vec{r}_{B/RM} \times {^b \dot{\vec{v}}_{RM/e}}
      + \mat{J}_{b/RM} \cdot {^b \dot{\vec{\omega}}_{b/e}}
      &= \vec{g}_{b/RM} - \vec{\omega}_{b/e} \times \vec{h}_{b/RM}
         - \vec{v}_{RM/e} \times \vec{p}_{b/e}
   \end{aligned}

Rewriting the equations as a linear system:

.. math::
   :label: model6a_real_system

   \mat{A}_{r/RM}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{RM/e}} \\
     {^b \dot{\vec{\omega}}_{b/e}} \\
   \end{bmatrix}
   = \begin{bmatrix}
       \vec{b}_1\\
       \vec{b}_2\\
     \end{bmatrix}

Where:

.. math::

   \begin{aligned}
     \mat{A}_{r/RM} &=
       \begin{bmatrix}
         {m_b \, \mat{I}_3} & {-m_b \crossmat{\vec{r}_{B/RM}}} \\
         {m_b \, \crossmat{\vec{r}_{B/RM}}} & {\mat{J}_{b/RM}} \\
       \end{bmatrix} \\
     \\
     \vec{b}_1 &=
       \vec{f}_b - \vec{\omega}_{b/e} \times \vec{p}_{b/e} \\
     \vec{b}_2 &=
       \vec{g}_{b/RM}
       - \vec{\omega}_{b/e} \times \vec{h}_{b/RM}
       - \vec{v}_{RM/e} \times \vec{p}_{b/e} \\
   \end{aligned}


Real mass + apparent mass
^^^^^^^^^^^^^^^^^^^^^^^^^

Writing the dynamics in matrix form not only makes it straightforward to solve
for the state derivatives, it also makes it easy to incorporate the apparent
inertia matrix from `Apparent mass of a parafoil`_. Adding the apparent
inertia into the system matrix and accounting for the translational and
angular apparent momentum produces:

.. math::
   :label: model6a_complete_system

   \begin{bmatrix}
     \mat{A}_{r/RM} + \mat{A}_{a/RM}
   \end{bmatrix}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{RM/e}} \\
     {^b \dot{\vec{\omega}}_{b/e}} \\
   \end{bmatrix}
   = \begin{bmatrix}
       \begin{aligned}
          \vec{b}_3 \\
          \vec{b}_4
      \end{aligned}
     \end{bmatrix}

.. math::

   \begin{aligned}
     \vec{b}_3 &= \vec{b}_1 - \vec{\omega}_{b/e} \times \vec{p}_{a/e} \\
     \vec{b}_4 &=
       \vec{b}_2
       - {\vec{v}_{RM/e} \times \vec{p}_{a/e}}
       - {\vec{\omega}_{b/e} \times \vec{h}_{a/RM}}
       + {\vec{v}_{RM/e} \times \left( \mat{M}_a \cdot \vec{v}_{RM/e} \right) }
   \end{aligned}

Where :math:`\mat{A}_{a/RM}` is the apparent inertia matrix of the canopy from
:eq:`apparent_inertia_matrix`, :math:`\mat{M}_a` is the apparent mass matrix
from :eq:`apparent_mass_matrix`, and :math:`\vec{p}_{a/e}` and
:math:`\vec{h}_{a/RM}` are the linear and angular apparent momentums from
:eq:`apparent_linear_momentum` and :eq:`apparent_angular_momentum`. The extra
term :math:`\vec{v}_{RM/e} \times \left( \mat{M}_a \vec{v}_{RM/e} \right)` in
:math:`\vec{b}_4` is necessary to avoid double counting the aerodynamic moment
already accounted for by the section pitching coefficients.


Model 6b
--------

Following the same logic as `Model 6a`_, but targeting :math:`^b
\vec{v}_{B/e}` and using the momentum about the body center of mass :math:`B`
produces a simpler model with a diagonal system matrix, but at the cost of
requiring the body center of mass to be determined before computing the
apparent inertia matrix with respect to that point. For that reason the
apparent mass is neglected here, although if :math:`B` lies in the xz-plane
then the method described in `Apparent mass of a parafoil`_ could be used.

The main purpose of this model is for validating model implementations. An
implementation of this model is available as
:external+glidersim:py:class:`Paraglider6b
<pfh.glidersim.paraglider.ParagliderSystemDynamics6b>` in the ``glidersim``
package.

.. math::
   :label: model6b_p

   \vec{p}_{b/e} = m_b \, \vec{v}_{B/e}

.. math::
   :label: model6b_h

   \vec{h}_{b/B} = \mat{J}_{b/B} \cdot \vec{\omega}_{b/e}

Computing the inertial derivatives with respect to the body frame:

.. math::
   :label: model6b_momentum_derivatives1

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}}
       &= m_b \, {^b \dot{\vec{v}}_{B/e}}
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e} \\
     \\
     {^e \dot{\vec{h}}_{b/B}}
       &= \mat{J}_{b/B} \cdot {^b \dot{\vec{\omega}}_{b/e}}
          + \vec{\omega}_{b/e} \times \vec{h}_{b/B}
   \end{aligned}

Using the body center of mass as the reference point simplifies the equation
for angular momentum:

.. math::
   :label: model6b_momentum_derivatives2

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}} &= \mat{f}_b \\
     {^e \dot{\vec{h}}_{b/B}} &= \mat{g}_{b/B}
   \end{aligned}

Combining :eq:`model6b_momentum_derivatives1` and
:eq:`model6b_momentum_derivatives2`: and rewriting as a linear system:

.. math::
   :label: model6b_real_system

   \begin{bmatrix}
     m_b & 0 \\
     0 & \mat{J}_{b/B}
   \end{bmatrix}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{B/e}} \\
     {^b \dot{\vec{\omega}}_{b/e}}
   \end{bmatrix}
   = \begin{bmatrix}
       \vec{f}_b - \vec{\omega}_{b/e} \times \vec{p}_{b/e} \\
       \vec{g}_{b/B} - \vec{\omega}_{b/e} \times \vec{h}_{b/B}
     \end{bmatrix}


Model 6c
--------

Another option is to target :math:`^b \dot{\vec{v}}_{RM/e}` directly, but again
using the momentum about the body center of mass :math:`B`. Like `Model 6b`_
this also produces a simpler dynamics model, but again at the cost of making it
less convenient to precompute the apparent inertia matrix.

The main purpose of this model is for validating model implementations. An
implementation of this model is available as
:external+glidersim:py:class:`Paraglider6c
<pfh.glidersim.paraglider.ParagliderSystemDynamics6c>` in the ``glidersim``
package.

Computing the inertial derivatives with respect to the body frame:

.. math::
   :label: model6c_momentum_derivatives1

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}}
       &= m_b \left(
            {^b \dot{\vec{v}}_{RM/e}}
            + {^b \dot{\vec{\omega}}_{b/e}} \times \vec{r}_{B/RM}
          \right)
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e}
     \\
     {^e \dot{\vec{h}}_{b/B}}
       &= \mat{J}_{b/B} \cdot {^b \dot{\vec{\omega}}_{b/e}}
          + \vec{\omega}_{b/e} \times \vec{h}_{b/B}
   \end{aligned}

Using the body center of mass as the reference point simplifies the equation
for angular momentum:

.. math::
   :label: model6c_momentum_derivatives2

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}} &= \mat{f}_b \\
     {^e \dot{\vec{h}}_{b/B}} &= \mat{g}_{b/B}
   \end{aligned}

Combining :eq:`model6c_momentum_derivatives1` and
:eq:`model6c_momentum_derivatives2`: and rewriting as a linear system:

.. math::
   :label: model6c_real_system

   \begin{bmatrix}
     m_b & -m_b \crossmat{\vec{r}_{B/RM}} \\
     0 & \mat{J}_{b/B}
   \end{bmatrix}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{RM/e}} \\
     {^b \dot{\vec{\omega}}_{b/e}}
   \end{bmatrix}
   = \begin{bmatrix}
       \vec{f}_b - \vec{\omega}_{b/e} \times \vec{p}_{b/e} \\
       \vec{g}_{b/B} - \vec{\omega}_{b/e} \times \vec{h}_{b/B}
     \end{bmatrix}


Model 9a
--------

Similar to `Model 6a`_, this design uses the riser connection midpoint `RM` as
the reference point for both the body and the payload, which simplifies
incorporating the apparent mass matrix. However, this model treats the body
and payload as separate components, connected by a rotational spring-damper
model that adds an additional three degrees-of-freedom. A similar 9DoF model
derivation can be found in :cite:`gorman2012EvaluationMultibodyParafoil`
(9DoF, but relative roll and pitch are unconstrained).

.. Why didn't I use that derivation? Like most papers, it used used implicit
   vector notation and skips significant steps of the derivation, making
   validation difficult. Also, it merged the individual components of the
   apparent matrices from Lissaman and Brown's method for computing apparent
   mass :cite:`lissaman1993ApparentMassEffects`. This derivation uses explicit
   vector notation to avoid mistakes (particularly when taking derivatives)
   and significantly simplifies the inclusion of the apparent inertia matrix
   from Barrow's method :cite:`barrows2002ApparentMassParafoils`.

An implementation of this model is available as
:external+glidersim:py:class:`Paraglider9a
<pfh.glidersim.paraglider.ParagliderSystemDynamics9a>` in the ``glidersim``
package. The ``glidersim`` package also includes
:external+glidersim:py:class:`Paraglider9b
<pfh.glidersim.paraglider.ParagliderSystemDynamics9b>`, which uses the centers
of mass as the reference points for the body and payload dynamics; that choice
simplifies the derivatives for angular momentum (because it eliminates the
moment arms), but prohibits incorporating the effects of apparent mass.


Real mass only
^^^^^^^^^^^^^^

Start with the equations for the translational and angular momentum of the
body :math:`b` about the reference point :math:`RM` as observed by the inertial
reference frame :math:`e`:

.. math::
   :label: model9a_body_p

   \begin{aligned}
     {\vec{p}_{b/e}}
       &= m_b \, \vec{v}_{B/e} \\
       &= m_b \left(
            {\vec{v}_{RM/e}} + {\vec{\omega}_{b/e}} \times {\vec{r}_{B/RM}}
          \right)
   \end{aligned}

.. math::
   :label: model9a_payload_p

   \begin{aligned}
     {\vec{p}_{p/e}}
       &= m_p \, \vec{v}_{P/e} \\
       &= m_p \left(
            {\vec{v}_{RM/e}} + {\vec{\omega}_{b/e}} \times {\vec{r}_{P/RM}}
          \right)
   \end{aligned}

.. math::
   :label: model9a_body_h

   \vec{h}_{b/RM} =
     m_b \, \vec{r}_{B/RM} \times \vec{v}_{RM/e}
     + \mat{J}_{b/RM} \cdot \vec{\omega}_{b/e}

.. math::
   :label: model9a_payload_h

   \vec{h}_{p/RM} =
     m_p \, \vec{r}_{P/RM} \times \vec{v}_{RM/e}
     + \mat{J}_{p/RM} \cdot \vec{\omega}_{p/e}

Compute the two momentum derivatives:

.. math::
   :label: model9a_momentum_derivatives1

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}}
       &= {^b \dot{\vec{p}}_{b/e}} + \vec{\omega}_{b/e} \times \vec{p}_{b/e}

       &= m_b \left(
            {^b \dot{\vec{v}}_{RM/e}}
            + {^b \dot{\vec{\omega}}_{b/e}} \times {\vec{r}_{B/RM}}
          \right)
            + \vec{\omega}_{b/e} \times \vec{p}_{b/e}

     {^e \dot{\vec{h}}_{b/RM}}
       &= {^b \dot{\vec{h}}_{b/RM}} + {\vec{\omega}_{b/e} \times \vec{h}_{b/RM}}

       &= m_b \vec{r}_{B/RM} \times {^b \vec{\dot{v}}_{RM/e}}
          + {\mat{J}_{b/RM} \cdot {^b \dot{\vec{\omega}}_{b/e}}}
          + {\vec{\omega}_{b/e} \times \vec{h}_{b/RM}}

     {^e \dot{\vec{p}}_{p/e}}
       &= {^p \dot{\vec{p}}_{p/e}} + \vec{\omega}_{p/e} \times \vec{p}_{p/e}

       &= m_p \left(
            {^p \dot{\vec{v}}_{RM/e}}
            + {^p \dot{\vec{\omega}}_{p/e}} \times {\vec{r}_{P/RM}}
          \right)
            + \vec{\omega}_{p/e} \times \vec{p}_{p/e}

       &= m_p \left(
            {^b \dot{\vec{v}}_{RM/e}}
            + \vec{\omega}_{b/p} \times \vec{v}_{RM/e}
            + {^p \dot{\vec{\omega}}_{p/e}} \times {\vec{r}_{P/RM}}
          \right)
            + \vec{\omega}_{p/e} \times \vec{p}_{p/e}

     {^e \dot{\vec{h}}_{p/RM}}
       &= {^p \dot{\vec{h}}_{p/RM}} + {\vec{\omega}_{p/e} \times \vec{h}_{p/RM}}

       &= m_p \vec{r}_{P/RM}
            \times {^p \dot{\vec{v}_{RM/e}}}
            + \mat{J}_{p/RM} \cdot {^p \dot{\vec{\omega}}}_{p/e}
            + \vec{\omega}_{p/e} \times \vec{h}_{p/RM}

       &= m_p \vec{r}_{P/RM}
            \times \left( {^b \dot{\vec{v}_{RM/e}}} + \vec{\omega}_{b/p} \times \vec{v}_{RM/e} \right)
            + \mat{J}_{p/RM} \cdot {^p \dot{\vec{\omega}}}_{p/e}
            + \vec{\omega}_{p/e} \times \vec{h}_{p/RM}

   \end{aligned}

Derivatives of the payload momentums are computed in terms of the body
velocity derivative in the body frame to allow writing the dynamics as
a single system of equations. First, compute the net external forces and
moments:

.. For angular momentum, see Stevens Eq:1.7-1 (pg35)

.. math::
   :label: model9a_net_forces

   \begin{aligned}
     \vec{f}_b &= \vec{f}_{b,\textrm{aero}} + \vec{f}_{b,\textrm{weight}} \\
     \vec{g}_{b/RM} &= \vec{g}_{b,\textrm{aero}} + \vec{g}_{b,\textrm{weight}} \\
     \vec{f}_p &= \vec{f}_{p,\textrm{aero}} + \vec{f}_{p,\textrm{weight}} \\
     \vec{g}_{p/RM} &= \vec{g}_{p,\textrm{aero}} + \vec{g}_{p,\textrm{weight}}  \\
   \end{aligned}

And equate them to the derivatives of momentum with respect to the inertial
frame:

.. math::
   :label: model9a_momentum_derivatives2

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}} &=
       \vec{f}_b - \vec{f}_{RM} \\
     {^e \dot{\vec{h}}_{b/RM}} + \vec{v}_{RM/e} \times \vec{p}_{b/e} &=
       \vec{g}_{b/RM} - \vec{g}_{RM} \\
     {^e \dot{\vec{p}}_{p/e}} &=
       \vec{f}_p + \vec{f}_{RM} \\
     {^e \dot{\vec{h}}_{p/RM}} + \vec{v}_{RM/e} \times \vec{p}_{p/e} &=
       \vec{g}_{p/RM} + \vec{g}_{RM} \\
   \end{aligned}

[[**FIXME**: ambiguous notation? I'm interested in communicating "the moment
about `RM` due to the spring" and "the moment about `RM` due to the aerodynamic
forces", etc]]

[[**FIXME**: define `g_{b,aero}` etc? Has contributions from both aerodynamic
moments as well as forces applied on some lever arm to `RM`.]]

[[**FIXME**: need to describe `f_{RM}` and `g_{RM}`

The spring-damper connection produces forces and moments shared by the body
and the payload. There are six variables but only three degrees of freedom.
Both systems have the riser connection point :math:`RM` at a fixed position,
and the force only exists to maintain the fixed relative positioning.

.. math::
   :label: model9a_linear_spring_moment

   \vec{g}_{RM} =
     \begin{bmatrix}
       \begin{aligned}
         \kappa_{\phi} \phi &+ \kappa_{\dot{\phi}} \dot{\phi} \\
         \kappa_{\theta} \theta &+ \kappa_{\dot{\theta}} \dot{\theta} \\
         \kappa_{\gamma} \gamma &+ \kappa_{\dot{\gamma}} \dot{\gamma} \\
       \end{aligned}
     \end{bmatrix}

Where :math:`\vec{\omega}_{p/b}^p = \left< \phi, \theta, \gamma \right>` are
the angular rates of the payload, :math:`^p \dot{\vec{\omega}}_{p/b}^p
= \left< \dot{\phi}, \dot{\theta}, \dot{\gamma} \right>` are the angular
accelerations of the payload, and the :math:`\kappa` are the stiffness and
dampening coefficients of the spring-damper model.

This is a very simple model. A better model would need to account for the
coupling between dimensions, and should really be a function of the riser
strap width.]]

Combining equations :eq:`model9a_momentum_derivatives1` and
:eq:`model9a_momentum_derivatives2` and rewriting as a linear system provides
the dynamics of the real mass (solid mass plus the enclosed air) in terms of
:math:`^b \dot{\vec{v}}_{RM/e}`, :math:`^b \dot{\vec{\omega}}_{b/e}`, :math:`^b
\dot{\vec{\omega}}_{p/e}^p`, and :math:`\vec{f}_{RM}^b`:

.. math::
   :label: model9a_real_system

   \mat{A}_{r/RM}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{RM/e}^b} \\
     {^b \dot{\vec{\omega}}_{b/e}^b} \\
     {^p \dot{\vec{\omega}}_{p/e}^p} \\
     {   \vec{f}_{RM}^b}
   \end{bmatrix}
   = \begin{bmatrix}
       \vec{b}_1^b \\
       \vec{b}_2^b \\
       \vec{b}_3^p \\
       \vec{b}_4^p
     \end{bmatrix}

Where:

.. math::

   \mat{A}_{r/RM} =
     \begin{bmatrix}
       {m_b \, \mat{I}_3}
         & {-m_b \crossmat{\vec{r}_{B/RM}^b}}
         & {\mat{0}_{3\times3}}
         & {\mat{I}_3} \\
       {m_b \, \crossmat{\vec{r}_{B/RM}^b}}
         & {\mat{J}_{b/RM}^b}
         & {\mat{0}_{3\times3}}
         & {\mat{0}_{3\times3}} \\
       {m_p \, \mat{C}_{p/b}}
         & {\mat{0}_{3\times3}}
         & {-m_p \crossmat{\vec{r}_{P/RM}^p}}
         & {-\mat{C}_{p/b}} \\
       {m_p \, \crossmat{\vec{r}_{P/RM}^p} \mat{C}_{p/b}}
         & {\mat{0}_{3\times3}}
         & {\mat{J}_{p/RM}^p}
         & {\mat{0}_{3\times3}}
     \end{bmatrix}

.. math::
   :label: model9a_dynamics_RHS

   \begin{aligned}
      \vec{b}_1^b &=
        \vec{f}_b^b
        - \vec{\omega}_{b/e}^b \times \vec{p}_{b/e}^b \\
      \vec{b}_2^b &=
        \vec{g}_b^b
        - \vec{g}_{RM}^b
        - \vec{v}_{RM/e}^b \times \vec{p}_{b/e}^b
        - \vec{\omega}_{b/e}^b \times \vec{h}_{b/RM}^b \\
      \vec{b}_3^p &=
        \vec{f}_p^p
        - \vec{\omega}_{p/e}^p \times \vec{p}_{p/e}^p
        - m_p \vec{\omega}_{b/p}^p \times \vec{v}_{RM/e}^p \\
      \vec{b}_4^p &=
        \vec{g}_b^p
        + \vec{g}_{RM}^p
        - \vec{v}_{RM/e}^p \times \vec{p}_{p/e}^p
        - \vec{\omega}_{p/e}^p \times \vec{h}_{p/RM}^p
        - m_p \vec{r}_{P/RM}^p \times \left( \vec{\omega}_{b/p}^p \times \vec{v}_{RM/e}^p \right)
   \end{aligned}


Real mass + apparent mass
^^^^^^^^^^^^^^^^^^^^^^^^^

As with the 6-DoF system, the effects of apparent mass on the canopy can be
accounted for by adding the apparent inertia matrix from `Apparent mass of
a parafoil`_ to the components of the system matrix associated with the
translational and angular acceleration of the body and accounting for the
translational and angular apparent momentum:

.. math::
   :label: model9a_complete_system

   \left(
     \mat{A}_{r/RM}
     + \begin{bmatrix}
         \mat{A}_{a/RM} & \mat{0}_{6\times6} \\
         \mat{0}_{6\times6} & \mat{0}_{6\times6}
       \end{bmatrix}
   \right)
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{RM/e}^b} \\
     {^b \dot{\vec{\omega}}_{b/e}^b} \\
     {^p \dot{\vec{\omega}}_{p/e}^p} \\
     {   \vec{f}_{RM}^b}
   \end{bmatrix}
   = \begin{bmatrix}
       \vec{b}_5^b \\
       \vec{b}_6^b \\
       \vec{b}_3^p \\
       \vec{b}_4^p
     \end{bmatrix}

.. math::

   \begin{aligned}
     \vec{b}_5^b &= \vec{b}_1^b - \vec{\omega}_{b/e} \times \vec{p}_{a/e} \\
     \vec{b}_6^b &=
       \vec{b}_2^b
       - {\vec{v}_{RM/e} \times \vec{p}_{a/e}}
       - {\vec{\omega}_{b/e} \times \vec{h}_{a/RM}}
       + {\vec{v}_{RM/e} \times \left( \mat{M}_a \cdot \vec{v}_{RM/e} \right) }
   \end{aligned}

Where :math:`\mat{A}_{a/RM}` is the apparent inertia matrix of the canopy from
:eq:`apparent_inertia_matrix`, :math:`\mat{M}_a` is the apparent mass matrix
from :eq:`apparent_mass_matrix`, and :math:`\vec{p}_{a/e}` and
:math:`\vec{h}_{a/RM}` are the linear and angular apparent momentums from
:eq:`apparent_linear_momentum` and :eq:`apparent_angular_momentum`. The extra
term :math:`\vec{v}_{RM/e} \times \left( \mat{M}_a \vec{v}_{RM/e} \right)` in
:math:`\vec{b}_6^b` is necessary to avoid double counting the aerodynamic
moment already accounted for by the section pitching coefficients.
