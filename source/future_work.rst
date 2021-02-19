***********
Future Work
***********

.. Review the steps (from data generating to the predictive model) and
   survey the open questions / remaining work for each step.

   * Summarize the tidbits I've learned and open questions I know about?

   * Maybe call these *resources*; they're incomplete, but still useful.


To summarize, what are the approximate steps to go from a database of flight
tracks to a predictive model?


#. Flight reconstruction

#. Wind field reconstruction (continuous wind field regression or maybe a set
   of structured features)

#. Wind feature detection in individual tracks

#. Detecting correlations (between wind features, time, temperature, etc)

#. Encoding correlated features in a predictive model


Other:

* Data cleaning, sanitization

* Create a representative set of paraglider dynamics models

* Proposal design (wind vector dynamics, control input dynamics)

* Defining "wind features"; could be anything from an unstructured
  point-estimate of the average horizontal wind in some surface to the
  presence of more structured feature like a thermal.

* Filtering architecture (GMSPPF might be a good starting point?)

* Faster paraglider dynamics models; the NLLT is almost surely too slow;
  coefficient lookup alone is killer. Given the number of simulations that
  will likely be required for reasonable flight reconstruction accuracy,
  I suspect that using the non-linear model to generate linear or
  piecewise-linear models will be essential.



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


Data sanitization
-----------------

* [[Survey the content of an IGC file?]]

* The raw data is stored in IGC files, which must be parsed and sanitized.
  Parsing is straightforward, since the data follows a well-defined format.
  Sanitizing the data is more difficult: erratic timestamps, pressure altitude
  biases, and unknown sensor characteristics all present their own sets of
  concerns.

* Characterizing sensor noise (GPS, variometer)

  * Not sure how to generalize over such a wide range of tracks.

* Atmospheric parameters (air density)

* Supplementary sources

  * Topography (eg, a DEM), meteorology (eg, RASP, TherMap), related fields
    (drainage networks, flowfield tools for wind farms), etc

* Should I discuss the error between the GNSS and pressure altitude to segue
  into atmospheric parameter estimation? I like the idea of surveying the data
  first: a "first pass" look at the data. Acknowledge the questions and issues
  in the introduction


Atmospheric Parameters
----------------------

The IGC files record altitude using two different measurements: one from the
GNSS device, one from barometric pressure. The GNSS altitude is an estimate of
the current geometric altitude. The pressure altitude is the altitude at which
the atmospheric pressure would match the currently observed conditions under
international standard atmospheric (:term:`ISA`) conditions.

You can use the relationship between pressure and altitude to estimate the
current atmospheric parameters:

.. math::
   :label: pressure_to_altitude

   h = \frac{T_0}{L} \cdot \left( 1 - {\left( \frac{p}{P_0} \right)}^\frac{LR}{Mg} \right)

Because the pressure altitude converts pressure to altitude while assuming ISA
conditions, non-ISA conditions will produce a variometer bias
:math:`\epsilon_v = z_\textrm{GNSS} - z_\textrm{vario}`. The bias can be
positive or negative, depending on atmospheric conditions. In general, if the
air temperatures are higher than 19°C (ISA temperature) the pressure altitude
will be lower than GNSS altitude, but alignment also depends on atmospheric
pressure and lapse rate.

.. figure:: figures/data/vario_gnss_bias.*

   GNSS versus pressure altitude.

Because the relationship between pressure and altitude in
:eq:`pressure_to_altitude` is non-linear, the bias is a function of altitude.
The relationship is an exponential (FIXME: I think this claim is valid?) so
fitting an exponential bias should work, but a more robust solution is to fit
the atmospheric parameters themselves.

The parameter estimation problem is more difficult because the GNSS and
variometer measurements are often out of alignment. GNSS tracks commonly
experience a time delay that depends on the device and atmospheric conditions.

.. figure:: figures/data/vario_bias_with_sequence_alignment.png
   :width: 90%

   Variometer bias as a function of altitude.

First with the raw sequences, which exhibits variable bias depending on GNSS
delay (exacerbated in regions of rapid ascent or descent), and again after
performing sequence alignment.


Parameter Estimation
^^^^^^^^^^^^^^^^^^^^

.. FIXME: should I use the `align*` or `aligned` environment?

