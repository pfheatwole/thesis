.. This chapter demonstrates how to model a paraglider wing and simulate its
   dynamics. The modeling process combines basic technical specs from a user
   manual with photographic information and reasonable assumptions about
   paraglider wing design. The simulations perform static and dynamic
   performance tests (polar plots and flight maneuvers, respectively) and
   compare them to expected behaviors.


*************
Demonstration
*************

The previous chapters developed a parametric paraglider model. This chapter
demonstrates how to estimate the parameters from incomplete specification data
in order to approximately model a commercially available paraglider wing.
A major component of the modeling process is how to augment the missing
information with reasonable assumptions.

Once the model is complete, it is sanity checked by comparing estimates of its
longitudinal steady-state aerodynamics over the range of control inputs
against published performance data, such as minimal sink rate and speed range.
The chapter concludes with flight simulations using the model in a variety of
flight scenarios.


Model
=====

This section demonstrates one possible workflow to create an approximate model
of a real wing from basic technical specs. Many detailed components, such as
the harness, line geometry, are replaced with simplified models.

Implementations of the simplified models are provided as part of the
`glidersim` package.

[[FIXME: review how well the resulting model matches the specs (all
dimensions: lengths, areas, masses, etc)]]


Available data
--------------

[[What did I have to work with?]]

* Wing data is available from three primary sources:

  1. Technical specifications and user manuals

  2. Pictures

  3. Physical measurements


Photos
^^^^^^

