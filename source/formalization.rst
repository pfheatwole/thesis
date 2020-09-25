****************************
Formalized Problem Statement
****************************

[[**FIXME**: this chapter needs a good title]]

The questions in this paper must be transformed into a set of mathematical
equivalents before we can apply tools that estimate their answers. This
chapter converts the informal problem statements from the introduction into
formal, probabilistic relationships.

This step involves acknowledging the inherent uncertainty in the data and
their models, defining the underlying form of the questions, and using the
rules of conditional probability to decompose the problem into a series of
intermediate steps.


Order of events:

1. Reiterate the problem statement: learning wind patterns from a set of
   tracks, which first requires learning the wind fields from individual
   tracks.

#. Learning the wind fields requires some relationship between what we know
   (flight tracks) and what we want (wind fields). That relationship comes in
   the form of paraglider dynamics. (**This is the motivation for my
   paraglider dynamics model.**) Using the dynamics to build a set of
   proposals is the realm of *simulation-based filtering*.

#. Because the paraglider dynamics require more than just wind, we must
   estimate all the components of the flight used by the dynamics. Recreating
   the entire state of a flight is what I'm calling "flight reconstruction."

**Where in these steps should I establish the necessity of acknowledging the
inherent uncertainty?** 


SCRATCHWORK
===========

Goals:

* Break the informal problem statement into subtasks

* Demonstrate the need for dealing with uncertainty

* Introduce filtering methods

* Formalize the subtasks in the language of probability [[Don't define the
  distributions, just use probabilistic relationships to acknowledge their
  existence]]

* Conclude with the need for a paraglider dynamics model


Outline:

1. Introduction

   1. Restate the informal problem statement

   #. Break the informal task into informal subtasks [[no probability yet]]

      [[Maybe develop the ideas "in reverse", then summarize in order?]]

      1. Estimate wind vectors from position

      #. Estimate wind field regression model for an individual track

      #. Build a set of regression models

      #. Pattern detection over the set of regression models

      #. Encode a predictive model

   #. Highlight the focus of this thesis: estimating the sequence of wind vectors

      * The predictive model motivates the sequence of events, but it all starts
        with getting the wind vector time-series.

      * We have uncertain position data and unknown wind, controls, and model.
        That uncertainty motivates a probabilistic formulation.

#. Probabilistic filtering

   * [[For now, assume this chapter has already been written. This section
     lets me assume the reader has all the knowledge they need for me to dive
     right into "here's my problem as a particle filtering problem"]]

   * Managing uncertainty through Bayesian probability

   * Uncertainty propagates through everything, so EVERYTHING is described in
     terms of distribution

   * Conditional probability is the key, in SO many ways

     * Relates what we know to estimate what we don't

     * Enables decomposition (eg, Markov processes -> recursive estimation)

   * Filtering problems

   * Filtering frameworks [[simulation-based filtering, in particular]]

   * Predictive models? (only seems relevant for understanding the ultimate
     goal)

   * Regression models? (only seems relevant once you get to the point of
     estimating wind fields from the wind vectors)

