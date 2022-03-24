.. This chapter combines component models into composite *system dynamics*
   models.


***************
System dynamics
***************

This chapter combines the individual :doc:`component models
<paraglider_components>` into composite *system dynamics* models. In this
paper, a *system dynamics* model is a set of derivatives that define the
translational and angular acceleration of groups of components that represent
an aircraft, specified using a coordinate system attached to the aircraft.
Developing a system model can be roughly described as a sequence of steps:

1. Choose a set of components to represent the aircraft

#. Characterize their connections

#. Choose a dynamics reference point for the composite system

#. Develop the system of equations for the accelerations


Components
==========

The previous chapter defined component models for the canopy, suspension lines,
and harness; in the system models, these are lumped into two quasi-rigid-body
groups called the *body* and the *payload*. The *body* of the glider is the
combination of canopy and suspension lines. The *payload* includes the harness,
pilot, and their gear (in this simplified model, the pilot and their gear are
treated as additional masses that are added to the mass of the harness).

These models are quasi-rigid because the dynamics equations will only consider
their instantaneous configurations when calculating their accelerations;
conservation of momentum requires accounting for redistributions of mass, but
doing so would require inertia derivatives as functions of time derivatives of
the control input (such as weight shift, accelerator, etc), which would
significantly complicate the model. Because the redistributions of mass are
relatively small for typical scenarios, these models assume the affect of
violating conservation of momentum is negligible.


.. Terminology: "body" and "payload" aircraft coordinate systems

It is important to note that the unfortunately ambiguous terminology of *body*
is deliberate. The paraglider community typically refers to the combination of
canopy and lines as a *paraglider wing*, but the "body" convention improves
consistency with existing *parafoil-payload* literature (which in turn
inherited the term from conventional aeronautics literature). Some texts
prefer the term *parafoil*, but having the same prefix :math:`p` for both
*parafoil* and *payload* makes subscripting the variables unnecessarily
difficult. Similarly, using "wing" would be preferred in this context, but
subscripting with :math:`w` causes confusion when discussing wind vectors.
Referring to whatever group of components include the canopy as the *body* was
a compromise chosen for consistency with existing literature.


Connections
===========

.. Model the connection between the "lumped" components (body and payload)

Next, the system model must characterize the connection between the body and
payload. In literature, parafoil-payload models are commonly categorized by
their *degrees-of-freedom* (DoF): the total number of dimensions in which the
components of the system are free to move. The body has 3-DoF for
translational motion and another 3-DoF for rotational motion, and if the
payload is allowed to translate or rotate relative to the body, those
additional DoF are added to the total DoF of the system model. For example, in
a 6-DoF model, the body and payload are connected as a single rigid body, with
no relative motion between them.

.. figure:: figures/paraglider/dynamics/paraglider_fbd_6dof.*
   :name: paraglider_fbd_6dof

   Diagram for a 6-DoF model.


.. 9-DoF model

For typical paragliding flight maneuvers, assuming a fixed payload orientation
is reasonably accurate, but with one significant failing: although the
relative roll and twist are typically negligible, relative pitch about the
riser connections is very common, even during static glides. Friction at the
riser carabiners (and aerodynamic drag, to a lesser extent) dampen pitching
oscillations, but the payload is otherwise free to pitch as necessary to
maintain equilibrium. Assuming a fixed relative pitch angle introduces
a fictitious pitching moment that disturbs the equilibrium conditions of the
wing and artificially dampens the pitching dynamics during maneuvers. To
mitigate that issue, the obvious solution is to add an additional DoF, but for
demonstration purposes it is simpler to define a full 9-DoF model, where the
body and payload are connected at the :ref:`riser midpoint
<paraglider_components:Accelerator>` :math:`RM`. The connection is modeled as
a spring-damper system, which produces an internal force :math:`\vec{F}_R` and
moment :math:`\vec{M}_R`:

.. FIXME: should be `f_RM` and `m_RM` or similar

.. figure:: figures/paraglider/dynamics/paraglider_fbd_9dof.*
   :name: paraglider_fbd_9dof

   Diagram for a 9-DoF model with internal forces.


Reference point
===============

Each dynamics model must choose a reference point about which the moments and
angular inertia are calculated. A common choice for conventional aircraft is
the center of real mass because it decouples the translational and angular
dynamics of isolated objects. For a paraglider, however, this is not possible:
paragliders are sensitive to apparent mass, which depends on the direction of
motion, so there is no "center" that decouples the translational and rotational
terms of the apparent inertia matrix :cite:`barrows2002ApparentMassParafoils`.
Because the system matrix cannot be diagonalized there is no advantage in
choosing the center of real mass. Instead, the reference point can be chosen
such that it simplifies other calculations.

.. Note that the reference point for the dynamics can be different from the
   point for tracking the glider position

