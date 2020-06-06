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

  * Gonzolez 1993, :cite:`gonzalez1993PrandtlTheoryApplied`

  * Belloc, :cite:`belloc2015WindTunnelInvestigation`

* Paraglider Dynamics

  * Babinsky 1999, :cite:`babinsky1999AerodynamicPerformanceParagliders`

  * Slegers, :cite:`gorman2012EvaluationMultibodyParafoil`


Canopy Aerodynamics
===================


Lifting-line theory
-------------------

NT


Non-linear lifting line theory
------------------------------

<Introduce non-linear (aka, "numerical") lifting line theories.>

.. figure:: figures/paraglider/dynamics/phillips_scratch.*

   Wing sections for Phillips' method.


Apparent Mass
=============

Newton's second law states that the acceleration of an isolated object is
proportional to the net force applied to that object:

.. math::

   \vec{a} = \frac{\sum{\vec{F}}}{m}

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

   \vec{a} = \frac{\sum{\vec{F}}}{m + m_a}

This *apparent mass* :math:`m_a` becomes increasingly more significant as the
density of the vehicle approaches the density of the fluid. If the density of
the vehicle is much greater than the density of the fluid the effect is often
ignored, as is the case for traditional aircraft, which are much more dense
than the surrounding air. For lightweight aircraft, however, such as
a parafoil, where the density of the vehicle is much closer to the density of
the air, the effect can be significant.

Notes to self:

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
  as the basis for `Model6b`.

* :cite:`thomasson2000EquationsMotionVehicle`: The equations in Lissaman and
  Barrows assume irrotational flows. This paper also considers rotational flow?
  I think?


Dynamics Models
===============

A paraglider can be considered a system composed of canopy, lines, harness,
and pilot. Although nearly every component are highly flexible they tend to
remain relatively rigid during normal flight. The flight dynamics can be
greatly simplified by assuming a rigid body model.


Six degree-of-freedom models
----------------------------

In these models, the paraglider is approximated as a single rigid body.
With all the components held in a fixed position, the dynamics can be
described by solving for the derivatives of translational and angular
momentum.



Nine degree-of-freedom models
-----------------------------

Model 9a
^^^^^^^^

This model breaks the system into two components: a body and a payload. The
body includes the lines, canopy, and enclosed air. The payload includes the
harness and pilot. The body and payload are modeled using a single connection
point :math:`R` which is positioned at the midpoint between the two riser
connection points.

There are nine degrees of freedom: six for the orientations of the body and
payload, three for the velocity of the connection point, and three for the
internal force between the two components.

It chooses the centers of mass as the reference points for the body and
payload. This simplifies the derivatives for angular momentum (since it
eliminates the moment arms), but it makes it difficult to incorporate the
effects of apparent mass.


Model 9b
^^^^^^^^

This model also uses the body and payload 


.. _paraglider_fbd_9dof:
.. figure:: figures/paraglider/dynamics/paraglider_fbd_9dof.*

   Free body diagram for a 9-DoF model.

Use the reference geometry in :numref:`paraglider_fbd_9dof`. The nine
degrees-of-freedom model defines the paraglider as a system of two bodies: the
canopy and the payload (the harness). The dynamic equations can be written by
solving for the translational momentum :math:`^e \dot{\vec{p}}
= \sum{\vec{F}}` and angular momentum :math:`^e \dot{\vec{h}} = \sum \vec{M}`
for both bodies.

.. math::
   :label: 9dof_body_p

   \begin{aligned}
   {\vec{p}^b_{b/e}}
      &= m_b \, \vec{v}^b_{B/e} \\
      &= m_b \left(
            {\vec{v}^b_{R/e}}
            + {\vec{\omega}^b_{b/e}} \times {\vec{r}^b_{B/R}}
         \right)
   \end{aligned}

.. math::
   :label: 9dof_body_p_dot

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
   :label: 9dof_payload_p_dot

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
   :label: 9dof_body_h_dot

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
   :label: 9dof_payload_h_dot

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

.. math::
   :label: 9dof_linear_system

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
