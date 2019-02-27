2019-02-20 Freewrite
====================

I'm struggling to push back into the project. Why? I think it's because the
project seems too big to get a handle on. I've created a whole slew of pieces,
but individually they're all still very raw and often incomplete, or even
broken.


Okay, so what are the pieces of the thesis, and what's wrong with them?

* Data processing

  * IGC processing: well, this is actually reasonably done, just not very useful
    at the moment (since I'm not trying to filter actual tracks)

  * Vario debiasing: Makes strong assertions without strong theoretical
    underpinnings.

  * **A lot of this can be pushed into a separate, short section**: "In order
    to apply this method to non-simulated data, there is a host of data
    processing tasks: estimating the GPS error with a Chi2 distribution,
    debiasing the altitude data with dynamic time warping, transforming
    between geographic coordinate systems (geodetic, ECEF, and tangent plane
    representations), etc." This could even be a "Future Work" subsection.

* Paraglider dynamics model
  
  The airfoils are probably my biggest weakness (XFOIL results are *very*
  sensitive to small changes to the airfoils), but I'm also suspicious that
  paragliding wings experience separation bubbles or similar, such that the
  theoretical estimates are over-optimistic

  Oh, reminder to self: do I know what the airfoil data looks like for the
  quarter-scale wing model used by Belloc? I never did finish up recreating
  his results using Phillip's method.

* Particle filter
  
  Not implemented yet. Well, that's not strictly true: it's more that the
  GMSPPF isn't implemented. Which filters have I implemented: do I have
  a particle smoother yet? Is it feasible to do flight reconstruction on a 15
  second section and see how that turns out?


Okay, so how do I answer these qualms?

* It's incomplete: of course it is, this is an exploratory project

* It has broken stuff: which pieces are broken, how are they broken, and why
  are they broken? Put a bounding box that says you're aware of the issues and
  makes other people confident in knowing where they stand.

* Vario debiasing lacks theoretical underpinnings: that doesn't matter, you're
  not going to run the particle filter on non-simulated tracks anyway. You
  could mention it in passing, but not attempt to prove it.


Takeaways:

* Give people confidence they know what it is you're providing. Preempt them
  with regards to incompleteness, bugs, poor design, etc etc.

* Make a list of whatever assumptions you need to present your findings in
  a legitimate way. You can do whatever you need to within the bounds of your
  own constraints.

* Review your particle filtering + smoothing code. See if you can put it into
  a workable state such that you can simulate 15 seconds of flight

* Think of some good demonstrations for the filtering method (assume you had
  a working particle smoother and paraglider dynamics model: what tests would
  you like to run to **show its efficacy?**)
  
  Well, in terms of wind: still air, entering a thermal, exiting a thermal,
  lateral gusts. In terms of controls: zero controls, steady brake, step
  input, ramp input, changing sides (left ramp then right ramp, whatever).

* **Making sure my Phillip's method is working reasonably well seems like
  a high priority.** Maybe contact Belloc and ask if my XFOIL data looks
  correct?


2019-02-26 Chicken or the Egg
=============================

I keep waffling between writing content and building the structure. The
structure of the document informs the content I'm writing, but until I have
some content, I get stuck thinking of what the structure should be.

Maybe I should write a set of individual files on individual topics, then work
backwards?
