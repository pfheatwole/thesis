*********************
Flight Reconstruction
*********************

.. The Introduction introduced the data (time series of positions), and
   motivated the need for better estimates of the wind vectors. This chapter
   walks through producing wind vector estimates from the positions.

* Recap: the goal is to estimate local wind vectors during a flight using
  position-only flight data.

* Informal description of how that could be done.

  [[Describe a pilot standing on the ground, looking up at a paraglider. They
  can use their knowledge of paraglider performance to ballpark the wind
  conditions up near the paraglider. We need to encode that knowledge in
  a mathematical model, and teach a computer to do the same estimation
  process.]]

* Chapter objectives


* The objective is to use a recorded flight track to estimate the wind vectors
  encountered during that flight.

* This task is difficult because the data does not contain direct observations
  of the wind vectors. The only data is position and time. There aren't many
  sources of additional data for a flight that occurred in the past; an
  additional information must from the structure encoded in the relationships
  between variables. In this case, the relationship is *causal*: the data are
  observations of an effect (paraglider motion), and we wish to infer the
  cause (wind vectors). [[We want to determine the conditions that produced
  the sequence of position measurements.]]

* [[Define *inverse problem*. Give a few examples? Discuss why they are hard
  and how they can fail?]]

* Solving an inverse problem requires a mathematical relationship between the
  observations (the data) and the target. That relationship introduces more
  information by imposing additional structure not present in the data alone.

* The key insight is that the data was produced by some *data-generating
  process*. A mathematical model of the *data-generating process* provides
  a relationship that can be used to solve the inverse problem.

* The model encodes the relationships between all the variables involved in
  producing the positions. It allows the designer to capture their subject
  knowledge of how the data and the target are related.

* In this case, the data are a sequence of position measurements over time.
  The paraglider's change in position is simply its motion, which is
  determined by the paraglider dynamics. The paraglider dynamics are the
  result of interactions with gravity and wind. The interactions with the wind
  are described by the canopy aerodynamics.

  [[You could **describe** the motion with kinematics, but kinematics are not
  causal relationships. You can't use them to infer anything about the
  environment.]]

* There is flexibility in designing the paraglider dynamics model, but for our
  current problem it must incorporate the canopy aerodynamics in some way,
  since the aerodynamics are what define the relationship between the state of
  the wind field and the paraglider motion. To estimate the wind vectors from
  the flight data, we must model the data-generating process with a paraglider
  dynamics model that incorporates the canopy aerodynamics.

* Given a suitable model of the paraglider dynamics, we can define a model of
  the data-generating process. The data is a sequence, and the natural
  representation of a sequential process is the *state-space model*.

* [[Define a state-space model for the position data-generating process using
  the paraglider dynamics only. Assume wind and control inputs are known.]]

* [[This definition is incomplete: the paraglider dynamics depend
  on the control inputs and the wind vectors, which do not appear in the
  model. The model must have definitions for all variables involved.]]

* [[We now have a complete model of the data-generating process, and it can be
  used to solve the inverse problem.]]

* [[But there's a problem: it includes a lot of variables with unknown values.
  The system as-is is indeterminate: with no constraints on the value of the
  control inputs and wind vectors there are no constraints on the paraglider
  state. The "answer" could be anything.

  The underlying problem is uncertainty: uncertain variable values, uncertain
  model dynamics, and uncertain measurements. Logical reasoning in
  indeterminate systems requires probability theory. Instead of seeking
  **exact** answers, the "solution" to the inverse problem is to estimate
  entire probability distributions over **all** possible answers.

  The question is no longer "can we compute the answer" but "how well can we
  constrain the range of plausible answers". There might not be enough
  information to constrain the wind vectors; hard to tell at this point.

  Should I introduce underdetermined systems, and discuss stochastic equations
  as underdetermined systems?]]


* "The idea of using the math of probability to represent and manipulate
  uncertainty is commonly referred to as *Bayesian statistics*"
  (`schon2018ProbabilisticLearningNonlinear`). Bayesian statistics is
  a framework for reasoning through conditional probability.

* At this point it can be helpful to rewrite our problem statement in
  probabilistic terms.

* Our original goal of estimating the wind vectors given the observed data is
  equivalent to saying we need to estimate the probability distribution over
  wind vectors given the data, written as :math:`p\left( wind \given data
  \right)`.

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

* [[find :math:`p \left( wind \given data \right)` by estimating the full
  joint pdf then marginalizing the *nuisance variables*]]

* We can't estimate the full joint pdf directly since it's also intractable,
  but thankfully the process model satisfies the *Markov property*. *Markov
  processes* are intuitive to represent as a state-space model. State-space
  models can be used to decompose the joint pdf into independent factors which
  a be estimated recursively to build up the full joint distribution.

* The objective now is to use the state-space model to build up the full joint
  distribution so we can marginalize the nuisance variables in order to
  compute :math:`p \left( wind \given data \right)`.



* [[The state-space model is a system of equations. In theory, we would like
  to invert them (solve for the unknown), but that's not possible here (too
  many unknowns, too complicated, etc). What's more, even if we knew the wind
  vectors and control inputs, the inverse probably doesn't even exist: it's
  pretty unlikely that this is a 1:1 function. Instead, we must be content
  with using the *forward dynamics* to generate a weighted set (a
  distribution) of possible solutions.]]


* Define *filtering problem*

* *Flight reconstruction* as a filtering problem

* This paper only provides the paraglider dynamics. The rest must be dealt
  with in the "Future Work" section.

* [[I should at least preview how you use the recursive filtering equation to
  solve the filtering problem? If you can't invert the dynamics you have to
  rely on sequential state estimation via forward simulation.

  Solving a filtering problem requires a filtering architecture, which is
  beyond the scope of this paper, although I'll probably mention it in the
  "Future Work" chapter. ]]

