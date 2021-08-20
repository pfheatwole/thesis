************
Introduction
************


Scratch 2021-08-21
==================

**I need an introduction that previews what I did, and why it's important.**


What's wrong with my current introduction? It overemphasizes the details of
flight reconstruction. Flight reconstruction is part of the "solution" step to
the problem of estimating wind vectors from position data, but that's it.


Recall, three steps to an intro:

1. The context

   I want to estimate wind vectors from flight tracks, but they only record
   position data.

2. The problem and its significance

   I need a causal model to link the position data to wind vectors. That
   causal model takes the form of a paraglider dynamics model. (At this point
   I can link to an appendix discussing flight reconstruction. I can mention
   the MH370 paper here, or later on in that flight reconstruction appendix.)

   So, the "problem" is that I need a **distribution** of paraglider dynamics
   models, which would be a significant because it would enable flight
   reconstruction.

3. The response

   So key details of my response:

   * The dynamics models must be capable of representing "typical flight
     conditions"

     * In terms of physical model, that means it must support the most common
       control inputs.

     * In terms of aerodynamics that means wing rotation, indirect thermal
       interactions, relatively high angles of attack, etc

   * Need to generate MANY models, either programmatically or from minimal
     specification data




* What did I do? I created a causal paraglider model for flight simulation.

* Why do you need a causal model? For flight reconstruction.

* What is flight reconstruction? In this case, it means inferring
  a distribution over unobserved variables.

