.. This chapter validates [[...]].

   The simulations perform static and dynamic performance tests (polar plots
   and flight maneuvers, respectively) and compare them to expected behaviors.


Validation
==========

.. Present results that validate the models.

   1. Create the Belloc canopy geometry and compare the wind tunnel data to
      simulated results.

      Provide tables that demonstrate that the NLLT performs as well or better
      than the VLM models. Add percent error when possible.

   2. Compare the Hook 3 polar curve data to simulated results

      Provide tables that show the percent error between the simulated and
      measured results.


Foil aerodynamics
-----------------

.. This section performs two things:

   1. Constructs a model of the foil geometry

   2. Compares the NLLT estimates to the wind tunnel measurements

   It accomplishes:

   1. The foil geometry is easy to use

   2. The foil geometry implementation is correct

   3. The NLLT appears to be working correctly

   4. The NLLT appears to be a good choice for modeling a paraglider in static,
      uniform-flow conditions


.. Validate the performance of Phillips' method for analyzing a parafoil canopy
   in steady-state conditions.

The :doc:`foil_aerodynamics` chapter selected Phillips' NLLT because it
appeared to satisfy the :ref:`introduction:Modeling requirements` established
at the beginning of this paper; this section uses wind tunnel measurements to
validate that choice. First it recreates the geometry using the
:ref:`foil_geometry:Simplified model`, then it recreates the range of test
conditions used by the experiment and tabulates the aerodynamic coefficients
estimated by the NLLT. The estimates are compared to the wind tunnel data, as
well as to other standard aerodynamic models commonly recommended for nonlinear
geometries.


Geometry
^^^^^^^^

.. Demonstrate and validate the foil geometry and aerodynamics using Belloc's
   reference wing. There are two points here:

   1. Show how easy it is to implement specs from actual papers

   2. Show the accuracy of the NLLT and its implementation (within the accuracy
      constraints of the section coefficient data)

The geometry from a 2015 parafoil wind tunnel test
:cite:`belloc2015WindTunnelInvestigation` makes an excellent case study of
a foil specification from literature that positions the sections using
alternative reference points on the section chords. Moreover, the geometry
satisfies the assumptions of the :ref:`foil_geometry:Simplified model`, making
an implementation of the geometry almost trivial.

First, the paper describes the geometry of the full-scale canopy they wish to
study:

.. list-table:: Full-scale wing dimensions
   :header-rows: 1

   * - Property
     - Value
     - Unit
   * - Arch height
     - 3.00
     - m
   * - Central chord
     - 2.80
     - m
   * - Projected area
     - 25.08
     - m\ :sup:`2`
   * - Projected span
     - 11.00
     - m
   * - Projected aspect ratio
     - 4.82
     - --
   * - Flat area
     - 28.56
     - m\ :sup:`2`
   * - Flat span
     - 13.64
     - m
   * - Flat aspect ratio
     - 6.52
     - --

For the wind tunnel test, a one-eighth scale physical model was constructed
from a wood-carbon frame with polyurethane foam sections covered in fiberglass.
Physical dimensions and positions were provided for the physical model as
pointwise data with linear interpolation between each point.

.. FIXME: Should I use these tables or just give the explicit equations?
   They're messy, but I do like the fact that they highlight the fact that you
   **can** use pointwise data in a linear interpolator just as easily.

.. csv-table:: Wind tunnel wing geometry data at panel’s ends
   :header: :math:`i`, :math:`y` [m], :math:`z` [m], :math:`c` [m], :math:`r_x`, :math:`r_{yz}`, :math:`\\theta` [deg]

   0, -0.688,  0.000, 0.107, 0.6, 0.6, 3
   1, -0.664, -0.097, 0.137, 0.6, 0.6, 3
   2, -0.595, -0.188, 0.198, 0.6, 0.6, 0
   3, -0.486, -0.265, 0.259, 0.6, 0.6, 0
   4, -0.344, -0.325, 0.308, 0.6, 0.6, 0
   5, -0.178, -0.362, 0.339, 0.6, 0.6, 0
   6,  0.000, -0.375, 0.350, 0.6, 0.6, 0
   7,  0.178, -0.362, 0.339, 0.6, 0.6, 0
   8,  0.344, -0.325, 0.308, 0.6, 0.6, 0
   9,  0.486, -0.265, 0.259, 0.6, 0.6, 0
   10, 0.595, -0.188, 0.198, 0.6, 0.6, 0
   11,  0.664, -0.097, 0.137, 0.6, 0.6, 3
   12,  0.688,  0.000, 0.107, 0.6, 0.6, 3

