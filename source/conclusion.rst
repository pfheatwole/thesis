**********
Conclusion
**********

.. "The conclusion interprets the results to answer the question that we posted
   at the end of the context section."

   Assume an impatient reader will jump here. This is your last chance to
   convince them the paper is worth reading.


Results
=======

.. This section is one of payoffs for the paper! Until now I was developing the
   model, showing how to construct them, and validating the results. This is
   where I get to show some applications. (Granted, estimating the polar curve
   is a good application already.) In the introduction I claimed that one of
   the applications of dynamic simulations is to study the behavior of
   a system.

.. What was done? Summarize the work and its key outcomes.

This project completed the set of tasks outline in its
:ref:`introduction:Roadmap`:

1. It developed a novel :doc:`foil_geometry` specifically to enable simple
   representations of paraglider canopies.

2. It selected, implemented and :ref:`validated <validation:Foil aerodynamics>`
   a fast-but-accurate theoretical aerodynamics model well-suited to the
   nonlinear geometries and challenging flow conditions of paraglider canopies,
   as outlined in the :ref:`introduction:Modeling requirements` defined at the
   beginning of the project.

3. It developed :doc:`parametric models <paraglider_components>` to estimate
   the inertial properties and resultant forces of the components of
   a paraglider.

4. It used the parametric components to :doc:`demonstrate <demonstration>` how
   to produce a complete flight dynamics model of a commercial paraglider wing
   using only limited technical data, photos, and video of the wing.

5. It :ref:`validated <validation:Niviuk Hook 3 system dynamics>` the
   longitudinal performance of the demonstration model against basic flight
   test data, as well as highlighted some areas in which the accuracy of flight
   dynamics could be improved.

This final section of the paper will address the last of the
:ref:`introduction:Modeling requirements`: it will revisit the set of
:ref:`motivating questions <Questions>` that helped guide the design process,
and consider the ability of these models to answer them.


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

.. raw:: html or singlehtml

   <br/>

.. figure:: figures/paraglider/demonstration/figure8_Reynolds.*
   :name: figure8_Reynolds

   Figure-8 when neglecting accurate Reynolds numbers

.. raw:: html or singlehtml

   <br/>

.. figure:: figures/paraglider/demonstration/figure8_Reynolds_and_apparent_mass.*
   :name: figure8_Reynolds_and_apparent_mass

   Figure-8 neglecting both apparent mass and accurate Reynolds numbers

.. raw:: html or singlehtml

   <br/>

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

A reliable way to start a lively discussion on a paragliding forum is to
question what happens when a wing encounters a thermal on only one side of its
wing. Some pilots will argue that the thermal will pull the wing in; other
pilots will argue that the thermal will push the wing away. A grand desire of
this project was that the resulting flight dynamics model might be able to shed
light on why two seasoned pilots might hold such opposing views.

This final study used the Niviuk Hook 3 size 23 components from the
:doc:`demonstration` with a 6-DoF system dynamics model. The scenario is
simple: place a thermal slightly off-center of the path of a paraglider flying
straight forward at equilibrium with symmetric brakes. Because the span of the
wing is only :math:`8.84 \, [m]`, the thermal was placed :math:`15 \, [m]` to
the right with exponential falloff such that the thermal strength was reduced
to 5% by the time it reached the center of the canopy with a peak (core)
strength of :math:`3 \, [\frac{m}{s}]` (extremely strong for such a tight
thermal). The effect of the exponential falloff was a peak gradient of
:math:`0.67 \, [\frac{m}{s}]` from the wingtip nearest the thermal to the
center of the canopy as the glider passed the core.

.. figure:: figures/paraglider/demonstration/indirect_thermal.*

   Indirect thermal interaction.

   The first row represents the Euler angles for position, the second row
   represents the angular velocities, and the third row is the angular
   accelerations.

These results can be viewed in two ways: quantitatively and qualitatively. From
a quantitative perspective the results are disappointing: the absolute angular
deviations were on the order of 1°, which seem impossibly small for pilots to
argue over. From a qualitative perspective, however, the results are perhaps
more interesting. As the wing passes the thermal, the canopy initially rolls to
the right (into the thermal), pitches forward (into the thermal), and the
adverse yaw twists the wing to the left (away from the thermal); although the
angular deviations are tiny it may produce an effect similar to falling, which
needs only a small distance to produce a striking sensation. The same logic
applies after the initial response, where the accelerates again, but more
rapidly, and in the opposite direction: now the wing is rolling away from the
thermal while yawing into it. Perhaps the sensation of acceleration holds the
key to the argument: whether a pilot is more sensitive to roll or yaw, and
whether they're more sensitive to the initial or secondary accelerations may
offer a partial explanation?

Personally I find this argument unconvincing. Despite the potential explanation
offered by the qualitative analysis, it seems much more likely that the model
has failed to capture one or more of the significant dynamics of the system.
One possible cause is the foil aerodynamics model, which is not intended to
capture unsteady aerodynamics; despite its accuracy in the wind tunnel testing,
it may be inadequate for this level of subtlety in dynamic scenarios. Another
possible cause is the quasi-rigid-body assumption imposed on the canopy
geometry; real wings would flex and distort, especially in such a strong
thermal, and it seems like that such deformations may play a larger roll that
anticipated.

