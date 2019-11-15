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
