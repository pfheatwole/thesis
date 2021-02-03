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

   4. The approach: introduce more information via flight dynamics

   5. The focus: building a dynamics model for the particle filter

   6. The outcomes: a fully parametric paraglider model


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
knowledge gained from previous flights: although local wind configurations are
difficult to predict in detail, they can exhibit recurring patterns. By
learning those patterns a pilot can assess the current wind conditions more
quickly and more accurately, and can prioritize flying to areas that are
likely to support their flight goals.


.. Establishing a niche (Problem and Significance): learn patterns from data

Traditionally, wind patterns are discovered by pilots with a large amount of
flight time in a particular area, and are shared directly from one pilot to
another. For the pilot community to learn reliable patterns, individual pilots
must first recognize them and then be able to communicate them with precision.
An appealing alternative would be to aggregate recorded flight data from many
pilots over many flights, detect any wind patterns automatically from those
flights, and build a graphical map to communicate the features of the wind
field visually instead of relying on verbal descriptions. In support of this
idea, there already exist large databases with millions of recorded flights
spanning several decades. These databases continue to grow as pilots record
and share their flights for personal and competitive purposes. The difficulty
with using those records is that most flight devices only record a tiny amount
of the information available to a pilot; in fact, the average flight record
can only be expected to include a time series of positions. There is typically
no information regarding the orientation, velocity, acceleration, pilot
control inputs (brakes, accelerator, etc), or the weather conditions. Even the
details of the aircraft are unknown, although some do record the wing make and
model. The question then becomes whether there is enough information in
position-only time series data to recover the wind vectors that were present
during a flight.


.. Occupying the niche (Response): developing a paraglider dynamics model to
   enable flight reconstruction

This thesis considers the procedures necessary to recover a sequence of wind
vectors from position-only time series flight data. The first step is to
formulate the goal in mathematical terms, which will determine the underlying
structure of the problem, and what information would be required to solve it.
It concludes that a robust solution would require a dynamics model of the
paraglider that produced the flight record, and so those dynamics are the
focus of this thesis. The primary output of this project is the design and
implementation of a parametric paraglider dynamics model and simulator for
generating flight tracks from a given wind field and pilot control sequence.
The paper will discuss how the dynamics model enables simulation-based
filtering methods to perform statistical flight reconstruction, [[and
concludes with a discussion of the remaining work?]]


.. Context

   "Provides the full context in a way that flows from the opening."

Paragliding
===========

.. Introduce paragliding as a sport

.. FIXME : merge this section into "Wind fields"?


.. What is paragliding?

Paragliding is a recreational flying activity that uses a lightweight,
flexible wing for non-powered flight. The pilot is strapped into a harness
suspended from the wing by a network of thin connecting lines. The pilot
controls the wing by manipulating the lines and shifting their weight side to
side in the harness.

There are a variety of reasons that people choose to fly. Some flights begin
with an explicit goal: maximum flight time, maximum distance, maximum
altitude, or perhaps to follow some particular route. Some pilots compete
against other pilots in organized events, some compete against their own
personal records, and some just want to relax and see where the wind takes
them. Regardless of the underlying goal, there is one underlying concern that
is common to every pilot: how to deal with the constraints of gliding flight.


.. How does gliding flight depend on the wind?

A paraglider is a non-powered aircraft, so its motion is determined by how
it interacts with gravity and the air. A pilot can steer the glider through
the air, but they cannot control how the air is moving relative to the ground.
Ultimately, it is the wind that determines how a paraglider is able to move
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
point in a region. Each point in the wind field has specific *wind velocity*,
also known as a *wind vector*. In this paper the terms are considered
interchangeable, but in aeronautics literature the term *wind vector* often
refers to only the lateral motion of the air (comprised of wind speed and
horizontal wind direction).


.. Where do they occur?

