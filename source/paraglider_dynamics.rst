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


* Define *dynamics*

* What are paraglider dynamics used for?

  [[They're what I'll be using to generate flight trajectories.]]


.. Roadmap

* Establish the modeling requirements in the context of flight reconstruction

* Discuss existing paraglider models from literature?

* Individual component dynamics

  [[inertia and control systems?]]

  * Wing

  * Harness

* Composite system dynamics

  [[Degrees-of-freedom, connection model, etc?]]

* Demonstrate the polar curves of my Hook3ish? (Feels a bit off here. Hrm.)

* [[**FIXME**: where do I describe the aerodynamic *control points*?]]


Modeling requirements
=====================

* [[This stage is about what I'm **not** choosing to model as much as it is
  about what I am.]]

* [[A paraglider can be considered a system composed of canopy, lines,
  harness, and pilot. Although nearly every component are made from highly
  flexible materials, they tend to remain relatively rigid during typical
  flight conditions. The flight dynamics can be greatly simplified by assuming
  a rigid body model.]]

* I put a lot of work into non-uniform wind, etc, in the aerodynamics. The
  dynamics model should be capable of leveraging that flexibility.

* Intuitive (as possible), sufficiently flexible, etc. [[FIXME: vague]]

* Degrees of freedom? (eg, include relative motion of the harness?)

* [[Weight shift control is in, riser controls are out]]

  **Does it make sense to have this "modeling requirements" up front if this
  chapter includes both the wing and the harness?**


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


Canopy
======

[[This section describes what goes into the dynamics function: velocities,
gravity, control inputs, inertia, air density, etc.]]


Inertia
-------

Solid mass
^^^^^^^^^^

[[Total mass and inertia matrix of the upper and lower surface materials]]


Upper and lower surface masses:

.. math::
   :label: surface_masses

   \begin{aligned}
     m_{\mathrm{u}} &= \rho_{\mathrm{u}} a_{\mathrm{u}} \\
     m_{\mathrm{l}} &= \rho_{\mathrm{l}} a_{\mathrm{l}}
   \end{aligned}


Upper and lower surface inertias:

.. math::
   :label: surface_inertias

   \begin{aligned}
     \mat{J}_{\mathrm{u}/\mathrm{O}} &= \rho_{\mathrm{u}} \mat{J}_{a_u/\mathrm{O}} \\
     \mat{J}_{\mathrm{l}/\mathrm{O}} &= \rho_{\mathrm{l}} \mat{J}_{a_l/\mathrm{O}}
   \end{aligned}

Where the :math:`a` and :math:`\mat{J}` are the areas and areal inertias for
the canopy surfaces (from :ref:`derivations:Area`).


Air mass
^^^^^^^^

[[As the canopy accelerates, the air inside must accelerate at the same rate,
and so must be included in the inertial calculations of the canopy. (This
assumes the air is incompressible, which is reasonable at these speeds, and
neglects surface porosity, so the enclosed air travels with the wing.)
Although the canopy is porous, and thus constantly receiving an inflow of air
through the intakes, the leakage is slow enough that the volume of air can be
treated as constant.]]

Mass of the enclosed air:

.. math::
   :label: air_mass

   m_{\mathrm{air}} = \rho_{\mathrm{air}} v

Inertia matrix of the enclosed air:

.. math::
   :label: air_inertia

   \mat{J}_{\mathrm{air}/O} = \rho_{\mathrm{air}} \mat{J}_{\mathrm{v}/\mathrm{O}}

Where :math:`v` and :math:`\mat{J}_\mathrm{v}` are the volume and volume
inertia for the inside the canopy (from :ref:`derivations:Volume`).


Apparent Mass
^^^^^^^^^^^^^

Newton's second law states that the acceleration of an isolated object is
proportional to the net force applied to that object:

.. math::

   a = \frac{\sum{F}}{m}

