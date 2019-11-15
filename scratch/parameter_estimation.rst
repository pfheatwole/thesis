* Particle Gibbs (PGAS) requires at least two trajectories from
  :math:`p(x_{1:T} | y_{1:T})`. Can you get that from a GMSPPF? Seems like the
  GMSPPF only produces the marginal distributions, so you probably can't use
  it with PGAS.

  Suppose the GMSPPF produced great marginals though. Could you use that as an
  input to another step that produced valid trajectories? The problem of
  sampling from the high distributions is the variance, but maybe smoothed
  marginals would mitigate that...