It is important to notice the difference between the section numbers :math:`i`
used in the paper and the section indices :math:`s` used in the simplified
model; the section indices are easily calculated using the normalized linear
distance along the :math:`\left< y, z \right>` points. Also, the reference data
is defined with the wing tips at :math:`z = 0`, whereas the convention of this
paper places the canopy origin at the leading edge of the central section; this
is easily accommodated by subtracting the central :math:`z = -0.375` from all
:math:`z`-coordinates. (Alternatively, the
:external+glidersim:py:class:`implementation
<pfh.glidersim.foil_layout.FoilLayout>` of the simplified model in
``glidersim`` can shift the origin automatically.)

.. figure:: figures/paraglider/geometry/airfoil/NACA-23015.*
   :name: airfoil_NACA_23015

   NACA 23015

Calculating the section indices for each point and using linear interpolation
as a function of the section index produces a set of piecewise-linear design
curves, and assigning every section a NACA
23015 airfoil (:numref:`airfoil_NACA_23015`) completes the foil geometry model.

.. raw:: latex

   \newpage

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_canopy_chords.*

   Chord surface for Belloc's reference paraglider wing.

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_canopy_airfoils.*

   Profile surface for Belloc's reference paraglider wing.

.. FIXME: compute the summary specs and compare; area, span, etc


Wind tunnel setup
^^^^^^^^^^^^^^^^^

.. Describe the test setup and the data

The setup mounted the 1/8-scale model on a 1 meter rod connected to force
sensors, and set the wind tunnel to a 40 m/s airspeed. Measurements were taken
with the angle of attack and sideslip ranging over :math:`-5 < \alpha < 22` and
:math:`-15 < \beta < 15` (a range suitable capturing longitudinal performance
post-stall). For better accuracy, wind tunnel measurements should be corrected
for wall interactions with the flow (:cite:`barlow1999LowSpeedWindTunnel`;
:cite:`drela2014FlightVehicleAerodynamics`, Sec. 10.3). However, because
classical wind tunnel wall corrections assume a flat wing, the data for the
arched parafoil are uncorrected for wall effects.


Aerodynamics models
^^^^^^^^^^^^^^^^^^^

The wind tunnel data will be compared to three theoretical aerodynamics models,
one that includes viscous effects, and two that do not (inviscid models):

1. NLLT: the :ref:`numerical lifting-line <foil_aerodynamics:Phillips'
   numerical lifting-line>` model from
   :cite:`phillips2000ModernAdaptationPrandtl`

2. `AVL <https://web.mit.edu/drela/Public/web/avl/>`__: an extended vortex
   lattice method by Mark Drela :cite:`drelaAthenaVortexLattice` (who also
   authored XFOIL :cite:`drela1989XFOILAnalysisDesign` while at MIT) . With
   a long history in academic research, this is the primary reference for
   comparing the results of the NLLT. 

3. `XFLR5 <https://www.xflr5.tech/xflr5.htm>`__: an experimental vortex lattice
   method from the open source wing modeling tool by André Deperrois. This
   model is marked "experimental" by the author because it is still under
   development, but the principle is to mitigate the "small angles"
   approximation relied on by standard vortex lattice methods by reorienting
   the foil geometry instead of reorienting the flow. The purpose of including
   this method in these tests is to show the effect of the simplifying
   assumptions used when designing the system of equations for aerodynamics
   models. For conventional aircraft where the flow angles are relatively
   small, small angle approximations are reasonable, but for nonlinear
   geometries at large angles of attack, classic methods such as AVL begin to
   struggle.


