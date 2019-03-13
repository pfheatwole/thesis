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

My wing geometry definitions allow for the generation of a 3D mesh suitable
for CFD, but that's beyond the scope of my project. I would love to compare
CFD methods to Phillips.

Also, my Phillips method doesn't seem to work very well. I tried to recreate
the results from :cite:`bellocWindTunnelInvestigation2015`, but I seem to be
overestimating the lift, thus significantly overestimating the wing's
performance.


.. TODO::

   * Discuss the methods for estimating the aerodynamic forces on a wing. What
     are their pros/cons; why did I choose Phillips; does my model support CFD
     methods.

   * Testing methodology: is my model correct?

   * How do you go from forces to accelerations? What about the wing's
     inertia?




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

[1]Bencatel R, de Sousa JT, Girard A. Atmospheric flow field models applicable
for aircraft endurance extension. Progress in Aerospace Sciences 2013;61:1–25.

NT


Control Sequences
=================

NT


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
