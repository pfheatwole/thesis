Introduction to a thesis
========================

The structure of an introduction to a thesis, as presented by "Explorations of
Style":

1. Introduction to the introduction

   This section is a condensed version of the three moves (context, problem,
   and response). For a thesis, this may be useful for "getting to the point"
   more quickly than a full introduction, but without the extreme concision of
   an abstract.

2. Context

   "Provides the full context in a way that flows from the opening."

3. Restatement of the problem

   "Restate the problem and significance in light of the more thoroughly
   detailed context."

4. Restatement of the response

   Now that I've highlighted the set of problems, discuss my work towards
   solving those problems. This time, leverage the detail in the *full*
   context and restated problem description to elaborate on the details of the
   response.

5. Roadmap



Intro to the Intro
==================

The introduction to the introduction is important to my project since the
scope is so broad. Trying to establish the entire context in detail before
getting to a description of what my thesis offers will make the reader wait
a long time before they learn about my contribution. You need to **put the
contribution of the paper front and center; the reader should know ASAP what
they will gain by reading it.**

John Swales' model for "Creating a Research Space" consists of three "moves":

1. Establishing a research territory
 
2. Establishing a niche
 
3. Occupying the niche

 
(An alternative is "Context", "Problem and Significance", and "Response".)

According to Explorations of Style, "An Introduction to the introduction [...]
will be a short version of the three moves, often in as little as three
paragraphs, ending with some sort of transition to the next section where the
full context will be provided."

In my case, I will first set the context (my research territory: paragliding
dependencies on wind patterns), then introduce my motivating goal (my niche:
learning wind patterns from flight data), then introduce how I've made
progress towards goal (how I've occupied the niche: by building the flight
reconstruction portion of the model).


A brief introduction to paragliding
===================================

NT


Relevant weather characteristics
================================


Good general atmospheric references:

* Atmospheric Thermodynamics (North, Erukhimova; 2009)

* Atmospheric Science (Wallace, Hobbs; 2006)



Some useful definitions:

* "The *geoid* is the shape the ocean surface would take under the influence
  of gravity **and the rotation of the Earth** alone, if other influences such
  as winds and tides were absent." This is not a sphere, or even an oblate
  ellipsoid; it is an irregular surface, since the Earth does not have uniform
  density; the surface of the goid is higher than the reference ellipsoid
  wherever there a mass excess, and lower than the reference ellipsoid
  wherever there is a mass deficit. All points on the geoid have the same
  *effective potential* (the sum of gravitational potential energy **and**
  centrifugal potential energy).

* *geopotential altitude* is "calculated from a mathematical model that
  adjusts the altitude to include the variation of gravity with height"

* *geometric altitude* is "the standard direct vertical distance above mean
  sea level"


Lapse rates
-----------

* Lapse rates are typically given in terms of geopotential altitude (not
  geometric altitude)

* The *dry adiabatic lapse rate* is 10.0 C/km. The *moist adiabatic lapse
  rate* is 0.55 C/km. The average lapse rate defined by the international
  standard atmosphere is 6.49 C/km (the ISA model is "based on average
  conditions at mid latitudes"). The average is between the dry and moist
  adiabatic lapse rates, which makes sense.


* Super-adiabatic lapse rates

  How can the environmental lapse rate be *greater* than the DALR? **I think
  I'm missing the significance of adiabatic processes.** I'm guessing the dry
  adiabatic rate is kind of a reference line; if you go above or below this
  nicely behaved curve, stability changes.

  According to `theweatherprediction.com`, a super-adiabatic lapse rate is
  usually caused by intense solar heating at the surface.


* How does an adiabatic process work?

  "An *adiabatic process* occurs without transfer of heat or mass of
  substances between a thermodynamic system and its surroundings. In an
  adiabatic process, energy is transferred to the surroundings only as
  *work*."

* I'm planning to group group all the {altitude, pressure} measurements into
  a single set, and fit them to a single dry adiabatic curve. Does my "fit to
  a single dry adiabatic curve" equivalent to saying that I'm pretending that
  those measurements were all taken from the same parcel of air rising through
  an adiabatic expansion?  Seems like a rather strong assumption.

  Also, I'm assuming that the lapse rate doesn't vary with horizontal changes.
  **Is this reasonable?** For example, around mountainous terrain, if the
  boundary layer follows the topography, then the air near the mountain will
  probably be hotter than the air further away, right? (ie, I'm assuming that
  neighboring region will have roughly the same temperature at the same AGL?)


Convective boundary layer
-------------------------

Synonyms: *convective planetary boundary layer*, *atmospheric mixing layer*,
*dry adiabatic layer*

* The CBL is a PBL when positive buoyancy flux at the surface creates
  a thermal instability and thus generates additional or even major turbulence
  (aka, *convective available potential energy*, or CAPE)"

* "A CBL is typical in tropical and mid-latitudes during daytime."


* How far up do thermals extend? That is, how high can paragliders fly?

  According to `garratt1994ReviewAtmosphericBoundary`, it is generally below
  [2 - 3] km, but over deserts in mid-summer under strong surface heating the
  ABL may be as much as 5 km deep, and even deeper in conditions of vigorous
  cumulonimbus convection"


In `oberson2010ConvectiveBoundaryLayer`, he emphasizes that this is the layer
mixed by **dry** thermals; do you never have thermals in saturated air?



Inversion layers
----------------

* What is an inversion layer?

  When the atmospheric temperature is increasing instead of decreasing with
  altitude.

* What are the types of thermal inversions?

  There are *surface* inversions near the Earth, and vs *aloft* 


* What is the range of altitudes where they're likely to occur? Under what
  conditions are they more common (hot or cold days)? What is the role of
  local geography (eg, mountains increase thermal inversions in valleys)?

  (Sounds like in Salt Lake City they're more common during the winter, but
  I'm not sure if that generalizes to "they're more common during cold days".)

* What are the effects of a thermal inversion layer?

  * Temperature inversions block atmospheric convection. (Describe *stable*
    versus *unstable* air; note that "unstable" is not the same as
    "turbulent"; "instability" refers to the amount of positive bouyancy).
    This lack of mixing traps pollutants, so air quality decreases.

    I suspect this also reduces the maximum height of thermals?

  * As rain falls into cooler if, it can produce freezing rain.

* How do thermal inversions relate to lapse rates?

* How likely are paragliders to encounter thermal inversions? (ie, how
  important/relevant are they for the purposes of my thesis?)

  They are more common above valleys surrounded by mountains, so I suppose
  mountain flying is more likely. (Ridge soaring is typically lower altitude
  anyway, isn't it?)


* What are the differences between a *thermal inversion layer* and *cloud
  base*?

* Interesting sidenote: if you're able to reliably detect thermal inversions,
  that could be a really interesting model input. I'm guessing it'd be at
  least somewhat informative regarding the behavior of thermals in that region
  (presence/absence, etc).

