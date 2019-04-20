The Objective
=============

The project started with a question: can you learn to find wind patterns by
looking at old paraglider flights? The flights only record position
information, so you need a lot of modelling, but can it be done?


I started with a bunch of naive assumptions: Kalman filtering with a pure
kinematics model (since I knew nothing about paraglider dynamics), no clue how
to develop the correlations over space to detect the pa


* I only knew Kalman filtering with basic PVA models (kinematics only, linear
  model assumptions, etc)

* I knew basic Python (no numpy, pandas, etc) so getting the data was more
  work that anticipated (foolish, wasn't it?)

* My linear algebra was crap (shows up everywhere, it turns out)

* My statistics was crap: I didn't really understand bayesian reasoning, I'd
  never heard of Bayesian networks or particle filters



So what was my basic idea?

I figured I'd use a kinematics model (PVA) with the position information to
find regions were the glider was lifting and sinking. Quantize those lift and
sink velocities, and assign their values to a regular grid. Apply basic
correlation statistics to find linear correlations between regions. I had no
idea how to approach encoding the model, or evaluating the model, or
broadcasting wind velocity estimates between gliders, etc.

So Kalman filtering + correlation statistics, in other words. Once I realized
that pairwise linear correlations were junk, I looked into basic geostatistics
and discovered Gaussian processes. Those seemed useless (partly because
I didn't really understand them, and partly because my data is woefully
incomplete), I ended up deep diving into a bunch of new topics:


The pattern detection launched me into a survey of Bayesian networks.

The limitations of a kinematics-only model launched me into particle
filtering; of course, those require the dynamics, so I ended up reviewing
paraglider aerodynamics, which required me to self-teach basic aerodynamics.
Before I went too far, though, I wanted to see if you could even have a prayer
of encoding such a model in a way that would be useable by an embedded system.
I ended up researching succinct data structures, and messing with graph
encodings, just to convince myself that it had a reasonable chance of being
implementable. By then I returned to Bayesian networks, only to decide that
they were probably overkill in their nominal form (continuous functions,
whereas I wanted truncated models), and the specific form of that data would
depend on whether I could even estimate the wind vector in the first place.
Thus I was back to particle filters. I then began to implement a paraglider
dynamics model from Benedetti's thesis, which turned out to be a useful
starting point but ultimately rubbish. So, I had to create my own, which
launched me on a long survey of parafoil literature.


Oh, what have I actually done? Well, I created a simple Paraglider geometry
definition and implemented it in Python. Given the wing definition, I then
needed to estimate the forces+inertias of the wing+harness system. Arched and
swept wings are a pain to analyze, so I chose a numerical lifting line method
developed by Phillips. I've tried to verify it against a wind tunnel test of
a quarter scale model built by Belloc, but it doesn't agree particularly well
(overestimates the lift coefficients). I'm not sure why, but hey, at least
I have a model + dynamics to use with a particle filter.

Of course, a naive particle filtering is painfully slow for anything beyond
tiny problems with only a few state variables and reasonable dynamics. Thus
I began researching particle filter architectures until I settled on the
GMSPPF developed by Merwe for his dissertation. I haven't finished
implementing that, but I probably should.... Hm..
