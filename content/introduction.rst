************
Introduction
************

Introduction goes here.


Okay, I'm struggling to get the ball rolling here, so just braindump: what is
this thesis about? What are the pieces?


.. todo::

    Create a solid outline. Does it warrant parts+chapters, or just
    chapters?


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
