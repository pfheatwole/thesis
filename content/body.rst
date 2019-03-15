****************
Paraglider Model
****************

Flight simulations require a model of the aircraft. Although there are flight
simulators that include models of specific paraglider configurations, none of
provided parametric models. Performing statistical parameter estimation
requires a parametric model, so I needed to create one.

I started with the design from :cite:`benedettiParaglidersFlightDynamics2012`,
and applied extensive modifications to support the needs of my thesis. This
model combines two components: the wing and the harness.

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
recreate the results from :cite:`bellocWindTunnelInvestigation2015`, but
I seem to be overestimating the lift, thus significantly overestimating the
wing's performance. Thankfully, this is not unexpected: in
:cite:`chreimViscousEffectsAssessment2017` they investigate Phillips'
nonlinear numerical lifting line theory. He checks it for convergence and
accuracy against three wings: straight, elliptical, and swept. It converged
for the straight and elliptical wing, but not for the swept wing (so no good
data could be produced), but for the other two methods is overestimated CL for
the straight and elliptical wings. In
:cite:`chreimChangesModernLiftingLine2018` he reintroduces the Pistolesi
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
methods (see :cite:`chreimViscousEffectsAssessment2017`), or for the
generation of a 3D mesh suitable for CFD.



Literature Review
-----------------

* :cite:`phillipsModernAdaptationPrandtl2000` introduced a numerical LLT

* :cite:`hunsakerNumericalLiftingLineMethod2011` observed issues with wings
  with sweep and/or dihedral

* :cite:`chreimViscousEffectsAssessment2017` reviewed the applicability of
  Phillips method, and confirmed the issues with sweep noted by Hunsaker

* :cite:`chreimChangesModernLiftingLine2018` adapted Phillips method to use
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

In :cite:`hunsakerNumericalLiftingLineMethod2011` they are investigating
Phillips' method and observe that CL increases as the grid is refined. **This
is great news since that matches my experience.** (I need to read that paper,
but this note is taken from :cite:`chreimViscousEffectsAssessment2017`,
section 3.1.3 (pg 7).



*****************
Flight Simulation
*****************

Flight simulation is essentially the generation of a time series of model
states. You define the model state and control inputs, then use the model
dynamics to iteratively update the state. 

Simulated flights are essential for testing the [[accuracy/correctness]] of an
aircraft model.

They are also essential for testing flight reconstruction algorithms: unlike
real flight data, which has many unobserved variables, a simulated flight has
access to the entire state space. This allows you to verify how well
a reconstructed flight matches the "true" state. It isn't perfect, of course:
just because you can reconstruct a simulated flight doesn't mean the method
will work on real flights, but if it fails on simulated flights then you can
be sure it will also fail on real flights.

To generate interesting test flights, you need interesting flight conditions,
where "interesting" may refer to the wind, or pilot inputs, or both. This
chapter is a cursory overview of those "interesting" scenarios.


Wind Fields
===========

bencatelAtmosphericFlowField2013

The most basic wind field is still air. Another basic test case is a uniform
wind field, where the wind vectors are the same everywhere; the uniform wind
field is useful to verify glider performance (a 360 turn in a non-zero wind
field should produce a drifting helix, not a circle).

The more interesting scenarios are where the wind vector is variable in time
and/or space. Although real wind conditions are complex and variable, for
testing purposes it is useful to focus on specific features. In
:cite:`bencatelAtmosphericFlowField2013` they
identify three basic categories of wind behavior: wind shear, updrafts, and
gusts. Shear is a change in the wind vector for a change in position, updrafts
(and downdrafts) are non-zero vertical components of the wind vector, and
gusts are changes (typically rapid, turbulent changes) to the wind magnitude
and/or direction.


Control Sequences
=================

A paraglider has only a few formal control inputs: a left and right brakes, an
accelerator (or "speed bar"), and weight shifting.

Braking
-------

[[What happens as a you apply a single brake? Asymmetric brakes? Symmetric
brakes?]]


Accelerating
------------

[[What happens when you press the accelerator?]]


Weight Shifting
---------------

[[What happens during weight shifting?]]



Simulator
=========

NT


*********************
Flight Reconstruction
*********************

* Define the state

* Define underdetermined systems

* Define probabilistic methods / simulation-based filtering


Particle Filtering
==================

Designing a particle filter requires designing the prior, likelihood, and
state dynamics, right? So I've got model dynamics (how the wing is moving
through the air), control "dynamics" (how the set of control inputs is likely
to be changing in time; eg, it's unlikely for speedbar to go from 0% to 100%
in 0.25sec, and unlikely that it's changes are white noise), and wind dynamics
(again, white noise seems unnecessarily imprecise; the wind fluctuates
quickly, but not instantaneously).

TODO: for a self-check, write out the basic set of particle filter equations


***************
Data Processing
***************

Given a working particle filter, you can perform flight reconstruction on
actual flights. But first you need to parse and sanitize the flight data.


* Sanitize the timestamps

* Check the GPS noise model (Chi^2 test)

* Debias the variometer data (via dynamic time warping or similar)

* Estimate atmospheric conditions (air density in particular)


******************
Pattern Extraction
******************

Given a set of flights, look for patterns that would be useful to pilots. I'm
hoping that neighboring regions will be correlated, meaning they can be used
to predict each other.

Each flight is an observation of a subset of the true wind field. [[They can
be aggregated?]] Pattern detection requires that sections of the wind field
follow repeatable wind configurations.

Finding correlations between regions requires a large number of pairwise
observations.

The wind field changes over time, so flights need to be aggregated by time
(open problem; group they by hour?).


****************
Predictive Model
****************

Combine the set of wind patterns into a predictive model that can be queried
by inputting the current time, position, and wind estimates.


Model Encoding
==============

To be useable using an in-flight device with no access to cellular network,
the model must be self-contained, and it must meet the storage and computation
constraints of a low-power embedded device. How the model is encoded is
fundamental to how it is queried. [[Is it though? On-disk encoding isn't
necessarily the same as the in-memory representation; granted though, the
advantage of what I was doing was to make the on-disk model be compact and
directly queriable without loading it into memory.]]