This simple rule is sufficient and effective for determining the behavior of
isolated objects, but when an object is immersed in a fluid it is longer
isolated. When an object moves through a fluid there is an exchange of
momentum, and so the momentum of the fluid must be taken into account as well.
[[FIXME: poor explanation. The "exchange of momentum" is what produces the
fluid dynamics, after all. The problem is using aerodynamics coefficients that
were produced under steady-state conditions to estimate accelerated (unsteady)
motion.]]

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
is much greater than the density of the fluid then the effect is often
ignored, but for lightweight aircraft the effect can be significant.

Because apparent mass effects are the result of a volume in motion relative to
a fluid, its magnitude depends on the direction of the motion relative to the
volume. Unlike the inertia due to real mass, apparent inertia is anisotropic,
and the diagonal terms of the apparent mass matrix are independent. [[FIXME:
it's related to this projected surface area; that's probably not obvious.]]

An exact calculation of the apparent mass for an arbitrary geometry with
respect to an arbitrary reference point is not trivial. For a classic
discussion of the topic, see :cite:`lamb1945Hydrodynamics`. A more recent
reference discussing apparent mass in the context of parafoils is
:cite:`lissaman1993ApparentMassEffects`, which used an ellipsoid model to
establish a parametric form commonly used in parafoil-payload literature. An
updated derivation in :cite:`barrows2002ApparentMassParafoils` added
corrections to the ellipsoid model.

This paper uses the method from :cite:`barrows2002ApparentMassParafoils`. For
a replication of that method for estimating the apparent mass matrix of
a parafoil, but given in the notation of this paper, see
:ref:`derivations:Apparent Mass of a Parafoil`. For the purpose of defining
a dynamics model incorporating apparent mass, the relevant detail from that
derivation is that the reference point for the dynamics must lie in the
xz-plane of the canopy.


Notes to self
-------------

* It's not correct to say that the effect becomes greater as the density of the
  vehicle decreases. Whether it is **significant** depends only on the ratio `m
  / m_a`. If :math:`m \gg m_a` then no worries.

  However, `m` does depend on the density of the vehicle, and `m_a` does depend
  on the density of the fluid. But `m_a` also depends on the shape of the
  object and the relative velocity of the fluid.

  It's not a big deal, but careful how you word it.


Suspension lines
================

* :cite:`kulhanek2019IdentificationDegradationAerodynamic`: mentions some
  papers on line drag coefficients, start here

* I'm not including explicit models for the bridle. The canopy geometry
  assumes the existence of a bridle that will produce the specified shape. At
  most, I've added control points and drag coefficients for the lines. Turns
  out it has a significant (ie, not massive but still noticeable) impact on
  sensitive things like the glide ratio.

* I'm lumping all the line drag into a single point for each half of the wing.
  I'm assuming isotropic drag because drag due to lines naturally becomes
  insignificant as alpha increases (when aerodynamic resistance in the
  z-direction becomes dominated by the canopy anyway), and the wing can't
  operate at a particularly high angle of attack anyway.


Harness
=======

* :cite:`kulhanek2019IdentificationDegradationAerodynamic`: uses Virgilio's
  presentation; I guess I'll do the same. That model treats the harness as
  a sphere with an isotropic drag coefficient normalized by cross-sectional
  area. Review the docstring for `harness.py:Spherical`.


Inertia
-------

The harness is modeled as a solid sphere of uniform density. With a total mass
:math:`m_p`, center of mass :math:`P`, and projected surface area :math:`S_p`,
the moment of inertia is:

.. math::

   \mat{J}_{p/P} =
     \begin{bmatrix}
      J_{xx} & 0 & 0 \\
      0 & J_{yy} & 0 \\
      0 & 0 & J_{zz}
     \end{bmatrix}

where

.. math::

   J_{xx} = J_{yy} = J_{zz} = \frac{2}{5} m_p r_p^2 = \frac{2}{5} \frac{m_p S_p}{\pi}

