****************
Paraglider Model
****************

Key Points:

* Individual components of a paraglider

  * The physical object (describe what it is you want to model; geometry,
    materials, etc)

  * The dynamics (equations that encode the physical behavior for simulation)

* The composite model (ie, the parafoil-payload **system**)

  * There are many references on parafoil-payload systems. It would be nice if
    I can generalize them as composites of the wing + harness components
    I defined earlier.

Considerations:

* The dynamics models are required to satisfy some need. I need to establish
  the needs of each modeling component, then show that those needs are being
  met.


Simulators require dynamics models for each component, and so flight
simulators require a model of the aircraft. Although there are existing flight
simulators that include models of specific paraglider configurations, none of
those models are parametric. Performing statistical parameter estimation
requires a parametric model, so I needed to create one.

Each Paraglider model is built from two parts: a wing and a harness. (I am
neglecting to model the connecting lines from the risers to the wing.)

I started with designs from :cite:`benedetti2012ParaglidersFlightDynamics`,
and applied extensive modifications to support the needs of my thesis.


Behaviors
=========

[[I should start by discussing the behaviors I would like to capture, since
that determines things what must be modeled. Things like the degrees of
freedom, or the fact that I do not want to assume that the relative wind is
uniform (eg, when flying through a thermal).]]


Paragliding Wing
================


Physical Description
--------------------

Airfoil
^^^^^^^

The cross-sectional slices of the parafoil.

Discuss the most significant points and definitions:


Geometric definitions of the airfoil: leading edge, trailing edge, chord line,
camber line, upper surface, lower surface

