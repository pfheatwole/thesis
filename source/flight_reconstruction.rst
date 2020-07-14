*********************
Flight Reconstruction
*********************

The questions in this paper must be transformed into a set of mathematical
equivalents before we can apply tools that estimate their answers.

This involves acknowledging the inherent uncertainty in the data and their
models, defining the underlying form of the questions, and using the rules of
conditional probability to decompose the problem into a series of intermediate
steps.


Probabilistic Methods
=====================

It is essential to acknowledge the inescapable uncertainty throughout these
questions. Even the small amount of data we do have, the sequence of positions
over time, is uncertain due to sensor noise and encoding inaccuracies. When
uncertainty cannot be eliminated, it no longer makes sense to look for
specific answers, but rather for the distribution that covers the range of
plausible answers. This is the realm of probabilistic methods.

The starting point is to recognize that all the questions in this paper follow
a general form: "what is the value of *this* given the value of *that*?"
Answers depend on the relationships between variables.


The mathematical framework for reasoning through conditional probability is
the language of *Bayesian statistics*.

The underlying philosophy of Bayesian statistics is the use of probability to
describe uncertainty.

This section provides a Bayesian formulation of the goals of this project.


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