In particular, the :ref:`method <paraglider_components:Apparent mass>` to
estimate the apparent inertia matrix requires that the reference point lies in
the :math:`xz`-plane of the canopy. Two natural choices in that plane are the
leading edge of the central section, or the midpoint between the two risers.
The :ref:`riser midpoint <system_dynamics:Connections>` :math:`RM` has the
advantage that is a fixed point in both the body and payload coordinate
systems, which means it does not depend on the relative position or orientation
of the payload with respect to the body. (This choice simplifies the equations
for the :ref:`9-DoF model <derivations:Model 9a>` while maintaining consistency
with the :ref:`6-DoF model <derivations:Model 9a>`.)

.. 6a and 9a use `RM`, but the others don't


System inputs
=============

The inputs :math:`\vec{u}` to the system model the control inputs for each
component (with the exception of the trailing edge :ref:`deflection distances
<deflected_airfoil_arc>` :math:`\delta_d(s)` which are computed internally
using the suspension lines and foil geometry models), the wind velocity
:math:`\vec{v}_{W/e}`, air density :math:`\rho_\textrm{air}`, and the gravity
vector :math:`\vec{g}`.

.. math::
   :label: system inputs

   \vec{u} =
     \left\{
       \delta_a,
       \delta_{bl},
       \delta_{br},
       \delta_w,
       \vec{v}_{W/e}^b,
       \rho_\textrm{air},
       \vec{g}^b,
     \right\}

Here the wind field is assumed to be uniform so the wind velocity at every
control point is defined by a single, constant vector, but for non-uniform
wind fields there will be a unique wind vector for each aerodynamic control
point.

.. FIXME: discussion:

   * `v_W/e` could be written as a matrix (an array of vectors)

   * These are functions of time, not standalone/"instantaneous" variables.

   * Input vectors are in local (body and/or payload coordinates.

   * I've decided to have the state dynamics models transform all the vectors
     into body coordinates so the system models don't have to. For the 9-DoF,
     I'm passing `Theta_p2b` to allow transforming the wind vectors for the
     payload control points into payload coordinates; they need `C_p2b`
     anyway, so that's not a big deal, and passing them as Euler angles allows
     them to be used for the restoring moments.]]


Equations of motion
===================

The `equations of motion <https://en.wikipedia.org/wiki/Equations_of_motion>`__
are developed by solving for the derivatives of translational momentum
:math:`{^e \dot{\vec{p}}} = \sum{\vec{F}} = m \dot{\vec{v}}` and angular
momentum :math:`{^e \dot{\vec{h}}} = \sum \vec{M} = \mat{J} \dot{\vec{\omega}}`
for each group of components :cite:`hughes2004SpacecraftAttitudeDynamics`. In
addition to requiring the forces, moments, and inertia matrices for each
component, each system model must choose a dynamics reference point and whether
to account for the affects of *apparent mass*. The :ref:`appendix
<derivations:Paraglider system models>` includes derivations demonstrating
different choices for several each model.


.. 6-DoF model

For the 6-DoF model, the most complete is :ref:`derivations:Model 6a` which
accounts for the effects of apparent mass, while :ref:`derivations:Model 6b`
and :ref:`derivations:Model 6c` have the advantage of simplicity (making them
easier to implement and useful for validating implementations of more complex
models). The derivation produces a system of equations
:eq:`model6a_complete_system` that can be solved for the two vector
derivatives that describe the accelerations of the body relative to the earth
frame :math:`\mathcal{F}_e` taken with respect to the body frame
:math:`\mathcal{F}_b`:

.. math::
   :label: model6a_system_derivatives

   \begin{aligned}
     {^b \dot{\vec{v}}_{RM/e}} \qquad & \textrm{translational acceleration of the riser midpoint} \, RM \\
     {^b \dot{\vec{\omega}}_{b/e}} \qquad & \textrm{angular acceleration of the body} \\
   \end{aligned}

.. [[Notice, the current values of the variables are the :math:`\vec{x}
   = \left\{\vec{v}_{RM/e}, \vec{\omega}_{b/e} \right\}`]]


.. 9-DoF

Similarly, for the 9-DoF model, :ref:`derivations:Model 9a` also develops
a complete system of equations :eq:`model9a_complete_system` that account for
apparent mass of the canopy, but with the addition of a separate angular
acceleration for the payload with respect to the payload frame
:math:`\mathcal{F}_p`:

.. math::
   :label: model9a_system_derivatives

   \begin{aligned}
     {^b \dot{\vec{v}}_{RM/e}} \qquad &\textrm{translational acceleration of the riser midpoint} \, RM \\
     {^b \dot{\vec{\omega}}_{b/e}} \qquad & \textrm{angular acceleration of the body} \\
     {^p \dot{\vec{\omega}}_{p/e}} \qquad & \textrm{angular acceleration of the payload} \\
   \end{aligned}
