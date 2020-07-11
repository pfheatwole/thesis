***********
Derivations
***********


Area and Volume of a Mesh
=========================

The paraglider dynamics requires the inertial properties of the canopy surface
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
surface material areal densities.

First, cover each surface in a triangulated mesh, so each surface is
represented by a set of :math:`N` triangles :math:`\left\{ t_n
\right\}^N_{n=1}`. Each triangle is defined by three points :math:`t_n
= \left\{ \vec{p_{n,1}}, \vec{p_{n,2}}, \vec{p_{n,3}} \right\}` in canopy
coordinates which have been ordered to produce a right-handed sequence
suitable for the surface. These triangles can be used to compute the surface
areas and enclosed volume of the canopy.

For surface areas, each triangular area is easily computed using the vector
cross-product of two legs of the triangle:

.. math::

   a_m =
      \frac{1}{2}
      \rho
      \left[
         \left( \vec{p_{m,2}} - \vec{p_{m,1}} \right)
         \times
         \left( \vec{p_{m,3}} - \vec{p_{m,2}} \right)
      \right]

The total area is the sum of the triangle areas:

.. math::

   A = \sum^M_{m=1} a_m

The centroid of each triangle:

.. math::

   \vec{c}_m = \frac{1}{3} \sum^3_{i=1} \vec{p_{m,i}}

The centroid of the net surface area:

.. math::

   \overline{\vec{A}} = \frac{1}{A} \sum^M_{m=1} a_m \vec{c}_m

The covariance matrix of the surface area:

.. math::

   \mat{C}_A = \sum^M_{m=1} a_m \vec{c}_m \vec{c}_m^T

The inertia tensor of the surface area about the origin :math:`O`:

.. math::

   \mat{J}_{A/O} = \mathrm{trace} \left( \mat{C}_A \right) \vec{I}_3 - \mat{C}_A

And tada, there are the three relevant properties for each surface area: the
total area :math:`A`, the centroid :math:`C`, and the inertia tensor
:math:`\mat{J}`.


Volume
------

Now for the volume. For the purposes of computing the inertia properties of
the enclosed air, it is convenient to neglect the air intakes and treat the
canopy as a closed volume. Given this simplifying assumption, build another
surface mesh that covers the total canopy surface as well as the left and
right wing tip sections. Given a surface triangulation over the closed canopy
geometry using :math:`N` triangles :math:`\left\{ t_n \right\}^N_{n=1}` as
before in the area calculations, the volume can be computed as follows:

.. TODO: should t_k be a matrix? That'd make sense when I compute its
   determinant.

First, treat each triangle as the face of a tetrahedron that includes the
origin. The signed volume of the tetrahedron formed by each triangle is given
by:

.. math::

   v_n =
      \frac{1}{6}
      \left(
         \vec{p_{n,1}} \cdot \vec{p_{n,2}}
      \right)
      \times \vec{p_{n,3}}

Given that the vertices of each triangle were oriented such that they satisfy
a right-hand rule, the sign of each volume will be positive if the normal
vector for each triangular face points away from the origin, and negative if
it points towards the origin. In essence the tetrahedrons "overcount" the
volume for triangles pointing away from the origin, then the triangles facing
the origin subtract away the excess volume. The final volume of the canopy is
the simple sum:

.. math::

   V = \sum^N_{n=1} v_n

For the volume centroid of each tetrahedron:

.. math::

   \overline{\vec{v}}_n = \frac{1}{4} \sum^3_{i=1} \vec{p_{n,i}}

And the centroid of the total volume:

.. math::

   \overline{\vec{V}} = \frac{1}{V} \sum^N_{n=1} \overline{\vec{v}}_n

Lastly, calculating the inertia tensor of the volume can be simplified by
computing the inertia tensor of a prototypical or "canonical" tetrahedron and
applying an affine transformation to produce the inertia tensor of each
individual volume.

First, given the covariance matrix of the "canonical" tetrahedron:

.. math::

   \mat{\hat{C}} \defas \begin{bmatrix}
      \frac{1}{60} & \frac{1}{120} & \frac{1}{120}\\
      \frac{1}{120} & \frac{1}{60} & \frac{1}{120}\\
      \frac{1}{120} & \frac{1}{120} & \frac{1}{60}
   \end{bmatrix}


Use the points in each triangle to define:

