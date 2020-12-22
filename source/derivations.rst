***********
Derivations
***********


Parametric wing modeling with airfoils
======================================

.. Meta: Derive my parametrization of points on the wing surfaces

**FIXME**: choose a good section title


1. The goal:

     `r_P/O`

   We need a mesh of points on the surfaces relative to the origin.


.. The general equation

#. Decompose `r_P/O` using points in wing sections

   [[It's easier to design section profiles in 2D, so the points are relative
   to the section. You finish the wing by specifying the pose of the section
   relative to the canopy. FIXME: explain `r_{P/LE}^a` here.]]

   Airfoil geometries specify the points relative to the leading edge by
   convention, so `r_P/O` naturally decomposes to:

     `r_{P/O}^c = r_{P/LE}^c + r_{LE/O}^c`

     `r_{P/LE}^c = c * C_c/s @ T_s/a @ r_{P/LE}^a`

   This form (the result of using wing sections) introduces scale (`c`),
   position (`r_LE/O`), orientation (`C_c/s`), and "points in the section"
   (`r_P/LE`).

   [[FIXME: I didn't explain where `r_{P/LE}^c` comes from.]]


.. An additional decomposition

#. Decompose `r_LE/O` using an arbitrary reference point.

   It's often inconvenient to specify section position using the leading edge.
   Instead, allow the designer to use an arbitrary reference point `RP`:

     `r_LE/O = r_LE/RP + r_RP/O`

   This lets a designer specify section position using whatever point is the
   most convenient.

#. Parametrize the reference point using points on the section chords:

     `r_LE/RP = c * R @ C_c/s @ xhat`

   Where:

     `R = diag(r_x, r_y, r_z)`

     `0 <= r_x, r_y, r_z <= 1` (proportions of the chord)

     `xhat = [1, 0, 0]^T` (the chord lies along `xhat`)

#. The general, partially parametrized, equation:

     `r_P/O = r_P/LE + r_LE/RP + r_RP/O`

     `r_P/O = c * C_c/s @ T_s/a @ r_P/LE + c * R @ C_c/s @ xhat + r_RP/O`

   I say "general" because it'd be a reasonable target for code that
   implements a general geometry defined in terms of wing sections. Parafoils
   et al could reasonably defined using this form, using their own internal
   choices to define these parameters. It'd be nice not to lock a model into
   a particular parametrization of orientation, or reference point, or
   whatever. (Then again, it does force the user into using a reference point
   on the chord, so "general" is probably the wrong name. Also, the second
   form isn't immediately usable by parametrizations that specify section
   scale/pitch/yaw by defining the LE and TE as two points.)

   To design a wing, specify: `c`, `C_c/s`, `r_P/LE`, `R`, and `r_RP/O`. **This
   is almost exactly the same amount of work as before, you only need to add
   `R`.** Minimal extra effort for a lot of convenience.

#. Some parameter choices that work well for parafoils:

     Let `r_y = r_z`

     Parametrize `C_c/s` using intrinsic Euler roll and pitch angles

     Specify the intrinsic section roll angle as `gamma = arctan(dz/dy)` (where
     `dz/dy` comes from `r_RP/O`). [[FIXME: this avoids section yaw, but
     I forget: why was that important?]]

   To specify a parafoil you just need to design: `c`, `r_x`, `r_yz`, `r_RP/O`,
   `theta`, and the section airfoils.

   **FIXME**: write the final version using the actual functions (of section
   index, fractions of the chord, etc) instead of this generalized notation
   ("any point P" is not particularly clear)

#. <Examples of completing the definition with parametric functions
   (elliptical functions, etc) using *design parameters* (span, taper ratio,
   etc) choices of reference points, etc>


**FIXME**: move the parafoil-specific choices and design examples into
:doc:`canopy_geometry`.


General parametrization of a chord surface
==========================================

[[NOTE TO SELF: the origin of the chord surface is defined by the origins of
the position functions. Let the user of the chord surface (eg,
a `ParagliderWing`) position and orient the chord surface as they like; don't
pollute this definition with constraints like "the origin is the central
leading edge".]]


[[The first step of designing a wing using *wing sections* is to specify the
position, scale, and orientation of each section. Doing that produces
a surface from the section chords, which I'm calling a *chord surface*.]]

Mathematically, that means defining a function that returns points on the
section chords as a function of some arbitrary *section index* and some ratio
:math:`0 \le r \le 1` that specifies the position on the chord.

Because the section leading edge will be used as the origin for the section
profiles, it is intuitive to start by defining the leading edge as
a parametric curve of the section index.

Dropping the section index parameter for notational simplicity, this means we
need :math:`\vec{r}_{\mathrm{LE}/\mathrm{O}}^c` for each section, where
:math:`\mathrm{O}` is the canopy origin.

The chord surface is produced by specifying the position, scale, and
orientation of each section. For the position of a section, you can use any
reference point :math:`\mathrm{RP}` in the coordinate system of that section.

**I hate `RP`. I'm already using `R` by itself, and later I refer to a point
`P`; stick to single variables. Also, should I change `pc` to `r` for
positions on the chord? Or `t`, since that's the "standard" parametric
variable?**

.. math::

   \vec{r}_{\mathrm{LE}/\mathrm{O}}^c =
     \vec{r}_{\mathrm{RP}/\mathrm{O}}^c
     + \vec{r}_{\mathrm{LE}/\mathrm{RP}}^c

If the leading edge is defined as the origin of the section, then the equation
simplifies to:

.. math::

   \vec{r}_{\mathrm{LE}/\mathrm{O}}^c =
     \vec{r}_{\mathrm{RP}/\mathrm{O}}^c
     + \mat{C}_{c/s} \vec{r}_{\mathrm{LE}/\mathrm{RP}}^s

Where :math:`\mat{C}_{c/s}` is the directed cosine matrix (DCM) of the wing
reference frame :math:`\mathcal{F}_w` with respect to the section reference
frame :math:`\mathcal{F}_s`.

Although the reference point can be any point in the section's coordinate
system, it is convenient to constrain it to be a point on the section chord,
in which case the reference point is a function of the chord ratio :math:`r`
such that :math:`\vec{r}_{\mathrm{LE}/\mathrm{RP}}^s = r\, c\, \hat{x}^s_s`,
where :math:`\hat{x}^s_s = \begin{bmatrix}1 & 0 & 0\end{bmatrix}^T` is the
section x-axis in the section coordinate system.

**FIXME: is \hat{x} just `<1, 0, 0>`, or `<-1, 0, 0>`, or something? So `r
\cdot \hat{x}` is a point some distance along the unit chord? If so, I could
generalize this and just just `c \cdot f(r)` for arbitrary curves in the
airfoil coordinate system, like the camber curve or airfoil coordinates. No
need to keep all these separate.**

.. math::

   \vec{r}_{\mathrm{LE}/\mathrm{O}}^c =
         \vec{r}_{\mathrm{RP}/\mathrm{O}}^c
         + \mat{C}_{c/s} r\, c\, \hat{x}^s_s


This equation covers the majority of the choices for chord surface
parametrizations in common use. Designs that position the chords by specifying
their leading edge are equivalent to setting :math:`r = 0` and
:math:`\vec{r}_{\mathrm{RP}/\mathrm{O}}^c
= \vec{r}_{\mathrm{LE}/\mathrm{O}}^c`. Other designs use the quarter-chord
positions for the reference points, in which case :math:`r = 0.25`.

The problem with these fixed parametrizations is that they only support
a single reference point for design in all three dimensions. If a designer
wants to position the quarter-chord (:math:`r = 0.25`) along a circular arch
and the trailing edge (:math:`r = 1`) along a straight line, then they must
manually calculate the positions that would achieve that design for a given
reference point. It is much easier to allow different reference points for
each dimension.

Define:

.. math::

   \mat{R} \defas \begin{bmatrix}
      r_x & 0 & 0\\
      0 & r_y & 0\\
      0 & 0 & r_z
   \end{bmatrix}

The final form of the generalized equation for the leading edge, allowing
independent design curves and reference point for each of the position
dimensions, is then:

.. math::

   \vec{r}_{\mathrm{LE}/\mathrm{O}}^c =
     \vec{r}_{\mathrm{RP}/\mathrm{O}}^c
     + \mat{R} \mat{C}_{c/s} c\, \hat{x}^s_s

And the position of some point :math:`P` at a point :math:`0 \le p \le 1` on
the section chords: **[[am I switching from `r` to `p` now?]]**

.. math::

   \begin{aligned}
   \vec{r}_{P/O}^c
     &= \vec{r}_{LE/O}^c + \vec{r}_{P/LE}^c\\
     &= \vec{r}_{LE/O}^c - \vec{r}_{LE/P}^c\\
     &=
        \left(
          \vec{r}_{\mathrm{RP}/\mathrm{O}}^c
            + \mat{R} \mat{C}_{c/s} c\, \hat{x}^s_s
        \right)
        - p\, \mat{C}_{c/s} c\, \hat{x}^s_s\\
   \end{aligned}


Which simplifies to the final, general form of points on the section chords as
a function of the section index :math:`s` and the chord ratio :math:`p`:

.. math::
   :label: chord_points

   \vec{r}_{P/O}^c(s, p) =
      \vec{r}_{\mathrm{RP}/\mathrm{O}}^c(s)
      + \left(\mat{R}(s) - p\right) \mat{C}_{c/s} c(s)\, \hat{x}^s_s(s)

All the notational baggage can make this equation look more complicated than
it really is. Suppose the points on the chord are simply :math:`\left\langle
x, y, z \right\rangle` in wing coordinates, the reference points in wing
coordinates are :math:`\vec{r}_{RP/O} = \left\langle x_r, y_r, z_r
\right\rangle`, and :math:`\mat{K}(s) = \left(\mat{R}(s) - p\right) c(s)`,
then the structure is easier to see:

.. math::
   :label: simplifed_chord_points

   \left\langle x, y, z \right\rangle =
      \left\langle x_r, y_r, z_r \right\rangle
      + \mat{K} \hat{x}_s^c

Or, using separate equations instead of matrix math (FIXME: awkward, I'm
switching from using the `s` subscript to indicate the section x-hat to using
the subscript to reference the x, y, and z components of the section x-hat but
in the wing coordinate system):

.. math::

   \begin{aligned}
   x &= x_r + (r_x - p) \hat{x}_x\\
   y &= y_r + (r_y - p) \hat{x}_y\\
   z &= z_r + (r_z - p) \hat{x}_z
   \end{aligned}


Designing a chord surface with these equations requires five steps:

1. Define the *section index* :math:`s`

2. Define a scalar-valued function for the section scaling factors
   :math:`c(s)`

3. Choose the reference point positions on the chords :math:`\left\{ r_x(s),
   r_y(s), r_z(s) \right\}`.

4. Define a 3-vector valued function for the section reference point positions
   in wing coordinates :math:`\vec{r}_{RP/O}^c(s) = \left\langle x(s), y(s),
   z(s) \right\rangle`

5. Define the section orientation matrices :math:`\mat{C}_{c/s}(s)`

[[In :doc:`canopy_geometry` I show a set of choices that work well for
designing parafoils.]]


Parametric design curves
========================

[[Not sure where to put this. I'm using these in the examples, and again in my
"case study", wherever that ends up. **How important is it that I present the
mathematical versions?**

For now I think I'll present the basic idea, but refer to the code for the
complete implementation. These are messy, I should stick them in derivations.
They're not essential to this paper.]]

[[The `elliptical_chord` and `elliptical_arc` are helper functions that
generate an `EllipticalArc` object. Should I focus on deriving the
`EllipticalArc`?]]


Elliptical chord
----------------

An elliptical arc can be describe with three parameters: A, B, and the
constant. Alternatively, letting the constant be `1` you can think of these
three parameters as the normalized major axis, normalized minor axis, and
scale.

The parametric model requires `c(s)`, the chord length as a function of
section index. If the chord distribution is an elliptical function of section
index, then the major axis is `s`, which ranges from -1 to +1. That leaves two
parameters for the designer.

There are two typical options: `<root, tip>` and `<root, taper>`. My
implementation offers `c = f(s; root, tip)`, where `root` and `tip` are the
design parameters.


Elliptical arc
--------------

The arc of a wing is the vector-valued function of `<y, z>` coordinates. The
majority of parafoil arcs can be described with an elliptical function.

Similar to the elliptical chord, an elliptical arc can be defined as
a function three parameters. Again, the function parameter is `s` with a set
domain of -1 to +1, leaving two design parameters.

One parametrization is to pair the arc anhedral (the angle from the wing root
to the wing tip) with the section roll angle at the wing tip. Assuming arc
anhedral, this choice constrains `2 * anhedral <= tip_roll < 90`.

My implementation offers this as `yz = elliptical_arc = f(s; anhedral,
tip_roll)`, where `anhedral` and `tip_roll` are the design parameters. If
`tip_roll` is unspecified a circular arc is assumed (so `tip_roll
= 2 * anhedral`).


Polynomial torsion
------------------

The most common spanwise geometric torsion is a explicit torsion angles at
specific section indices with linear interpolation between sections.

For parafoils, it can be more natural to use non-linear curves. A generalized
interpolator can use a polynomial:

.. math::

   \theta(s) =
     \begin{cases}
       0 & s < s_{start} \\
       T p^\beta & s \ge s_{start}
     \end{cases}

Where :math:`T` is the maximum torsion at the wingtip, :math:`p = \frac{\lvert
s \rvert - s_{start}}{1 - s_{start}}`,  the fraction from :math:`s_{start}` to
the wingtip, and :math:`0 \le s_{start} < 1`.

So :math:`\beta = 1` is linear interpolation from :math:`s_{start} \le \lvert
s \rvert \le 1`, :math:`\beta = 2` is quadratic, etc.


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
surface material areal densities. [[FIXME: what? Reword: we want the total
area, total area centroid, and dimensionless inertia matrices. We can scale
those by the upper and lower surface densities to get the actual values.]]

First, for each of the upper and lower surfaces, cover the surface with
a triangulated mesh so it is represented by a set of :math:`N` triangles. Each
triangle is defined by three points :math:`\left\{ \mathrm{P1}, \mathrm{P2},
\mathrm{P3} \right\}_n` in canopy coordinates. For convenience, define position
vectors for each of the three points of the nth triangle: :math:`\vec{r}_{i,n}
\defas \vec{r}_{Pi/O,n}`.

The area of each triangle is easily computed using the vector cross-product of
two legs of the triangle:

.. math::

   a_n =
      \frac{1}{2}
      \rho
      \left\|
         \left( \vec{r}_{2,n} - \vec{r}_{1,n} \right)
         \times
         \left( \vec{r}_{3,n} - \vec{r}_{2,n} \right)
      \right\|

The total area of the surface is the sum of the triangle areas:

.. I wasn't crazy about the notation `a = sum(a_n)`, but it is clean  and it
   matches Hughes (eg, see Eq:9 on page 44 (53), where `p = sum(p_n)`)

.. math::

   a = \sum^N_{n=1} a_n

The area centroid of each triangle:

.. math::

   \overline{\vec{a}}_n \defas
     \frac{1}{3} \left( \vec{r}_{1,n} + \vec{r}_{2,n} + \vec{r}_{3,n} \right)

And the centroid :math:`\mathrm{A}` of the total surface area with respect to
the canopy origin :math:`\mathrm{O}`:

.. math::

   \vec{r}_{\mathrm{A}/\mathrm{O}} = \frac{1}{a} \sum^N_{n=1} a_n \overline{\vec{a}}_n

The covariance matrix of the total surface area:

.. math::

   \mat{\Sigma}_a = \sum^N_{n=1} a_n \overline{\vec{a}}_n \overline{\vec{a}}_n^T

The inertia tensor of the total surface area :math:`a` about the canopy origin
:math:`\mathrm{O}`:

.. math::

   \mat{J}_{a/\mathrm{O}} = \mathrm{trace} \left( \mat{\Sigma}_a \right) \vec{I}_3 - \mat{\Sigma}_a

And tada, there are the three relevant properties for each surface area: the
total area :math:`a`, the area centroid
:math:`\vec{r}_{\mathrm{A}/\mathrm{O}}`, and the inertia tensor
:math:`\mat{J}_{a/\mathrm{O}}`.


Volume
------

Now for the volume. For the purposes of computing the inertia properties of the
enclosed air, it is convenient to neglect the air intakes and treat the canopy
as a closed volume. Given this simplifying assumption, build another triangular
mesh that covers the entire canopy surface as well as the left and right wing
tip sections. For this derivation, it is essential that the points on each
triangle are ordered such that a right-handed traversal produces a normal
vector pointing out of the volume. It is also essential that the complete mesh
does not contain any holes, or the volume may be miscounted. Given a surface
triangulation over the closed canopy geometry using :math:`N` triangles, the
volume can be computed as follows.

First, treat each triangle as the face of a tetrahedron that includes the
origin. The signed volume of the tetrahedron formed by each triangle is given
by:

.. math::

   v_n =
      \frac{1}{6}
      \left(
         \vec{r}_{1,n} \cdot \vec{r}_{2,n}
      \right)
      \times \vec{r}_{3,n}

Given that the vertices of each triangle were oriented such that they satisfy
a right-hand rule, the sign of each volume will be positive if the normal
vector for each triangular face points away from the origin, and negative if
it points towards the origin. In essence the tetrahedrons "overcount" the
volume for triangles pointing away from the origin, then the triangles facing
the origin subtract away the excess volume. The final volume of the canopy is
the simple sum:

.. math::

   v = \sum^N_{n=1} v_n

For the volume centroid of each tetrahedron:

.. Divide by 4 since this implicitly includes the origin at <0,0,0>

.. math::

   \overline{\vec{v}}_n \defas \frac{1}{4} \sum^3_{i=1} \vec{r}_{i,n}

And the centroid :math:`\mathrm{V}` of the total volume with respect to the
canopy origin :math:`\mathrm{O}`:

.. math::

   \vec{r}_{\mathrm{V}/\mathrm{O}} = \frac{1}{v} \sum^N_{n=1} v_n \overline{\vec{v}}_n

Lastly, calculating the inertia tensor of the volume can be simplified by
computing the inertia tensor of a prototypical or "canonical" tetrahedron and
applying an affine transformation to produce the inertia tensor of each
individual volume.

First, given the covariance matrix of the "canonical" tetrahedron:

.. math::

   \mat{\hat{\Sigma}} \defas \begin{bmatrix}
      \frac{1}{60} & \frac{1}{120} & \frac{1}{120}\\
      \frac{1}{120} & \frac{1}{60} & \frac{1}{120}\\
      \frac{1}{120} & \frac{1}{120} & \frac{1}{60}
   \end{bmatrix}


Use the points in each triangle to define:

.. math::

   \mat{T}_n \defas
      \begin{bmatrix}
         | & | & | \\
         \vec{r}_{1,n} & \vec{r}_{2,n} & \vec{r}_{3,n}\\
         | & | & | \\
      \end{bmatrix}

The covariance of each tetrahedron volume is then:

.. math::

   \mat{\Sigma}_n = \left| \mat{T}_n \right| \mat{T}_n^T \mat{\hat{\Sigma}} \mat{T}_n

And the covariance matrix of the complete volume:

.. math::

   \mat{\Sigma}_v = \sum^N_{n=1} \mat{\Sigma}_n

And at last, the inertia tensor of the volume about the origin :math:`O` can
be computed directly from the covariance matrix:

.. math::

   \mat{J}_{v/O} = \mathrm{trace} \left( \mat{\Sigma}_v \right) \vec{I}_3 - \mat{\Sigma}_v


[[FIXME: make a table showing the six variables and their names. Well, nine
variables? There are upper and lower surfaces.]]


Apparent mass of a parafoil
===========================

This section presents Barrows' method for estimating the apparent mass matrix
of a wing with circular arc anhedral. The equations have been adapted to use
the standard notation of this paper. The terms derived in this section will be
added to the real mass of the canopy when running the paraglider dynamics
models. For a discussion of apparent mass effects, see
:ref:`paraglider_dynamics:Apparent Mass`.


Barrows Formulation
-------------------

This section needs to define the terms that will be needed by the dynamics
models:

* :math:`\mat{A}_{a/R}`: apparent inertia matrix with respect to some
  *reference point* :math:`R`. This matrix is comprised of a translational
  inertia part :math:`\mat{M}_a` and a rotational inertia part
  :math:`\mat{J}_{a/R}`.

* :math:`\vec{r}_{RC/R}`: roll center with respect to :math:`R`

* :math:`\vec{r}_{PC/RC}`: pitch center with respect to the *roll center*
  :math:`RC`

In this section, all vectors are assumed to be in the canopy coordinate system.

Some notes about Barrows' development:

* It assumes the foil is symmetric about the xz-plane (left-right symmetry)
  and about the yz-plane (fore-aft symmetry).

* It assumes the canopy arc is circular.

* It assumes a constant chord length over the entire span.

* It assumes constant thickness over the entire span.

* It assumes no chordwise camber.

* It assumes the chords are all parallel to the x-axis (which also means no
  geometric twist). This mostly isn't a problem since our coordinate system is
  defined by the central chord, the geometric torsion angles tend to be quite
  small, and twist tends to occur over segments which represent negligible
  volume compared to the bulk of the wing.

.. figure:: figures/paraglider/dynamics/barrows.*
   :name: barrows_diagram

   Geometry for Barrow's apparent mass equations.

Some initial definitions:

.. math::

   \begin{aligned}
     t   &= \text{Airfoil thickness.} \\
     h^* &= \frac{h}{b} \\
   \end{aligned}

First, the apparent mass terms for a flat wing of a similar volume, from
Barrows' equations 34-39:

.. math::

   \begin{aligned}
     m_{f11} &= k_A \pi \left( t^2 b / 4 \right) \\
     m_{f22} &= k_B \pi \left( t^2 c / 4 \right) \\
     m_{f33} &= \left[ \mathrm{AR} / \left( 1 + \mathrm{AR} \right) \right] \pi \left( c^2 b / 4 \right) \\
     \\
     I_{f11} &= 0.055 \left[ \mathrm{AR} / \left( 1 + \mathrm{AR} \right) \right] b S^2 \\
     I_{f22} &= 0.0308 \left[ \mathrm{AR} / \left( 1 + \mathrm{AR} \right) \right] c^3 S \\
     I_{f33} &= 0.055 b^3 t^2
   \end{aligned}

Where :math:`k_A` and :math:`k_B` are the "correction factors for
three-dimensional effects":

.. math::

   \begin{aligned}
     k_A &= 0.85 \\
     k_B &= 1.0
   \end{aligned}

Assuming the parafoil arc is circular and with no chordwise camber, use Barrows
equations 44 and 50 to compute the *pitch center* :math:`PC` and *roll center*
:math:`RC` as points directly above the *confluence point* :math:`C` of the
arc:

.. math::

   \begin{aligned}
     z_{PC/C}  &= -\frac{r \sin \left( \Theta \right)}{\Theta} \\
     z_{RC/C}  &= -\frac{z_{PC/C} \; m_{f22}}{m_{f22} + I_{f11}/r^2} \\
     z_{PC/RC} &= z_{PC/C} - z_{RC/C}
   \end{aligned}

Modifying the apparent mass terms from the flat wing to approximate the terms
for the arched wing, Barrows equations 51-55:

.. math::

   \begin{aligned}
     m_{11} &= k_A \left[ 1 + \left(\frac{8}{3}\right){h^*}^2 \right] \pi \left( t^2 b / 4 \right) \\
     m_{22} &= \frac{r^2 m_{f22} + I_{f11}}{z^2_{PC/C}} \\
     m_{33} &= m_{f33} \\
     \\
     I_{11} &= \frac{z^2_{PC/RC}}{z^2_{PC/C}} r^2 m_{f22} + \frac{z^2_{RC/C}}{z^2_{PC/C}} I_{f11} \\
     I_{22} &= I_{f22} \\
     I_{33} &= 0.055 \left( 1 + 8 {h^*}^2 \right) b^3 t^2
   \end{aligned}

The apparent mass and apparent moment of inertia matrices are then defined in
Barrows equations 1 and 17:

.. math::
   :label: apparent_mass_matrix

   \mat{M}_a \defas
     \begin{bmatrix}
       m_{11} & 0      & 0 \\
       0      & m_{22} & 0 \\
       0      & 0      & m_{33}
     \end{bmatrix}

.. math::
   :label: apparent_moment_of_inertia_matrix

   \mat{I}_a \defas
     \begin{bmatrix}
       I_{11} & 0      & 0 \\
       0      & I_{22} & 0 \\
       0      & 0      & I_{33}
     \end{bmatrix}

Define two helper matrices:

.. math::

   \mat{S}_2 \defas
     \begin{bmatrix}
       0 & 0 & 0 \\
       0 & 1 & 0 \\
       0 & 0 & 0
     \end{bmatrix}

.. math::

   \mat{Q} = \mat{S}_2 \crossmat{\vec{r}_{PC/RC}} \mat{M}_a \crossmat{\vec{r}_{RC/R}}

Where :math:`\crossmat{\vec{x}}` is the :ref:`cross-product matrix operator
<crossmat>`.

Using the helper matrices, use Barrows equation 25 to write the rotational
part of the apparent inertia matrix:

.. math::

   \mat{J}_{a/R} \defas
      \mat{I}
      - \crossmat{\vec{r}_{RC/R}} \mat{M}_a \crossmat{\vec{r}_{RC/R}}
      - \crossmat{\vec{r}_{PC/RC}} \mat{M}_a \crossmat{\vec{r}_{PC/RC}} \mat{S}_2
      - \mat{Q}
      - \mat{Q}^T

And the corresponding angular momentum of the apparent mass about :math:`R`,
using Barrows equation 24:

.. math::

   \vec{h}_{a/R} =
      \left(
         \mat{S}_2 \crossmat{\vec{r}_{PC/RC}} + \crossmat{\vec{r}_{RC/R}}
      \right) \mat{M}_a \vec{v}_{R/e} + \mat{J}_{a/R} \omega

And finally, the completed apparent inertia matrix with respect to the riser
connection point :math:`R`, from Barrows equation 27:

.. math::
   :label: apparent_inertia_matrix

   \mat{A}_{a/R} =
     \begin{bmatrix}
       \mat{M}_a & -\mat{M}_a \left( \crossmat{\vec{r}_{RC/R}} + \crossmat{\vec{r}_{PC/RC}} \mat{S}_2 \right) \\
       \left( \mat{S}_2 \crossmat{\vec{r}_{PC/RC}} + \crossmat{\vec{r}_{RC/R}} \right) \mat{M}_a & \mat{J}_{a/R}
   \end{bmatrix}

Plus the vectors necessary to incorporate :math:`\mat{J}_{a/R}` into the
final dynamics:

.. math::

   \vec{r}_{PC/RC} = \begin{bmatrix} 0 & 0 & z_{PC/RC}\end{bmatrix}

Linear momentum of the apparent mass:

.. math::
   :label: apparent_linear_momentum

   \vec{p}_{a/e} =
     \mat{M}_a \cdot \left(
       \vec{v}_{R/e}
       - \crossmat{\vec{r}_{RC/R}} \omega_{b/e}
       - \crossmat{\vec{r}_{PC/RC}} \mat{S}_2 \cdot \omega_{b/e}
     \right)

Angular momentum of the apparent mass about :math:`R`:

.. math::
   :label: apparent_angular_momentum

   \vec{h}_{a/R} =
     \left(
       \mat{S}_2 \cdot \crossmat{\vec{r}_{PC/RC}} + \crossmat{\vec{r}_{RC/R}}
     \right) \cdot \mat{M}_a \cdot \vec{v}_{R/e}
     + \mat{J}_{a/R} \cdot \omega_{b/e}


Notes to self
-------------

* If :ref:`paraglider_dynamics:Reference Point` said this section gives
  reasons that `R` should be in the xz-plane, then make sure this section
  covers that.

* Doesn't Barrows use the *principal axes*? See my comment at the end of the
  "Introduction" to Barrows' paper about the coordinate axes needing to be
  parallel to the principal axes. I think the fact that I'm assuming the wing
  has fore-aft and later symmetry is what allows me to use the canopy axes.

* I'm not crazy about the notation `\mat{A}_{a/R}`, but this matrix isn't like
  anything else in my paper so for now I'll leave it.


Paraglider Models
=================

[[**FIXME**: preview the models. Model `6a` is the most complete,
incorporating `A_{a/R}`. Models `6b` and `6c` are simpler but require
computing `r_{B/R}` before computing `A_{a/B}` (plus `B` is not strictly
a fixed point since air density changes); they are mostly useful for verifying
the implementations.]]


Model 6a
--------

This section describe a paraglider dynamics model with 6 degrees of freedom.
It uses a rigid-body assumption, and incorporates the effects of apparent
mass. The dynamics are computed with respect to the riser midpoint :math:`R`
instead of the wing center of mass :math:`B` because it avoids needing to
recompute the apparent inertia matrix whenever `B` changes. In this
derivation all vectors are in the canopy coordinate system :math:`c`, so the
vector coordinate systems are implicit in the notation.

The derivation develops the equations of motion by starting with derivatives
of linear and angular momentum. The derivation is largely based on the
excellent :cite:`hughes2004SpacecraftAttitudeDynamics`, although this section
uses this paper's version of Stevens' notation (see :ref:`symbols:Notation and
Symbols`).

An implementation of this model is available as :py:class:`Paraglider6a
<glidersim:pfh.glidersim.paraglider.Paraglider6a>` in the ``glidersim``
package. The ``glidersim`` package also includes :py:class:`Paraglider6b
<glidersim:pfh.glidersim.paraglider.Paraglider6b>` and :py:class:`Paraglider6c
<glidersim:pfh.glidersim.paraglider.Paraglider6c>`, which decouple the
translational and angular equations of motion by choosing the glider center of
gravity for the dynamics reference point, but do not incorporate the apparent
mass matrix.


Real mass only
^^^^^^^^^^^^^^

Start with the equations for the translational and angular momentum of the
body :math:`b` about the reference point :math:`R` as observed by the inertial
reference frame :math:`e`:

.. math::
   :label: model6a_p

   \begin{aligned}
     {\vec{p}_{b/e}}
       &= m_b \, \vec{v}_{B/e} \\
       &= m_b \left(
            {\vec{v}_{R/e}} + {\vec{\omega}_{b/e}} \times {\vec{r}_{B/R}}
          \right)
   \end{aligned}

.. ref: Stevens Eq:1.7-3 (pg36)

.. math::
   :label: model6a_h

   \vec{h}_{b/R} =
     m_b \, \vec{r}_{B/R} \times \vec{v}_{R/e}
     + \mat{J}_{b/R} \cdot \vec{\omega}_{b/e}

Compute the momentum derivatives in the inertial frame :math:`\mathcal{F}_e`
in terms of derivatives in the body frame :math:`\mathcal{F}_b`:

.. math::
   :label: model6a_momentum_derivatives1

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}}
       &= {^b \dot{\vec{p}}_{b/e}}
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e}

       &= m_b \left(
            {^b \dot{\vec{v}}_{R/e}}
            + {^b\dot{\vec{\omega}}_{b/e}} \times {\vec{r}_{B/R}}
            + {\vec{\omega}}_{b/e} \times {\cancelto{0}{^b \dot{\vec{r}_{B/R}}}}
          \right)
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e}

       &= m_b \left(
            {^b \dot{\vec{v}}_{R/e}}
            + {^b\dot{\vec{\omega}}_{b/e}} \times {\vec{r}_{B/R}}
          \right)
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e}

     \\

     {^e \dot{\vec{h}}_{b/R}}
       &= {^b\dot{\vec{h}}_{b/R}} + {\vec{\omega}_{b/e} \times \vec{h}_{b/R}}

       &= m_b \left(
            {\cancelto{0}{^b \dot{\vec{r}_{B/r}}}} \times \vec{v}_{R/e}
            + \vec{r}_{B/R} \times {^b \dot{\vec{v}_{R/e}}}
          \right)
          + {\mat{J}_{b/R} \cdot {^b \dot{\vec{\omega}}_{b/e}}}
          + {\vec{\omega}_{b/e} \times \vec{h}_{b/R}}

       &= m_b \, \vec{r}_{B/R} \times {^b \dot{\vec{v}_{R/e}}}
          + {\mat{J}_{b/R} \cdot {^b \dot{\vec{\omega}}_{b/e}}}
          + {\vec{\omega}_{b/e} \times \vec{h}_{b/R}}

   \end{aligned}

Relate the derivatives of momentum with respect to the inertial frame to the
net force on the body :math:`f_b` and the net moment on the body about the
reference point :math:`g_{b/R}`:

.. For angular momentum, see Stevens Eq:1.7-1 (pg35)

.. math::
   :label: model6a_momentum_derivatives2

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}} &= \mat{f}_b \\
     {^e \dot{\vec{h}}_{b/R}} + \vec{v}_{R/e} \times \vec{p}_{b/e} &= \mat{g}_{b/R}
   \end{aligned}

Where

.. math::

   \begin{aligned}
     \vec{f}_b &= {\vec{f}_{\textrm{b,aero}}} + {\vec{f}_{\textrm{b,weight}}} \\
     \vec{g}_{b/R} &= {\vec{g}_{\textrm{b,aero}}} + {\vec{r}_{B/R} \times {\vec{f}_{\textrm{b,weight}}}}
   \end{aligned}

Combining :eq:`model6a_momentum_derivatives1` and
:eq:`model6a_momentum_derivatives2` gives the final equations for the dynamics
of the real mass (solid mass plus the enclosed air) in terms of :math:`^b
\dot{\vec{v}}_{R/e}` and :math:`^b \dot{\vec{\omega}}_{b/e}`:

.. math::
   :label: model6a_dynamics_equations

   \begin{aligned}
      m_b \, {^b \dot{\vec{v}}_{R/e}}
      + m_b \, {^b \dot{\vec{\omega}}_{b/e}} \times \vec{r}_{B/R}
      &= \vec{f}_b
         - \vec{\omega}_{b/e} \times \vec{p}_{b/e}

      m_b \, \vec{r}_{B/R} \times {^b \dot{\vec{v}}_{R/e}}
      + \mat{J}_{b/R} \cdot {^b \dot{\vec{\omega}}_{b/e}}
      &= \vec{g}_{b/R} - \vec{\omega}_{b/e} \times \vec{h}_{b/R}
         - \vec{v}_{R/e} \times \vec{p}_{b/e}
   \end{aligned}

Rewriting the equations as a linear system:

.. math::
   :label: model6a_real_system

   \mat{A}_{r/R}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{R/e}} \\
     {^b \dot{\vec{\omega}}_{b/e}} \\
   \end{bmatrix}
   = \begin{bmatrix}
       \vec{b}_1\\
       \vec{b}_2\\
     \end{bmatrix}

