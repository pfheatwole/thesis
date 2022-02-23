.. This chapter demonstrates how to use the component models to create
   paraglider system models and simulate their dynamics. The modeling process
   combines basic technical specs from a user manual with photographic
   information and reasonable assumptions about paraglider wing design. The
   simulations perform static and dynamic performance tests (polar plots and
   flight maneuvers, respectively) and compare them to expected behaviors.


*************
Demonstration
*************

One reason that modeling a commercial paraglider wing is difficult is because
the published specifications are limited to basic summary measurements. A major
task of the modeling process is augmenting the missing information to create
a complete model. To address that difficulty, this paper developed parametric
:doc:`component models <paraglider_components>` that encode assumptions of the
unknown structure.

This chapter demonstrates one possible workflow to estimate the parameters of
the component models by combining publicly available technical specifications
and photographs with knowledge of typical paraglider wing design. Once the
components are combined into a :doc:`system model <system_dynamics>`, it is
validated by comparing its estimates of the glider's longitudinal steady-state
aerodynamics over the range of control inputs against published performance
data, such as minimum sink rate and speed range. The chapter concludes with
flight simulations using the model in a variety of flight scenarios.


Model creation
==============

.. Introduce the wing

The paraglider wing used in this example is a Niviuk Hook 3. With forgiving
flight characteristics targeting advanced beginners, this wing is not intended
for acrobatics, so the :ref:`limitations <foil_aerodynamics:limitations>` of
the :ref:`aerodynamics method <foil_aerodynamics:Phillips' numerical
lifting-line>` are not an issue when simulating the majority of flights
produced by this wing.

.. figure:: figures/paraglider/demonstration/Hook3_front_view.jpg
   :name: Hook3_front_view

   Front-view of an inflated Niviuk Hook 3

Wing data is available from four primary sources:

1. Technical specifications and user manuals

2. Flight test data from certifications and reviews

3. Pictures and videos

4. Physical measurements

For this chapter, physical measurements will not be used. Although physical
measurements are ideal, they are frequently difficult to obtain (especially for
older wings). Instead, this demonstration is focused on showing that it is
feasible to create an approximate wing model even if physical measurements are
unavailable.


Technical specs
---------------

From the official `technical specifications manual
<https://niviuk.com/niviuk/customer_pdf/Descatalogado/Hook%203/Datos%20t%C3%A9cnicos/HOOK3_TECNIC_ENG.pdf>`_:

.. list-table:: Wing data
   :header-rows: 1
   :widths: auto

   * - Property [unit]
     - Size 23
     - Size 25
     - Size 27
   * - Flat area [m\ :sup:`2`]
     - 23
     - 25
     - 27
   * - Flat span [m]
     - 11.15
     - 11.62
     - 12.08
   * - Flat aspect ratio
     - 5.40
     - 5.40
     - 5.40
   * - Projected area [m\ :sup:`2`]
     - 19.55
     - 21.25
     - 22.95
   * - Projected span [m]
     - 8.84
     - 9.22
     - 9.58
   * - Projected aspect ratio
     - 4.00
     - 4.00
     - 4.00
   * - Root chord [m]
     - 2.58
     - 2.69
     - 2.8
   * - Tip chord [m]
     - 0.52
     - 0.54
     - 0.56
   * - Standard mean chord [m]
     - 2.06
     - 2.14
     - 2.23
   * - Number of cells
     - 52
     - 52
     - 52
   * - Total line length [m]
     - 218
     - 227
     - 236
   * - Central line length [m]
     - 6.8
     - 7.09
     - 7.36
   * - Accelerator line length [m]
     - 0.15
     - 0.15
     - 0.15
   * - Solid mass [kg]
     - 4.9
     - 5.3
     - 5.5
   * - In-flight weight range [kg]
     - 65-85
     - 80-100
     - 95-115

This section defines the model parameters for a model of the size 23 wing. The
same process is used — but not shown — to created models of the size 25 and 27
wings for the discussion on :ref:`demonstration:Model validation`.

.. FIXME: link to the implementation in glidersim