Summary parameters (ref:
http://laboratoridenvol.com/paragliderdesign/airfoils.html#4): maximum
thickness, position of maximum thickness, max camber, position of max camber,
nose radius, trailing edge angle (?)

Aerodynamic behavior and coefficients: lift, drag, and moment curves; stall
point; stability; more?

In fact, a LOT of the aerodynamic terminology should probably be introduced
here (as part of the discussion on airfoils). More keywords: angle of attack,
stall point, chord, camber, pitching moment, aerodynamic center


Parafoil
^^^^^^^^

.. TODO::

   * How should I cite the "Paraglider Design Handbook"? Just as a website?


Key points: planform (flat area, flat span, etc), lobe (projected area,
projected span, **dihedral**), spanwise airfoils, washin/washout (geometric
twist)


The majority of the geometry definitions are to describe the *parafoil*.
A parafoil has a given planform, which is the projection of the wing onto the
xy-plane. The planform is then curved by the connecting lines to produce the
arched, dihedral shape of the wing. (The PDH calls the frontal view the *lobe*
and defines several lobes (circular, elliptical, double circles, etc))

The planform dimensions describe the projected outline, but not the volumetric
shape; the volumetric shape of the parafoil is dictated by its cross-sections.
A 2D cross-section of a wing is called an *airfoil*. The airfoil is the
fundamental building block of a wing. Some wings have a spanwise variation of
the airfoil in order to adjust the performance characteristics of the wing,
but my model has not yet implemented that detail.


Wing
^^^^

Parafoil + lines + risers



Mathematical Model
------------------

.. TODO::

   * Discuss the methods for estimating the aerodynamic forces on a wing. What
     are their pros/cons; why did I choose Phillips; does my model support CFD
     methods.

   * Testing methodology: is my model correct?

   * How do you go from forces to accelerations? What about the wing's
     inertia?


References:

* :cite:`phillips2000ModernAdaptationPrandtl` introduced a numerical LLT

* :cite:`hunsaker2011NumericalLiftingLineMethod` observed issues with wings
  with sweep and/or dihedral

* :cite:`chreim2017ViscousEffectsAssessment` reviewed the applicability of
  Phillips method, and confirmed the issues with sweep noted by Hunsaker

* :cite:`chreim2018ChangesModernLiftingLine` adapted Phillips method to use
  the Pistolesi boundary conditions, and verified that is was able to predict
  the section coefficients for a wing with 45-degree sweep.

* :cite:`belloc2015WindTunnelInvestigation` has actual data which I can use to
  check my equations.


Survey: what are the typical ways of estimating the aerodynamics of a wing?

* Lifting-lines

* Vortex panels

* Computational fluid dynamics


The original way to estimate the aerodynamic forces on a wing was introduced
by Prandtl. This method assumes that the quarter-chord of the wing is
a straight line with a constant airfoil. More sophisticated methods allow for
a quarter-chord that arcs in a 2D plane, but because a paragliding wing
typically has both dihedral and sweep, it requires a 3D lifting line method.
I chose a method developed by Phillips, which is essentially a vortex panel
method with a single panel.

Unfortunately, Phillips' method doesn't seem to work very well. I tried to
recreate the results from :cite:`belloc2015WindTunnelInvestigation`, but
I seem to be overestimating the lift, thus significantly overestimating the
wing's performance. Thankfully, this is not unexpected: in
:cite:`chreim2017ViscousEffectsAssessment` they investigate Phillips'
nonlinear numerical lifting line theory. He checks it for convergence and
accuracy against three wings: straight, elliptical, and swept. It converged
for the straight and elliptical wing, but not for the swept wing (so no good
data could be produced), but for the other two methods is overestimated CL for
the straight and elliptical wings. In
:cite:`chreim2018ChangesModernLiftingLine` he reintroduces the *Pistolesi
boundary condition* to mitigate the shortcomings of Phillips' method, but he
claims corrects the performance for wings with sweep; he does not test it with
wings with dihedral.

Thankfully, all this uncertainty isn't a big deal in terms of my project,
since I'm not expecting to filter true flight tracks anyway. My model is still
sufficient to demonstrate the qualitative behavior of a wing in interesting
flight scenarios, as well as for developing the infrastructure. True, the
method I implemented (Phillips) doesn't work terribly well, but my wing
geometry definitions are well suited for more sophisticated methods.
Calculating points anywhere on the wing is easy, allowing for 3/4 chord
positions (the *Pistolesi boundary condition*) for better numerical lifting
line methods (see :cite:`chreim2017ViscousEffectsAssessment`), or for the
generation of a 3D mesh suitable for computational fluid dynamics (CFD)
methods.


Scratch notes
-------------

* In `bellocWindTunnelInvestigation2015`, he works through several
  developments related to estimating the dynamics, and has a great summary in
  the introduction. In the introduction mentions that "Theoretical analysis of
  arched wings is scarce in the literature, partly because the Prandtl lifting
  line theory is not applicable to arched wings", then in his conclusion,
  "using a 3D potential flow code like panel method, vortex lattices method or
  an adapted numerical lifting line seems to be a sufficient solution to
  obtain the characteristics of a given wing". **Usable as the basis for
  choosing Phillips method (an adapted numerical lifting line)?**

* In :cite:`hunsaker2011NumericalLiftingLineMethod` they are investigating
  Phillips' method and observe that CL increases as the grid is refined.
  **This is great news since that matches my experience.** (I need to read
  that paper, but this note is taken from
  :cite:`chreim2017ViscousEffectsAssessment`, section 3.1.3 (pg 7).


Paragliding Harness
===================

This is the "payload".


Physical Description
--------------------

My current design uses a spherical approximation for the harness forces, with
the center of mass coinciding with the riser attachments, so the harness
geometry is simple. [[FIXME: this description sucks]]


Mathematical Model
------------------

NT


Parafoil-Payload System
=======================

.. TODO::

   * Discuss some of the major parafoil-payload papers and the modelling
     choices they made.

This is the combination of wing and payload (harness).

I should review existing paraglider models, including the different degrees
of freedom and what that choice implies. I should frame my new design in terms
of existing terminology to make it easier to relate.


Physical Description
--------------------

NT


Mathematical Model
------------------

NT


Performance
===========

[[

This is a **huge** topic. It's not the primary focus of my thesis, so should
I just punt it off onto "other resources", or should I detail the basic
performance characteristics with a few curves, or ...?

At the least I should probably demonstrate that my model definition satisfies
my design requirements. For example, build an example wing and show how it
behaves when flying through asymmetric wind (a big feature of my design).

]]
