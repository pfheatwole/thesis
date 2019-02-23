Main Content
============

My project started with a question: can you determine local wind patterns from
paragliding flight tracks? Flights are recorded as sequences of timestamped
positions; I wanted to see if positions alone would provide enough
information. The catch is that the way the wing moves through the air is
reliant on not only the wind, but on the pilot control inputs (braking,
accelerating, and weight shifting), as well as the performance characteristics
of the wing itself. [In terms of model parameters, this leads to a highly
underdetermined system of equations. [**Somewhat correct, but the system
I need to solve is for the state, which depends on the model parameters; the
model is essentially a set of nuisance parameters.**]] Everyone I talked to
said it was too difficult, but no one could say *why* it couldn't be done.
I decided to attempt the problem, even if that meant my project was nothing
more than detailing why it was impossible.

My philosophy at the beginning was simple: if you told me a paraglider is
currently flying, then without any further information I can still make
reasonable assumptions about the wind speed and gustiness, since paragliding
wings have relatively small operating ranges. If you told the pilot's position
at two points close in time, I can make an even better guess of the wind
speed, [and a very broad guess about the wind direction [awkward phrasing]].
The key frame of mind for this project is not "can you make a guess about the
wind from simple position information?" but rather "**how good** of an
estimate about the wind can you make from position information?" An estimate
doesn't need to be particularly precise in order to be useful to pilots trying
to understand the local wind patterns.

My first approach was a simple kinematics-only model using assumptions of
average paraglider wing performance. The problem with this method is that
estimates are still very high variance, since it is unclear which movements
are the result of changing wind and which are the result of changing pilot
controls. Answering that question for such an underdetermined system required
a change to simulation-based filtering methods.

The essence of simulation-based methods is to make many guesses about the
current state of the system and use those guesses to estimate a future state.
Each guess is weighted according to how well its prediction matched the
measured future state. Although there is no closed form probability
distribution for these guesses, by making a large number of guesses you can
arrive at an empirical distribution of the system state. This is the basis of
particle filtering methods.

The great difficulty with model simulations is that they require equations
that encode the model dynamics. Aerodynamics are non-trivial in even the most
simple applications, and paragliders are particularly challenging due to their
curving shapes. In addition to the dynamics equations, the paraglider models
themselves are uncertain, since the wing specifications are generally unknown
for any given recorded flight; instead of a single, exactly-defined model, you
need a parametric model in order to apply statistical methods to not only the
system state, but the model parameters as well.

Given a parametric paraglider model and a method for evaluating the
aerodynamic forces that arise from a given set of wind conditions and control
inputs, you can design a set of state dynamics equations for the total system.
Those state dynamics are the basis of generating predictions as part of the
particle filter time update step.

The great issue then becomes the number of particles necessary to get a good
empirical estimate of the true state probability distribution; in general, the
number of particles depends on the number of state variables, which means
a large number are required for estimating all of the model, wind, and control
input states. Because each the prediction for each particle depends on the
computationally expensive paraglider model dynamics, this large number of
particles becomes prohibitively expensive to compute. For this reason a naive
particle filter design is infeasible; more sophisticated particle methods are
required.

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


The final requirement for flight reconstruction is obtaining usable flight
data by parsing and sanitizing IGC files. Parsing is straightforward, since
the data follows a well-defined format. Sanitizing the data is more difficult:
timestamps, pressure altitude, and GNSS altitude all present their own sets of
concerns. Due to time constraints, data parsing and sanitization will not be
handled in this thesis.



So, given the wisdom of hindsight, what is the progression for solving this
problem?

1. Define a parametric paraglider model

2. Implement paraglider dynamics

#. Create test environments (wind conditions and control inputs)

#. Implement a simulator that generates flight trajectories

#. Generate test flights using a known paraglider parameters

#. Define system-wide state transition equations for the GMSPPF

   These equations say how each state component is changing in time. The
   paraglider model uses the aerodynamics *given* the wind and control
   inputs. The wind and control inputs fluctuate relatively slowly, so
   first-order Markov processes is probably fine (white noise is too high
   frequency).
   
#. Implement a UKF+GMSPPF framework

#. Use the GMSPPF to produce trajectory distributions for each of the test
   flights using the *known* paraglider model parameters

#. Expand the method to deal with *unknown* paraglider model parameters by
   embedding the GMSPFF (which use proposed model parameters) into a particle
   Metropolis-Hastings method (which proposes the model parameters)





Designing a particle filter requires designing the prior, likelihood, and
state dynamics, right? So I've got model dynamics (how the wing is moving
through the air), control "dynamics" (how the set of control inputs is likely
to be changing in time; eg, it's unlikely for speedbar to go from 0% to 100%
in 0.25sec, and unlikely that it's changes are white noise), and wind dynamics
(again, white noise seems unnecessarily imprecise; the wind fluctuates
quickly, but not instantaneously).

TODO: for a self-check, write out the basic set of particle filter equations
