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


Canopy Aerodynamics
===================


Lifting-line theory
-------------------

NT


Non-linear lifting line theory
------------------------------

<Introduce non-linear lifting line theory.>

.. figure:: figures/paraglider/dynamics/phillips_scratch.*

   Wing sections for Phillips' method.


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
      {\vec{F}^b_{\textrm{wing,aero}}}
      + {\vec{F}^b_{\textrm{wing,weight}}}
      - {m_b \, {\vec{\omega}^b_{b/e}} \times {\vec{v}^b_{R/e}}}
      - {m_b \, {\vec{\omega}^b_{b/e}} \times {\vec{\omega}^b_{b/e}} \times {\vec{r}^b_{B/R}}}\\
      {\vec{F}^b_{\textrm{p,aero}}}
      + {\vec{F}^p_{\textrm{p,weight}}}
      - {m_p \, {\vec{\omega}^p_{b/e}} \times {\vec{v}^p_{R/e}}}
      - {m_p \, {\vec{\omega}^p_{p/e}} \times {\vec{\omega}^p_{p/e}} \times {\vec{r}^p_{P/R}}}\\
      {\vec{M}^b_{\textrm{wing,aero}}}
      + {\vec{M}^b_{\textrm{wing,weight}}}
      - {\vec{M}^b_R}
      - {\vec{\omega}^b_{b/e} \times \left( {\mat{J^b_B} \vec{\omega}^b_{b/e}} \right)}\\
      {\vec{M}^p_{\textrm{p,aero}}}
      + {\vec{M}^p_R}
      - {\vec{\omega}^p_{p/e} \times \left( {\mat{J^p_P} \vec{\omega}^p_{p/e}} \right)}
   \end{bmatrix}
