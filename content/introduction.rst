************
Introduction
************


Intro to the Intro
==================

.. Establishing a research territory (Context):

* A paraglider is a non-motorized aircraft, which means paragliding pilots are
  totally dependent on the local wind field.

* They rely on the vertical wind component for sustained flight, and the
  horizontal wind components determine the direction and distance they can
  fly.

* The success of a flight depends on the pilot's ability to recognize the
  current wind configuration so that they can choose a flight path that allows
  them to achieve their flight goals. [[Because a gliding aircraft is
  constantly descending relative to the local air, it is vital that a pilot
  can locate regions of rising air as soon as possible.]]

* Although local wind configurations are difficult to predict, they do
  exhibit regional trends. By learning the regional trends, a pilot can assess
  the current wind conditions more quickly [[than they would without prior
  knowledge of the patterns]].


.. Establishing a niche (Problem and Significance):

* Traditionally, recurring wind patterns are discovered by pilots with
  a large amount of flight time in a given area, and are shared directly
  from one pilot to another. For the pilot community to learn reliable
  patterns, individual pilots must detect each pattern and be able to
  communicate them with precision.

* An alternative [[to pilots manually detecting and communicating the
  patterns]] could be to aggregate recorded flight data from many pilots over
  many flights and build a predictive model of the wind field.

* The difficulty with this option is that GPS devices only record a tiny
  amount of the information available to a pilot: there is typically no
  information regarding the orientation, velocity, acceleration, pilot control
  inputs (brakes, accelerator, etc), or the weather conditions. Even the
  details of the aircraft performance are unknown. The question then becomes
  whether there is enough information in position-only data to recover the
  wind vectors present during a flight.


.. Occupying the niche (Response):


* This thesis investigates the procedures necessary to produce a regression
  model over wind fields using position-only paraglider flight data. It
  contributes a parametric paraglider dynamics model for simulating paraglider
  flight tracks for a given wind field and pilot control sequence. It
  discusses how to use the dynamics model with simulation-based filtering
  methods to perform statistical flight reconstruction. Lastly, it discusses
  the requirements for assembling a predictive model suitable for in-flight
  wind field estimation. [[FIXME: review these topics, liable to change]]


Context
=======

* Paragliding

  * Paragliding as a sport

  * The equipment: wing and harness

  * The dependency on the wind field. Discuss how pilots rely on wind (both
    vertical and horizontal).

  Paragliding is a non-motorized form of flight, which means it requires wind
  power for sustained flight. Pilots rely on their ability to find regions of
  rising air in order to gain altitude. They must also determine the
  direction and magnitude of the wind in order to calculate suitable landing
  zones. [[ie, pilots are totally dependent on the local wind pattern]]


* Wind fields

  * Characteristics (shear, updrafts, gusts)

  * Patterns: dependency on time of year, latitude, topography, etc.

  * Probably focus on wind field information that is important to pilots. For
    example, house thermals, finding lift along a ridge, avoiding sink near
    a stream, 


Restatement of the problem (and significance)
=============================================

[[Keep in mind: the problem is "learning the wind patterns", not why the wind
is important to paragliders.]]

* The importance of determining the current wind conditions as soon as
  possible (both pre-flight and mid-flight).

* Why knowing historical patterns improve estimates of current conditions.

* Learning wind patterns by personal experience and word of mouth

* Learning wind patterns from recorded flights

   * Why would you want to do such a thing?

* A statistical predictive model would be able to:

  * Automate pattern discovery [[Some trends may be subtle or infrequent.]]

  * Utilize all flights from all pilots instead of requiring multiple
    flights by the same pilot. [[If a pilot only encountered a particular
    wind configuration a single time, they wouldn't recognize it as part of
    a recurring pattern.]]

  * Expand the set of detectable patterns: a single flight can only
    observe a small portion of the wind field. By merging multiple flights
    that occurred at the same time, you can build a more comprehensive
    observation of the field. With larger observations there are more
    opportunities for detecting useful patterns.

  * Provide confidence levels: a statistical model can quantify the
    variance in its predictions, since it knows how much evidence is
    present for a particular pattern. [[How does this compare to
    word-of-mouth knowledge? Pilots can be deceived/biased about their
    experiences; memories are faulty.]]

* What flight data is available?

* The difficulties of learning wind patterns from the available data

  * Position-only data: no observations of the wind vectors, pilot inputs, or
    topography. No knowledge of wing parameters or sensor characteristics.

