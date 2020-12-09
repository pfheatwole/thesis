***********
Future Work
***********

.. Review the steps (from data generating to the predictive model) and
   survey the open questions / remaining work for each step.

   * Summarize the tidbits I've learned and open questions I know about?

   * Maybe call these *resources*; they're incomplete, but still useful.


Paraglider modeling
===================

* Computational improvements for the dynamics model: Even if the NLLT gives
  reasonable results, it's probably too slow to use with a particle filter.
  It'd be great to pre-process the solutions; maybe train a neural network?

* Riser-control

* Canopy distortions (mainly cell billowing, but also during weight shift,
  riser control, etc)


Flight reconstruction
=====================


Data
----

* Characterizing sensor noise (GPS, variometer)

  * Not sure how to generalize over such a wide range of tracks.

* Atmospheric parameters (air density)

* Supplementary sources

  * Topography (eg, a DEM), meteorology (eg, RASP, TherMap), related fields
    (drainage networks, flowfield tools for wind farms), etc


Filtering architecture
----------------------

* Are wind vectors independent, or do you try to fit the wind field
  regression model "on-line", and use that to inform the priors? (This would
  probably make any smoothing equations a lot more difficult.)

* What do you need for a particle filter?

  * Fundamentally, a particle filter needs two things:

    1. Proposals (dynamics model)

    2. Likelihoods (observation model)

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

* Suggest the GMSPPF?


Designing good proposals
------------------------

* Part of this goes in the filtering architecture; ideally you'd like to
  condition (or "adapt") the proposal based on the observation (more important
  as the observation becomes more informative, ie the likelihood becomes more
  peaked).

* Multivariate GP for the control inputs?

* Wind field models and/or turbulence models for wind vectors?

* Paraglider model identification (model parameter estimation). Use an
  empirical database for glider parameters?


Wind field estimation
=====================

* Estimate the underlying wind field of individual tracks (eg, fit a kriging
  model)

* Combine flights that overlap in time + space?

* Model-free or model-based?

* Constraints

  * Assume constant mean over a fixed time interval?


Wind field patterns
===================

* Choice of modeling target

  * Separate the horizontal and vertical components?

  * *Model-free* or *model-based* structure?

    Are patterns *data-driven* (using unstructured wind velocities), or do you
    try to detect and fit explicit thermal models, shear models, etc?

* Representation (Points, lines, areas, volumes? Grids or polygons?)


Predictive modeling
===================

* Given a set of wind field regression models, you need to find regions with
  overlapping observations, then look for correlations in those co-observed
  regions.

* Regional correlations must be encoded into a predictive model that can be
  queried (ie, if part of the wind field is (noisily) observed, and they have
  known correlations, the predictive model should produce estimates of
  unobserved regions)

* Ultimately, this predictive model will be useable in-flight, so as the pilot
  samples the wind field, the predictive model can suggest regions with
  desirable wind patterns.

* How to combine the set of wind field regression models into a spatiotemporal
  predictive model?

* How do you encode the patterns such that a mobile device can query them?
