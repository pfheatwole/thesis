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
:cite:`bencatel2013AtmosphericFlowField` they identify three basic categories
of wind behavior: wind shear, updrafts, and gusts. Shear is a change in the
wind vector for a change in position, updrafts (and downdrafts) are non-zero
vertical components of the wind vector, and gusts are changes (typically
rapid, turbulent changes) to the wind magnitude and/or direction.


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
