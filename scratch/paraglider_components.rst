* The "rigid canopy" simplification together with the 6DoF model is what
  allows me to neglect the riser strap width. I think the 9DoF model should
  incorporate the riser strap width when computing the relative roll restoring
  moment.


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


Deflection angles
=================

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