Results
^^^^^^^


Lift vs drag
""""""""""""

The standard way to summarize the efficiency of a wing is to plot the amount of
lift it produces versus the amount of drag; with practice, such charts can be
used to quickly approximate performance characteristics such as its glide
ratio. They are also useful for quickly comparing the relative performance of
each aerodynamics method.


.. Pseudo-inviscid results; requires setting `Cd = 0`

   Demonstrates how well the NLLT lift matches XLFR5's "Tilted Geometry" method
   over the lower range of alpha. Once alpha approaches stall, the NLLT
   diverges since it's not a true inviscid method; it's using the viscous lift
   coefficients to determine the circulation distribution.

.. figure:: figures/paraglider/belloc/NLLT/pseudoinviscid_CL_vs_CD.*
   :name: Belloc_CL_vs_CD_pseudoinviscid

   Lift vs induced drag

The first thing step during validation is to verify the test setup for each of
the models. One way to do that is by comparing methods that are expected to
produce equivalent results; in this case, the inviscid methods from AVL and
XFLR5 should be nearly identical at low angles of attack, and should estimate
zero drag at zero lift coefficient and zero sideslip. Because the NLLT uses
aerodynamic coefficients that include viscous effects it is not directly
comparable to the inviscid models, but because viscosity is not expected to
have a significant effect on lift at low angles of attack, it is possible to
disregard the viscous drag coefficients and plot the pseudo-inviscid polar
curve by setting the viscous drag coefficients to zero, as shown in
:numref:`Belloc_CL_vs_CD_pseudoinviscid`. (This is a "pseudo" inviscid curve
since the section lift coefficients used by the NLLT include viscous effects.)
The resulting drag coefficient is limited to drag produced by the creation of
lift, as would be predicted by the inviscid methods. This plot is useful
because it validates that the geometry model and test conditions were
configured correctly in all tools, and provides evidence that the NLLT was
implemented correctly.

.. figure:: figures/paraglider/belloc/NLLT/standard/CL_vs_CD.*
   :name: Belloc_CL_vs_CD

   Lift vs drag

The second plot (:numref:`Belloc_CL_vs_CD`) compares the inviscid methods to
the NLLT with the unadjusted aerodynamic coefficients from XFOIL. The first
thing to note is the difference compared to the pseudo-inviscid plot
(:numref:`Belloc_CL_vs_CD_pseudoinviscid`): as expected, including viscous drag
significantly improves the agreement between the theoretical and experimental
results for the NLLT. Another observation is the significance of the inviscid
assumption, with both inviscid methods overestimating lift and underestimating
drag at higher angles of attack. This plot also appears to show the effect of
the "small angles" approximation relied on by AVL, with the experimental
"tilted geometry" method from XFLR5 providing better accuracy at high angles of
attack and sideslip.


.. figure:: figures/paraglider/belloc/NLLT/Cd_surface_CL_vs_CD.*
   :name: Belloc_CL_vs_CD_surface

   Lift vs drag with extra viscous drag due to "surface characteristics"

A final plot (:numref:`Belloc_CL_vs_CD_surface`) is more for future reference
than validation. Instead of the unadjusted aerodynamic coefficients from XFOIL,
it adds the additional viscous drag due to "surface characteristics" suggested
in :cite:`ware1969WindtunnelInvestigationRamair` as a result of their wind
tunnel tests on parafoils. Because this empirical adjustment will be used in
the :doc:`demonstration` portion of this paper, this plot is useful to show the
expected accuracy of the NLLT when applied to a model of commercial paraglider
wing used for dynamic simulations.


Coefficients vs angle of attack
"""""""""""""""""""""""""""""""

Another valuable way to summarize wing behavior is to plot the
longitudinal-centric coefficients (lift, drag, and pitching moment) versus the
angle of attack :math:`\alpha`. These results are grouped into four quadrants
by the sideslip angle :math:`\beta` used during the test.

