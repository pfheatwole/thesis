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


2019-03-01 Starting to Sprint
=============================

I need to pick up the pace. I'm feeling really stressed out, like I'm never
going to finish. Today I notice that Professor Khosmood never updated my
"incomplete" grade for "Artificial Intelligence" and it defaulted to an "F",
so now I have to call him on Monday to discuss what the grade should have
been. If he gives me a "C" I'll be satisfied; not happy, but at least I can
still graduate.

I have fallen so so far below expectations. I started my school career with
a whimper (DeVry), then fought back until I started getting good grades in all
my difficult classes at MJC, then I started CalPoly and continued with good
grades. And yet, despite all those successes that *suggest* I'm a competent
engineer, I have lately demonstrated a systematic failure to make something of
myself.

It's time to renew my efforts. I'm going to bash away at this stupid paper,
pushing more and more content until it bursts at the seams. I need to crush
this malaise and get it done.


2019-03-04 (Filtering) Process Noise
====================================

I've been attempting to "plan my work and work my plan", but that only works
well if the plan is good. Back when I was trying to determine if a filter
structure existed that could handle the extremely undetermined nature of my
project, I discovered the Gaussian mixture sigma-point Kalman filter (GMSPPF).
I couldn't build it of course: I needed a paraglider dynamics model. And so,
I went off to design the model, and now I've returned to the GMSPPF.

The GMSPPF isn't terribly complicated, but it does have a lot of details.
I was struggling to keep all those details in my head, to integrate the
paraglider state, wind "state", and control "state" into the filtering
process, simultaneously, when I realized I had missed the obvious stepping
stone: given a known paraglider dynamics model, and by assuming *known* wind
and control inputs, what does the relevant UKF look like? Until I can answer
that, the GMSPPF is irrelevant (since I need a working UKF for the wing
first).

And so, my stepping stones are:

1. Given known wind and control inputs, design the process noise for the
   paraglider state, and get the UKF working (simulate a flight trajectory,
   then run a UKF over a subset of paraglider state variables (say, you
   observe position and orientation and output an estimate of the complete
   pose).

2. Design a process model for wind that can capture the potential variability
   of local wind changes. This isn't for producing the wind fields, it's for
   producing and estimate of the mean and covariance of the wind at the
   paraglider's current location. A reasonable estimate is probably a Gaussian
   process.

3. Build the GMSPPF framework. The UKF in step 1 assumed that the paraglider
   state is observable (given an observation of the position and orientation),
   but I don't have any measurements for the wind, so I'm going to have to
   simulate them.
   
**Question**: Should I build a UKF that receives an observation of the wind
and get that working first? Maybe I should start by building a UKF that gets
noisy observations of all the states. So, the progression would become:

1. A UKF with noisy observations of the wing position+orientation, and known
   wind and control inputs.

2. A UKF with noisy observations of the wing position+orientation, with noisy
   observations of the wind, and known control inputs. (The wind becomes part
   of the filter output).

3. A UKF with noisy observations of the wing position+orientation, known wind,
   and noisy observations of the control inputs. (The inputs become part of
   the filter output).

4. A UKF with noisy observations of the wing pose, wind, and control inputs.
   (At this point, the system is still well-determined and observable,
   I think.)

5. FIXME


2019-03-13 Back to Basics
=========================

The big problem with modelling the control input "dynamics" as independent
white noise sources is that you'll end up with nonsense combinations, like
full brakes and full speedbar, or wildly fluctuation inputs. I would prefer to
model these sequences with a multi-output Gaussian process so that I can place
priors over smoothness and cross-correlations (non-zero speedbar suggests less
braking, etc). Turns out that's really hard, so I'm going back to the building
blocks of the project: a paraglider model, a few sample wind fields (for
demonstration purposes), a control sequence generator (hand-crafting control
inputs), and a simulator to generate the trajectories.

I need to get those basics clean and written up before I know if I'll have
time for anything extra, like filtering.
