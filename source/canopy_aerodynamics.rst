*******************
Canopy Aerodynamics
*******************

The paraglider dynamics are complicated enough on their own, so for now I'm
splitting the canopy aerodynamics into their own section.


The classic method for estimating the aerodynamic performance of a wing is
Prandtl's *lifting-line theory* (LLT). This deceptively simple model allowed
analytical solutions to the lift distribution.

For wings with significant sweep and/or dihedral, the classic LLT breaks down.
These more complex geometries require adaptations to account for the
non-linear behaviors, resulting in *non-linear lifting line* (NLLT) theories.
These are often also known as "numerical" lifting-line theories, since they
require numerical solutions.


Lifting-line
============

[[Describe the classic approach and its limitations.]]


Inviscid methods
================

* It'd be cool to show a purely inviscid analysis first. Those are more common
  in many analyses, and more commonly applied to unusual geometry. I can use
  its poor performance to motivation Phillips' method. It also gives me the
  chance to introduce the method (since I'll need to discuss it at some point
  anyway before I compare it with Phillips).

* Notice there are a variety of limitations to my chosen inviscid model: see
  `https://www.xflr5.tech/docs/Part%20IV:%20Limitations.pdf`. When I say "this
  is what inviscid methods produce", what I really mean is "this is the
  performance of the particular inviscid method I applied"


Phillips' numerical lifting-line
================================

.. figure:: figures/paraglider/dynamics/phillips_scratch.*

   Wing sections for Phillips' method.


* In Phillips' original derivation they assumes uniform flow for Eq:5, but I'm
  using the non-uniform version from Hunsaker-Snyder Eq:5. Hunsaker mentions
  that this *local upstream velocity* `V_rel,i` "differs from the global
  freestream velocity `V_inf` in that it may also have contributions from
  prop-wash **or rotations of the lifting surface about the aircraft center of
  gravity.**" Is he implying that Phillips' method is useable as-is during
  rotations?

* I'm using airfoil data from XFOIL, which is unreliable post-stall, but I'm
  including significant post-stall coefficient data anyway to observe how
  Phillips' method behaves in those regions. It's useful to understand how the
  method behaves in post-stall regions in the event you have accurate
  post-stall airfoil data. (ignoring the fact that the 3D wing basically
  shoots that to heck anyway)

* By using section coefficient data, I'm ignoring cross-flow effects. I'm sure
  the arc of the wing has a significant effect on the boundary layer, which
  we're assuming is constant over the entire section.


Case Study
==========

(This is where I'll introduce Belloc's reference wing and wind tunnel data.
I can refer to it when I'm showing examples of the chord surface geometries as
an real-world application of the chord surface concept.)

Every new tool should be validated, and for aerodynamic codes validation often
involves comparing theoretical models to wind tunnel measurements. For the
tools proposed in this paper, validation should include demonstrating the
flexibility of the geometry definition proposed in :doc:`paraglider_canopies`
and the performance of the aerodynamics code proposed in
:ref:`paraglider_dynamics:Non-linear lifting line theory`.

An excellent test case for the geometry and aerodynamics is available from
:cite:`belloc2015WindTunnelInvestigation`, which provides both point-wise
geometry data and wind tunnel performance.


Geometry
--------

Chord Surface
^^^^^^^^^^^^^

.. list-table:: Full-scale wing dimensions
   :header-rows: 1

   * - Dimension
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

The physical model was built at a quarter-scale. Physical dimensions and
positions were provided for the physical model.

.. csv-table:: Model wing geometry data at panel’s ends
   :header: :math:`i`, :math:`y_i` [m], :math:`z_i` [m], :math:`c_i` [m], Airfoil shifting location [%], Airfoil tilt angle [deg]

   0, -0.688,  0.000, 0.107, 60, 3
   1, -0.664, -0.097, 0.137, 60, 3
   2, -0.595, -0.188, 0.198, 60, 0
   3, -0.486, -0.265, 0.259, 60, 0
   4, -0.344, -0.325, 0.308, 60, 0
   5, -0.178, -0.362, 0.339, 60, 0
   6,  0.000, -0.375, 0.350, 60, 0
   7,  0.178, -0.362, 0.339, 60, 0
   8,  0.344, -0.325, 0.308, 60, 0
   9,  0.486, -0.265, 0.259, 60, 0
   10, 0.595, -0.188, 0.198, 60, 0
   11,  0.664, -0.097, 0.137, 60, 3
   12,  0.688,  0.000, 0.107, 60, 3

It is important to notice the difference between the section numbers used here
and the section indices used in the parafoil canopy geometry.

Also, the reference data is defined with the wing tips at :math:`z = 0`,
whereas the chord surface convention places the canopy origin at the leading
edge of the central section. This is easily accommodated by the chord surface
implementation, which simply shifts the origin to suit the final geometry.

.. TODO:: Should I use these tables or just give the explicit equations?
   They're messy, bu I do like the fact that they highlight the fact that you
   **can** use pointwise data.

Inputting the values to the canopy geometry produces:

.. raw:: latex

   \newpage

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_curves.*

.. figure:: figures/paraglider/geometry/canopy/examples/build/belloc_canopy.*


Airfoils
^^^^^^^^

It uses a NACA 23015.

.. figure:: figures/paraglider/geometry/airfoil/NACA-23015.*

   NACA 23015



Aerodynamics
------------

(Compare the wind tunnel data against the NLLT and a *vortex lattice method*
(VLM) from XFLR5.

.. figure:: figures/paraglider/belloc/CL_vs_alpha.*

   Lift coefficient vs angle of attack.

.. figure:: figures/paraglider/belloc/CD_vs_alpha.*

   Lift coefficient vs angle of attack.

.. figure:: figures/paraglider/belloc/CM_vs_alpha.*

   Global pitching coefficient vs angle of attack.

This is the global pitching coefficient, which includes contributions from
both the section pitching coefficients and the aerodynamic forces. The VLM
estimate appears to be using the wrong reference point, but it isn't clear
from the program documentation what the error might be. The results are left
here for completeness and to highlight the uncertainty in how the VLM was
applied.

.. figure:: figures/paraglider/belloc/CL_vs_CD.*

   Lift coefficient vs drag coefficient.

.. figure:: figures/paraglider/belloc/CL_vs_CM.*

   Lift coefficient vs global pitching coefficient.