.. figure:: figures/paraglider/belloc/NLLT/standard/CL_vs_alpha.*
   :name: Belloc_CL_vs_alpha

   Lift coefficient vs angle of attack

The first (and arguably most interesting) plot is for lift versus angle of
attack (:numref:`Belloc_CL_vs_alpha`). Separating lift into its own plot
reveals the source of the flatline region in the "Lift vs drag" plots; the wing
enters stall (so lift ceases to grow) at approximately :math:`\alpha = 17°,
\beta = 0°`, and slightly earlier during sideslip (although the nonlinearity of
the geometry dramatically affects the stall pattern and "smooths" the effect
making it more difficult to see).

The more interesting result, however, is that all three theoretical methods are
in very close agreement for the majority of the range, they all mispredict the
zero-lift angle of attack, and they all uniformly overestimate the slope of the
lift curve. This anomaly is difficult to explain; at :math:`\beta = 0°` and low
angles of attack, the effects of viscosity should have a negligible effect on
lift, and the vortex lattice methods should perform very well, but they don't.
The fact that the NLLT agrees with them is encouraging (again, the fact that it
uses lift coefficients that account for viscosity should have a negligible
effect in this test, and so the NLLT is expected to agree with the inviscid
methods). I contacted the authors of both the wind tunnel data and the NLLT,
and neither author had any immediate feedback on what would cause this issue.
Nevertheless, there are two useful takeaways:

1. The NLLT is at least as accurate as the inviscid methods.

2. The NLLT is approximating the nonlinear effects of early stall, whereas the
   inviscid methods maintain a virtually linear response. This is an
   encouraging sign that the NLLT is a suitable choice given my
   :ref:`introduction:Modeling requirements` that the aerodynamics should
   provide "graceful degradation of accuracy" as it approaches high angles of
   attack.

This plot also highlights a limitation of relying on aerodynamic coefficients:
the NLLT cannot produce a solution if any of the sections experience
a section-local angle of attack that exceeds the range supported by the set of
aerodynamic coefficients. This is effect is clear as the sideslip angle
increases: because the wing is arched, as sideslip becomes positive (so the
relative wind approaches from the right of the wing) the angle of attack on the
left wingtip increases. As a result, as soon as global :math:`\alpha` and
:math:`\beta` produce a section-local :math:`\alpha` that exceeds the maximum
value in the coefficients lookup table, the NLLT cannot produce a solution. The
inviscid models, on the other hand, are founded on linear relationships with no
upper bound, allowing them to generate estimates at significantly higher angles
of attack and sideslip. Whether a bad estimate is better than no estimate,
however, depends on the application.


.. figure:: figures/paraglider/belloc/NLLT/standard/CD_vs_alpha.*
   :name: Belloc_CD_vs_alpha

   Drag coefficient vs angle of attack

When considering drag versus angle of attack (:numref:`Belloc_CD_vs_alpha`),
the most noteworthy details are how all three methods fail to predict the rapid
increase in drag as the wing enters the stall region, and how the "tilted
geometry" of the XFLR5 model allows it to more accurately track the shape (if
not the value) of the viscous solution.


.. figure:: figures/paraglider/belloc/NLLT/standard/Cm_vs_alpha.*
   :name: Belloc_Cm_vs_alpha

   Pitching coefficient vs angle of attack.

Another coefficient that has a strong impact on the pitch stability of
a paraglider canopy is the pitching moment versus angle of attack
(:numref:`Belloc_Cm_vs_alpha`). This plot can be viewed as pre- and post-stall
conditions (before and after :math:`\alpha = 17°` in the :math:`\beta = 0°`
quadrant), and are worth considering separately.

In the pre-stall region, the plot shows how a negative pitching moment grows
with :math:`\alpha`, resulting in negative feedback that provides a restoring
force back to equilibrium. If the wing pitches backwards, the negative pitching
moment will help bring the canopy back overhead into a stable position.

In the post-stall region, the effect of flow separation can be seen in the
experimental data by the sudden flat response of the pitching coefficient to
:math:`\alpha`. This reason is complex, but informative:

* Because the lift vector at positive :math:`\alpha` points forwards, lift
  creates a negative (forward) pitching moment. At stall, lift decreases, which
  increases :math:`C_m`.

* Because drag points backwards, it creates a positive (backwards) pitching
  moment. At stall, drag dramatically increases, which also increases
  :math:`C_m`.

* At stall, flow separation typically starts at the trailing edge on the upper
  surface. The loss of pressure creates a negative (forwards) pitching moment,
  which decreases :math:`C_m`.

For the wind tunnel model, it appears that (again, for the :math:`\beta = 0°`
case) these effects are counteracting each other, producing a relatively flat
:math:`C_m` in the post-stall region. The inviscid method used by AVL fails to
capture the nonlinearity of flow separation, causing it to overestimate the
lift and underestimate drag that together producing a significantly inaccurate
pitching moment post-stall. (Unfortunately the experimental method in XFLR5 had
a bug that produced zero sideforce, so its results are omitted.) The NLLT
performs much better, but still highlights the effect of using the well-known
"optimistic" estimates produced by XFOIL near the stall region; and again, the
NLLT fails to converge when the section-local :math:`\alpha` of the downwind
wingtip exceeds the maximum :math:`\alpha` supported by the coefficients lookup
table instead of producing progressively more incorrect results.


Coefficients vs sideslip
""""""""""""""""""""""""

A third perspective of wing behavior is to plot the coefficients that affect
motion in the :math:`y`-direction (sideforce, rolling moment, and yawing
moment) versus angle of sideslip :math:`\beta`. These results are grouped into
four quadrants by the angle of attack :math:`\alpha` used during the test.
Unfortunately, the experimental method in XFLR5 had a bug that produced zero
sideforce, which is also coupled to the roll and yaw moments, so its results
are omitted.


.. figure:: figures/paraglider/belloc/NLLT/standard/CY_vs_beta.*
   :name: Belloc_CY_vs_beta

   Lateral force coefficient vs sideslip

Plotting sideforce vs sideslip (:numref:`Belloc_CY_vs_beta`) showed good
agreement between the experimental data and both theoretical models, although
the NLLT has a slight accuracy advantage over the inviscid method.


.. figure:: figures/paraglider/belloc/NLLT/standard/Cl_vs_beta.*
   :name: Belloc_Cl_vs_beta

   Rolling coefficient vs sideslip

In the rolling moment versus sideslip test (:numref:`Belloc_Cl_vs_beta`) we
find the only examples where the inviscid method outperforms the NLLT, but
otherwise this plot demonstrates no noteworthy effects.


.. figure:: figures/paraglider/belloc/NLLT/standard/Cn_vs_beta.*
   :name: Belloc_Cn_vs_beta

   Yawing coefficient vs sideslip

The last plot, for the yawing moment versus sideslip
(:numref:`Belloc_Cn_vs_beta`) has several similarities to
:numref:`Belloc_Cm_vs_alpha`, except instead of demonstrating the pitch
stability of the wing, it demonstrates the yaw stability of the wing. When the
relative wind approaches from the right (:math:`\beta > 0°`) a positive yaw
moment will turn the canopy into the wind, and vice-versa for wind from the
left. And again, the effect of failing to accurately model stall conditions on
individual sections (the downwind sections, specifically) causes both methods
to overestimate the restoring moment. Nevertheless, the NLLT succeeded in
capturing at least part of the effect, once again proving the value of the
method over purely inviscid solutions.


Niviuk Hook 3 system dynamics
-----------------------------

.. How accurate is the model? This section involves **expected** outcomes,
   which means we already know what we expect to see. Validation is about
   *confirming*, not *learning*.


.. What is model validation? Why is it difficult for paragliders?

The previous chapter provided a :doc:`demonstration` of how to estimate the
parameters of the component models for a commercial paraglider wing. Having
defined the component models, they are combined into a composite
:doc:`system_dynamics` model that provides the behavior of the complete glider.
Getting to this point with such little information required many modeling
assumptions, simplifications, approximations, and outright guesswork, so the
natural next step is to question the validity of the model: how accurately does
it estimate the true behavior of the physical system? In any modeling project
it is vital to validate the model by comparing its estimates to experimental
data, and this case is no exception.

