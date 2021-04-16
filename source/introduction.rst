************
Introduction
************

.. Meta:

   Structure taken from `Exploration of Style
   <https://explorationsofstyle.com/2013/02/20/structuring-a-thesis-introduction/>`_.

   This chapter should establish:

   1. The problem: learn wind patterns from recorded flights

   2. The value: feedback helps pilot enjoy better flights

   3. The difficulty: not enough data

   4. The solution: introduce more information via flight dynamics

   5. The work: building a dynamics model for a particle filter

   6. The result: a fully parametric paraglider model


.. Intro to the Intro

.. Establishing a research territory (Context): wind patterns help pilots

Paragliding is a recreational flying activity that uses a lightweight,
flexible wing for non-powered flight. Because paragliders lack a motor, their
motion is entirely dictated by interactions with gravity and wind.
A successful flight depends on the pilot's ability to recognize the structure
of the local air currents and navigate them in order to achieve their flight
goals, which may include optimizing for flight time, distance, or a particular
route. Because a glider is constantly spending energy to counteract the force
of gravity, the pilot must recognize the wind patterns as quickly as possible
to minimize energy loss. Experienced pilots assess the nearby air currents by
observing vegetation, birds, or other pilots, but they can also leverage
knowledge gained from previous flights; although local wind configurations are
difficult to predict in detail, they can exhibit recurring patterns. By
learning those patterns a pilot can assess the current wind conditions more
quickly and more accurately, and can prioritize flying to areas that are
likely to support their flight goals.


.. Establishing a niche (Problem and Significance): learn patterns from data

Traditionally, wind patterns are discovered by pilots with a large amount of
flight time in a particular area, and are shared directly from one pilot to
another. For the pilot community to learn reliable patterns, individual pilots
must first recognize a pattern and then be able to communicate it with
precision. An appealing alternative would be to aggregate recorded flight data
from many pilots over many flights, detect any wind patterns automatically
from those flights, and build a graphical map to communicate the features of
the wind field visually instead of relying on verbal descriptions. In support
of this idea, there already exist large databases with millions of recorded
flights spanning several decades. These databases continue to grow as pilots
record and share their flights for personal and competitive purposes. The
difficulty with using those records is that most flight devices only record
a tiny amount of the information available to a pilot; in fact, the average
flight record can only be expected to include a time series of positions.
There is typically no information regarding the orientation, velocity,
acceleration, pilot control inputs (brakes, accelerator, etc), or the weather
conditions. Even the details of the aircraft are unknown, although some do
record the wing make and model. The question then becomes whether there is
enough information in position-only time series data to recover the wind
vectors that were present during a flight.


.. Occupying the niche (Response): developing a paraglider dynamics model to
   enable flight reconstruction

This thesis considers the procedures necessary to estimate wind field
structure from position-only time series flight data. The first step is to
formulate the goal in mathematical terms, which will determine the underlying
structure of the problem, and what information would be required to solve it.
It concludes that a robust solution would require a dynamics model of the
paraglider that produced the flight record, and so those dynamics are the
focus of this thesis. The primary output of this project is the design and
implementation of a parametric paraglider dynamics model and simulator for
generating flight tracks from a given wind field and pilot control sequence.
[[**Specifically, I'm interested in creating dynamics models from bare-bones
knowledge of the paraglider system: wing, harness, etc.**]] The paper will
discuss how the dynamics model enables simulation-based filtering methods to
perform statistical flight reconstruction, [[and concludes with a discussion
of the remaining work?]]


.. Context

   "Provides the full context in a way that flows from the opening."

Paragliding
===========

.. Introduce paragliding as a sport

.. FIXME : merge this section into "Wind fields"?


.. What is paragliding?

Paragliding is a recreational flying activity that uses a lightweight,
flexible wing for non-powered flight. The pilot is strapped into a harness
suspended from the wing by a network of thin connecting lines. The wing is
controlled by manipulating the lines and shifting the pilot's weight inside
the harness.

There are a variety of reasons that people choose to fly. Some flights begin
with an explicit goal: maximum flight time, maximum distance, maximum
altitude, or perhaps to follow some particular route. Some pilots compete
against other pilots in organized events, some compete against their own
personal records, and some just want to relax and see where the wind takes
them. Regardless of the goal, there is one underlying concern that is common
to every pilot: how to deal with the constraints of gliding flight.


