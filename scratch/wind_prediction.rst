* The purpose of an *online* predictive model (ie, during a flight) is
  essentially to *calculate the conditional distribution over the wind
  field*.


Wind Estimation and Forecasting
-------------------------------

* The first part is *wind field estimation* using position-only data

  It's possible that this is actually two steps: the particle filter may treat
  each wind vector estimate as independent, or it may run a regression model
  "on-line" as the wind vector particles appear. **I'm intrigued at the idea
  of using the particle ensemble as a noisy observation with "on-line"
  kriging.**

* The second part is *wind field forecasting* (building a predictive model)

Both of these parts can be built using a different set of inputs/outputs
(weather data, topographic data, flight data, etc) and different model
components (weather model, paraglider model, etc)

My paper should do a recap of wind vector estimation methods; for example, the
circle method for estimating the horizontal components of wind, or thermal
estimation algorithms (like that particle filter in
`notter2018EstimationMultipleThermal`). I should review existing methods, and
establish why they are not sufficient for my purposes. (For example, the
circle method is unable to track thermals effectively, has poor spatial
resolution, etc.) Most importantly, I should **always start by showing why the
simple or "obvious" approaches to each task are insufficient.**

I have notes on the circling method in `~/wind/inbox/NOTES.md`, maybe I should
organize them into a mini-section for the thesis. I already have code for the
circle fitting, I could even have a few screenshots to show it off.

Perhaps I should start by surveying the different components of the composite
wind field (eg, the mean field, global shear, local shear, updrafts, etc).
Each component (horizontal and vertical features) may have their own
literature on estimation methods.

I should probably summarize some of the relevant terms (topography, convective
boundary layer, etc).


Kriging with non-Gaussian measurements
--------------------------------------

How does a kriging model deal with measurement uncertainty? More specifically,
how can a kriging model (a multivariate Gaussian) incorporate measurements
corrupted by non-Gaussian noise?

This is important to how I use the empirical distribution over flight
trajectories (ie, particles) to build a regression model (kriging) over the
wind vectors.

For simplicity's sake, suppose the wind field at some point is bimodal; you
have two significantly different possible values. Averaging a bimodal
distribution gives an estimate that doesn't make *either* of the modes.
