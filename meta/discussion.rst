************
Introduction
************


Filtering
=========

* Several great quotes from the introduction to "Particle filters and data
  assimilation" (Fearnhead and Kunsch; 2018):

  "State space models can be used to incorporate subject knowledge on the
  underlying dynamics of a time series by the introduction of a latent Markov
  state-process." (This is the essence of what I'm doing, except a that I'm not
  using the latent values to improve my estimate of the position: I'm
  interested in the latent state itself.)

  "A state-space model specifies the joint distribution of all the variables
  that are required for a dynamic model based on subject knowledge, and the
  variables that have been observed."


Relevant weather characteristics
================================

Good general atmospheric references:

* Atmospheric Thermodynamics (North, Erukhimova; 2009)

* Atmospheric Science (Wallace, Hobbs; 2006)


Some useful definitions:

* "The *geoid* is the shape the ocean surface would take under the influence
  of gravity **and the rotation of the Earth** alone, if other influences such
  as winds and tides were absent." This is not a sphere, or even an oblate
  ellipsoid; it is an irregular surface, since the Earth does not have uniform
  density; the surface of the goid is higher than the reference ellipsoid
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


***********
Flight Data
***********

This section of the paper will discuss the data I will use (IGC tracks), its
limitations, and how I plan to mitigate those limitations.


I've been wrestling with how to break down this information, and I suspect my
answer lies in Bayesian modelling, as usual: the key is to **separate the raw
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
==========

<TODO>

Some important aspects:

* These allow me to define *sequences* of data. Any data that has sequential
  structure with respect to time will gain additional information since the
  **measurements are correlated**.

* Timestamps in IGC tracks are untrustworthy. Describe the cleaning process.

* Timestamps in IGC tracks have variable time resolution.


Altitude
========

IGC tracks include two measurements of altitude: one from a GNSS device, and
one from a variometer.

Although both devices report an altitude, the two variables are not
equivalent. The GNSS uses signals from multiple satellites to measure the
*geopotential altitude*: the vertical distance above the mean sea level. The
variometer uses an atmospheric pressure sensor, which it converts to the
*pressure altitude*: the geopotential altitude that would produce the given
pressure measurement under standard atmospheric conditions.


[[Geopotential altitude is directly useable in conservation of energy
calculations, while pressure altitude is more convenient for pilots that need
to assess the expected aerodynamic performance of their aircraft.]]


Both types of measurement have advantages and disadvantages. GNSS altitudes
are less susceptible to systematic bias, but processing delays mean they often
lag behind the true position of the aircraft; this lag makes GNSS signals less
reliable for capturing rapid altitude fluctuations. [[**Does GPS lag apply to
horizontal the same as to the vertical? What causes GPS lag?**]] The pressure
sensor in a variometer is more capable of capturing rapid altitude
fluctuations, but the assumptions it makes when converting the atmospheric
pressure to pressure altitude mean it contains a systematic,
altitude-dependent bias.

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
---------

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
--------------

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
---------

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
========

The position data in IGC tracks comes from global navigation satellite systems
(GNSS), such as GPS, Galileo, GLONASS, QZSS, and Beidou.

The systems work based on *pseudo-ranges*: the distance traveled at the speed
of light for the amount of time delay **as measured by the local clock**. The
relative delay relies on the local oscillator, which may be imprecise.
[[FIXME: verify this paragraph]]

Positions are determined by trilateration [[or multilateration]]: using the
speed of light and time of flight calculations from a set of satellites, the
users position lies at the intersection of the measured ranges.



Open Questions
--------------

* What are *ephemeris*?

* What are "real-time kinematics"?


Random Notes
------------

* Possibly want to define the common accuracy measures (root mean square, "2
  drms" is "twice the distance root mean square error", circular error
  probable (CEP), spherical error probable (SEP), etc)

  ref: https://www.gpsworld.com/gps-accuracy-lies-damn-lies-and-statistics/

* Discuss *dilution of precision*, its types, and their effects. In
  particular, differentiate vertical and horizontal DoP.

* "GPS time does not follow UTC leap seconds. So GPS time is ahead of UTC by
  an integral number of seconds." (Wikipedia:GPS Signals)



Accuracy and Precision
----------------------

References:

* `https://wiki.openstreetmap.org/wiki/Accuracy_of_GPS_data`

* `Global Navigation Satellite Systems and their applications`; Madry, 2015


Notes

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

  ref: https://support.strava.com/hc/en-us/articles/216917917-Why-is-GPS-data-sometimes-inaccurate-


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


How does GNSS accuracy degrade? What do the errors look like?

* TODO: non-Gaussian noise

* TODO: dilution of precision


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

Disabled on 2000-05-03. With SA the two-sigma error was 45m, without SA
the two-sigma error was 6.3m.

Do receivers automatically benefit from disabled SA, or did they require
special support?

ref: `https://www.gps.gov/systems/gps/modernization/sa/data/`


Fix Latency
-----------

* Is the signal lag the same for horizontal and vertical data?

