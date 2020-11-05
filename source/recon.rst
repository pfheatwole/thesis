[[This is a scratchfile for the "Flight Reconstruction" chapter]]


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