[[**FIXME**: use `p` subscript for payload? It's what I use in the code]]


Controls
--------

[[Discuss modeling weight shift as a displacement of the harness center of
mass :math:`P`]]


Aerodynamics
------------

FIXME


System models
=============

[[Models of the composite system]]


Reference point
---------------

One of the first steps in developing an aircraft dynamics model is to choose
a reference point for the translational dynamics. A common choice is the
system center of mass because it decouples the translational and angular
dynamics. For paragliders, however, the center of mass is not a fixed point
because it is not a strictly rigid body system: weight shift, accelerator, and
atmospheric air density all effect the location of the paraglider center of
mass. Also, paragliders are sensitive to apparent mass, which don't have
a single "center"; that is, there is no point that minimizes all of the terms
in the apparent inertia matrix, and there is no point that decouples the
translational and rotational terms of the apparent inertia matrix. Because the
system matrix cannot be diagonalized there is no advantage in choosing the
center of mass. Instead, the reference point can be chosen such that it
simplifies other calculations.

.. Note that the point you use for computing the dynamics can be different
   from the point you use for tracking the glider trajectory over the Earth.

As mentioned in `Apparent Mass`_, estimating the apparent mass of the canopy
is simplified if the reference point lies in the xz-plane of the wing. The
most natural choices in that plane are the leading edge of the central
section, or the midpoint between the two risers connections, which is constant
regardless of the width the riser chest strap.

This paper chooses the midpoint between the two riser connections, designated
:math:`RM`, for all dynamics equations because it is also the most natural
choice for the vehicle velocity state variable in the simulator. The reason is
that because the riser midpoint is likely to be near to where a pilot would
place their flight device, it is also the most representative of the data
measured by flight recorders, making it the most convenient point for
comparing real flight data to simulated data.

Another advantage is that the riser midpoint is typically very close to the
glider center of mass, which makes it easy to visualize the glider motion when
developing the models.


A six degrees-of-freedom model
------------------------------

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

For the derivation of the mathematical model, see :ref:`derivations:Model 6a`.


A nine degrees-of-freedom model
-------------------------------

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

[[Discuss the 7-, 8-, and 9-DoF models from literature?]]

This section develops a model with nine degrees of freedom: six for the
orientations of the body and payload, and three for the velocity of the
connection point shared by the body and payload. The body and payload are
modeled as two rigid bodies connected at the riser midpoint :math:`RM`, with
the connection modeled as a spring-damper system.

.. figure:: figures/paraglider/dynamics/paraglider_fbd_9dof.*
   :name: paraglider_fbd_9dof

   Diagram for a 9-DoF model with internal forces.

The equations of motion are developed by solving for the translational
momentum :math:`^e \dot{\vec{p}} = \sum{\vec{F}}` and angular momentum
:math:`^e \dot{\vec{h}} = \sum \vec{M}` for both bodies.

For the derivation of the mathematical model, see :ref:`derivations:Model 9a`.


Discussion
==========


Pros
----

* Somewhat mitigates the *steady flow* assumption by including apparent mass.


Limitations
-----------

* Inherits the limitations of the aerodynamics method:

  * Assumes section coefficients are representative of the entire wing segment
    (ignores inter-segment flow effects, etc)

* Rigid-body assumption (none of the canopy, connecting lines, or payload are
  actually rigid bodies)

* Violates conservation of momentum since it doesn't account for accelerations
  due to redistributions of mass (due weight shift and the accelerator).

* Quasi-steady-state assumption (I'm using steady-state aerodynamics to
  simulate non-steady conditions by assuming the conditions are changing
  "slowly enough.") I've included adjustments for apparent mass, but I'm still
  assuming the steady-state solution is representative of the unsteady
  solution. Also, my equations for the apparent mass themselves are under
  a steady-state assumption; see :cite:`thomasson2000EquationsMotionVehicle`
  for a discussion of apparent mass in unsteady flows.

  Consider the fact that the canopy is interacting with the "underlying" wind
  field, so that the motion of the canopy changes the local wind vectors. This
  effect should propagate through time, but for my simulator I'm only using
  the "global" wind field, neglecting any effects of the previous timestep. (I
  am trying to account for apparent mass, but I don't think that's really the
  same thing, since that doesn't change the local aerodynamics.)

* Barrow's method has several assumptions (circular arc anhedral, spanwise
  uniform thickness, etc) that are wrong for real wings.
