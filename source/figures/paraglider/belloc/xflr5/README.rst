This is an XFLR5 project for analyzing a reference paraglider wing from [1].

The primary purpose of this implementation is to highlight the limitations of
the inviscid method in AVL. By default, both AVL and XFLR5 assume the
freestream is parallel to the x-axis, but XFLR5 has an experimental option to
reorient the geometry instead of the freestream when running analyses. Using
tilted geometry is not recommended by the developer, and appears to have
significant issues when computing the moment coefficients, but the lift
coefficient performance seems promising and worth discussion.

These results are from development version `r1237` (a v6.48 pre-release) which
includes a fix when using the tilted geometry option (bug #156).

Note that the current version still includes a bug where the x-coordinate of
the reference point resets whenever a polar is reconfigured, or when the
program restarts, so the "CoG.X" is reported as `0.285` instead of `0.350`,
but these results were in fact computed using the central chord of `0.350`.
Because the moment coefficients seem wrong this is irrelevant, but worth
noting.

1. Belloc, Hervé. Wind tunnel investigation of a rigid paraglider reference
   wing. 2015. Journal of Aircraft 52:703–8. doi:10.2514/1.C032513


Geometry
========

The paper gives the coordinates of the 60% chord points, but XFLR5 uses
leading edge coordinates, so the values must be converted.

XFLR5 defines `N` wing panels using `N+1` wing sections. Each section is
defined by a spanwise distance, x-offset, dihedral angle, and twist angle.
Instead of explicit y-coordinates, XFLR5 uses panel lengths; this is confusing
because it calls the panel length "y [m]", but that value is actually the
cumulative linear panel span starting from the root, so dihedral, sweep, etc,
will make the y-coordinate of each section leading edge smaller than specified
by the `y_i` value. To produce the `y_i` for this geometry, use the L2 norm of
the `xyz` coordinates provided by the paper. For example, in Python:

.. code:: python

   xyz = np.array(  # One half of the symmetric wing
       [
           [0.000,  0.000, -0.375],
           [0.000,  0.178, -0.362],
           [0.000,  0.344, -0.325],
           [0.000,  0.486, -0.265],
           [0.000,  0.595, -0.188],
           [0.000,  0.664, -0.097],
           [0.000,  0.688,  0.000],
       ],
   )
   panel_lengths = np.linalg.norm(np.diff(xyz, axis=0), axis=1)
   y = np.cumsum(np.r_[0, panel_lengths])  # The "y" for XFLR5 wing design
   # result: y = [0, .178, .349, .503, .636, .750, .850]

   # For the dihedral angles of each panel:
   dyz = np.diff(xyz[:, 1:], axis=0)  # y and z coordinates only
   dihedral = np.rad2deg(np.arctan2(-dyz.T[1], dyz.T[0]))
   # result: dihedral = [-4.2, -12.6, -22.9, -35.2, -52.8, -76.1]
