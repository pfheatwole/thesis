**************
Aircraft Model
**************


Maneuvering Target Tracking
===========================

"In manoeuvring target tracking, a primary trade-off is the robust tracking of
manoeuvres against the accurate tracking of constant velocity (CV) motion."


This is saying that you need to trade off between smooth motion accuracy (the
constant velocity notion) versus accelerated maneuvers. White noise
acceleration does provide a probability distribution with support over the
constant velocity trajectory, but random walks are likely to generate
unrealistic motion (aircraft are frequently well-described as CV, but random
walks are virtually never CV).


This is one of the different approaches I should highlight: maneuvering target
tracking might use pre-defined maneuvers (structured dynamics) or random walk
(unstructured). For example, the MH370 search used structured (pre-defined)
maneuvers, but my random walk PF will probably use unstructured (random walk)
proposals.



*********
Filtering
*********


Performance
===========


Jittering
---------

If the process noise is small, you don't get much variation in the particles
during the time update. One way to decrease the odds of sample impoverishment
is to use *jittering*. See `fearnhead1998SequentialMonteCarlo`, page 53


Design and Validation
=====================

Cramer-Rao
----------

A big design point of my filter is that I know I won't get super precise
estimates, but all I need are **sufficiently** precise estimates.

The Cramer-Rao lower bound is the theoretical lowest variance estimator of
a static parameter. In my case, the static parameters are those belonging to
the wing. Honestly though, I don't care about those nuisance parameters. What
I do care about are the dynamic thermal parameters (eg, the thermal center).
Forget whether my filter achieves the best possible estimate; does the
theoretical best possible estimate give me **sufficient** precision?

In `notter2018EstimationMultipleThermal` they investigate this question for
their multiple thermal tracking particle filter. I should review this notion
and summarize the conceptual impact on my design, even if I can't reproduce
the actual CLRB for my model. (Notice, the CLRB is typically defined for
static parameters, but Notter uses the results from
`tichavsky1998PosteriorCramerRaoBounds` to apply the concept to the dynamic
parameters of the thermal centers).

Q: doesn't the CLRB depend on the form of the likelihood function? What is the
likelihood function (aka the data distribution) for my system?

**Try to describe the likelihood function for my filter, in non-mathematical
terms.**