.. math::

   \mat{T}_n \defas
      \begin{bmatrix}
         | & | & | \\
         \vec{p_{n,1}} & \vec{p_{n,2}} & \vec{p_{n,3}}\\
         | & | & | \\
      \end{bmatrix}

The covariance of each tetrahedron volume is then:

.. math::

   \mat{C}_n = \left| \mat{T}_n \right| \mat{T}_n^T \mat{\hat{C}} \mat{T}_n

And the covariance matrix of the complete volume:

.. math::

   \mat{C}_V = \sum^N_{n=1} \mat{C}_n

And at last, the inertia tensor of the volume about the origin :math:`O` can
be computed directly from the covariance matrix:

.. math::

   \mat{J}_{V/O} = \mathrm{trace} \left( \mat{C}_V \right) \vec{I}_3 - \mat{C}_V


Apparent Mass of a Parafoil
===========================

This section uses Barrows' method for estimating the apparent mass matrix of
a wing with arc anhedral. These terms will be added to the real mass of the
canopy when running the paraglider dynamics models. For a discussion of
apparent mass effects, see :ref:`paraglider_dynamics:Apparent Mass`.


Barrows Formulation
-------------------

This section needs to define the terms that will be needed by the dynamics
models:

* :math:`\mat{A}_{a,R}`: apparent moment of inertia matrix about R

* :math:`\vec{r}^c_{RC/R}`

* :math:`\vec{r}^c_{PC/RC}`

Some notes about Barrows development:

* It assumes the foil is symmetric about the xz-plane (left-right symmetry)
  and about the yz-plane (fore-aft symmetry).

* It assumes the foil arch is circular.

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
   t &= \text{Airfoil thickness.}\\
   h^* &= \frac{h}{b}\\
   \end{aligned}

First, the apparent mass terms for a flat wing of a similar volume, from
Barrows' equations 34-39:

.. math::

   \begin{aligned}
   m_{f11} &= k_A \pi \left( t^2 b / 4 \right)\\
   m_{f22} &= k_B \pi \left( t^2 c / 4 \right)\\
   m_{f33} &= \left[ \mathrm{AR} / \left( 1 + \mathrm{AR} \right) \right] \pi \left( c^2 b / 4 \right)\\
   \\
   I_{f11} &= 0.055 \left[ \mathrm{AR} / \left( 1 + \mathrm{AR} \right) \right] b S^2\\
   I_{f22} &= 0.0308 \left[ \mathrm{AR} / \left( 1 + \mathrm{AR} \right) \right] c^3 S\\
   I_{f33} &= 0.055 b^3 t^2
   \end{aligned}

Where :math:`k_A` and :math:`k_B` are the "correction factors for
three-dimensional effects":

.. math::

   \begin{aligned}
   k_A &= 0.85\\
   k_B &= 1.0
   \end{aligned}

Assuming the parafoil arch is circular and not chordwise camber, use Barrows
equations 44 and 50 to compute the *pitch center* :math:`PC` and *roll center*
:math:`RC` as points directly above the *confluence point* :math:`C` of the
arc:

.. math::

   \begin{aligned}
   z_{PC/C} &= -\frac{r \sin \left(\Theta\right)}{\Theta}\\
   z_{RC/C} &= -\frac{z_{PC/C} \; m_{f22}}{m_{f22} + I_{f11}/r^2}\\
   z_{PC/RC} &= z_{PC/C} - z_{RC/C}
   \end{aligned}

Modifying the apparent mass terms from the flat wing to approximate the terms
for the arched wing, Barrows equations 51-55:

.. math::

   \begin{aligned}
   m_{11} &= k_A \left[ 1 + \left(\frac{8}{3}\right){h^*}^2 \right] \pi \left( t^2 b / 4 \right)\\
   m_{22} &= \frac{r^2 m_{f22} + I_{f11}}{z^2_{PC/C}}\\
   m_{33} &= m_{f33}\\
   \\
   I_{11} &= \frac{z^2_{PC/RC}}{z^2_{PC/C}} r^2 m_{f22} + \frac{z^2_{RC/C}}{z^2_{PC/C}} I_{f11}\\
   I_{22} &= I_{f22}\\
   I_{33} &= 0.055 \left( 1 + 8 {h^*}^2 \right) b^3 t^2
   \end{aligned}

The apparent mass and apparent moment of inertia matrices are then defined in
Barrows equation 1:

.. math::

   \mat{M}_a \defas
   \begin{bmatrix}
      m_{11} & 0 & 0\\
      0 & m_{22} & 0\\
      0 & 0 & m_{33}
   \end{bmatrix}

.. math::

   \mat{I}_a \defas
   \begin{bmatrix}
      I_{11} & 0 & 0\\
      0 & I_{22} & 0\\
      0 & 0 & I_{33}
   \end{bmatrix}

Define two helper matrices:

.. math::

   \mat{S}_2 \defas \begin{bmatrix} 0 & 0 & 0\\0 & 1 & 0\\0 & 0 & 0\end{bmatrix}

.. math::

   \mat{Q} = \mat{S}_2 \crossmat{\vec{r}^c_{PC/RC}} \mat{M}_a \crossmat{\vec{r}^c_{RC/R}}

Where :math:`\crossmat{\vec{x}}` is the :ref:`cross-product matrix operator
<crossmat>`.

Using the helper matrices, use Barrows equation 25 to write the rotational
part of the apparent inertia matrix:

.. math::

   \mat{J}_{a,R} \defas
      \mat{I} - \crossmat{\vec{r}^c_{RC/R}} \mat{M}_a \crossmat{\vec{r}^c_{RC/R}}
      - \crossmat{\vec{r}^c_{PC/RC}} \mat{M}_a \crossmat{\vec{r}^c_{PC/RC}} \mat{S}_2
      - \mat{Q} - \mat{Q}^T

And the corresponding angular momentum of the apparent mass about :math:`R`,
using Barrows equation 24:

.. math::

   \vec{h}_{a,R} =
      \left(
         \mat{S}_2 \crossmat{\vec{r}^c_{PC/RC}} + \crossmat{\vec{r}^c_{RC/R}}
      \right) \mat{M}_a \vec{v}^c_R + \mat{J}_{a,R} \omega

And finally, the completed moment of inertia matrix about the riser connection
point :math:`R`, from Barrows equation 27:

.. math::

   \mat{A}_{a,R} =
   \begin{bmatrix}
      \mat{M}_a & -\mat{M}_a \left(
         \crossmat{\vec{r}^c_{RC/R}} + \crossmat{\vec{r}^c_{PC/RC}} \mat{S}_2
      \right)\\
      \left(
         \mat{S}_2 \crossmat{\vec{r}^c_{PC/RC}}
         + \crossmat{\vec{r}^c_{RC/R}}
      \right) \mat{M}_a & \mat{J}_{a,R}
   \end{bmatrix}

Plus the vectors necessary to incorporate :math:`\mat{A}_R` into the final
dynamics:

.. math::

   \vec{r}^c_{PC/RC} = \begin{bmatrix} 0 & 0 & z_{PC/RC}\end{bmatrix}

Linear momentum of the apparent mass:

.. math::

   \vec{p}^b_a = \mat{M}_a \cdot \left(
      \vec{v}^b_{R/e}
      - \crossmat{\vec{r}^b_{RC/R}} \omega^b_{b/e}
      - \crossmat{\vec{r}^b_{PC/RC}} \mat{S}_2 \cdot \omega^b_{b/e}
   \right)

Angular momentum of the apparent mass about :math:`R`:

.. math::

   \vec{h}^b_{a,R} =
      \left(
         \mat{S}_2 \cdot \crossmat{\vec{r}_{PC/RC}} + \crossmat{\vec{r}_{RC/R}}
      \right) \cdot \mat{M}_a \cdot \vec{v}^b_{R/e}
      + \mat{J}_{a,R} \cdot \omega^b_{b/e}


Notes to self
-------------

* If :ref:`paraglider_dynamics:Reference Point` said this section gives
  reasons that `R` should be in the xz-plane, then make sure this section
  covers that.


Paraglider Models
=================

Model 6a
--------

This design uses the riser connection point :math:`R` for the dynamics
reference point, and incorporates the apparent mass matrix. [[The glidersim
package also includes `Paraglider6b`, which decouples the translational and
angular equations of motion by choosing the glider center of gravity for the
dynamics reference point to simplify the equations of motion, but does not
incorporate the apparent mass matrix.]]

An implementation of this model is available as :py:class:`Paraglider6a
<glidersim:pfh.glidersim.paraglider.Paraglider6a>` in the ``glidersim``
package.