#. Formulate "wind vector estimation" as a probabilistic filtering problem

   * Probably a good spot to formalize what I mean by *flight reconstruction*

   * Should I focus on just the "wind vector estimation" problem, relying on
     that informal logic, or should I work backwards ("we want a predictive
     model, which requires a set of patterns, which requires ..."), writing
     each one as a general probabilistic formulation?

     I kind of like the idea of reiterating that "reverse order" derivation in
     a more structured way; we'll see how icky the math gets.

   * Don't choose any particular filtering architecture at this point, just
     write the basic probabilist relationships.

   * Every particle filter will need a proposal distribution and a likelihood

     * **The proposal distribution motivates the need for a paraglider
       dynamics model.** The dynamics depend on the wind and control inputs,
       so we need dynamics (proposals) for those too.

     * Not sure how I'll deal with the likelihood, if at all. I probably have
       enough just getting through the dynamics...




[[[[[[[[[[]]]]]]]]]]


* What is the ultimate goal that motivated this project?

  * The ultimate goal is to produce a predictive model that can estimate the
    wind vectors at unobserved locations in the wind field given measurements
    of other points in the wind field.

  * [[Maybe use language like "patterns", etc]]



* What are the subtasks?

  * Finding patterns in wind field regression models requires a set of wind
    field regression models.

  * Finding individual regression models requires estimating the wind vectors
    at individual points in time.


* How do you use position to estimate wind?

  * [[What does position tell you about wind?]]

  * Individual positions tell you nothing except the fact that a pilot chose
    to be flying that day. It suggests reasonable flying conditions, but you
    don't even know what (the weather could have changed, the wing may be
    unusually high performance, or the pilot could just be crazy).

  * You need a sequence of position over time to learn anything.




  * "State-space models can be used to incorporate subject knowledge of the
    underlying dynamics of a time series by the introduction of a latent Markov
    state-process."

  * The basic strategy is one of guessing everything that could have happened,
    eliminate the implausible scenarios, then reason about what's left.
    Mathematically, the goal is to generate a large set of "proposals" (guesses)
    that are consistent with the dynamics (ie, we need to guess everything that
    could *conceviably* happen) and weight them according to how compatible they
    are with the data (give them a plausibility score based on how likely the
    measurement would be if the proposal was what really happened).

  * Proposals are changes to the state that could happen given our knowledge of
    the dynamics. Instead of saying "anything could happen" we assume some
    things are impossible (such as the wing flight at the speed of light or
    accelerating at 10g), which constrains what could have happened. We then
    look at the measurement and constrain the possibilities even more. What's
    left might be usefully precise, or it might still be vague.

  * Recursive estimation accepts that you can't generate a proposal for the
    entire trajectory in one go, so instead you generate proposals for each
    time step sequentially. This assumption typically involves a Markov
    assumption to simplify the math.


* What makes the task difficult?

  * We don't have any measurements of the thing we're estimating; only have
    measurements of a variable which is related to it.

  * There is uncertainty everywhere: the dynamics, the other state variables,
    even the measurements are noisy.


* How do you manage uncertainty?

  * The language of probability.


* What probabilistic tools/frameworks are available?

  * Particle filters / sequential Monte Carlo


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



* Although you could estimate the regression model for the wind field at the
  same time as you're estimating the wind vectors (and indeed, this would
  theoretically perform better), it's easier to model the wind vectors as
  a Markov process.

]]


Managing Uncertainty
====================

It is essential to acknowledge the inescapable uncertainty throughout these
questions. Even the small amount of data we do have (a sequence of positions
over time) is uncertain due to sensor noise and encoding inaccuracies
(quantization error). When uncertainty cannot be eliminated, it no longer
makes sense to look for exact answers, but rather for the distribution that
covers the plausible range of answers. This is the realm of probabilistic
methods.

The starting point is to recognize that all the questions in this paper follow
a general form: "what is the value of *this* given the value of *that*?"
Answers depend on the relationships between variables.


The mathematical framework for reasoning through conditional probability is
the language of *Bayesian statistics*.

The underlying philosophy of Bayesian statistics is the use of probability to
describe uncertainty.

This section provides a Bayesian formulation of the goals of this project.


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

   This is the "flight reconstruction" step, so really what you're doing is
   building an estimate of the probability distribution over the wind,
   paraglider model, and pilot inputs, then marginalizing over model and
   controls to get just the distribution over the wind.

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
     modelling spatial correlations equates to choosing a proper kernel
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

[[This section is as much for myself as anything, as I attempt to formalize
the description from the introduction into probabilistic terms. I would like
to start with the kernel of the idea and iteratively refine the details,
expanding the question complexity while converting the details into
mathematical form. The goal is to walk the reader through the development of
the idea and how the math motivates the design path.]]


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


Predictive Modeling
===================

[[On a track-by-track basis, I'm trying to estimate, or "learn", the wind
velocity field as a function of position. But more than that, I am proposing
that the wind field has regular patterns that depend on the time of day, day
of the year, and weather conditions. Conceivably there is a useable set of
wind field models that capture recurring elements. If you know the historical
patterns then if you can figure out the likely current configurations then you
should be able to predict the unobserved parts of the wind field.]]