* What is the GPS satellite transmit frequency?


Sources
^^^^^^^

Read `http://catb.org/gpsd/performance.html`. Search for "list of stages",
which discusses the processing pipeline of that application; good conceptual
starting point for this question.


For a reasonably representative "worst case scenario", suppose a UART at
`9600baud, 8+1 coding`. That's `9600/9 ~= 1067` bytes/second. The standard
NMEA fix sequence is 65 bytes, so ~6.1ms to transmit a basic fix.


Receiver Synchronization
------------------------

High-end GPS receivers can include *disciplined oscillators* (DO). It would
see it adjusts the temperature around an oscillating crystal to tune the
frequency. Tuning is performed by comparing clock output against the GPS
signals. The DO is used to generate an **extremely** accurate and precise 1 HZ
output (aka, a "1 pulse per second" line, or 1PPS) for synchronization
purposes. Errors are typically measured in nanoseconds.

* See
  `https://electronics.stackexchange.com/questions/30750/why-do-gps-receivers-have-a-1-pps-output`


****************
Paraglider Model
****************

Discussion
==========

* Should I discuss my commitment to stateless models?



Limitations
-----------

Conservation of angular momentum
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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


Steady-state assumption
^^^^^^^^^^^^^^^^^^^^^^^

In the conclusion of "Specialized System Identification for Parafoil and
Payload Systems" (Ward, Costello; 2012), they not that "the simulation is
created entirely from steady-state data". Is this similar to assumptions I'm
making? For example, Phillips is probably not accurate during turns.


Force estimation
^^^^^^^^^^^^^^^^

* I will need to discuss the limitations of the lifting-line methods. For
  starters, you need to have previously computed the coefficients for the
  deformed section profile, including when braking, and for the range of
  Reynolds numbers.



Figures
=======


Geometry
--------

* Geometric definitions

  Should supplement the geometric definitions with plots that are annotated to
  highlight the parameters, where possible (lengths and angles, mostly)

* Examples of each type of design parameter:

  * Elliptical planforms: flat span, length of the central chord, taper
    (length ratio of central chord versus wing tip chord), ``sweepMed``
    (maximum rate of change of sweep angle?), ``sweepMax`` (angle from central
    leading edge to the wing tip leading edge?), torsion (*does this really
    belong to the elliptical planform? or to the general case parafoil
    planform?*)

  * Elliptical lobes: ``dihedralMed`` (maximum of change of curvature?),
    ``dihedralMax`` (angle from the central chord to the wing tip chord?)


The planform and lobe diagrams are 2D. Just make some tables (possibly in the
same SVG, instead of using RST tables?) with different combinations. **Make
sure to have the parameters clearly labeled in the diagrams. Don't be like
Benedetti.**

I'm not sure how to best show the 3D versions of the completed parafoil.
Graphing 3D in still images is kind of awkward. Probably best to keep them
simple (no grids, minimal axes labels), this is for basic **qualitative**
understanding, not for quantitative purposes.


Moment of inertia
-----------------

* Are any figures essential for describing this concept? Can I just quietly
  skip my nasty derivation?


Force estimation
----------------

* Should I try to define the geometry for Phillips' method, or should I simply
  reference his paper? It would be *nice* if I could make a diagram that
  describes my implementation, but that seems like a LOT of work.


*********************
Flight Reconstruction
*********************

The flight simulation section discussed how to use the paraglider model with
known inputs (controls and wind) to generate state trajectories. Part of that
discussion was to define the state variables. The flight reconstruction
concept could start by defining *inverse problems* and *underdetermined
systems*, which leads into probabilistic methods (*simulation-based
filtering*). The purpose of flight reconstruction (in this context) is to determine the
unknowns (here, those are the model parameters, the control inputs, and the
wind vectors).

Key points:

* Bayesian filtering combines the observed data with prior knowledge of the
  system to generate a joint distribution over all the variables. Bayesian
  methods require a prior (over the state values and model parameters),
  a likelihood (for the observed data), and model dynamics (for the state
  transitions).

* Monte Carlo methods generate the joint distribution by exploring the
  possible space of plausible values. The exploration of different values uses
  *proposals*. The proposals must incorporate existing knowledge of the
  variables, including its constraints. For example, the model parameter
  proposals should reflect realistic wing configurations. The wind dynamics
  should not exceed realistic turbulence power distributions. Control inputs
  should be relatively low frequency (eg, it's unlikely for the speedbar to go
  from zero to maximum in a quarter of a second).



Filtering
=========

Forward versus Inverse Problems
-------------------------------

"Inverse problems include both parameter estimation and function estimation.
[...] A common characteristic is that we attempt to infer causes from measured
effects. A forward, or direct problem has known causes that produce effects or
results defined by the mathematical model.  Because the measured data is often
noisy or indistinct, the solution to the inverse problem may be difficult to
obtain accurately."

**Can I say that my application of particle filtering is to use a forward
problem (the flight simulator) to produce a solution to the inverse problem?**