.. math::
   :label: model6a_p

   \begin{aligned}
   {\vec{p}^b_{b/e}}
      &= m_b \, \vec{v}^b_{B/e} \\
      &= m_b \left(
            {\vec{v}^b_{R/e}}
            + {\vec{\omega}^b_{b/e}} \times {\vec{r}^b_{B/R}}
         \right)
   \end{aligned}


.. math::
   :label: model6a_p_dot

   \begin{aligned}
   {^e \dot{\vec{p}}^b_{b/e}}
      &= m_b \left(
            {^e \dot{\vec{v}}_{R/e}}
            + {^e\dot{\vec{\omega}}_{b/e}} \times {\vec{r}^b_{B/R}}
            + {\vec{\omega}^b_{b/e}} \times {^e\dot{\vec{r}}^b_{B/R}}
         \right)

      &= m_b \left(
            {^b\dot{\vec{v}}^b_{R/e}}
            + {\vec{\omega}^b_{b/e}} \times {\vec{v}^b_{R/e}}
            + {^b\dot{\vec{\omega}}^b_{b/e}} \times {\vec{r}^b_{B/R}}
            + {\vec{\omega}^b_{b/e}} \times \left(
               {\cancelto{0}{^b \dot{\vec{r}}^b_{B/R}}}
               + {\vec{\omega}^b_{b/e}} \times {\vec{r}^b_{B/R}}
              \right)
         \right)

      &= m_b \left(
            {^b\dot{\vec{v}}^b_{R/e}}
            + {\vec{\omega}^b_{b/e}} \times {\vec{v}^b_{R/e}}
            + {^b\dot{\vec{\omega}}^b_{b/e}} \times {\vec{r}^b_{B/R}}
            + {\vec{\omega}^b_{b/e}} \times {\vec{\omega}^b_{b/e}} \times {\vec{r}^b_{B/R}}
         \right)

      &= {\vec{F}^b_{\textrm{wing,aero}}} + {\vec{F}^b_{\textrm{wing,weight}}}
   \end{aligned}

.. math::
   :label: model6a_h_dot

   \begin{aligned}
   {^e \dot{\vec{h}}_{b/e}}
      &= {^b\dot{\vec{h}}_b}
         + {\vec{\omega}^b_{b/e} \times \vec{h}_b}

      &= {\mat{J^b_B}{^b \dot{\vec{\omega}}^b_{b/e}}}
         + {\vec{\omega} \times \left( \mat{J^b_B} \vec{\omega}^b_{b/e} \right)}

      &= {\vec{M}^b_{\textrm{wing,aero}}} + {\vec{M}^b_{\textrm{wing,weight}}}
   \end{aligned}


.. math::
   :label: model6a_linear_system

   \begin{bmatrix}
      {m_b \mat{I_3}} & {-m_b \crossmat{\vec{r}^b_{B/R}}} & {\mat{0_{3\times3}}} & {\mat{I_3}}\\
      {\mat{0_{3\times3}}} & {\mat{J^b_B}} & {\mat{0_{3\times3}}} & {-\crossmat{\vec{r}^b_{R/B}}}\\
   \end{bmatrix}
   \begin{bmatrix}
      {^b \dot{\vec{v}}^b_{R/e}}\\
      {^b \dot{\vec{\omega}}^b_{b/e}}\\
   \end{bmatrix}
   =\begin{bmatrix}
      \vec{B}_1\\
      \vec{B}_2\\
   \end{bmatrix}


Model 9a
--------

This design uses the riser connection midpoint `R` as the reference point
for both the body and the payload, which simplifies incorporating the apparent
mass matrix.

Similar derivations:

* "Spacecraft Attitude Dynamics" (Hughes; 2004):
  :cite:`hughes2004SpacecraftAttitudeDynamics`. Good development of
  how to use the derivatives of translational and angular acceleration to
  develop the equations of motion, and its application to multi-rigid-body
  dynamics.

* "Evaluation of Multibody Parafoil Dynamics Using Distributed Miniature
  Wireless Sensors" (Gorman;
  2012): :cite:`gorman2012EvaluationMultibodyParafoil`

An implementation of this model is available as :py:class:`Paraglider9a
<glidersim:pfh.glidersim.paraglider.Paraglider9a>` in the ``glidersim``
package.