You want to use observations to predict the current state. (Not sure "predict"
is the right word here though; it's more like "estimation", except that
estimation in statistics means "estimating the true value of the observed
thing", whereas I'm trying to estimate the value of the **unobserved** thing.)

* Given a model, you would like to predict the value you would observe at
  other points in the wind field.

* Static models that simply summarize historical averages or rates aren't
  useless, but they are pretty boring; for example, in Michael von Kaenel's
  thesis the conclusion was simply "stay along the ridge", which pilots
  already know.

  Instead, we want a probabilistic model that gives answers that have been
  **conditioned** on some *set of observations* :math:`\mathcal{O}
  = \left\{x\right\}`. But there are multiple levels to this: a simple kriging
  model can use just the current observations to try and build a regression
  model over the current state, but conceptually the trained model is
  essentially using the historical data as "pseudo-observations". You're not
  just conditioning the answer based on current observations, but on the
  historical observations as well. Mathematically, we say that the historical
  data is encoded in a *model* :math:`\mathcal{M}`, so the distribution
  becomes :math:`\vec{x} \sim p \left(\vec{x} \given \mathcal{O}, \mathcal{M}
  \right)`.

  This distinction is obvious to data science practitioners, but it's probably
  helpful to make the idea explicit for the less mathematically inclined
  reader.


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


Simulation-based filtering
==========================

* "State-space models can be used to incorporate subject knowledge on the
  underlying dynamics of a time series by the introduction of a latent Markov
  state-process." (:cite:`fearnhead2018ParticleFiltersData`)

  We tend to do this without realizing it: when we watch a paraglider moving
  around in the air, we use our intuition of wing performance (how the wing
  interacts with the wind) to get a feeling for what the wind is doing. We
  incorporate use our experience with wing dynamics to estimate the wind.


Extra Notes
===========

* Is it correct to say that the control inputs and the wind vectors are
  marginally *independent* (in the absence of the pose), but conditionally
  dependent given the pose of the wing? A gut check says yes: if you asked
  me to guess a pilot controls in the blind, I'd have to be vague, but if you
  told me they were banking to the right with a gust coming from the left,
  I'd be much more inclined to believe they were applying right brakes (and
  in the middle of a turn).

  It might help to draw the model graph for the two scenarios. Wind doesn't
  *directly* influence the controls, it does it *indirectly*, through the
  pilot's objective/strategy. The pilot's decision making process takes in
  the wind, post, and objective, and produces the control output as a
  response, but if you delete that strategy from the model graph then
  there isn't a dependency between the wind and controls; they're only
  related by their common effect: the trajectory.

  This question probably belongs together with the discussion on *maneuvering
  target tracking*.


SNIPPETS
========

* The goal of estimating the wind vector using incomplete and noisy
  observations of the system is referred to as a *filtering problem*.

  [[This term comes from the field of *stochastic processes*, which is the
  study of processes that are partly predictable and partly random.]]

* How can you estimate the unobserved wind vectors given the observed flight
  tracks?

* What is flight reconstruction? How do you accomplish it?

* What is simulation-based filtering? How does it deal with underdetermined
  systems?

* Running the particle filter over a specific flight produces a set of
  observations over points in the wind field at a specific time

* The wind is a *latent variable*. We want to infer its value from the
  observed variables.

  Sometimes the latent variable is merely an intermediate value you add to the
  model to connect the observations to the dynamics, but in this case it's the
  latent variable itself which is our target. **The goal of "wind vector
  estimation" is one of inferring a latent variable.**

  A *latent variable model* is one which "aim to explain observed variables in
  terms of latent variables"; I am attempting to explain changes in position
  by inferring the wind, and then choosing the values that gave the "best"
  explanation.

  Technically the wind could have been measured (ie, quantitatively) in
  practice, so in some contexts it would be called a *hidden variable*.

* Every subtask has it's own modeling difficulties. Like for the wind
  regression model, you have to just assume a mean value over the specified
  time interval, which is obviously going to be pretty poor for high variance
  regions. It seems likely that assumed-constant parameters in general are
  likely to struggle; stationarity, homoscedasticity, all sorts of fun
  concepts.