.. How does gliding flight depend on the wind?

A paraglider is a non-powered aircraft, so its motion is determined by how
it interacts with gravity and the air. A pilot can steer the glider through
the air, but they cannot control how the air is moving relative to the ground.
Ultimately, it is the wind that limits how a paraglider is able to move
relative to the ground.

As with all lifting surfaces, the aerodynamics of a paragliding wing depend on
the relative velocity between the wing and the air, not the relative velocity
between the wing and the ground; the wing will accelerate until an equilibrium
state is achieved. If the air is ascending a pilot can slow their descent, or
even gain altitude; conversely, sinking air will cause the wing to descend
more quickly. The horizontal component of the wind dictates the ground speed
of the glider in a given direction, which determines what regions of the air
the pilot can access, and what landing zones they can reach. As a result,
pilots must understand the structure of the wind field in order to plan their
flight path and achieve their flight goals.


Wind fields
===========

.. What is a wind field?

A *wind field* refers to the detailed variations of local air currents at each
point in a region. Each point in the wind field has a specific *wind
velocity*, also known as a *wind vector*. It is important to note that in this
paper the terms are considered interchangeable, but in aeronautics literature
the term *wind vector* often refers to only the lateral motion of the air
(comprised of wind speed and horizontal wind direction).


.. What wind fields are paragliding pilots interested in? Where do they occur?