.. math::
   :label: stochastic_pressure_to_altitude

   \begin{aligned}
   h &\sim \mathcal{N}(\mu_h, 2)                                                          &\mathrm{m}\\[1.0ex]
   \mu_h &= \frac{T_0}{L} \cdot \left( 1 - {\left( \frac{p}{P_0} \right)}^{LR/Mg} \right) &\mathrm{m}\\[1.0ex]
   T_0 &\sim \mathcal{N}(288.15, 10)                                                      &\mathrm{K}\\[1.0ex]
   L &\sim \mathcal{N}(0.0065, 0.003)                                                     &\mathrm{K \cdot m^{-1}}\\[1.0ex]
   P_0 &\sim \mathcal{N}(1013.25, 15)                                                     &\mathrm{hPa}\\[1.0ex]
   R &\equiv 8.3144598                                                                    &\mathrm{J \cdot K^{-1} \cdot mol^{-1}} \\[1.0ex]
   M &\equiv 0.0289644                                                                    &\mathrm{kg \cdot mol^{-1}}\\[1.0ex]
   g &\equiv 9.80665                                                                      &\mathrm{kg \cdot m \cdot s^{-2}}
   \end{aligned}


In :eq:`pressure_to_altitude` I do stuff.

TODOs:

* Use the Turkey tracks to show how the bias is a function of altitude

* Plot the priors

* Plot the posterior for several of the Greece tracks and observe that
  although they are very precise (small posterior variance) they don't agree
  with each other (suggesting some devices may have systematic biases/errors?)


Using probability and simulation to deal with missing data
----------------------------------------------------------

[[Yoinked from the eliminated "Flight reconstruction" chapter]]

* Unfortunately, the paraglider dynamics depend on more unknowns that just the
  wind, so reconstructing the wind vectors amounts to reconstructing the
  complete state trajectory.

  The system as-is is indeterminate: with no constraints on the value of the
  control inputs and wind vectors there are no constraints on the paraglider
  state. The "answer" could be anything.

  The underlying problem is uncertainty: uncertain variable values, uncertain
  model dynamics, and uncertain measurements. Logical reasoning in
  indeterminate systems requires probability theory. Instead of seeking
  **exact** answers, the "solution" to the inverse problem is to estimate
  entire probability distributions over **all** possible answers.

  The question is no longer "can we compute the answer" but "how well can we
  constrain the range of plausible answers". There might not be enough
  information to constrain the wind vectors; hard to tell at this point.

  Should I introduce underdetermined systems, and discuss stochastic equations
  as underdetermined systems?]]

* "The idea of using the math of probability to represent and manipulate
  uncertainty is commonly referred to as *Bayesian statistics*"
  (`schon2018ProbabilisticLearningNonlinear`). Bayesian statistics is
  a framework for reasoning through conditional probability.

* At this point it can be helpful to rewrite our problem statement in
  probabilistic terms.

* Our original goal of estimating the wind vectors given the observed data is
  equivalent to saying we need to estimate the probability distribution over
  wind vectors given the data, written as :math:`p\left( wind \given data
  \right)`.

* This distribution by itself is intractable, which is what motivated our need
  to model the *data-generating process*. We introduced the paraglider
  dynamics in order to establish the relationship between position and wind,
  but those dynamics depend on more than just the wind vectors: they also
  depend on the pilot control inputs, air density, and the design of the wing
  itself. Thus, solving this inverse problem means we need to estimate more
  than just the wind vectors: we need estimates for the entire set of inputs.

* Those additional quantities are commonly referred to as *nuisance
  variables*, since they are not (explicitly) of interest to our problem,
  nevertheless they are necessary to compute our goal.

* [[find :math:`p \left( wind \given data \right)` by estimating the full
  joint pdf then marginalizing the *nuisance variables*]]

* We can't estimate the full joint pdf directly since it's also intractable,
  but thankfully the process model satisfies the *Markov property*. *Markov
  processes* are intuitive to represent as a state-space model. State-space
  models can be used to decompose the joint pdf into independent factors which
  a be estimated recursively to build up the full joint distribution.

* The objective now is to use the state-space model to build up the full joint
  distribution so we can marginalize the nuisance variables in order to
  compute :math:`p \left( wind \given data \right)`.

* [[The state-space model is a system of equations. In theory, we would like
  to invert them (solve for the unknown), but that's not possible here (too
  many unknowns, too complicated, etc). What's more, even if we knew the wind
  vectors and control inputs, the inverse probably doesn't even exist: it's
  pretty unlikely that this is a 1:1 function. Instead, we must be content
  with using the *forward dynamics* to generate a weighted set (a
  distribution) of possible solutions.]]


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
