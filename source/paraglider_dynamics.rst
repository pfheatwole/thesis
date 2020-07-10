
A paraglider can be considered a system composed of canopy, lines, harness,
and pilot. Although nearly every component are highly flexible they tend to
remain relatively rigid during normal flight. The flight dynamics can be
greatly simplified by assuming a rigid body model.



*******************
Paraglider Dynamics
*******************

.. list-table:: Wings
   :header-rows: 1
   :align: center

   * - Wing 1
     - Wing 2
     - Wing 3
   * - .. image:: figures/paraglider/geometry/foil2.*
     - .. image:: figures/paraglider/geometry/foil2.*
     - .. image:: figures/paraglider/geometry/foil2.*
   * - .. image:: figures/paraglider/geometry/foil2.*
     - .. image:: figures/paraglider/geometry/foil2.*
     - .. image:: figures/paraglider/geometry/foil2.*
   * - .. image:: figures/paraglider/geometry/foil2.*
     - .. image:: figures/paraglider/geometry/foil2.*
     - .. image:: figures/paraglider/geometry/foil2.*


Related Work
============

* This paper is specifically about paragliding wings, but in terms of the
  aerodynamics it is closely related to *parafoil-payload systems* (primarily
  of interest to the military and aerospace organizations) and *kites* (kite
  boarding, airborne wind energy systems, etc)


* Canopy Aerodynamics

  * Gonzalez 1993, :cite:`gonzalez1993PrandtlTheoryApplied`

  * Belloc, :cite:`belloc2015WindTunnelInvestigation`

  * :cite:`kulhanek2019IdentificationDegradationAerodynamic`

  * :cite:`belloc2015WindTunnelInvestigation`

  * :cite:`belloc2016InfluenceAirInlet`

  * :cite:`babinsky1999AerodynamicPerformanceParagliders`

  * Cells (distortions, etc):

    * :cite:`kulhanek2019IdentificationDegradationAerodynamic`

    * :cite:`lolies2019NumericalMethodsEfficient`


* Paraglider Dynamics

  * Babinsky 1999, :cite:`babinsky1999AerodynamicPerformanceParagliders`

  * Slegers, :cite:`gorman2012EvaluationMultibodyParafoil`

  * :cite:`ward2014ParafoilControlUsing`

  * Apparent mass

    * :cite:`lissaman1993ApparentMassEffects`

    * :cite:`thomasson2000EquationsMotionVehicle`

    * :cite:`barrows2002ApparentMassParafoils`



Reference Point
===============

Before developing the components of the dynamics models, it is helpful to
choose a common reference point for the translational dynamics. [[Why?]]
Traditionally, aircraft models choose the system center of mass, because it
decouples the translational and angular dynamics. For paragliders, however,
the center of mass is not a fixed point: weight shift, accelerator, and
atmospheric air density all effect the location of the paraglider center of
mass. This makes it a poor choice for tracking the vehicle trajectory over
time.

Selecting a fixed point on the vehicle slightly increases the complexity of
the dynamics equations, but it simplifies [["stuff"; does it make the 9 DoF
less complicated since the hinge is now through `R`?]]. For reasons to be
discussed in `Apparent Mass`_, the dynamics are simplified if reference is
a point in the xz-plane of the wing. The most natural choices in that plane
are the leading edge of the central section, or the midpoint between the two
risers, which is constant regardless of the width the riser chest strap.

This paper uses the midpoint between the two riser connection points,
designated :math:`R`, for all dynamics equations. Because the risers are very
near to where the pilot would place their flight device, this is the most
representative of the data measured by flight recorders, making it the most
convenient for comparing real flight data to simulated data.


Apparent Mass
=============

Newton's second law states that the acceleration of an isolated object is
proportional to the net force applied to that object:

.. math::

   a = \frac{\sum{F}}{m}

This simple rule is sufficient and effective for determining the behavior of
isolated objects, but when an object is immersed in a fluid it is longer
isolated. When an object moves through a fluid there is an exchange of
momentum, and so the momentum of the fluid must be taken into account as well.

In static scenarios, where the vehicle is not accelerating relative to the
fluid (ie, changing speed and/or direction), this exchange of momentum is
traditionally summarized by coefficients that describe how the forces and
moments on the wing change with the air velocity. But for unsteady flows, where
the vehicle is accelerating relative to the fluid, the net force on the vehicle
can no longer be equated to the product of the vehicle's mass and acceleration.
Instead, when a net force is applied to an object in a fluid, it will
accelerate more slowly than the object would have in isolation; it is as if the
vehicle has increased its mass:

.. math::

   a = \frac{\sum{F}}{m + m_a}

This *apparent mass* :math:`m_a` becomes more significant as the density of
the vehicle approaches the density of the fluid. If the density of the vehicle
is much greater than the density of the fluid the effect is often ignored, as
is the case for traditional aircraft, which are much more dense than the
surrounding air. For lightweight aircraft, however, such as a parafoil, where
the density of the vehicle is much closer to the density of the air, the
effect can be significant.

