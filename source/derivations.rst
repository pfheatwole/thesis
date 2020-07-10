*************************
Supplementary Derivations
*************************


Area and Volume of a Mesh
=========================

The paraglider dynamics requires the inertial properties of the canopy surface
areas and volume. These include the magnitudes (total mass or volume),
centroids, and inertia tensors. All of these quantities can be computed using
a triangular surface mesh over the canopy surfaces.

What follows is a reproduction of the procedure developed in
:cite:`blow2004HowFindInertia`, which is a functionally equivalent to the
procedure from :cite:`zhang2001EfficientFeatureExtraction` but with a more
intuitive interpretation and complete equations for the inertia tensors.


Area
----

To compute the mass distribution of the upper and lower surfaces, start by
computing the dimensionless inertia tensor of the areas then scale them by the
surface material areal densities.

First, cover each surface in a triangulated mesh, so each surface is
represented by a set of :math:`N` triangles :math:`\left\{ t_n
\right\}^N_{n=1}`. Each triangle is defined by three points :math:`t_n
= \left\{ \vec{p_{n,1}}, \vec{p_{n,2}}, \vec{p_{n,3}} \right\}` in canopy
coordinates which have been ordered to produce a right-handed sequence
suitable for the surface. These triangles can be used to compute the surface
areas and enclosed volume of the canopy.

For surface areas, each triangular area is easily computed using the vector
cross-product of two legs of the triangle:

.. math::

   a_m =
      \frac{1}{2}
      \rho
      \left[
         \left( \vec{p_{m,2}} - \vec{p_{m,1}} \right)
         \times
         \left( \vec{p_{m,3}} - \vec{p_{m,2}} \right)
      \right]

The total area is the sum of the triangle areas:

.. math::

   A = \sum^M_{m=1} a_m

The centroid of each triangle:

.. math::

   \vec{c}_m = \frac{1}{3} \sum^3_{i=1} \vec{p_{m,i}}

The centroid of the net surface area:

.. math::

   \overline{\vec{A}} = \frac{1}{A} \sum^M_{m=1} a_m \vec{c}_m

The covariance matrix of the surface area:

.. math::

   \mat{C} = \sum^M_{m=1} a_m \vec{c}_m \vec{c}_m^T

The inertia tensor of the surface area:

.. math::

   J = \mathrm{trace} \left( \mat{C} \right) \vec{I}_3 - \mat{C}

And tada, there are the three relevant properties for each surface area: the
total area :math:`A`, the centroid :math:`C`, and the inertia tensor
:math:`J`.


Volume
------

Now for the volume. For the purposes of computing the inertia properties of
the enclosed air, it is convenient to neglect the air intakes and treat the
canopy as a closed volume. Given this simplifying assumption, build another
surface mesh that covers the total canopy surface as well as the left and
right wing tip sections. Given a surface triangulation over the closed canopy
geometry using :math:`N` triangles :math:`\left\{ t_n \right\}^N_{n=1}` as
before in the area calculations, the volume can be computed as follows:

.. TODO: should t_k be a matrix? That'd make sense when I compute its
   determinant.

First, treat each triangle as the face of a tetrahedron that includes the
origin. The signed volume of the tetrahedron formed by each triangle is given
by:

.. math::

   v_n =
      \frac{1}{6}
      \left(
         \vec{p_{n,1}} \cdot \vec{p_{n,2}}
      \right)
      \times \vec{p_{n,3}}

Given that the vertices of each triangle were oriented such that they satisfy
a right-hand rule, the sign of each volume will be positive if the normal
vector for each triangular face points away from the origin, and negative if
it points towards the origin. In essence the tetrahedrons "overcount" the
volume for triangles pointing away from the origin, then the triangles facing
the origin subtract away the excess volume. The final volume of the canopy is
the simple sum:

.. math::

   V = \sum^N_{n=1} v_n

For the volume centroid of each tetrahedron:

.. math::

   \overline{\vec{v}}_n = \frac{1}{4} \sum^3_{i=1} \vec{p_{n,i}}

And the centroid of the total volume:

.. math::

   \overline{\vec{v}} = \frac{1}{V} \sum^N_{n=1} \overline{\vec{v}}_n

Lastly, calculating the inertia tensor of the volume can be simplified by
computing the inertia tensor of a prototypical or "canonical" tetrahedron and
applying an affine transformation to produce the inertia tensor of each
individual volume.

First, given the covariance matrix of the "canonical" tetrahedron:

.. math::

   \mat{\hat{C}} \defas \begin{bmatrix}
      \frac{1}{60} & \frac{1}{120} & \frac{1}{120}\\
      \frac{1}{120} & \frac{1}{60} & \frac{1}{120}\\
      \frac{1}{120} & \frac{1}{120} & \frac{1}{60}
   \end{bmatrix}


Use the points in each triangle to define:

.. math::

   \mat{T}_n \defas
      \begin{bmatrix}
         | & | & | \\
         \vec{p_{n,1}} & \vec{p_{n,2}} & \vec{p_{n,3}}\\
         | & | & | \\
      \end{bmatrix}

The covariance of each tetrahedron volume is then:

.. math::

   \mat{C}_n = \left| \mat{T}_n \right| \mat{T}_n^T \mat{\hat{C}} \mat{T}_n

And the covariance matrix of the complete volume:

.. math::

   \mat{C} = \sum^N_{n=1} \mat{C}_n

And at last, the inertia tensor of the volume can be computed directly from
the covariance matrix:

.. math::

   \mat{J} = \mathrm{trace} \left( \mat{\hat{C}} \right) \vec{I}_3 - \mat{\hat{C}}

