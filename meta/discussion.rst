* *wind vector* or *wind velocity*  ?

  In general, "velocity" is "rate change of position". The wind isn't changing
  position (the air is), so I'm tending towards "vector"

  Ooh, but "wind vector" typically refers to the horizontal component only.
  Dare I use *air velocity* for 3D local wind?

* I'm assuming that the wind field regression model would capture all the
  information about the wind field, but does the fact that the pilot chose to
  core in a particular way contain any information that would not be capture
  by the wind field estimate? Would there be any "residual information" in the
  paraglider track once you have the wind field regression model?



********
Chapters
********


Introduction
============

* The question isn't "*can you* estimate the wind from a paragliding track?",
  but "*how precisely can you* ...?"

* One likely complaint is the inaccuracy of GPS data, so I should confront
  this early on, and discuss why I think it might be worth trying anyway.
  First, just because it's *less* accurate doesn't mean the results aren't
  still *useful*. Also, GPS continues to improve in accuracy; the fact that
  older tracks were often inaccurate shouldn't mean we can't start designing
  a system for newer tracks with better accuracy.

* Don't mix up the two problems: *discovery* and *use*. If a tool deals with
  both, don't get focused on the tool: stay focused on the individual problem.

* Note to self: this paper is strictly focused on estimating wind vectors from
  flight data. Any discussion of estimating structure or extracting patterns
  from sets of flights must be relegated to the "Future Work" chapter.


Predictive modeling
-------------------

* I'm interested in both *estimation* and *prediction*: pilots want accurate
  estimates of places they've been (estimation), but also of places they
  haven't been yet (prediction).

* You can only predict what you can detect. You can only discover "recurring
  structure" if you're capable of detecting that structure in the first place.

* You can only condition predictions on structure you can detect (applies
  both to detecting structure from data and in-flight)

* Accuracy is important both when estimating from data and in-flight. If
  you're trying to condition a prediction based on some variable, then your
  "from data" and "in-flight" estimates better agree or the predictions
  could be worse than an unconditional (marginalized) prediction.

* Earlier I discussed aspect of wind field structure like thermals, sink,
  and shear, but don't those are sort of "summaries" of the wind field.
  Those are good targets for "feature detectors", but I'm arguing that
  better feature detectors can be created if they have access to the
  underlying wind field.

* Static models that simply summarize historical averages or rates aren't
  useless, but they are pretty boring; for example, in Michael von Kaenel's
  thesis the conclusion was simply "stay along the ridge", which pilots
  already know.

  Instead, we want a probabilistic model that gives answers that have been
  **conditioned** on some *set of observations* :math:`\mathcal{O}
  = \left\{x\right\}`. But there are multiple levels to this: a simple kriging
  model can use just the current observations to try and build a regression
  model over the current state, but conceptually the trained model is
  essentially using the historical data as "pseudo-observations". You're not
  just conditioning the answer based on current observations, but on the
  historical observations as well. Mathematically, we say that the historical
  data is encoded in a *model* :math:`\mathcal{M}`, so the distribution
  becomes :math:`\vec{x} \sim p \left(\vec{x} \given \mathcal{O}, \mathcal{M}
  \right)`.

  This distinction is obvious to data science practitioners, but it's probably
  helpful to make the idea explicit for the less mathematically inclined
  reader.


Problems of discovery and use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Problems of discovery: patterns are discovered by combining structural
  information gained by repeated flights in the same area.

  * Pilots must recognize the structure during a flight. The structure may be
    subtle or the pilot may not be paying attention.

    [[Local structure may be predictive of structure elsewhere, but humans
    are usually better at recognizing local features than relationships
    separated by space.

    Some pilots are more likely to remember the presence of structure versus
    it's absence, but the absence of a feature might be highly predictive of
    structure elsewhere.

    Humans are pretty good at patterns, but I expect computers to beat them
    here (given sufficient data); maybe this is the result of pilots only
    being able to view snippets of the wind field at any one time, as opposed
    to after the flight where the computer gets to see the entire field
    simultaneously?]]

  * Pilots have to remember the structure. Wind fields are complicated, so
    pilots can only remember the average structure and the most significant
    features. Over time, memory of those details fade.

  * Pilots must be able to communicate the structure. Sharing information
    verbally is imprecise and time consuming.

  * Pilots have to recognize **recurring** structure. If some details don't
    seem significant they're likely to be overlooked.


  * Discovering recurring patterns requires combining the data from repeated
    flights in the same area. Individual pilots may intuitively combine the
    data from their own flights, but unless they share their experiences
    with other pilots then the flights of a group of pilots cannot be
    combined.

    Structure must be communicated clearly, but communication between pilots
    is verbal, which is imprecise and time consuming.

  * If two pilots fly in the same area on the same day, they're likely to
    sample different parts of the wind field. That information should be
    combined into a joint estimate.