All in all, despite the underwhelming results the truth is this was always an
ambitious goal, and I hope it demonstrates the theoretical advantages of
pursuing flight dynamics models that are capable of capturing the effects of
non-uniform wind vectors along the span of the wing, and will serve as
a starting point for some future work. Perhaps we will someday have an answer
for the forums.


Future work
===========


Canopy
------

* Arc deformations: the :ref:`design curves <foil_geometry:Summary>` that
  define the foil geometry are not required to be constant functions; they can
  be functions of control inputs, such as weight shift. The primary difficulty
  is that the current implementation of the :ref:`NLLT
  <foil_aerodynamics:Phillips' numerical lifting-line>` assumes that the shape
  of the canopy is constant, but that a practical limitation, not a theoretical
  one.

.. _Weight_shift_modeling:

* Weight shift modeling: the :ref:`validation:Steady-state turn` sanity check
  of the demonstration model suggests that lateral movement of the mass
  centroid is not the primary control mechanism for weight shift control. The
  alternative mechanism is the wing deformations that occur during weight
  shift. At the outset of this project the assumption was that the canopy
  deformations during weight shift would be negligible compared to the
  displacement of payload mass, but the turn radius and sink rate suggest
  otherwise. It may be fruitful to generate plausible :math:`yz(s, \delta_w)`
  design curves (so the foil arc deforms as a function of weight shift), and
  consider if the changes to the canopy aerodynamics would explain the
  inaccuracies in the rigid canopy model. If canopy arc deflections prove to be
  a significant factor for accurate weight shift predictions, they should
  probably be implemented as an interaction between :math:`yz(s)` and the
  suspension line model. (Paraglider pilots quickly discover the relationship
  between chest riser strap width and weight shift control, which strongly
  suggests that the lines play a dominant role).

* Choice of airfoil: the :doc:`demonstration` chose the NACA 24018 as an
  example of a conservative guess, but if a few commercial section profiles
  were measured accurately (including their spanwise variation), all models of
  commercial paraglider wings would benefit.

* Deflected profiles: the demonstration used section :ref:`Profiles` produced
  by a "two circle" model of trailing edge deflection. That optimistic model
  was designed to balance the accuracy of profile deformation against the
  ability to estimate the aerodynamic coefficients with XFOIL. In reality,
  their unnaturally smooth curvature likely causes them to underestimate flow
  separation. Future work would benefit from more accurate deflection profiles.

* Aerodynamic coefficients: in conjunction with more accurate deflection
  profiles, another improvement would be is to use more sophisticated methods
  to estimate the aerodynamic coefficients. One option is RFOIL from Delft
  University of Technology (a fork of XFOIL that is reported to improve
  estimates, particularly at high angles of attack), or to apply a complete
  computational fluid dynamics approach with OpenFoam.


Lines
-----

* The parameters for the :ref:`brakes <paraglider_components:Brakes>` are
  confusing at first glance, and tedious to tune. At the least they would
  benefit from an automated procedure where instead of having to tune
  :math:`s_\textrm{start,1}` and :math:`s_\textrm{stop,1}` to match
  :math:`\kappa_b` (which was in turn limited by the
  :math:`\bar{\delta_d}_\textrm{max}` supported by the aerodynamic coefficient
  set). It would be much easier to define :math:`s_\textrm{start,1}` and
  :math:`s_\textrm{stop,1}` at some hypothetical value of :math:`\kappa_b` and
  have the lines adjust their values based on the true :math:`\kappa_b`.


Harness
-------

* The :ref:`spherical model <paraglider_components:Harness>` neglects pitch and
  yaw moments due to angle of attack and sideslip, but because paragliders put
  their legs out in front those effects seem likely.

* The harness model uses constant drag coefficients.
  :cite:`kulhanek2019IdentificationDegradationAerodynamic` developed a model
  for the harness that accounts for Reynolds numbers, but that model was not
  tested in this work.


System dynamics
---------------

* This paper derived a :ref:`9-DoF <derivations:Model 9a>` system dynamics
  model that modeled the connection between the lines and payload as
  a spring-damper system, but without flight testing the parameters were
  difficult to estimate. It would be interesting to review the applicability of
  the spring-damper model and to estimate suitable parameters. I suspect that
  the lack of canopy deformations and the inability of the 6-DoF to show
  payload-relative roll are at least partial explanation of the underwhelming
  results of the `indirect thermal study <Study: indirect thermal
  interaction>`_. The sensation of payload-relative roll and yaw accelerations
  could definitely play a role in why pilots disagree on the behavior of
  a paraglider encountering a thermal.


Open source
===========

The `materials <https://github.com/pfheatwole/thesis/>`__ to produce this paper
and its `implementation <https://github.com/pfheatwole/glidersim/>`__
:cite:`heatwolev2022.03.0aGlidersim` are both available under permissive open
source licenses. Although this work focused on paragliders, the structure of
the models is mirrored in the structure of the code, and should be easily
adaptable to other gliding aircraft such as hang gliders or kites. For maximum
versatility and approachability, the entire implementation was built on the
Python scientific computing stack; despite not producing the fastest
implementation, Python made up for the performance cost with value in other
areas:

* Free (unlike MATLAB, AutoCAD, etc)

* Extensive cross-domain usage (aerospace, computer science, etc)

* Powerful scientific computing libraries (NumPy, SciPy, Numba)

* Easy to integrate into tools with native Python interpreters (such as
  FreeCAD, Blender, and QGIS)

I am grateful for the work freely shared by those who came before, and hope
that this material may provide some value to those who follow.