Canopy
------

.. This section should highlight how a reasonable approximation can be
   produced from the minimal wing data like flat and inflated span, taper,
   etc. Show what data I had, what assumptions I used to fill in the blanks,
   and how well the result matched the target.

The first component model of the paraglider system is for the :ref:`canopy
<paraglider_components:Canopy>`. The canopy model uses a :doc:`foil_geometry`
model and :ref:`physical details <paraglider_components:Solid mass>` such as
material densities and surface extents to estimate the aerodynamics and
inertial properties of the canopy.


Geometry
^^^^^^^^

.. Workflow:

   0. Choose a scaling factor (`b` or `b_flat`)

      **Isn't this only for my normalized `yz(s)`?** All the other pieces only
      depend on `s`. Interesting, because that'd mean I could just make `b_flat`
      a parameter of `elliptical_arc` instead of scaling inside `Foil`. Oh, wait,
      I'm also scaling the chord distribution by `b_flat`; right, because
      I thought it was easier to think in terms of proportional chord lengths.

      Even so, you don't HAVE to do it this way for the paper. **Just use the
      explicit distances for this chapter, even if it doesn't match the code.**

      Counterpoint: it does make it easier to define the arc, even if I don't
      explain the details. Just say "Here, I've provided an elliptical arc
      generator: you just need to specify the mean anhedral, tip roll, and flat
      span."

   1. Fit the flattened chord surface (`c(s)`, `x(s)`, `r_x(s)`)

   2. Fit the arc (`yz(s), r_yz(s)`)

   3. Apply geometric twist (`theta(s)`)

   4. Specify section profiles (airfoils) and their coefficients

      [[Introduce gridded coefficients]]



.. Span (b_flat)

[[Start by defining :math:`b_\textrm{flat}`, which can be read directly from
the technical specs.]]

.. FIXME: discuss

   * The choice of :ref:`section index <foil_geometry:Section index>` makes this
     step simpler because you can use the `b_flat` instead of `b_proj`. Explain
     that?

   * In ``glidersim`` this is a scaling factor for the normalized
     ``FoilGeometry``; that's an implementation detail, but the point of this
     section is to demonstrate how it makes things easier to define foils, so
     it's not irrelevant.


.. Chord length (c)

