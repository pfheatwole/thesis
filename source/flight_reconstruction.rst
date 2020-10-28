*********************
Flight Reconstruction
*********************

.. Meta:

   * Introduce inverse problems and filtering problems

   * Argue that full flight reconstruction is necessary for wind vector
     estimation

   * Motivate the paraglider dynamics model.

   * It should convert the informal problem statement (turning sequences of
     positions into sequences of wind vectors) into the formal problem
     of flight reconstruction.

   * It should establish flight reconstruction as a filtering problem. It
     should not discuss filtering architectures for solving the filtering
     problem.


   * It should introduce all the state variables (paraglider, controls, and
     wind), the basic form of the paraglider dynamics function, the notion of
     a parametric paraglider model, parameters of that model, etc.

   * The big objective of this paper is to argue that there exists *some* path
     towards estimating wind vectors from position data. The objective of this
     chapter is to argue that the complete system dynamics (paraglider,
     controls, and environment) are *necessary* to solve the filtering problem.
     It should not attempt to argue that the system dynamics are *sufficient*
     to solve the filtering problem.

   * It should leave the reader with a clear map of the steps that would be
     required to use the dynamics to perform flight reconstruction.



Key points:

* To estimate the wind fields, we need the wind vectors.

  [[Jumping the gun here: the more general problem is "we need a relationship
  between the wind field and the paraglider's change in position over time"]]

* Flight tracks don't record wind vectors; they only record position.

* We need a relationship between glider position and the wind so the position
  data can be used to estimate the wind.


* The key insight is that the data was produced by some *data-generating
  process*.

* The mathematical model of the *data-generating process* encodes the
  relationships between all the variables involved in producing the positions.

* If we have that mathematical model we can use it to estimate the unknown
  quantities.

* For paraglider motion, the sequence of positions is the result of the
  paraglider dynamics. The paraglider dynamics are the result of interactions
  with gravity and wind. The interactions with the wind are described by the
  canopy aerodynamics.

* Thus, we can use the paraglider dynamics as the link between between what we
  know (changes in position over time) to gain information about what want to
  know (the wind vectors encountered during the flight).


* We are observing an effect (changes in position) and attempting to infer the
  cause (wind vectors). Mathematically this is known as an *inverse problem*.
  The sequence of positions are the output of some function that describes the
  motion of the paraglider in response to some inputs; we seek to determine
  the inputs.


* [[Discuss solving systems of equations? Seems like a good place to introduce
  the idea of "solving" underdetermined systems.

  Solving inverse problems is like solving systems of equations: to solve for
  the unknowns you need enough information, where "information" comes in two
  forms: data, and relationships. We don't have enough data, and probably
  can't obtain more (beyond general meteorology information, elevation models,
  etc), so we must try to introduce extra relationships until we have enough
  information.

  Sometimes though there simply enough enough information to completely
  determine the state of all the variables. Such *underdetermined systems*
  cannot be solved exactly; they can only be constrained to some limited
  range. The question then is not "is the value known precisely?" but rather
  "is the value known well enough to be useful?"


* Like most real-world inverse problems, there is uncertainty in every aspect
  of this model: the position sequences are noisy measurements of the true
  position, the paraglider dynamics are an approximation of the true model,
  etc.

  Thus, a complete solution to the inverse problem must provide *uncertainty
  quantification* along with any answer. This is not a measure of the true
  accuracy, but at least it summarizes all the uncertainty that the model is
  aware of.

* "The idea of using the math of probability to represent and manipulate
  uncertainty is commonly referred to as *Bayesian statistics*"
  (`schon2018ProbabilisticLearningNonlinear`)

  Bayesian statistics is a framework for reasoning through conditional
  probability.


* At this point it can be helpful to rewrite our problem statement in
  probabilistic terms.

* Our original goal of estimating the wind vectors given the observed data is
  equivalent to saying we need to estimate the probability distribution over
  wind vectors given the data, written as `p(wind | data)`.

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

* [[find `p(wind | data)` by estimating the full joint pdf then marginalizing
  the *nuisance variables*]]

* We can't estimate the full joint pdf directly since it's also intractable,
  but thankfully the process model satisfies the *Markov property*. *Markov
  processes* are intuitive to represent as a state-space model. State-space
  models can be used to decompose the joint pdf into independent factors which
  a be estimated recursively to build up the full joint distribution.

* The objective now is to use the state-space model to build up the full joint
  distribution so we can marginalize the nuisance variables in order to
  compute `p(wind | data)`.




* The state-space model transition function is the key mathematical (as
  opposed to intuitive) motivation for the canopy aerodynamics




SSM
===

A basic discrete-time state space model:

.. math::

   \begin{aligned}
   \vec{x}_{k} &= f_x \left( \vec{x}_{k-1}, \vec{\delta}_{k-1}, \vec{w}_{k-1}, \mathcal{M} \right) \\
   \vec{\delta}_{k} &= f_{\delta} \left( \vec{\delta}_{k-1} \right) \\
   \vec{w}_{k} &= f_{w} \left( \vec{w}_{k-1} \right) \\
   \vec{z}_k &= g \left( \vec{x}_k \right)
   \end{aligned}


And what would it look like in a Bayesian filtering problem?


.. math::

   p_{\mathcal{M}} \left( \vec{x}_{0:K} \given \vec{z}_{0:K} \right) =
     p_{\mathcal{M}} \left( \vec{x}_{0:K-1} \given \vec{z}_{0:K-1} \right)
     \frac
       {
         p \left( \vec{x}_{k} \given \vec{x}_{k-1}, \vec{\delta}_{k-1}, \vec{w}_{k-1}, \mathcal{M} \right)
         p \left( \vec{\delta}_{k} \given \vec{\delta}_{k-1} \right)
         p \left( \vec{w}_{k} \given \vec{w}_{k-1} \right)
         p \left( \vec{z}_k \given \vec{x}_k \right)
      }
      {p \left( \vec{z}_k \given \vec{z}_{0:k-1} \right)}


Or, for the full flight reconstruction problem:

.. math::

   p \left( \vec{x}_{0:K}, \vec{\delta}_{0:K}, \vec{w}_{0:K} \given \vec{z}_{1:K} \right) =
     \prod_{k=1}^K \Big\{
       p \left( \vec{z}_k \given \vec{x}_k \right)
       p \left( \vec{x}_k \given \vec{x}_{k-1}, \vec{\delta}_{k-1}, \vec{w}_{k-1} \right)
       p \left( \vec{\delta}_k \given \vec{\delta}_{k-1} \right)
       p \left( \vec{w}_k \given \vec{w}_{k-1} \right)
     \Big\}
     p \left( \vec{x}_0 \right)
     p \left( \vec{\delta}_0 \right)
     p \left( \vec{w}_0 \right)
     p \left( \mathcal{M} \right)


**Maybe I should introduce a general form of this equation when I'm talking
about state-space models, then refer back to it. Don't define this explicitly
(what does it add to the discussion?), leave it in state-space model form.**



* "State-space models can be used to incorporate subject knowledge on the
  underlying dynamics of a time series by the introduction of a latent Markov
  state-process." (:cite:`fearnhead2018ParticleFiltersData`)

  We tend to do this without realizing it: when we watch a paraglider moving
  around in the air, we use our intuition of wing performance (how the wing
  interacts with the wind) to get a feeling for what the wind is doing. We
  incorporate use our experience with wing dynamics to estimate the wind.




MISC
====

* **I strongly support using `=` for the state-space model, and `~` for the
  resulting statistical model.**

* The motivating questions of this paper must be transformed into a set of
  mathematical equivalents before we can apply tools that estimate their
  answers. This chapter converts the informal problem statements from the
  introduction into formal, probabilistic relationships.

  This step involves acknowledging the inherent uncertainty in the data and
  their models, defining the underlying, probabilistic form of the questions,
  and using the rules of conditional probability to decompose the problem into
  a series of intermediate steps.


* Good books on state estimation:

  * "Optimal State Estimation" (Simon; 2006)

  * "Time series analysis by state space methods" (Durbin, Koopman; 2012)

* The starting point for any statistical analysis should be to understand the
  *data-generating process*. If your target is directly involved in the DGP,
  then great, you've got statistical dependence to work with. If not, you'll
  need to introduce additional relationships to induce statistical dependence
  between the observed variables and the target.


* "Probabilistic learning of nonlinear dynamical systems using sequential
  Monte Carlo", page 4, equation 7. In fact, just reread Sec:2 until it
  clicks. This is probably the crux of how I motivate the paraglider dynamics.


* What is *flight reconstruction*?

  * In this paper, the term *flight reconstruction* refers to this process of
    estimating the complete state of the flight at each time step. The rest of
    this chapter defines the "complete state", why it is necessary, etc.

  * [[Should this have been established in the Introduction? Or is this part
    expanding on / formalizing the ideas proposed in the introduction?]]

  * [[Might be a great place to mention the MH370 paper; that's a relatable
    example of a flight reconstruction problem. That paper also has a nice
    introduction to the *Chapman–Kolmogorov equation* which I should
    reference.]]

* What is the intuition behind *flight reconstruction*?

  * Conditional probability is the key, in SO many ways

    * Relates what we know to estimate what we don't

    * Enables decomposition (eg, Markov processes -> recursive estimation)

* What makes the task difficult?

  * We don't have any measurements of the thing we're estimating; we only have
    measurements of a variable which is **related** to it.

  * There is uncertainty everywhere: the dynamics, the other state variables,
    even the measurements are noisy.

* It is essential to acknowledge the inescapable uncertainty throughout these
  questions. Even the small amount of data we do have (a sequence of positions
  over time) is uncertain due to sensor noise and encoding inaccuracies
  (quantization error). When uncertainty cannot be eliminated, it no longer
  makes sense to look for exact answers, but rather for the distribution that
  covers the plausible range of answers. This is the realm of probabilistic
  methods.


* What is simulation-based filtering? How does it deal with underdetermined
  systems?


* Individual positions tell you nothing except the fact that a pilot chose to
  be flying that day. It suggests reasonable flying conditions, but you don't
  even know what (the weather could have changed, the wing may be unusually
  high performance, or the pilot could just be crazy). The information is how
  the position changes over time.




* State-space models:

  * Model the evolution of some state over time, with (potentially noisy)
    observations of that state.

  * The idea is to implicitly describe the trajectory using repeated *steps*
    generated by the state transition function.

  * The *filtering problem* is to produce an estimate of the current state given
    all the observations up to the current time.

  * The observations 

* Although a filtering architecture could estimate the wind vectors
  concurrently with the wind field regression model, for simplicity this
  chapter assumes these steps are separate. In particular, it models the
  sequence of wind vectors as a Markov process, so it can't incorporate the
  wind field regression model into the prior for each wind vector.

* We're trying to relate motion to wind vectors, and that relationship is
  defined by the canopy aerodynamics, so any solution must utilize the canopy
  aerodynamics.

* This inverse problem isn't deterministic: it's stochastic. There is
  uncertainty in the data, wind, controls, and model, so a complete solution
  should provide *uncertainty quantification*. Instead of providing an exact
  answer, there will be ranges of answers and their estimated probabilities.

* Estimating the values of a stochastic process is a *statistical filtering
  problem*.

* Estimating the joint probability directly is intractable, but the Markov
  property allows the problem to be rewritten in a tractable form: the
  *recursive filtering equation*.

  [[Old phrasing: "Statistical filtering problems involving values that evolve
  over time can be modeled with the *recursive filtering equation*."]]

* The recursive filtering equation is composed from a set of priors
  (probabilities before seeing any data), a transition function (a dynamics
  model), and a likelihood function (an observation model).

* The transition function is how we "introduce more information" into the
  problem (via the aerodynamics).

* Writing the wind vector estimation task in terms of the recursive filtering
  equation also reveals that there are several subtasks:

  1. State estimation

  2. Parameter estimation (aka model estimation)

  3. Input estimation (wind and control vector sequences)

* "Solving" the filtering problem simply means "estimate the joint probability
  distribution", then *marginalize* the "nuisance" variables (control inputs,
  model parameters, etc) to compute the joint distribution over the position
  and wind vectors. (*Nuisance variables* aren't interesting by themselves,
  but they must be accounted for: the targets depend on the nuisance
  variables, and so the uncertainty of the nuisance variables must be
  incorporated into the uncertainty of the target variables.)

* In shorter form, given a statistical model (in the form of the state-space
  model) we want to compute the posterior over the states, inputs, and model
  parameters.

  (See "Philosophy and the practice of Bayesian statistics"; Gelman and
  Shalizi, 2013, pp11-12)


* This paper will not discuss filtering architectures for solving the
  filtering problem (this includes all of state, parameter, and input
  estimation). **The focus of this work is on the dynamics model, which
  provides the transition function.**




SCRATCHWORK
===========

* The ultimate goal that motivated this project is to produce a predictive
  model that can estimate the wind vectors at unobserved locations in the wind
  field given measurements of other points in the wind field.

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

* The term *flight path reconstruction* seems to have a particular meaning in
  some portions of the aerospace community, where it is used to indicate
  kinematics-based state estimation as a component in model validation and
  calibration. (For a good survey on this topic, see
  :cite:`mulder1999NonlinearAircraftFlight`.) As a kinematics-based method,
  the models are built around *specific forces* and angular rates instead of
  aerodynamic forces and moments. As such, it is more concerned with
  **describing** and aircraft's motion instead of **explaining** its motion.
  (Counterpoint: the MH370 paper calls their methods "flight path
  reconstruction", and they incorporate things like maneuvers, which are not
  pure kinematics?)

  I'm calling my efforts in this paper "flight reconstruction" because it's
  not just the path of the wing I'm interested in. I'm also reconstruction the
  environment of the flight (the wind and control inputs).

* Flight reconstruction as a *state estimation* problem. State estimation
  might mean improving an estimate of an observed quantity, or it could mean
  producing an original estimate of an unobserved quantity.

* Performing *parameter estimation* implies that you have a parametric model
  in the first place.

* In most aerodynamic literature, when they talk about *parameter estimation*
  they typically have access to the aircraft in question and can execute
  a specific set of maneuvers to learn the behavior of the system. I have no
  access to the wing, no knowledge of the control inputs, and the maneuvers are
  assumed unsteady (not the result of the control inputs alone).


Statistical filtering
---------------------

* Although you could estimate the regression model for the wind field at the
  same time as you're estimating the wind vectors (and indeed, this would
  theoretically perform better), it's easier to model the wind vectors as
  a Markov process.

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




Subtask breakdown
-----------------

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
-------------------------------

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
-------------------

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
------------------------

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
