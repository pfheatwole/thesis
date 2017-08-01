************
Introduction
************


This project is about using timestamped paraglider flight tracks to recreate
the wind conditions at the time of the flight. If that is possible, then each
flight represents a stochastic snapshot of a possible wind configuration. With
enough of these observations, you can establish recurring patterns in the wind
configurations, and use those patterns to create a predictive model.

This type of pattern extraction requires a large number of observations. There
do exist databases of paragliding flight records, known as *IGC tracks*. At its
most basic level, an IGC file is a time series of latitude, longitude, and
altitude measurements. Those position measurements must be combined with
a paraglider dynamics model to simulate the possible pilot controls and wind
conditions that could have produced that sequence positions.

This process requires several steps:

1. Cleaning the raw measurement data

2. Generating the simulated flights

3. Aggregating the flights to produce a set of wind configurations

4. Analyzing the set of wind configurations for recurring patterns (that is,
   correlations in time and space).


Pieces
======

Needs text here?




Data Filtering
--------------

This is where I filter raw sensor data (GPS and vario), and timestamps

I'm planning to use:

1. Pandas for timestamp filtering

2. Kalman filters for the sensor data

The Kalman filters will require a lot of design choices. The covariance matrices in particular need a lot of careful tuning; I'm planning to approximate then optimize them using Expectation-Maximization, over a large set of tracks, then averaging the individual noise matrices to determine the "average" noise.


Simulation-based filtering
--------------------------

* Use track data to recreate flight conditions

* Specifically: what was the glider likely doing, and what was the wind
  likely doing?

* This section requires significant particle filtering design.

Data aggregation
----------------

* A single IGC has many measurements of an area. These must be reduced to
  some form of summary.
  
* How do you group the timestamped data points, how do you summarize the
  grouped data points, etc.

Predictive modelling
--------------------

* Given a set of wind summary data from the aggregated track data, look for
  repeated patterns that allow for predictive modelling.

* Specifically, can you find points in space which are strong indicators of
  the wind conditions in other points in space?


.. figure:: images/wind_triangle.*
    :alt: Wind Triangle
    :align: center

    Wind Triangle