Inverse problems are about inferring causes from the observed effects; seems
like a good description of what I'm doing (only I have a tiny sample of
observed effects; namely, a change in position over time).


Probabilistic inference / simulation-based filtering
----------------------------------------------------

I liked this sentence in Duvenaud's dissertation: "*Probabilistic inference*
takes a group of hypotheses (a *model*) and weights those hypotheses based on
how well their predictions match the data." **I often use the term
"simulation-based filtering", but maybe I should review that term.**

"**data** driven forecasting" vs "**model** driven forecasting"

See `reich2015ProbabilisticForecastingBayesian`

* Model driven: eg, by analyzing topography (for example, RASP)

* Data driven: eg, by analyzing flight tracks (like von Kaenel's thesis)

Basically, do you look at the observations alone (with no though to the
underlying model), or do you also refer to the "surrogate process" from which
they were generated?

He describes "data-driven" as "bottom-up", or *empirical* models, whereas
"model-driven" are "top-down" or *mechanistic* models. Empirical models rely
on the data, mechanistic models rely on the model dynamics.

On page 182: "model-based forecast uncertainties taking the role of prior
distributions"



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

I read somewhere that a guy complained about testing your model by fitting it
against simulated data (or something; he didn't like the idea that "yay, we
recreated data we expected!" was not helpful). Gelman, on the other hand, is
a huge fan of *fake-data simulation*, where you generate data from a model
using "true" parameters, then observing the behavior of the statistical
procedures (how well they work, how they fail). There is a related procedure
called *predictive simulation*, where you fit a model, generate data from it,
then compare that generated data to the actual data (I believe this is also
called *posterior predictive checking*). See
:cite:`gelman2007DataAnalysisUsing`.


The *curse of dimensionality* refers to needing **more** data as the dimension
increases, so you have to pursue the *blessing of abstraction*: the more
structure you account for, the **less** data you need. (FIXME: I don't think
this is the correct use of the phrase *blessing of abstraction*, which refers
to the observation that sometimes its easier to a learn general knowledge
faster than specific knowledge?)

   ^^ This is a concept I need to highlight in my thesis, since it motivates
   my detail efforts. The more information I want to squeeze out of the data,
   the more structure I need to introduce. You don't get something for
   nothing: for every question you want to answer, you need either need more
   data or more structural information (like paraglider wing dynamics)


Jittering
---------

If the process noise is small, you don't get much variation in the particles
during the time update. One way to decrease the odds of sample impoverishment
is to use *jittering*. See `fearnhead1998SequentialMonteCarlo`, page 53


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


Modelling
=========


Pilot Control Inputs
--------------------

Should I model the pilot controls as *multivariate autoregressive Gaussian
processes*? (See `turner2011GaussianProcessesState`, section 3.6)


I'm unhappy with treating the four pilot controls as independent random walks
(for the purpose of my filtering method), since that will generate mostly
nonsense control sequences. There are several considerations for generating
realistic pilot control sequences:

* Controls don't change erratically (they are generally smooth)

* Controls tend to change together (you don't want full left brake and right
  weight shift, or full symmetric braking together with full speedbar)

* Controls tend to be the result of a pilot attempting some maneuver (so you
  can consider the controls a latent process of the unobserved "maneuver")


For controlling smoothness, maybe an *integrated Ornstein-Uhlenbeck process*
(which I think is like integrating a random walk over acceleration?), or
a Gaussian process with an appropriately smooth kernel.

For correlated controls (ie, how they vary together), I may want to think of
the pilot controls as points on some "data generating manifold". This idea
shows up in animation, using low-dimensional manifolds for generating
high-dimensional human skeletal animations; see Wang's thesis
`wang2005GaussianProcessDynamical`. The manifold is a kind of constraint on
how the variables change together.

For maneuvering, I have done no research, but this is important for realistic
maneuvers. Without encoding a notion of maneuvers, you'll get very poor
performance during constant input sequences, like during a 360. (Random walks
and their ilk will be very unlikely to produce fixed brake positions, which
are essential to smooth flights.)


Notes to self in case Foxit crashes:

* I'm currently reading "Pattern Recognition and Machine Learning", chapter 12
  (continuous latent variables). I might then follow up with chapter 6 on
  "kernel methods".

* In Bishop, Chapter 6, page 296 (314), he has "Techniques for constructing
  new kernels"


Using Gaussian processes
^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^

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


******************************
Wind Estimation and Prediction
******************************

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


Wind field regression
---------------------

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



Wind field prediction
---------------------

Model Encoding
^^^^^^^^^^^^^^

* To be useable using an in-flight device with no access to cellular network,
  the model must be self-contained, and it must meet the storage and
  computation constraints of a low-power embedded device. How the model is
  encoded is fundamental to how it is queried. [[Is it though? On-disk
  encoding isn't necessarily the same as the in-memory representation; granted
  though, the advantage of what I was doing was to make the on-disk model be
  compact and directly queriable without loading it into memory.]]
