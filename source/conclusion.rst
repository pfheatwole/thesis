**********
Conclusion
**********

.. What are the results of this project?

   Assume an impatient reader will jump here. This is your last chance to
   convince them the paper is worth reading.


Applications
============

[[Discuss how can people use these sorts of models: statistical filtering,
control modeling, and studying wing behavior. This section is one of payoffs
for the paper In the introduction to the paper I claimed that one of the
applications of dynamic simulations is to study the behavior of a system.
Having concluded the model is usably accurate, demonstrate how the model can be
used to learn about the behavior of the physical system.]]


Study: drag breakdown
---------------------

A common question for curious pilots is how to reduce the drag of their glider
so they can improve the glide ratio or top speed of their wing. The natural
progression of this curiosity is wonder where all the drag comes from in the
first place. One way to answer that question is to plot the drag contributions
from each component :cite:`babinsky1999AerodynamicImprovementsParaglider`.

.. figure:: figures/paraglider/demonstration/drag_breakdown.*

   Drag breakdown for Niviuk Hook 3 23 with a pod harness.

Viscous drag includes effects such as the sheer forces produced by the
viscosity of the air, and the pressure drag due to flow separation (the
"vacuum" that can occur on the downwind side of an object); these forms of drag
occur on every surface of the glider, including the lines and payload. Inviscid
drag is less intuitive: commonly referred to as "lift-induced drag", it is the
energy lost in the vorticity that the wing sheds into its wake as a side-effect
of producing lift.

This diagram provides a satisfying look into the behavior of a wing across the
range of speeds. At the low end, pilots understand that the "brakes" will slow
the wing by increasing its drag, but may be surprised to discover that the
increase in drag is dominated by how the wing produces lift. At the high end,
it can be surprising to learn what proportion of the total system drag is
produced by the seemingly-negligible suspension lines. Although drag is just
one piece of the lift/drag ratio, this sort of breakdown is valuable for
estimating how much improvement is possible by (for example) reducing the drag
of the payload.

This decomposition is also educational because it offers another perspective of
how each component of the wing affects the overall design. Consider the general
guideline that paraglider wings are designed to achieve their maximum glide
ratio at "trim" (zero controls), which usually coincides with the speed that
minimizes the total system drag (as seen here). Now suppose the design was
changed; for example, increasing the aspect ratio of the canopy will tend to
decrease its lift-induced drag, which in turn requires repositioning the
payload at trim. The complete system behavior is a complex interaction of
components, and having access to a parametric model such as this is an
excellent resource for quickly answering questions about glider efficiency by
developing an intuition of how their interactions affect the system behavior.


.. This diagram can also provide a useful to "sanity check".

   Compare the model to known results, such as
   :cite:`babinsky1999AerodynamicImprovementsParaglider`.

   * Accuracy of the :ref:`section profiles <Profiles>`

   * Accuracy of the 2D aerodynamic coefficients (XFOIL tends to overestimate
     CL and underestimate CD)

   Then again, are these really THAT different from the accuracy limitations of
   the 3D aerodynamics? Spanwise-flow violate the assumptions of the 2D
   coefficients, surface imperfections, etc. At maximum braking you'd expect
   the foil distortions (creasing, etc) to have a significant impact for a real
   wing. At high speed I'm ignoring deformations to the air intakes [[]]



Study: effects of Reynolds numbers and apparent mass
----------------------------------------------------

There were two questions at the start of this project that affected my modeling
choices:

1. How significant are the effects of apparent mass?

2. How significant are the effects of accurate Reynolds numbers?

.. Sidenote: :cite:`babinsky1999AerodynamicPerformanceParagliders` shows the 3D
   lift coefficient, but not an indepth study

Both contributions to the flight dynamics are typically neglected in paraglider
dynamics models without clear justification or discussion of their expected
impact on model accuracy. The models developed in this paper can be used to
provide insight on those questions. Using the Niviuk Hook 3 (size 23) component
models created for the :doc:`demonstration`, a programming script created
multiple instances of the 6-DoF system models, configuring them to either
respect or ignore the effects of apparent mass and precise Reynolds numbers
(which are normally computed dynamically for each wing section). Pairs of
models — one with the full dynamics and the other lacking one or both effects
— are put into a figure-8 maneuver starting at that model's equilibrium state
and receiving the same control inputs over a span of 60 seconds. (The maneuver
did not use weight shift control to avoid possible issues modeling canopy
deformations.) Three simulations were run:

1. To show the affect of neglecting apparent mass
   (:numref:`figure8_apparent_mass`)

2. To show the effect of neglecting accurate Reynolds numbers by using
   a constant :math:`Re = 2 \times 10^6` (:numref:`figure8_Reynolds`)

3. To show the combined effect of neglecting both apparent mass and accurate
   Reynolds values (:numref:`figure8_Reynolds_and_apparent_mass`)

.. figure:: figures/paraglider/demonstration/figure8_apparent_mass.*
   :name: figure8_apparent_mass

   Figure-8 when neglecting apparent mass

.. figure:: figures/paraglider/demonstration/figure8_Reynolds.*
   :name: figure8_Reynolds

   Figure-8 when neglecting accurate Reynolds numbers

.. figure:: figures/paraglider/demonstration/figure8_Reynolds_and_apparent_mass.*
   :name: figure8_Reynolds_and_apparent_mass

   Figure-8 neglecting both apparent mass and accurate Reynolds numbers

.. figure:: figures/paraglider/demonstration/figure8_Reynolds_and_apparent_mass_topdown.*
   :name: figure8_Reynolds_and_apparent_mass_topdown

   Figure-8 neglecting both apparent mass and accurate Reynolds numbers,
   topdown view

The differences produced by each simplification are similar in this case, and
will be discussed jointly. First, the less noticeable difference between the
two simulations in :numref:`figure8_Reynolds_and_apparent_mass` is the total
altitude loss, where the "fixed Reynolds, no apparent mass" model descended an
extra 2 meters. The difference is not visually interesting so no side-view is
shown, but the effect is worth noting and should be expected for two reasons:

1. There is minimal acceleration in the :math:`z`-direction so the
   :math:`z`-component of the apparent mass is negligible.

2. The sections most impacted by the incorrect Reynolds values are at the
   outside of the span. Since the majority of the lift is produced by the
   central sections, which are already near the :math:`Re = 2 \times 10^6`
   value, total lift is not greatly affected by assuming a fixed value of
   :math:`Re`.

The more significant effect was on the lateral motion of the glider, which is
easier to see from a top-down perspective
(:numref:`figure8_Reynolds_and_apparent_mass_topdown`), where the complete
model exhibited a turn radius of :math:`54 \, [m]` versus :math:`51 \, [m]` of
the simplified model. (The cumulative horizontal distances traveled were
:math:`522 \, [m]` at :math:`8.7 \, \left[\frac{m}{s}\right]` and :math:`532 \,
[m]` at :math:`8.87 \, \left[\frac{m}{s}\right]`, respectively.) Again, the
effect is expected for two reasons:

1. Apparent mass resists changes to the translational velocity, which reduced
   the complete models centripetal acceleration and prevented it from producing
   as narrow a turn as the simplified model.

2. Lower Reynolds values resulted in lower lift coefficients, especially for
   sections with deflected trailing edges (since their increased curvature
   magnifies the viscous effects). The lift vectors of sections on the inside
   semispan are angled into the turn and pull the canopy into the circle, so
   reducing their lift contributions further reduced the complete models
   centripetal acceleration.

Because these affects are heavily dependent on the glider design and specific
flight maneuvers, this discussion focused on the qualitative nature of these
effects. Whether these sources of error are significant depend heavily on the
model (the canopy geometry in particular, as well as target airspeed of the
glider) and its application. For example, when developing a linearized model to
generate an error term for a control model these effects can be safely
neglected, but any long-run simulation should review their specific control
sequence (because turning magnifies their impact). With this model, checking
the impact of such choices is readily available.


Study: indirect thermal interactions
------------------------------------

.. figure:: figures/paraglider/demonstration/indirect_thermal.*

   Indirect thermal interaction.

[[FIXME: explain. The wing is flying straight at equilibrium, when it enters
a thermal 15 meters to its right. The thermal strength has a squared distance
decay to 5% by the time it :math:`y = 0`, so only the right side of the wing
experiences a significant change to lift.  Etc etc.]]

[[Inconclusive results; discuss that in `Future work`_.]]