Where:

.. math::

   \begin{aligned}
     \mat{A}_{r/R} &=
       \begin{bmatrix}
         {m_b \, \mat{I}_3} & {-m_b \crossmat{\vec{r}_{B/R}}} \\
         {m_b \, \crossmat{\vec{r}_{B/R}}} & {\mat{J}_{b/R}} \\
       \end{bmatrix} \\
     \\
     \vec{b}_1 &=
       \vec{f}_b - \vec{\omega}_{b/e} \times \vec{p}_{b/e} \\
     \vec{b}_2 &=
       \vec{g}_{b/R}
       - \vec{\omega}_{b/e} \times \vec{h}_{b/R}
       - \vec{v}_{R/e} \times \vec{p}_{b/e} \\
   \end{aligned}


Real mass + apparent mass
^^^^^^^^^^^^^^^^^^^^^^^^^

Writing the dynamics in matrix form not only makes it straightforward to solve
for the state derivatives, it also makes it easy to incorporate the apparent
inertia matrix from `Apparent mass of a parafoil`_. Adding the apparent
inertia into the system matrix and accounting for the translational and
angular apparent momentum produces:

.. math::
   :label: model6a_complete_system

   \begin{bmatrix}
     \mat{A}_{r/R} + \mat{A}_{a/R}
   \end{bmatrix}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{R/e}} \\
     {^b \dot{\vec{\omega}}_{b/e}} \\
   \end{bmatrix}
   = \begin{bmatrix}
       \begin{aligned}
          \vec{b}_3 \\
          \vec{b}_4
      \end{aligned}
     \end{bmatrix}

