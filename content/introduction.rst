************
Introduction
************

The structure of an introduction to a thesis, as presented by "Explorations of
Style":

1. Introduction to the introduction
2. Context
3. Restatement of the problem
4. Restatement of the response
5. Roadmap


[[FIXME: I've written these as explicit subsections, but that's probably too
on the nose.]]


Introduction to the Introduction
================================

Establishing a research territory (Context):

   Paragliding is a non-motorized form of flight that uses a flexible nylon
   wing to soar using wind power. Pilots rely on their ability to find regions
   of rising air while avoiding regions of sinking air. Although local wind
   patterns are difficult to predict, they do exhibit regional trends;
   Learning local wind patterns from other pilots is a key skill for learning
   to fly in a new area.

Establishing a niche (Problem and Significance):

   Traditionally, local wind patterns are discovered by pilots with a large
   amount of flight time in an area, and are shared directly from one pilot to
   another. For the pilot community to learn reliable patterns, individual
   pilots must detect the pattern and be able to communicate it with
   precision. An alternative could be to aggregate recorded flight data
   from many pilots over many flights and build a statistical model of the
   wind field to reveal highly correlated regions of the wind field. This
   model can:

   * Automate pattern discovery

   * Utilize all flights from all pilots instead of requiring multiple flights
     by the same pilot.

   * Expand the set of detectable patterns: a single flight can only observe
     a small portion of the wind field. By merging multiple flights that
     occurred at the same time, you can build a more comprehensive observation
     of the field. With larger observations there are more opportunities for
     detecting useful patterns.
     
   * Provide confidence levels: a statistical model can quantify the variance
     in its predictions, since it knows how much evidence is present for
     a particular pattern. [[How does this compare to word-of-mouth
     knowledge?]]

Occupying the niche (Response):

   This thesis investigates the procedures necessary for processing flight
   data to produce a statistical model for predicting regional correlations in
   local wind fields. It contributes a parametric paraglider dynamics model
   for simulating paraglider flights, given a wind field and pilot control
   inputs. Lastly, it discusses how to use the dynamics model inside
   simulation-based filtering methods to perform statistical flight
   reconstruction using position-only flight data.
   

Context
=======

[["Provide the full context in a way that flows from the opening."

In this section, I could provide examples of the kinds of wind patterns that
would be useful for a pilot. Finding lift along a ridge, avoiding sink near
a stream, etc.]]


* Paragliding as a sport

* Paraglider wings (the aircraft)

* How pilots rely on wind (both vertical and horizontal)

* Wind information that is important to pilots


Restatement of the problem
==========================

["Restate the problem and significance in light of the more thoroughly
detailed context."

Here I can point out that paraglider flight tracks do not contain wind
information, or data that can be directly used to estimate the wind field. You
don't know the topography, the wind field, the pilot inputs, the wing
parameters, or the sensor characteristics.]]


* How pilots learn wind patterns

* Learning wind patterns from data

* Available flight data


Restatement of the response
===========================

[[Discuss simulation-based filtering methods. Highlight that simulating
a flight requires a dynamic model of the wing.]]


Predictive Modeling
-------------------

* Flight reconstruction to estimate the wind field during a flight

* Wind field estimates to discover patterns

* Wind patterns into a predictive model


Contributions of my paper
-------------------------

* Defining the problem (yes, this is a contribution!)

* Code

  * Paraglider dynamics model

  * Reference wind models

  * A simulator

  * IGC parsing code

  * Rudimentary GMSPPF?  (Stretch goal!!!)

I'm trying to sketch a possible path forward. This is the problem I'd like to
solve, these are the available resources, this is how those resources might
make a solution possible.

**I am not using physical models of wind field features in the wind field
estimation process. (Other papers specifically try to model thermal updrafts,
etc.) I'm essentially trying to recover point measurements of a wind field;
you could theoretically use those pseudo-observations as part of a more
sophisticated modelling method that does make assumptions about the kinds of
wind features being experienced.**


Roadmap
=======

[["Brief indication of how the thesis will proceed."]]


Old Introduction
================

1. Paragliding

   Paragliding is a non-motorized form of flight in which a pilot uses
   a flexible nylon wing to fly using wind power. Pilots rely on their ability
   to find regions of rising air in order to gain altitude. They must also
   determine the direction and magnitude of the wind in order to calculate
   suitable landing zones.