Unfortunately, experimental data is extremely scarce for commercial paraglider
wings. Unlike the previous section, wind tunnel measurements are unavailable.
What's worse, the dynamic behavior of a wing in motion is significantly more
complex than the static behavior of a wing held fixedly in a wind tunnel. As
a result, validation is limited to point data and general expectations gleaned
from sources such as glider certifications and consumer wing reviews. Clearly
such sources lack the rigor to "prove" model accuracy, but — when taken
together — they can still provide incremental confidence that a model is
adequate to answer basic questions of wing performance.


Polar curve
^^^^^^^^^^^

.. Compare model estimates of the glider's longitudinal steady-state
   aerodynamics over the range of control inputs against published performance
   data, such as minimum sink rate and speed range.

.. Plot and discuss the predicted polar curves.

   I don't have access to experimental polar curves, but I do have point
   estimates from certification and wing review flights.

   Use this section to really highlight the limitations/assumptions of the
   model? Unknown airfoil, unknown true line positions, lack of a proper
   `LineGeometry` (so brake deflections and arc changes when accelerator is
   applied are both unknown), no cell billowing, etc etc. Seems like a good
   place to point out "this is overestimating lift and underestimating drag, as
   expected."


.. Polar curves

The conventional way to summarize the performance of a gliding aircraft is with
a chart called the *polar curve*. These curves show the vertical and horizontal
speed of the aircraft at equilibrium over the range of brake and accelerator
inputs, providing information such as the speed range of the glider and its
glide ratio at different speeds. Given the wealth of information compactly
communicated by a polar curve, they are an excellent starting point for
critiquing the estimates of a flight dynamics model for a glider.

The previous section demonstrated the creation of a paraglider model for
a Niviuk Hook 3, size 23. Now, models for the larger sizes of the wing (created
using the same workflow) will be compared to experimental data by comparing
measurements from test flights to the predicted polar curves.


Size 25
"""""""

.. FIXME: how to cite `Hook 3 Parapente Mag 148.pdf`?

The experimental data for this section is taken from a size 25 version of the
wing that was reviewed for the French magazine "Parapente Mag". Unfortunately,
reviews such as this cannot provide the entire polar curve: because each point
is laborious to measure accurately, reviews only provide noteworthy values,
such as the minimum and maximum speeds, or the horizontal and vertical speeds
that mark the "minimum sink" and "best glide" operating points of the glider.
Despite this ambiguity, by plotting the experimental point data over the
theoretical curve it is possible to get a sense of the general accuracy of the
model estimates.

.. figure:: figures/paraglider/demonstration/polar_25.svg

   Polar curve for Niviuk Hook 3 size 25

   Colored markings are theoretical data from the model, black markings are
   experimental data from Parapente Mag. Red represents symmetric braking,
   green represents accelerating, and the blue diagonal line marks the
   predicted best glide ratio. The three black vertical lines mark the
   experimental values for minimum speed, trim speed, and maximum speed; the
   left black dot is the "minimum sink" operating point, and the right dot is
   the "best glide" operating point.

If the model is a good approximation of the glider that generated the data
— and assuming the data was collected accurately — then the experimental values
should match the predicted values:

* The minimum ground speed should align with the leftmost endpoint of the red
  curve

* Trim speed should align with the point where the red and green curves connect

* The maximum ground speed should align with the rightmost endpoint of the
  green curve

* The "minimum sink" operating point should lie on the point where the curve
  reaches its minimum

* The "best glide" operating point should lie on the point where the blue line
  touches the polar curve

Although the diagram is a convenient way to summarize so much information it
can be hard to distinguish specific values, so their numerical equivalents are
listed below.