.. math::

   \begin{aligned}
     \vec{b}_3 &= \vec{b}_1 - \vec{\omega}_{b/e} \times \vec{p}_{a/e} \\
     \vec{b}_4 &=
       \vec{b}_2
       - {\vec{v}_{R/e} \times \vec{p}_{a/e}}
       - {\vec{\omega}_{b/e} \times \vec{h}_{a/R}}
       + {\vec{v}_{R/e} \times \left( \mat{M}_a \cdot \vec{v}_{R/e} \right) }
   \end{aligned}

Where :math:`\mat{A}_{a/R}` is the apparent inertia matrix from
:eq:`apparent_inertia_matrix`, :math:`\mat{M}_a` is the apparent mass matrix
from :eq:`apparent_mass_matrix`, and :math:`\vec{p}_{a/e}` and
:math:`\vec{h}_{a/R}` are the linear and angular apparent momentums from
:eq:`apparent_linear_momentum` and :eq:`apparent_angular_momentum`. The extra
term :math:`\vec{v}_{R/e} \times \left( \mat{M}_a \vec{v}_{R/e} \right)` is
necessary to avoid double counting the aerodynamic moment already accounted
for by the section pitching coefficients.

[[The final step is to compute the derivatives with respect to the inertial
frame so the simulator can integrate the derivatives to track the paraglider
position and orientation over time with respect to the tangent plane:

.. math::

   \begin{aligned}
      {^e \dot{\vec{v}_{R/e}}} &=
        {^b \dot{\vec{v}_{R/e}}}
        + \vec{\omega}_{b/e} \times \vec{v}_{R/e} \\
      {^e \dot{\vec{\omega}_{b/e}}} &= {^b \dot{\vec{\omega}_{b/e}}}
   \end{aligned}

FIXME: verify this explanation]]