[[Next up is the chord length distribution. The technical specifications only
list the root, tip, and mean chord lengths, but a reasonable guess is that the
wing uses a truncated elliptical distribution. (Paragliding wings commonly use
truncated elliptic functions because they encourage elliptic lift
distributions, thus reducing induced drag.) Fitting an elliptic function to
the root and tip lengths and computing the mean average chord length of the
resulting function confirms the elliptic assumption.

[[Check: fitting an elliptical produces a standard mean of 2.06m, which
matches the technical specs exactly.]]

.. FIXME: compare the specified vs computed flat areas


.. Fore-aft positioning (r_x, x)

[[The next step is to design the fore-aft positioning of the sections, which
are controlled by the :math:`r_x(s)` and :math:`x(s)` design curves. Although
the obvious choice is to choose :math:`r_x(s) = 0` and measure the
:math:`x`-offsets of each section, this choice often produces an unnecessarily
complicated :math:`x(s)` function. Instead, paragliders can often be described
with some constant :math:`r_x(s)` and :math:`x(s) = 0`. The constant reference
position can be estimated by considering pictures of the inflated wing, but
since flattened drawings are commonly available in technical manuals they are
typically more convenient. (Admittedly, such drawings are not always to scale,
and so should be used with caution.) For this wing, a small amount of trial
and error using a top-down view from the wing user manual suggests :math:`r_x
= 0.7`.]]
As seen in :numref:`Hook3_topdown`, the elliptical chord assumption with
:math:`r_x = 0.7` gives a close match to the drawing in the manual.

.. figure:: figures/paraglider/demonstration/Hook3_topdown.jpg
   :name: Hook3_topdown

   Top-down outline of flattened canopy

   The black outline is the boundary of the model's flattened chord surface.
   The colored background is taken from the user manual for the wing.

[[FIXME: sanity check the flattened chord surface. Span, area, AR.]]


.. Arc (yz-curve)

With the flattened chord surface completed, the next step is to define the
*arc* (position in the :math:`yz`-plane). Photos of the wing suggest that
a circular arc segment is a reasonable starting point. There are several ways
to estimate the elliptical arc parameters of the physical wing, such as the
width to height ratios, or visual estimation of the arc angle, but [[since the
specs included both the flattened and projected spans, the simplest method is
to guess :math:`\phi_\textrm{tip}` and increase the arc angle
:math:`\Gamma_\textrm{tip}` until the projected span matches the expected
value.]]

[[FIXME: finish writing. For example, checking the "naive" fit based on
a circular arc is pretty close, but the projected surface area doesn't match
the specs; the fit can be improved by replacing the circular arc with an
elliptical arc. For this section, use trig to compute the elliptical parameters
manually, but mention that ``glidersim`` provides helper functions to simplify
the process.

My final fit was `mean_anhedral = 32`, `tip_anhedral = 75`. Note that the
``elliptical_arc`` function uses "anhedral" (`mean_anhedral` and
`tip_anhedral`) to describe the angles might by the positions of the `yz`
curve, not the orientation of individual sections.]]

.. FIXME:

   * Explain how I adjusted `mean_anhedral` until the projected values are
     roughly correct?

   * Explain how I chose `r_yz`? Technically this would depend on the
     geometric torsion, but since I'm unsure the safe choice is `r_yz = 0.5`

   * Show the rear-view picture and the resulting model? I'd prefer
     a straight-on photo, it's hard to tell with angled photos.

   * Confirm the projected area and projected span


.. Geometric torsion (theta)

After the relatively straightforward process of positioning the section comes
the more difficult task of estimating their orientation. In the
:ref:`simplified model <foil_geometry:Simplified model>` section roll is
defined by the curvature of the :math:`yz`-curve and the section yaw is defined
as zero, but the section pitch :math:`\theta(s)` (or *geometric torsion*) can
be difficult to measure. Most parafoils benefit from a small amount of
increasing geometric torsion towards the wing tips (or *washin*), and
a conservative guess of 4 degrees at the wingtip should be reasonably accurate.
[[FIXME: how does the torsion develop? Most designs assume linear, but I use
a polynomial.]]

.. FIXME: what's the DISTRIBUTION for the Hook 3? No way to confirm? The
   angles are small and difficult to measure from a wing on the ground.

[[FIXME: sanity check the inflated chord surface. Span, area, AR.]]


.. Section profiles

After the section layout (scale, position, and orientation) is complete, each
section must be assigned an airfoil.

[[FIXME: explain my choice. Belloc used the 23015, but
:cite:`lingard1995RamairParachuteDesign` says that many older designs used
a Clark-Y with 18% thickness. I chose the NACA 24018 as a sort of clumsy
compromise. He also mentions that newer gliders have "benefited from glider
technology and use a range of low-speed section" like the LS(1)-0417 (which
was also chosen by :cite:`becker2017ExperimentalStudyParaglider`).]]

.. figure:: figures/paraglider/demonstration/braking_NACA24018.*
   :name: airfoil set, braking NACA24018

   Set of NACA 24018 airfoils with trailing edge deflections.

[[FIXME: explain why this is an extremely optimistic model of how parafoil
sections deform with increasing brake inputs. I'd go as far as to say that
this is the number one source of error in the model.]]

[[FIXME: explain how I produced those profiles. Oof.]]

[[FIXME: explain using XFOIL to estimate the section coefficients]]


Inertia
^^^^^^^

[[Assigning the section profiles completes the (idealized) parametric
:doc:`foil geometry <foil_geometry>` model, and it can be used to define
a :ref:`canopy model <paraglider_components:Canopy>` for the paraglider wing
by assigning it physical attributes such as surface material densities (to
calculate its inertia) and air intake extents (to calculate the viscous drag
corrections).

.. Materials (rho_upper, rho_lower, rho_ribs)

In this case, the surface material densities can be read directly from the
materials section of the user manual:

.. ref: HOOK3_MANUAL_ENG.pdf, Sec:11.2, p.15

.. list-table:: Hook 3 material densities
   :header-rows: 1
   :align: center
   :name: hook3_material_densities

   * - Surface
     - Material
     - Density :math:`\left[ \frac{kg}{m^2} \right]`
   * - Upper
     - Porcher 9017 E77A
     - 0.039
   * - Lower
     - Dominico N20DMF
     - 0.035
   * - Internal ribs
     - Porcher 9017 E29
     - 0.041


.. FIXME: the specs list the total wing weight at 4.7kg, but the
   upper/lower/rib materials only account for 2.5kg or so. My mass
   calculations neglect the extra mass due to things like the lines, riser
   straps, carabiners, internal v-ribs, horizontal straps, tension rods, etc,
   so I'm underestimating that mass, but I'm also assuming the vertical ribs
   are solid (no ports) so that makes up for a bit of the missing mass


.. Air intakes (s_end, r_upper, r_lower)

For the air intakes, the user manual provides a projected diagram (Fig. 11.4,
p. 17) which shows that the air intakes start at the 21st of 26 ribs spreading
out from the central rib; assuming a linear spacing of the ribs this would
correspond to :math:`s = 0.807`, so :math:`s_\textrm{end} = 0.8` is
a reasonable guess for the spanwise extent of sections with air intakes.

The other dimension of the air intakes is the size of their opening, which is
determined by the extent of the upper and lower surface. This value is
difficult to determine precisely from photos, but thankfully its effect on the
solid mass inertia and viscous drag is relatively minor; in the absence of
physical measurements, a reasonable guess is :math:`r_\textrm{upper} = -0.04`
and :math:`r_\textrm{lower} = -0.09` for an air intake length roughly 5% of the
length of the chord.

.. figure:: figures/paraglider/demonstration/air_intakes.*

   NACA 24018 with air intakes

[[FIXME: sanity check the total mass. The specs list the total wing weight at
4.9kg, but the canopy upper/lower/rib materials only account for 2.95kg. My
mass calculations neglect the extra mass due to things like the lines, riser
straps, carabiners, internal v-ribs, horizontal straps, tension rods, etc, so
I'm underestimating that mass, but I'm also assuming the vertical ribs are
solid (no ports) so that makes up for a bit of the missing mass]]


Suspension lines
----------------

The second component model of the paraglider system is for the :ref:`suspension
lines <paraglider_components:Suspension lines>`. It is responsible for
positioning the payload, adjusting the position as a function of the
accelerator input, computing the trailing edge deflection angles, and
estimating the aerodynamic drag of the lines.

.. FIXME: I'm okay neglecting the weight of the lines?


Riser position
^^^^^^^^^^^^^^

.. Design variables: kappa_x, kappa_z, kappa_A, kappa_C, kappa_a

[[This demonstration uses the simplified line geometry model. Instead of
modeling the complete set of lines, it focuses on producing the effects of the
lines with as few parameters as possible.]]

.. kappa_A and kappa_C

* FIXME: how should I estimate :math:`\kappa_A` and :math:`\kappa_C`? Guess
  them from the line layout diagram from the user manual, or measure the
  physical wing?



.. kappa_x

* Line lengths from pg8 of the Hook 3 technical specifications:

  Neglecting the riser length of `0.470m`, the total lengths of the lines from
  the risers to the tabs:

  .. code-block::

    2A1   = 3.994
    A1    = 1.958
    a1    = 0.361
    Total = 6.313

    2C1   = 4.720
    C1    = 1.253
    c1    = 0.308
    Total = 6.281

  If you neglected the differences in the cascades for the As and Cs, the
  riser should be virtually centered between the two, which would mean if
  `kappa_A = 0.11` and `kappa_C = 0.59` then `kappa_x = 0.35`. However, the Cs
  first cascade is higher, thus larger angles, so the total length of the Cs
  will be "too long" (the more you deviate from a straight line, the longer
  the length to reach the destination).

  A few crude guesses suggest the `kappa_x = 0.5` isn't terrible.

  Using the lengths of the As and Cs is difficult, because `kappa_x` is very
  sensitive to small differences. For the Hook3, if they were the same length
  then `kappa_x = 0.35`, but if `kappa_x = 0.5` (a large difference in
  horizontal position) then the `C = 0.9898 * A`: scarcely more than 1%
  difference!

  Is using the nominal glide speed a better measure? I wonder how much
  `kappa_x/kappa_z` affects stability... Is `kappa_x` important?

  Maybe tune `kappa_x` to maximize the glide ratio? That happens at `kappa_x
  = 0.5c`. Of course it's common for the optimum glide ratio to occur when
  speedbar is applied, but whatever. Let's assume this wing was optimized for
  best glide at trim.


.. kappa_z

* FIXME: I think :math:`\kappa_z` is the "Central line length" from the specs
  (normalized by the root chord, IIRC), but what about :math:`\kappa_x`?
  I think I guessed that based on the maximum speed on the polar


.. kappa_a

[[From the specs, the accelerator line length :math:`\kappa_a = 0.15`]]


Brakes
^^^^^^

.. Design variables: s_delta_start0/1, s_delta_stop0/1, kappa_b

[[Tricky to explain how to define `kappa_b` since it depends on the set of
profiles, the chord distribution, and the brake deflection distribution. Refer
to `SimpleLineGeometry.maximize_kappa_b`]]


.. Deflection angle distribution and braking profiles

   Design variables: s_delta_start0/1, s_delta_stop0/1

   Keep this discussion after `kappa_b` since the stop variables should match
   when the maximum supported deflection occurs.

**Estimating start/stop positions**

The true deflection angle distribution depends on the complete physical
line geometry (line lengths and cascade angles, but since the simple model
does not include those the deflection angles must be assumed/guessed.

[[Estimate the parameters of the quartic model in
:ref:`paraglider_components:Brakes` by looking at a rear-view photo of
a wing.]]

.. figure:: figures/paraglider/demonstration/Hook3_rear_view.jpg
   :name: Hook3_rear_view

   Rear-view of an inflated Hook 3 with symmetric brake deflections

[[From this picture you can see that the brake deflection doesn't start until
some distance from the root. The brake lines are hard to see, but their
deflections are intuitive. The result is that instead of using a true line
geometry, you can get away with an approximate deflection distribution using
a simple cubic function with a few carefully chosen end points.]]

[[This method is admittedly weak. Probably not a major problem in practice,
but call it out when discussing reasons why I'm not comparing this to actual
flight data (goes together with the other uncertainties, like unknown
airfoil).]]

.. figure:: figures/paraglider/demonstration/Hook3_TE_0.25_0.50.*

   Quartic brake deflections, :math:`\delta_{bl} = 0.25` and :math:`\delta_{br}
   = 0.5`

.. raw:: html or singlehtml

   <br/>

.. figure:: figures/paraglider/demonstration/Hook3_TE_1.00_1.00.*

   Quartic brake deflections, :math:`\delta_{bl} = 1.00` and
   :math:`\delta_{br} = 1.0`


[[FIXME: explain how I generated some VERY idealized deformed profiles to
implement deflected trailing edges]]

[[FIXME: explain using XFOIL to get the section coefficients.]]


Line drag
^^^^^^^^^

.. Design variables: total line length, line diameter, r_L2LE (lumped
   positions for the line surface area), and Cd_lines

* FIXME: how should I specify the total line length and lumped position for
  the line drag? I really hate `r_L2LE`; should it just assume two points at
  `<0.5c, +/- 0.25 b/2, 0.25 z_RM>`? I haven't assigned these proper variable
  names yet; leave it that way?

  Also, the line drag coefficient assumes the lines are the same diameter
  everywhere, which is clearly wrong. The lines getter smaller as you go up
  the cascade.


Payload
-------

.. Total payload mass, spherical radius, drag coefficient, etc

   Design variables: m_p, z_riser, S_p, C_d,p, kappa_w

The second component model of the paraglider system is for the :ref:`harness
<paraglider_components:Harness>`. This component is responsible for [[...]].

The manual for the size 23 wing specifies a maximum in-flight weight limit of
85kg, and the (true) solid mass of the physical wing is 4.9kg, so a 75kg
payload is reasonable. To choose the projected area and drag coefficient,
[[consider]] :cite:`benedetti2012ParaglidersFlightDynamics` (p. 85) or
:cite:`babinsky1999AerodynamicPerformanceParagliders` (p. 422); given that 75kg
is a lower-than-average payload (so smaller frontal area), and that this is
a beginner-grade wing (so a more aerodynamic "pod" harness is less likely),
a reasonable guess of the projected area would be :math:`S_\textrm{payload}
= 0.55 \left[\textrm{m}^2\right]` with an drag coefficient of
:math:`C_{d,\textrm{payload}} = 0.8`. At that size the payload mass centroid
should be approximately 0.5m below the risers (especially since the uniform
density assumption neglects that the legs shift the center of mass below the
volume centroid).

.. Regarding the center of mass position, the DHV air worthiness guide p.9 says
   the harness riser attachment points must be "between 35 to 65cm above the
   seat board and must be separated from each other by 35cm to 55cm".

   The `para-test.com` (p.22 in `HOOK3_MANUAL_ENG.pdf` lists the "harness to
   risers distance" as 49cm for all wings, so that's another good source.


Model validation
================

.. How accurate is the model? This section involves **expected** outcomes,
   which means we already know what we expect to see. Validation is about
   *confirming*, not *learning*.

   Geometry expectations: does the geometry accurately predict specifcations
   that were not explicitly included in the model? Flattened and projected
   area, span, and aspect ratio; total mass; etc. (Hm, I think that's better to
   consider when defining the model. It's what you'd check when deciding if you
   can "stop" tweaking.)

   Behavior expectations: polar plots, 360 turn radius, 360 sink rate, etc.
   These tend to fall into static and dynamic behaviors; it's not essential to
   declare them that way, but it might be useful for thinking of behaviors.

   For dynamic behavior discussion points, see
   :cite:`wild2009AirworthinessRequirementsHanggliders` Sec:4.1 (pg28) for the
   DHV maneuvers for wing classification. Also,
   :cite:`lingard1995RamairParachuteDesign` Sec:7 and Sec:8.


[[Work in progress:

Validating the model is difficult for several reasons:

* Unlike the ``case study``, wind tunnel measurements are unavailable.

* There are more components, and their connections.

* Dynamic behavior is significantly more complex than static behavior

* more?

]]


Polar curve
-----------

.. Plot and discuss the predicted polar curve.

   Use this section to really highlight the limitations/assumptions of the
   model? Unknown airfoil, unknown true line positions, lack of a proper
   `LineGeometry` (so brake deflections and arc changes when accelerator is
   applied are both unknown), no cell billowing, etc etc. Seems like a good
   place to point out "this is overestimating lift and underestimating drag, as
   expected."


.. Equilibrium states

* [[FIXME: define *equilibrium state*]]

* [[FIXME: consider the zero input condition, and discuss how allowing the
  payload to pitch changes the result. (The 6a has a smaller theta_b2e and
  a positive theta_p2e (since b2e==p2e for 6a), whereas 9a has a larger b2e and
  negative p2e.) A plot isn't worth it since the angles are so small, so maybe
  just list the angles.]]


.. Polar curves

* [[FIXME: define *polar curve*. Explain how they summarize the equilibrium
  states over a range of accelerator and symmetric brake inputs.]]

* [[FIXME: add figure for polar curves. For which size and pod type? **Probably
  choose configurations that I'll be analyzing**; not much point showing
  multiple polars if some don't have data.]]

* [[FIXME: Discuss the zero input states ("trim").]]

* [[Discuss the range of control inputs.

  For the brakes, I'm only modeling 43cm of brake travel; that's not a ton.

  For the accelerator, I'm guessing at :math:`\kappa_A` and :math:`\kappa_C`.
  The design is pretty sensitive to those.


.. I don't have access to full polar curves, but I do have point estimates from
   certification and wing review flights.


[[Size 25 test from `Hook 3 Parapente Mag 148.pdf`]]

.. figure:: figures/paraglider/demonstration/polar_25.svg

* My horizontal speed at trim is about 0.35 m/s slower than theirs.



[[Size 27 test from `hook 3 perfils.pdf`]]

.. figure:: figures/paraglider/demonstration/polar_27.svg


* My horizontal speed at trim is about 0.35 m/s slower than theirs.

* They list min sink as occurring with 50% brakes. Given that `kappa_b
  = 0.46` for the size=27 model, 50% of 60cm corresponds to `delta_a = 0.65`,
  but for the size=27 model the min sink occurs closer to `delta_a = 0.2`.
  **Assuming everything else is fine** that would suggest my brake model is
  wrong? Like, the L/D ratio dies off too fast for my model? (Of course, can
  I trust them that such a convenient value of brakes produces min sink?)

* Cool, they claim max glide is at 0% brakes! Confirms my choice for
  `kappa_x` if it's true. As good as any justification, I guess.

* Their best glide with a pod harness is 9.5: for my model with `S=0.6, CD=0.4`
  I get 9.68? Verify.


* Extra data from the certification test `2013-01-23_hook3_23_en`:

  * FIXME: what size and pod type?

  * List the minimum speed as `<25km/h` (`6.94m/s`)

  * List the sink rate after to sharply banked turns as `>14m/s`. My model
    doesn't have enough control authority to get CLOSE to that.

  * Symmetric control travel `>60cm` (my model size=23 only supports `kappa_b
    = 0.43m` due to the limitations of the aerodynamic coefficient data)

    That means I'm modeling <72% of the travel they got during the test. No
    wonder their "steeply banked turn" is so much more extreme than I can
    produce. What would my polar look like if you extrapolated it that far?


Discussion:

* For the riser midpoint, I assume `kappa_z` is just the "height", and that
  `kappa_x` was chosen such that best glide is at trim.

* My model relies on section coefficients, but I don't have coefficient data
  from extreme trailing edge deflections, so I can only model roughly the first
  70% of the brake range. That's one factor why my minimum speeds are too high.

  The value of `kappa_b` depends on the glider since it's normalized by the
  chord lengths, but for the 25 `kapa_b = 0.444` and for the 27 `kappa_b
  = 0.463`.



Steady-state turn
-----------------

* Apply 100% brake and observe steady-state radius, turn rate, and bank angle

  Compare to the sink rates during a hard turn in the DHV ratings guide; are
  they "within spec"? Does the DHV guide define "hard turn"? I'm restricting
  the amount of brake input; probably can't reach a "hard" turn.

  I could try to justify this by arguing that "hard turns aren't part of
  typical flight conditions", but really the issue is about accuracy for
  a given brake input.

* In `2013-01-23_hook3_23_en` they have the sink rate after two "steeply
  banked" turns is `>14m/s`. For my model, full brakes and weight shift only
  get it to `1.397m/s`. Wow, optimistic much? I wish I knew what bank angle
  they considered "steep". Granted, I'm using VERY optimistic airfoil data and
  am SEVERELY limiting the brake travel (they say the symmetric control travel
  is `>60cm`, whereas I'm limited to `kappa_b = 0.43m`, so this model only
  covers <72% of the travel they used in their tests)


Impulsive controls
------------------

* Control input impulses (on/off of symmetric brake, asymmetric brake,
  accelerator, weight shift). See the DHV certifications for guidelines.


Exiting accelerated flight
--------------------------

According to Sec:4.5.1 of the DHV ratings guide, it sounds like wings dive
**forward** when the accelerator is abruptly released. For my current
Hook3ish, rapidly letting off the accelerator produces a ~20deg positive pitch
(**backwards**), not forwards. Sure, after pitching backwards it then pitches
forwards to `-7°`, but still, odd. Related: `2013-01-23_hook3_23_en` says the
wing pitches forward less than `30°` upon exiting accelerated flight, which
I guess agrees with my model.

Is this because I'm neglecting changes to the canopy geometry? Or is it
symptomatic of the fact that I assume the lines stay taught? Conceptually,
when you quickly release the speedbar, the A lines will quickly extend; it
takes some time for the harness to drop (or the wing to rise) enough to regain
tension, so the wing is certainly going to behave in ways not modeled by my
equations. Good to point out.


Model investigation
===================

.. Validation was about CONFIRMATION; this section is about LEARNING. What can
   we learn by playing with the model?

   This section is the payoff for the paper! In the introduction to the paper
   I argued that dynamic simulations let you study the behavior of a system.
   Having concluded the model is usably accurate, this is where I show off what
   it can do.

[[Run interesting scenarios and consider the observed behavior. Useful to
discuss both the behavior of the (true) physical system and the model.]]


Apparent mass
-------------

Compare the real versus apparent mass matrices.

Under what conditions? It depends on the current velocity. Maybe compare the
real mass, apparent mass at hands-up equilibrium, apparent mass during a turn,
etc. The point is to **highlight the magnitude of the effect**.

Consider the relative magnitudes and the likely effects from accounting for
apparent inertia. Then show some scenarios where the effects are significant
(figure-8s) and highlight the magnitude of the effect.


Steep turn
----------

In `2013-01-23_hook3_23_en` they list the sink rate after two "steeply banked"
turns as `>14m/s` (31mph!). For my model, full brakes and weight shift only get
it to down to `1.42m/s`. Wow, optimistic much? Granted, I'm severely limiting
the brake travel and am using VERY optimistic airfoil data, but still. **Do
they define "steep"?**

Ah, they rate it as class B, which agrees with sections 4.1.8 and 4.1.9 of the
DHV standard :cite:`wild2009AirworthinessRequirementsHanggliders`, pg31. The
DHV say "steepest possible **spiral** dive achievable in two turns". They also
specify "no counter-turn".

Well, observe that I'm only able to achieve a 20° bank angle; that's NOTHING
compared to a "hard spiral dive" you'd see in an SIV. I wonder which component
model is the limiting factor?

Geeze, later in "Behavior exiting a steep spiral" they recorded a `19m/s` sink
rate for the 85kg! Clearly I am unable to model a spiral.


Off-center thermal interaction
------------------------------

**This was a major goal of my work.** It's one of the major reasons I insisted
on the aerodynamics supporting non-uniform wind fields.

* Bonus: how does geometric torsion affect the off-center thermal scenario?


Discussion
==========

* This chapter suggests a workflow:

  1. Fit the flattened chord surface (`c(s)`, `x(s)`, `r_x(s)`)

  2. Fit the arc (`yz(s), r_yz(s)`)

  3. Apply geometric twist (`theta(s)`)

  4. Specify section profiles (airfoils) and their coefficients

     [[Indexed profile sets; discuss coefficient tables?]]

  5. Specify material densities (upper, lower, ribs) for computing the inertia

  6. Specify a suspension line model (harness position, accelerator function,
     brake deflection distribution, line drag)

     (includes an initial guess for :math:`kappa_x`

  7. Specify a harness model

  8. Specify a system model (connection parameters, if applicable)

  9. Adjust `kappa_x` until maximum glide is at zero controls


* Everything related to the airfoils is sketchy. The choice of airfoil,
  modeling their deflected geometries, modeling the deflection distribution,
  etc. Tons of uncertainty here. Just stick a big red flag in it and say "hey,
  if you want to solve this problem, here's a big sticking point."

* This chapter focuses on collecting the necessary information to produce the
  model. For the actual implementation, refer to ``glidersim``:

  * :external+glidersim:py:func:`pfh.glidersim.extras.wings.niviuk_hook3`

  * https://github.com/pfheatwole/glidersim/blob/main/scripts/build_hook3.py