2. Wind patterns
   
   These wind patterns are completely dictated by the local topography and
   weather conditions. Although such trends can be highly variable, general
   wind patterns can be determined over the course of many flights. For
   example, some sections of terrain might have a higher than average
   occurrence of rising air, a situation that is highly desirable by pilots.

3. Learning the wind patterns
   
   Historically, such regional weather patterns have been communicated from
   pilot to pilot by word of mouth, but there is an another possibility. Many
   pilots use flight devices that record their flights as timestamped position
   sequences; these flights are uploaded to online databases for recreational
   purposes. It is possible that these flight databases contain sufficient
   information to find some of the general weather patterns using statistical
   methods.

   This project is about using those timestamped paraglider flight tracks to
   recreate the wind conditions that were present at the time of the flight.
   By considering each flight as a stochastic snapshot of the possible wind
   patterns, then given enough samples it is possible to create a database of
   general trends, just as a human pilot would do.

4. Building a predictive model

   This database of patterns can be encoded into a predictive model that can
   be evaluated in-flight, by comparing current conditions to historical
   trends. In this way a pilot can seek out regions that are likely to contain
   rising air, and can avoid regions likely to contain sinking air.


New Introduction
================

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
wings have relatively small operating ranges. If you told me the pilot's
position at two points close in time, I can make an even better guess of the
wind speed, [and a very broad guess about the wind direction [awkward
phrasing]]. The key frame of mind for this project is not "can you make
a guess about the wind from simple position information?" but rather "**how
good** of an estimate about the wind can you make from position information?"
An estimate doesn't need to be particularly precise in order to be useful to
pilots trying to understand the local wind patterns.

My first approach was a simple kinematics-only model using assumptions of
average paraglider wing performance. The problem with this method is that
estimates are still very high variance, since it is unclear which movements
are the result of changing wind and which are the result of changing pilot
controls. Answering that question for such an underdetermined system required
a change to simulation-based filtering methods. [[FIXME: probably better to
say this in terms of "There are two types of model: kinematics-only and
dynamics. The problem with a kinematics-only model, given the limits of this
poorly observed model, is...]] 

The essence of simulation-based methods is to make many guesses about the
current state of the system and use those guesses to predict a future state.
Each guess is weighted according to how well its prediction matched the
measured future state. Although there is no closed form probability
distribution for these guesses, by making a large number of guesses you can
arrive at an empirical distribution of the system state. This is the basis of
particle filtering methods. [[Careful: verify this claim.]]

The great difficulty with model simulations is that they require equations
that encode the model dynamics. Aerodynamics are non-trivial in even the most
simple applications, and paragliders are particularly challenging aircraft to
analyze due to their curvature and flexibility. In addition to the
aerodynamics, the paraglider models themselves are uncertain, since the wing
specifications are generally unknown for any given recorded flight; instead of
a single, exactly-defined model, you need a parametric model that can be
configured to match the unknown wing. Because the wing configuration is
unknown, this estimation problem must be applied to not only the system state,
but to the model parameters as well (also known as a "dual estimation
problem").

Given a parametric paraglider model and a method for evaluating the
aerodynamic forces that arise from a given set of wind conditions and control
inputs, you can design a set of state dynamics equations for the total system.
Those state dynamics are the basis of generating predictions as part of the
particle filter time update step.

The great issue then becomes the number of particles necessary to get a good
empirical estimate of the true state probability distribution; in general, the
number of particles depends on the number of state variables, which means
a large number are required for estimating all of the model, wind, and control
input states. Because the paraglider model dynamics are computationally
expensive, it is prohibitively expensive to generate individual predictions
for a large number of particles. For this reason a naive particle filter
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

The final requirement for flight reconstruction is obtaining usable flight
data by parsing and sanitizing IGC files. Parsing is straightforward, since
the data follows a well-defined format. Sanitizing the data is more difficult:
erratic timestamps, pressure altitude biases, and unknown sensor
characteristics all present their own sets of concerns. Due to time
constraints, data parsing and sanitization will not be handled in this thesis.



So, given the wisdom of hindsight, what is the progression for solving this
problem?

1. Define a parametric paraglider model

2. Implement paraglider dynamics

#. Create test environments (wind conditions and control inputs)

#. Implement a paragliding flight simulator

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