Model 6b
--------

Following the same logic as `Model 6a`_, but targeting :math:`^b
\vec{v}_{B/e}` and using the momentum about the body center of mass :math:`B`
produces a simpler model with a diagonal system matrix, but at the cost of
requiring the body center of mass to be determined before computing the
apparent inertia matrix.

.. math::
   :label: model6b_p

   \vec{p}_{b/e} = m_b \, \vec{v}_{B/e}

.. math::
   :label: model6b_h

   \vec{h}_{b/B} = \mat{J}_{b/R} \cdot \vec{\omega}_{b/e}

Computing the inertial derivatives with respect to the body frame:

.. math::
   :label: model6b_momentum_derivatives1

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}}
       &= m_b \, {^b \dot{\vec{v}}_{R/e}}
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e} \\
     \\
     {^e \dot{\vec{h}}_{b/B}}
       &= \mat{J}_{b/B} \cdot {^b \dot{\vec{\omega}}_{b/e}}
          + \vec{\omega}_{b/e} \times \vec{h}_{b/B}
   \end{aligned}

Computing the momentum about the body center of mass simplifies the equation
for angular momentum:

.. math::
   :label: model6b_momentum_derivatives2

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}} &= \mat{f}_b \\
     {^e \dot{\vec{h}}_{b/B}} &= \mat{g}_{b/B}
   \end{aligned}