Because apparent mass effects are the result of a volume in motion relative to
a fluid, its magnitude depends on the direction of the motion relative to the
volume. Unlike the inertia due to real mass, apparent inertia is anisotropic,
and the diagonal terms of the apparent mass matrix are independent.


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

* If `Reference Point`_ said this section gives reasons that `R` should be in
  the xz-plane, then make sure this section covers that.

* It's not correct to say that the effect becomes greater as the density of the
  vehicle decreases. Whether it is **significant** depends only on the ratio `m
  / m_a`. If :math:`m \gg m_a` then no worries.

  However, `m` does depend on the density of the vehicle, and `m_a` does depend
  on the density of the fluid. But `m_a` also depends on the shape of the
  object and the relative velocity of the fluid.

  It's not a big deal, but careful how you word it.

Some references I need to discuss:

* :cite:`lissaman1993ApparentMassEffects`: outlined a simple method for
  estimating the apparent mass of parafoils.

* :cite:`barrows2002ApparentMassParafoils`: added corrections to the equations
  from Lissaman. Provides the setup for a linear system 6 DoF model that I used
  as the basis for `Model6a`.

* :cite:`thomasson2000EquationsMotionVehicle`: The equations in Lissaman and
  Barrows assume irrotational flows. This paper also considers rotational flow?
  I think?


Six degree-of-freedom dynamics
==============================

In these models, the paraglider is approximated as a single rigid body.
With all the components held in a fixed position, the dynamics can be
described by solving the system of equations produced by equating the
derivatives of translational and angular momentum to the sum of forces and
moments on the rigid body.

[[FIXME: the six and nine DoF introductions should have parallel structure.
Write one of them, then adapt it for the other so they develop in the same
way.]]

.. figure:: figures/paraglider/dynamics/paraglider_fbd_6dof.*
   :name: paraglider_fbd_6dof

   Diagram for a 6-DoF model.

The derivation in this section is available as `Paraglider6a` in the
`glidersim` package. It uses the riser connection point :math:`R` for the
dynamics reference point, and incorporates the apparent mass matrix. [[The
glidersim package also includes `Paraglider6b`, which decouples the
translational and angular equations of motion by choosing the glider center of
gravity for the dynamics reference point to simplify the equations of motion,
but does not incorporate the apparent mass matrix.]]

[[Can I link to the glidersim module documentation from here?]]


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


Nine degree-of-freedom dynamics
===============================

The 6-DoF models constrain the relative payload orientation to a fixed
position. This is reasonably accurate for average flight maneuvers, but it has
one significant failing: although the relative roll and twist are typically
[[negligible]], relative pitch about the riser connections is very common.
Friction at the riser carabiners adds a damping effect to pitching
oscillations, but in general the harness is free to pitch as necessary to
maintain equilibrium. Assuming a fixed pitch angle introduces a incorrect
pitching moment that disturbs the equilibrium conditions of the wing and
artificially dampens the pitching dynamics during maneuvers.

To mitigate that issue, models with higher degrees of freedom break the system
into two components, a body and a payload, and permit relative orientations
between the two components. The body includes the lines, canopy, and enclosed
air. The payload includes the harness and pilot.

[[Discuss the 7-, 8-, and 9-DoF models from literature]]

This section develops a model with nine degrees of freedom: six for the
orientations of the body and payload, three for the velocity of the connection
point, and three for the internal force between the two components. The body
and payload are modeled as two rigid bodies connected at the riser midpoint
:math:`R`, with the connection modeled as a spring-damper system.

.. figure:: figures/paraglider/dynamics/paraglider_fbd_9dof.*
   :name: paraglider_fbd_9dof

   Diagram for a 9-DoF model with internal forces.

The equations of motion are developed by solving for the translational
momentum :math:`^e \dot{\vec{p}} = \sum{\vec{F}}` and angular momentum
:math:`^e \dot{\vec{h}} = \sum \vec{M}` for both bodies.

The model in this section is available as `Paraglider9a` in the `glidersim`
package. It uses the riser connection midpoint `R` as the reference point for
both the body and the payload, which simplifies incorporating the apparent
mass matrix.

[[The glidersim package also includes `Paraglider9b`, which uses the centers
of mass as the reference points for the body and payload dynamics. That choice
simplifies the derivatives for angular momentum (since it eliminates the
moment arms), but it makes it more difficult to incorporate the effects of
apparent mass.]]


Similar derivations:

* "Spacecraft Attitude Dynamics" (Hughes; 2004):
  :cite:`hughes2004SpacecraftAttitudeDynamics`. Good development of
  how to use the derivatives of translational and angular acceleration to
  develop the equations of motion, and its application to multi-rigid-body
  dynamics.

* "Evaluation of Multibody Parafoil Dynamics Using Distributed Miniature
  Wireless Sensors" (Gorman;
  2012): :cite:`gorman2012EvaluationMultibodyParafoil`


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
