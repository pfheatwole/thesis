* The "rigid canopy" simplification together with the 6DoF model is what
  allows me to neglect the riser strap width. I think the 9DoF model should
  incorporate the riser strap width when computing the relative roll restoring
  moment.

* FIXME: where do I define the aerodynamic *control points*? (They're part of
  my "design language" for the components.)

* Every paraglider component should probably summarize:

  1. The parameters that define it

  2. The control inputs it provides to the system model

* Work flow:

  1. Describe what the component really is

  2. Describe how I'm modeling it

  3. The results of that modeling choice

     a. Inertia

     b. Controls

     c. Aerodynamics


  eg, "The harness is... I'm modeling it as a sphere... The inertia of
  a sphere is ... You control it by moving its CM... The aerodynamics are
  isotropic."

  eg, "The lines are this complicated bridle, but I'm lumping into a finite
  set of control points."

* **The focus of these sections are the MODEL, not about the thing itself.**
  I do NOT need to provide thorough overviews of the thing being modeled.
  Focus on

  1. What details I'm choosing to model

  2. How I'm choosing to model them

  Related, I'm struggling with having simple physical descriptions before
  launching into the models. For example, "the canopy is built from X" doesn't
  take much. Feels funny having it stand alone, the descriptions so far have
  been too short. So what if I lumped them together in the intro to the
  chapter? "The paraglider is three components: a canopy, which is X,
  suspension lines, which are Y, and a harness, which is Z."

* The canopy says what deformations it supports (trailing edge only), then
  **the suspension line model gets to leverage that to simplify itself**
  (doesn't need to support C-riser controls, stabilo, etc).


Canopy
======


Inertia
-------

* Barrow's method has several assumptions (circular arc anhedral, spanwise
  uniform thickness, etc) that are wrong for real wings.

* Apparent inertial calculations are definitely wrong when brakes are being
  applied; they're effectively increasing the thickness in the fore-aft
  direction.


Controls
--------

* Vertical deflection distance is a reasonably stable measure since the lines
  can basically only pull straight down.


Aerodynamics
------------

* Quasi-steady-state assumption (I'm using steady-state aerodynamics to
  simulate non-steady conditions by assuming the conditions are changing
  "slowly enough.") I've included adjustments for apparent mass, but I'm still
  assuming the steady-state solution is representative of the unsteady
  solution. Also, my equations for the apparent mass themselves are under
  a steady-state assumption; see :cite:`thomasson2000EquationsMotionVehicle`
  for a discussion of apparent mass in unsteady flows.

  Consider the fact that the canopy is interacting with the "underlying" wind
  field, so that the motion of the canopy changes the local wind vectors. This
  effect should propagate through time, but for my simulator I'm only using
  the "global" wind field, neglecting any effects of the previous timestep. (I
  am trying to account for apparent mass, but I don't think that's really the
  same thing, since that doesn't change the local aerodynamics.)

* Rigid-body assumption (none of the canopy, connecting lines, or payload are
  actually rigid bodies)

* This canopy model does not [[describe]] individual cells or their resulting
  distortions (billowing, wrinkling etc), but it does account for trailing
  edge deflections and the additional drag due to air intakes.

  The aerodynamic model developed in :doc:`foil_aerodynamics` is able to
  account for some of those effects through adjustments to the section
  coefficients.


Harness
=======

* See :cite:`wild2009AirworthinessRequirementsHanggliders`, pg26 for
  a discussion of harness dimensions (riser separation distance, etc)

* The chest strap width is neglected in this paper. The 6DoF model ignores
  relative rotations of the payload, and the 9DoF model hides this effect
  inside the rotational restoring coefficients. Probably not a big deal
  because turbulence is such a high frequency signal I'd never be able to
  estimate it from IGC data anyway.]]

* Review the docstring for `harness.py:Spherical`.


Suspension lines
================

* Bridle:

  * :cite:`altmann2015FluidStructureInteractionAnalysis` discusses using
    *fluid-structure interaction* to optimize the line cascading to optimize
    wing performance

  * :cite:`lolies2019NumericalMethodsEfficient` discusses the "effect of line
    split joint angles on sail deformation"

* Rigging angle:

  * *rigging*: "the system of ropes, chains, and tackle used to support and
    control the masts, sails, and yards of a sailing vessel"

  * Lingard 1995: uses a *rigging angle* for positioning the payload, which is
    related to the assumption "that the system can be induced to fly at the
    angle of attack corresponding to optimum L/D". I don't like coupling those
    two concepts this closely; if you want to compute the angle that would
    induce the optimum L/D you can then specify the `kappa_x, kappa_z` just
    the same without muddying the definition.

  * Benedetti :cite:`benedetti2012ParaglidersFlightDynamics` uses the same
    idea for positioning the harness as I do, except he uses relative `x` and
    absolute `z` whereas I use relative for both.

* The riser position uses simple 2D relations, the trailing edge deflections
  use a simple parametric representation, and the line segments are lumped for
  the inertia and drag calculations

* The mass distribution of the lines would depend on the bridle geometry and
  the masses of the lines; I don't know the bridle geometry, and the lines
  themselves are of variable weights. However, the lines get thinner as you
  approach the canopy, so their center of mass is probably relatively close to
  the paraglider center of mass, so they're contribution is assumed to be
  negligible to the overall dynamics.


Deflection angles
-----------------

* Because I'm not modeling the entire geometry, I must also approximate the
  brake deflection angles. The end effect is that this implementation only
  models the final position of the risers as a function of accelerator, and
  the deflection angles of the trailing edges as a function of left and right
  brakes.

* It is computationally prohibitive (and unnecessary) to solve for the
  aerodynamic coefficients of each section profile at each timestep. Instead,
  a set of coefficients can be precomputed for a set of deflection angles, and
  then the aerodynamics method can simply interpolate between the individual
  coefficient solutions.

  Interpolating between coefficient solutions requires a deflection index;
  a natural choice is the *deflection angle* :math:`\delta_f`.

  [[Is this discussion necessary? The canopy aerodynamics are a function of
  its shape, and its shape can be deformed by adjusting the deflection angle.
  That's it. This discussion relates specifically to the choice to model the
  foil using 2D section coefficients.]]


Related work
============

* Canopy Aerodynamics

  * Gonzalez 1993, :cite:`gonzalez1993PrandtlTheoryApplied`

  * Belloc, :cite:`belloc2015WindTunnelInvestigation`

  * Kulhanek, :cite:`kulhanek2019IdentificationDegradationAerodynamic`

  * :cite:`belloc2016InfluenceAirInlet`

  * :cite:`babinsky1999AerodynamicPerformanceParagliders`

  * Cells (distortions, etc):

    * :cite:`kulhanek2019IdentificationDegradationAerodynamic`

    * :cite:`lolies2019NumericalMethodsEfficient`


* Paraglider Dynamics

  * Babinsky 1999, :cite:`babinsky1999AerodynamicPerformanceParagliders`

  * Slegers, :cite:`gorman2012EvaluationMultibodyParafoil`

  * :cite:`ward2014ParafoilControlUsing`

  * Apparent mass

    * :cite:`lissaman1993ApparentMassEffects`

    * :cite:`thomasson2000EquationsMotionVehicle`

    * :cite:`barrows2002ApparentMassParafoils`