Combining :eq:`model6b_momentum_derivatives1` and
:eq:`model6b_momentum_derivatives2`: and rewriting as a linear system:

.. math::
   :label: model6b_real_system

   \begin{bmatrix}
     m_b & 0 \\
     0 & \mat{J}_{b/B}
   \end{bmatrix}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{B/e}} \\
     {^b \dot{\vec{\omega}}_{b/e}}
   \end{bmatrix}
   = \begin{bmatrix}
       \vec{f}_b - \vec{\omega}_{b/e} \times \vec{p}_{b/e} \\
       \vec{g}_{b/B} - \vec{\omega}_{b/e} \times \vec{h}_{b/B}
     \end{bmatrix}

The simulator was designed to integrate :math:`^e \dot{\vec{v}}_{R/e}`, not
:math:`^e \dot{\vec{v}}_{B/e}`:

.. math::

   \begin{aligned}
     \vec{v}_{R/e}
       &= \vec{v}_{B/e} + \vec{r}_{R/B} \times \vec{\omega}_{b/e} \\
     \\
     ^b \dot{\vec{v}}_{R/e}
       &= ^b \dot{\vec{v}}_{B/e}
          + \vec{r}_{R/B} \times ^b \dot{\vec{\omega}}_{b/e} \\
     \\
     ^e \dot{\vec{v}}_{R/e}
       &= ^b \dot{\vec{v}}_{R/e}
          + \vec{\omega}_{b/e} \times \vec{V}_{R/e}
   \end{aligned}