* Problems of use

  * Pilots have to **remember** the patterns. Most pilots just memorize the
    most reliable features and rely on heuristics for guessing the rest.

  * Pilots have to recognize when they are applicable. [[Some only apply
    during the summer, or if there's a north wind, etc.]]


Conditioning
^^^^^^^^^^^^

* I feel rather strongly that a predictive model that can condition on
  observations of the current wind field **could** dramatically outperform
  a static prediction. What's not clear is **when** it would.

  MVK briefly considered this in Sec:4.2 but his conclusion what that the
  weather conditions that would determine if you'd fly in the first place
  don't help further when predicting thermal (beyond simple day+time
  selectors).

  His conclusion was that the fact that you're flying in an area in the first
  place then that already contains the information that the conditions must be
  favorable, and the thermals that occur are those associated with those
  favorable conditions; the weather conditions themselves are superfluous.

  He didn't elaborate on his procedure, how he determined the wind, etc, so
  I'm not willing to put much confidence in this conclusion.

  It might be suggestive, though, that (assuming he did the analysis
  correctly) that the kinds of thermals his tool looks for are relatively
  insensitive to wind conditions; this could either mean that (1) those
  thermals are fundamentally insensitive to wind direction, or (2) his
  procedure is only capable of detecting the kinds of thermals that are
  insensitive to wind.

  His analysis focused on mountainous areas and cross country flights; that
  might have something to do with it. Maybe high altitude mountain thermals
  tend to be less sensitive to prevailing winds. Pity he didn't consider
  pairwise correlations of hotspot occurrences.


Wind field estimation
---------------------

* To **motivate why it's worth the cost and complexity to recover the wind
  vectors**, I need to start with existing tools (that rely on heuristics),
  list out their limitations, then explain the advantages of estimating the
  actual wind field.

  What do you stand to gain by recovering the wind vectors?

  1. Eliminate (or mitigate) the limitations of relying on heuristics

     * **Use all the information** (don't discard chunks of the track between
       segments; if a glider "loses" the thermal and reenters, don't discard the
       information when they're "outside" the thermal)

     * Don't rely on **fixed feature structure** (like linear thermals)

     * Don't rely on arbitrary (and difficult to tune) thresholds

  2. Enable new functionality / flexibility in learning features

     * Compare the estimated field to forecasts (RASP, Regtherm)

     * Use observations of the actual wind field to predict the features

* Most existing tools that extract wind field structure from IGC files are
  "thermal hotspot" maps. They start by detecting regions where the glider
  exceeded some minimum sinkrate or it ascended more than some cutoff
  threshold. (If you failed to core a thermal then no record would be kept.
  Granted, that might be a good thing, but it also might be too pessimistic.)
  Then they might try to determine the thermal trigger point: `Track2Thermic`
  assumes a simple linear extrapolation; MVK is similar, but he tries to
  correct the linear extrapolation model by seeking elevation peaks near that
  line.

  Ultimately though, they use *heuristics* to estimate the wind, not actual
  system dynamics.

* Thermal detectors are *feature detectors*. They don't estimate the fine
  detail of the wind field; instead they **summarize** regions of the wind
  field using some predefined structure. They don't have access to good
  estimates of the actual wind field, so they rely on heuristics over
  paraglider motion.

  Heuristics rely on the **effects** of the wind field, not the wind field
  itself. The same cause can have many different effects, which is why trying
  to determine the cause from an observed effect is such a pain. More
  importantly, features are summary information about the *effects*, but what
  I really want is information about the underlying *cause*.

  Heuristics fail to make full use of our domain knowledge of canopy
  aerodynamics. There is structure in the data that is not used to collect
  more information. They make inefficient use of the data.

  In summary, heuristics rely on the paraglider track having a particular
  structure (eg, coring a thermal), but **the structure of the flight is not
  necessarily indicative of the underlying structure**. It's suggestive, but
  not equivalent. Using the dynamics lets you recover the underlying structure
  without depending on structure of the flight (although circling flight will
  definitely help reduce uncertainty).

  **Feature extraction should be split into two steps: (1) estimate the wind
  vectors, and (2) extract features from the wind vectors.** Doing those two
  steps at the same time is suboptimal.

* Kept getting lost on how to present existing tools (linearized thermals,
  circling method, etc) that attempt to extract wind field structure from
  position-only flight data. Do I introduce them first, discuss their
  inadequacies, and only then define my performance criteria? Or do I define
  the criteria then show how existing tools fail to satisfy them?

* **Do the limitations of existing predictive tools stem from their lack of
  access to the underlying wind field?**

  Can I start with some limitations of existing tools (limitations in their
  existing functionality or straight up missing functionality) and establish
  that those limitations stem from the fact that they're trying to extract
  information from the **effects** of the underlying thing instead of working
  on the thing itself?

  eg, instead of locating regions of that wind field with rising air, they
  have to rely on heuristics of the paraglider motion


Thermal hotspot detectors
^^^^^^^^^^^^^^^^^^^^^^^^^

* I don't think any of the "thermal detector" type models attempt to determine
  the actual vertical wind velocity. They use heuristics of the paraglider
  motion as a decision function to segment the track based on whether the
  glider appears to be in a thermal.

* Relying on the paraglider motion introduces (at least) two assumptions:

  1. The pilot successfully detect the thermal

  2. They successfully cored the thermal.

     If they missed it, or if they tried and failed, the flight will not
     satisfy the threshold.

* They assume the motion of the glider tracks the shape of the thermal.

* Rely on track segmentation. Appears that most split the track into "gliding"
  and "thermaling" segments. For each "thermal" segment, they mark a hotspot.
  They might use the average horizontal position, or they may try to determine
  the trigger point.

* Methods that attempt to determine the trigger start by linearizing the
  paraglider motion over the thermal segment, and project back to the surface
  to mark a trigger point; some methods simply mark the line's intersection
  with the surface, others (like MVK) attempt to find a nearby point on the
  surface that are more probable to act as thermal triggers (eg, cliffs or
  peaks).

* Using linearization of paraglider motion to determine trigger points assumes
  that the motion center is coincident with the thermal center. Seems like that
  kind of extrapolation is bound to be pretty noisy, especially as AGL
  increases. Also, linearization assumes the thermal is linear, but it's common
  for them to bend.

* Some (like `Track2Thermic`) will record extra information about the thermal,
  such as its inclination (as a proxy for the wind direction).

* By relying on heuristics (such as minimum descent rate, altitude gained, etc)
  they are sensitive to noise. To avoid false positives, they usually apply
  thresholds, such as minimum duration or total altitude gained. The thresholds
  must be large enough to avoid false positives, but not so large as too miss
  short segments.

* They are effectively looking for "thermal signatures" in the paraglider
  motion. This might actually be more effective than a general wind field
  regression approach, but thresholding will likely result in most of the
  tracks (and thus data) being discarded.

* MVK looked into filtering hotspots based on weather conditions (cloud base,
  wind direction and speed, etc), and concluded they didn't provide any extra
  information. In the end he only filters based on day and time-of-day. His
  explanation is that flights in a region occur under similar weather
  conditions; in other words, **the fact that the flight occurred at all
  already contains all the useful information**. The pilot has already selected
  for those conditions.

  Some concerns about his conclusions:

  * How did he filter based on wind? (Pointwise correlations for each hotspot
    against some prevailing wind? Against the wind at the hotspot?

  * What values for the wind did he use?

    In the "Multi Centroid" section of Sec:3.5.3 he mentions using the
    linearization to estimate the wind direction and strength; I assume he
    used this for filtering, which could **easily** explain it. Using
    linearized paraglider motion to estimate wind drift is almost definitely
    going to be super noisy.

    Did he estimate it for each hotspot? Did he try to estimate some global
    mean? He mentions "Regtherm": did he look up the values from that? You
    need to make sure that the estimates of the wind vectors match the actual
    underlying field; if the wind estimates from he flight data are wrong, if
    the forecasts from Regtherm are wrong, etc, you'll get junk output.

* Limitations

  * Don't try to estimate the wind vectors themselves. Instead they rely on
    heuristics: motion patterns the indicate a thermal.

  * The patterns are relatively noisy feature detectors, so they apply threshold
    functions to "validate" segments.

  * Determining the "trigger point" relies on the ability to linearize the
    thermaling segment. (MVK uses piecewise linearization on the top and bottom
    halves to deal with "bending".)

  * **It would be a better to say "these are the regions where pilots often
    experienced lift" instead of "these are the points where pilots successfully
    cored a thermal".**

    I'm also interested in mapping regions of sink; keep the solution more
    general.

* Discussion

  * What if you applied this type of model to the general wind field instead of
    the paraglider track? Best of both worlds? 

    * Focusing on the actual wind field would eliminate relying on the pilot to
      have noticed the thermal and to have cored it correctly.

    * Might allow replacing the arbitrary thresholds with proper probabilistic
      distributions. You're either confident of the estimate or not.

    * The "hotspot" is a very concise information summary, which is nice, and is
      probably the information a pilot would really want anyway.

  * If you started by estimating the wind field, could you use these methods
    there? The goal would be to utilize their strengths (computationally cheap,
    hotspot maps are intuitive) while avoiding their negatives (use the variance
    of the wind field instead of clumsy threshold functions, don't rely on the
    paraglider motion to estimate a linear fit to the thermal, etc)

    It's possible that this "hotspot detector" idea is useful for higher AGL
    scenarios.


Circling method
^^^^^^^^^^^^^^^

* Assumes constant airspeed.

* If a track isn't circling then the circle fit will be dominated by noise:
  fluctuations in airspeed, fluctuations in wind speed, and observation error.
  When the glider is circling, it affords a sort of triangulation; similar to
  triangulation, you don't want the ground velocities to be collinear.
  Circling lets you constrain the solution to a reasonably small region.


Flight Reconstruction
=====================

The primary goal of this chapter is to motivate the paraglider dynamics model.
It should provide a conceptual explanation of how to estimate the sequence of
wind vectors given the sequence of positions. It should introduce Bayesian
filtering and model-based methods. It should define a state-space model for
the data-generating process, and briefly describe how the SSM can be used to
solve the recursive filtering problem; the SSM should clearly motivate the
three dynamics functions (wing, wind, and controls). It should not discuss
specific filtering architectures (particle filters, etc) for solving the
filtering problem.


* Our initial goal is to estimate the wind *field*, but the flight data does
  not record any direct observations of the wind field. It only records the
  glider position over time. Thus, estimating the wind field from the data is
  an *inverse problem*: we need a relationship between the glider's position
  over time, and the wind field.

  The glider interacts with the wind field through the local wind vectors. The
  interaction is given by the canopy aerodynamics. Thus, we have an
  intermediate goal: first, use the canopy aerodynamics to estimate
  observations of the local wind vectors, then use the local wind vectors to
  build a regression model over the wind field (or maybe use them to fit some
  explicit wind field structure, like a thermal).

  **We have no relationship between the wind field as a whole and the
  paraglider's position over time. We only have a relationship to the local
  wind vectors. Thus, we must use our knowledge of the canopy aerodynamics to
  estimate the local wind vectors before we can build the complete regression
  model. (Technically you could build the regression model as part of the wind
  vector estimation process, but this chapter is merely establishing the basic
  workflow.)**

* It is essential to acknowledge the inescapable uncertainty throughout these
  questions. Even the small amount of data we do have (a sequence of positions
  over time) is uncertain due to sensor noise and encoding inaccuracies
  (quantization error). When uncertainty cannot be eliminated, it no longer
  makes sense to look for exact answers, but rather for the distribution that
  covers the plausible range of answers. This is the realm of probabilistic
  methods.

* What is simulation-based filtering? How does it deal with underdetermined
  systems?

* Individual positions tell you nothing except the fact that a pilot chose to
  be flying that day. It suggests reasonable flying conditions, but you can't
  even be sure of that (the weather could have changed, the wing may be
  unusually high performance, or the pilot could just be crazy). The important
  information is how the position changes over time.

* Although a filtering architecture could estimate the wind vectors
  concurrently with the wind field regression model, for simplicity this
  chapter assumes these steps are separate. In particular, it models the
  sequence of wind vectors as a Markov process, which means the wind field
  regression model can't be incorporated into the prior for each wind vector.

* We're trying to relate motion to wind vectors, and that relationship is
  defined by the canopy aerodynamics, so any solution must utilize the canopy
  aerodynamics.

* This inverse problem isn't deterministic: it's stochastic. There is
  uncertainty in the data, wind, controls, and model, so a complete solution
  should provide *uncertainty quantification*. Instead of providing an exact
  answer, there will be ranges of answers and their estimated probabilities.

* Estimating the values of a stochastic process is a *statistical filtering
  problem*.

* Estimating the joint probability directly is intractable, but the Markov
  property allows the problem to be rewritten in a tractable form: the
  *recursive filtering equation*.

  [[Old phrasing: "Statistical filtering problems involving values that evolve
  over time can be modeled with the *recursive filtering equation*."]]

* The recursive filtering equation is composed from a set of priors
  (probabilities before seeing any data), a transition function (a dynamics
  model), and a likelihood function (an observation model).

* The transition function is how we "introduce more information" into the
  problem (via the aerodynamics).

* Writing the wind vector estimation task in terms of the recursive filtering
  equation also reveals that there are several subtasks:

  1. State estimation

  2. Parameter estimation (aka model estimation)

  3. Input estimation (wind and control vector sequences)

* "Solving" the filtering problem simply means "estimate the joint probability
  distribution", then *marginalize* the "nuisance" variables (control inputs,
  model parameters, etc) to compute the joint distribution over the position
  and wind vectors. (*Nuisance variables* aren't interesting by themselves,
  but they must be accounted for: the targets depend on the nuisance
  variables, and so the uncertainty of the nuisance variables must be
  incorporated into the uncertainty of the target variables.)

* In shorter form, given a statistical model (in the form of the state-space
  model) we want to compute the posterior over the states, inputs, and model
  parameters.

  (See "Philosophy and the practice of Bayesian statistics"; Gelman and
  Shalizi, 2013, pp11-12)

* This paper will not discuss filtering architectures for solving the
  filtering problem (this includes all of state, parameter, and input
  estimation). **The focus of this work is on the dynamics model, which
  provides the transition function.**

* The term *flight path reconstruction* seems to have a particular meaning in
  some portions of the aerospace community, where it is used to indicate
  kinematics-based state estimation as a component in model validation and
  calibration. (For a good survey on this topic, see
  :cite:`mulder1999NonlinearAircraftFlight`.) As a kinematics-based method,
  the models are built around *specific forces* and angular rates instead of
  aerodynamic forces and moments. As such, it is more concerned with
  **describing** and aircraft's motion instead of **explaining** its motion.
  (Counterpoint: the MH370 paper calls their methods "flight path
  reconstruction", and they incorporate things like maneuvers, which are not
  pure kinematics?)

  I'm calling my efforts in this paper "flight reconstruction" because it's
  not just the path of the wing I'm interested in. I'm also reconstruction the
  environment of the flight (the wind and control inputs).

* Flight reconstruction as a *state estimation* problem. State estimation
  might mean improving an estimate of an observed quantity, or it could mean
  producing an original estimate of an unobserved quantity.

* Performing *parameter estimation* implies that you have a parametric model
  in the first place.

* In most aerodynamic literature, when they talk about *parameter estimation*
  they typically have access to the aircraft in question and can execute
  a specific set of maneuvers to learn the behavior of the system. I have no
  access to the wing, no knowledge of the control inputs, and the maneuvers are
  assumed unsteady (not the result of the control inputs alone).

* What are some of the problems we face?

  * Indirect observations (it's an inverse problem)

  * Our transition function depends on unobserved variables (underdetermined
    system)

  * We don't have an inverse transition function for the state (have to rely on
    the forward transitions and work backwards)

  * We don't know the forward transition function (we don't know the paraglider
    parameters)

* My main point is that existing tools are limited in what structure they can
  detect/estimate given a flight track. To do better, we need a model-based
  solution: we need a dynamics model.

* If you can produce a better estimate of the structure of the wind field
  during a flight, then you can detect better patterns.

* More detailed knowledge of the wind field structure means more opportunities
  for conditioning predictions. The goal is to condition on the structure. If
  you're limited to the coarse features that existing tools can extract, then
  you're limited in how you can condition.

* If estimates of the conditioning variable are poor, then you might be better
  of with marginal predictions.


Key points
----------

* Introduce inverse problems and filtering problems

* Argue that full flight reconstruction is necessary for wind vector
 estimation

* Motivate the paraglider dynamics model.

* It should convert the informal problem statement (turning sequences of
 positions into sequences of wind vectors) into the formal problem
 of flight reconstruction.

* It should establish flight reconstruction as a filtering problem. It
 should not discuss filtering architectures for solving the filtering
 problem.

* It should introduce all the state variables (paraglider, controls, and
 wind), the basic form of the paraglider dynamics function, the notion of
 a parametric paraglider model, parameters of that model, etc.

* The big objective of this paper is to argue that there exists *some* path
 towards estimating wind vectors from position data. The objective of this
 chapter is to argue that the complete system dynamics (paraglider,
 controls, and environment) are *necessary* to solve the filtering problem.
 It should not attempt to argue that the system dynamics are *sufficient*
 to solve the filtering problem.

* It should leave the reader with a clear map of the steps that would be
 required to use the dynamics to perform flight reconstruction.


Introduction
------------

* The motivating questions of this paper must be transformed into a set of
  mathematical equivalents before we can apply tools that estimate their
  answers. This chapter converts the informal problem statements from the
  introduction into formal, probabilistic relationships.

  This step involves acknowledging the inherent uncertainty in the data and
  their models, defining the underlying, probabilistic form of the questions,
  and using the rules of conditional probability to decompose the problem into
  a series of intermediate steps.

* The starting point for any statistical analysis should be to understand the
  *data-generating process*. If your target is directly involved in the DGP,
  then great, you've got statistical dependence to work with. If not, you'll
  need to introduce additional relationships to induce statistical dependence
  between the observed variables and the target.

* What is *flight reconstruction*?

  * In this paper, the term *flight reconstruction* refers to this process of
    estimating the complete state of the flight at each time step. The rest of
    this chapter defines the "complete state", why it is necessary, etc.

  * [[Should this have been established in the Introduction? Or is this part
    expanding on / formalizing the ideas proposed in the introduction?]]

  * [[Might be a great place to mention the MH370 paper; that's a relatable
    example of a flight reconstruction problem. That paper also has a nice
    introduction to the *Chapman–Kolmogorov equation* which I should
    reference.]]

* What is the intuition behind *flight reconstruction*?

  * Conditional probability is the key, in SO many ways

    * Relates what we know to estimate what we don't

    * Enables decomposition (eg, Markov processes -> recursive estimation)

* What makes the task difficult?

  * We don't have any measurements of the thing we're estimating; we only have
    measurements of a variable which is **related** to it.

  * There is uncertainty everywhere: the dynamics, the other state variables,
    even the measurements are noisy.


Statistical modeling
--------------------

* Is "underdetermined system" the right term? I have latent variables I can't
  solve for exactly, but I can at least produce some estimate of their value.
  I suspect "underdetermined" is wrong (albeit useful for developing the
  concept). See `jaynes1984PriorInformationAmbiguity` for a discussion.

  I think "underdetermined" is probably fine (ie, accurate enough; its meaning
  is clear). In `jaynes1984PriorInformationAmbiguity` he mentions that when
  Bertrand used "ill-posed" he "evidently meant the term in the sense of
  'underdetermined'".

* Interesting to consider the link between *inverse problems* and *statistical
  inference*. I like the discussion at the start of "Introduction to Bayesian
  Computing" (Calvetti, Somersallo; 2007; pg1)

  * *inverse problem*: "the problem of retrieving information of unknown
    quantities by **indirect** observations"

  * *statistical inference*: "the problem of inferring properties of an
    unknown distribution from data generated from that distribution"
    (Calvetti, Somersallo; 2007; pg1)

    Another view: in `jaynes1984PriorInformationAmbiguity`, he (in
    a roundabout way) says that *inference* is the quantitative use of
    probability theory for reasoning logically in indeterminate situations.

  Suppose you have `X = Y + Z`. If you observe Y and Z you can "retrieve
  information" about X via those indirect observations. That's an inverse
  problem.

  But we don't have perfect measurements of Y or Z. So we're still doing an
  inverse problem, but now instead of complete information about X, we have
  incomplete information. If we know the distributions of Y and Z we can
  determine the distribution of X, but X is still considered a *random
  variable*.

* **I strongly support using `=` for the state-space model, and `~` for the
  resulting statistical model.**

* "Probabilistic learning of nonlinear dynamical systems using sequential
  Monte Carlo", page 4, equation 7. In fact, just reread Sec:2 until it
  clicks. This is probably the crux of how I motivate the paraglider dynamics.

* [[Discuss solving systems of equations? Seems like a good place to introduce
  the idea of "solving" underdetermined systems.

  Solving inverse problems is like solving systems of equations: to solve for
  the unknowns you need enough information, where "information" comes in two
  forms: data, and relationships. We don't have enough data, and probably
  can't obtain more (beyond general meteorology information, elevation models,
  etc), so we must try to introduce extra relationships until we have enough
  information.

  Sometimes though there simply enough enough information to completely
  determine the state of all the variables. Such *underdetermined systems*
  cannot be solved exactly; they can only be constrained to some limited
  range. The question then is not "is the value known precisely?" but rather
  "is the value known well enough to be useful?"

* Like most real-world inverse problems, there is uncertainty in every aspect
  of this model: the position sequences are noisy measurements of the true
  position, the paraglider dynamics are an approximation of the true model,
  etc.

  Thus, a complete solution to the inverse problem must provide *uncertainty
  quantification* along with any answer. This is not a measure of the true
  accuracy, but at least it summarizes all the uncertainty that the model is
  aware of.


State-space modeling
^^^^^^^^^^^^^^^^^^^^

* State-space models:

  * Model the evolution of some state over time, with (potentially noisy)
    observations of that state.

  * The idea is to implicitly describe the trajectory using repeated *steps*
    generated by the state transition function.

  * The *filtering problem* is to produce an estimate of the current state given
    all the observations up to the current time.

  * The observations 

A basic discrete-time state space model:

.. math::

   \begin{aligned}
   \vec{x}_{k} &= f_x \left( \vec{x}_{k-1}, \vec{\delta}_{k-1}, \vec{w}_{k-1}, \mathcal{M} \right) \\
   \vec{\delta}_{k} &= f_{\delta} \left( \vec{\delta}_{k-1} \right) \\
   \vec{w}_{k} &= f_{w} \left( \vec{w}_{k-1} \right) \\
   \vec{z}_k &= g \left( \vec{x}_k \right)
   \end{aligned}

And what would it look like in a Bayesian filtering problem?

.. math::

   p_{\mathcal{M}} \left( \vec{x}_{0:K} \given \vec{z}_{0:K} \right) =
     p_{\mathcal{M}} \left( \vec{x}_{0:K-1} \given \vec{z}_{0:K-1} \right)
     \frac
       {
         p \left( \vec{x}_{k} \given \vec{x}_{k-1}, \vec{\delta}_{k-1}, \vec{w}_{k-1}, \mathcal{M} \right)
         p \left( \vec{\delta}_{k} \given \vec{\delta}_{k-1} \right)
         p \left( \vec{w}_{k} \given \vec{w}_{k-1} \right)
         p \left( \vec{z}_k \given \vec{x}_k \right)
      }
      {p \left( \vec{z}_k \given \vec{z}_{0:k-1} \right)}

Or, for the full flight reconstruction problem:

.. math::

   p \left( \vec{x}_{0:K}, \vec{\delta}_{0:K}, \vec{w}_{0:K} \given \vec{z}_{1:K} \right) =
     \prod_{k=1}^K \Big\{
       p \left( \vec{z}_k \given \vec{x}_k \right)
       p \left( \vec{x}_k \given \vec{x}_{k-1}, \vec{\delta}_{k-1}, \vec{w}_{k-1} \right)
       p \left( \vec{\delta}_k \given \vec{\delta}_{k-1} \right)
       p \left( \vec{w}_k \given \vec{w}_{k-1} \right)
     \Big\}
     p \left( \vec{x}_0 \right)
     p \left( \vec{\delta}_0 \right)
     p \left( \vec{w}_0 \right)
     p \left( \mathcal{M} \right)

**Maybe I should introduce a general form of this equation when I'm talking
about state-space models, then refer back to it. Don't define this explicitly
(what does it add to the discussion?), leave it in state-space model form.**


* "State-space models can be used to incorporate subject knowledge on the
  underlying dynamics of a time series by the introduction of a latent Markov
  state-process." (:cite:`fearnhead2018ParticleFiltersData`)

  We tend to do this without realizing it: when we watch a paraglider moving
  around in the air, we use our intuition of wing performance (how the wing
  interacts with the wind) to get a feeling for what the wind is doing. We
  incorporate use our experience with wing dynamics to estimate the wind.


State-estimation
^^^^^^^^^^^^^^^^

* Good books on state estimation:

  * "Optimal State Estimation" (Simon; 2006)

  * "Time series analysis by state space methods" (Durbin, Koopman; 2012)

* Although you could estimate the regression model for the wind field at the
  same time as you're estimating the wind vectors (and indeed, this would
  theoretically perform better), it's easier to model the wind vectors as
  a Markov process.

* The wind is a *latent variable*. We want to infer its value from the
  observed variables.

  Sometimes the latent variable is merely an intermediate value you add to the
  model to connect the observations to the dynamics, but in this case it's the
  latent variable itself which is our target. **The goal of "wind vector
  estimation" is to infer a latent variable.**

  A *latent variable model* is one which "aim to explain observed variables in
  terms of latent variables"; I am attempting to explain changes in position
  by inferring the wind, and then choosing the values that gave the "best"
  explanation.

  Technically the wind could have been measured (but wasn't), so in some
  contexts it would be called a *hidden variable*.

* Every subtask has it's own modeling difficulties. Like for the wind
  regression model, you have to just assume a mean value over the specified
  time interval, which is obviously going to be pretty poor for high variance
  regions. It seems likely that assumed-constant parameters in general are
  likely to struggle; stationarity, homoscedasticity, all sorts of fun
  concepts.

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


Paraglider modeling
-------------------

* Commit to a rigid body assumption

* Sufficiently flexible to model the most important details of real gliders

* Parametrization that makes it easy for users to create desired
  configurations (generating a representative set of wings would be a lot
  easier if more people get involved in coding up the configurations)

* The model design should also consider the aerodynamics methods that will be
  required. Designing with wing sections enables analysis using lifting-line
  methods, which are fast and accurate enough for our purposes. **Call out
  design by wing sections as a deliberate design choice.**

* Need to consider the aerodynamic scenarios we're going to ask of the model:
  I was interested in "glancing blows" through a thermal (when the wing tips
  experience different vertical wind), for example.


Canopy Geometry
===============

* Problem statement: we need a way to estimate the aerodynamics and inertial
  properties of paraglider canopies. Those can be estimated from the canopy
  geometry.

  * The objectives for modeling:

    1. Capable of representing (albeit approximately) existing wings

    2. Intuitive/easy for a user to produce a model of an existing wing by
       using the most readily-available data (technical specs, technical
       diagrams, physical wing-in-hand you can measure, or pictures).

    3. Support aerodynamic methods

  * For aerodynamics, common aerodynamic codes rely on a small set of choices:

    * Points on the chord surface (lifting-line methods)

    * Points on the camber surface (vortex lattice methods)

    * Points on the foil surface (general panel methods, like VSAERO?)

    The geometry should support querying points on all three surfaces. That
    should be sufficient for LLT, VLM, panel codes, and CFD (since you can
    query the explicit 3D geometry).

    I'm pretty sure that targeting LLT methods requires using *wing sections*.
    Similarly, if I want to support empirical adjustments to the viscous drag
    coefficient then obviously that also implies that I need to design the
    wing using wing sections.

* How do you design a mathematical model that achieves those requirements?

  * [[Through careful decomposition and parametrization. Introduce "wing
    sections" and how they simplify wing design using a two step process
    (specify the scale, position, and orientation of sections, then assign
    section profiles). Introduce the concept of section chords and the chord
    surface.]]

  * The shape of a parafoil canopy can be defined in many ways. The simplest
    way is to specify a set of points over the surface to produce an explicit
    representation of the shape. The issue is that the intricate, non-linear
    geometry of a parafoil requires a large number of points.

  * Instead of defining the shape with an explicit set of points, the complex
    shapes of parafoil canopies can usually be decomposed into a simpler set
    of parametric equations.

  * If a complex shape can be represented with simple parametric equations,
    then each parameter of the parametric equations tend to be better at
    capturing structural knowledge than the explicit set of points.

  * Because each parameter communicates more information than an explicit
    coordinate, fewer parameters are required, which tends to mean much less
    work is required to specify a design target.

  * The conventional way to decompose a wing is to use *wing sections*. Wing
    sections make a wing easier to design and easier to analyze.

    [[Discuss designing with chords + profiles versus designing the surfaces
    directly.]]

  * Instead of designing the 3D shape of a wing directly (ie, as a large set
    of points), simple wings are traditionally decomposed into 2D wing
    *sections* :cite:`abbott1959TheoryWingSections` distributed along the
    span.

    [[I don't like this phrasing: what does "directly" mean? Probably better
    to talk in terms of **structure**, since I'm thinking in terms of
    structured vs unstructured shapes; maybe use those terms?]]

  * [[What the advantages of designing with wing sections as opposed to
    designing arbitrary wing geometries? ie, what are the benefits of the
    structured approach of "design by wing sections"?]]

  * Designing the wing is then broken into two steps:

    1. Specify the scale, position, and orientation of each section.

    2. Assign a 2D profile to each section, called an *airfoil*, which defines
       the upper and lower surfaces of the section.

  * There are a variety of conventions for the first step. [[This is where
    you specify the chord surface. By "variety of conventions" what I mean is
    "variety of parametrizations", but they're all relatively similar.]]

* How should I cite the "Paraglider Design Handbook"? Just as a website?

* Not sure where to put this, but I'm going with a "canopy" coordinate system
  `c` instead of a "wing" coordinate system, because (1) many sources use `w`
  for "wind", and (2) the paraglider wing inherits the canopy's coordinate
  system (the canopy can exist without the wing, not vice versa).


Parametric designs
------------------

* I claim that I need a parametric paraglider dynamics model. Why?

  * Due to model uncertainty, flight reconstruction will can use the correct
    model; instead, we have to rely on a representative of paraglider dynamics
    models. Unfortunately, we don't have any paraglider dynamics models, much
    less a set that covers the range of available wings. At best we have a set
    of minimal technical specs, so we need a tool that lets us produce wing
    models from technical specs. **Parametric models with a good choice of
    parametrization make it easy to model wings from simplified technical
    specs.**

  * Explicit geometries are too time consuming to expect users to produce them
    by hand. I need to produce reasonably accurate models with less effort.

  * (Idealist vision) Parametric models support parameter estimation. Existing
    data probably won't work, but conceptually it'd be nice to support.

* Interesting that although most designs allow linear interpolation of airfoil
  geometries, it's trivial to support arbitrary interpolation functions (as
  long as they're smooth). Exponential, logarithmic, etc, they're just how you
  determine the transition factor between the two.

* Interesting to note that "design by wing sections" is closely related to
  common 3D modeling methods. It is similar to *lofting* in the sense that you
  are generating a solid by interpolating between profiles at each section. It
  is similar to *sweeping* a profile along a curve, except that the profile
  (the shape being "swept") can change size (if the wing uses a non-constant
  chord), shape (if the wing uses a non-uniform profile), and orientation
  (rotation of the profile about the curve if there is geometric twist).

  Another big difference is the use of separate curves for designing in the
  `x` and `yz` planes, but you could probably convert this definition into
  a single curve (eg, compute the final leading edge) and scaling factor (the
  chord lengths scale the profiles). **This geometry should be straightforward
  to use as an input to a 3D modeling program.** In fact, FreeCAD and Blender
  already have Python API's, so this should be pretty easy to use this as
  a backend for parametric geometries in those programs.]]


Wing sections
-------------

* I'm not interested in a grand exposition of airfoil considerations. I just
  want to draw attention to the aspects that are important enough to affect my
  modeling choices. However, this might be a good place to introduced many of
  the relevant aerodynamic concepts/terminology (angle of attack, stall point,
  chord, camber, pitching moment, aerodynamic center, etc)

* There are some model constraints if the canopy aerodynamics can be analyzed
  using section coefficient data. In particular, segments must be able to be
  well-approximated as a single profile given a width. Things that cause this
  constraint be violated include:

  * Non-uniform profiles along the segment (need smaller segments)

  * Non-uniform torsion (again, need smaller segments)

  * Section y-axes are not parallel to each other (eg, wedge-shaped
    segments)

  * Section y-axes are not parallel to the segment quarter-chord (eg,
    "sheared" sections, like with swept wings or vertical sections with
    non-flat yz-curves)

* Important terms: leading edge, trailing edge, chord line, camber line, upper
  surface, lower surface

* Common parameters: maximum thickness, position of maximum thickness, max
  camber, position of max camber, nose radius, trailing edge angle (?)

  ref: http://laboratoridenvol.com/paragliderdesign/airfoils.html#4

* Ways to specify the curve of an airfoil:

  * Explicit set of points

  * Parametric function of the curve itself

  * Camber line, thickness function, and a convention


Parametrization
---------------

* The goal is to design a wing using simplified *design parameters* instead of
  specifying the surface points directly. A good parametrization imposes
  structure on the geometry, which has several advantages:

  * Mitigate the excessive flexibility in the general equation (restrict
    designs to "reasonable" values, or at least designs that can be roughly
    analyzed using section coefficients)

  * Reduce the workload (parameters are like "summaries")

  * Make wings easier to modify

  * Make wings easier to compare

  * Make it easier to specify design uncertainty (priors)

* What do I mean by "parametrize the general equation"?

  [[I mean "define the variables of the general equation using parametric
  functions that capture the underlying structure of the canopy."]]

  The general parameters are able to represent any structure, but they don't
  encode enough structure. This is a problem because it pushes the work onto
  the designer. If you can assume more underlying structure you can save the
  designer from needing to provide that structure themselves. A good choice of
  parameters lets them focus on the important details.

  The purpose of a parametric surface is to decompose a complicated surface
  geometry into a set of simple design functions. The purpose of "parametric"
  functions (like an elliptical arc) is the **capture the structure** of the
  function, preferably with as few parameters as possible.

  [[I feel like "parametric function" is poorly named, unless that's
  a conventional way to say "specify the values of a function through
  functions of some parameters instead of specifying the values directly".

  Counterpoint: the "parameter" of a parametric function essentially chooses
  a particular instantiation of that function. Think of the parameters as
  choosing some constants that complete the definition of the function.]]

* Existing surface parametrizations are either awkward (you can do what you
  need, but it's to fiddly), limited (you can't use it to express your desired
  design), or incomplete (eg, the PDH left a lot of the equations undefined).
  Fixing those problems is what what motivated my work on a new
  parametrization. I started by defining a general surface equation (for
  points on the surfaces), then showed that different definitions of those
  general parameters can "recover" those existing parametrizations. I finished
  with a particular choice of parameter definitions that make it easy to
  define parafoils.

* Benedetti :cite:`benedetti2012ParaglidersFlightDynamics` uses fixed `r_x
  = r_yz = 0.25`.

* I never really thought about it, but if the general surface equation can
  "recover" existing models (given an appropriate parametrization), then **an
  implementation that targets the general surface equation should be
  compatible with specifications from those existing parametrizations**. You
  just need an "adapter" model. You should be able to handle geometries from
  AVL, XFLR5, etc.

* How would I describe the parametrizations MachUpX, XFLR5, AVL, etc? More
  importantly: should I even try? Probably best to just discuss their choices
  at a high level without trying to put them into mathematical form. The
  angle+direction in particular would require calculus (unless you were okay
  strictly describing them in terms of linear segments)

* :cite:`lingard1995RamairParachuteDesign` [[Parametrization?]]

* You can position wing sections in several ways

  * Absolute coordinates (from the wing root)

  * Relative coordinates (from the previous section)

  * Absolute angle and distance (from the wing root)

  * Relative angle and distance (from the previous section)

  (NB: angles for positioning may be different from angles for orientation)

  **When would angle+distance be preferable?**

  Some parametrizations use a combination for the different position components
  (like XFLR5 which uses absolute position for `x`, and section-relative
  angle+distance for `y` and `z`).


Section index
^^^^^^^^^^^^^

* **MY CHOICE OF SECTION INDEX HAS A NAME:** it's the *normalized arc length*
  of `yz(s)`. It's great because users don't need to care how long it is,
  the index is always `-1 <= s <= 1`. I don't use the arc length of the 3D
  position curve because it was much more difficult to imagine the effects.
  You can't just look at the yz-curve by itself and say "`s = 0.5` should be
  right about there" because you can't see the "depth" due to the x-component
  of position. Oh, and you can't use `x` by itself (what's its length?), but
  `yz` has a length independent of the parametrization.

* Recall the idea of a *section index*: it's a way to uniquely identify
  a "spanwise station". Most aerodynamic methods use `s = 2 * y / b`, but for
  parafoils I found it more convenient to use `s = 2 * y_flat / b_flat`.

  **A section index should not depend on the geometry itself.** The identity
  of a section "which section" should not change just because the geometry
  changed. This is important if you ever want to handle distortions (eg, cell
  compression). 

  It was confusing me earlier today: I was trying to determine what AVL used
  for the section index, but it describes the geometry using a set of explicit
  positions (xyz for the LE), so there's no obvious choice. Then I remembered
  that the section index was supposed to represent some normalized index from
  0 to 1 (or +/- 1). It can be convenient to use for defining a wing (like
  I do), but not required.

* Section index enables you to decouple parameters: for example, I don't want
  to care about `y` at all when defining `x` or `c`. It can also be useful
  when *querying* the sections; you can define a wing using section indices
  but query it using `y`, or whatever; the section index can make it easier,
  however, especially for highly curved wings like a parafoil.

  **Summary: using an abstracted *section index* has advantages both for (1)
  designing the geometry and (2) querying points on the geometry.**

* Many tools define a geometry just by specifying a set of coordinates and
  relying on linear interpolation between them. There's no **explicit**
  "section index" necessary to define the geometry. Nevertheless, the
  position along the leading edge line will still designate a unique section.


Existing parametrizations
^^^^^^^^^^^^^^^^^^^^^^^^^

* AVL:

  Section index: `s = 2y/b`. This isn't obvious: they use discrete sections,
  so there isn't an explicit section index, but spanwise panel spacing is
  determined according to `y`. I guess you could argue this is a function of
  the aerodynamic method, but I'd argue that since they're using `y` to
  specify the segments that that's implicitly they're choice of how they index
  the sections of each segment. **I suppose if you only allow pointwise
  section definitions and never deform the geometry (ie, flattening it) then
  maybe the section index is irrelevant?**

  Position: leading edge for position reference point and rotation point;
  absolute coordinates for position

  Orientation: Sections spanwise axes are always parallel to yhat (so sweep is
  a shearing effect). Sections are rolled so they remain perpendicular to the
  segment yz-curve (my notation), which matches 

  Sections are sheared along `x`, and rotated to remain perpendicular to `yz`.
  You can specify an intrinsic (body-axes) Euler angle for relative pitch, but
  it only changes the aerodynamics; the chords themselves (the actual
  geometry) are always parallel to xhat.

  From `avl_doc.txt`:

    Xle,Yle,Zle =  airfoil's leading edge location
    Chord       =  the airfoil's chord  (trailing edge is at Xle+Chord,Yle,Zle)
    Ainc        =  incidence angle, taken as a rotation (+ by RH rule) about the
                   surface's spanwise axis projected onto the Y-Z plane.

    [...]

    Note that Ainc is used only to modify the flow tangency boundary condition
    on the airfoil camber line, and does not rotate the geometry of the
    airfoil section itself. This approximation is consistent with linearized
    airfoil theory.

* XFLR5:

  Section index: `s = 2yflat/bflat`

  Position: confusion here. The program uses `y` but it's really `y_flat`; for
  example, a panel from `y=0` to `y=1` at `dihedral=45` would end with an
  actual y-coordinate of root(2). The `x` is an absolute coordinate called
  `offset`. The `z` is determined by the total change accumulated from the
  start. You can't specify `z` directly, you can only specify the `dihedral`
  and wait for `z` to accumulate across the segments. (Yuck.)

  The `z` is like MachUpX then; specify a `dihedral` angle (intrinsic Euler
  section roll) and a segment "span".

  Orientation: intrinsic Euler pitch-roll sequence. Section pitch angle
  specified by `twist`, section roll angle is specified by `dihedral`, the
  initial intrinsic Euler roll angle of each section. Sections are linearly
  blended into the next segment. The final segment terminates at the exact
  angle specified for that segment.

* MachUpX: `s = y`; leading edge for position reference point; absolute
  coordinates for `y`; explicit section pitch and roll intrinsic Euler angles;
  the `x` and `z` are calculated by projecting along the specified angle until
  reaching the next specified `y` (I think? Review)

  Section index: `s = y_flat / semispan` (`y_flat` is implicit)

  Position: leading edge. No absolute coordinates at all, you can only specify
  direction and distance for each segment. Define `sweep` and `dihedral` to
  produce a vector direction, and the segment length (segments are specified
  using normalized section indices, then scaled by `semispan`) is the vector
  magnitude.

  Orientation: `dihedral` determines section roll, `twist` determines section
  pitch, sweep does not produce section yaw (so it just shears in `x`).
  Standard intrinsic pitch-roll Euler sequence.

* Benedetti: `s = y`; quarter-chord for position reference point; absolute
  coordinates for position; absolute section pitch as intrinsic rotation
  angle; implicit section roll from `dz/dy`

* Paraglider Design Handbook:

  The site figures show a "referral line" for position, and "rotation point"
  for rotation origins. Both are chord ratios (they lie on the chord). In the
  diagram he says they don't need to be the same, but from the code it looks
  like they always are.

  Also weird: he requires the designer to specify both `y` and `yflat`. He
  uses back-right-up coordinates, so he calls them `x-rib` and `xp` (for
  "xprime").

  For torsion, if `kbbb = 0`, then he uses `washin`. If `kbbb = 1`, then
  `alpham` sets the max washin and uses linear interpolation (he uses `x` for
  `y_flat`, so its just linear interpolation over the section index). If `kbbb
  = 2` then you can add an offset `alphac` for the wing root, then he uses
  linear interpolation out to the tip.

  I think `x-rib` is `y_flat` and `xp` (x-prime) is `y`?

  He uses a "right-back-down" coordinate system. You specify `y_flat` as `x`,
  and `y` as `x'` (x-prime, or `xp` in the code).

  Section index: `s = 2 * y_flat / b_flat`

  Orientation: intrinsic Euler pitch (angle: `Washin`) then intrinsic Euler
  roll (angle: `beta`) (**same as me!**)

  Positioning is weird: the user specifies both the flat and projected
  spanwise coordinate for every rib (instead of just defining the flat span
  and the final position). This wing design seems to rely on some external
  program computing the positions, `x`, `xp`, `z`, etc: they all depend on how
  you've curved the wing, but in a sense I think they contain redundant
  information (so `lep` doesn't have to compute it?). Very odd, and awkward:
  I hate having to rely on a third-party CAD tool. **Why have rotation angles
  and whatnot at all if you're just going to require the user to calculate
  stuff in CAD?**

  In the picture he mentions a "referral line", but I can't find that anywhere
  in the code. I'm pretty sure this never made it into implementation.
  Whatever his intent, you can only specify the "rotation point" (but what the
  does the `z` coordinate designate? The position of the RP?)


My parametrization
^^^^^^^^^^^^^^^^^^

* My particular parametrization makes some reasonable assumptions about
  parafoils that lets it eliminate a few parameters, and use intuitive specs
  to define those more general parameters.

  This is where I choose a definition of the section index, set `r_y = r_z
  = r_yz`, parametrize `C_c/s` using Euler angles, etc. Conceptually you can
  start with a unit square, then specify the chord lengths, then specify the
  flat span, then the torsion, then `x(s)`, then `yz(s)`, and never have to
  worry about messing up the previous steps.

* I need analyze the canopy aerodynamics by using section coefficient data,
  which affects my choice of parametrization.

  To keep the sections perpendicular to the segment span I set `r_y = `r_z`
  and use the derivatives of `yz` to define the section roll angle. (Not sure
  I'm actually required to set `r_y = r_z` for this to work, but it's more
  intuitive, and I prefer simpler designs.) [[**Does this belong here?** Or
  should it go in the "Orientation" subsection when I'm choosing the
  parametrization of the DCM?]]

* For notational simplicity, I'm going to drop the explicit section index
  parameter :math:`s`, so  :math:`LE(s) \to LE`, :math:`r_x(s) \to r_x`, etc.

* If I'm using `r_x` etc for the reference points on the chord, then I kind of
  like using `r` (instead of `pc`) for selecting a point on the chord, since
  it seems intuitive to consider `r_x - r`, etc; the reference versus the
  requested. Or maybe `t`, since that's the "standard" variable for parametric
  curves.

* **My design is very closely related** to the one in "Paraglider Design
  Handbook", except he requires explicit rotation points and he doesn't appear
  to allow different reference points for `x` and `yz`. (Also, it doesn't look
  like the code supports `RP` anyway, despite it appearing in the site
  diagrams.)

* Should I acknowledge that parametric surfaces usually use `u` and `v` for
  the parameters?

* Discuss the parameters (`-1 <= s <= 1` and `0 <= r <= 1`; at least,
  I think those are the parameters? They are the arguments of the design
  functions.)

* Discuss the design functions (`x(s)`, `C_w2s(s)`, etc)

  **Those parameters can themselves be parametric functions** of some
  (arbitrary) choice of section index (eg, an elliptical arc). Discuss
  explicit vs parametric design curves (expressiveness versus number of
  parameters, essentially).

  Explain that some "functions" can be scalars, like `r_x(s) = 0`

  Note that at this point that although the design curves are parametrized
  by the section index it has only been defined as an arbitrary parameter
  that uniquely identifies a section (ie, the general form of the equation
  acknowledges that some index must exist, but leaves its definition
  unspecified).

* In my canopy geometry definitions, I'm using `\Gamma` for "dihedral", but
  aren't `\Theta` and `\Gamma` simply the Euler angles? Shouldn't I use
  standard Euler angle notation? Sure, `\Gamma` is typically use for "wing
  dihedral", but dihedral is usually the angle between the xy-plane and the
  vector from the wing root to the wing section, isn't it? If so, then
  `\Gamma` is misleading.

* Confirm my use of terminology: "dihedral" versus "section roll". How do you
  differentiate between the angle the vector from the origin to the section
  makes relative to the y-axis versus the intrinsic Euler roll of the section?
  XFLR5, MachUpX, and Benedetti use `dihedral` to refer to **section** roll
  angle; `jann2003AerodynamicCoefficientsParafoil` refers to *arc anhedral
  angle* as the angle from root-to-tip. In "General Aviation Aircraft Design"
  (Gudmundsson; 2013; pg318) he refers to dihedral as the angle made by the
  vector from the root to the **wingtip**.

  Summary: **section vs wing (or "arc") anhedral**. Hrm. On the bright side,
  I can use `theta` and `gamma` for the Euler angles, which just so happen to
  match the standard notation for torsion and dihedral (well, `Gamma` for
  dihedral, but ah well; maybe `gamma` for section dihedral isn't such a bad
  thing; "big" versus "small" for "wing" versus "section" has a nice symmetry
  to it).

* **Why is using a reference point on the chords so important?** You could use
  any reference point relative to the leading edge; what's so special about
  points on the chord? I feel like there was something related to distortions,
  or the ability to analyze via section coefficients or something, but I can't
  remember what.

* Should I rewrite my definition (the equation showing my parametrization) of
  the LE so it's explicitly proportional to the wing span? In general it
  doesn't have to be, but for my implementation it is (I think). I'm defining
  a curve with `yz` etc, but you have to scale it up by `b_flat / 2`.

  Including this explicit scaling factor is (1) more accurate, and (2) might be
  useful for comparing to other parametrizations (like the one in MachUpX).

* Should my "design curve" plots match the notation in the code?

* **Provide a table of parameter symbols, names, and descriptions.** It should
  match the six function plots in all of my examples, and appear before those
  examples to make it super clear.


Section index
^^^^^^^^^^^^^

[[I need to motivate my choice of section index, choosing `r_y = r_z` (to make
designing `yz` more intuitive), and using a roll-pitch Tait-Bryan sequence (or
a pitch-roll "proper" Euler angle sequence?) for the DCMs.]]

* *section index*: a unique identifier for each section.

* What I'm calling a "section index" is often called a "spanwise station" in
  literature. See "General Aviation Aircraft Design", Eq:9-36 (pg 319/325).
  I'll probably stick with this since it's more explicit (it's an index, so
  I'm going to call it that) plus I don't want any mixups between the classic
  definition of `spanwise station = 2y/b` (especially since that name doesn't
  say **which** span). Kinda nice that "station" and "section" both start with
  `s` though.

* **Major reasons I'm introducing the section index**: the `y` are non-linear
  relative to `y_flat`, so things like twist produce weird spanwise variations
  if you use `y`. Also, `y_flat` includes a scaling factor that the normalized
  `s` does not, so parameters don't depend on the absolute scale of the wing.

* My definition of the section index is similar to something used by Abbott,
  except he used `s = 2 * y / b` whereas I'm using the flat versions.

* Flat coordinates are useful since they can be measured from a wing lying on
  the ground.

* The arched versions are less convenient when sampling points along the
  span (as is done in Phillips).

* The traditional choices are the y-coordinate (so :math:`s \defas y`) or the
  normalized span coordinate (so :math:`s \defas 2 \frac{y}{b}`), but those
  become unwieldy for non-linear wings. (They are also non-constant if the
  wing is subject to deformations which change the section y-coordinates.) For
  parafoil design it's much more convenient to use the flat spanwise
  coordinate (this simplifies mixed design between the flattened and inflated
  wing shapes).

  Assuming the semispans are symmetric (reasonable for a parafoil), define:

  .. math::

     s \defas \, 2 \, \frac{y_\mathrm{flat}}{b_\mathrm{flat}}

* I'm using :math:`b_\mathrm{flat} = \mathrm{length}(yz(s))` even though the
  :math:`yz(s)` might not define the "true" physical span. (The reference
  points might not be the maximum y-coordinates.)

* I should mention that although I've define the section using the normalized
  arc length of `yz`, **it doesn't prevent you from using conventional
  (explicit) definitions**. For example, in Belloc, he doesn't give the
  section index, but that's okay: I just recompute them from the points.


Scale
^^^^^

[[Interesting stuff about chord lengths goes here. This is about how you
specify the chord distribution, and not a discussion about wing design (taper,
aspect ratios, etc).]]

* The *scale* of a section is the scaling factor to produce the section
  profile from a normalized airfoil curve.

* How do you specify scale?

  * What is a chord?

    The *chord* of a section is the line connecting the leading edge to the
    trailing edge. The scale of a wing section is determined by the length of
    the chord.

  * The airfoils are scaled such that the camber line starts at the leading
    edge and terminates at the trailing edge of the section. (In other words,
    an airfoil is the section profile normalized by the chord length.)

* You can specify chords as either a position and length, or as two
  positions (typically the leading and trailing edges). `FreeCAD` and
  `SingleSkin` do it that way; probably more?

  I suspect that the position+length representation lends itself to simpler
  equations, but it'd be interesting to check. For example, suppose
  a straight `0.7c` with an elliptical chord; what do the leading and
  trailing edge functions look like? Do they lose that nice,
  analytical-function look?

  Of course, the difference is a bit moot: if you have `LE(s)` and `TE(s)`,
  just set `r_x = 0` and `c(s) = norm(LE(s) - TE(s))`.


Position
^^^^^^^^

[[Interesting stuff on positioning sections goes here. Leading edge, trailing
edge, quarter-chord, whatever.]]

* How do you specify position?

  * The position of a section is the vector from the wing origin to some
    reference point in the section-local coordinate system.

  * The leading edge of a wing section is the most common section-local origin
    because airfoils are traditionally defined with the leading edge as the
    origin. This choice is convenient since the wing section and the airfoil can
    share a coordinate system.

  * The most common reference point for the position is the leading edge, but
    other choices are possible.

* What is :math:`yz(s)`? In short, for each section of the wing, pick the
  point at :math:`r_{yz} \, c` back from the leading edge. Project that
  point onto the yz-plane. Do this for all sections to produce a curve. The
  :math:`s` is the normalized length along that curve. The length of that
  curve also defines :math:`b_\mathrm{flat}`, since it would be the span of
  the reference line if you "unrolled" the wing so all the z-coordinates are
  zero.

* Point out that although the "leading edge" and "trailing edge" of the
  airfoil is defined by the camber line (which in turn defines the chord
  line), the chord line of the airfoil is ultimately just a way of
  positioning the profile onto the chord surface. You could choose any
  arbitrary line, you just need to make sure that whatever line you use to
  generate the coefficients matches the orientation and scale of the profile
  you assign to the final wing.


Orientation
^^^^^^^^^^^

* How do you specify orientation?

  * The orientation of a section is the orientation of the section's local
    coordinate system relative to the wing's.

  * Can specify it explicitly using angles, or implicitly by specifying the
    shape of the position curves.

* [[From PDH: "washin promotes spanwise tension and stability, preventing the
  wing tips fold unexpectedly".

  It also encourages the wing to stall from the wing tips first; unlike plane
  wings, you want the middle of the wing to be the last to stall so you don't
  "taco" the canopy.]]

* Section DCMs can be decomposed into intuitive design parameters by defining
  the section orientations as Euler angles. The decomposition also facilitates
  mixed-design of the flattened and inflated wing geometries. [[How?]]

* Euler angles can be encoded using "intrinsic" or "extrinsic" axes: intrinsic
  rotations are rotations about the body-fixed axes, extrinsic rotations are
  about the axes that are fixed in the object being rotated. Intrinsic
  (body-fixed) rotations are referred to as "proper Euler" angles; extrinsic
  (object-fixed) rotations are referred to as "Tait-Bryan" angles.

* I've chosen to parametrize the section orientations as an intrinsic
  pitch-roll sequence, so :math:`\phi` for section dihedral and :math:`\theta`
  for section torsion.

  Note that this breaks with my earlier work that refers to "section dihedral"
  as :math:`\Gamma`. I decided to abandon :math:`\Gamma` as the parametrization
  (how you **specify** section orientation) for several reason:

  1. Section dihedral is a pain to define in an unambiguous way for wings with
     geometric torsion: do you use the angle between the body y-axis and (a) the
     section y-axis or (b) the projection of the section y-axis onto the
     yz-plane?

  2. :math:`\Gamma` already has a conventional definition as **wing** dihedral
     (overloading it to refer to section dihedral is not ideal)

  3. I've been trying to always use right-handed rotations for everything, but
     the conventional definition of a positive dihedral angle corresponds to
     a negative right-handed rotation about the +x-axis.

  4. Euler angles already have well established conventions for the angle
     variables (phi, theta, gamma).

  In short, a formal definition of section dihedral angles might be an
  interesting concept from the perspective of wing analysis, but for wing
  design it's not very helpful.

* The way I've designed section roll and pitch correspond to either an
  intrinsic pitch-roll sequence or an extrinsic roll-pitch sequence. (How do
  the matrices compare? So far my definition has been using intrinsic angles;
  should I stick with that? What does the extrinsic pitching rotation matrix
  look like? Keep in mind, I want to define the roll matrix using `dz/ds` and
  `dy/ds`.) One advantage is conceptual: assuming the wing starts out flat,
  you can think of the section torsion as happening first, so pitch-roll is
  intuitive.

* This DCM parametrization keeps the section y-axes in the yz-plane (ie, it
  ignores `dx/ds`). Positioning with `x(s)` simply shifts the sections
  ("shears the chords") into position with no rotation with no rotation about
  the z-axis. (I'm pretty sure this is a reasonable constraint for most wing
  designs? Using wing section coefficient data assumes the wing segment can be
  described by taking a uniform section profile and stretching it by some
  width; if the sections in the segment have section yaw, then then segment
  would be a wedge, and the "linear segment" approximation falls apart.)

  Related: https://www.youtube.com/watch?v=w1AuPn_oBnU. I suspect that they
  aren't reorienting the profiles but are simply reorienting the ribs to
  minimize cross-flow. Simple concept, you just need to compute the
  "typical" airflow for a point on the wing and slice the wing along that
  airfoil (so the ribs won't match the section profiles anymore).

* Using `yz` to define `phi` keeps the sections perpendicular to the segment
  spans, plus it reduces the number of parameters.

* Might be good to define washin, washout, angle of incidence, mounting angle,
  etc. There's quite a bit of confusion around those terms, so I'm explicitly
  trying to avoid using them at all. I'm using the angle relative to the
  central chord, that's it.

* *geometric torsion*: the section orientation angle produced by
  a right-handed rotation about the wing y-axis

  Or, the angle from the wing x-axis to the section x-axis, as produced by
  a right-handed rotation about the wing y-axis

  .. math::
     :label: section_torsion

     \Theta \defas
        \arctan \left(
           \frac
              {\vec{\hat{x}}_\mathrm{wing} \times \vec{\hat{x}}_\mathrm{section}}
              {\vec{\hat{x}}_\mathrm{wing} \cdot \vec{\hat{x}}_\mathrm{section}}
           \cdot \vec{\hat{y}}_\mathrm{wing}
        \right)

  From the definition of the torsion angle :math:`\Theta` in
  :eq:`section_torsion` you have the rotation matrices for geometric torsion:

  .. math::
     :label: section_torsion_matrix

     \mat{\Theta} &\defas \begin{bmatrix}
        \cos(\theta) & 0 & \sin(\theta)\\
        0 & 1 & 0\\
        -\sin(\theta) & 0 & \cos(\theta)
     \end{bmatrix}

* *section anhedral*: the angle from the wing y-axis to the section y-axis, as
  produced by a right-handed rotation about the wing x-axis.

  Note that this mathematical definition of the anhedral angle is different
  from the conventional definition of dihedral angle. The convention for wing
  dihedral is that the angle is measured as the positive "upwards" angle of
  the wing. That definition is ambiguous, so this definition uses signed
  angles and standard right-hand rules.

  [[FIXME: **I need to choose** a standard term: dihedral or anhedral. I think
  I prefer dihedral simply because it's more common, and if I use `\Gamma` I'd
  like it to agree with convention. There is the downside that it's
  a **negated** right-hand rotation about the +x-axis, but if I'm not using
  `Gamma` to define the section orientations it probably doesn't matter.]]

  .. math::
     :label: section_dihedral

     \Gamma \defas
        \arctan \left(
           \frac
              {\vec{\hat{y}}_\mathrm{wing} \times \vec{\hat{y}}_\mathrm{section}}
              {\vec{\hat{y}}_\mathrm{wing} \cdot \vec{\hat{y}}_\mathrm{section}}
           \cdot \vec{\hat{x}}_\mathrm{wing}
        \right)

  To use the airfoil data you need the spanwise axis of the wing segments to
  be parallel to the wing sections that comprise the segment. (At least,
  I think that's the case: I doubt the airfoil coefficients would be accurate
  if the sections were slanted relative to the segment span.) You can enforce
  this parallel alignment by constraining the section dihedral to stay
  orthogonal to the yz-curve, which is why I define the dihedral with the
  derivatives of `yz`. If you didn't do that you'd have a sort of shearing of
  the sections along the segment.

  Oh, I bet this is also related to why lifting-line methods fail for swept
  wings; part of that is because of spanwise flow, but you also have sections
  y-axes that don't align with the segment!]]

  From the definition of the dihedral angle :math:`\Gamma` in
  :eq:`section_dihedral` you have the rotation matrices for section dihedral:

  .. math::
     :label: section_dihedral_matrix

     \mat{\Gamma} &\defas \begin{bmatrix}
        1 & 0 & 0\\
        0 & \cos(\Gamma) & -\sin(\Gamma)\\
        0 & \sin(\Gamma) & \cos(\Gamma)
     \end{bmatrix}

  The disadvantage of :eq:`section_dihedral_matrix` is its dependence on the
  arctangent function in :eq:`section_dihedral`, which is undefined for wing
  sections that achieve a 90° section dihedral. To avoid the divide by zero,
  the matrix can be computed using the derivatives of the arc reference
  curves:

  .. math::
     :label: section_dihedral_alternative

     \Gamma = \arctan \left( \frac{dz}{dy} \right)

  .. math::

     \begin{aligned}
     K &= \frac{1}{\sqrt{\left(dy/ds\right)^2 + \left(dz/ds\right)^2}}\\
     \\
     \mat{\Gamma} &= \frac{1}{K} \begin{bmatrix}
        K & 0 & 0\\
        0 & dy/ds & -dz/ds\\
        0 & dz/ds & dy/ds
     \end{bmatrix}
     \end{aligned}

* Section direction-cosine matrix (DCM):

  .. math::
     :label: section_DCM

     \mat{C}_{c/s} = \mat{\Gamma} \mat{\Theta}

* Section :math:`x`-axis:

  .. math::

     \vec{\hat{x}} = \mat{\Gamma} \mat{\Theta} \begin{bmatrix}1\\0\\0\end{bmatrix}

* I think this design happened because I wanted the arc (yz-curve) to define
  the section orientation. The wing starts flat, then the lines pull various
  sections downwards (and inwards), which is why I start with a flat wing and
  then rotate it about the global x-axis (not the section x-axes): it was
  simply easier for me to reason about. Oh, and **to compute the final angle
  of a section you don't have to integrate over all the section-local
  angles.**

  Consider what would happen if the yz-curve did not define the section
  orientation: you would have section profiles sheared along the curve, their
  y-axes not parallel to the segment span. You are going to get some funky
  cross-flow due to spanwise pressure gradients (section coefficients assume
  uniform pressure distributions along the segment span) so the section
  coefficients are unlikely to be representative of the actual behavior.

  (Hm, **how does this work with wing sweep?** I'm not allowing section yaw,
  but if the wing is swept then the section y-axes are not parallel to the
  quarter-chord segment.)

  **If I state up front that I want a simple geometry that's amenable to
  analysis by wing coefficients, then these choices are well motivated.** Of
  course, I can't yet define or analyze billowing cells but ah well.

  Aah, okay, I get it now: you start by designing the flat wing. I'm assuming
  that when the wing is flat the only thing you design is `c(s)`, `x(s)`, and
  `theta(s)`: the wing is flat, so that rotation is naturally about the wing
  (global) y-axis. You then use the line geometry to pull down on the sections,
  and I assume that pulling down will produce a bending, not a shearing, of the
  wing segments; also, the lines don't know (or care) about the section x-axes,
  they which is why dihedral is rotation about the global x-axis. It's all
  about the sequence of events.

* The choice of parametrization of the section orientation arises from the
  intuitive sequence of wing design. You start by laying out the wing sections
  of the flat wing; the section y-axes start parallel to the body y-axis, and
  geometric torsion leaves them that way. You then use the line geometry to
  pull down on the sections to produce the yz-curve; the lines are assumed to
  pull straight down without distorting the section profiles, which means
  bending the cells, not shearing them.

  These assumptions are probably a bit strong for "real" wing design. In
  particular, the assumption that the section y-axes all start parallel to the
  body y-axis. Assuming no relative yaw is also suspect; just because it makes
  analysis with section coefficients more difficult doesn't mean wing
  designers don't do it.


Discussion
----------

Distortions
^^^^^^^^^^^

* Should I discuss cells, billowing, distortion, etc, in the paper? I'm not
  working on / implementing these, so they can probably go in the
  "Limitations" section (whatever that turns out to be)

* There are are two types of distortion to a canopy:

  1. *Static* distortions

     Theoretically you could pre-compute these and incorporate them into the
     rigid-body model. Things like cell billowing (which changes the section
     profiles and "compresses" the cell and wing widths)

  2. *Dynamic* distortions

     My model (currently) assumes a rigid body model, so I'm not modeling
     dynamic scenarios like weight shift, riser control, accelerator-induced
     section "flattening", wing collapse, wing tip flapping, etc.

* References:

  * Babinksy (:cite:`babinsky1999AerodynamicPerformanceParagliders`) discusses
    the effect of billowing on flow separation, and
    :cite:`babinsky1999AerodynamicImprovementsParaglider` discusses using
    stiffeners to reduce the impact

  * Kulhanek (:cite:`kulhanek2019IdentificationDegradationAerodynamic`) has
    brief discussion of these impacts

  * Belloc (:cite:`belloc2016InfluenceAirInlet`) discusses the effects of air
    intakes, and suggests some modeling choices

  * There are a bunch of papers on *fluid-structure interaction* modeling.

  * Altmann (:cite:`altmann2009NumericalSimulationParafoil`) discusses the
    overall impact of cell billowing on glide performance, and has a great
    discussion of how design choices (cell structure, ribs, etc) can mitigate
    the problem; in future papers
    (:cite:`altmann2015FluidStructureInteractionAnalysis`,
    :cite:`altmann2019FluidStructureInteractionAnalysis`) he discusses
    implementation details. Fogell
    (:cite:`fogell2014FluidstructureInteractionSimulations`,
    :cite:`fogell2017FluidStructureInteractionSimulation`,
    :cite:`fogell2017FluidStructureInteractionSimulations`) has a lot to say
    on FSI, including some critique of the applicability of Altmann's method
    to parachutes.

    Another recent paper well worth reviewing (good discussions and great
    references list) is :cite:`lolies2019NumericalMethodsEfficient`, which is
    co-authored by Bruce Goldsmith! Neat. One of their big ideas seems to be
    using "mass-spring systems" from computer animation applications for
    paraglider cloth simulations.


Canopy Aerodynamics
===================

* Discuss the methods for estimating the aerodynamic forces on a wing. What
  are their pros/cons? Why did I choose Phillips? Does my geometry make it
  easy to use CFD methods?

* In `lingard1995RamairParachuteDesign` he uses a linear aerodynamics model.

* Make sure to highlight the usefulness of having a full non-linear dynamics
  model (versus simple linear models such as *stability derivatives*). **Hit
  this hard! Make it blindingly obvious that having access to an accurate
  non-linear model will support future tasks.**

* I will need to discuss the limitations of the lifting-line methods. For
  starters, you need to have previously computed the coefficients for the
  deformed section profile, including when braking, and for the range of
  Reynolds numbers.

* Steady-state assumption: In the conclusion of "Specialized System
  Identification for Parafoil and Payload Systems" (Ward, Costello; 2012), they
  note that "the simulation is created entirely from steady-state data". This
  is one of my major assumptions as well. This will effect accuracy during
  turns and wind fluctuations, and ignores hysteresis effects (boundary layers
  exhibit "memory" in a sense; the same wind vector can produce a separation
  bubble or not depending on how that state was achieved).


Validation
----------

* I'll be using Belloc's wind tunnel data, but what other considerations are
  their for checking the performance (accuracy) of the model? And how do
  I communicate it?

* I should choose the most common performance measures of a wing and show those
  (the "polar curves", stability curves, etc?)

* Should I make a plot of uniform and non-uniform wind? Maybe show the two
  section lift plots on top of each other. Maybe a summary statistic ("the
  asymmetric wind case produce 20% more lift on the other side!" etc)


Scratchwork
-----------

The original way to estimate the aerodynamic forces on a wing was introduced
by Prandtl. This method assumes that the quarter-chord of the wing is
a straight line with a constant airfoil. More sophisticated methods allow for
a quarter-chord that arcs in a 2D plane, but because a paragliding wing
typically has both dihedral and sweep, it requires a 3D lifting line method.
I chose a method developed by Phillips, which is essentially a vortex panel
method with a single panel.

Unfortunately, Phillips' method doesn't seem to work very well. I tried to
recreate the results from :cite:`belloc2015WindTunnelInvestigation`, but
I seem to be overestimating the lift, thus significantly overestimating the
wing's performance. Thankfully, this is not unexpected: in
:cite:`chreim2017ViscousEffectsAssessment` they investigate Phillips'
nonlinear numerical lifting line theory. He checks it for convergence and
accuracy against three wings: straight, elliptical, and swept. It converged
for the straight and elliptical wing, but not for the swept wing (so no good
data could be produced), but for the other two methods is overestimated CL for
the straight and elliptical wings. In
:cite:`chreim2018ChangesModernLiftingLine` he reintroduces the *Pistolesi
boundary condition* to mitigate the shortcomings of Phillips' method, but he
claims corrects the performance for wings with sweep; he does not test it with
wings with dihedral.

Thankfully, all this uncertainty isn't a big deal in terms of my project,
since I'm not expecting to filter true flight tracks anyway. My model is still
sufficient to demonstrate the qualitative behavior of a wing in interesting
flight scenarios, as well as for developing the infrastructure. True, the
method I implemented (Phillips) doesn't work terribly well, but my wing
geometry definitions are well suited for more sophisticated methods.
Calculating points anywhere on the wing is easy, allowing for 3/4 chord
positions (the *Pistolesi boundary condition*) for better numerical lifting
line methods (see :cite:`chreim2017ViscousEffectsAssessment`), or for the
generation of a 3D mesh suitable for computational fluid dynamics (CFD)
methods.


References
----------

* :cite:`phillips2000ModernAdaptationPrandtl` introduced a numerical LLT

* :cite:`hunsaker2011NumericalLiftingLineMethod` investigates Phillips' method
  and observe that CL increases as the grid is refined. **This is great news
  since that matches my experience.** (I need to read that paper, but this note
  is taken from :cite:`chreim2017ViscousEffectsAssessment`, section 3.1.3 (pg7).

  Observed issues with wings with sweep and/or dihedral. In particular, on pg4:
  **"As the numerical integration is refined, the velocity induced along the
  bound portion of a vortex sheet with sweep approaches infinity."** Note that
  this quote was referring to their method using vortex sheets, but in the
  conclusion they also say "For wings with sweep and/or dihedral, the method
  does not produce grid-resolved results which was also found to be the case
  with the method of Phillips and Snyder."

* :cite:`chreim2017ViscousEffectsAssessment` reviewed the effectiveness of
  Phillips' method to flat wings with rectangular, elliptical, and swept
  planforms. Confirmed the issues with sweep noted by Hunsaker. **Good
  discussion of the theory.** Failed to find convergence for the swept wing?
  Why would that be? Granted, it was swept 45 degrees, which is pretty severe.
  He doesn't give the details of the non-convergence.

* :cite:`chreim2018ChangesModernLiftingLine` adapted Phillips method to use
  the Pistolesi boundary conditions, and verified that is was able to predict
  the section coefficients for a wing with 45-degree sweep.

* :cite:`mclean2012UnderstandingAerodynamicsArguing` has a good discussion on
  lifting-line methods (see page 381) and some of their limitations, the
  Pistolesi boundary condition, etc

* `bellocWindTunnelInvestigation2015`: wind tunnel data, useful for checking if
  Phillips' method is applicable to a paraglider (assuming my section
  coefficient data and implementation are correct)

  Works through several developments related to estimating the dynamics, and
  has a great summary in the introduction. In the introduction mentions that
  "Theoretical analysis of arched wings is scarce in the literature, partly
  because the Prandtl lifting line theory is not applicable to arched wings",
  then in his conclusion, "using a 3D potential flow code like panel method,
  vortex lattices method or an adapted numerical lifting line seems to be
  a sufficient solution to obtain the characteristics of a given wing".

* :cite:`kulhanek2019IdentificationDegradationAerodynamic` tested Phillips'
  method on the Belloc reference wing (he also discusses many other aspects of
  a paraglider, such as cell distortion, line drag, the harness, etc)


Paraglider Geometry
===================

* Building a parametric paraglider model requires parametric components. One
  of the motivations for my project is to build a top-down parametric
  paraglider system.

* **Drive home why parametric is so important for my needs.** It makes it
  easier to model existing wings, which makes the models easier to compare
  against existing wings. It also makes it easier to implement existing wings,
  which makes it less expensive to build a database/catalog of models for
  existing wings. I need a catalog of wings in order to build a distribution
  over the wing parameters, which is necessary for the flight reconstruction
  model (which is uncertain about the wind model, thus needs a prior over wing
  models.) It also increases flexibility: a fixed canopy geometry doesn't
  allow making the lobe anhedral a function of the accelerator, which has
  significant effects on aerodynamic performance (eg, modern wings often have
  their best glide ratios when a small amount of speedbar has been applied,
  keeping the wing more arced for "hands-up stability").

* I started with designs from :cite:`benedetti2012ParaglidersFlightDynamics`,
  and applied extensive modifications to support the needs of my thesis.

* Did I ever investigate / discuss the effect of riser width? In real wings
  that has a pretty big effect on weight shift control, but for weight shift
  control I'm only modeling the shift in the center of mass.


Paraglider Dynamics
===================

* Should I discuss my commitment to stateless models?

* I should include a test case flying through some sort of non-uniform wind
  field, since that was one of my original design requirements of the
  aerodynamics method. Glancing blow of a thermal was my original idea.

* There is a lot of literature on *parafoil-payload* systems. Discuss that and
  relate it to my current work. Degrees of freedom, connection types, etc. Good
  to frame my design in terms of existing literature to make them easier to
  relate.



Conservation of angular momentum
--------------------------------

.. code:: python

   # With `delta_a = 0`
   In [1]: J_w.round(3)
   Out[1]:
   array([[386.351,   0.   ,   3.449],
          [  0.   , 334.429,   0.   ],
          [  3.449,   0.   ,  53.431]])

   # With `delta_a = 1`
   In [1]: J_w.round(3)
   Out[1]:
   array([[378.398,   0.   , -36.486],
          [  0.   , 330.8  ,   0.   ],
          [-36.486,   0.   ,  57.755]])


So, when you press the accelerator you'd expect `P` an `Q` to increase, and
`R` to decrease (in order to maintain angular momentum). Thankfully the change
is relatively minor (in my opinion). The +x displacement does reduce the yaw
rate by about 8%, but you're not usually yawing terribly fast anyway, right?

So, I will *ignore* conservation of angular momentum due to changes in
accelerator and air density (that is, changes over time), but I will
*incorporate* their instantaneous values when calculating angular
acceleration.


Flight Simulation
=================

Key points:

* Defines a set of states.

  These states do not need to be the same thing you would give the dynamics
  model, but you need to be able to convert between the two; for example, the
  position state might be `lat/lng/ele`  even though the paraglider dynamics
  expects `x/y/z`. This is important later when using the dynamics for
  filtering, since the flight data deals with latitude and longitude. The
  simplest is to use the *flat-Earth equations* ("Aircraft Control and
  Simulation"; Stevens, 2016); the tangent-plane approximation should work fine
  over the small ranges typically covered by a paraglider.

* Builds a stateful model from the stateless paraglider dynamics model

* Requires dynamics models for the wing, wind, and pilot controls

* Useful for model verification, behavior investigation, and building sample
  flight data for the purpose of developing the flight reconstruction
  software.


An aircraft *dynamics model* defines the instantaneous rate of change over
time of an aircraft's state variables in response to a given input. A *flight
simulator* uses the aircraft dynamics model to produce a time series of model
states called a *state trajectory*.

Simulated flights are essential for testing the [[accuracy/correctness]] of an
aircraft model. They are also essential for testing flight reconstruction
algorithms: they provide complete knowledge of the true world state, which can
be used to validate the output of the flight reconstruction process. [[unlike
real flight data, which has many unobserved variables, a simulated flight has
access to the entire state space. This allows you to verify how well
a reconstructed flight matches the "true" state. It isn't perfect, of course:
just because you can reconstruct a simulated flight doesn't mean the method
will work on real flights, but if it fails on simulated flights then you can
be sure it will also fail on real flights.]]

To generate interesting test flights, you need interesting flight conditions,
where "interesting" may refer to the wind, or pilot inputs, or both. This
chapter is a cursory overview of those "interesting" scenarios.


Encoding Rotations
------------------

* :cite:`sola2017QuaternionKinematicsErrorstate` has a great discussion of the
  many different quaternion encodings


******
Topics
******


Atmosphere
==========

Good general atmospheric references:

* Atmospheric Thermodynamics (North, Erukhimova; 2009)

* Atmospheric Science (Wallace, Hobbs; 2006)


Definitions
-----------

* "The *geoid* is the shape the ocean surface would take under the influence
  of gravity **and the rotation of the Earth** alone, if other influences such
  as winds and tides were absent." This is not a sphere, or even an oblate
  ellipsoid; it is an irregular surface, since the Earth does not have uniform
  density; the surface of the geoid is higher than the reference ellipsoid
  wherever there a mass excess, and lower than the reference ellipsoid
  wherever there is a mass deficit. All points on the geoid have the same
  *effective potential* (the sum of gravitational potential energy **and**
  centrifugal potential energy).

* *geopotential altitude* is "calculated from a mathematical model that
  adjusts the altitude to include the variation of gravity with height"

* *geometric altitude* is "the standard direct vertical distance above mean
  sea level"


Lapse rates
-----------

* Lapse rates are typically given in terms of geopotential altitude (not
  geometric altitude)

* The *dry adiabatic lapse rate* is 10.0 C/km. The *moist adiabatic lapse
  rate* is 0.55 C/km. The average lapse rate defined by the international
  standard atmosphere is 6.49 C/km (the ISA model is "based on average
  conditions at mid latitudes"). The average is between the dry and moist
  adiabatic lapse rates, which makes sense.

* Super-adiabatic lapse rates

  How can the environmental lapse rate be *greater* than the DALR? **I think
  I'm missing the significance of adiabatic processes.** I'm guessing the dry
  adiabatic rate is kind of a reference line; if you go above or below this
  nicely behaved curve, stability changes.

  According to `theweatherprediction.com`, a super-adiabatic lapse rate is
  usually caused by intense solar heating at the surface.

* How does an adiabatic process work?

  "An *adiabatic process* occurs without transfer of heat or mass of
  substances between a thermodynamic system and its surroundings. In an
  adiabatic process, energy is transferred to the surroundings only as
  *work*."

* I'm planning to group group all the {altitude, pressure} measurements into
  a single set, and fit them to a single dry adiabatic curve. Does my "fit to
  a single dry adiabatic curve" equivalent to saying that I'm pretending that
  those measurements were all taken from the same parcel of air rising through
  an adiabatic expansion?  Seems like a rather strong assumption.

  Also, I'm assuming that the lapse rate doesn't vary with horizontal changes.
  **Is this reasonable?** For example, around mountainous terrain, if the
  boundary layer follows the topography, then the air near the mountain will
  probably be hotter than the air further away, right? (ie, I'm assuming that
  neighboring region will have roughly the same temperature at the same AGL?)


Convective boundary layer
-------------------------

Synonyms: *convective planetary boundary layer*, *atmospheric mixing layer*,
*dry adiabatic layer*

* The CBL is a PBL when positive buoyancy flux at the surface creates
  a thermal instability and thus generates additional or even major turbulence
  (aka, *convective available potential energy*, or CAPE)"

* "A CBL is typical in tropical and mid-latitudes during daytime."

* How far up do thermals extend? That is, how high can paragliders fly?

  According to `garratt1994ReviewAtmosphericBoundary`, it is generally below
  [2 - 3] km, but over deserts in mid-summer under strong surface heating the
  ABL may be as much as 5 km deep, and even deeper in conditions of vigorous
  cumulonimbus convection"

In `oberson2010ConvectiveBoundaryLayer`, he emphasizes that this is the layer
mixed by **dry** thermals; do you never have thermals in saturated air?


Inversion layers
----------------

* What is an inversion layer?

  When the atmospheric temperature is increasing instead of decreasing with
  altitude.

* What are the types of thermal inversions?

  There are *surface* inversions near the Earth, and vs *aloft* 

* What is the range of altitudes where they're likely to occur? Under what
  conditions are they more common (hot or cold days)? What is the role of
  local geography (eg, mountains increase thermal inversions in valleys)?

  (Sounds like in Salt Lake City they're more common during the winter, but
  I'm not sure if that generalizes to "they're more common during cold days".)

* What are the effects of a thermal inversion layer?

  * Temperature inversions block atmospheric convection. (Describe *stable*
    versus *unstable* air; note that "unstable" is not the same as
    "turbulent"; "instability" refers to the amount of positive bouyancy).
    This lack of mixing traps pollutants, so air quality decreases.

    I suspect this also reduces the maximum height of thermals?

  * As rain falls into cooler if, it can produce freezing rain.

* How do thermal inversions relate to lapse rates?

* How likely are paragliders to encounter thermal inversions? (ie, how
  important/relevant are they for the purposes of my thesis?)

  They are more common above valleys surrounded by mountains, so I suppose
  mountain flying is more likely. (Ridge soaring is typically lower altitude
  anyway, isn't it?)

* What are the differences between a *thermal inversion layer* and *cloud
  base*?

* Interesting sidenote: if you're able to reliably detect thermal inversions,
  that could be a really interesting model input. I'm guessing it'd be at
  least somewhat informative regarding the behavior of thermals in that region
  (presence/absence, etc).


Wind Features
-------------

* The most basic wind field is still air. Another basic test case is a uniform
  wind field, where the wind vectors are the same everywhere; the uniform wind
  field is useful to verify glider performance (a 360 turn in a non-zero wind
  field should produce a drifting helix, not a circle).

  The more interesting scenarios are where the wind vector is variable in time
  and/or space. Although real wind conditions are complex and variable, for
  testing purposes it is useful to focus on specific features. In
  :cite:`bencatel2013AtmosphericFlowField` they identify three basic categories
  of wind behavior: wind shear, updrafts, and gusts. Shear is a change in the
  wind vector for a change in position, updrafts (and downdrafts) are non-zero
  vertical components of the wind vector, and gusts are changes (typically
  rapid, turbulent changes) to the wind magnitude and/or direction.


Bayesian Filtering
==================


* The *curse of dimensionality* refers to needing **more** data as the
  dimension increases. When you simplify the model, you can abstract away some
  of the detail, leading to the *blessing of abstraction*
  (:cite:`goodman2011LearningTheoryCausality`), which refers to the observation
  that sometimes its easier to a learn general knowledge faster than specific
  knowledge. (ie, simpler models are less specific, thus more general, but
  there are fewer parameters (and possibly **simpler** parameters) which are
  easier to fit (less data).

* The more information I want to squeeze out of the data, the more structure
  I need to introduce. You don't get something for nothing: for every question
  you want to answer, you need either need more data or more structural
  information (like paraglider wing dynamics)


State-space models
------------------

* Several great quotes from the introduction to "Particle filters and data
  assimilation" (Fearnhead and Kunsch; 2018):

  "State space models can be used to incorporate subject knowledge on the
  underlying dynamics of a time series by the introduction of a latent Markov
  state-process." (This is the essence of what I'm doing, except that I'm not
  using the latent values to improve my estimate of the position: I'm
  interested in the latent state itself.)

  "A state-space model specifies the joint distribution of all the variables
  that are required for a dynamic model based on subject knowledge, and the
  variables that have been observed."


Forward versus Inverse Problems
-------------------------------

* "Inverse problems include both parameter estimation and function estimation.
  [...] A common characteristic is that we attempt to infer causes from
  measured effects. A forward, or direct problem has known causes that produce
  effects or results defined by the mathematical model. Because the measured
  data is often noisy or indistinct, the solution to the inverse problem may be
  difficult to obtain accurately."

* In a sense, filtering uses solutions to the forward problem to produce
  a weighted set of solutions to the inverse problem.

* Inverse problems attempt to infer unobserved causes from the observed
  effects.


Probabilistic inference / simulation-based filtering
----------------------------------------------------

* I liked this sentence in Duvenaud's dissertation:

    "*Probabilistic inference* takes a group of hypotheses (a *model*) and
    weights those hypotheses based on how well their predictions match the
    data."

* "**data** driven forecasting" vs "**model** driven forecasting" (see
  `reich2015ProbabilisticForecastingBayesian`)

  * Model driven: eg, by analyzing topography (for example, RASP)

  * Data driven: eg, by analyzing raw position (like von Kaenel's thesis)

  Basically, do you look at the observations alone (with no though to the
  underlying model), or do you also refer to the "surrogate process" (the
  *data-generating process*) from which they were generated?

  He describes "data-driven" as "bottom-up", or *empirical* models, whereas
  "model-driven" are "top-down" or *mechanistic* models. Empirical models rely
  on the data, mechanistic models rely on the model dynamics.

  On page 182: "model-based forecast uncertainties taking the role of prior distributions"


Data Assimilation
-----------------

*Data assimilation* is to geophysics what *filtering* is to engineering. They
both deal with the *state estimation problem* by combining theory (models)
with observations (data). See `fearnhead2018ParticleFiltersData`. (I like this
paper. One of its stated goals is to encourage interoperability between
geophysics and engineering disciplines. Section 1.2 has a very helpful
overview of the related terminologies of the two fields.)

I should try to phrase my problem in terms of both, or however makes sense to
tie in the geophysics realm. There's probably a bunch of good literature to
cite.


Validation
----------

* I read somewhere that a guy complained about testing your model by fitting it
  against simulated data (or something; he didn't like the idea that "yay, we
  recreated data we expected!" was not helpful). Gelman, on the other hand, is
  a huge fan of *fake-data simulation*, where you generate data from a model
  using "true" parameters, then observing the behavior of the statistical
  procedures (how well they work, how they fail). There is a related procedure
  called *predictive simulation*, where you fit a model, generate data from it,
  then compare that generated data to the actual data (I believe this is also
  called *posterior predictive checking*). See
  :cite:`gelman2007DataAnalysisUsing`.


Jittering
---------

If the process noise is small, you don't get much variation in the particles
during the time update. One way to decrease the odds of sample impoverishment
is to use *jittering*. See `fearnhead1998SequentialMonteCarlo`, page 53



Flight Reconstruction
=====================

The flight simulation section discussed how to use the paraglider model with
known inputs (controls and wind) to generate state trajectories. Part of that
discussion was to define the state variables. The flight reconstruction
concept could start by defining *inverse problems* and *underdetermined
systems*, which leads into probabilistic methods (*simulation-based
filtering*). The purpose of flight reconstruction (in this context) is to
determine the unknowns (here, those are the model parameters, the control
inputs, and the wind vectors).

Key points:

* Bayesian filtering combines the observed data with prior knowledge of the
  system to generate a joint distribution over all the variables. Bayesian
  methods require priors (over the state values, model parameters, and model
  inputs), a likelihood (for the observed data), and model dynamics (for the
  state transitions).

* Monte Carlo methods generate the joint distribution by exploring the
  possible space of plausible values. The exploration of different values uses
  *proposals*. The proposals must incorporate existing knowledge of the
  variables, including its constraints. For example, the model parameter
  proposals should reflect realistic wing configurations. The wind dynamics
  should not exceed realistic turbulence power distributions. Control inputs
  should be relatively low frequency (eg, it's unlikely for the speedbar to go
  from zero to maximum in a quarter of a second).

* Ultimately, flight reconstruction is a *Bayesian filtering problem*


Data preparation
----------------

Key Points:

* In order to perform flight reconstruction on actual flights, you need to
  parse, sanity check, clean, and transform the IGC data into the format
  required by the dynamics model.

* The outputs from this stage are the only parts of the flight that were
  observed; everything else must be simulated. These data limitations
  establish the constraints for the flight reconstruction stage.

Example tasks:

* Sanitize the timestamps

* Debias the variometer data (via dynamic time warping or similar)

* Estimate atmospheric conditions (air density in particular)

* Track segmentation. The filter assumes the paraglider is "in-flight", so
  this implies detecting takeoff and landing, as well as dealing with stall
  conditions (which essentially break up the track by rapidly ramping
  uncertainty).


Cramer-Rao
----------

A big design point of my filter is that I know I won't get super precise
estimates, but all I need are **sufficiently** precise estimates.

The Cramer-Rao lower bound is the theoretical lowest variance estimator of
a static parameter. In my case, the static parameters are those belonging to
the wing. Honestly though, I don't care about those nuisance parameters. What
I do care about are the dynamic thermal parameters (eg, the thermal center).
Forget whether my filter achieves the best possible estimate; does the
theoretical best possible estimate give me **sufficient** precision?

In `notter2018EstimationMultipleThermal` they investigate this question for
their multiple thermal tracking particle filter. I should review this notion
and summarize the conceptual impact on my design, even if I can't reproduce
the actual CLRB for my model. (Notice, the CLRB is typically defined for
static parameters, but Notter uses the results from
`tichavsky1998PosteriorCramerRaoBounds` to apply the concept to the dynamic
parameters of the thermal centers).

Q: doesn't the CLRB depend on the form of the likelihood function? What is the
likelihood function (aka the data distribution) for my system?

**Try to describe the likelihood function for my filter, in non-mathematical
terms.**


Proposal Distributions
----------------------

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


Pilot Control Inputs
^^^^^^^^^^^^^^^^^^^^

There are several considerations for generating realistic pilot control
sequences:

* Controls don't change erratically (they are generally smooth)

* Controls tend to change together (you don't want full left brake and right
  weight shift, or full symmetric braking together with full speedbar)

* Controls tend to be the result of a pilot attempting some maneuver (so you
  can consider the controls a latent process of the unobserved "maneuver")

I'm unhappy with treating the four pilot controls as independent random walks
(for the purpose of my filtering method), since that will generate mostly
nonsense control sequences. Also, common random walk stochastic processes such
as *integrated white noise* or an *integrated Ornstein-Uhlenbeck process* are
**mean reverting**, which may not be good for control inputs, because why
would you assume a particular mean value?

It's also a problem that the controls range from `0` to `1`, so the random
walk must be constrained. You can use a Gaussian random walk with a logistic
transform over the output to map `(-inf, +inf)` onto `(0, 1)`, but you'll need
to adjust the magnitude of the step size near the bounds (and even then you'll
never actually reach them), and the nonlinear transform means the steps will
be more likely to revert to `0.5` than towards the bounds.


And even if you solve the bounds issue, there's still the issue of "does the
output resemble a realistic control sequence?" Control inputs do tend to have
lots of little variations as the wing bounces around, but they're dominated by
periodic *manuevers* where the controls vary together systematically (ie, they
become highly correlated). Random walks will produce particularly poor
performance during constant input maneuvers, like during a 360 turn. (Random walks
and their ilk will be very unlikely to produce fixed brake positions, which
are essential to smooth flights.)


For correlated controls (ie, how they vary together), I may want to think of
the pilot controls as points on some "data generating manifold". This idea
shows up in animation, using low-dimensional manifolds for generating
high-dimensional human skeletal animations; see Wang's thesis
`wang2005GaussianProcessDynamical`. The manifold is a kind of constraint on
how the variables change together.

* Should I model the pilot controls as *multivariate autoregressive Gaussian
  processes*? (See `turner2011GaussianProcessesState`, section 3.6)

* **How is this done in human motion tracking?** Do they use previously
  learned manifolds to perform a sort of "maneuvering target tracking", where
  they determine what "maneuver" the human is performing and choose the
  manifold for that maneuver?


* There's some good info in "Pattern Recognition and Machine Learning". I like
  Chapter:6 (kernel methods) and Chapter:12 (continuous latent variables).


* I like the terminology used in `li2003SurveyManeuveringTarget`: they're
  discussing the *input estimation problem*, and separate the methods into two
  categories: *model-based* and *model-free*. (Related: "data driven" vs "model
  driven", from :cite:`reich2015ProbabilisticForecastingBayesian`)

  Model-based methods rely on some concept of *maneuvers*: prior knowledge of
  likely input sequences. These can be hand-crafted or learned from data. Maneuvers
  (particularly in high dimensional space, such as human motion) are often the
  output of a process over some low-dimensional latent space; if you can learn
  the manifold over that low-dimensional space and the mapping to the high
  dimensional space, you can track the target via the latent variables.

  Model-free methods are essentially random walks: they assume no prior
  knowledge of likely input sequences. (Although they may assume knowledge of
  the derivatives, leading to things like *integrated white noise*.) These are
  simple to implement, but are likely to have excessively high variance
  compared to realistic inputs.

* Decision-based maneuvering target tracking is a *decision problem*. You must
  decide about the onset and termination of a maneuver, which makes this
  a *track segmentation problem*, which is ultimately a *change-point
  detection problem*. (see "Part IV" of Li's "Maneuvering target tracking"
  survey series).

* Li (`li2002SurveyManeuveringTarget`) says that *decision* is selection from
  a discrete set of candidates, whereas *estimation* is selection from
  a continuum of candidates. So if you have a predefined set of maneuvers, you
  have a decision-based problem (the current maneuver). If the target's
  control inputs operate on a continuum, you have an estimation problem (the
  current value of the input).

* Interesting sidenote: consider the likely inputs from a pilot; there's a lot
  of potential structure there. They're unlikely to symmetric brakes with
  accelerator because it defeats the purpose. They're unlikely to use small
  (eg, 5%) asymmetric brake inputs with accelerator since it may exhibit
  inverted control authority. They're more likely to use weight shift with
  accelerator for directional control. They're unlikely to use small
  asymmetric input for a long duration, unless they're deliberately "crabbing"
  into the wind (a huge radius 360 is uncommon).

  Suppose you low-pass filtered the true control inputs. Would it look roughly
  like a sequence of maneuver inputs? (eg, straight, left turn, straight, left
  turn, hard left turn)


Using Gaussian processes
------------------------

A Gaussian process is good for enforcing smoothness, and since they're good
for human animation they're probably also good for handling the correlations
and maneuvers. Another big advantage is that Gaussian probabilities are the
easiest to combine with other methods that expect Gaussian random variables
(eg, you can use the mean+covariance directly inside the GMSPPF?). I'm hoping
that I can make the GMSPPF work together with the GP (the GMSPPF samples from
the GP prior and updates the GP by using the posterior mixture as
pseudo-observations), but there's a problem: **the GMSPPF seems nice for
producing the filtering distribution, but not so nice for generating plausible
state trajectories since the particles don't retain ancestor information**
(you know the state distribution at each point, but for any point in that
distribution you don't know the state distribution that led to that specific
point).

Aah, but wait: sure, that Gaussian mixture is a big lumpy distribution, but
can't you just compute queries using each individual Gaussian mixture
component **as if it was the only one** and adding their results?

FULL STOP, THINK ABOUT WHAT YOU'RE DOING

I've lost sight of the purpose here. The purpose of the GMSPPF is to drive
forward the state of the wing (namely, it's pose); the evolution of that state
is the result of the wing dynamics, given the wind and pilot controls as
inputs. But what if I don't know the pilot controls? I need to place
a distribution over that set of random variables as well; I also need
a transition function to let them evolve over time, which means I need
a dynamics model for the pilot controls. The dynamics model should encode
realistic behaviors; I am thinking a Gaussian process is a good way to produce
that encoding.


As a maneuvering target
-----------------------

"In manoeuvring target tracking, a primary trade-off is the robust tracking of
manoeuvres against the accurate tracking of constant velocity (CV) motion."

This is saying that you need to trade off between smooth motion accuracy (the
constant velocity notion) versus accelerated maneuvers. White noise
acceleration does provide a probability distribution with support over the
constant velocity trajectory, but random walks are likely to generate
unrealistic motion (aircraft are frequently well-described as CV, but random
walks are virtually never CV).

This is one of the different approaches I should highlight: maneuvering target
tracking might use pre-defined maneuvers (structured dynamics) or random walk
(unstructured). For example, the MH370 search used structured (pre-defined)
maneuvers, but my random walk PF will probably use unstructured (random walk)
proposals.


Likelihood function
^^^^^^^^^^^^^^^^^^^

The likelihood function answers "how probable is this observation given the
state+model?" My only observable is the GPS data, and I'll need to choose
a noise model. GPS errors are often non-Gaussian, but that's still a common
choice. I should at least mention that, and that there are some methods for
attempting to "check the estimator for consistency" (eg, using a *Chi^2 test*;
see `bar-shalom2004EstimationApplicationsTracking`, Sec:1.4.17)

Some of the problems with the GPS data in an arbitrary IGC file:

* Unknown raw signal noise characteristics observed by the device

* Unknown signal filtering performed by the device

* Quantization effects from encoding lossy GPS coordinates in the IGC file

* I'll need to explicitly call out my decision to convert the latitude and
  longitude data into a tangent-plane coordinate system.


Filter Validation
^^^^^^^^^^^^^^^^^

One of the advantages of Bayesian methods is that you have a *generative
model*: given all the dynamics you can generate new sample tracks, degrade
them with synthetic noise, then use it to check the performance of the filter.

It would be cool to show how the GPS coordinates degrades with different types
of noise (Gaussian and Student-T in particular). If I had a working filter I'd
love to see how different noise models (the true noise versus the noise model
in the likelihood function) affect filter performance. I don't have a working
filter, but I think this is still worth mentioning. Namely, **one of my
deliverables is a generative model that can be used for filter validation**.


Wind Estimation and Prediction
==============================

* The goal of an *online* predictive model (ie, during a flight) is to
  *calculate the conditional distribution over the wind field*. This goal
  requires several steps:

  1. Generate wind field point estimates from a single track

  #. Generate a wind field regression model from the point estimates

  #. Generate an set of wind field regressions models from a set of tracks

  #. Extract patterns from the set of wind field regression models

  #. Encode the patterns in a predictive Bayesian model (forecasting model)

  #. Generate wind field point estimates using an in-flight device

  #. Use the point estimates to generate a state of belief about the current
       wind patterns


* Perhaps I should start by surveying the different components of the
  composite wind field (eg, the mean field, global shear, local shear,
  updrafts, etc). Each component (horizontal and vertical features) may have
  their own literature on estimation methods. This is also important for
  honestly representing the difficulties in trying to estimate the wind field.

* I must define the relevant terms: topography, convective boundary layer

* Am I planning on demonstrating a Gaussian process regression model for a 3D
  wind field? Cokriging / multiple-output Gaussian processes are NOT trivial.
  You might get decent results by treating each output dimension as
  independent, but that doesn't seem likely.


Point estimates
---------------

* Should my paper should do a recap of wind vector estimation methods; for
  example, the circle method for estimating the horizontal components of wind,
  or thermal estimation algorithms (like that particle filter in
  `notter2018EstimationMultipleThermal`). I should review existing methods,
  and establish why they are not sufficient for my purposes. (For example, the
  circle method is unable to track thermals effectively, has poor spatial
  resolution, etc.) Most importantly, I should **always start by showing why
  the simple or "obvious" approaches to each task are insufficient.**

  I have notes on the circling method in `~/wind/inbox/NOTES.md`, maybe
  I should organize them into a mini-section for the thesis. I already have
  code for the circle fitting, I could even have a few screenshots to show it
  off.

* Limitations of the *circle method*:

  * Target needs to be circling

  * Assumes constant airspeedx

  * The naive implementation is really sensitive to noise, so it needs to
    average over a significant period of time. The more samples you average
    over the worse the precision (averaging discards information)

* I'm assuming the particle filter must rely on position only data from the
  IGC file, but couldn't it incorporate "external" information? There are many
  rich resources: mean weather values for the region, radiosonde data,
  topographic information, weather models (eg, RASP), etc.

* Sequential Monte Carlo methods typically use the Markov assumption for the
  sequence of states, but is it possible to fit a regression model "on-line"
  as the point estimates appear (as the particle filter moves forward), then
  use that regression model for future wind proposals? (So future proposals
  depend not only on the previous wind state, but also on the regression model
  prediction for that point in space.) In a sense, if you consider the wind
  field "current state" as capturing all previous wind field information,
  I can see an argument for it satisfying the Markov assumption. Not sure how
  you'd use it with a particle smoother though.

* I have a complaint that the hotpots from "Paraglider Thermal Maps" largely
  boil down to "fly along the ridge", but in hindsight that shouldn't be
  surprising since **that algorithm explicitly fits the trigger points to
  ridges**.


Wind field regression
---------------------

* I'm trying to estimate the wind field from instantaneous estimates of points
  in the wind field (the wind vectors). Those observations are subject to
  measurement noise, model error (eg, the rigid body assumption), even
  fluctuations in the wind field.

* Do you use a grid? (I think this is equivalent to asking if you're using
  a discrete or continuous regression model?) If you use a discrete grid, is
  it a regular or irregular?

* Do you use topographic features as extra inputs?

* Is the regression model data-driven only, or does it incorporate physical
  models of different wind features? (eg, does the regression model try to
  detect wind features, such as thermals, shear lines, etc, and use physical
  models as priors over that region?) Some papers that try to detect and
  localize thermals then assign a physical model to each possible thermal and
  estimate their parameters (see `notter2018EstimationMultipleThermal`).


Kriging with non-Gaussian measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

How does a kriging model deal with measurement uncertainty? More specifically,
how can a kriging model (a multivariate Gaussian) incorporate measurements
corrupted by non-Gaussian noise?

This is important to how I use the empirical distribution over flight
trajectories (ie, particles) to build a regression model (kriging) over the
wind vectors.

For simplicity's sake, suppose the wind field at some point is bimodal; you
have two significantly different possible values. Averaging a bimodal
distribution gives an estimate that doesn't make *either* of the modes.


Pattern Extraction
------------------

Key Points:

* Each flight is a sample of some subset of a larger wind field that occurred
  at some point in time and space. Perform a spatial or spatiotemporal
  regression (kriging) over the noisy wind vector estimates from the flight to
  build an estimate of the underlying wind field.

* Each regression model is an observation of a particular configuration of the
  wind field. The goal is to find patterns in the wind field configurations.
  Use the set of wind field observations to reveal strongly correlated regions
  of the wind field that can be used to predict each other.

* A predictive model answers queries by seeing if any of the observed regions
  are correlated with other locations of the wind field. Finding correlated
  regions requires that sections of the wind field follow repeatable wind
  configurations. (eg, "lift over here usually means sink over there", or "a
  west wind over here means ridge lift over there")

* Finding correlations between regions requires a large number of pairwise
  observations of the correlated regions. (ie, you need flights that observe
  both regions at the same time)

* The wind field changes over time, so flights need to be aggregated by time
  (open problem; group they by hour?).

  How do you handle the spatiotemporal averaging? In terms of time, do you
  group observations by a sliding 1-hour window, etc? In terms of space, do
  you use a continuous regression model or do you use a grid?

* Computing the regression field for a track generates a lot of data, but you
  can compress the result by discarding information about regions that didn't
  exceed some "confidence threshold". If you're not confident, don't waste
  compute time on that region when you're generating the patterns. **Knowledge
  of structure leads to compression opportunities.**


Predictive Model Encoding
=========================

* To be useable using an in-flight device with no access to cellular network,
  the model must be self-contained, and it must meet the storage and
  computation constraints of a low-power embedded device. How the model is
  encoded is fundamental to how it is queried. [[Is it though? On-disk
  encoding isn't necessarily the same as the in-memory representation; granted
  though, the advantage of what I was doing was to make the on-disk model be
  compact and directly queriable without loading it into memory.]]


Flight Data
===========

This section of the paper will discuss the data I want to use (IGC tracks),
its limitations, and how I plan to mitigate those limitations.

I've been wrestling with how to break down this information, and I suspect my
answer lies in Bayesian modeling, as usual: the key is to **separate the raw
data from the random variables**. There are variables that I'm trying to
observe; they are noisy, but are *observable* with respect to some
relationship with the data. So, break up "here's the raw data I have to work
with", and "here are the random variables I can estimate from that noisy
data".

I'd like to get some (small) amount of credit for the work I did on parsing
and cleaning the IGC code. I need to think about *how I present this work*.
I was thinking about putting it in an appendix, but the more I think about it,
the more I think it should go up front.

Start the paper by showing what data is available in an normal IGC track.
Time, latitude, longitude, pressure altitude, and GNSS altitude. Discuss the
limitations of that data (no sensor characteristics, etc), and summarize what
you can reasonably output.

**Establishing the information available from a normal IGC track sets up the
rest of the work!** Highlighting the data shows what you have to work with for
the purposes of recreating the wind field for a given track. (Remember,
building a regression model over a single wind field is different from
extracting patterns from a *set* of wind fields.)

Extra notes:

* IGC tracks intended for official scoring (so called "IGC FR" tracks, versus
  "non-IGC FR" tracks, to use the official IGC spec nomenclature) are required 


Timestamps
----------

* These allow me to define *sequences* of data. Any data that has sequential
  structure with respect to time will gain additional information since the
  **measurements are correlated**.

* Timestamps in IGC tracks are untrustworthy. Describe the cleaning process.

* Timestamps in IGC tracks have variable time resolution.


Altitude
--------

IGC tracks include two measurements of altitude: one from a GNSS device, and
one from a variometer. The GNSS device measures signals from multiple
satellites to determine the current *geodetic altitude*: the distance above
the WGS84 reference ellipsoid. The variometer measures air pressure to
determine the current *pressure altitude*: the distance above the WGS84
reference ellipsoid that would produce the measured atmospheric pressure under
international standard atmosphere (ISA) conditions.
:cite:`2016IGCFlightRecorder`

[[Geopotential altitude is directly useable in conservation of energy
calculations, while pressure altitude is more convenient for pilots that need
to assess the expected aerodynamic performance of their aircraft.]]

Both types of measurement have advantages and disadvantages. GNSS estimates
are more prone to "spurious" fixes: relatively large, random displacements
from the true position. GNSS altitudes are less susceptible to systematic
bias, but processing delays mean they often lag behind the true position of
the aircraft; this lag makes GNSS signals less reliable for capturing rapid
altitude fluctuations. [[**Does GPS lag apply to horizontal the same as to the
vertical? What causes GPS lag?**]] The pressure sensor in a variometer is more
capable of capturing rapid altitude fluctuations, but the assumptions it makes
when converting the atmospheric pressure to pressure altitude mean it contains
a systematic, altitude-dependent bias.

A flight reconstruction filter will need accurate estimates of both the
geopotential altitude and the air density, but the IGC data only includes the
lagged geopotential altitude measurements and no direct observations of the
air density. This means that the GNSS and pressure altitudes must be combined
to not only improve the geopotential altitude measurements, but also to
estimate the air density. Those requirements pose two strongly coupled
problems.

1. Estimating the true atmospheric conditions

2. Computing the true geopotential altitude from the pressure sensor data
   using the correct, non-ISA atmospheric conditions

Estimating the true atmospheric conditions lets you compute the air density,
and use the sensitive pressure measurements to produce better geopotential
altitude measurements. [[The pressure measurements do not suffer from the time
lag and smoothing that plagues the GNSS measurements.]]


Main Body
^^^^^^^^^

[[**This section is mostly old crap**]]

A variometer is a device which measures "pressure altitude", and reports the
vertical change in pressure altitude. Although this is effective as a local
measure of altitude, absolute pressure altitude has two problems related to
biasing:

1. A fixed-offset bias

2. A dynamic-offset bias

The fixed-offset is a stationary bias between the true altitude and the
measured pressure altitude. This error occurs because the pressure at a given
altitude will vary with the current weather conditions. To correct this error,
a reference altitude must be used to calibrate the variometer. Because this
calibration requires a known altitude, which is often unknown at paragliding
launch sites, many paragliding tracks are not calibrated at all. Thus, there
is a constant bias across the entire track.

In addition, there is a dynamic bias that varies with altitude. This error
occurs due to the assumptions required to convert pressure and temperature
into an estimate of altitude. **The variometer is able to measure temperature
and pressure, but not the lapse rate; that is, it does not know the true
change in altitude for a given change in temperature. Thus, the variometer
must rely on an average: the International Standard Atmosphere (ISA) is
defined around the average pressure at sea level (1013.25hPa), the average
temperature (15C), and the average lapse rate (2C/1000ft). Because the vario
assumes the lapse rate, its altitude estimate will only match the geometric
altitude when the average temperature of the air column is equal to the
average temperature predicted by the ISA.**

An approximate correction to the fixed-offset bias can be implemented by
computing the average altitude across the entire track, for both the GPS and
pressure altitudes, then subtracting that error from the pressure altitude
series. For example, if the average GPS altitude is 553m, and the average
variometer altitude is 545m, then the error is 545m - 553m = -8m. However,
this naive average error will include both the fixed and dynamic errors. Thus,
as the altitude range of the flight increases, then this "average" error will
be biased towards whatever altitude was most common in the flight.

Another naive method would calculate the error at each timestamp, sort the
errors by altitude, then perform a linear regression over "Error vs Altitude".
The issue with this method is that the GPS altitude is subject to variable,
and potentially large, time delays. Thus, the GPS altitude at one timestep may
be a lagged version of the pressure altitude at a previous timestep. Because
this lag is variable, a constant time lag cannot correct the time discrepancy.

To correctly debias the pressure altitude measurements requires dealing with
both the dynamic altitude bias and the dynamic time lag. Thus, the solution
becomes a sequence alignment issue.

One approach to sequence alignment of two time series is dynamic time warping.


Talking points
^^^^^^^^^^^^^^

* What data is available (GNSS altitude and pressure altitude)

* Pros/cons:

  * GNSS altitude lags the variometer, and often introduces a smoothing effect

  * Pressure altitude assumes standard ISA conditions, which introduces
    a systematic, altitude-dependent bias

* Atmospheric characteristics

  * **Lapse rate**: the rate at which the air temperature decreases as
    a function of altitude. A negative lapse rate means the temperature
    increases. A sign inversion in the lapse rate corresponds to a thermal
    inversion; for example, the temperature starts to increase with altitude
    instead of decreasing.

* Atmospheric measurements

  * **Radiosonde** is a telemetry instrument carried into the atmosphere on
    a weather balloon.

* Recovering pressure from pressure altitude

* Sequence alignment of GNSS and pressure altitude with dynamic time warping
  (this gives you the correct {pressure, altitude} pairs, else you'd be using
  the lagged altitudes)

* Estimating atmospheric conditions using a least-squares fit of atmospheric
  pressure and GNSS altitude (uses the atmospheric equations)


Questions
^^^^^^^^^

* What about humidity? See `guinn2016QuantifyingEffectsHumidity`.

* Using a reference temperature (eg, at an airport) should include the
  {altitude, temperature} point on the fit line. Not available in general, but
  would be helpful if I could at least find a few flights that I could use for
  validation (my estimate versus IGRA data, airport data, etc)

  Oh, alternatively, if you *knew* the altitude at takeoff, and the variometer
  gave the pressure, then you can (assuming the humidity) determine the
  temperature! That might be easier than looking for a nearby reference
  temperature.

* What about inversion layers? Should I attempt change point detection?

  I will probably only observe a small layer of atmosphere; if the lapse rate
  is not constant from MSL to the lowest observed atmosphere, then it's likely
  a least-squares fit of the MSL temperature and pressure will be
  unrealistically high/low.
  
  The fact that the MSL parameters are unrealistic isn't a problem if I know
  not to extrapolate outside the observed range, but it does reveal a flaw:
  what if there are inversion layers *inside* the observed range?


GPS Data
--------

The position data in IGC tracks comes from global navigation satellite systems
(GNSS), such as GPS, Galileo, GLONASS, QZSS, and Beidou.

The systems work based on *pseudo-ranges*: the distance traveled at the speed
of light for the amount of time delay **as measured by the local clock**. The
relative delay relies on the local oscillator, which may be imprecise.
[[FIXME: verify this paragraph]]

Positions are determined by *trilateration* (or *multilateration*): using the
speed of light and time of flight calculations from a set of satellites, the
users position lies at the intersection of the measured ranges.


Misc
^^^^

* In "Global positioning systems, inertial navigation, and integration"
  (Grewal; 2007), he discusses "time-correlated noise" in Kalman filters. See
  page 279

* In "Global positioning systems, inertial navigation, and integration"
  (Grewal; 2007), he discusses "rejecting anomalous sensor data" in Sec:8.9.4,
  page 309. He uses a chi-squared test to reject outliers. As I recall, I was
  hoping to use this information, but how?

* What kind of chi-squared test is being suggested by Bar-Shalom for checking
  the GPS noise covariance?


Technical Details
^^^^^^^^^^^^^^^^^

* What are *ephemeris*?

* What are *real-time kinematics*?

* "GPS time does not follow UTC leap seconds. So GPS time is ahead of UTC by
  an integral number of seconds." (Wikipedia:GPS Signals)


Accuracy and Precision
^^^^^^^^^^^^^^^^^^^^^^

References:

* `https://wiki.openstreetmap.org/wiki/Accuracy_of_GPS_data`

* `Global Navigation Satellite Systems and their applications`; Madry, 2015

Notes

* Possibly want to define the common accuracy measures (root mean square, "2
  drms" is "twice the distance root mean square error", circular error
  probable (CEP), spherical error probable (SEP), etc)

  See: https://www.gpsworld.com/gps-accuracy-lies-damn-lies-and-statistics/

* What is *dilution of precision*? Discuss the different types and their
  effects. In particular, differentiate vertical and horizontal DoP.

* "GPS provides two levels of service: Standard Positioning Service (SPS) and
  Precise Positioning Service (PPS)."

  See:
  https://www.faa.gov/about/office_org/headquarters_offices/ato/service_units/techops/navservices/gnss/faq/gps/

  According to the "SPS performance standard", "with current (2007)
  Signal-in-Space (SIS) accuracy, well designed GPS receivers have been
  achieving horizontal accuracy of 3 meters or better and vertical accuracy of
  5 meters or better 95% of the time."

  See: https://www.gps.gov/technical/ps/2008-SPS-performance-standard.pdf

* "[The] government commits to broadcasting the GPS signal in space with
  a global average *user range error* (URE) of ≤7.8 m (25.6 ft.), with 95%
  probability. Actual performance exceeds the specification. On May 11, 2016,
  the global average URE was ≤0.715 m (2.3 ft.), 95% of the time.

  *User range error* is a measure of ranging accuracy (distance from the user
  to a satellite), *user accuracy* refers to how close the device's calculated
  position is from the true, expressed as a radius."

  "GPS-enabled smartphones are typically accurate to within a 4.9m radius
  under open sky."

  See: https://www.gps.gov/systems/gps/performance/accuracy/


* "Position accuracy, 95%

  * <= 9m horizontal, global average

  * <= 15m vertical, global average

  * <= 17m horizontal, worst site

  * <= 37m vertical, worst site

  See: https://www.gps.gov/systems/gps/performance/


* "GPS devices typically need to receive signals from **at least 7 or
  8 satellites** to calculate location to within about 10 meters."

  See:
  https://support.strava.com/hc/en-us/articles/216917917-Why-is-GPS-data-sometimes-inaccurate-

* Some devices can combine multiple satellite systems (eg, GPS and GLONASS) to
  improve accuracy.

What factors affect GNSS accuracy?

* GNSS factors:

  * *Selective availability*: prior to 2000-05-01, clock degradation
    (process-δ) and ephemeris manipulation (process-ε) reduced accuracy from
    ~10m to ~100m. The process-δ acts directly over satellite clock
    fundamental frequency, which has a direct impact on pseudoranges to be
    calculated by user's receivers. The process-ε consists in truncating
    information related to the orbits.
    (`https://gssc.esa.int/navipedia/index.php/GPS_Services`)

    When SA was disabled, normal GPS receivers automatically benefited. They
    did not require modifications; the signals degradations were simply turned
    off.

    According to `https://www.gps.gov/systems/gps/modernization/sa/faq/`, "in
    theory, civil receivers [SPS] should now match the accuracy of PPS
    receivers under normal circumstances. [...] PPS still gives advantages to
    the military beyond accuracy."

* Receiver design factors:

  * Hardware: antenna, augmentation schemes (differential GPS (most commonly
    used for maritime, but is being discontinued), wide area augmentation
    system (for aviation), etc)

  * Algorithmic: forward error correction, processing latency, battery life
    versus accuracy trade-offs, etc

  * Other: real-time kinematic (RTK) positioning

* Situational factors:

  * Ionospheric conditions (ionized particles; "the state of the ionosphere is
    the single major source of error in our GPS error budget" [Madry, p43])

  * Tropospheric conditions (water vapor and other particulates attentuate and
    **delay** the signals (different frequencies are delayed by different
    amounts); relatively minor source of error?)

  * Satellite geometry (how many are visible by the user, and how are they
    positioned relative to the user)

  * Reflected signals: reflections show up as time delayed signals, which
    break the time of flight calculations, and *multipath propagation* produce
    multiple, likely desynchronized, copies of a signal (examples: between
    tall buildings, canyon walls, etc)

  * Attenuated signals: signals are partially or totally blocked by absorption
    or reflection (examples: inside an aircraft, backpack, etc)

* How does GNSS accuracy degrade? What do the errors look like? (discuss
  non-Gaussian noise, "dilution of precision", etc)


Historical GPS accuracy
^^^^^^^^^^^^^^^^^^^^^^^

* What can I say in terms of average performance? I need to choose an assumed
  baseline (worst-case) performance in order to interpret the data.

* How did typical GPS accuracy change over time?

* Are newer devices more or less accurate (eg, they might be trading off
  accuracy for better battery life; see
  `https://fellrnr.com/wiki/GPS_Accuracy`)


Differential GPS
^^^^^^^^^^^^^^^^

* What is it?

* When was it introduced?

* How common is it in commodity GPS receivers?

* The US Coast Guard ran the NDGPS network, but they're shutting that down as
  of 2018 since the average GPS performance satisfies maritime performance
  requirements, and since alternative GPS augmentation schemes are available
  (eg, for agriculture, aviation, etc).


Selective Availability
^^^^^^^^^^^^^^^^^^^^^^

* What is it?

* Disabled on 2000-05-03. With SA the two-sigma error was 45m, without SA the
  two-sigma error was 6.3m.

* Do receivers automatically benefit from disabled SA, or did they require
  special support?

See: `https://www.gps.gov/systems/gps/modernization/sa/data/`


Latency (from fix to readout)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Is the signal lag the same for horizontal and vertical data?

* What is the GPS satellite transmit frequency?

* Read `http://catb.org/gpsd/performance.html`. Search for "list of stages",
  which discusses the processing pipeline of that application; good conceptual
  starting point for this question.

  For a reasonably representative "worst case scenario", suppose a UART at
  `9600baud, 8+1 coding`. That's `9600/9 ~= 1067` bytes/second. The standard
  NMEA fix sequence is 65 bytes, so ~6.1ms to transmit a basic fix.


Receiver Synchronization
^^^^^^^^^^^^^^^^^^^^^^^^

High-end GPS receivers can include *disciplined oscillators* (DO). It would
see it adjusts the temperature around an oscillating crystal to tune the
frequency. Tuning is performed by comparing clock output against the GPS
signals. The DO is used to generate an **extremely** accurate and precise 1 HZ
output (aka, a "1 pulse per second" line, or 1PPS) for synchronization
purposes. Errors are typically measured in nanoseconds.

* See
  `https://electronics.stackexchange.com/questions/30750/why-do-gps-receivers-have-a-1-pps-output`
