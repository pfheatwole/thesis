This isn't (currently) a planned section in the thesis, but a holding place
for some scattered thoughts related to all things flight reconstruction.
Really, establishing the idea of "flight reconstruction" will probably happen
in the introduction to the paper.


Modelling
=========


Pilot Control Inputs
--------------------

Should I model the pilot controls as *multivariate autoregressive Gaussian
processes*? (See `turner2011GaussianProcessesState`, section 3.6)


I'm unhappy with treating the four pilot controls as independent random walks
(for the purpose of my filtering method), since that will generate mostly
nonsense control sequences. There are several considerations for generating
realistic pilot control sequences:

* Controls don't change erratically (they are generally smooth)

* Controls tend to change together (you don't want full left brake and right
  weight shift, or full symmetric braking together with full speedbar)

* Controls tend to be the result of a pilot attempting some maneuver (so you
  can consider the controls a latent process of the unobserved "maneuver")


For controlling smoothness, maybe an *integrated Ornstein-Uhlenbeck process*
(which I think is like integrating a random walk over acceleration?), or
a Gaussian process with an appropriately smooth kernel.

For correlated controls (ie, how they vary together), I may want to think of
the pilot controls as points on some "data generating manifold". This idea
shows up in animation, using low-dimensional manifolds for generating
high-dimensional human skeletal animations; see Wang's thesis
`wang2005GaussianProcessDynamical`. The manifold is a kind of constraint on
how the variables change together.

For maneuvering, I have done no research, but this is important for realistic
maneuvers. Without encoding a notion of maneuvers, you'll get very poor
performance during constant input sequences, like during a 360. (Random walks
and their ilk will be very unlikely to produce fixed brake positions, which
are essential to smooth flights.)


Notes to self in case Foxit crashes:

* I'm currently reading "Pattern Recognition and Machine Learning", chapter 12
  (continuous latent variables). I might then follow up with chapter 6 on
  "kernel methods".

* In Bishop, Chapter 6, page 296 (314), he has "Techniques for constructing
  new kernels"


Using a Gaussian process for the pilot controls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Gaussian process is good for enforcing smoothness, and since they're good
for human animation they're probably also good for handling the correlations
and maneuvers. Another big advantage is that Gaussian probabilities are the
easiest to combine with other methods that expect Gaussian random variables
(eg, you can use the mean+covariance directly inside the GMSPPF?). I'm hoping
that I can make the GMSPPF work together with the GP (the GMSPPF samples from
the GP prior and updates the GP by using the posterior mixture as
pseudo-observations), but there's a problem: **the GMSPPF seems nice for
producing the filtering distribution, but not so nice for generating plausible
state trajectories since the particles don't retain ancestor information**
(you know the state distribution at each point, but for any point in that
distribution you don't know the state distribution that led to that specific
point).

Aah, but wait: sure, that Gaussian mixture is a big lumpy distribution, but
can't you just compute queries using each individual Gaussian mixture
component **as if it was the only one** and adding their results?

FULL STOP, THINK ABOUT WHAT YOU'RE DOING

I've lost sight of the purpose here. The purpose of the GMSPPF is to drive
forward the state of the wing (namely, it's pose); the evolution of that state
is the result of the wing dynamics, given the wind and pilot controls as
inputs. But what if I don't know the pilot controls? I need to place
a distribution over that set of random variables as well; I also need
a transition function to let them evolve over time, which means I need
a dynamics model for the pilot controls. The dynamics model should encode
realistic behaviors; I am thinking a Gaussian process is a good way to produce
that encoding.


Maneuvering Target Tracking
---------------------------

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


Filtering
=========

Forward versus Inverse Problems
-------------------------------

"Inverse problems include both parameter estimation and function estimation.
[...] A common characteristic is that we attempt to infer causes from measured
effects. A forward, or direct problem has known causes that produce effects or
results defined by the mathematical model.  Because the measured data is often
noisy or indistinct, the solution to the inverse problem may be difficult to
obtain accurately."

**Can I say that my application of particle filtering is to use a forward
problem (the flight simulator) to produce a solution to the inverse problem?**

Inverse problems are about inferring causes from the observed effects; seems
like a good description of what I'm doing (only I have a tiny sample of
observed effects; namely, a change in position over time).