Model 6c
--------

Another option is to target :math:`^b \vec{v}_{R/e}` directly, but again using
the momentum about the body center of mass :math:`B`. Like `Model 6b`_ this
also produces a simpler dynamics model, but again at the cost of making it
less convenient to precompute the apparent inertia matrix.

Computing the inertial derivatives with respect to the body frame:

.. math::
   :label: model6c_momentum_derivatives1

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}}
       &= m_b \left(
            {^b \dot{\vec{v}}_{R/e}}
            + ^b \dot{\vec{\omega}}_{b/e} \times \vec{r}_{B/R}
          \right)
          + \vec{\omega}_{b/e} \times \vec{p}_{b/e}
     \\
     {^e \dot{\vec{h}}_{b/B}}
       &= \mat{J}_{b/B} \cdot {^b \dot{\vec{\omega}}_{b/e}}
          + \vec{\omega}_{b/e} \times \vec{h}_{b/B}
   \end{aligned}

Computing the momentum about the body center of mass simplifies the equation
for angular momentum:

.. math::
   :label: model6c_momentum_derivatives2

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}} &= \mat{f}_b \\
     {^e \dot{\vec{h}}_{b/B}} &= \mat{g}_{b/B}
   \end{aligned}

Combining :eq:`model6c_momentum_derivatives1` and
:eq:`model6c_momentum_derivatives2`: and rewriting as a linear system:

.. math::
   :label: model6b_real_system

   \begin{bmatrix}
     m_b & -m_b \crossmat{\vec{r}_{B/R}} \\
     0 & \mat{J}_{b/B}
   \end{bmatrix}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{B/e}} \\
     {^b \dot{\vec{\omega}}_{b/e}}
   \end{bmatrix}
   = \begin{bmatrix}
       \vec{f}_b - \vec{\omega}_{b/e} \times \vec{p}_{b/e} \\
       \vec{g}_{b/B} - \vec{\omega}_{b/e} \times \vec{h}_{b/B}
     \end{bmatrix}


Model 9a
--------

[[**FIXME**: this derivation is currently broken and incomplete. Needs to be
updated to match the implementation, which also includes the apparent mass.]]

Similar to `Model 6a`_, this design uses the riser connection midpoint `R` as
the reference point for both the body and the payload, which simplifies
incorporating the apparent mass matrix. However, this model treats the body
and payload as separate components, connected by a rotational spring-damper
model that add an additional three degrees-of-freedom. A similar 9DoF model
derivation can be found in :cite:`gorman2012EvaluationMultibodyParafoil`
(9DoF, but relative roll and pitch are unconstrained) or
:cite:`slegers2010EffectsCanopypayloadRelative` (8DoF model that allows
relative pitch and yaw but not relative roll).

.. FIXME: why didn't I use that derivation?

An implementation of this model is available as :py:class:`Paraglider9a
<glidersim:pfh.glidersim.paraglider.Paraglider9a>` in the ``glidersim``
package. The ``glidersim`` package also includes :py:class:`Paraglider9b
<glidersim:pfh.glidersim.paraglider.Paraglider9b>`, which uses the centers of
mass as the reference points for the body and payload dynamics. That choice
simplifies the derivatives for angular momentum (since it eliminates the
moment arms), but it makes it more difficult to incorporate the effects of
apparent mass.


Real mass only
^^^^^^^^^^^^^^

Start with the equations for the translational and angular momentum of the
body :math:`b` about the reference point :math:`R` as observed by the inertial
reference frame :math:`e`:

.. math::
   :label: model9a_body_p

   \begin{aligned}
     {\vec{p}_{b/e}}
       &= m_b \, \vec{v}_{B/e} \\
       &= m_b \left(
            {\vec{v}_{R/e}} + {\vec{\omega}_{b/e}} \times {\vec{r}_{B/R}}
          \right)
   \end{aligned}

.. math::
   :label: model9a_payload_p

   \begin{aligned}
     {\vec{p}_{p/e}}
       &= m_p \, \vec{v}_{P/e} \\
       &= m_p \left(
            {\vec{v}_{R/e}} + {\vec{\omega}_{b/e}} \times {\vec{r}_{P/R}}
          \right)
   \end{aligned}


.. math::
   :label: model9a_body_h

   \vec{h}_{b/R} =
     m_b \, \vec{r}_{B/R} \times \vec{v}_{R/e}
     + \mat{J}_{b/R} \cdot \vec{\omega}_{b/e}

.. math::
   :label: model9a_payload_h

   \vec{h}_{p/R} =
     m_p \, \vec{r}_{P/R} \times \vec{v}_{R/e}
     + \mat{J}_{p/R} \cdot \vec{\omega}_{p/e}

Relate the derivatives of momentum with respect to the inertial frame to the
net forces and moments:

.. For angular momentum, see Stevens Eq:1.7-1 (pg35)

.. math::
   :label: model9a_momentum_derivatives1

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}} &= \mat{f}_b^b \\
     {^e \dot{\vec{h}}_{b/R}} + \vec{v}_{R/e} \times \vec{p}_{b/e} &= \mat{g}_b^b - \vec{g}_R^b \\
     {^e \dot{\vec{p}}_{p/e}} &= \mat{f}_p^p \\
     {^e \dot{\vec{h}}_{p/R}} + \vec{v}_{R/e} \times \vec{p}_{p/e} &= \mat{g}_p^p + \vec{g}_R^p \\
     \\
     \vec{f}_b^b &= \vec{f}_{\textrm{wing,aero}}^b + \vec{f}_{\textrm{wing,weight}} \\
     \vec{g}_b^b &= \vec{g}_{\textrm{wing,Cm}}^b + \vec{g}_{\textrm{wing,f}}^b \\
     \vec{f}_p^p &= \vec{f}_{\textrm{payload,aero}}^p + \vec{f}_{\textrm{payload,weight}} \\
     \vec{g}_p^p &= \vec{g}_{\textrm{payload,Cm}}^p + \vec{g}_{\textrm{payload,f}}^p \\
   \end{aligned}

[[Where :math:`\vec{f}_{\textrm{wing,aero}}` and
:math:`\vec{f}_{\textrm{payload,aero}}` may have contributions from both
aerodynamic moments as aerodynamic forces applied at some lever arm.]]

Compute the two momentum derivatives:

.. math::
   :label: model9a_momentum_derivatives2

   \begin{aligned}
     {^e \dot{\vec{p}}_{b/e}}
       &= m_b \left(
            {^e \dot{\vec{v}}_{R/e}}
            + {^e\dot{\vec{\omega}}_{b/e}} \times {\vec{r}_{B/R}}
            + {\vec{\omega}_{b/e}} \times {^e\dot{\vec{r}}_{B/R}}
          \right)

       &= m_b \left(
            {^b\dot{\vec{v}}_{R/e}}
            + {\vec{\omega}_{b/e}} \times {\vec{v}_{R/e}}
            + {^b\dot{\vec{\omega}}_{b/e}} \times {\vec{r}_{B/R}}
            + {\vec{\omega}_{b/e}} \times \left(
               {\cancelto{0}{^b \dot{\vec{r}}_{B/R}}}
               + {\vec{\omega}_{b/e}} \times {\vec{r}_{B/R}}
              \right)
          \right)

       &= m_b \left(
            {^b\dot{\vec{v}}_{R/e}}
            + {\vec{\omega}_{b/e}} \times {\vec{v}_{R/e}}
            + {^b\dot{\vec{\omega}}_{b/e}} \times {\vec{r}_{B/R}}
            + {\vec{\omega}_{b/e}} \times {\vec{\omega}_{b/e}} \times {\vec{r}_{B/R}}
          \right)

       &= m_b \left(
            {^b\dot{\vec{v}}_{R/e}}
            + {^b\dot{\vec{\omega}}_{b/e}} \times {\vec{r}_{B/R}}
          \right)
          + {\vec{\omega}_{b/e}} \times {\vec{p}_{b/e}}

     {^e \dot{\vec{h}}_{b/R}}
       &= {^b\dot{\vec{h}}_{b/R}} + {\vec{\omega}_{b/e} \times \vec{h}_{b/R}}

       &= {\mat{J}_{b/R} \cdot {^b \dot{\vec{\omega}}_{b/e}}}
          + {\vec{\omega}_{b/e} \times \vec{h}_{b/R}}

   \end{aligned}

