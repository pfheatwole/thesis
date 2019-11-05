****************************
Introduction 2 (Alternative)
****************************

(This is an off-the-cuff Bayesian modelling approach.)

I want to know :math:`\vec{w}_{1:T}`, but I only have :math:`\vec{y}_{1:T}`,
so my target is to learn :math:`p(\vec{w}_{1:T} \mid \vec{y}_{1:T})`. To do
that I need a relationship between the sequence of flight positions and the
wind vectors. That relationship is given by the paraglider aerodynamics model
:math:`f({\cdot\,} ; M)`, which is parametrized by the wing model :math:`M`.

If we knew :math:`M`, we might try to target :math:`p(\vec{w}_{1:T} \mid
\vec{y}_{1:T}, M)`, but the aerodynamics model also requires the pilot inputs
:math:`\vec{\delta}_{1:T}`, so we are forced to target :math:`p(\vec{w}_{1:T}
\mid \vec{y}_{1:T}, \vec{\delta}_{1:T}, M)`. The problem is that we still have
no function that can describe this distribution in closed-form. Because there
is not analytical solution, we are forced to use Monte Carlo methods, which
approximates the target by generating samples from this intractable
distribution. Also, we don't know the true :math:`\vec{\delta}` or :math:`M`,
so we need a representative set of samples for those as well.

We need to utilize the aerodynamics of the wing in order to explore the
representative sets of values for each of the variables, then use those
samples to estimate our target.

.. math::

   p(\vec{w}_{1:T} \mid \vec{y}_{1:T}, \vec{\delta}_{1:T}, M) = \frac{ p(\vec{w}_{1:T}, \vec{y}_{1:T}, \vec{\delta}_{1:T}, M)}{p(\vec{y}_{1:T}, \vec{\delta}_{1:T}, M)} \
                                                              = \frac{ p\left(\vec{w}_{1:T}, \vec{y}_{1:T}, \vec{\delta}_{1:T}, M\right)}{\int p\left(\vec{w}_{1:T}, \vec{y}_{1:T}, \vec{\delta}_{1:T}, M \right) \mathrm{d} \vec{w}_{1:T}}

.. ::

   An alternative, two-line version of the above

   .. math::

      p(\vec{w}_{1:T} \mid \vec{y}_{1:T}, \vec{\delta}_{1:T}, M) &= \frac{ p(\vec{w}_{1:T}, \vec{y}_{1:T}, \vec{\delta}_{1:T}, M)}{p(\vec{y}_{1:T}, \vec{\delta}_{1:T}, M)} \\
                                                                 &= \frac{ p\left(\vec{w}_{1:T}, \vec{y}_{1:T}, \vec{\delta}_{1:T}, M\right)}{\int p\left(\vec{w}_{1:T}, \vec{y}_{1:T}, \vec{\delta}_{1:T}, M \right) \mathrm{d} \vec{w}_{1:T}}


Computing the target requires knowing the joint probability
:math:`p(\vec{w}_{1:T}, \vec{y}_{1:T}, \vec{\delta}_{1:T}, M)`, which is
unknown. Instead, we will use the chain rule of probability to rewrite the
joint distribution as the product of several conditional distributions which
we can estimate.

.. math::

   p(\vec{w}_{1:T}, \vec{y}_{1:T}, \vec{\delta}_{1:T}, M) = p(\vec{y}_{1:T} \mid \vec{w}_{1:T}, \vec{\delta}_{1:T}, M) p(\vec{w}_{1:T}, \vec{\delta}_{1:T}, M)


Or, using ``\left`` and ``\right``:

.. math::

   p\left(\vec{w}_{1:T}, \vec{y}_{1:T}, \vec{\delta}_{1:T}, M\right) = p\left(\vec{y}_{1:T} \mid \vec{w}_{1:T}, \vec{\delta}_{1:T}, M\right) p\left(\vec{w}_{1:T}, \vec{\delta}_{1:T}, M\right)


We can use SMC and MCMC methods to produce samples from the joint
distribution, then average over the wind components of each particle to
estimate our ultimate target: the distribution over the wind vectors
present during the flight.