* What's wrong with existing causal models?

  * Simplistic aerodynamics (linear models, no concept of stall)

  * Longitudinal models only (don't support wing rotation)

  * Assume uniform wind (can't detect indirect thermal interactions)

  * Limited control inputs (at best they support left and right brakes; I also
    need accelerator and weight shift, those are too common to ignore)

  * "They assume the dynamics are already known." Such as? Like, they assume
    the complete wing aerodynamic coefficients are known?

* So, given those limitations, what did I want?

  * Non-linear aerodynamics 

  * Non-uniform wind (what happens when a paraglider interacts indirectly with
    a thermal)

  * Graceful degradation near stall

* I don't need a model of a single wing. I need a model of many wings. They're
  time consuming to create, so the creation process should be streamlined.
  Especially given the limited amounts of data available.

  I wanted to **make it easy to produce paraglider models from minimal data
  that achieve my performance goals**.

  The approach I chose was *parametric modeling*.





Introduction overview
=====================

* Pilots use information about the wind field to plan their flights

* They can get information about the wind field by observing the environment,
  but they can also get information from wind patterns (recurring structure in
  the wind field)

* <Talk about the benefits of wind patterns, and discuss problems of discovery
  and use>

* Learning wind patterns automatically from flight data would have benefits
  for the problems of discovery and use

  <Discuss the how and why of learning patterns from data>

* Before you can learn **recurring** structure from flight data, you need to
  be able to estimate the structure for each individual flight. This is
  difficult because flight data only contains position information.

  There are existing tools to estimate wind field structure from position
  data, but they are limited since they don't know the wind vectors.

  Instead of relying on heuristics (which require explicit motion patterns and
  can only detect specific, predefined structures), it would be better to
  start by estimating the wind vectors, use them to estimate the underlying
  wind field, and then use it to "detect features" (scare quotes because I'm
  leaving the definition of a "feature" vague; once you have the wind field
  it's up to the designer to decide what "feature" means)

* Estimating the wind vectors requires full-on *flight reconstruction*


Wind field reconstruction XXX
=============================

[[These will be confusing because I redefined "wind field reconstruction".]]

How would wind field reconstruction help discover wind patterns?

  * Provide uncertainty quantification (heuristics are like point estimates;
    they average over entire regions).

    [[You could technically add uncertainty quantification to heuristic-based
    detectors, but what would those probability distributions be? (What's the
    prior over the existence of a feature at a particular point? What's the
    prior over the explicit glider path? Etc.) It's easier to place vague
    priors over the wind field and paraglider dynamics than to place them over
    individual features.]]

  * Feature detection is simpler and more reliable. It's easier to extract
    features directly from the wind field instead of relying on hard-coded
    patterns in the paraglider's motion.

  * Enable spatially-distributed structure

    * Point predictions can be useful summaries of the wind field, but they
      can't capture a lot of interesting structure.

    * Pilots are interested in **everything** related to wind velocity: shear,
      venturi, dangerous blowback areas, expected wind velocity (useful for
      planning distances)

    * It's a lot easier to summarize spatially-distributed structure if you
      have the actual wind field instead of having to code up some motion
      signature to detect it. Stay as general as possible when estimating the
      vectors.

* How would wind field reconstruction help use wind patterns?

  * Predictions can be conditioned on the actual state of the wind field
    instead of the presence/absence of detected features.

    [[This is vague: in a sense, a "feature" is simply some predefined
    structure, which you'd still need to detect. This just makes it easier?]]

    With access to the causal wind field, a predictive model can condition its
    predictions on the state of the wind field, so on-line predictions can try
    to match the current state of the world. **Predictive models are MUCH more
    useful if they can condition on observations of the current (or
    forecasted) wind field.**

    [[FIXME: you could technically condition patterns based on whether other
    patterns were detected; I don't think this changes that. The more
    important part is probably that feature detection is more reliable, thus
    conditioning based on feature detection is more reliable.

    Maybe it'd be better to argue that making it easier to produce structure
    summaries you'd have more opportunities for conditioning variables.]]


Related Works
=============

[[This seems too broad to put up front; I do love papers with these sections,
but I suspect it'd get unwieldy very fast if I put this discussion here.]]


* Wind estimation

  * Offline wind estimation / Learning from flight databases

    * :cite:`ultsch2010DataMiningDistinguish`

    * :cite:`vonkanel2010ParaglidingNetSensorNetwork`

  * Online wind estimation

    * :cite:`vonkanel2011IkarusLargescaleParticipatory`

    * :cite:`wirz2011RealtimeDetectionRecommendation`

    * :cite:`kampoon2014WindFieldEstimation`

* State estimation

  * :cite:`mulder1999NonlinearAircraftFlight`

* Applications of a predictive wind model

  * Flight reconstruction

    * Malaysian Airlines Flight 370, "Bayesian Methods in the search for
      MH370" (:cite:`davey2016BayesianMethodsSearch`)

    * Flight reconstruction of a tethered glider:
      :cite:`borobia2018FlightPathReconstructionFlight` (is this actually
      flight **path** reconstruction?)

  * Path planning during a flight

    * :cite:`menezes2018EvaluationStochasticModeldependent`: flight planning
      with environmental estimates. Might have some useful overlap for how
      I frame the tasks of this paper.

    * :cite:`lawrance2011PathPlanningAutonomous`

    * :cite:`lawrance2011AutonomousExplorationWind`

    * :cite:`lawrance2009WindEnergyBased`

  * Input estimation

    * :cite:`kampoon2014WindFieldEstimation`



SCRATCH
=======

* Should I differentiate *estimating* the state of an **observed** region
  versus *predicting* the state of an **unobserved** region? I'm using them in
  a more general sense than their definition in time-series analysis.

* [[Existing, heuristic-based tools don't have access to the wind field, which
  means they can't condition predictions based on the state of the wind field.
  Instead, they can only condition on crude measurements like the season or
  time of day, which can result in simplistic predictions that are simple
  "average" configurations averaged over arbitrary time intervals.

  In a sense, the model is marginalizing over the unspecified inputs. Existing
  models don't take observations of the wind field into account, so they're
  effectively marginalizing over **all possible conditions** to produce an
  average. (Or something like that.)]]

* People are already predicting aspects of the wind field structure from
  data (eg, thermal maps). **This is to do is qualitatively different from
  conditioning on things like "month". This section must communicate that.**

  I must contrast my approach with existing methods that "learn from flight
  data", like the thermal maps. Those are *model-free* methods
  (kinematic-based filtering), I'm focusing on *model-based* methods.

  (Related: "data driven" vs "model driven", from "Probabilistic forecasting
  and Bayesian data assimilation" (Reich, Cotter; 2015). Also, page 549 of
  "Statistical Rethinking" (McElreath; 2020), which is discussing the problem
  of using noisy data to predict future data (like simple ARMA models do,
  thus propagating measurement error into the prediction.)

  Another difference: I think the flight-based maps average over all flights
  (possibly segmented by month/season). I'm interested in a predictive model
  that can condition the prediction based on current conditions; for that you
  need individual patterns, not a simple average.

* My intermediate objective is *model-based* filtering to estimate the
  underlying wind field. (*Model-based* methods can dramatically outperform
  *model-free* methods such as kinematics-only Kalman filters).

  Model-free methods like "paragliding thermal map" tend to just show
  "pilots found lift near the ridge, and sink over bodies of water".
  Interesting, but ultimately **not very informative**, because that
  information is already encoded in heuristics that pilot's already know: lift
  along ridges, sink over bodies of water.

  Worse, they neglect the fact that a paraglider can be ascending in sink
  (under weird conditions), or descending in lift. This makes the "data" far
  too noisy; you could fix this by averaging if you had a ton of observations,
  but you don't: each observation is precious.

* Interesting: you can think of the methods that are simple averages over
  a time interval as a prior for the wind field during that interval. I'm just
  wanting to take it further and condition that prior (to get the posterior).
  I think that's kinda what he means on page 171 (182) of "Probabilistic
  forecasting and Bayesian data assimilation" when he mentions "model-based
  forecast uncertainties taking the role of prior distributions"


* The fact that the solution involves a distribution over all possible
  solutions highlights the fact that the question is not "can I produce an
  estimate of the wind vectors?" to "can I produce a **useful** estimate of
  the wind vectors?"

  For example, if no information at all is given, a wind speed estimate of
  "between 0 and 150 mph" is likely to be correct, but it is not useful. If
  a pilot is told that a paraglider is currently flying, then with no
  further information they can still make reasonable assumptions about the
  maximum wind speed, since paragliding wings have relatively small
  operating ranges. If you told them the pilot's position at two points
  close in time, they can make an even better guess of the wind speed and
  a very rough guess about the wind direction. Intuitively, this is an
  "eliminate the impossible" approach: by assuming some reasonable limits on
  the wind speed and wing performance you can improve the precision of the
  estimate.

  The key frame of mind for this project is that the question is not "can you
  produce an estimate the wind from position-only data?", but rather "how
  **how good** of an estimate of wind is possible from position-only data?" An
  estimate doesn't need to be especially precise in order to be useful to
  a pilot who is trying to understand the local wind patterns.

* The fundamental idea of this project is to augment a tiny amount of flight
  data with a large amount of system knowledge. Related to this idea is
  *model-free* vs *model-based* methods: if you have information about the
  target, use it. This project has many components, and each component needs
  a model; conceptually you can start with *model-free* methods for everything
  and replace them with *model-based* ones. (I'm not sure if kinematics-only
  models would fall under model-free or not...)

  From :cite:`li2003SurveyManeuveringTarget`: "a good *model-based* tracking
  algorithm will greatly outperform any *model-free* tracking algorithm if the
  underlying model turns out to be a good one". (See also
  :cite:`li2005SurveyManeuveringTarget` for more discussion of this notion?)


* Managing uncertainty through Bayesian statistics

  *Bayesian statistics* is a theoretical framework that interprets statements
  of *probability* as statements of ignorance; probability represents the
  *degree of belief* in some outcome. It uses the rules of probability to
  relate uncertain quantities and to quantify the "state of ignorance" of the
  result.

  You don't produce "best guess" point-estimates, you produce an entire
  distribution over all possible values. The question is not "can I produce
  **an** estimate?" but rather "can I produce a **useful** estimate?" You can
  always produce an answer, but it's only useful if the probability mass is
  spread over a useably small range of outcomes.

* Dealing with the underdetermined system via simulation-based methods

  * Producing the distribution over possible outcomes requires first producing
    the set of possible outcomes and then assigning weights (probabilities) to
    each outcomes. Generating the outcomes requires a relationship between the
    data (the flight track) and the outcomes (the wind vectors). The
    relationship between the paraglider position and the wind is provided by
    the paraglider dynamics.

  * A difficulty with this approach is that the paraglider dynamics rely on
    not only the wind vectors, but also on the wing dynamics, orientation, and
    pilot controls. Because those values were not recorded, they are not
    present in the observational data, which means this *inverse problem* must
    deal with a highly underdetermined system of equations. In the terminology
    of statistics, this means the wind vectors are not *identifiable*: there
    are many different flight scenarios that could explain the observed data.
    The wind cannot be determined without knowledge the wing behavior and
    control inputs, which means that *simulation-based filtering* methods are
    required.

    [[What about PVA approaches that ignore the relative wind, such as Michael
    von Kaenel's thesis?]]

    [[Useful paragraph, but it doesn't explain how you solve it. This is
    basically arguing (again) that you need a distribution over outcomes, but
    that wasn't suppose to be the point of this paragraph. It was supposed to
    be about highlight the fact that you utilize the relationship between the
    flight track and the wind vectors you need more information, and that
    information comes from simulations. You don't care about the simulations
    themselves (they're nuisance parameters), you just care about getting that
    sweet distribution over the wind vectors.]]

  * The essence of simulation-based methods is to explore the possible true
    state by utilizing a large set of guesses, called *proposals*. Each
    proposal is a possible value of the current state, and each proposal
    receives a score, called a *weight*, according to how well they explain
    the observations. Although there is no closed form probability
    distribution for these guesses, by making a large number of guesses you
    can arrive at an empirical probability distribution over solutions of the
    system state at each point in time. The precise state of the system is
    still unknown, but the set of possible solutions may be bounded enough to
    be useful.

  * Given a complete set of dynamics (for the wing, pilot controls, and wind),
    you can generate simulated flight trajectories.

* Approximating the missing dynamics through a parametric model (enables
  parameter estimation or empirical approximations of wing models)

  * The great difficulty with model simulations is that they require equations
    that encode the model dynamics. Aerodynamics are non-trivial in even the
    most simple applications, and paragliders are particularly challenging
    aircraft to analyze due to their curvature and flexibility. In addition to
    the aerodynamics, the paraglider models themselves are uncertain, since
    the wing specifications are generally unknown for any given recorded
    flight; instead of a single, exactly-defined model, you need a parametric
    model that can be configured to match the unknown wing. Because the wing
    configuration is unknown, this estimation problem must be applied to not
    only the system state, but to the model parameters as well (also known as
    a *dual estimation problem*).


*********************
Flight Reconstruction
*********************

* [[Should I preview how to use the recursive filtering equation to solve the
  filtering problem? If you can't invert the dynamics you have to rely on
  sequential state estimation via forward simulation.

  Solving a filtering problem requires a filtering architecture, which is
  beyond the scope of this paper, although I'll probably mention it in the
  "Future Work" chapter. ]]


* This paper only provides a parametric paraglider dynamics model. The rest of
  the flight reconstruction problem is left as "Future Work".

  There's a lot left to do (choosing a filtering architecture, designing
  proposal distributions, cleaning the data, etc), but the starting point is
  the dynamics model of the data-generating process, and that's what this
  paper provides.

  Importantly, the dynamics model is parametrized by the glider design.
  Because we don't know what glider is being flown, we need to simulate
  a variety of wing configurations. You can do that statistically as part of
  the filtering process (*parameter estimation*), but more likely we'll need
  to generate an empirical distribution over the wing parameters (a
  "representative set of wings") and draw simulations from that instead.

* When designing the state-space model system dynamics, maybe refer to
  :cite:`mcelreath2020StatisticalRethinking`? Great discussion of this in
  Sec:16.2.4. Also in Sec:16.4 he discusses "geocentric" models, such as ARMA,
  which might be useful. Kinematic models explain *what* happens, not *why*;
  my model must understand the why (the aerodynamics).


Subtask breakdown
=================

The motivating question is "how to predict the current wind field given
observations of previous wind configurations?" Before you can build a model
for the current wind field, you need to estimate the previous wind fields.
Estimating the previous wind fields requires observations of each field, which
requires generating estimates of the wind velocities present during the
recorded flights. The path forward then becomes:

1. Estimate the wind vector sequences given the position vector sequences.

   You're estimating wind as a function of time, but only at discrete times.

   :math:`w_{1:T} \sim p\left( w_{1:T} \given r_{1:T} \right)`

   This can be computed from the output of the "flight reconstruction" step.
   First, flight reconstruction estimates the joint probability distribution
   over the wind, paraglider model, and pilot inputs. Then, the posterior over
   the wind vectors can be computed from the joint distribution by
   marginalizing over paraglider model, state, and controls.

   How you implement this depends on whether you assume the wind vectors are
   either independent (ie, :math:`w_t \,\bot\, w_{0:t-2} \,|\, w_{t-1}`). You
   could conceivably build the regression model over `w` as you go (so if you
   visit an area, leave, and return relatively soon you might want to use the
   wind vector estimate from the prior visit), but that'd be **significantly**
   more complex.

2. Build wind field regression models

   Modeling considerations at this stage:

   * Real wind fields vary over time. How will the model capture that
     variability? It could appear as an explicit parameter of the regression
     model (so the regression model is a time-varying spatial function), or it
     could appear in the indexing scheme for the set of regression models (so
     each day is split into time intervals and a regression model is fitted to
     each interval).

   * Wind fields vary considerably with altitude. For the purposes of
     predictive modeling, aircraft height above ground level (AGL) may be
     a better predictor than the absolute altitude.

   * How should the spatial correlations be handled? The wind field is
     a spatial function, and some points in the field with be known with much
     greater certainty than others, so the uncertainty must include spatial
     variability as well. The traditional method for placing a distribution
     over spatial functions is to use a Gaussian process, so the choice of
     modeling spatial correlations equates to choosing a proper kernel
     function.

3. Build a predictive model from the set of regression models

   This model will try to match new observations against the set of fitted
   regression models. Because of the computational complexity involved with
   evaluating the full regression models, this step will likely require (at
   least) two sub-steps:

   1. Extract a set of high-confidence patterns from the regression models.
      (There's no point calculating low-probability estimates, so record
      strongly correlated areas and discard the rest.)

   2. Select patterns that match the current observations


Brief probabilistic development
===============================

The long-term objective of this project is to learn wind patterns from
recorded flights, but the more fundamental problem is how to estimate the wind
field from an individual flight. Each step of the process follows the same
formula: how can we use relationships to things we know to estimate
something we don't know? This section develops these questions by rewriting
them in mathematical terms, letting the needs of the math guide the process.

To begin, our initial problem statement is to "estimate the wind field present
during a paraglider flight". In mathematical form, we want to know the value
of the wind field:

.. math::

   \mathcal{W}

Because precise knowledge is impossible, we must be content with an estimate.
To quantify the inherent uncertainty in our estimate we must invoke the
language of probability, so our new objective is to "estimate the probability
distribution over the wind field:

.. math::

   p \left( \mathcal{W} \right)


[[Wait, this looks like a probability distribution over the models. Shouldn't
it be more like :math:`\mathcal{W} = p(w(r))` (not sure how to write "the
probability of wind vector `w` as a function of position `r`").

How do Gaussian processes write values of a field as a function of position?
Ah, right: a GP is a distribution over functions, not a collection of
distributions over variables (sorta). Consider each "realization" of a GP as
a possible "configuration" of the true function. You don't write "the
probability of `w` as a function of `r`, you just say "what is the
distribution over `w`?" then test that distribution at `r`.

So the "wind field regression" problem isn't a problem of a bunch of individual
estimates at different points, it's a problem of a single distribution over
a function which takes on values at a bunch of different points. So yeah, in
that sense you might designate :math:`W(\vec{r})` the true target, and the
distribution over the true wind field is :math:`W(\vec{r}) \sim
\mathcal{W}(\vec{r}) = \mathcal{G}_W(\vec{r})`.

References:

* "Model-based Geostatistics" (Diggle, 2007)

* "Automatic model construction with Gaussian processes" (Duvenaud; 2014)

]]

The next task is to develop relationships between what we know and what we
want. At the beginning, the only thing we know is the sequence of the
paraglider's position over time. To put this into mathematical terms, we start
by defining the time as :math:`t` and the paraglider position as
:math:`\vec{r}`. Because the flight is recorded as a sequence of position over
time, this means everything we know is encoded in :math:`\vec{r}(t)`.

However, because the position was recorded using a GPS device it will be
subject to sensor noise. To account for the sensor noise we need the language
of probability to formalize the uncertainty. To simplify the notation, start
by defining :math:`\vec{r}_t \defas \vec{r}(t)`. The mathematical form of what
we know is then given by the probability distribution over the position is
then :math:`p(\vec{r}_t)`.

Given these new terms, our original objective can be defined as "estimate the
wind field given a sequence of positions from a paraglider flight".
Mathematically, our objective has now become:

.. math::

   p\left(\mathcal{W}\right) =
      \int_{\vec{r}_t}
         p \left( \mathcal{W} \given \vec{r}_t \right)
         p \left( \vec{r}_t \right)
         \mathrm{d}\vec{r}_t

Because there is no direct relationship between the global wind field and the
positions over time, we must decompose the problem definition into
intermediate steps. For instance, although the ultimate objective is to
estimate the entire wind field, our relationship between the wind and the
paraglider position comes in the form of the paraglider aerodynamics, which
only depend on the instantaneous wind velocities :math:`\vec{w}_t`. This
expanded goal is then:

.. math::

   p \left( \mathcal{W} \given \vec{w}_t, \vec{r}_t \right)
      p \left( \vec{w}_t \given \vec{r}_t \right)
      p \left( \vec{r}_t \right)


Some progress can be made by expanding the term :math:`p \left( \vec{w}_t
\given \vec{r}_t \right)`. We know that the position of the paraglider depends
on the wind velocity. An application of Bayes formula produces:

.. math::

   p \left( \vec{w}_t \given \vec{r}_t \right) =
      \frac
         {p \left( \vec{r}_t \given \vec{w}_t \right) p \left( \vec{w}_t \right)}
         {p \left( \vec{r}_t \right)}


Using the terms to rewrite our objective:

.. math::

   p \left( \mathcal{W} \given \vec{w}_t, \vec{r}_t \right)
      p \left( \vec{r}_t \given \vec{w}_t \right)
      p \left( \vec{w}_t \right)


Note that the relationship given by :math:`p \left( \vec{r}_t \given \vec{w}_t
\right)` is ultimately one of the model dynamics. Unfortunately we don't have
any explicit relationship between the position of a paraglider given the wind
field; we do, however, anticipate having a dynamics model that describes the
relationship between a paraglider's movement and the wind if we also know the
paraglider model :math:`\mathcal{M}` and the pilot control inputs
:math:`\vec{u}_t`. By the rules of probability we expand:

.. math::

   p \left( \vec{r}_t \given \vec{w}_t \right) =
      p \left( \vec{r}_t \given \vec{w}_t, \vec{u}_t, \mathcal{M} \right)
      p \left( \vec{u}_t, \mathcal{M} \right)



The Bayesian Formulation
========================

Before we can look for recurring patterns in the wind fields, we need to
estimate the individual wind fields from each flight. Before we can estimate
the wind field of an individual flights, we need an estimate of the sequence
of wind vectors :math:`\vec{w}_{1:T}`.

We want to know :math:`\vec{w}_{1:T}`, but we only have the sequence of
positions :math:`\vec{p}_{1:T}`, so our first step is to target :math:`p
\left( \vec{w}_{1:T} \given \vec{p}_{1:T} \right)`. To do that we need
a relationship between the sequence of flight positions and the wind vectors.
That relationship is given by the paraglider aerodynamics model
:math:`f({\cdot\,} ; M)`, which is parametrized by the wing model :math:`M`.

If we knew :math:`M`, we might try to target :math:`p \left( \vec{w}_{1:T}
\given \vec{p}_{1:T}, M \right)`, but the aerodynamics model also requires the
pilot inputs :math:`\vec{\delta}_{1:T}`, so we are forced to target :math:`p
\left( \vec{w}_{1:T} \given \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right)`. The
problem is that we still have no function that can describe this distribution
in closed-form. Because there is no analytical solution that we can solve
directly, we are forced to use Monte Carlo methods, which approximate the
target by generating samples from this intractable distribution. It is
important to note that we also don't know the true :math:`\vec{\delta}_{1:T}`
or :math:`M`, so we need to generate a representative set of samples for those
as well.

The ultimate goal is to generate representative sets of samples for each of
the unknowns and input those samples into aerodynamic functions of the wing to
simulate many possible flights. These simulations will generate
a representative set of plausible flights, called *trajectories*, then score
(or *weight*) each possible flight based on how plausibly it could have
created the observed flight path. That set of weighted trajectories is the
Monte Carlo approximation of that intractable target, :math:`p \left(
\vec{w}_{1:T} \given \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right)`.

.. math::

   p \left( \vec{w}_{1:T} \given \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right) = \frac{ p \left( \vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right)}{p \left( \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right)} \
                                                                              = \frac{ p \left( \vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right) }{\int p \left( \vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right) \mathrm{d} \vec{w}_{1:T}}

.. ::

   An alternative, two-line version of the above

   .. math::

      p(\vec{w}_{1:T} \given \vec{p}_{1:T}, \vec{\delta}_{1:T}, M) &= \frac{ p(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M)}{p(\vec{p}_{1:T}, \vec{\delta}_{1:T}, M)} \\
                                                                   &= \frac{ p\left(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M\right)}{\int p\left(\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right) \mathrm{d} \vec{w}_{1:T}}


Computing the target requires knowing the joint probability :math:`p \left(
\vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right)`, which is
unknown. Instead, we will use the chain rule of probability to rewrite the
joint distribution, which we *cannot* estimate, as the product of several
conditional distributions, which we *can* estimate.

.. math::

   p \left( \vec{w}_{1:T}, \vec{p}_{1:T}, \vec{\delta}_{1:T}, M \right) = p \left( \vec{p}_{1:T} \given \vec{w}_{1:T}, \vec{\delta}_{1:T}, M \right) p \left( \vec{w}_{1:T}, \vec{\delta}_{1:T}, M \right)

At last, we can use SMC and MCMC methods to produce samples from the joint
distribution, then average over the wind components of each particle to
estimate our ultimate target: the distribution over the wind vectors that were
present during the flight.


Existing tools
==============

[[VERY INCOMPLETE]]


I need to introduce the existing tools for learning wind patterns from flight
data, discuss their advantages and disadvantages, and use their disadvantages
to motivate the cost and complexity of recovering the actual wind vectors.

* Tools that extract structure from flight data:

  * Thermal detectors (Paragliding Thermal Maps, `Track2Thermic`, etc)

  * wind estimators (circle method only?)

* *Patterns* are **recurring** data, which requires multiple flights. An
    example of a tool that combines flights is `Paragliding Thermal Maps`.

* [[How do they work?]]

  * They are trying to learn features of the wind field, but the flight data
    does not contain observations of the wind field, so they use paraglider
    motion as a proxy.

  * Because they are dealing with paraglider motion instead of the actual wind
    field, they rely on heuristics: signatures in the paraglider motion that
    indicate particular features. The heuristics typically involve motion
    summaries like sink rate, altitude gain, ground speed, etc.

  * They segment the track based on detection of those features.

  * To avoid false positives, they filter segments by apply threshold
    functions (minimum segment duration, total altitude gained, minimum or
    maximum ground speed, etc) and reject segments that do not reach the
    threshold.

    The effect is that they can only detect "large" features with well defined
    structure that the pilot succeeded in exploring sufficiently.

* [[What are their strengths?]]

  * Computationally fast

  * The simplicity of feature summaries (hotspots) are intuitive

  * Focusing on "large" features basically means they require a really strong
    signal, which might not be a bad idea at higher AGL.

* [[What are their limitations?]]

  * Inefficient data utilization (they discard too much information)

    * Segments are isolated from each other (you can only learn individual
      features, not global structure; the segments don't inform each other)

    * Thresholds are all-or-nothing (eg, if a pilot didn't core a thermal long
      enough, the entire segment is rejected)

    * Data outside of accepted segments are ignored entirely

    * Use approximate relationships (heuristics) instead of explicit
      relationships (aerodynamics) that require particular motion structure

  * Assumptions about the structure of the wind field

    * Inflexible (explicit structural requirements, aka "motion signatures").
      For example, they assume that thermals are linear (or at least
      piecewise-linear)

  * Assumptions about the performance of the paraglider

    * Average sink rate for all paragliders

    * Neglect how bank angle affects sink rate

  * Assumptions about the motion

    * Rely on the pilot (1) detecting the thermal, and (2) successfully coring
      the thermal

    * Assume the motion of the glider reflects the structure of the thermal

  * Implementation difficulties

    * Features require explicitly designed motion signatures

    * Thresholds are typically fixed and sensitive. Trying to find
      a one-size-fits-all choice is problematic and time consuming.

  * Misc

    * Point-wise outputs limit them to features that can be summarized as
      points.

* Why are they so limited?

  * Because of how they extract information about the wind field from the
    flight data.

  * They rely on heuristics, which can only extract limited information.

  * Because they're limited in what structure they can detect in the available
    data, which limits them in both *what* and *how* they predict.

  * If you can't detect the underlying structure you can't predict it

  * If you can't detect the underlying structure you can't condition on it

* How well do those tools address the problems of discovery and use?

  * Not great. They're limited in both *what* and *how* they can predict.

* [[How can their limitations be improved upon?]]

  * Don't require fixed motion structure

  * Don't require fixed wind field structure

  * Don't discard data

  * Don't use arbitrary thresholds

* [[Segue into my proposal.]]

  * Adding extra information in the form of paraglider dynamics lets you
    extract more information from the data.

  * Separate the steps of extracting wind field information from motion, and
    detecting features in the wind field

* Instead of mapping the wind field, they map where pilots **found** thermals.


OLD OUTLINE 2
=============


Inverse problems
----------------

* Simple example of solving an equation, and a system of equations

* Define *underdetermined system*

* You can "fix" an underdetermined system by adding more information: more
  data, or more relationships (equations)

* What if you still don't have enough information? What does it mean to
  "solve" an underdetermined system?

  We have to rely on statistical inference: instead of "solving" the problem,
  we infer properties of the distribution over what the solution might be.

* Define *inverse problem*

* We are trying to estimate the wind vectors using observations of position.
  We don't observe the wind vectors directly, so wind vector estimation from
  the available data is an *inverse problem*.

* Underdetermined systems cannot be solved exactly, they can only be solved
  approximately. Instead of seeking the single "true" value, the problem
  becomes one of estimating a distribution over all possible values.


* [[The goal is to use statistics to gain information about some target based
  in information gained from some observed data. Conditioning one variable on
  another requires a **statistical dependency** between the them. The
  relationship can be direct or indirect.

  The natural starting place for any data analysis problem is to define
  a model of the data-generating process. If the target is not a member of the
  data-generating process you must be able to extend the model with new
  relationships to induce the dependency. Otherwise, the observed data is not
  informative about the value of the target.]]


Filtering problems
------------------

* A common example of an underdetermined system is a measurement corrupted by
  noise.

* [[Sometimes observations are produced in a sequential fashion]]

* [[Introduce sequential processes]]

* [[Sequential estimation has a special mathematical form]]

* Define *filtering problem*

* Solving a *filtering problem* requires a model of the *data-generating
  process*

* [[*State-space models* are the natural representation of sequential
  data-generating processes]]

* [[Converting a state-space model to a statistical model]]

* [[Using the full statistical model to solve the filtering problem]]


Flight reconstruction as a filtering problem
--------------------------------------------

.. Could also model this as a *state-estimation problem* if you consider
   the unknown inputs as "state".

* Define a state-space model of the paraglider position

* Review the components of the state-space model

* Define *nuisance variable*

* [[Unlike unpredictable noise terms, these nuisance variables have structured
  dynamics that capture essential information.]]

* Nevertheless, evaluating the paraglider dynamics requires concrete values
  for all of its parameters. Where do those values come from?

* Define *simulation-based filtering*

  [[Essentially, you draw "guesses" for the unobserved variables from
  a proposal distribution, then use the rules of probability to compute the
  posterior probability of the target while accounting for the uncertainty in
  those unobserved variables.]]

  **I should probably stop using the phrase "simulation-based filtering".
  Every filtering architecture that uses a transition function is "simulating"
  the dynamics. I sure highlight the need to simulate the unknown data, but
  stop using this term: it's not informative.**

* [[Flight reconstruction (as we'll be doing it) is many problems in one:
  state-estimation, input-estimation, and parameter-estimation. In the end we
  will marginalize over the nuisance variables to get just the posterior
  distributions of the wind vectors.]]


.. Conclusion

* In this paper, the term *flight reconstruction* refers to this process
  of estimating the full joint probability distribution over all the variables
  in the state-space model for the entire flight sequence.

* The focus of this paper is to provide a parametric paraglider model suitable
  for flight reconstruction of average, non-acrobatic paragliding flights.


OLD OUTLINE 4
=============

* The most informative relationship is a *causal* one. (As opposed to merely
  *descriptive* models? Are "heuristics" descriptive models?)

* We want to understand what caused the sequence of positions. In technical
  terms, we want a model of the *data-generating process*.

* The data is a sequence of position measurements over time. The changes in
  position are the result of the paraglider motion, which is determined by the
  paraglider dynamics. The dynamics are a causal model of paraglider motion.

* Thus, the model of the data-generating process must incorporate the
  paraglider dynamics.

* There is flexibility in defining a paraglider dynamics model, but we are
  interested in how the dynamics are affected by the wind vectors, so the
  dynamics must include the wind as an input. The components of the dynamics
  that result from interactions with the wind are given (mostly) by the canopy
  aerodynamics.

* Thus, the data-generating process must incorporate a paraglider dynamics
  model that includes a causal aerodynamics model.


***************************
Parametric paraglider model
***************************

* What are the physical model criteria?

  * Intuitive (easy to produce the desired design)

  * Time efficient (it shouldn't take a lot of time to get a reasonable
    approximation)

  * Information efficient (get good results with minimal specification data)


* What are the dynamics model criteria?

  * Doesn't assume the aerodynamics are linear. Linearity has not be
    demonstrated to be an acceptable trade-off, so the aerodynamics method
    must not rely on the linearity assumption.

  * Uses open source tools and libraries

  Bonus criteria:

  * The modeling process should keep in mind that it's not just wing designers
    that are interested in paraglider performance. When I started I had
    questions about paraglider performance, and answers were hard to come by.
    (In a way, I am the primary audience of this paper: I wanted to learn how
    paragliders behave, and I did.)

  * I've seen many discussions online about wing behavior; it would be useful if
    the model could be used to simulated specific scenarios of interest.

    For example, how does a wing react to an indirect thermal interaction? That
    would require aerodynamics that don't assume symmetric wind across the wing.


*************************
Introduction (2021-08-20)
*************************

.. Meta:

   Structure taken from `Exploration of Style
   <https://explorationsofstyle.com/2013/02/20/structuring-a-thesis-introduction/>`_.

   This chapter should establish:

   1. The problem: learn wind patterns from recorded flights

   2. The value: feedback helps pilot enjoy better flights

   3. The difficulty: not enough data

   4. The solution: introduce more information via flight dynamics

   5. The work: building a dynamics model for a particle filter

   6. The result: a fully parametric paraglider model


.. Intro to the Intro

.. Establishing a research territory (Context): wind patterns help pilots

Paragliding is a recreational flying activity that uses a lightweight,
flexible wing for non-powered flight. Because paragliders lack a motor, their
motion is entirely dictated by interactions with gravity and wind.
A successful flight depends on the pilot's ability to recognize the structure
of the local air currents and navigate them in order to achieve their flight
goals, which may include optimizing for flight time, distance, or a particular
route. Because a glider is constantly spending energy to counteract the force
of gravity, the pilot must recognize the wind patterns as quickly as possible
to minimize energy loss. Experienced pilots assess the nearby air currents by
observing vegetation, birds, or other pilots, but they can also leverage
knowledge gained from previous flights; although local wind configurations are
difficult to predict in detail, they can exhibit recurring patterns. By
learning those patterns a pilot can assess the current wind conditions more
quickly and more accurately, and can prioritize flying to areas that are
likely to support their flight goals.


.. Establishing a niche (Problem and Significance): learn patterns from data

Traditionally, wind patterns are discovered by pilots with a large amount of
flight time in a particular area, and are shared directly from one pilot to
another. For the pilot community to learn reliable patterns, individual pilots
must first recognize a pattern and then be able to communicate it with
precision. An appealing alternative would be to aggregate recorded flight data
from many pilots over many flights, detect any wind patterns automatically
from those flights, and build a graphical map to communicate the features of
the wind field visually instead of relying on verbal descriptions. In support
of this idea, there already exist large databases with millions of recorded
flights spanning several decades. These databases continue to grow as pilots
record and share their flights for personal and competitive purposes. The
difficulty with using those records is that most flight devices only record
a tiny amount of the information available to a pilot; in fact, the average
flight record can only be expected to include a time series of positions.
There is typically no information regarding the orientation, velocity,
acceleration, pilot control inputs (brakes, accelerator, etc), or the weather
conditions. Even the details of the aircraft are unknown, although some tracks
do record the wing make and model. The question then becomes whether there is
enough information in position-only time series data to recover the wind
vectors that were present during a flight.


.. Occupying the niche (Response): developing a paraglider dynamics model to
   enable flight reconstruction

This thesis considers the procedures necessary to estimate wind field
structure from position-only time series flight data. The first step is to
formulate the goal in mathematical terms, which will determine the underlying
structure of the problem, and what information would be required to solve it.
It concludes that a robust solution would require a dynamics model of the
paraglider that produced the flight record, and so those dynamics are the
focus of this thesis. The primary output of this project is the design and
implementation of a parametric paraglider dynamics model and simulator for
generating flight tracks from a given wind field and pilot control sequence.
[[**Specifically, I'm interested in creating dynamics models from bare-bones
knowledge of the paraglider system: wing, harness, etc.**]] The paper will
discuss how the dynamics model enables simulation-based filtering methods to
perform statistical flight reconstruction, [[and concludes with a discussion
of the remaining work?]]


.. Context

   "Provides the full context in a way that flows from the opening."

Paragliding
===========

.. Introduce paragliding as a sport

.. FIXME : merge this section into "Wind fields"?


.. What is paragliding?

Paragliding is a recreational flying activity that uses a lightweight,
flexible wing for non-powered flight. The pilot is strapped into a harness
suspended from the wing by a network of thin connecting lines. The wing is
controlled by manipulating the lines and shifting the pilot's weight inside
the harness.

There are a variety of reasons that people choose to fly. Some flights begin
with an explicit goal: maximum flight time, maximum distance, maximum
altitude, or perhaps to follow some particular route. Some pilots compete
against other pilots in organized events, some compete against their own
personal records, and some just want to relax and see where the wind takes
them. Regardless of the goal, there is one underlying concern that is common
to every pilot: how to deal with the constraints of gliding flight.


.. How does gliding flight depend on the wind?

A paraglider is a non-powered aircraft, so its motion is determined by how
it interacts with gravity and the air. A pilot can steer the glider through
the air, but they cannot control how the air is moving relative to the ground.
Ultimately, it is the wind that limits how a paraglider is able to move
relative to the ground.

As with all lifting surfaces, the aerodynamics of a paragliding wing depend on
the relative velocity between the wing and the air, not the relative velocity
between the wing and the ground; the wing will accelerate until an equilibrium
state is achieved. If the air is ascending a pilot can slow their descent, or
even gain altitude; conversely, sinking air will cause the wing to descend
more quickly. The horizontal component of the wind dictates the ground speed
of the glider in a given direction, which determines what regions of the air
the pilot can access, and what landing zones they can reach. As a result,
pilots must understand the structure of the wind field in order to plan their
flight path and achieve their flight goals.


Wind fields
===========

.. What is a wind field?

A *wind field* defines the detailed variations of local air currents
throughout some region. Each point in the wind field has a specific *wind
velocity*, also known as a *wind vector*. It is important to note that in this
paper the terms are considered interchangeable, but in aeronautics literature
the term *wind vector* often refers to only the lateral motion of the air (the
horizontal wind speed and direction).


.. What wind fields are paragliding pilots interested in? Where do they occur?
   What is special about the ABL?

The wind fields that are relevant to paragliding pilots occur in the lowest
portion of the atmosphere: the *atmospheric boundary layer* (ABL). The ABL is
in direct contact with the Earth's surface, whose variations produce
significant instability in the surrounding wind field. In particular,
paragliding is restricted to the very lowest region of the ABL; most countries
limit free-flight activities to a maximum altitude of approximately 5,500
m (18,000 ft), which means gliders are restricted to the most volatile region
of the ABL.


.. What factors contribute to the (volatile) structure of a wind field?

   FIXME : discuss surface heating, thermal convection, lapse rates,
   topography, vegetation, mountain waves, etc. Global structure combines with
   topography to produce the local structure.


.. What are some examples of identifiable structures in a wind field that are
   relevant to paraglider pilots?

* Although the small-scale detail and stochastic nature of wind fields make
  precise mapping impossible, pilots routinely identify larger-scale features
  that summarize specific characteristics of local regions.

* [[Describe the local wind field as a composite of basic features: thermal
  lift and sink, orographic lift, shear (including venturi), etc. See
  :cite:`bencatel2013AtmosphericFlowField`

  Prioritize wind field structure that is important to pilots. For example,
  house thermals, ridge lift, sink over water, etc.]]


.. Why is it important for a pilot to determine wind field structure quickly?

Much of the skill in piloting a gliding aircraft is in maintaining the
glider's energy budget, which requires careful aircraft control and efficient
path planning. Because planning a path through an environment depends on
accurate knowledge of that environment, pilots are constantly looking for
information about the structure of the wind field.

[[Vertical wind directly impacts energy budgets. Horizontal wind determines
where they can go and how time/energy it costs to get there. They need to find
lift while avoiding sink, make sure they can reach the LZ, etc.]]


.. How do pilots estimate the structure of the wind field?

The direct way to learn the structure of a wind field is to explore. The
problem is that exploration takes time, and time has a significant energy
cost; a wing remains airborne by constantly exchanging its momentum with the
air, which means it is constantly spending energy. Pilots cannot afford to
explore at random; they need strategies for efficient path planning that will
focus their exploration on promising regions. If their strategy fails, they
can be left without sufficient altitude to continue their flight, or they can
be blocked by a headwind that prevents them from reaching their destination
(regardless of their altitude).

Another direct source of information is to observe other objects interacting
with the wind field. For example, dust, debris, and insects can be caught in
air currents, so their motion can provide information from a distance. Soaring
birds, such as hawks and vultures, are excellent navigators of the wind field,
and can indicate lifting air; even other pilots can provide a hint as to the
conditions elsewhere. Also, although pilots are typically focused on the wind
conditions at higher altitudes, useful information can be gained by observing
behavior closer to the ground, such as vegetation and ripples on water.
Anything that interacts with the wind can be a potential source of
information. [[FIXME: reword.]]


.. How can pilots predict the structure of the wind field?

Another valuable, albeit indirect, source of information is the local
topography. Paragliding pilots rely heavily on understanding how the
environment affects the wind field. Regions with more sun exposure will tend
to produce warmer air that can rise through thermal convection. The
orientation of the ground (or other objects such as trees and buildings)
relative to surface winds can produce useful updrafts; many popular flying
sites use the lift generated when an onshore breeze collides with a coastal
bluff. Under some conditions warm air near the surface can respond to
so-called *thermal triggers* that function like a wick; by disturbing the
equilibrium conditions at the surface the trigger can initiate bubbles or
columns of rising air that pilots can use to increase their energy budget.

[[Meteorological forecasts (weather forecasts, `RASP
<http://www.drjack.info/twiki/bin/view/RASPop/WebHome>`__ `soaringmeteoGFS
<http://soaringmeteo.org/GFSw/googleMap.html>`__, `Paragliding Maps
<http://www.paraglidingmaps.com>`__)

Although there are many methods to help a pilot predict the local wind field,
there is one that is particularly effective: local *wind patterns*.


.. Restatement of the problem (and significance)

   "Restate the problem and significance in light of the more thoroughly
   detailed context."

Wind field patterns
===================

.. This section establishes that it is easier to estimate and predict the
   structure of a wind field if you have knowledge of recurring structure.
   There are problems in discovering and using that knowledge which can
   benefit from building predictive models from flight data. Unfortunately the
   flight data doesn't contain observations of the wind field, so this section
   concludes by motivating wind field estimation.

   Discuss wind patterns, their importance, and how they're learned


.. What are *wind patterns*?

In this paper, a *wind pattern* is any **recurring structure** in a wind
field. The term "structure" refers to any identifiable order, and does not
imply any particular configuration; uniform flows, shear, orographic lift,
convective sources and sinks, etc, and any combinations of those, can all be
considered structured configurations. The term "recurring" refers to the fact
that some regions of a wind field can exhibit the same structure at different
times.


.. Why are wind patterns so **particularly** valuable to pilots?

[[Pilots need to predict the wind field structure before they visit a region,
and estimate its structure once they arrive.]] Knowledge of local wind
patterns is particularly valuable in both scenarios. First, if some region of
a wind field exhibits recurring structure, then pilots can use that to predict
its structure without spending glider energy exploring that area. Second, once
a pilot has begun traversing some region, historical patterns provide
additional perspective that can help a pilot correctly interpret the wind they
encounter. Ultimately, knowledge of wind patterns help pilots determine the
structure of a wind field more *efficiently* (both in terms of time and
energy) and more *accurately* when they can base their expectations on known
patterns.

[[Consider both the vertical and horizontal components. Consider both
pre-flight (flight planning) and in-flight scenarios.]]

[[Another advantage of wind patterns is that they are practical: they focus on
what did happen, not what might happen in theory. All the other means of
predicting the wind field, like meteorological models, etc, are only useful if
the theory is able to produce an accurate causal model; if a causal model is
wrong, its predictions are wrong.]]


.. What challenges prevent pilots from taking advantage of wind patterns?

Pilots who want to take advantage of wind patterns face a variety of
challenges that can be broadly classified as problems of *discovery* and
problems of *use*. Traditionally, pilots discover wind patterns by flying in
the same region repeatedly, and by sharing their observations with other
pilots. This means that individual pilots must accurately identify, record,
and recall the data that may form a pattern; in practice, the volume of detail
encountered during a flight means that pilots tend to recall only the most
significant details. Similarly, when the data is spread between pilots, it
must be accurately and thoroughly communicated, but in practice only
large-scale summaries are shared between pilots, and the majority of the
detail is lost. Given what data remains, if the evidence of recurring
structure is strong enough, the pilots may be able to identify any patterns.
Once a pattern has been discovered, each pilot must be able to recall the
pattern and under what conditions it occurs.


.. Can flight data be used to address those challenges?

   **THE DRIVING QUESTION OF THIS PAPER.**

These problems of identifying, recording, recalling, and combining data into
patterns are not [[well suited]] to pilots whose time and attention is already
dedicated to the more physical aspects of flying. As an alternative, if wind
field structure can be determined from individual data records, it would
enable the creation of automated tools to address the problems of discovery
and use.


.. Step 1: address "problems of discovery"

* What are the advantages of pattern discovery from recorded flights?

  * Automate pattern discovery [[ie, it's convenient? Also, some patterns may
    be subtle; they may involve conditions that humans won't typically pick up
    on (especially ones involving negatives, like "if there is NOT lift over
    here, they may be lift over there")]]

  * More opportunities to find patterns in flights that are spread out over
    longer time periods. Some trends may be infrequent, and pilot
    memories fade.

  * Utilize all recorded flights from all pilots instead of requiring multiple
    flights by the same pilot. [[If a pilot only encountered a particular wind
    configuration a single time, they wouldn't recognize it as part of
    a recurring pattern.]]

  * Expand the set of detectable patterns: a single flight can only
    observe a small portion of the wind field. By merging multiple flights
    that occurred at the same time, you can build a more comprehensive
    observation of the field. With larger observations there are more
    opportunities for detecting useful patterns.

  * Quantifying/encoding the patterns in mathematical form would enable the
    creation of a *predictive model*, which can then address problems of use.
    [[This is hard to follow; explain how simply producing a list of patterns
    is different from making predictions by conditioning on current state.]]


.. Step 2: address "problems of use"

* What are *predictive models*?

  * Predictive models encode predictable structure. Some wind field patterns
    can be predicted based on time of day/year, some can be predicted based on
    the values of other regions of the wind field, etc. This is the essence of
    "conditioning" our predictions.

  * Predictive models inform pilots of historical trends, which can help them
    recognize the current structure as early as possible; ideally, before they
    even fly into a new area. They can also improve the accuracy of a pilot's
    estimate of the current wind field.

  * [[**Computer** models that predict the structure of the wind field.]]

  * [[I'm leaving "pattern" vague, so this can include things like Paragliding
    Thermal Map, etc. Those tools only estimate simple point sources I'm still
    considering them "recurring structure".]]

* What are the benefits of encoding patterns in predictive models?

  * [[We discussed the value of patterns earlier. This is about the benefits of
    having a predictive model built from those patterns.]]

  * Save the pilot from having to memorize the patterns

  * Save the pilot from having to remember the conditions under which a pattern
    is applicable.

    Conditioning on the state of the wind field enables predictions that are
    consistent with the observations. Conditioned models attempt to predict the
    *actual* configuration instead of some *average* configuration (which is
    typically produced by averaging over some arbitrary time interval).

    Conditioning to produce estimates that are consistent with the observations
    of the current wind configuration (averages lump everything together).
    Useful both pre-flight (condition on weather forecasts) and in-flight
    (condition on actual conditions).

    [[Note: you don't have to use the same predictive model for pre-flight and
    in-flight prediction; for example, if you have wind forecasts on a grid of
    the surrounding area, you could train the model using the values of those
    predictor variables (which are **not** the same thing as observations of
    the wind field itself.]]

  * Visualizing structure on a graphical map is convenient.
    :cite:`wirz2011RealtimeDetectionRecommendation`

  * A statistical predictive model can provide confidence levels: it
    can quantify the variance in its predictions, since it knows how much
    evidence is present for a particular pattern. [[How does this compare to
    word-of-mouth knowledge? Pilots can be deceived/biased about their
    experiences; memories are faulty.]]


[[FIXME: discussion here.

Conclusion: before you can estimate **recurring** structure, you need to be
able to estimate the structure for the individual flights from the flight
data.]]


Wind field reconstruction
=========================

.. We've established that learning patterns and predictive models from flight
   data would be a good thing, but first we need to able to reconstruct the
   wind fields from individual flights. This section should review existing
   tools, consider how successful they are, and consider the source of their
   limitations.

   The fundamental problem with existing tools is they have to rely on
   heuristics (non-causal relationships that try to estimate wind field
   structure directly from paraglider position). This limitation means they
   fail to adequately address all those problems of discovery and use.


.. What is *wind field reconstruction*?

In this paper, *wind field reconstruction* refers to the process of estimating
the structure of regions of the wind field that was present during a flight.


* [[Introduce the data (IGC files) here?]]


.. Are there existing tools to extract wind field structure from flight data?

* Paragliding Thermal Map, etc

* [[FIXME: what about prediction? "Paragliding Thermal Map" does let you
  filter by time of year.]]


.. How do they work?

Because flight data does not include the actual wind vectors, existing tools
rely on *heuristics*: approximation methods that rely on the wind field
containing features with some predefined structure that can be detected based
on specific patterns of the paraglider motion. For example, thermal detectors
may require a minimum sink rate or total altitude gained, and they are forced
to make strong assumptions about the state and parameters of the glider (such
as average sink rate). Horizontal wind estimators may require that the glider
was circling at a fixed airspeed. Other methods may try to fit the vertical and
horizontal components simultaneously; for example, one method assumes
a circling glider is accurately coring a thermal that is inclined with respect
to the wind, so fitting a thermal model. [[FIXME: edit]]

To avoid false positives, heuristic-based feature detectors typically introduce
constraints on the motion such as minimum duration, minimum number of cycles,
etc. Given a interval, the output is assumed to be representative of the wind
field over the entire interval. The result is a sort of "average structure"
that tends to "smooth out" the regions they fit. Subtleties in the wind field
are lost.

[[FIXME: probably a good place to mention that, over a short time span, you
can't tell the difference between headwind+lift versus braking?]]

[[FIXME: discuss energy-based methods?]]

Ultimately, each heuristic can only detect an explicit feature, and only if the
motion of the paraglider matches a predefined motion signature; the rest of the
data is discarded, which also discards valuable information.

[[FIXME: plus, that kind of output is hard to use to condition a predictive
model. You'd either have to run a similar feature detector in-flight (which is
likely to be VERY noisy) or you have to convert those features into something
that can be more easily related to the kind of data available in-flight (eg,
convert a thermal "feature" into an average sink rate or something).]]


.. What are their limitations?

[[Existing tools use heuristics that rely on coincidental instead of causal
relationships. Indirect relationships are the cause of awkward hacks/filters
like "require the paraglider to be circling" or "sink rate must be at least
1m/s". Direct relationships avoid those.]]

The heuristics impose some limitations:

* They can only detect specific kinds of structure. They cannot determine the
  wind field structure in general.

* They rely on specific paraglider motion patterns. They do this because they
  don't have a direct relationship between paraglider motion and wind field
  structure, so they have to rely on heuristics.


.. How well do existing tools address the problems of *discovery* and *use*?

These restrictions limit both *what* structure heuristic-based tools can
detect (and thus in what structure they can predict), as well as *how* their
outputs can be used to make predictions. As a result, these tools are
generally inadequate for addressing the problems of discovery and use.


.. How can the limitations of heuristics be avoided?

[[Instead of trying to estimate wind features directly from paraglider motion,
the goal should be to break the process into multiple steps that use
**direct** relationships: paraglider motion is directly related to wind
vectors, wind vectors are directly related to the (continuous) wind field, and
the wind field contains the structure that contains the wind features.]]

The underlying cause of these restrictions is that the tools have to rely on
paraglider motion as a proxy for wind vectors. If the wind field itself was
available, feature detectors could target its structure directly instead of
relying on paraglider motion as a proxy.

* Why would wind vector estimation improve wind field reconstruction?

  * Don't require explicit motion patterns. The entire sequence of positions
    contains information about the wind field; don't throw some of it away
    just because an interval doesn't fit some predefined motion signature.

  * Don't require explicit wind structure (ie, don't limit the estimator to
    structure that adheres to an explicit model, like a linearized thermal.
    You can *summarize* regions of the wind field using that sort of
    structure, but that should not be fundamental to *estimating* the wind
    field.)

* Are there existing methods for estimating wind vectors from position-only
  flight data?

  Yes, but they rely on the same type of heuristics that were discussed
  earlier, with the same limitations.

  They typically rely on a moving-average approach; for example, the circling
  method is essentially an average over a time interval. Moving-average
  methods require long intervals to reduce estimate noise, but as a result the
  estimates are over-smoothed (and that's assuming the constant-airspeed
  assumption held over that interval).


* CATCH-ALL COLLECTION

  The existing methods fail because they don't have enough information
  (because they don't impose enough structure). They rely on indirect
  relationships and questionably strong assumptions.

  The heuristics mentioned so far are *model-free* methods that rely on
  **coincidental** relationships between the particular motion sequence and
  the feature being detected. In contrast, *model-based* methods rely on
  **causal** relationships: causal dynamics introduce additional information
  about the system dynamics which can then be used to extract more information
  from the data.

  Better wind vector estimation requires a direct, causal relationship between
  wind vectors and paraglider position.

  In particular, we need to model the paraglider dynamics. The canopy
  aerodynamics provide the link between the paraglider motion and the wind
  field. But, because the paraglider only interacts with points in the wind
  field, the relationship only provides information about the local wind
  vectors.

  [[Conclusion: the goal is to estimate the continuous wind field from
  position-only flight data, but we don't have a relationship to do that
  directly. What we do know (partially) is the paraglider dynamics, so we need
  to start by targeting the sequence of wind vectors encountered at discrete
  points in the wind field.]]


.. Restatement of the response

   "Leverage the detail presented in the full context to elaborate on the
   details of the response."

Flight reconstruction
=====================

.. This section establishes the intuition behind reconstructing the complete
   state trajectory of a flight from a time series of positions. The goal is
   to recover the wind vectors at individual points to enable estimating the
   continuous structure of the wind field, but the wind vectors are related to
   position through the paraglider dynamics, which require more inputs than
   just the wind vectors, so the complete state must be reconstructed. It
   concludes by motivating :math:`\dot{x} = f(x, u)`, which is what the
   `pfh.glidersim` Python package is designed to provide.


The conclusion of the previous section is that reconstructing a wind field
from flight data should start by estimating the sequence of wind vectors. The
difficulty is that flight records are limited to position-only data; they do
not contain any direct observations of the wind vectors. The solution is to
exploit knowledge of how the sequence of positions were generated.

[[FIXME: should/did the previous section explain that targeting wind vectors
instead of the final wind field enables the use of causal dynamics? I don't
want to introduce the dynamics yet (that should happen in these paragraphs),
but if so, I shouldn't just announce "we should start by estimating the wind
vectors!" in the conclusion to "Wind field reconstruction"]]


.. Develop the intuition with an informal description

Imagine a paragliding pilot standing on the ground, looking up at a paraglider
in flight. Under average conditions, the pilot on the ground could watch the
paraglider for a few moments and be able to produce a reasonable guess of the
current wind conditions near the glider. Their guess is imprecise, and yet
pilots routinely use this kind of estimate to decide whether to launch their
own glider. How does that work, and can it form the basis of better wind
estimation?

[[Consider the fact that they're not relying on specific motion signatures;
they rely on approximations, but not the heuristics discussed previously.
Also, it's important to remember that "imprecise" is relative; the estimate
merely needs to be **useful**.]]

The key is that their estimate is built not only from the paraglider motion,
but also from their intuition for how paraglider motion depends on the wind;
given what they know about average paraglider performance, and the range of
wind conditions in which a pilot would choose to remain airborne, they can
imagine a range of possible scenarios and predict how a wing would respond to
each possibility. [[FIXME: it's not obvious how this is different from
heuristics, which also use "intuition" of how paraglider motion depends on the
wind.]] Scenarios that don't agree with the observed motion are unlikely to be
correct can be rejected, and the ones that remain establish a range of
plausible values.


.. Formalize the steps

Estimating wind vectors using flight data is very similar, but first this
intuitive approach must be formalized in mathematical terms: the pilot's
intuition of wing performance is replaced with numerical physics, the ad hoc
set of plausible wind vectors is replaced with a principled set of proposals,
and the conclusion is replaced with a probability distribution.

First, the intuitive strategy of the pilot standing on the ground as
a sequence of steps:

1. Learn how a paraglider's motion depends on its interactions with the wind
   and a pilot's control inputs.

2. Imagine a set of plausible guesses for the current wind vector and control
   inputs.

3. Use the knowledge of paraglider behavior to predict how the paraglider
   would move if each guess was correct.

4. Consider how well each of the guesses explained how the paraglider is
   actually moving.

5. Summarize the plausible range for the current wind vector.

Then, rewrite the intuitive steps in formal terms:

1. Model the *data-generating process*.

2. Generate a set of *proposals*.

3. Use the model dynamics to solve the *forward problem* for each proposal.

4. *Weight* each proposal according to how well it matches the observation.

5. Use the set of solutions to the forward problem to establish a distribution
   of plausible solutions to the *inverse problem*.


Model the data-generating process
---------------------------------

.. "Learn how a paraglider's motion depends on its interactions with the wind
   and a pilot's control inputs."

The fundamental insight to solving the inverse problem is to explicitly
recognize that flight records are the output of some *data-generating
process*. A model of the data-generating process describes how the data was
created. By defining the relationships between all the variables involved in
the process, the model encodes structural knowledge that can be used to solve
the inverse problem.

In the case of paraglider flight tracks, the data is a series of position
measurements recorded at discrete points in time. The natural representation
of such a sequential process is a discrete-time *state-space model*. The
process is modeled as a system of two vector-valued equations: one for the
model state :math:`\vec{x}`, and one for the measurements :math:`\vec{y}`. For
simplicity, these model often assume that each measurement is evenly spaced in
time at intervals of some time period :math:`T`, allowing each sample to be
referenced with a discrete-time index :math:`k = \{0, 1, ...\}`, with
a corresponding continuous-time index of :math:`t_k = kT`. (In practice, the
flight data may not be evenly spaced, in which case this model cannot be used
directly, but that's irrelevant to this discussion.)

The sequence of states is the iterated output of some *transition function*
:math:`f`, and the sequence of observations is the output of some *observation
function* `g`. The transition function encodes how the state variables evolve
over time, in response to their current values :math:`\vec{x}_k` and any
exogenous inputs :math:`\vec{u}_k` (such as the wind vector :math:`\vec{w}_k`,
or the vector of pilot controls :math:`\vec{\delta}_k`), while the observation
function defines how the data is related to the state variables. The resulting
state-space model is deceptively simple:

.. math::
   :label: discrete-time state-space model

   \begin{aligned}
     \vec{x}_{k+1} &= f \left( \vec{x}_k, \vec{u}_k \right) \\
     \vec{y}_k &= g \left( \vec{x}_k \right)
   \end{aligned}

Defining the state-space model means defining the transition and observation
functions. The details of the observation function depend on the choice of
state variables, but for the purposes of this discussion the only requirement
is that it depends on the current state. Defining the transition function is
more difficult: in order to estimate wind vectors from the flight data the
state dynamics must depend on the canopy aerodynamics, since they define the
relationship between the wind field and the paraglider motion. In other words,
a simple *descriptive* model, such as kinematics, would not contain the
*causal* relationships necessary to infer the inputs that produced the
observed behavior (:cite:`mcelreath2020StatisticalRethinking`:28).

The underlying :ref:`system dynamics <paraglider_systems:System dynamics>`
(which drive the :ref:`state dynamics <paraglider_systems:State dynamics>`)
are naturally defined by differential equations involving the continuous-time
index :math:`t`, which means computing state transitions requires integrating
the state derivatives :math:`\dot{\vec{x}}(t)` over the simulation time
interval (:cite:`simon2006OptimalStateEstimation`:27):

.. math::
   :label: state-dynamics

   \dot{\vec{x}}(t) = f \left( \vec{x}(t), \vec{u}(t) \right)

.. math::
   :label: state-transition

   \vec{x}_{k+1} = \vec{x}_k + \int_{t_k}^{t_{k+1}} \dot{\vec{x}}(t) dt


The final step of modeling the data-generating process is to account for all
the sources of uncertainty. The system dynamics are an idealization of the
true physics, the measurements are corrupted by sensor noise, and (in this
case) the system inputs are entirely unknown. As a result, the deterministic
equations must be replaced with stochastic relationships; instead of precise
point values, the inputs, states, and observations are random variables
distributed according to probability distributions:

.. math::
   :label: noisy discrete-time state-space model

   \begin{aligned}
     \vec{w}_0 &\sim p(\vec{w}_0) \\
     \vec{\delta}_0 &\sim p(\vec{\delta}_0) \\
     \vec{x}_0 &\sim p(\vec{x}_0) \\
     \vec{w}_{k+1} &\sim p \left( \vec{w}_{k+1} \given \vec{w}_{k} \right) \\
     \vec{\delta}_{k+1} &\sim p \left( \vec{\delta}_{k+1} \given \vec{w}_k, \vec{\delta}_k, \vec{x}_k \right) \\
     \dot{\vec{x}}(t) &= f \left( \vec{x}(t), \vec{u}(t) \right) \\
     \hat{\vec{x}}_{k+1} &= \vec{x}_k + \int_{t_k}^{t_{k+1}} \dot{\vec{x}}(t) dt \\
     \vec{x}_{k+1} &\sim p \left( \vec{x}_{k+1} \given \hat{\vec{x}}_{k+1} \right) \\
     \vec{y}_k &\sim p\left( \vec{y}_k \given \vec{x}_k \right)
   \end{aligned}

In practice the uncertainties will depend on conditional relationships that
encode additional structure (the wind vector will depend on its previous
value, the pilot controls will depend on the pilot's intentions, etc), but
such details are beyond the scope of this paper. Nevertheless, the essence of
the wind vector estimation problem is captured by equations
:eq:`state-dynamics`, :eq:`state-transition`, and :eq:`noisy discrete-time
state-space model`. This stochastic model of the data-generating process is
ready to be combined with "plausible guesses" of the unknown states and inputs
in order to solve the inverse problem.


Generate a set of proposals
---------------------------

.. "Imagine a set of plausible guesses for the current wind vector."

* [[Define *proposal*, give examples, etc]]

  Earlier I only mentioned proposals for the wind vectors, but I'll need to
  deal with the control inputs too.


A "guess" or *proposal* is equivalent to drawing a sample from a probability
distribution. The probabilities for each variable can be based on prior
knowledge of plausible values, or on estimates of recent values. 



Solve the forward problem
-------------------------

.. "Use the knowledge of paraglider behavior to imagine how the paraglider
   would be moving if each guess was correct."

[[Define *forward problem*]]

[[Here, "solving" the forward problem is "solving" it in the sense of
"solving" differential equations. In practice, it means, evaluating the state
transition function :eq:`state-transition`.

Given the set of "guesses" for the system inputs, the state transition
function :eq:`state-transition` can be used to predict how the paraglider
would move if the guess is correct. In the context of differential equations,
this step is referred to as *solving* the equation.]]


Weight the outcomes
-------------------

.. "Consider how well each of the guesses explained how the paraglider is
   actually moving."

[[Each proposal produced a different solution to the forward problem; the were
predictions of the system behavior. Now you need to "score" each prediction by
comparing it to the actual observed behavior.]]

.. math::
   :label: predictive weight

   \alpha_{k|k-1}^{(n)} = \alpha_{k-1|k-1}^{(n)} p \left( \vec{x}_{k}^{n)} \given \vec{x}_{k-1}^{n)} \right)

.. math::
   :label: posterior weight

   \alpha_{k|k-1}^{(n)} = \alpha_{k-1|k-1}^{(n)} p \left( \vec{x}_{k}^{n)} \given \vec{x}_{k-1}^{n)} \right)



Solve the inverse problem
-------------------------

.. "Summarize the plausible range for the current wind vector."

.. Too many unknowns means this is a stochastic filtering problem

The target?

.. math::

   \begin{aligned}
      p \left( \vec{w}_{1:K} \given \vec{y}_{1:K} \right)
        &=
          \iint p \left(
            {\vec{w}_{1:K}, \vec{x}_{1:K}, \vec{\delta}_{1:K}}
            \given \vec{y}_{1:K} \right) d \vec{x}_{1:K} \, d \delta_{1:K}\\
        &\approx \sum_{n = 1}^N \alpha_{K|K}^{(n)} \vec{w}_{1:K}^{(n)}
   \end{aligned}

[[The relationship is *causal*: the data are observations of an effect
(paraglider motion), and the wind is a cause.]]

The flight track recorded an effect (position) and we we wish to infer
a cause. In stochastic filtering theory, the problem of trying to infer
a cause from an effect (or more generally, inferring an input from an observed
output) is referred to as an *inverse problem*.

[[We want to determine the conditions that produced the sequence of position
measurements.]]

* [[Define *inverse problem*. Give a few examples? Discuss why they are hard
  and how they can fail?]]

  * Wind is only one of the causes; the output (position) is the result of
    multiple inputs.

  * There may be multiple combinations of input that produce the same output
    (the solution is not guaranteed to be "unique").

  * The data is noisy.

* [[FIXME: define "solving" an inverse problem. Given complete information and
  the ability to compute the function inverse, you can compute the true inputs
  that produced a given output. If there is a many-to-one relationship, or if
  some information is unknown (including corruptions due to noise), you can't
  solve for a single, absolute answer; the best you can do is estimate
  a probability distribution over the possible inputs that produced the
  observed output.]]

* Solving an inverse problem requires a mathematical relationship between the
  observations (the data) and the target. That relationship introduces more
  information by imposing additional structure not present in the data alone.


.. Flight reconstruction as a filtering problem

* [[Define *flight reconstruction* as the process by which you estimate the
  unknown state variables given the inputs.]]

* [[Present *flight reconstruction* as a *filtering problem*, which will
  introduce the recursive filtering equation. The filtering equation needs
  a *transition function* (which for a continuous-time model appears as
  a differential equation).

  **This is where I motivate** :math:`\dot{\vec{x}} = f(\vec{x}, \vec{u})`,
  which is what `glidersim` provides: parametric models to produce the
  :math:`\dot{\vec{x}}`. Refer back to :eq:`state-transition`, which is where
  `x-dot` first appeared.]]

  For the "fundamental recursions", see
  :cite:`kantas2015ParticleMethodsParameter`, Eq:3.1 through Eq:3.3

  [[Good place to cite :cite:`davey2016BayesianMethodsSearch`?]]


Conclusion
----------

[[Need a segue into the next section.]]

[[FIXME: in previous iterations I started with the target being the joint
probability over the sequence of wind vectors given the sequence of states,
`p(w|x)`, declared it as intractable, then used the Markov property to
motivate sequential estimation. Does that still deserver a mention? In the
current write-up I effectively took a short-cut by starting with the informal
description and translating it into probabilistic terms.]]


Parametric paraglider modeling
==============================

.. This section sets up the entire paper!

   1. Specification: how you create the model (choice of parameters)

   2. Functionality: what the model must do


The previous section established that flight reconstruction requires
a dynamics model of the aircraft that produced the data. Unfortunately,
paraglider flight records do not include a model of the aircraft, so one must
be created. The model must be capable of simulating commercial paraglider
wings under the entire range of flight conditions that could have
realistically occurred during the flight. This intended application
significantly constrains how the model must be specified and places demanding
requirements on the functionality it must provide.


Specification
-------------

The physical model must be able to capture the essential details of the
physical system given the available data. This is not trivial for commercial
paraglider wings, because the available data is severely limited:
manufacturers only provide summary measurements, such as total surface area,
span, and number of cells, as well as information necessary for repairs, such
as individual suspension line lengths. Because the official specifications are
so limited, they must be augmented with domain expertise to "fill in" the
missing structure. Parametric models replace explicit geometry data with
parametric functions that encode assumptions of the unknown structure. The
parameters summarize the structure, simplifying the specification in order to
reduce the time and data required to create a model. As a result, it is vital
that a model can be specified in terms of parameters that can be inferred from
the available data.

.. FIXME: list the available data? Official manufacturers specifications,
   physical measurements, photos and videos, safety specification reports, etc


Functionality
-------------

The dynamics model should be able to capture the behavior of the system over
the entire range of flight conditions that will be encountered during flight
reconstruction. However, due to the severely limited sensor data, flight
reconstruction is necessarily limited to relatively simple scenarios; it would
be unreasonable to expect reconstruction of flights involving extreme
scenarios such as acrobatic maneuvers, deep stalls, and wing collapses.
Instead, this project is deliberately limiting itself to a model that would
enable flight reconstruction of paraglider flights under "average" flight
conditions.


.. What are some explicit goals and non-goals of the model functionality?

The precise model fidelity required for accurate flight reconstruction is
unclear, so this paper is a "best effort" attempt at predicting [[that. To
guide the development, here are several explicit goals and non-goals of the
final paraglider dynamics model:


[[FIXME: this is messy. These affect the component models, the system models,
and sometimes both (eg, choice of control inputs).]]

Goals:

* Must support the most common control inputs for a paraglider: left brake,
  right brake, accelerator, and weight shift.

  The control schemes of parafoil-payload systems are not suitable for
  paraglider modeling. Although some parafoil-payload models include a control
  input for "rotating" the canopy, it is not easily mapped onto the physical
  geometry of a paraglider, which is more easily described using explicit
  changes to line lengths.

* Must support the [[amounts]] of rotation and sideslip that occur during
  average paraglider flights.

  Either way, longitudinal-only models (that assume head-on relative wind) are
  clearly inadequate in the general case.

* Must support a large operating range for angle of attack

* Must demonstrate graceful performance degradation as the angle of attack
  approaches stall conditions.

  Most models use simplified aerodynamics that assume small angles of attack,
  which is frequently a poor approximation during paraglider flights. It is
  expected that accuracy will degrade near stall, but it should not fail
  outright, and its predictions should be reasonable.

* Must support non-uniform wind velocities across the canopy (eg, when the
  wing encounters wind shear, indirect thermal interactions, etc)

  I'm interested in demonstrating the significance (or non-significance) of
  non-uniform relative wind (instead of assuming it is negligible).

* Must support variable air density.

  In practice this is a reasonable assumption, but a fixed value of air
  density should not be encoded in the model.

* [[Must support non-uniform section coefficients, in order to support
  approximate models of existing wings. This affects both the canopy geometry
  and the canopy aerodynamics component models.]]

* Must account for the effects of :ref:`paraglider_components:Apparent mass`

  As with non-uniform relative wind, the significance of apparent mass effects
  should be demonstrated before assuming it is negligible.

* Must support non-fixed payload orientations.

  The significance of relative payload motion should be determined before
  assuming it is negligible. Also, during average flight conditions the
  payload can be reasonably well described with a fixed orientation, but which
  orientation to use for static conditions and the effects of that restriction
  during dynamic conditions must be reviewed.


Non-goals:

* Canopy deformations (no riser control, no wing collapses, etc)

* Acrobatic maneuvers (rapid accelerations, extreme angles of attack, etc)


.. What are some examples of scenarios I would like to simulate?

[[Another way to specify the target functionality is through specific
scenarios, such as:

* A wing that encounters a thermal during a turn. The thermal core may be
  located towards the inside wing tip, the center of the wing, or the outside
  wing tip.

* [[FIXME: more interesting scenarios here]]


Roadmap
=======

.. "Brief indication of how the thesis will proceed."

This project designs and implements a parametric paraglider dynamics model
suitable for paraglider flight reconstruction. The modeling process begins in
:doc:`foil_geometry`, which develops a novel parametric geometry specifically
tailored for the non-linear details of typical paraglider wings.
:doc:`foil_aerodynamics` establishes basic performance criteria for selecting
an aerodynamics method suitable for analyzing paraglider motion, and presents
an adaptation of a non-linear lifting line method that meets those criteria.

Given the geometric and aerodynamic models of the paraglider canopy, it will
design a complete set of :doc:`component models <paraglider_components>` and
combine them into the final :doc:`system models <paraglider_systems>`. The
final step that enables a dynamics model to produce a flight simulation is to
choose a suitable set of state variables, and link the state dynamics to the
paraglider system dynamics.

To conclude the primary contributions of this paper, :doc:`demonstration`
presents an example that uses the parametric model to approximate a commercial
paraglider wing, compare static performance analyses to expected results, and
demonstrate several dynamic scenarios to highlight the flexibility of the
model.

In closing, :doc:`future_work` briefly surveys the remaining steps to solving
the flight reconstruction problem, extracting wind field patterns from sets of
recorded flights, and encoding those patterns into a predictive model.