* [[Define *atmospheric boundary layer* here? It's where paragliding occurs.]]


.. What causes wind fields in the ABL?

Wind fields are caused by large-scale air flows interacting with local
features, such as topography, surface materials, vegetation, solar exposure,
etc.

* [[Discuss lapse rates, prevailing winds, thermal convection, mountain waves,
  etc? Global structure combines with topography to produce the local
  structure, so it may be useful to start here.]]

* [[These contributing factors determine the structure of the wind field.]]


.. What are some examples of structure in a wind field?

[[FIXME: keep?]]


.. What aspects of wind field structure are relevant to paraglider pilots?

* [[Thermal lift and sink, orographic lift, shear (including venturi), etc.

  Describe the local wind field as a composite of basic features? Shear,
  updrafts, and gusts. See :cite:`bencatel2013AtmosphericFlowField`

  Prioritize wind field information that is important to pilots. For example,
  house thermals, finding lift along a ridge, avoiding sink near a stream,
  etc.]]


.. Why is it important for a pilot to determine wind field structure quickly?

Much of the skill in piloting a gliding aircraft is in maintaining the
glider's energy budget, which requires careful aircraft control and efficient
path planning. Because planning a path through an environment depends on
accurate knowledge of that environment, pilots are constantly looking for
information about the structure of the wind field.

[[Vertical wind directly impacts energy budgets. Horizontal wind determines
where they can go and how time/energy it costs to get there. They need to find
lift while avoiding sink, make sure they can reach the LZ, etc.]]


.. How do pilots estimate the structure of the wind field?

The direct way to learn the structure of a wind field is to explore. The
problem is that exploration takes time, and time has a significant energy
cost; a wing remains airborne by constantly exchanging its momentum with the
air, which means it is constantly spending energy. Pilots cannot afford to
explore at random; they need strategies for efficient path planning that will
focus their exploration on promising regions. If their strategy fails, they
can be left without sufficient altitude to continue their flight, or they can
be blocked by a headwind that prevents them from reaching their destination
(regardless of their altitude).

Another direct source of information is to observe other objects interacting
with the wind field. For example, dust, debris, and insects can be caught in
air currents, so their motion can provide information from a distance. Soaring
birds, such as hawks and vultures, are excellent navigators of the wind field,
and can indicate lifting air; even other pilots can provide a hint as to the
conditions elsewhere. Also, although pilots are typically focused on the wind
conditions at higher altitudes, useful information can be gained by observing
behavior closer to the ground, such as vegetation and ripples on water.
Anything that interacts with the wind can be a potential source of
information. [[FIXME: reword.]]


.. How can pilots predict the structure of the wind field?

Another valuable, albeit indirect, source of information is the local
topography. Paragliding pilots rely heavily on understanding how the
environment affects the wind field. Regions with more sun exposure will tend
to produce warmer air that can rise through thermal convection. The
orientation of the ground (or other objects such as trees and buildings)
relative to surface winds can produce useful updrafts; many popular flying
sites use the lift generated when an onshore breeze collides with a coastal
bluff. Under some conditions warm air near the surface can respond to
so-called *thermal triggers* that function like a wick; by disturbing the
equilibrium conditions at the surface the trigger can initiate bubbles or
columns of rising air that pilots can use to increase their energy budget.

[[Meteorological forecasts (weather forecasts, `RASP
<http://www.drjack.info/twiki/bin/view/RASPop/WebHome>`__ `soaringmeteoGFS
<http://soaringmeteo.org/GFSw/googleMap.html>`__, `Paragliding Maps
<http://www.paraglidingmaps.com>`__)

Although there are many methods to help a pilot predict the local wind field,
there is one that is particularly effective: local *wind patterns*.


.. Restatement of the problem (and significance)

   "Restate the problem and significance in light of the more thoroughly
   detailed context."

Wind field patterns
===================

.. This section establishes that it is easier to estimate and predict the
   structure of a wind field if you have knowledge of recurring structure.
   There are problems in discovering and using that knowledge which can
   benefit from building predictive models from flight data. Unfortunately the
   flight data doesn't contain observations of the wind field, so this section
   concludes by motivating wind field estimation.

   Discuss wind patterns, their importance, and how they're learned


.. What are *wind patterns*?

In this paper, a *wind pattern* is any **recurring structure** in a wind
field. The term "structure" refers to any recognizable order, and does not
imply any particular configuration; uniform flows, shear, orographic lift,
thermal sources and sinks, etc, and any combinations of those, can all be
considered structured configurations. The term "recurring" refers to the fact
that some regions of a wind field can exhibit the same structure at different
times.


.. Why are wind patterns so **particularly** valuable to pilots?

The reason local wind patterns are so particularly valuable is that they help
pilots determine the structure of a wind field more *efficiently* (both in
terms of time and energy) and more *accurately* when they can base their
expectations on known patterns.

Wind patterns are useful for both prediction and estimation. First, if some
region of a wind field exhibits recurring structure, then pilots can use that
to predict its structure without needing to spend glider energy exploring that
area. Second, once a pilot has begun traversing some region, historical
patterns can provide additional perspective that can help a pilot correctly
interpret the wind they encounter.

[[Consider both the vertical and horizontal components. Consider both
pre-flight (flight planning) and in-flight scenarios.]]

[[Another advantage of wind patterns is that they are practical: they focus on
what did happen, not what might happen in theory. All the other means of
predicting the wind field, like meteorological models, etc, are only useful if
the theory is able to produce an accurate causal model; if a causal model is
wrong, its predictions are wrong.]]


.. What challenges are involved?

Pilots who want to take advantage of wind patterns face a variety of challenges
that can be broadly classified as problems of *discovery* and problems of
*use*.


.. What are problems of *discovery*?

Traditionally, pilots discover wind patterns by flying in the same region
repeatedly, and by sharing their observations with other pilots.

[[FIXME: what are the limitations of these "traditional" methods]]


.. What are problems of *use*?

* [[Pilots have to memorize the patterns, when they're applicable, etc.]]


.. Can flight data be used to address those challenges?

   **THE DRIVING QUESTION OF THIS PAPER.**

[[If wind field structure can be determined from flight data, it would enable
the creation of tools to address the problems of discovery and use.]]

[[ie, if you can discover patterns automatically using flight data it would
address the problems of discovery; once you know the patterns you can encode
them in a predictive model that can condition on the current wind field display
suitable patterns graphically, which would address the problems of use]]


.. Step 1: address "problems of discovery"

* What are the advantages of pattern discovery from recorded flights?

  * Automate pattern discovery [[ie, it's convenient? Also, some patterns may
    be subtle; they may involve conditions that humans won't typically pick up
    on (especially ones involving negatives, like "if there is NOT lift over
    here, they may be lift over there")]]

  * More opportunities to find patterns in flights that are spread out over
    longer time periods. Some trends may be infrequent, and pilot
    memories fade.

  * Utilize all recorded flights from all pilots instead of requiring multiple
    flights by the same pilot. [[If a pilot only encountered a particular wind
    configuration a single time, they wouldn't recognize it as part of
    a recurring pattern.]]

  * Expand the set of detectable patterns: a single flight can only
    observe a small portion of the wind field. By merging multiple flights
    that occurred at the same time, you can build a more comprehensive
    observation of the field. With larger observations there are more
    opportunities for detecting useful patterns.

  * Quantifying/encoding the patterns in mathematical form would enable the
    creation of a *predictive model*, which can then address problems of use.
    [[This is hard to follow; explain how simply producing a list of patterns
    is different from making predictions by conditioning on current state.]]


.. Step 2: address "problems of use"

* What are *predictive models*?

  * Predictive models encode predictable structure. Some wind field patterns
    can be predicted based on time of day/year, some can be predicted based on
    the values of other regions of the wind field, etc. This is the essence of
    "conditioning" our predictions.

  * Predictive models inform pilots of historical trends, which can help them
    recognize the current structure as early as possible; ideally, before they
    even fly into a new area. They can also improve the accuracy of a pilot's
    estimate of the current wind field.

  * [[**Computer** models that predict the structure of the wind field.]]

  * [[I'm leaving "pattern" vague, so this can include things like Paragliding
    Thermal Map, etc. Those tools only estimate simple point sources I'm still
    considering them "recurring structure".]]

* What are the benefits of encoding patterns in predictive models?

  * [[We discussed the value of patterns earlier. This is about the benefits of
    having a predictive model built from those patterns.]]

  * Save the pilot from having to memorize the patterns

  * Save the pilot from having to remember the conditions under which a pattern
    is applicable.

    Conditioning on the state of the wind field enables predictions that are
    consistent with the observations. Conditioned models attempt to predict the
    *actual* configuration instead of some *average* configuration (which is
    typically produced by averaging over some arbitrary time interval).

    Conditioning to produce estimates that are consistent with the observations
    of the current wind configuration (averages lump everything together).
    Useful both pre-flight (condition on weather forecasts) and in-flight
    (condition on actual conditions).

    [[Note: you don't have to use the same predictive model for pre-flight and
    in-flight prediction; for example, if you have wind forecasts on a grid of
    the surrounding area, you could train the model using the values of those
    predictor variables (which are **not** the same thing as observations of
    the wind field itself.]]

  * Visualizing structure on a graphical map is convenient.
    :cite:`wirz2011RealtimeDetectionRecommendation`

  * A statistical predictive model can provide confidence levels: it
    can quantify the variance in its predictions, since it knows how much
    evidence is present for a particular pattern. [[How does this compare to
    word-of-mouth knowledge? Pilots can be deceived/biased about their
    experiences; memories are faulty.]]


[[FIXME: discussion here.

Conclusion: before you can estimate **recurring** structure, you need to be
able to estimate the structure for the individual flights from the flight
data.]]


Wind field reconstruction
=========================

.. We've established that learning patterns and predictive models from flight
   data would be a good thing, but first we need to able to reconstruct the
   wind fields from individual flights. This section should review existing
   tools, consider how successful they are, and consider the source of their
   limitations.

   The fundamental problem with existing tools is they have to rely on
   heuristics (non-causal relationships that try to estimate wind field
   structure directly from paraglider position). This limitation means they
   fail to adequately address all those problems of discovery and use.


.. What is *wind field reconstruction*?

In this paper, *wind field reconstruction* refers to the process of estimating
the structure of regions of the wind field that was present during a flight.


* [[Introduce the data (IGC files) here?]]


.. Are there existing tools to extract wind field structure from flight data?

* Paragliding Thermal Map, etc

* [[FIXME: what about prediction? "Paragliding Thermal Map" does let you
  filter by time of year.]]


.. How do they work?

Because flight data does not include the actual wind vectors, existing tools
rely on *heuristics*: approximation methods that rely on the wind field
containing features with some predefined structure that can be detected based
on specific patterns of the paraglider motion. For example, thermal detectors
may require a minimum sink rate or total altitude gained, and they are forced
to make strong assumptions about the state and parameters of the glider (such
as average sink rate). Horizontal wind estimators may require that the glider
was circling at a fixed airspeed. Other methods may try to fit the vertical and
horizontal components simultaneously; for example, one method assumes
a circling glider is accurately coring a thermal that is inclined with respect
to the wind, so fitting a thermal model. [[FIXME: edit]]

To avoid false positives, heuristic-based feature detectors typically introduce
constraints on the motion such as minimum duration, minimum number of cycles,
etc. Given a interval, the output is assumed to be representative of the wind
field over the entire interval. The result is a sort of "average structure"
that tends to "smooth out" the regions they fit. Subtleties in the wind field
are lost.

[[FIXME: probably a good place to mention that, over a short time span, you
can't tell the difference between headwind+lift versus braking?]]

[[FIXME: discuss energy-based methods?]]

Ultimately, each heuristic can only detect an explicit feature, and only if the
motion of the paraglider matches a predefined motion signature; the rest of the
data is discarded, which also discards valuable information.

[[FIXME: plus, that kind of output is hard to use to condition a predictive
model. You'd either have to run a similar feature detector in-flight (which is
likely to be VERY noisy) or you have to convert those features into something
that can be more easily related to the kind of data available in-flight (eg,
convert a thermal "feature" into an average sink rate or something).]]


.. What are their limitations?

[[Existing tools use heuristics that rely on coincidental instead of causal
relationships. Indirect relationships are the cause of awkward hacks/filters
like "require the paraglider to be circling" or "sink rate must be at least
1m/s". Direct relationships avoid those.]]

The heuristics impose some limitations:

* They can only detect specific kinds of structure. They cannot determine the
  wind field structure in general.

* They rely on specific paraglider motion patterns. They do this because they
  don't have a direct relationship between paraglider motion and wind field
  structure, so they have to rely on heuristics.


.. How well do existing tools address the problems of *discovery* and *use*?

These restrictions limit both *what* structure heuristic-based tools can
detect (and thus in what structure they can predict), as well as *how* their
outputs can be used to make predictions. As a result, these tools are
generally inadequate for addressing the problems of discovery and use.


.. How can the limitations of heuristics be avoided?

[[Instead of trying to estimate wind features directly from paraglider motion,
the goal should be to break the process into multiple steps that use
**direct** relationships: paraglider motion is directly related to wind
vectors, wind vectors are directly related to the (continuous) wind field, and
the wind field contains the structure that contains the wind features.]]

The underlying cause of these restrictions is that the tools have to rely on
paraglider motion as a proxy for wind vectors. If the wind field itself was
available, feature detectors could target its structure directly instead of
relying on paraglider motion as a proxy.

* Why would wind vector estimation improve wind field reconstruction?

  * Don't require explicit motion patterns. The entire sequence of positions
    contains information about the wind field; don't throw some of it away
    just because an interval doesn't fit some predefined motion signature.

  * Don't require explicit wind structure (ie, don't limit the estimator to
    structure that adheres to an explicit model, like a linearized thermal.
    You can *summarize* regions of the wind field using that sort of
    structure, but that should not be fundamental to *estimating* the wind
    field.)

* Are there existing methods for estimating wind vectors from position-only
  flight data?

  Yes, but they rely on the same type of heuristics that were discussed
  earlier, with the same limitations.

  They typically rely on a moving-average approach; for example, the circling
  method is essentially an average over a time interval. Moving-average
  methods require long intervals to reduce estimate noise, but as a result the
  estimates are over-smoothed (and that's assuming the constant-airspeed
  assumption held over that interval).


* CATCH-ALL COLLECTION

  The existing methods fail because they don't have enough information
  (because they don't impose enough structure). They rely on indirect
  relationships and questionably strong assumptions.

  The heuristics mentioned so far are *model-free* methods that rely on
  **coincidental** relationships between the particular motion sequence and
  the feature being detected. In contrast, *model-based* methods rely on
  **causal** relationships: causal dynamics introduce additional information
  about the system dynamics which can then be used to extract more information
  from the data.

  Better wind vector estimation requires a direct, causal relationship between
  wind vectors and paraglider position.

  In particular, we need to model the paraglider dynamics. The canopy
  aerodynamics provide the link between the paraglider motion and the wind
  field. But, because the paraglider only interacts with points in the wind
  field, the relationship only provides information about the local wind
  vectors.

  [[Conclusion: the goal is to estimate the continuous wind field from
  position-only flight data, but we don't have a relationship to do that
  directly. What we do know (partially) is the paraglider dynamics, so we need
  to start by targeting the sequence of wind vectors encountered at discrete
  points in the wind field.]]


.. Restatement of the response

   "Leverage the detail presented in the full context to elaborate on the
   details of the response."

Flight reconstruction
=====================

.. This section establishes the intuition behind reconstructing the complete
   state trajectory of a flight from a time series of positions. The goal is
   to recover the wind vectors at individual points to enable estimating the
   continuous structure of the wind field, but the wind vectors are related to
   position through the paraglider dynamics, which require more inputs than
   just the wind vectors, so the complete state must be reconstructed. It
   concludes by motivating :math:`\dot{x} = f(x, u)`, which is what the
   `pfh.glidersim` Python package is designed to provide.


The conclusion of the previous section is that reconstructing a wind field
from flight data should start by estimating the sequence of wind vectors. The
difficulty is that flight records are limited to position-only data; they do
not contain any direct observations of the wind vectors. The solution is to
exploit knowledge of how the sequence of positions were generated.

[[FIXME: should/did the previous section explain that targeting wind vectors
instead of the final wind field enables the use of causal dynamics? I don't
want to introduce the dynamics yet (that should happen in these paragraphs),
but if so, I shouldn't just announce "we should start by estimating the wind
vectors!" in the conclusion to "Wind field reconstruction"]]


.. Develop the intuition with an informal description

Imagine a paragliding pilot standing on the ground, looking up at a paraglider
in flight. Under average conditions, the pilot on the ground could watch the
paraglider for a few moments and be able to produce a reasonable guess of the
current wind conditions near the glider. Their guess is imprecise, and yet
pilots routinely use this kind of estimate to decide whether to launch their
own glider. How does that work, and can it form the basis of better wind
estimation?

[[Consider the fact that they're not relying on specific motion signatures;
they rely on approximations, but not the heuristics discussed previously.
Also, it's important to remember that "imprecise" is relative; the estimate
merely needs to be **useful**.]]

The key is that their estimate is built not only from the paraglider motion,
but also from their intuition for how paraglider motion depends on the wind;
given what they know about average paraglider performance, and the range of
wind conditions in which a pilot would choose to remain airborne, they can
imagine a range of possible scenarios and predict how a wing would respond to
each possibility. [[FIXME: it's not obvious how this is different from
heuristics, which also use "intuition" of how paraglider motion depends on the
wind.]] Scenarios that don't agree with the observed motion are unlikely to be
correct can be rejected, and the ones that remain establish a range of
plausible values.


.. Formalize the steps

Estimating wind vectors using flight data is very similar, but first this
intuitive approach must be formalized in mathematical terms: the pilot's
intuition of wing performance is replaced with numerical physics, the ad hoc
set of plausible wind vectors is replaced with a principled set of proposals,
and the conclusion is replaced with a probability distribution.

First, the intuitive strategy of the pilot standing on the ground as
a sequence of steps:

1. Recognize that the motion of a paraglider is the result of how the
   paraglider is interacting with the wind, given the particular wing model,
   the type of harness, and the pilot's inputs to the wing.

2. Learn the details of how a paraglider responds to wind given different
   control inputs.

3. Imagine a set of plausible guesses for the current wind vector.

4. Use the knowledge of paraglider behavior to imagine how the paraglider
   would be moving if each guess was correct.

5. Consider how well each of the guesses explained how the paraglider is
   actually moving.

6. Summarize the plausible range for the current wind vector.

Then, rewrite the intuitive steps in formal terms:

1. Identify the *data-generating process*.

2. Model of the *data-generating process*.

3. Generate a set of *proposals*.

4. Use the model dynamics to solve the *forward problem* for each proposal.

5. *Weight* each proposal according to how well it matches the observation.

6. Use the set of solutions to the forward problem to establish a distribution
   of plausible solutions to the *inverse problem*.


Identify the data-generating process
------------------------------------

The key viewpoint is that the paraglider's position is the output of some
*data-generating process*. [[FIXME: define *data-generating process*?]]

In this case, the data are a sequence of position measurements over time. The
positions are a (noisy) record of the paraglider's motion, which is determined
by the paraglider dynamics. The paraglider dynamics are the result of
interactions with gravity and wind. The interactions with the wind are
described by the canopy aerodynamics [[which provide the causal link between
paraglider motion and the wind]].

[[

You could **describe** the motion with kinematics, but kinematics are not
causal relationships. You can't use them to infer anything about the
environment.

From :cite:`mcelreath2020StatisticalRethinking`, page 28:

  Bayesian data analysis usually means producing a story for how the data came
  to be. This story may be *descriptive*, specifying associations that may be
  used to predict outcomes, or it may be *causal*, a theory of how some events
  produce other events.

]]

[[At this stage it's important to acknowledge that some of the **observed**
motion is false due to sensor error.]]


Model the data-generating process
---------------------------------

* A model of a *data-generating process* describes how the data was created.
  For the pilot standing on the ground, the data are visual measurements of
  paraglider position, and the paraglider position is the result of the
  paraglider dynamics.

* The model of the *data-generating process* encodes the known relationships
  between all the variables involved in that process. Those relationships
  impose additional structure that can be used to solve the inverse problem.

  [[Explain how the model design step allows the designer to express their
  subject knowledge of how the data and the target are related.]]

* There is flexibility in designing the paraglider dynamics model (the
  "golem"), but for our current problem it must incorporate the canopy
  aerodynamics in some way, since the aerodynamics are what define the
  relationship between the state of the wind field and the paraglider motion.
  To estimate the wind vectors from the flight data, we must model the
  data-generating process with a paraglider dynamics model that incorporates
  the canopy aerodynamics.

* [[Link to :cite:`mcelreath2020StatisticalRethinking`? Great discussion of
  this in Sec:16.2.4. Also in Sec:16.4 he discusses "geocentric" models, such
  as ARMA, which might be useful.]]


.. State-space models of sequential processes

[[Explain using state-space models to describe sequential processes. The
general form of state-space models is enough to necessitate a dynamics model,
which is what provides the link between what we know (the output of the
sequential process) to what we want (the sequence of wind vectors)]]

* Given a suitable model of the paraglider dynamics, we can define a model of
  the data-generating process. In this case the data is a sequence, and the
  natural representation of a sequential process is the *state-space model*.

  For a discrete-time, linear, time-invariant model:

  .. math::
     :label: discrete-time linear state-space model

     \begin{aligned}
       x_{k+1} &= \mat{A}_k x_k + \mat{B}_k u_k \\
       y_k &= \mat{C}_k x_k + \mat{D}_k u_k
     \end{aligned}

  For a continuous-time, non-linear, non-time-invariant model:

  .. math::
     :label: continuous-time non-linear state-space model

     \begin{aligned}
       \frac{d}{dt} \vec{x}(t) &= f \left( t, \vec{x}(t), \vec{u}(t) \right) \\
       \vec{y}(t) &= h \left( t, \vec{x}(t), \vec{u}(t) \right)
     \end{aligned}

* In this case, the :math:`\vec{x}(t)` are the current state of the flight at
  time :math:`t`, and :math:`\vec{y}(t)` are the position. The data is
  a sequence of positions, which are a noisy observation of the true position.

* A complete specification includes a definition of every component in
  :math:`\vec{x}` and how it is evolving over time.

* [[Define a state-space model for the position-data-generating process using
  the paraglider dynamics only. Assume wind and control inputs are known.]]

* We now have a complete model of the data-generating process, and it can be
  used to solve the inverse problem.

  [[Well, the form at least is complete: the paraglider dynamics depend on the
  control inputs and the wind vectors, which do not appear in the model. The
  model must have definitions for all variables involved. The discussion of
  unknown inputs should get pushed back into "Future Work".]]


Generate a set of proposals
---------------------------

[[Define *proposal*, give examples, etc]]


Solve the forward problem
-------------------------

[[Define *forward problem*]]


Weight the outcomes
-------------------

[[Describe how each proposal produces a predicted behavior, which you then
compare to the observed actual behavior.]]


Solve the inverse problem
-------------------------

.. Too many unknowns means this is a stochastic filtering problem

[[The relationship is *causal*: the data are observations of an effect
(paraglider motion), and the wind is a cause.]]

The flight track recorded an effect (position) and we we wish to infer
a cause. In stochastic filtering theory, the problem of trying to infer
a cause from an effect (or more generally, inferring an input from an observed
output) is referred to as an *inverse problem*.

[[We want to determine the conditions that produced the sequence of position
measurements.]]

* [[Define *inverse problem*. Give a few examples? Discuss why they are hard
  and how they can fail?]]

  * Wind is only one of the causes; the output (position) is the result of
    multiple inputs.

  * There may be multiple combinations of input that produce the same output
    (the solution is not guaranteed to be "unique").

  * The data is noisy.

* [[FIXME: define "solving" an inverse problem. Given complete information and
  the ability to compute the function inverse, you can compute the true inputs
  that produced a given output. If there is a many-to-one relationship, or if
  some information is unknown (including corruptions due to noise), you can't
  solve for a single, absolute answer; the best you can do is estimate
  a probability distribution over the possible inputs that produced the
  observed output.]]

* Solving an inverse problem requires a mathematical relationship between the
  observations (the data) and the target. That relationship introduces more
  information by imposing additional structure not present in the data alone.


.. Flight reconstruction as a filtering problem

* [[Define *flight reconstruction* as the process by which you estimate the
  unknown state variables given the inputs.]]

* [[Present *flight reconstruction* as a *filtering problem*, which will
  introduce the recursive filtering equation. The filtering equation needs
  a *transition function* (which for a continuous-time model appears as
  a differential equation). **This is where I motivate :math:`\dot{x} = f(x,
  u)`, which is what `glidersim` provides: a parametric model to produce the
  :math:`\dot{x}`.** ]]

  For the "fundamental recursions", see
  :cite:`kantas2015ParticleMethodsParameter`, Eq:3.1 through Eq:3.3

  [[Good place to cite :cite:`davey2016BayesianMethodsSearch`?]]


Conclusion
----------

[[Need a segue into the next section.]]


Parametric paraglider modeling
==============================

.. This section sets up the entire paper!

   Flight reconstruction needs a dynamics model. They're not in the flight
   records, so they must be estimated. This project develops a parametric
   paraglider model to make it easiser to approximate existing wings. The
   parameters are chosen to make it as easy as possible to incorporate what
   little data is available (technical specs from wing manuals).


The section `Model the data-generating process`_ explained why flight
reconstruction requires a dynamics model of the paraglider that produced the
data. This requirement presents several major problems:

1. The flight record does not provide the dynamics model that created the
   data, so one must be created.

2. Creating a high-fidelity dynamics model from detailed wing specifications
   is expensive. [[FIXME: eliminate this? "Its expensive, but that's
   irrelevant since we don't know it anyway."]]

3. Detailed specifications are not available for commercial paraglider wings;
   only summary technical specifications are known.

4. Most flight records don't even record what wing produced the data. Flight
   reconstruction must treat the dynamics model as a random variable.

Regardless of whether the wing model is known for an individual flight,
reconstructing an entire set of flight records will almost certainly require
many different paraglider wings. This project acknowledges the need to to
produce a large number of dynamics models from minimal specification
information.

[[Because we only have minimal technical specs, we'll need to "fill in" the
missing information with some reasonable design choices. For the canopy this
takes the form of parametric functions; for the harness we'll make assumptions
about the mass distribution and drag coefficient; etc. We'll also make
assumptions about how the components are connected (rigid body model, 6 and
9 DoF models, etc).]]

[[FIXME: finish motivating the creation of a **parametric** dynamics model.
Discuss what parameters would make sense here. The canopy aerodynamics can be
estimated from the canopy geometry; we have some basic shape information from
technical specs, so we would like a paraglider model parametrized by that data
(or as closely as possible). The canopy geometry can also be used to estimate
the inertial properties if you know the surface densities.]]


Roadmap
=======

.. "Brief indication of how the thesis will proceed."

This project designs and implements a parametric paraglider dynamics model
suitable for paraglider flight reconstruction. The modeling process begins in
:doc:`canopy_geometry`, which develops a novel parametric geometry
specifically tailored for the non-linear details of typical paraglider wings.
:doc:`canopy_aerodynamics` establishes some basic performance criteria for
selecting an aerodynamic method suitable for analyzing paraglider motion, and
presents an adaptation of a non-linear lifting line method that meets those
criteria.

Given a geometric and aerodynamic model of the paraglider canopy,
:doc:`paraglider_model` models the remainder of the paraglider as a rigid body
system and develops several dynamics models for paraglider motion. The final
step that enables the dynamics model to produce flight simulations is to
choose a suitable set of state variables, and link the state dynamics to the
paraglider dynamics; :doc:`flight_simulation` suggests one possible choice,
and presents the resulting dynamics function.

To conclude the primary contributions of this paper, :doc:`case_study` presents
an example that uses the parametric model to approximate a physical paraglider
wing, compare static performance analyses to expected results, and demonstrate
several dynamic scenarios to highlight the flexibility of the model.

In closing, :doc:`future_work` briefly surveys the remaining steps to solving
the flight reconstruction problem, extracting wind field patterns from sets of
recorded flights, and encoding those patterns into a predictive model.
