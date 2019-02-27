****************
Paraglider Model
****************

NT


Geometry
========

NT


Dynamics
========

NT


*****************
Flight Simulation
*****************

NT


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
