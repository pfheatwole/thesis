***********
Future Work
***********

Paraglider modeling
===================

Geometry
--------

FIXME


Dynamics
--------

FIXME



Flight Reconstruction
=====================


Filtering Architecture
----------------------

* What do you need for a particle filter?

  * Fundamentally, a particle filter needs two things:

    1. Proposals

    2. Likelihoods

  * The proposal are for the state. In this case, the "state" is not just the
    state of wing, but also of the wind and control inputs. Those are
    conceptually independent systems, so really we need three proposals.

  * Proposals are generically a relationship between a current value and some
    upcoming value. The only requirement of the proposals is that they assign
    a non-zero probability to all **possible** outcomes, but the more
    accurately they capture the true transition probabilities the better the
    estimate (since you're working with a finite number of particles).

    If the transitions from state to state arise represent the evolution of
    a dynamical system, then the proposal can be formed by the dynamics of the
    system. Ideally we would we have three "true" dynamics models for the
    wind, wind, and controls, but that's beyond the scope of this paper. For
    now I'll just assume integrated white noise is satisfactory.


* What do you need for the proposal?

  * We don't know the "true" paraglider dynamics model, so we're using
    a parametric approximation of it. That lack of knowledge of the parameters
    would lead into a *parameter estimation* problem, but it's unclear if
    statistical parameter estimation is feasible. It's probably more feasible
    to crowdsource a collection of parameters that describe existing wings,
    then building an empirical distribution over parameter sets. Each set can
    be given an (empirical) weight that says how likely that wing is to have
    been flown. You'd then run the particle filter with those weighted
    parameter sets to produce a rough approximation of the joint distribution
    over states and parameters.

  * Related to the parameter estimation issue: if I'm allowing the parameters
    of the wing canopy (the "design functions") to themselves be parametric,
    then you can't assume the model is time-homogeneous. You'll need to
    specify distributions over those hyperparameters and run parameter
    estimation over that larger space, which would be a GIANT pain;
    dimensional **explosion**. Well, I guess it's better to have a model that
    *can* be that flexible even if its not feasible to utilize that
    flexibility for some tasks. And hey, at least it'd help you quantify the
    impact of those hyperparameters (ie, you can see how bad your homogeneous
    model would be if the underlying data was actually using time-varying
    parameters).

* What do you need for the likelihood?


Designing good proposals
------------------------

* Part of this goes in the filtering architecture; ideally you'd like to
  condition (or "adapt") the proposal based on the observation (more important
  as the observation becomes more informative, ie the likelihood becomes more
  peaked).




Wind field estimation
=====================

FIXME


Wind field patterns
===================

FIXME
