It all started with a question: can I use old paragliding tracks to reveal
patterns in the wind?

It seemed reasonable that some regions of the topography would be more
consistent than others. Regions with higher-than-average consistency of lift
are referred to "house thermals", for example. If pilots can discover these
regions on their own, from experience, than it may be possible that enough
information is present in the flight tracks to discover similar patterns using
statistics.

At first, I had a huge dream: create a model, then network a bunch of
variometers with wireless radios to explore the wind field more quickly. It
soon became apparent that building the statistical model was the more
interesting, not to mention more feasible, aspect of the project. And so,
I put the variometer designs, the radio networking research, the android app,
etc, on hold.

I began exploring the data itself. The data is present in the form of so
called **IGC tracks**. At their most basic, these files are simply timestamped
position sequences: rows of plain text data containing time, latitude,
longitude, and altitude. There is no heading information, no acceleration or
velocity information, no pilot control input (braking, speedbar, etc), or any
other indications of the current weather conditions of the flight.

[[FIXME: awkward paragraph]] Thus, the recreation of the wind conditions must
rely on properties of the paraglider wings, and the feasible operating
conditions in which pilots may use them. Because the flight **track** (that
is, the movement of the glider relative to the ground) is the vector sum of
the **wind** vector (the movement of the air mass relative to the ground) plus
the **relative wind** vector (the movement of the air mass relative to the
glider), then the **track** represents an underdetermined system of equations.

By introducing constraints in the form of 1) allowable wind speed and gust
factor, and 2) standard operating ranges of paragliding wings, I theorized
that it may be possible to use a "eliminate the impossible" approach: by
proposing all possible weather conditions, then examining the respond of the
glider over time, it should be possible to bound the possible wind ranges.
Whether it is possible to constrain the wind sufficiently to provide useful
predictions remains to be seen. (ie, if the model can only claim "the wind is
between 0mph and 25mph, then although it is likely correct, it is not helpful)

This idea of simulation-based filtering is well captured in various forms of
Bayesian filtering. Because the set of solutions to the **track** system of
equations is potentially multimodal, the suitable Bayesian framework for
estimating the sets of wind and relative wind vectors is the **particle
filtering** methodology 

In this framework, a set of **particles** represent a set of assignment of
possible values for each state variable. Using the system dynamics, each
particle is propagated forward in time, and weighted according to its
posterior probability (that is, how likely the propagation is to occur under
the system model, and its likelihood of producing the given measurement under
the observation model). In this way, a set of feasible solutions to  the
underdetermined system can be produced; because this set of particles
represent an empirical estimate of the posterior distribution of the state
(that is, the probability distribution of the wind and relative wind, given
the observations plus the glider system dynamics), it is possible to generate
a set of summary statistics for the wind vector. Most simply, the mean and
variance of the wind vector can provide approximate confidence in the
estimate. (I suppose it is possible that other tests, such as testing for
multimodality, etc, can further elaborate this estimate. 

The set of summary statistics of this empirical distribution represent the
{mean, variance} state estimates at each timestamp in the original track. This
set of statistics can then be further reduced by utilizing the spatial and
temporal relationships of each timestep. If a track visits the same region at
multiple points in time, then the wind estimates at each timestamp can be
treated as a set of observations, which can themselves be aggregated to
produce a final state estimate of that point of space, within some time delta
(say, 10 minutes).

I have not yet investigated how this time delta should be chosen, whether is
should be fixed or dynamic, or anything else. This investigation will have to
wait until I have completed the particle filtering step.
