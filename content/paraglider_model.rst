****************
Paraglider Model
****************

Key Points:

* Components of a paraglider

* Physical model (geometry)

* Dynamics model

Considerations:

* The dynamics model is required to satisfy some need. I need to establish the
  needs of the model, then show how those needs are being met.


Flight simulations require a model of the aircraft. Although there are flight
simulators that include models of specific paraglider configurations, none of
provided parametric models. Performing statistical parameter estimation
requires a parametric model, so I needed to create one.

I started with the design from
:cite:`benedetti2012ParaglidersFlightDynamics`, and applied extensive
modifications to support the needs of my thesis. This model combines two
components: the wing and the harness.

My current design uses a spherical approximation for the harness forces, with
the center of mass coinciding with the riser attachments, so the harness
geometry is simple. [[FIXME: this description sucks]]

Each Paraglider model is built from two parts: a wing and a harness. (I am
neglecting to model the connecting lines from the risers to the wing.)


Wing Geometry
=============

The majority of the geometry definitions are to describe the *parafoil*.
A parafoil has a given planform, which is the projection of the wing onto the
xy-plane. The planform is then curved by the connecting lines to produce the
arched, dihedral shape of the wing.

The planform dimensions describe the projected outline, but not the volumetric
shape; the volumetric shape of the parafoil is dictated by its cross-sections.
A 2D cross-section of a wing is called an *airfoil*. The airfoil is the
fundamental building block of a wing. Some wings have a spanwise variation of
the airfoil in order to adjust the performance characteristics of the wing,
but my model has not yet implemented that detail.


Dynamics
========

Primary sources: bellocWindTunnelInvestigation2015,
phillipsModernAdaptationPrandtl2000


Source notes:

* In `bellocWindTunnelInvestigation2015`, he works through several
  developments related to estimating the dynamics, and has a great summary in
  the introduction. In the introduction mentions that "Theoretical analysis of
  arched wings is scarce in the literature, partly because the Prandtl lifting
  line theory is not applicable to arched wings", then in his conclusion,
  "using a 3D potential flow code like panel method, vortex lattices method or
  an adapted numerical lifting line seems to be a sufficient solution to
  obtain the characteristics of a given wing". **Usable as the basis for
  choosing Phillips method (an adapted numerical lifting line)?**


What are the typical ways of estimating the aerodynamics of a wing?

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
:cite:`chreim2018ChangesModernLiftingLine` he reintroduces the Pistolesi
boundary condition to mitigate the shortcomings of Phillips' method, but he
claims corrects the performance for wings with sweep; he does not test it with
wings with dihedral.

Thankfully, all this uncertainty isn't a big deal in terms of my project,
since I'm not expecting to filter true flight tracks anyway. My model is still
sufficient to demonstrate the qualitative behavior of a wing in interesting
flight scenarios, as well as for developing the infrastructure. True, the
method I implemented (Phillips) doesn't work terribly well, but my wing
geometry definitions are well suited for more sophisticated methods.
Calculating points anywhere on the wing is easy, allowing for 3/4 chord
positions (Pistolesi boundary condition) for better numerical lifting line
methods (see :cite:`chreim2017ViscousEffectsAssessment`), or for the
generation of a 3D mesh suitable for CFD.



Literature Review
-----------------

* :cite:`phillips2000ModernAdaptationPrandtl` introduced a numerical LLT

* :cite:`hunsaker2011NumericalLiftingLineMethod` observed issues with wings
  with sweep and/or dihedral

* :cite:`chreim2017ViscousEffectsAssessment` reviewed the applicability of
  Phillips method, and confirmed the issues with sweep noted by Hunsaker

* :cite:`chreim2018ChangesModernLiftingLine` adapted Phillips method to use
  the Pistolesi boundary conditions, and verified that is was able to predict
  the section coefficients for a wing with 45-degree sweep.


.. TODO::

   * Discuss the methods for estimating the aerodynamic forces on a wing. What
     are their pros/cons; why did I choose Phillips; does my model support CFD
     methods.

   * Testing methodology: is my model correct?

   * How do you go from forces to accelerations? What about the wing's
     inertia?


Scratch Notes
-------------

In :cite:`hunsaker2011NumericalLiftingLineMethod` they are investigating
Phillips' method and observe that CL increases as the grid is refined. **This
is great news since that matches my experience.** (I need to read that paper,
but this note is taken from :cite:`chreim2017ViscousEffectsAssessment`,
section 3.1.3 (pg 7).