[[

Because the wing behavior relies on not only the wind vectors, but also on the
wing dynamics, orientation, and pilot controls, this *inverse problem* must
deal with a highly underdetermined system of equations. Because such a system
cannot be solved exactly, the objective is to compute the *distribution* over
all possible solutions. This limitation further changes the question from "can
I recover the wind vectors?" to "can I recover a **useful** estimate of the
wind vectors?"

For example, if no information at all is given, a wind speed estimate of
"between 0 and 150 mph" is likely to be correct, but it is not useful. If
a pilot is told that a paraglider is currently flying, then with no further
information they can still make reasonable assumptions about the maximum wind
speed, since paragliding wings have relatively small operating ranges. If you
told them the pilot's position at two points close in time, they can make an
even better guess of the wind speed and a very rough guess about the wind
direction. Intuitively, this is an "eliminate the impossible" approach: by
assuming some reasonable limits on the wind speed and wing performance you can
improve the precision of the estimate.

The key frame of mind for this project is that the question is not "can you
estimate the wind from position-only data?", but rather "how **how good** of
an estimate of wind is possible from position-only data?" An estimate doesn't
need to be especially precise in order to be useful to a pilot who is trying
to understand the local wind patterns.

[[What about PVA approaches that ignore the relative wind, such as Michael von
Kaenel's thesis?]]

Unfortunately, the nonlinear dynamics and multimodal distributions involved
with this system make analytical solutions impossible. Instead,
*simulation-based filtering* methods are required. The essence of
simulation-based methods is to explore the possible true state by utilizing
a large of of guesses, called *proposals*. Each proposal is a possible value
of the current state, and each proposal creates a prediction about the future
by utilizing the system dynamics. Each proposal receives a score, called
a *weight*, according to how well its prediction matched the measured future
state. Although there is no closed form probability distribution for these
guesses, by making a large number of guesses you can arrive at an empirical
probability distribution over solutions of the system state at each point in
time. The precise state of the underdetermined system is still unknown, but
the set of possible solutions may be bounded enough to be useful.

]]



Restatement of the response
===========================

* The massively underdetermined system necessitates simulation-based filtering
  methods.

* Parametric paraglider dynamics model

* Flight simulation

  * **Does this go before or after the dynamics model? The simulator
    establishes the need for the dynamics model.**

* Flight reconstruction

  * The available data (time and position) is not enough to identify the wing
    model or determine the wing state. Without the wing state, solving for the
    wind vectors is an underdetermined system.

  * How to deal with the underdetermined system (simulation-based filtering

  * Running the particle filter over a specific flight produces a set of
    observations over points in the wind field at a specific time

* Wind field regression

  * Each flight is a set of observations. They need to be merged (if there are
    multiple overlapping flights) and used in a kriging process to build
    a regression model for the wind field at the time+place of the flight.

* Predictive model

  * Given a set of wind field regression models, needs to find regions with
    overlapping observations, then look for correlations in those co-observed
    regions.

  * Regional correlations must be encoded into a predictive model that can be
    queried (ie, if part of the wind field is (noisily) observed, and they
    have known correlations, the predictive model should produce estimates of
    unobserved regions)

  * Ultimately, this predictive model will be useable in-flight, so as the
    pilot samples the wind field, the predictive model can suggest regions
    with desirable wind patterns.


[[

The great difficulty with model simulations is that they require equations
that encode the model dynamics. Aerodynamics are non-trivial in even the most
simple applications, and paragliders are particularly challenging aircraft to
analyze due to their curvature and flexibility. In addition to the
aerodynamics, the paraglider models themselves are uncertain, since the wing
specifications are generally unknown for any given recorded flight; instead of
a single, exactly-defined model, you need a parametric model that can be
configured to match the unknown wing. Because the wing configuration is
unknown, this estimation problem must be applied to not only the system state,
but to the model parameters as well (also known as a *dual estimation
problem*).

Given a parametric paraglider model and a method for evaluating the
aerodynamic forces that arise from a given set of wind conditions and control
inputs, you can design a set of state dynamics equations for the total system.
Those state dynamics are the basis of generating predictions as part of the
particle filter time update step.

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

]]




Contributions of my paper
-------------------------

[[FIXME: I'm not sure where this content goes]]


* Defining the problem (yes, this is a contribution! But I'd have to be
  thoughtful about how I'd word that; can't just pat myself on the back for
  coming up with an idea.)

* Code

  * Paraglider dynamics model

  * Reference wind models (for testing the model and generating test flights)

  * A simulator

  * IGC parsing code

  * Rudimentary GMSPPF?  (Stretch goal!!!)


* I'm implementing everything in Python. Explain why.

  * Approachable syntax

  * Free (unlike matlab)

  * Numerical libraries (numpy, scipy)

  * Large library ecosystem (s2sphere, sklearn, databases, PyMC3, pandas, etc)


My efforts are centered on sketching a possible path forward. This is the
problem I'd like to solve, these are the available resources, this is how
those resources might make a solution possible.


Roadmap
=======

[["Brief indication of how the thesis will proceed."]]
