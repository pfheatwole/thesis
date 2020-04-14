Figures
=======


Geometry
--------

* Geometric definitions

  Should supplement the geometric definitions with plots that are annotated to
  highlight the parameters, where possible (lengths and angles, mostly)

* Examples of each type of design parameter:

  * Elliptical planforms: flat span, length of the central chord, taper
    (length ratio of central chord versus wing tip chord), ``sweepMed``
    (maximum rate of change of sweep angle?), ``sweepMax`` (angle from central
    leading edge to the wing tip leading edge?), torsion (*does this really
    belong to the elliptical planform? or to the general case parafoil
    planform?*)

  * Elliptical lobes: ``dihedralMed`` (maximum of change of curvature?),
    ``dihedralMax`` (angle from the central chord to the wing tip chord?)


The planform and lobe diagrams are 2D. Just make some tables (possibly in the
same SVG, instead of using RST tables?) with different combinations. **Make
sure to have the parameters clearly labeled in the diagrams. Don't be like
Benedetti.**

I'm not sure how to best show the 3D versions of the completed parafoil.
Graphing 3D in still images is kind of awkward. Probably best to keep them
simple (no grids, minimal axes labels), this is for basic **qualitative**
understanding, not for quantitative purposes.


Moment of inertia
-----------------

* Are any figures essential for describing this concept? Can I just quietly
  skip my nasty derivation?


Force estimation
----------------

* Should I try to define the geometry for Phillips' method, or should I simply
  reference his paper? It would be *nice* if I could make a diagram that
  describes my implementation, but that seems like a LOT of work.