.. list-table:: Niviuk Hook 3 25 simulated polar curve vs flight data
   :header-rows: 1

   * - Value
     - Experimental
     - Simulated
     - Error
   * - Minimum speed
     - 6.7
     - 7.4
     - +10%
   * - Minimum sink <h, v>
     - 9.22, 1.02
     - 9.6, 1.06
     - +4.2%, +3.9%
   * - Trim speed
     - 10.6
     - 10.2
     - -3.8%
   * - Maximum speed
     - 14.4
     - 14.7
     - +2.08%
   * - Best glide <h, v>
     - 10.4, 1.12
     - 10.2, 1.08
     - -1.9%, -3.6%
   * - Best glide ratio
     - 9.3
     - 9.44
     - +1.5%

Observations:

* The minimum ground speed of the theoretical model is significantly higher
  than the experimental value. That may be explained by the conservative value
  of :math:`\kappa_b = 0.44 \, [m]` (the maximum distance the brakes can be
  pulled; see the earlier discussion when defining the parameters for the
  :ref:`demonstration:Brakes`). The review listed the maximum brake length as
  >60cm, which suggests that this model can only apply <73% of the full range
  of brakes, so this result in unsurprising.

* Minimum sink occurs at about 0.4 m/s slower ground speed. This may be related
  to the procedure to generate the deflected :ref:`Profiles`, to the deflection
  distribution, or to the aerodynamic coefficient estimates from XFOIL.

* Minimum sink rate is remarkably close (1.06 versus 1.02 m/s), which I find
  surprising since I expected the "optimistic" airfoil set :numref:`airfoil
  set, braking NACA24018` to overestimate lift during braking.

* The theoretical model underestimates the ground speed at trim. Although this
  could be due to it overestimating the drag, it is far more likely that the
  model is overestimating the lift of the wing, so less speed is required to
  counteract the weight of the glider.

* This experimental data reported the best glide at 10.4 m/s when trim was 10.6
  m/s. This disagrees with our earlier assumption that best glide should occur
  at trim.

* The model overestimates the maximum ground speed. This may suggest it is
  underestimating drag, or it could suggest that the model parameters are wrong
  (:math:`\kappa_C` in particular has a large impact on maximum speed), or it
  could be because this rigid body model neglects foil deformations (it assumes
  the accelerator produces a perfect pitch-rotation of the foil) as well as the
  section profile deformations that increase with speed.

In truth, these observations are just a few of the possible issues with the
theoretical model (not to mention issues with the experimental data itself);
there are so many simplifications at work, and point data cannot hope to reveal
all their flaws. These results suggest that the performance of the model is
excellent when predicting longitudinal equilibrium, but a wider variety of wing
models need to be examined to determine if this excellence generalizes to other
wings.


Size 27
"""""""

.. FIXME: how to cite `hook 3 perfils.pdf`?

The experimental data for this section is taken from a size 27 version of the
wing that was reviewed for the Spanish magazine "Parapente". As with the size
25 model, plotting the experimental data on top of the theoretical curves
produces valuable reference data:

.. figure:: figures/paraglider/demonstration/polar_27.svg

   Polar curve for Niviuk Hook 3 size 27

   Colored markings are theoretical data from the model, black markings are
   experimental data from Parapente. Red represents symmetric braking, green
   represents accelerating, and the blue diagonal line marks the predicted best
   glide ratio. The three black vertical lines mark the experimental values for
   minimum speed, trim speed, and maximum speed; the left black dot is the
   "minimum sink" operating point, and the right dot is the "best glide"
   operating point.

As before, the numerical equivalents of the data in the figure above:

.. list-table:: Niviuk Hook 3 27 simulated polar curve vs flight data
   :header-rows: 1

   * - Value
     - Experimental
     - Simulated
     - Error
   * - Minimum groundspeed
     - 6.7
     - 7.83
     - +17%
   * - Minimum sink <h, v>
     - 9.72, 1.15
     - 10.2, 1.12
     - +4.9%, -2.6%
   * - Trim speed
     - 11.1
     - 10.8
     - -2.7%
   * - Maximum speed
     - 15
     - 15.4
     - +2.7%
   * - Best glide <h, v>
     - 11.1, 1.17
     - 10.8, 1.13
     - -2.7%, -3.4%
   * - Best glide ratio
     - 9.5
     - 9.52
     - 0.21%

