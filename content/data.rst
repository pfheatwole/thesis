Data Preparation
================

.. todo::

   Discuss the data I will use (IGC tracks), its limitations, and how I plan to
   mitigate those limitations.


Timestamp Issues
----------------

<TODO>


Variometer Debiasing
--------------------

Vario debiasing via dynamic time warping.

Talking points:
 * How GPS lags the variometer
   
 * How GPS lag causes a smoothing effect

 * How altitude pressure introduces a bias with changing altitude

   * **Radiosonde** is a telemetry instrument carried into the atmosphere on
     a weather balloon.

   * **Lapse rate** is the rate at which the air temperature decreases as
     a function of altitude. A negative lapse rate means the temperature
     increases. A sign inversion in the lapse rate corresponds to a thermal
     inversion; for example, the temperature starts to increase with altitude
     instead of decreasing.

 * Determine the vario bias from the two tracks

 * Issues with aligning the two sequences


Open Questions:

 * If the vario assumes the International Standard Atmosphere (ISA) lapse rate
   of ~2C/1000ft (thus accounting for that automatically), then the residual
   error is not in fact the lapse rate, but the lapse rate error. If I compute
   the lapse rate error, can I combine it with the ISA to report the
   approximated "true" lapse rate? (ie, `2C + measured_error`)


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
into an estimate of altitude. The variometer is able to measure temperature
and pressure, but not the lapse rate; that is, it does not know the true
change in altitude for a given change in temperature. Thus, the variometer
must rely on an average: the International Standard Atmosphere (ISA) is
defined around the average pressure at sea level (1013.25hPa), the average
temperature (15C), and the average lapse rate (2C/1000ft). Because the vario
assumes the lapse rate, its altitude estimate will only match the geometric
altitude when the average temperature of the air column is equal to the
average temperature predicted by the ISA.

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
The issue with this method is that the GPS altitude is subject to variable, and
potentially large, time delays. Thus, the GPS altitude at one timestep may be a
lagged version of the pressure altitude at a previous timestep. Because this
lag is variable, a constant time lag cannot correct the time discrepancy.

To correctly debias the pressure altitude measurements requires dealing with
both the dynamic altitude bias and the dynamic time lag. Thus, the solution
becomes a sequence alignment issue.

One approach to sequence alignment of two time series is dynamic time warping.


Position Filtering
------------------

Kalman filter lat/lng/alt