The momentum derivatives for the payload follow the same derivation. Final
equations for the dynamics of the real mass (solid mass plus the enclosed air)
in terms of :math:`^b \dot{\vec{v}}_{R/e}`, :math:`^b
\dot{\vec{\omega}}_{b/e}`, :math:`^b \dot{\vec{\omega}}_{p/e}^p`, and
:math:`\vec{f}_R^b`:

[[**FIXME**: verify, derivative wrt `b`? If so, I should show those
derivatives as well, that's not obvious.]]

.. math::
   :label: model9a_dynamics_equations

   \begin{aligned}
      m_b \, {^b \dot{\vec{v}}_{R/e}}
      + m_b \, {^b \dot{\vec{\omega}}_{b/e}} \times \vec{r}_{B/R}
      &= \vec{f}_{\mathrm{net}}
         - \vec{\omega}_{b/e} \times \vec{p}_{b/e}

      m_b \, \vec{r}_{B/R} \times {^b \dot{\vec{v}}_{R/e}}
      + \mat{J}_{b/R} \cdot {^b \dot{\vec{\omega}}_{b/e}}
      &= \vec{g}_{\mathrm{net}} - \vec{\omega}_{b/e} \times \vec{h}_{b/R}
         - \vec{v}_{R/e} \times \vec{p}_{b/e}
   \end{aligned}

[[**FIXME**: these are the model6a dynamics]]

Rewriting the equations as a linear system:

.. math::
   :label: model9a_real_system

   \mat{A}_{r/R}
   \begin{bmatrix}
     {^b \dot{\vec{v}}_{R/e}^b} \\
     {^b \dot{\vec{\omega}}_{b/e}^b} \\
     {^b \dot{\vec{\omega}}_{p/e}^p} \\
     {^b \vec{f}_R^b}
   \end{bmatrix}
   = \begin{bmatrix}
       \vec{B}_1 \\
       \vec{B}_2 \\
       \vec{B}_3 \\
       \vec{B}_4
     \end{bmatrix}

Where:

.. math::

   \begin{aligned}
     \mat{A}_{r/R} &=
       \begin{bmatrix}
         {m_b \, \mat{I}_3} & {-m_b \crossmat{\vec{r}_{B/R}^b}} & {\mat{0}_{3\times3}} & {\mat{I}_3} \\
         {m_b \, \crossmat{\vec{r}_{B/R}^b}} & {\mat{J}_{b/R}^b} & {\mat{0}_{3\times3}} & {\mat{0}_{3\times3}} \\
         {m_p \, \mat{C}_{p/b}} & {\mat{0}_{3\times3}} & {-m_p \crossmat{\vec{r}_{P/R}^p}} & {-\mat{C}_{p/b}} \\
         {m_p \, \crossmat{\vec{r}_{P/R}^p}} \mat{C}_{p/b} & {\mat{0}_{3\times3}} & {\mat{J}_{p/R}^p} & {\mat{0}_{3\times3}} \\
       \end{bmatrix} \\
     \\
     \vec{B}_1 &=
       \vec{f}_b^b
       - \vec{\omega}_{b/e}^b \times \vec{p}_{b/e}^b \\
     \vec{B}_2 &=
       \vec{g}_b^b
       - \vec{g}_R^b
       - m_b \, \left( \vec{\omega}_{b/e}^b \times \vec{r}_{B/R}^b \right) \times \vec{v}_{R/e}^b
       - m_b \, \vec{r}_{B/R}^b \times \left( \vec{\omega}_{b/e}^b \times \vec{v}_{R/e}^b \right)
       - \vec{\omega}_{b/e}^b \times \left( \mat{J}_{b/R}^b \cdot \vec{\omega}_{b/e}^b \right)
       - \vec{v}_{R/e}^b \times \vec{p}_{b/e} \\
     \vec{B}_3 &=
       \vec{f}_p^p
       - m_p \mat{C}_{p/b} \cdot \left( \vec{\omega}_{b/e}^b \times \vec{v}_{R/e}^b \right)
       - m_p \, \vec{\omega}_{p/e}^p \times \left( \vec{\omega}_{p/e}^p \times \vec{r}_{P/R}^p \right) \\
     \vec{B}_4 &=
       \vec{g}_{p}^p
       + \vec{g}_R^p
       - m_p \, \left( \vec{\omega}_{p/e}^p \times \vec{r}_{P/R}^p \right) \times \vec{v}_{R/e}^p
       - m_p \, \vec{r}_{P/R}^p \times \mat{C}_{p/b} \cdot \left( \vec{\omega}_{b/e}^b \times \vec{v}_{R/e}^b \right)
       - \vec{\omega}_{p/e}^p \times \left( \mat{J}_p^p \cdot \vec{\omega}_{p/e}^p \right)
       - \vec{v}_{R/e}^p \times \vec{p}_{p/e}^p \\
   \end{aligned}

[[**FIXME**: need to describe `f_R` and `g_R`

The spring-damper connection produces forces and moments shared by the body
and the payload. There are six variables but only three degrees of freedom.
Both systems have the riser connection point :math:`R` at a fixed position,
and the force only exists to maintain the fixed relative positioning.

.. math::

   \vec{g}_R =
     \begin{bmatrix}
       \begin{aligned}
         \kappa_\phi \phi &+ \kappa_\dot{\phi} \dot{\phi} \\
         \kappa_\theta \theta &+ \kappa_\dot{\theta} \dot{\theta} \\
         \kappa_\gamma \gamma &+ \kappa_\dot{\gamma} \dot{\gamma} \\
       \end{aligned}
     \end{bmatrix}

Where :math:`\vec{\omega}_{p/b}^p = \left< \phi, \theta, \gamma \right>` are
the angular rates of the payload, :math:`^p \dot{\vec{\omega}}_{p/b}^p
= \left< \dot{\phi}, \dot{\theta}, \dot{\gamma} \right>` are the angular
accelerations of the payload, and the :math:`\kappa` are the stiffness and
dampening coefficients of the spring-damper model.

]]

[[**FIXME**: incorporate apparent inertia]]
