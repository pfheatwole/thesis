************
Introduction
************

1. Introduction to the introduction (brief version of the context, problem, and
   response)
2. Context
3. Restatement of the problem
4. Restatement of the response
5. Roadmap


Introduction to the Introduction
================================

Paragliding is a non-motorized form of flight in which a pilot uses a flexible
nylon wing to fly using wind power. Pilots rely on their ability to find
regions of rising air in order to gain altitude. They must also determine the
direction and magnitude of the wind in order to calculate suitable landing
zones.

These wind patterns are completely dictated by the local topography and weather
conditions. Although such trends can be highly  variable, general wind patterns
can be determined over the course of many flights. For example, some sections
of terrain might have a higher than average occurrence of rising air,
a situation that is highly desirable by pilots.

Historically, such regional weather patterns have been communicated from pilot
to pilot by word of mouth, but there is an another possibility. Many pilots
use flight devices that record their flights as timestamped position sequences;
these flights are uploaded to online databases for recreational purposes. It is
possible that these flight databases contain sufficient information to find
some of the general weather patterns using statistical methods.

This project is about using those timestamped paraglider flight tracks to
recreate the wind conditions that were present at the time of the flight.
By considering each flight as a stochastic snapshot of the possible wind
patterns, then given enough samples it is possible to create a database of
general trends, just as a human pilot would do.

This database of patterns can be encoded into a predictive model that can be
evaluated in-flight, by comparing current conditions to historical trends. In
this way a pilot can seek out regions that are likely to contain rising air,
and can avoid regions likely to contain sinking air.


The basic pipeline is as follows:

1. For each flight:

   A. Clean and filter the raw data

   B. Use the filtered data to estimate the wind state

   C. Sort the wind samples into a regularized grid over the topography

   D. Aggregate the wind samples in each bin to produce a set of hourly wind
      estimates

2. For each set of hourly wind estimates

   A. Compute the pairwise co-occurrences so you can determine what regions
      have enough samples to attempt pattern extraction.

   B. For regions with enough data, FIXME




Data Preparation
================

Clean and filter the raw data. Kalman filter the position data, DTW to debias
the variometer data, etc.


Wind Estimation
===============

Use simulation-based filtering to combine the filtered position data with
a paragliding dynamics model to estimate the wind forces that were interacting
with the glider.


Pattern Extraction
==================

Combine the sets of wind estimates by time and space, then use pattern
extraction to find wind correlations between nearby regions. Specifically, can
you find points in space which are strong indicators of the wind conditions in
other nearby points in space?


Predictive modelling
====================

Compile the sets of patterns into a predictive model that can be queried by
inputting the current wind estimates.

.. figure:: images/wind_triangle.*
    :alt: Wind Triangle
    :align: center

    Wind Triangle