Probabilistic inference / simulation-based filtering
----------------------------------------------------

I liked this sentence in Duvenaud's dissertation: "*Probabilistic inference*
takes a group of hypotheses (a *model*) and weights those hypotheses based on
how well their predictions match the data." **I often use the term
"simulation-based filtering", but maybe I should review that term.**

"**data** driven forecasting" vs "**model** driven forecasting"

See `reich2015ProbabilisticForecastingBayesian`

* Model driven: eg, by analyzing topography (for example, RASP)

* Data driven: eg, by analyzing flight tracks (like von Kaenel's thesis)

Basically, do you look at the observations alone (with no though to the
underlying model), or do you also refer to the "surrogate process" from which
they were generated?

He describes "data-driven" as "bottom-up", or *empirical* models, whereas
"model-driven" are "top-down" or *mechanistic* models. Empirical models rely
on the data, mechanistic models rely on the model dynamics.

On page 182: "model-based forecast uncertainties taking the role of prior
distributions"



Data Assimilation
-----------------

*Data assimilation* is to geophysics what *filtering* is to engineering. They
both deal with the *state estimation problem* by combining theory (models)
with observations (data). See `fearnhead2018ParticleFiltersData`. (I like this
paper. One of its stated goals is to encourage interoperability between
geophysics and engineering disciplines. Section 1.2 has a very helpful
overview of the related terminologies of the two fields.)

I should try to phrase my problem in terms of both, or however makes sense to
tie in the geophysics realm. There's probably a bunch of good literature to
cite.


Validation
----------

I read somewhere that a guy complained about testing your model by fitting it
against simulated data (or something; he didn't like the idea that "yay, we
recreated data we expected!" was not helpful). Gelman, on the other hand, is
a huge fan of *fake-data simulation*, where you generate data from a model
using "true" parameters, then observing the behavior of the statistical
procedures (how well they work, how they fail). There is a related procedure
called *predictive simulation*, where you fit a model, generate data from it,
then compare that generated data to the actual data (I believe this is also
called *posterior predictive checking*). See
:cite:`gelman2007DataAnalysisUsing`.


The *curse of dimensionality* refers to needing **more** data as the dimension
increases, so you have to pursue the *blessing of abstraction*: the more
structure you account for, the **less** data you need. (FIXME: I don't think
this is the correct use of the phrase *blessing of abstraction*, which refers
to the observation that sometimes its easier to a learn general knowledge
faster than specific knowledge?)

   ^^ This is a concept I need to highlight in my thesis, since it motivates
   my detail efforts. The more information I want to squeeze out of the data,
   the more structure I need to introduce. You don't get something for
   nothing: for every question you want to answer, you need either need more
   data or more structural information (like paraglider wing dynamics)


Jittering
---------

If the process noise is small, you don't get much variation in the particles
during the time update. One way to decrease the odds of sample impoverishment
is to use *jittering*. See `fearnhead1998SequentialMonteCarlo`, page 53


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


Proposal Distributions
----------------------

The great issue then becomes the number of proposals necessary to get a good
empirical estimate of the true state probability distribution; in general, the
number of proposals depends on the number of state variables, which means
a large number are required for estimating all of the model, wind, and control
input states. Because the paraglider model dynamics are computationally
expensive, it is prohibitively expensive to generate individual predictions
for a large number of proposals. For this reason a naive particle filter
design is infeasible; more sophisticated particle methods are required.

In this particular case it is helpful to realize that although the
aerodynamics are expensive to compute, evaluating the likelihood of each
prediction is cheap, since it is a simple distance calculation (the predicted
position versus the measured position). The Gaussian mixture sigma-point
particle filter (GMSPPF) utilizes this realization by replacing entire groups
of particles that are nearby in the state space with a mixture of Gaussians;
instead of propagating individual particles through the expensive dynamics,
you propagate entire regions of the state space by propagating each mixture
component using an unscented Kalman filter, then regenerate particles and
their weights using the inexpensive likelihood. This method can reduce the
number of expensive dynamics evaluations by several orders of magnitude.
