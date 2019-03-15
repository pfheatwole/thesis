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
