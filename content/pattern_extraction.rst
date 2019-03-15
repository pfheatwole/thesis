******************
Pattern Extraction
******************

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
