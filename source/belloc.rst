************
A Case Study
************

Every new tool should be validated, and for aerodynamic codes validation often
involves comparing theoretical models to wind tunnel measurements. For the
tools proposed in this paper, validation should include demonstrating the
flexibility of the geometry definition proposed in :doc:`paraglider_canopies`
and the performance of the aerodynamics code proposed in
:ref:`paraglider_dynamics:Non-linear lifting line theory`.

An excellent test case for the geometry and aerodynamics is available from
:cite:`belloc2015WindTunnelInvestigation`, which provides both point-wise
geometry data and wind tunnel performance.


.. list-table:: Full-scale wing dimensions
   :header-rows: 1

   * - Dimension
     - Unit
     - Value
   * - Arch height
     - m
     - 3.00
   * - Central chord
     - m
     - 2.80
   * - Projected area
     - m\ :sup:`2`
     - 25.08
   * - Projected span
     - m
     - 11.00
   * - Projected aspect ratio
     - --
     - 4.82
   * - Flat area
     - m\ :sup:`2`
     - 28.56
   * - Flat span
     - m
     - 13.64
   * - Flat aspect ratio
     - --
     - 6.52

The physical model was built at a quarter-scale. Physical dimensions and positions were provided for the physical model.

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