The observations are similar to that for the size 25 model. Overall the fit is
excellent. This model was limited to :math:`\kappa_b = 0.46 \, [m]`, or <76% of
the usable ">60cm" brake length, so the minimum ground speed is still too high.
And again, the model underestimates the ground speed at trim. The best glide
ratio matches exactly, although the theoretical model still slightly
underestimates the ground speed where that occurs.


Pitch stability
^^^^^^^^^^^^^^^

Another simple sanity check is to verify the glider pitch stability by flying
on a straight course at maximum speed and abruptly releasing the accelerator
(:cite:`wild2009AirworthinessRequirementsHanggliders`, Sec. 4.1.5). Releasing
the accelerator shifts the payload to shift aft, causing the canopy to pitch
backwards; in the positive-pitch position the glider briefly ascends as it
converts the energy from its high airspeed into altitude, but because the wing
loses airspeed so quickly it will "overshoot" its equilibrium point and need to
dive forward as the glider attempts to reestablish equilibrium.

The danger of this pitch-forward behavior is that it may induced a frontal
collapse of the canopy. To estimate the safety margin of the wing, the test
assigns a grade based on the negative pitch angle as it dives forward. If the
wing pitches forward less than 30° it receives an "A"; if it pitches forward
30–60° it receives a "C", and for >60° it receives an "F". The Niviuk Hook 3 is
rated as an "B" wing, and should not pitch forward more than 30°. Using this
model to simulate the test protocol by releasing the accelerator in 0.3s
produces:

.. figure:: figures/paraglider/demonstration/accelerator_fast_release_path_sideview.*

   Flight test, rapidly exiting accelerated flight, side view

   Black lines are drawn from the riser to the point directly above the payload
   to help visualize the canopy pitch angle, and are added every 0.5 seconds.

.. figure:: figures/paraglider/demonstration/accelerator_fast_release_pitch_angle.*

   Flight test, rapidly exiting accelerated flight, pitch angle

The model predicts the wing configuration will pitch backwards 23° before
diving forwards to a pitch angle of -13° which satisfies the expected grading.
Although this test is not particularly informative, it's simplicity makes it
worthwhile.

.. FIXME: Compare 6a and 9a?


Steady-state turn
^^^^^^^^^^^^^^^^^

.. 360° turn at 20° bank angle. Compare to Pagen's ballpark figures

Although the simplicity of longitudinal dynamics make them the best place to
start testing a model, the more difficult tests are for the dynamic behavior.
One simple test is to check the behavior during a steady 360° maneuver and
compare them to the "guidelines" in :cite:`pagen2001ArtParagliding` that lists
approximate sink rates and turn radii as a function of bank angle. The method
does come with some caveats, however: for example, the author does is not
discussing a specific glider, so these values are assumed to be averages of
wing performance; this this is a midrange paraglider wing, it is assumed to be
"average". Also, the author does not define the control inputs, but standard
piloting practice is to use a combination of weight shift and brake for an
efficient turn, so it is safe to assume the author is describing situations
with those control inputs. Simulating this scenario produces the results in
:numref:`path_360_topdown`:

.. figure:: figures/validation/path_360_topdown.svg
   :name: path_360_topdown

   Steady-state turn at a 20° bank angle, top-down view

.. list-table:: Steady-state turn validation
   :header-rows: 1

   * - Value
     - Guideline
     - Simulated
     - Error
   * - Turn radius [m]
     - ~12
     - 20
     - +67%
   * - Sink rate [m/s]
     - ~1.1
     - 1.5
     - +36%
   * - 360° turn rate [sec]
     - ~11.5
     - 16
     - +40%

Unlike the accurate estimates for the polar curves, which measured
steady-state, longitudinal dynamics, this model clearly struggles with this
test. It is unclear what is causing the discrepancy, but it is an important
counterpoint that highlights the many dimensions of model accuracy. It is also
suggests a direction for future work on :ref:`weight shift modeling
<weight_shift_modeling>`.