* [[Define *atmospheric boundary layer* here? It's where paragliding occurs.]]


.. What causes wind fields in the ABL?

Wind fields are caused by large-scale air flows interacting with local
features, such as topography, vegetation, solar exposure, etc.

* [[Discuss lapse rates, prevailing winds, thermal convection, mountain
    waves, etc? Global structure combines with topography to produce the local
    structure, so it may be useful to start here.]]

* [[These contributing factors determine the structure of the wind field.]]


.. What are some examples of structure in a wind field?

FIXME: keep?


.. What aspects of wind field structure are relevant to paraglider pilots?

* [[Thermal lift and sink, orographic lift, shear (including venturi), etc.

  Describe the local wind field as a composite of basic features? Shear,
  updrafts, and gusts. See :cite:`bencatel2013AtmosphericFlowField`

  Prioritize wind field information that is important to pilots. For example,
  house thermals, finding lift along a ridge, avoiding sink near a stream,
  etc.]]


.. How does wind field structure affect a pilot? Why is it so important for them
   to recognize the structure, and quickly?

[[Vertical wind directly impacts energy budgets. Horizontal wind determines
where they can go and how time/energy it costs to get there. They need to find
lift while avoiding sink, make sure they can reach the LZ, etc.]]


.. How do pilots estimate the structure of the wind field? Why is it important
   for a pilot to be able to **predict** wind field structure?

The direct way to determine a wind field is doing is to explore. The problem
is that a wing remains airborne by constantly exchanging its momentum with the
air, which means it is constantly spending energy; exploration takes time, and
time has a significant energy cost. Pilots can't afford to explore at random;
they need strategies for efficient path planning that will focus their
exploration on promising regions. If their strategy fails, they can be left
without sufficient altitude to continue their flight, or they can be trapped
by a headwind that prevents them from reaching their destination (regardless
of their altitude).

Efficient path planning minimizes energy expenditure. Pilots with greater
energy budgets are more likely to achieve their flight goals, but efficient
flight planning through an environment depends on accurate knowledge of that
environment. And so, pilots look for extra information to guide their flight
planning. [[FIXME: reword.]]

For example, dust, debris, and insects can be caught in stronger air currents,
providing information from a distance. Soaring birds, such as hawks and
vultures, are excellent navigators of the wind field; even other pilots can
provide a hint as to the conditions elsewhere. Also, although pilots are
typically focused on the wind conditions at higher altitudes, useful
information can be gained by observing behavior closer to the ground, such as
vegetation and ripples on water. Anything that interacts with the wind can be
a potential source of information. [[FIXME: reword.]]


[[Topography heuristics (surface sun exposure, ridge orientation to the wind,
likely thermal triggers, etc)

Another valuable source of information is the local topography. Paragliding
pilots rely heavily on understanding how the solid objects in the environment
affect the wind field. If the ground surface is uneven, then regions with more
sun exposure will tend to produce warmer air that can rise in thermal
convection. The orientation of the ground (or other objects such as trees and
buildings) relative to surface winds can produce orographic lift; many popular
flying sites utilize the lift generated when an onshore breeze collides with
a coastal bluff. Under some conditions the warm air near the surface can
respond to so-called *thermal triggers* that function like a wick; by
disturbing the equilibrium conditions at the surface they can initiate pockets
or columns of rising air that pilots can use to increase their energy budget.]]


[[Meteorological forecasts (weather forecasts, `RASP
<http://www.drjack.info/twiki/bin/view/RASPop/WebHome>`__ `soaringmeteoGFS
<http://soaringmeteo.org/GFSw/googleMap.html>`__, `Paragliding Maps
<http://www.paraglidingmaps.com>`__)


[[Conclude that *wind patterns* are particularly valuable. All the listed
causes, like meteorological models, etc, are only useful if you have the
correct causal model; if your causal model is wrong, its predictions are wrong.
Wind patterns are particularly nice because they're so simple. They're also
unique in that they represent what actually **DID** happen; they're not merely
suggestive of what **might** happen, given particular assumptions.]]



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


Pilots are able to determine the structure of a wind field more *efficiently*
(both in terms of time and energy) and more *accurately* when they can base
their expectations on known patterns. The motivating objective of this paper is
to help pilots extract valuable information about wind patterns from sets of
paragliding flight records.


.. What are *wind patterns*?

In this paper, a *wind pattern* is any **recurring structure** in a wind field.
The term "structure" refers to any observable order, and does not imply any
particular configuration; uniform flows, shear, orographic lift, thermal
sources and sinks, etc, and any combinations of those, can all be considered as
structured configurations. The term "recurring" refers to the fact that some
regions of a wind field can exhibit the same structure at different times.


.. Why are wind patterns so **particularly** valuable to pilots?

Wind patterns are beneficial to wind estimation in two ways. First, if some
region of a wind field exhibits recurring structure, then pilots can use that
to predict its structure without needing to spend glider energy exploring that
area. Second, once a pilot has begun traversing some region, historical
patterns can provide additional perspective that can help a pilot correctly
interpret the wind they encounter.

[[Consider both the vertical and horizontal components. Consider both
pre-flight (flight planning) and in-flight scenarios.]]


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


.. How can flight data help address those challenges?

[[If wind field structure can be determined from flight data, it would enable
the creation of tools to address the problems of discovery and use.]]

[[ie, if you can discover patterns automatically using flight data it would
address the problems of discovery; once you know the patterns you can encode
them in a predictive model that can condition on the current wind field display
suitable patterns graphically, which would address the problems of use]]


.. Step 1: address "problems of discovery"

* What are the advantages of pattern discovery from recorded flights?

  * Automate pattern discovery [[Some trends may be subtle or infrequent.]]

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

  * Visualizing structure on a graphical map is convenient

  * A statistical predictive model can provide confidence levels: it
    can quantify the variance in its predictions, since it knows how much
    evidence is present for a particular pattern. [[How does this compare to
    word-of-mouth knowledge? Pilots can be deceived/biased about their
    experiences; memories are faulty.]]


.. We've established that learning patterns and predictive models from flight
   data would be a good thing. Now review existing tools, consider how
   successful they are, and consider the source of their limitations.

   The fundamental problem with existing tools is they can't estimate the
   underlying wind field, so they have to rely on heuristics.

   The problem then is how to overcome those limitations? Well, but they have
   other limitations (ie, they fail to adequately address all those problems of
   discovery and use.

* [[Introduce the data (IGC files) here?]]


.. Are there existing tools to extract wind field structure from flight data?

* Paragliding Thermal Map, etc

* [[FIXME: what about prediction? PTM does let you filter by time of year.]]


.. How do they work?

Because flight data does not include the actual wind vectors, existing tools
rely on *heuristics*: approximation methods that rely on the wind field
containing features with some explicit structure that can be detected based on
particular patterns of the paraglider motion. For example, thermal detectors
may require a minimum sink rate, or total altitude gained; horizontal wind
estimators may require that the glider was circling at a fixed airspeed, etc.

To avoid false positives, heuristic-based feature detectors typically introduce
constraints on the motion such as minimum duration, minimum number of cycles,
etc. Given a interval, the output is assumed to be representative of the wind
field over the entire interval. The result is a sort of "average structure"
that tends to "smooth out" the regions they fit. Subtleties in the wind field
are lost.

Ultimately, each heuristic can only detect an explicit feature, and only if the
motion of the paraglider matches a predefined motion signature; the rest of the
data is discarded, which also discards valuable information.

[[FIXME: plus, that kind of output is hard to use to condition a predictive
model. You'd either have to run a similar feature detector in-flight (which is
likely to be VERY noisy) or you have to convert those features into something
that can be more easily related to the kind of data available in-flight (eg,
convert a thermal "feature" into an average sink rate or something).]]


.. How well do they address the problems of *discovery* and *use*?

These restrictions limit both *what* heuristic-based tools can detect (and
thus in what they can predict), as well as *how* their outputs can be used to
make predictions. As a result, these tools are generally inadequate for
addressing the problems of discovery and use. The underlying cause of these
restrictions is that the tools have to rely on paraglider motion as a proxy
for wind vectors. If the wind field itself was available, feature detectors
could target its structure directly.


Wind field estimation
=====================

.. To improve the ability to detect structure in the wind field, we need
   better estimates of the wind field itself. (We need estimates that don't
   rely on particular paraglider motion signatures.)

.. FIXME Should this section be called "Wind field reconstruction"? Estimation
   is a bit vague; "reconstruction" tends to communicate past-tense.

* What is *wind field estimation*?

* How would wind field estimation help?

  * [[Establish the performance criteria of a wind field estimator]]

  * Don't rely on specific motion patterns

  * Don't depend on explicit wind structure (ie, don't limit the estimator to
    structure that adheres to an explicit model, like a linearized thermal.
    You can *summarize* regions of the wind field using that sort of
    structure, but that should not be fundamental to *estimating* the wind
    field.)

  * Provide uncertainty quantification (heuristics are like point estimates)

  * Make existing methods more reliable. It's easier to extract features
    directly from the wind field instead of relying on hard-coded patterns in
    the paraglider's motion.

  * Enable spatially-distributed structure

    * Point predictions can be useful summaries of the wind field, but they
      can't capture a lot of interesting structure.

    * Pilots are interested in **everything** related to wind velocity: shear,
      venturi, dangerous blowback areas, expected wind velocity (useful for
      planning distances)

  * Enable conditional predictions based on the state of the wind field.

    With access to the causal wind field, a predictive model can condition its
    predictions on the state of the wind field, so on-line predictions can try
    to match the current state of the world. **Predictive models are MUCH more
    useful if they can condition on observations of the current (or
    forecasted) wind field.**

* How do you estimate the wind field from flight data?

  * The first step is to recover the actual wind vectors instead of using
    paraglider motion as a proxy for the wind vectors.

* Are there existing methods for estimating the wind vectors from the available
  data?

  * Yes, but those are *model-free* (data-driven methods) that rely on the
    heuristics we discussed earlier.

  * For the vertical, there are methods for estimating thermals (but they make
    strong assumptions about the state and parameters of the glider).

    [[Might be a good place to mention that, over a short time span, you can't
    tell the difference between headwind+lift versus braking.]]

  * For the horizontal, you can try to fit a thermal and compute the drift (but
    that involves a lot of strong assumptions). Same thing for the *circle
    method*.

* [[How can we produce such an estimator? (This is OLD, not sure where to put it.)]]

  * Existing models can't be easily extended to satisfy the criteria. Conclude
    that model-free methods are inadequate; model-based methods are required
    to produce "better" estimates of the wind field (ie, we need full *flight
    reconstruction*).

  * Heuristics are *model-free* methods, which rely on **coincidental**
    relationships between the particular motion sequence and the feature being
    detected. Using a *model-based* method enables introducing **causal**
    relationships: causal dynamics introduce "more" information and are able
    to extract more information from the data.

* Conclusion: a *model-based* approach is required.

* In particular, we need to model the paraglider dynamics. The canopy
  aerodynamics provide the link between the paraglider motion and the wind
  field. But, because the paraglider only interacts with points in the wind
  field, the relationship only provides information about the local wind
  vectors.


.. Restatement of the response

   "Leverage the detail presented in the full context to elaborate on the
   details of the response."

Flight reconstruction
=====================

.. So, the problem is "flight reconstruction" to enable building better tools
   for solving the problems of discovering and using wind patterns. What are
   the contributions of this paper towards solving the problem of flight
   reconstruction?

* [[We don't have a relationship to estimate the continuous wind field
  directly from a position sequence. We have to start by estimating wind
  vectors at discrete points using the **changes** in position.]]

* [[FIXME: move the "Flight Reconstruction" chapter into this section]]

* [[The main purpose of this section is to motivate :math:`\dot{x} = f(x, u)`,
  which is what ``glidersim`` provides.]]


Roadmap
=======

.. "Brief indication of how the thesis will proceed."


.. OUTDATED: As the first main chapter, :doc:`flight_reconstruction`
   formalizes the problem of wind field estimation in probabilistic terms by
   defining it as a :term:`filtering problem`. Solutions to filtering problems
   rely on having a model of the state dynamics, which motivates the bulk of
   this text: designing and implementing a parametric paraglider model.

The purpose of this project is to develop and implement a parametric
paraglider dynamics model suitable for paraglider flight reconstruction. The
modeling process begins in :doc:`canopy_geometry`, which develops a novel
parametric geometry specifically tailored for the non-linear details of
typical paraglider wings. :doc:`canopy_aerodynamics` establishes some basic
performance criteria for selecting an aerodynamic method suitable for
analyzing paraglider motion, and presents an adaptation of a non-linear
lifting line method that meets those criteria.

Given a geometric and aerodynamic model of the paraglider canopy,
:doc:`paraglider_geometry` models the remainder of the paraglider as a rigid
body system, and :doc:`paraglider_dynamics` develops several dynamics models
for paraglider motion. The final step that enables the dynamics model to
produce flight simulations is to choose a suitable set of state variables, and
link the state dynamics to the paraglider dynamics; :doc:`flight_simulation`
suggests one possible choice, and presents the resulting dynamics function.

To conclude the primary contributions of this paper, :doc:`case_study` presents
an example that uses the parametric model to approximate a physical paraglider
wing, compare static performance analyses to expected results, and demonstrate
several dynamic scenarios to highlight the flexibility of the model.

In closing, [[:doc:`data_considerations` and]] :doc:`future_work` briefly
surveys the remaining steps to solving the flight reconstruction problem,
extracting wind field patterns from sets of recorded flights, and encoding
those patterns into a predictive model.
