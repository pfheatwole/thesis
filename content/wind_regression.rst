*********************
Wind Field Regression
*********************

[[This is a placeholder section that I'll probably remove, depending on how
much content I'm able to create. It's possible I'll demo a crude Gaussian
process fit over the three wind vector components (treating each component as
independent, since multiple-output GPs are difficult), but we'll see.]]


I am not using physical models of wind field features in the wind field
estimation process. (Other papers specifically try to model thermal updrafts,
etc.) I'm essentially trying to recover point measurements of a wind field;
you could theoretically use those pseudo-observations as part of a more
sophisticated modelling method that does make assumptions about the kinds of
wind features being experienced. 

For example, a Gaussian process can place general expectations about peak
magnitudes, rate of changes, relationships to the topography, etc, but it does
not say "I may have identified a chimney thermal at this location, so I will
perform a Bayesian estimate over this possible model".