[[The ``glidersim`` package also includes :py:class:`Paraglider9b
<glidersim:pfh.glidersim.paraglider.Paraglider9b>`, which uses the centers of
mass as the reference points for the body and payload dynamics. That choice
simplifies the derivatives for angular momentum (since it eliminates the
moment arms), but it makes it more difficult to incorporate the effects of
apparent mass.]]

.. math::
   :label: model9a_body_p

   \begin{aligned}
   {\vec{p}^b_{b/e}}
      &= m_b \, \vec{v}^b_{B/e} \\
      &= m_b \left(
            {\vec{v}^b_{R/e}}
            + {\vec{\omega}^b_{b/e}} \times {\vec{r}^b_{B/R}}
         \right)
   \end{aligned}

.. math::
   :label: model9a_body_p_dot

   \begin{aligned}
   {^e \dot{\vec{p}}^b_{b/e}}
      &= m_b \left( 
            {^e \dot{\vec{v}}_{R/e}}
            + {^e\dot{\vec{\omega}}_{b/e}} \times {\vec{r}^b_{B/R}}
            + {\vec{\omega}^b_{b/e}} \times {^e\dot{\vec{r}}^b_{B/R}}
         \right)

      &= m_b \left(
            {^b\dot{\vec{v}}^b_{R/e}}
            + {\vec{\omega}^b_{b/e}} \times {\vec{v}^b_{R/e}}
            + {^b\dot{\vec{\omega}}^b_{b/e}} \times {\vec{r}^b_{B/R}}
            + {\vec{\omega}^b_{b/e}} \times \left(
               {\cancelto{0}{^b \dot{\vec{r}}^b_{B/R}}}
               + {\vec{\omega}^b_{b/e}} \times {\vec{r}^b_{B/R}}
              \right)
         \right)

      &= m_b \left(
            {^b\dot{\vec{v}}^b_{R/e}}
            + {\vec{\omega}^b_{b/e}} \times {\vec{v}^b_{R/e}}
            + {^b\dot{\vec{\omega}}^b_{b/e}} \times {\vec{r}^b_{B/R}} 
            + {\vec{\omega}^b_{b/e}} \times {\vec{\omega}^b_{b/e}} \times {\vec{r}^b_{B/R}}
         \right)

      &= {\vec{F}^b_{\textrm{wing,aero}}} + {\vec{F}^b_{\textrm{wing,weight}}} - {\vec{F}^b_R}
   \end{aligned}

.. math::
   :label: model9a_payload_p_dot

   \begin{aligned}
   {^e \dot{\vec{p}}^p_{p/e}}
      &= m_p \left( 
            {^e \dot{\vec{v}}_{R/e}}
            + {^e\dot{\vec{\omega}}_{p/e}} \times {\vec{r}^p_{P/R}}
            + {\vec{\omega}^p_{p/e}} \times {^e\dot{\vec{r}}^p_{P/R}}
         \right)

      &= m_p \left(
            {^p\dot{\vec{v}}^p_{R/e}}
            + {\vec{\omega}^p_{p/e}} \times {\vec{v}^p_{R/e}}
            + {^p\dot{\vec{\omega}}^p_{p/e}} \times {\vec{r}^p_{P/R}}
            + {\vec{\omega}^p_{p/e}} \times \left(
               {\cancelto{0}{^p \dot{\vec{r}}^p_{P/R}}}
               + {\vec{\omega}^p_{p/e}} \times {\vec{r}^p_{P/R}}
              \right)
         \right)

      &= m_p \left(
            {^p\dot{\vec{v}}^p_{R/e}}
            + {\vec{\omega}^p_{p/e}} \times {\vec{v}^p_{R/e}}
            + {^p\dot{\vec{\omega}}^p_{p/e}} \times {\vec{r}^p_{p/R}} 
            + {\vec{\omega}^p_{p/e}} \times {\vec{\omega}^p_{p/e}} \times {\vec{r}^p_{P/R}}
         \right)

      &= {\vec{F}^p_{\textrm{payload,aero}}} + {\vec{F}^p_{\textrm{payload,weight}}} + {\vec{F}^p_R}
   \end{aligned}


