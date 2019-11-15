*******************
Wind Field Patterns
*******************

Key Points:

* Each flight is a sample of a larger wind field that occurred at some point
  in time and space. Perform a spatial or spatiotemporal regression (kriging)
  over the noisy wind vector estimates from the flight to build an estimate of
  the underlying wind field.

* Each regression model is an observation of a particular configuration of the
  wind field. The goal is to find patterns in the wind field configurations.
  Use the set of wind field observations to reveal strongly correlated regions
  of the wind field that can be used to predict each other.

* The output of this stage is a set of spatial correlations (patterns).


Given a set of flights, look for patterns that would be useful to pilots. I'm
hoping that neighboring regions will be correlated, meaning they can be used
to predict each other.

Each flight is an observation of a subset of the true wind field. [[They can
be aggregated?]] Pattern detection requires that sections of the wind field
follow repeatable wind configurations.

Finding correlations between regions requires a large number of pairwise
observations.

The wind field changes over time, so flights need to be aggregated by time
(open problem; group they by hour?).