[[Start with some photos to show what I'm creating?]]


Technical specs
^^^^^^^^^^^^^^^

[[What data did I have? What did I use?]]

From the manual:

.. list-table:: Wing data
   :header-rows: 1

   * - Property
     - Value
     - Unit
   * - Root chord
     - 2.58
     - m
   * - Tip chord
     - 0.52
     - m
   * - Standard mean chord
     - 2.06
     - m
   * - Flat area
     - 23
     - m\ :sup:`2`
   * - Flat span
     - 11.15
     - m
   * - Flat aspect ratio
     - 5.40
     - --
   * - Projected area
     - 19.55
     - m\ :sup:`2`
   * - Projected span
     - 8.84
     - m
   * - Projected aspect ratio
     - 4.00
     - --
   * - Number of cells
     - 52
     - --
   * - Total line length
     - 218
     - m
   * - Central line length
     - 6.8
     - m
   * - Accelerator line length
     - 0.15
     - m
   * - Solid mass
     - 4.7
     - kg
   * - In-flight weight limit
     - 85
     - kg


Canopy
------

[[This section should highlight how a reasonable approximation can be produced
from the minimal wing data like flat and inflated span, taper, etc. Show what
data I had, what assumptions I used to fill in the blanks, and how well the
result matched the target.]]

[[This model uses two *design curves*: parametric functions rely on domain
expertise to "fill in the gaps" of the sparse technical data. It assumes an
elliptical chord distribution (which only requires the root and tip lengths),
and an elliptical `yz(s)` that only needs two (or even one) parameter by
assuming an elliptical (or circular) arc. Refer to their


Developing a canopy model has four basic steps:

1. Design the section layout

2. Assign section profiles

3. Specify the upper and lower surface extends to define air intakes

4. Specify the materials to enable computing the resulting real and air mass
   inertia matrices.


Foil layout
^^^^^^^^^^^

[[Introduce my choice of *design curves*: parametric equations that encode the
structural knowledge necessary to approximate a canopy geometry model from the
basic technical specs]]


Chord length
~~~~~~~~~~~~

[[The simplest place to start modeling the canopy is the chord length
distribution. In this case the specs only give the root, tip, and mean chord
lengths, but paragliding wings commonly use truncated elliptic functions
because they encourage elliptic lift distributions (thus reducing induced
drag). Fitting an elliptic function to the root and tip lengths and computing
the mean average chord length of the resulting function confirms the elliptic
assumption.


[[Also, confirm the flat area at this point.]]


Longitudinal positioning
~~~~~~~~~~~~~~~~~~~~~~~~

[[The next step is to choose the :math:`r_x` parameter. Although this
parameter can technically be a function of the section index, many wings can
be described with a constant value. This value can be estimated by considering
pictures of the inflated wing, but since flattened drawings are commonly
available in technical manuals they are typically more convenient.
(Admittedly, such drawings are not always to scale, and so should be used with
caution.) For this wing, a small amount of trial and error using a top-down
view from the wing user manual suggests :math:`r_x = 0.7`.]]

.. figure:: figures/paraglider/simulations/Hook3_topdown.jpg
   :name: Hook3_topdown

   Top-down outline of flattened canopy

   The black outline is the boundary of the model's flattened chord surface.
   The colored background is taken from the user manual for the wing.

As seen in :numref:`Hook3_topdown`, the elliptical chord assumption with
:math:`r_x = 0.7` gives a close match to the drawing in the manual.

[[Compare the areas given what I have so far?]]


Arc
~~~

The next step is to model the arc. For this wing, photos of the wing suggest
that a circular arc segment is reasonable. There are several ways to fit an
arc segment, such as the width to height ratios, or visual estimation of the
arc angle, but since the specs included both the flattened and projected
areas, it can be easier to simply increase the arc angle until the projected
area of the model matches the expected value.


[[FIXME: show a few examples: a circular arc and an elliptical arc. Just
enough to show the mean and tip dihedral angles I use in `glidersim`.]]

[[FIXME: how did I choose `r_yz`?]]

[[Show the rear-view picture and the resulting model?]]

[[In my case I adjusted `mean_anhedral` until the projected values are roughly
correct.]]


Geometric torsion
~~~~~~~~~~~~~~~~~

[[This is a guess. Paragliders can be expected to have positive torsion, but
the distribution is unknown to me.]]


Section profiles
^^^^^^^^^^^^^^^^

[[Choose an airfoil]]

* Why did I choose the 24018? Belloc used the 23015, but
  :cite:`lingard1995RamairParachuteDesign` says that many older designs used
  a Clark-Y with 18% thickness. I chose the 24018 as a sort of clumsy
  compromise. He also mentions that newer gliders have "benefited from glider
  technology and use a range of low-speed section" like the LS(1)-0417 (which
  was also chosen by :cite:`becker2017ExperimentalStudyParaglider`). I should
  have probably used the LS(1)-0417 but oh well.

[[FIXME: modified profiles for brake deflections]]

[[FIXME: section coefficients]]


Air intakes
^^^^^^^^^^^

[[Air intakes via upper/lower surface separation? I never measured them.]]


Materials
^^^^^^^^^

FIXME


Suspension lines
----------------

[[In a physically accurate model a complete specification of the line geometry
would define the accelerator function and brake deflections. Instead, this
model uses approximations for both, separately. After all, the paraglider
dynamics don't care HOW you define the functions, just that they're
available.]]

[[FIXME: what about the total line length and drag?]]


Accelerator
^^^^^^^^^^^

[[Position of the A and C connection points, accelerator geometry]]


Brake deflections
^^^^^^^^^^^^^^^^^

[[Assumed brake distribution]]

* **The "assume a brake deflection" step is super handwavy.** I didn't have
  time to model the actual line geometries, so I just fudged it. Not a major
  problem, but call it out when discussing reasons why I'm not comparing this
  to actual flight data (goes together with the other uncertainties, like
  unknown airfoil).

.. figure:: figures/paraglider/simulations/Hook3_rear_view.jpg
   :name: Hook3_rear_view

   Rear-view of an inflated wing

[[From this picture you can see that the brake deflection doesn't start until
some distance from the root. The brake lines are hard to see, but their
deflections are intuitive. The result is that instead of using a true line
geometry, you can get away with an approximate deflection distribution using
a simple cubic function with a few carefully chosen end points.]]

[[surface materials, ribs net mass]]

[[My mass calculations neglect the extra mass due to things like the riser
straps, carabiners, and internal v-ribs and straps, so I'm underestimating the
mass, but I'm also assuming the vertical ribs are solid (no ports) so that
makes up for a bit of the missing mass]]



Harness
-------

[[The specs say the wing can carry a maximum total weight (including the wing
mass itself) of 85kg. The wing is roughly 5kg, so a 75kg payload is
reasonable. I'm not modeling ]]

[[Total payload mass, radius of spherical approximation, etc]]

* I've been using 75kg, so the in-flight weight is ~80kg, well within limits.

[[FIXME: should I move the spherical harness model here? It's never set well
with me to have it in `Paraglider Dynamics`; that section feels scatterbrained
/ mistitled.]]


Static performance
==================


Equilibrium states
------------------

[[FIXME: what are they, and how do you compute them? These are the basis for
the polar curves.]]


Polar curves
------------

.. Steady-state, longitudinal-only analyses

* [[These curves summarize the equilibrium states over a range of control
  inputs.]]

* Show the polar curves and consider if they are reasonable. [[Using which
  model? 9a?]]

* [[Use this section to really highlight the limitations/assumptions of the
  model? Unknown airfoil, unknown true line positions, lack of a proper
  `LineGeometry` (so brake deflections and arc changes when accelerator is
  applied are both unknown), no cell billowing, etc etc.

  Seems like a good place to point out "this is overestimating lift and
  underestimating drag, as expected."]]


Dynamic performance
===================

.. Informative flight scenarios

* Steady-state turn rate and radius size

* Control input impulses (on/off of symmetric brake, asymmetric brake,
  accelerator, weight shift)

* Sink rates during a hard turn. (See the DHV ratings guide)

* Response to "exiting accelerated flight".

  According to Sec:4.5.1 of the DHV ratings guide, it sounds like wings dive
  **forward** when the accelerator is abruptly released. For my current
  Hook3ish, the wing experiences **backwards** pitch. Is this because I'm
  neglecting changes to the canopy geometry? Or is it symptomatic of the fact
  that I assume the lines stay taught? Conceptually, when you quickly release
  the speedbar, the A lines will quickly extend; it takes some time for the
  harness to drop (or the wing to rise) enough to regain tension, so the wing
  is certainly going to behave in ways not modeled by my equations. Good to
  point out.

* Does it exhibit "roll steering" vs "skid steering"? Or maybe the arc is too
  round for that effect. See :cite:`slegers2003AspectsControlParafoil`.

* The importance of apparent mass. Start by comparing the real versus apparent
  mass matrices; consider the relative magnitudes and the likely effects from
  accounting for apparent inertia. Then show some scenarios where the effects
  are noticeable.

* For more ideas, see :cite:`wild2009AirworthinessRequirementsHanggliders`
  Sec:4.1 (pg28) for the DHV maneuvers for wing classification

  Also, :cite:`lingard1995RamairParachuteDesign` Sec:7 and Sec:8.]]


Discussion
==========

* Everything related to the airfoils is sketchy. The choice of airfoil,
  modeling their deflected geometries, modeling the deflection distribution,
  etc. Tons of uncertainty here. Just stick a big red flag in it and say "hey,
  if you want to solve this problem, here's a big sticking point."


This chapter suggests a simple workflow:

1. Fit the flattened chord surface (`c(s)`, `x(s)`, `r_x(s)`)

2. Fit the arc (`yz(s), r_yz(s)`)

3. Apply geometric twist (`theta(s)`)

4. Specify section profiles (airfoils) and their coefficients

   [[Introduce gridded coefficients]]

5. Specify material densities (upper, lower, ribs) for computing the inertia

6. Specify a suspension line model (harness position, accelerator function,
   brake deflection distribution, line drag)

7. Specify a harness model