.. math::
   :label: model9a_body_h_dot

   \begin{aligned}
   {^e \dot{\vec{h}}_b}
      &= {^b\dot{\vec{h}}_b}
         + {\vec{\omega}^b_{b/e} \times \vec{h}_b}

      &= {\mat{J^b_B}{^b \dot{\vec{\omega}}^b_{b/e}}}
         + {\vec{\omega} \times \left( \mat{J^b_B} \vec{\omega}^b_{b/e} \right)}

      &= {\vec{M}^b_{\textrm{wing,aero}}}
         + {\vec{M}^b_{\textrm{wing,weight}}}
         - {\vec{r}^b_{R/B} \times \vec{F}^b_R}
         - \vec{M}^b_R
   \end{aligned}


.. math::
   :label: model9a_payload_h_dot

   \begin{aligned}
   {^e \dot{\vec{h}}_p}
      &= {^p\dot{\vec{h}}_p}
         + {\vec{\omega}^p_{p/e} \times \vec{h}_p}

      &= {\mat{J^p_P}{^p \dot{\vec{\omega}}^p_{p/e}}}
         + {\vec{\omega} \times \left( \mat{J^p_P} \vec{\omega}^p_{p/e} \right)}

      &= {\vec{M}^p_{\textrm{wing,aero}}}
         + {\vec{M}^p_{\textrm{wing,weight}}}
         - {\vec{r}^p_{R/P} \times \vec{F}^p_R}
         - \vec{M}^p_R
   \end{aligned}

And finally, the complete system of equations:

**FIXME: I think this is the old version that didn't include the apparent
mass. Compare to the code implementation.**


.. math::
   :label: model9a_linear_system

   \begin{bmatrix}
      {m_b \mat{I_3}} & {-m_b \crossmat{\vec{r}^b_{B/R}}} & {\mat{0_{3\times3}}} & {\mat{I_3}}\\
      {m_p \mat{C_{p/b}}} & {\mat{0_{3\times3}}} & {-m_p \crossmat{\vec{r}^p_{p/R}}} & {-\mat{C_{p/b}}}\\
      {\mat{0_{3\times3}}} & {\mat{J^b_B}} & {\mat{0_{3\times3}}} & {-\crossmat{\vec{r}^b_{R/B}}}\\
      {\mat{0_{3\times3}}} & {\mat{0_{3\times3}}} & {\mat{J^p_P}} & {\crossmat{\vec{r}^p_{P/R}} \mat{C_{p/b}}}
   \end{bmatrix}
   \begin{bmatrix}
      {^b \dot{\vec{v}}^b_{R/e}}\\
      {^b \dot{\vec{\omega}}^b_{b/e}}\\
      {^b \dot{\vec{\omega}}^b_{p/e}}\\
      {\vec{F}^b_R}
   \end{bmatrix}
   =\begin{bmatrix}
      \vec{B}_1\\
      \vec{B}_2\\
      \vec{B}_3\\
      \vec{B}_4
   \end{bmatrix}

where

.. math::

   \begin{aligned}
      \vec{B}_1 &= {\vec{F}^b_{\textrm{wing,aero}}}
      + {\vec{F}^b_{\textrm{wing,weight}}}
      - {m_b \, {\vec{\omega}^b_{b/e}} \times {\vec{v}^b_{R/e}}}
      - {m_b \, {\vec{\omega}^b_{b/e}} \times {\vec{\omega}^b_{b/e}} \times {\vec{r}^b_{B/R}}}\\
      \vec{B}_2 &= {\vec{F}^b_{\textrm{p,aero}}}
      + {\vec{F}^p_{\textrm{p,weight}}}
      - {m_p \, {\vec{\omega}^p_{b/e}} \times {\vec{v}^p_{R/e}}}
      - {m_p \, {\vec{\omega}^p_{p/e}} \times {\vec{\omega}^p_{p/e}} \times {\vec{r}^p_{P/R}}}\\
      \vec{B}_3 &= {\vec{M}^b_{\textrm{wing,aero}}}
      + {\vec{M}^b_{\textrm{wing,weight}}}
      - {\vec{M}^b_R}
      - {\vec{\omega}^b_{b/e} \times \left( {\mat{J^b_B} \vec{\omega}^b_{b/e}} \right)}\\
      \vec{B}_4 &= {\vec{M}^p_{\textrm{p,aero}}}
      + {\vec{M}^p_R}
      - {\vec{\omega}^p_{p/e} \times \left( {\mat{J^p_P} \vec{\omega}^p_{p/e}} \right)}
   \end{aligned}
