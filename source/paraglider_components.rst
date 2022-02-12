.. This chapter describes the three components of a paraglider (canopy, lines,
   and payload), defines their inputs, and provides parametric models for the
   inertial properties and resultant forces of each component.

.. FIXME: where do I define *control point*? The way I've worded tells the
   reader to expect explicit control points, not just vague descriptions of the
   component aerodynamics


****************
Component models
****************

A paraglider can be modeled as a :doc:`system <system_dynamics>` of three
components: a canopy, a harness, and suspension lines that connect the canopy
to the harness.

.. FIXME: add a figure to help visualize the 3 components?

To compute the dynamics of the composite system, each component model must
define three things:

1. Control inputs

2. Inertial properties

3. `Resultant force <https://en.wikipedia.org/wiki/Resultant_force>`__

This chapter develops basic models for each component, favoring simplicity
whenever possible. In particular, all models are based on a quasi-rigid body
assumption. [[FIXME: explain.]] This may seem like a major oversimplification,
but in practice it works quite well: although nearly every component of
a paraglider is made from highly flexible materials, they tend to remain
relatively rigid during typical flight conditions.


Canopy
======

.. What is the canopy? What does it do?

A paraglider canopy (or *parafoil*) is a kind of ram-air parachute: inflatable
lifting surfaces manufactured from nylon sheets with air intakes at the leading
edge that pressurize their internal volume. The shape of an inflated parafoil
is determined by a combination of surface materials, internal structure, air
pressure, and suspension lines. Because the canopy is flexible, pilots can
manipulate the suspension lines to change the shape of the canopy, allowing
them to control its aerodynamics.


.. How am I modeling it?

[[**FIXME: this paragraph is really wordy and hard to follow**]] To model
a parafoil, it is helpful to think of the canopy as a physical realization of
some idealized :doc:`foil geometry <foil_geometry>` that was optimized for
aerodynamic efficiency and stability. The physical wing is significantly more
complex since it must attempt to implement the target design using flexible
materials that deform once the canopy is pressurized (plus additional concerns
such as weight, physical reliability, manufacturability, etc), but the
deformations (cell billowing, profile flattening, surface wrinkling, etc) are
also exceptionally difficult to model without resorting to complete material
simulation :cite:`lolies2019NumericalMethodsEfficient`.

Instead, this model assumes that the idealized target geometry is an effective
representation of the physical canopy, then adds small empirical corrections
to account for the most significant error. It models the canopy volume with
smooth upper and lower surfaces, whose extents also serve to define the
section air intakes. It does not model individual cells, but it does
incorporate an estimate of the additional inertia from the internal ribs
between each cell. The only deformations included in the model are trailing
edge deflections due to pilot control inputs, which are accounted for with
precomputed section aerodynamic coefficients; it does not support manipulation
via load-bearing lines (used by pilots for maneuvers such as "big ears",
C-riser control, etc) or the *stabilo* lines (since the canopy is a rigid
model the wing tips can never cravat).

.. Technically, the foil design curves could be parametrized to implement
   time-dependent deformations, but in this paper the canopy is modeled as
   a quasi-rigid body.

.. Importantly, because it does not attempt to determine the shape based on
   line tensions there is no dependence on the :ref:`suspension line geometry
   <paraglider_components:Suspension lines>`.


.. Typically the upper surface of a paraglider wing wraps beyond the leading
   edge of the section profile, and the lower surface covers the region from
   the downstream edge of the air intakes until the trailing edge of the
   sections.

.. Most of the deformations invalidate the section coefficients and the
   assumptions of the numerical lifting-line method; models that handle foil
   deformations rely on full CFD modeling.


Controls
--------

.. How do pilots control the canopy?

A paraglider canopy is controlled by changing its shape through manipulation of
suspension lines. In theory, any of the suspension lines can be used to alter
the positions, orientations, or profiles of its wing sections, but this model
only supports trailing edge deflections produced by the lines connected to the
left and right brake handles.


.. How do you model the changes to the canopy shape?

When a pilot applies the :ref:`brakes <paraglider_components:Brakes>`, they
generate a continuous deformation along the trailing edge of the canopy. In
terms of the individual sections, this results in deformed variants of the
undeflected section profiles. Because this canopy model does not perform
material simulation, it requires that each variant has been precomputed and
assigned a unique *airfoil index* that associates it with a given brake input.
The choice of section index has a significant impact on the design of the
:ref:`suspension line <paraglider_components:Suspension lines>` model, and
should be chosen thoughtfully.


.. What is a good choice of index?

A simplistic (but not uncommon) approach is to model the trailing edge
deflection as a global rotation about some rotation point, and completely
ignore profile deformations. The airfoil index in this case is the deflection
angle measured between the deflected and undeflected chords. The rotation
point is typically implicit; for example, lifting-line models that assume
a fixed quarter-chord are implicitly rotating about the quarter-chord
position.

.. figure:: figures/paraglider/geometry/airfoil/deflected_airfoil_rotation.*
   :name: deflected_airfoil_rotation

   Deflection as a rotation of the entire profile.

By ignoring deformations of the profile geometry this model assumes the shape
of the aerodynamic coefficient curves do not change with brake deflections.
Instead, the deflection angle :math:`\delta_f` is added directly to the angle
of attack, meaning the control input produces a simple translation of the
section coefficients. The appeal of this model is the fact that it only
requires the section coefficient data from the undeflected profile.
Unfortunately, the accuracy of the model degrades rapidly as the deflection
angle is increased.

A more accurate model that is extremely common for wings built from rigid
materials is to use a discrete *flap* which rotates about a hinge point at
some fixed position along the chord:

.. figure:: figures/paraglider/geometry/airfoil/deflected_airfoil_hinge.*
   :name: deflected_airfoil_hinge

   Deflection as a rotation of a rigid flap about a fixed hinge point.

Fixed-hinge flaps are ubiquitous due to their simplicity and acceptable
accuracy for rigid wings. Unfortunately, this model is troublesome for
flexible wings because there are no fixed hinge points: parafoil edge
deflections develop as a variable arc, not a rigid rotation. Also, explicit
deflection angles are problematic because parafoil brake inputs cannot control
the deflection angles directly; they can only control the downward *deflection
distance* :math:`\delta_d` of the trailing edge:

.. figure:: figures/paraglider/geometry/airfoil/deflected_airfoil_arc.*
   :name: deflected_airfoil_arc

   Deflection as a vertical displacement of the trailing edge.

.. FIXME: is it safe to say that because the brakes pull nearly perpendicular
   to the chord that the decrease in brake line length is almost exactly equal
   to the deflection distance delta_d?

Because airfoils and section coefficients are conventionally normalized to
a unit chord, the natural choice of airfoil index for a parafoil is the
*normalized deflection distance* :math:`\overline{\delta_d}`, a function of
the *deflection distance* :math:`\delta_d` and the *chord length* :math:`c`:

.. math::
   :label: normalized deflection distance

   \overline{\delta_d} \defas \frac{\delta_d}{c}

The normalized deflection distances are unusual in that, although they are
control inputs to the canopy aerodynamics model, they are not direct inputs to
the system model. Instead, they are computed indirectly using values provided
by the :ref:`suspension lines <paraglider_components:Suspension lines>` and
the :doc:`foil geometry <foil_geometry>` so that the deflection distribution
along the span is a function of section index and brake inputs:

.. math::
   :label: spanwise normalized deflection distance

   \overline{\delta_d}\left(s, \delta_{bl}, \delta_{br} \right) =
     \frac
       {\delta_d \left(s, \delta_{bl}, \delta_{br} \right)}
       {c \left( s \right)}


.. FIXME: discussion

   * This model only defines the choice of section index; it does not specify
     how to generate the deflected profiles, which must be designed
     separately. This represents a significant extra step in the design
     process, but once a set of deformed profiles have been generated they can
     be reused for each canopy model. For an example set of deformed profiles,
     :ref:`demonstration:Section profiles`

   * This model assumes that a given vertical deflection distance will always
     produce a unique deflected profile (ie, the deformed profiles always take
     the same shape for a given value of :math:`\overline{\delta_d}`).


Inertia
-------

.. FIXME: point out that this model ignores trailing edge deflections when
   calculating the center of mass and rotational inertia

For a parafoil canopy in-flight, the effective inertia is produced by
a combination of three different masses: a *solid mass*, from the structural
materials, an *air mass*, from the air enclosed in the foil, and an *apparent
mass*, from the air surrounding the foil. (Some texts refer to the combination
of the solid and enclosed air masses as the *real mass*
:cite:`barrows2002ApparentMassParafoils`.)


Solid mass
^^^^^^^^^^

The *solid mass* is all the surface and structural materials that comprise the
canopy. A rigorous model would include the upper and lower surfaces, ribs,
half-ribs, v-ribs, horizontal straps, tension rods, tabs (line attachment
points), stitching, etc, but for this model the calculation is restricted to
the upper and lower surfaces and internal ribs. The internal ribs are assumed
to be solid (non-ported), resulting in an overestimate that is somewhat
mitigated by the absence of accounting for the other internal structures.

.. FIXME: discuss this simplification in :ref:`demonstration:Model`?

Assuming the material densities are uniform, the inertial properties of the
materials can be determined by first calculating the total area :math:`a` and
areal inertia matrix :math:`\mat{J}` for each surface (using the method in
:ref:`derivations:Area`), then scaling them by the areal densities :math:`\rho`
of each surface. The result is the total masses for the upper surface, lower
surface, and internal ribs:

.. math::
   :label: surface_masses

   \begin{aligned}
     m_{\mathrm{u}} &= \rho_{\mathrm{u}} a_{\mathrm{u}} \\
     m_{\mathrm{l}} &= \rho_{\mathrm{l}} a_{\mathrm{l}} \\
     m_{\mathrm{r}} &= \rho_{\mathrm{r}} a_{\mathrm{r}}
   \end{aligned}

And their mass moments of inertia about the canopy origin :math:`O`:

.. math::
   :label: surface_inertias

   \begin{aligned}
     \mat{J}_{\mathrm{u}/\mathrm{O}} &= \rho_{\mathrm{u}} \mat{J}_{a_u/\mathrm{O}} \\
     \mat{J}_{\mathrm{l}/\mathrm{O}} &= \rho_{\mathrm{l}} \mat{J}_{a_l/\mathrm{O}} \\
     \mat{J}_{\mathrm{r}/\mathrm{O}} &= \rho_{\mathrm{r}} \mat{J}_{a_r/\mathrm{O}}
   \end{aligned}

In theory the inertial properties are functions of the brake inputs since they
alter the distribution of mass, but in practice the effect is negligible. For
this project the centroids and moments of inertia for the solid mass are
calculated once using the undeflected section profiles.


Air mass
^^^^^^^^

Although the weight of the air inside the canopy is counteracted by its
buoyancy, it still represents significant mass. When the canopy is accelerated
the enclosed air is accelerated at the same rate, and must be included in the
inertial calculations. (This model neglects surface porosity; although the
canopy is porous, and thus constantly receiving an inflow of air through the
intakes, in a properly functioning wing the leakage is slow enough that the
volume of air can be treated as constant.)

Similar to the surface masses, the internal volume and its unscaled inertia
about the canopy origin is easily computed from the :doc:`foil_geometry` using
the method in :ref:`derivations:Volume`. Given the internal volume :math:`v`
and the current air density :math:`\rho_{\mathrm{air}}`, the total mass of the
enclosed air :math:`m_{\mathrm{air}}` is simply:

.. math::
   :label: air_mass

   m_{\mathrm{air}} = \rho_{\mathrm{air}} v

Similarly, for the inertia matrix of the enclosed air about the canopy origin
:math:`O`:

.. math::
   :label: air_inertia

   \mat{J}_{\mathrm{air}/O} = \rho_{\mathrm{air}} \mat{J}_{\mathrm{v}/\mathrm{O}}

.. FIXME: explicitly note that rho may be a function of time and position?


Apparent Mass
^^^^^^^^^^^^^

Newton's second law states that the acceleration of an isolated object is
proportional to the net force applied to that object:

.. math::

   a = \frac{\sum{F}}{m}

This simple rule is sufficient and effective for determining the behavior of
isolated objects, but when an object is immersed in a fluid it is longer
isolated. When an object moves through a fluid there is an exchange of
momentum, and so the momentum of the fluid must be taken into account as well.
In fact, it is this exchange of momentum that gives rise to the aerodynamic
forces on a wing. The difference is that apparent mass is an unsteady
phenomena that is not accounted for by simple aerodynamic models, such as
:ref:`foil_aerodynamics:Phillips' numerical lifting-line`.

In static scenarios, where the vehicle is not changing speed or direction
relative to the fluid, this exchange of momentum can be summarized with
coefficients that quantify the forces and moments on the wing due to air
velocity. But for unsteady flows, where the vehicle is accelerating relative
to the fluid, the net force on the vehicle is no longer simply the product of
the vehicle's "real" mass and acceleration. Instead, when a net force is
applied to an object in a fluid, it will accelerate more slowly than the
object would have in isolation, as if the vehicle has increased its mass:

.. math::

   a = \frac{\sum{F}}{m + m_a}

This *apparent mass* :math:`m_a` (or *added mass*
:cite:`thomasson2000EquationsMotionVehicle`) tends to become more significant
as the density of the vehicle approaches the density of the fluid. If the
density of the vehicle is much greater than the density of the fluid then the
effect is often ignored, but for lightweight aircraft the effect can be
significant.

.. Whether the apparent mass is significant depends only on the ratio `m
   / m_a`. If :math:`m \gg m_a` then no worries. However, `m` does depend on
   the density of the vehicle, and `m_a` does depend on the density of the
   fluid. But `m_a` also depends on the **shape** of the object and the
   relative velocity of the fluid. It's not a big deal, but careful how you
   word it.

Because apparent mass effects are the result of a volume in motion relative to
a fluid, its magnitude depends on the volume's shape and the direction of the
motion. Unlike the inertia due to real mass, apparent inertia is anisotropic,
and the diagonal terms of the apparent mass matrix are independent.
Calculating the apparent mass of an arbitrary geometry is difficult. For
a classic discussion of the topic, see :cite:`lamb1945Hydrodynamics`. For
a more recent discussion of apparent mass in the context of parafoils, see
:cite:`lissaman1993ApparentMassEffects`, which used an ellipsoid model to
establish a parametric form commonly used in parafoil-payload literature

This paper uses an updated method from
:cite:`barrows2002ApparentMassParafoils` which added corrections to the
ellipsoid model of :cite:`lissaman1993ApparentMassEffects`. (For a replication
of the equations in that method but given in the notation of this paper, see
:ref:`derivations:Apparent mass of a parafoil`.) The method uses several
significant simplifying assumptions (the dynamics reference point must lie in
the :math:`xz`-plane, the foil has circular arc, uniform thickness, uniform
chord lengths, etc), but the effects of deviations from the method's
assumptions are negligible for typical parafoil models.


Resultant force
---------------

.. FIXME: review, this is a very crude draft

A fast and effective method for estimating the canopy aerodynamics was
presented :ref:`earlier <foil_aerodynamics:Phillips' numerical lifting-line>`.
A significant advantage of that method is that it does not assume any
particular functional form of the aerodynamic coefficients (linear,
polynomial, etc), allowing their definition to use whatever form is
convenient. This model uses that flexibility to compose the section
coefficients as a two step process:

1. Pre-design the idealized airfoils associated with the range of trailing
   edge deflection, and estimate their aerodynamic coefficients.

2. Apply correction factors to individual sections to account for physical
   inaccuracies in the idealized airfoils.

The idealized airfoils are indexed by their normalized deflection distance
:eq:`normalized deflection distance`, which appears in Phillip' NLLT as the
control input :math:`\delta_i`; the indexed airfoils allow the brakes to
control the canopy aerodynamics with no modifications to the NLLT. Physical
inaccuracies refers to characteristics such as flattening, wrinkling, surface
roughness, air intakes, etc. For example, a common correction for parafoils is
to add an empirical estimate of the additional viscous drag due to air
intakes; see the :ref:`example model <demonstration:Surface materials>` for
a discussion.

.. FIXME: discussion?

   * Inherits the limitations of the aerodynamics method:

     * Assumes section coefficients are representative of entire wing segments
       (ignores inter-segment flow effects, etc)


The :ref:`aerodynamics model <foil_aerodynamics:Phillips' numerical
lifting-line>` provides the aerodynamic forces
:math:`\vec{f}_{f,\textrm{aero},n}` :eq:`section lift, 3D vortex lifting law`
and moments :math:`\vec{g}_{f,\textrm{aero},n}` :eq:`section moment` for the
:math:`N` foil sections.

.. math::
   :label: canopy weight

   \vec{f}_{f,\textrm{weight}} = m_p \vec{g}

.. math::
   :label: canopy aerodynamics aggregate

   \vec{f}_{f,\textrm{aero}} = \sum_{n=1}^{N} \vec{f}_{f,\textrm{aero},n}

.. math::
   :label: canopy moment

   \vec{g}_{f/R} =
     \sum_{n=1}^{N} \left( \vec{r}_{CP_n/R} \times \vec{f}_{f,\textrm{aero},n} \right)
     + \sum_{n=1}^{N} \vec{g}_{f,\textrm{aero},n}
     + \vec{r}_{S/R} \times \vec{f}_{f,\textrm{weight}}


Parameter summary
-----------------

In addition to the design curves that define the idealized
:doc:`foil_geometry`, the physical canopy model requires additional
information:

.. math::
   :label: canopy parameters

   \begin{aligned}
     \rho_u \qquad & \textrm{Areal density of the upper surface material} \\
     \rho_r \qquad & \textrm{Areal density of the internal rib material} \\
     \rho_l \qquad & \textrm{Areal density of the lower surface material} \\
     N_\textrm{cells} \qquad & \textrm{Number of internal cells} \\
     C_{D,\textrm{intakes}} \qquad & \textrm{Drag coefficient due to air intakes} \\
     C_{D,\textrm{surface}} \qquad & \textrm{Drag coefficient due to surface characterstics} \\
   \end{aligned}


Suspension lines
================

.. * Design parameters:

     * Brakes: start0, start1, stop0, stop1, kappa_b

     * Accelerator: kappa_A, kappa_C, kappa_x, kappa_z, kappa_a

   * Control inputs: delta_a, delta_bl, delta_br (produces delta_d)


.. What is the bridle? What does it do?

The suspension lines, or *bridle*, connect the canopy to the harness and
pilot. The lines are conventionally grouped into load-bearing sets (labeled
A/B/C/D, depending on their relative positions on the section chords), brake
lines (that produce the trailing edge deflections), and *stabilo* lines (that
assist in preventing the wing tips from curling into a dangerous *cravat*).
Starting from the canopy, the lines progressively attach together in
a *cascade* that terminates at two *risers* which connect the lines to the
harness. The bridle is responsible for producing the arc of the canopy,
suspending the harness at some position relative to the canopy, and allowing
the pilot to manipulate the shape of the canopy.


.. How am I modeling it?

For rigorous models the line geometry is a major factor in wing performance,
but for this project a fully-specified suspension line model would be both
tedious and redundant. It would be tedious because it would require the
lengths of every segment of every line, and it would be (mostly) redundant
because the :ref:`canopy model <paraglider_components:Canopy>` is
a quasi-rigid body whose *arc* is already defined by the :math:`yz`-curve of
the idealized foil geometry. As a result, the suspension lines can only affect
the riser position and trailing edge deflections, so this model can reasonably
use simple approximations that do not depend on an explicit line geometry.


.. What doesn't it model?

   * Load-bearing lines

   * *Stabilo* (the canopy is a rigid body so the wingtips can't cravat)

   * Chest riser strap width (the lines are quasi-rigid)

   * Weight-shift deformations

   * Line tensions (internal forces are irrelevant to the dynamics of a rigid
     body)

   * Spanwise connections (only considers the central A and C connections since
     the riser only moves in the xz-plane)



Controls
--------

The suspension lines provide two primary methods of controlling the paraglider
system: through brakes, which change the canopy aerodynamics, and the
accelerator, which repositions the payload underneath the canopy.


Brakes
^^^^^^

.. This model needs to provide :math:`\delta_d = f(s, \delta_{bl},
   \delta_{br})` as a function of independent left and right control inputs,
   :math:`0 \le \left\{ \delta_{bl}, \delta_{br} \right\} \le 1`. Earlier the
   canopy model said it needed this; see :eq:`normalized deflection distance`


A parafoil canopy can be manipulated by pulling on any of its many suspension
lines, but two of the lines in particular are dedicated to slowing the wing or
controlling its turning motion. Known as the *brakes* or *toggles*, these
controls induce downward trailing edge deflections (see
:numref:`deflected_airfoil_arc`) along each half of the canopy, increasing
drag on that side of the wing. Symmetric deflections slow the wing down, and
asymmetric deflections cause the wing to turn.

.. figure:: figures/paraglider/geometry/Wikimedia_Paragliding.jpg

   Asymmetric brake deflection.

   `Photograph <https://commons.wikimedia.org/wiki/File:Paragliding.jpg>`__  by
   Frédéric Bonifas, distributed under a CC-BY-SA 3.0 license.

.. figure:: figures/paraglider/geometry/Wikimedia_ApcoAllegra.jpg

   Symmetric brake deflection.

   `Photograph <https://commons.wikimedia.org/wiki/File:ApcoAllegra.jpg>`__ by
   Wikimedia contributor "PiRK" under a CC-BY-SA 3.0 license.

A physically accurate model of the deflection distribution would need to model
the length and angle of every line in the bridle and how the angles deform
during braking maneuvers. Because the line geometry was not a focus for this
project, an approximation is used instead.

First, observe that as brakes are progressively applied the deflections will
typically start near the middle and radiate towards the wing root and tip as
the brake magnitude is increased. For small brake inputs the deflections are
zero near the wing root and tip, but for large brake inputs even those
sections experience deflections.

To approximate this behavior, start by assuming the deflection distances from
each individual brake input are symmetric around some peak near the middle of
each semispan and vary as a quartic function :math:`q(p)`. Define the
polynomial coefficients such that the function value and slope are zero at
:math:`p = 0` and :math:`p = 1` and a peak at :math:`p = 0.5`. The result is
a quartic that is symmetric about :math:`p = 0.5` with a peak magnitude of
:math:`1`.

.. math::
   :label: quartic braking

   q(p) =
     \begin{cases}
       16p^4 - 32p^3 + 16p^2 &\mbox 0 \le p \le 1 \\
       0 & \mbox{else}
     \end{cases}

.. FIXME: compress the vertical scale of quartic.svg

.. figure:: figures/paraglider/geometry/quartic.svg
   :scale: 90%

   Truncated quartic distribution

Next define two variables for the section indices near the canopy root and tip
that control the start and stop points of the deflection. Representing the
start and stop positions as variables allows modeling how the deflection
distribution changes with the brake inputs. For both :math:`s_\textrm{start}`
and :math:`s_\textrm{stop}`, define their values when :math:`\delta_{br} = 0`
and :math:`\delta_{br} = 1`. Then, using linear interpolation as a function of
brake input:

.. math::
   :label: start stop indices

   \begin{aligned}
     s_\textrm{start} &=
       s_\textrm{start,0}
       + \left( s_\textrm{start,1} - s_\textrm{start,0} \right) \delta_b\\
     s_\textrm{stop} &=
       s_\textrm{stop,0}
       + \left( s_\textrm{stop,1} - s_\textrm{stop,0} \right) \delta_b
   \end{aligned}

The start and stop points can be used to map the section indices :math:`s` into
the domain of the quartic :math:`p`,  such that :math:`s = s_\textrm{start}
\rightarrow p = 0` and :math:`s = s_\textrm{stop} \rightarrow p = 1`:

.. math::
   :label: s2p

   p(s) = \frac{s - s_\textrm{start}}{s_\textrm{stop} - s_\textrm{start}}

The quartic output for each brake is unit magnitude, which should be scaled by
the brake input. Summing the two scaled outputs represent the fraction of
maximum brake deflection distance over the entire span. The maximum brake
deflection distance is a constraint set by the suspension line model parameter
:math:`\kappa_b`, the maximum length that the model will allow the pilot to
pull the brake line (although on a physical wing there isn't a clear limit to
how far the brakes can be pulled).

Finally, the total brake deflection distance is the sum of contributions from
left and right brake:

.. math::
   :label: total brake deflections

   \delta_d(s, \delta_{bl}, \delta_{br}) =
     \left(
       \delta_{bl} \cdot q(p(-s)) + \delta_{br} \cdot q(p(s))
     \right) \cdot \kappa_b

Together with the :doc:`foil_geometry`, the absolute brake deflection
distances can be used to compute each section's *airfoil index*
:eq:`normalized deflection distance`.


.. FIXME: discussion

   * Assumes the deflection distance is symmetric.

   * Accuracy depends on the arc anhedral.

   * Depending on the start and stop values, you might be able to create a model
     where a section's delta_d actually decreases?

   * For an example using the quartic model, see :ref:`demonstration:Brakes`.

   * This parameter is a convenient simplification: although the brake lines
     don't have a true "maximum length" (you can always "take a wrap"), they
     have an effective maximum length. Defining a maximum length allows
     simulations to use intuitive proportional controls instead of querying the
     model to determine the maximum lengths. The tradeoff is that you can never
     exceed this hard limit, but who cares?


Accelerator
^^^^^^^^^^^

.. FIXME: should I define :math:`\kappa_x`, :math:`\kappa_x`,
   :math:`\kappa_A`, and :math:`\kappa_C`, earlier than this? The accelerator
   control modifies `\kappa_A`, it doesn't own it.

.. Informal description

Paragliders are not powered aircraft, but pilots can increase their airspeed
by adjusting how the payload is positioned relative to the canopy. The
*accelerator* or *speed bar* is positioned under the pilot's feet, and by
pushing out they can shift the riser position :math:`RM` forward and up. The
canopy pitching angle, angle of attack, and airspeed must adjust to the new
equilibrium, changing both the airspeed and the glide ratio.

The goal is to model how the riser position changes as a function of the
accelerator control input :math:`0 \le \delta_a \le 1`.


.. Mathematical model

.. figure:: figures/paraglider/geometry/accelerator.*
   :name: accelerator_geometry

   Paraglider wing accelerator geometry.

For notational simplicity, define :math:`\overline{A}` and
:math:`\overline{C}` as the lengths of the lines connecting them to the riser
midpoint :math:`RM`:

.. math::

   \begin{aligned}
     \overline{A} &\defas \norm{\vec{r}_{A/RM}} \\
     \overline{C} &\defas \norm{\vec{r}_{C/RM}}
   \end{aligned}

The default lengths of the lines are defined by two pairs of design
parameters. First, the default position of the riser midpoint :math:`RM` is
defined with :math:`\kappa_x` and :math:`\kappa_z`; this is the position of
:math:`RM` when :math:`\delta_a = 0`. Second, two connection points along the
canopy root chord are defined with :math:`\kappa_A` and :math:`\kappa_C`;
connecting lines from these points are the physical means by which :math:`RM`
is positioned underneath the canopy. The :math:`A` lines connect near the
front of the wing, and are variable length; the pilot can use the
*accelerator* to shorten the lengths of these lines. The :math:`C` lines
connect towards the rear of the canopy, and are fixed length.

Geometrically, shortening :math:`\overline{A}` will move :math:`RM` forward
while rotating the :math:`C` lines. Aerodynamically, shortening
:math:`\overline{A}` effectively rotates the canopy pitch down about the point
:math:`C`, decreasing the global angle of incidence of the canopy; decreasing
the angle of incidence decreases lift, and the wing must accelerate to
reestablish equilibrium.

A fifth design parameter, the *accelerator length* :math:`\kappa_a`, is
required to define the maximum length change produced by the accelerator; this
is the maximum length that :math:`\overline{A}` can be decreased. This value
is limited by the physical geometry of the pulleys that give the pilot the
leverage to pull the canopy into its new position. The pilot uses the
*accelerator control input* :math:`\delta_a`, a value between 0 and 1, to
specify the total decrease in :math:`\overline{A}`:

.. math::
   :label: accelerator_length_A

   \overline{A}(\delta_a) = \overline{A_0} - \delta_a \kappa_a

For deriving the basic geometric relations, it is convenient to normalize all
the design parameters by the central chord. This avoids the extra terms in the
derivation and allows a wing design to scale naturally with the canopy.

The goal is to use the physical geometry, where the risers position is
determined by :math:`\overline{A}` and :math:`\overline{C}`, to define the
position of :math:`RM` a function of :math:`\delta_a`. The first step is to
determine the default line lengths by setting :math:`\delta_a = 0` and
applying the Pythagorean theorem:

.. math::
   :label: accelerator_initial

   \begin{aligned}
   \overline{A_0} &= \sqrt{\kappa_z^2 + \left( \kappa_x - \kappa_A \right) ^2}\\
   \\
   \overline{C_0} &= \sqrt{\kappa_z^2 + \left( \kappa_C - \kappa_x \right) ^2}
   \end{aligned}

In the general case, the line lengths are functions of :math:`\delta_a`:

.. math::
   :label: accelerator_geometry_line_lengths

   \begin{aligned}
   \overline{A}(\delta_a)^2 &= {RM}_z^2 + \left( {RM}_x - \kappa_A \right) ^2\\
   \\
   \overline{C}(\delta_a)^2 &= {RM}_z^2 + \left( \kappa_C - {RM}_x \right) ^2 = \overline{C_0}^2
   \end{aligned}

Where :math:`\overline{C} \equiv \overline{C_0}` due to the physical
constraint that the length of the :math:`C` lines are constant.

Subtract the two equations in :eq:`accelerator_geometry_line_lengths`:

.. math::

   \overline{A}(\delta_a)^2 - \overline{C_0}^2 =
      \left( {RM}_x - \kappa_A \right) ^2 - \left( \kappa_C - {RM}_x \right) ^2

Finally, substitute :eq:`accelerator_length_A` and solve for :math:`{RM}_x`
and :math:`{RM}_z` as functions of :math:`\delta_a`:

.. math::
   :label: accelerator_R_xz

   \begin{aligned}
   {RM}_x(\delta_a) &=
      \frac
         {\left( \overline{A_0} - \delta_a \kappa_a \right) ^2
          - \overline{C_0}^2 - \kappa_A^2 + \kappa_C^2}
         {2 \left( \kappa_C - \kappa_A \right)}\\
   \\
   {RM}_z(\delta_a) &=
      \sqrt{\overline{C_0}^2 - \left( \kappa_C - {RM}_x(\delta_a) \right) ^2 }\\
   \end{aligned}

The final position of :math:`RM` with respect to the leading edge (which is
also the origin of the canopy coordinate system), scaled by the length of the
central chord :math:`c_0` of the wing, is then:

.. math::
   :label: accelerator_R

   \vec{r}_{RM/LE}^b(\delta_a) =
      c_0 \cdot \left\langle -{RM}_x(\delta_a), 0, {RM}_z(\delta_a) \right\rangle

Where :math:`{RM}_x` was negated since the wing :math:`x`-axis is positive
forward.

.. FIXME: it's confusing that I mix RMx being positive for the derivation but
   negative for the wing. I've drawn the x-axis positive "forwards" in the
   diagram, but :eq:`accelerator_geometry_line_lengths` has it positive.

.. FIXME: discussion

   * This model assumes the accelerator does not change the arc or profiles.

   * This model uses the chord lines as the connection points, but for the
     physical wing the tabs are connected to the lower surfaces of the ribs.

   * :cite:`iosilevskii1995CenterGravityMinimal` and
     :cite:`benedetti2012ParaglidersFlightDynamics` discuss how positioning the
     center of mass impacts glider trim and stability.


Inertia
-------

This simplistic model assumes the inertia of the lines is negligible compared
to that of the canopy; in particular, inaccuracies in the simplified canopy
inertia are more significant than the line inertia, so this model simply
defines the translational and rotation inertia as zero.


Resultant force
---------------

Although the lines are nearly invisible compared to the rest of the wing, they
contribute a significant amount of aerodynamic drag. Because the total system
drag of a paraglider is relatively small, even a small increase can have
a large impact on sensitive characteristics such as glide ratio; in fact,
paraglider suspension lines contribute upwards of 20% of the total paraglider
system drag (:cite:`babinsky1999AerodynamicPerformanceParagliders`,
:cite:`kulhanek2019IdentificationDegradationAerodynamic`), and should not be
neglected.

.. How do you calculate the drag force?

This model does not provide an explicit line geometry, so it can't compute the
true line area distribution. Instead, it lumps the entire length of the lines
into configurable control points; for example, given the total line length and
average line diameter, the line area can be lumped into singularities such as
the centroid of line area for each semispan. As with other similar designs
:cite:`kulhanek2019IdentificationDegradationAerodynamic`, this model treats
the drag as isotropic (because the operating ranges of alpha and beta are so
small the line drag is effectively constant, and what little force exists
along the :math:`z`-axis is negligible compared to the lift of the canopy).
Given the total area :math:`S_\textrm{lines}` represented by each singularity
the total aerodynamic drag at some control point :math:`L` can be calculated
as in :cite:`kulhanek2019IdentificationDegradationAerodynamic` or
:cite:`babinsky1999AerodynamicPerformanceParagliders`:

.. math::
   :label: suspension lines total length

   S_l = \kappa_L \kappa_d

.. math:: :label: suspension lines aerodynamics, individual

   \vec{f}_{l,\textrm{aero},n} =
     \frac{1}{2}
     \rho_\textrm{air}
     \norm{\vec{v}_{W/L_n}}^2
     S_l
     C_{d,l,n}
     \hat{\vec{v}}_{W/L_n}

.. math:: :label: suspension lines aerodynamics, aggregate

   \vec{f}_{l,\textrm{aero}} = \frac{1}{N} \sum_{n=1}^{N} \vec{f}_{l,\textrm{aero},n}

.. math::
   :label: suspension lines moment

   \vec{g}_{l/R} =
     \frac{1}{N}
     \sum_{n=1}^{N}
     \vec{r}_{CP_n/R} \times \vec{f}_{l,\textrm{aero},n}


.. FIXME: I'm negelecting the weight of the lines


Parameter summary
-----------------

For the harness position:

.. math::

   \begin{aligned}
     \kappa_A \qquad & \textrm{Chord ratio to the A lines} \\
     \kappa_C \qquad & \textrm{Chord ratio to the C lines} \\
     \kappa_x \qquad & \textrm{Chord ratio to the } x\textrm{-coordinate of the riser midpoint} \\
     \kappa_z \qquad & \textrm{Chord ratio to the } z\textrm{-coordinate of the riser midpoint} \\
     \kappa_a \qquad & \textrm{Accelerator line length} \\
   \end{aligned}

For the brakes:

.. math::

   \begin{aligned}
     s_{\textrm{start},0}, s_{\textrm{start},1} \qquad
       & \textrm{Section indices where deflections begin for } \delta_b \in \{0, 1\} \\
     s_{\textrm{stop},0}, s_{\textrm{stop},1} \qquad
       & \textrm{Section indices where deflections end for } \delta_b \in \{0, 1\} \\
     \kappa_b \qquad & \textrm{Maximum trailing edge deflection distance} \\
   \end{aligned}

For the aerodynamics:

.. math::

   \begin{aligned}
     \kappa_L \qquad & \textrm{Total line length} \\
     \kappa_d \qquad & \textrm{Average line diameter} \\
     CP_n \qquad & \textrm{Lumped line point} \ n \\
     \vec{r}_{CP_n/R} \qquad & \textrm{Position of lumped point} n \\
     C_{d,l,} \qquad & \textrm{Line drag coefficient for control point} \ n \\
   \end{aligned}


Harness
=======

.. What is the harness? What does it do?

A paraglider harness is the seat for the pilot, which is suspended from the
risers. Safety straps over the legs and chest ensure the pilot cannot fall
from the harness in turbulent conditions or during unsteady maneuvers.
A tensioning strap in front of the pilot's chest controls the horizontal riser
separation distance, which allows the pilot to adjust the balance between
stability (sensitivity to turbulence) and wing responsiveness to weight shift
control. In addition to giving the pilot a safe place to sit, the harness also
provides places to store the pilot's gear, a pouch to contain the emergency
reserve parachute, and optional padding to protect the pilot in the event of
a crash.


.. How am I modeling it?

Instead of attempting to capture all the geometric irregularities of
paraglider harnesses, this model calls upon a time-honored solution from
physics: it considers the harness as a sphere. Moreover, the pilot, gear, and
reserve parachute are accounted for by simply adding their masses to the mass
of the harness. The harness, pilot, and gear are collectively referred to as
the *payload*.


Controls
--------

Paraglider harnesses allow pilots to shift their weight left and right, causing
an imbalanced load on each semispan. (For a real wing this maneuver also causes
a vertical shearing stress along the center of the foil, but due to the rigid
body assumption of the canopy model this deformation will be neglected.) The
weight imbalance causes the canopy to roll towards the shifted mass, resulting
in a gentle turn in the desired direction. Although the turn rate is less than
can be produced by the brakes, this maneuver causes less drag and is preferred
(when suitable) for its aerodynamic efficiency.

The movement of the pilot can be arguably described as occurring inside the
volume of the harness, so *weight shift* control can be modeled as
a displacement of the payload center of mass :math:`P`. Given that the pilot
can only shift a limited distance :math:`\kappa_w` in either direction,
a natural choice of control input is :math:`-1 \le \delta_w \le 1`. With the
harness initially centered in the canopy :math:`xz`-plane, the displacement due
to weight shift control is :math:`\Delta y = \delta_w \kappa_w`. The
displacement of the payload center of mass produces a moment on the risers that
rolls the wing and induces the turn.

Defining the riser midpoint :math:`RM` as the origin the harness-local
coordinate system, the position of the displaced center of mass is then:

.. math::
   :label: payload center of mass

   \vec{r}_{P/RM} = \bar{\vec{r}}_{P/RM} \, + \left< 0, \delta_w \kappa_w, 0 \right>


Inertia
-------

As in :cite:`virgilio2004StudyAerodynamicEfficiency` (and similarly in
:cite:`kulhanek2019IdentificationDegradationAerodynamic`), the payload is
modeled as a solid sphere of uniform density. With a total mass :math:`m_p`,
center of mass :math:`P`, and projected surface area :math:`S_p`, the moment
of inertia about the payload center of mass is simply:

.. math::

   \mat{J}_{p/P} =
     \begin{bmatrix}
       J_{xx} & 0 & 0 \\
       0 & J_{yy} & 0 \\
       0 & 0 & J_{zz}
     \end{bmatrix}

where

.. math::

   J_{xx} = J_{yy} = J_{zz} = \frac{2}{5} m_p r_p^2 = \frac{2}{5} \frac{m_p S_p}{\pi}


Resultant force
---------------

Harness drag coefficients were studied experimentally in
:cite:`virgilio2004StudyAerodynamicEfficiency`. The author measured several
harness models in a wind tunnel and converted the results into aerodynamic
coefficients normalized by the cross-sectional area of the sphere. For a more
sophisticated approach the coefficient can be adjusted to account
(approximately) for angle of attack and Reynolds number
:cite:`kulhanek2019IdentificationDegradationAerodynamic`, but this model
simply treats the drag coefficient as a constant.


.. math::
   :label: payload weight

   \vec{f}_{p,\textrm{weight}} = m_p \vec{g}

.. math::
   :label: payload aerodynamics

   \vec{f}_{p,\textrm{aero}} =
     \frac{1}{2} \rho_\textrm{air} \norm{\vec{v}_{W/P}}^2 S_p C_{D,p} \hat{\vec{v}}_{W/P}

.. math::
   :label: payload moment

   \vec{g}_{p/R} =
     \vec{r}_{CP/R} \times \vec{f}_{p,\textrm{aero}}
     + \vec{r}_{P/R} \times \vec{f}_{p,\textrm{weight}}


Note that the spherical nature of the model implies isotropic drag. Although
this is clearly a poor assumption for such a significantly non-spherical
object, the fact that the wind is rarely more than 15 degrees off the
:math:`x`-axis means the such a "naive" drag coefficient will remain fairly
accurate over the typical range of operation (regardless of the poor geometric
accuracy). This assumption also has the downside that it will never produce an
aerodynamic moment about the payload center of mass, but in the absence of
experimental data on the magnitude of the missing moment, this model continues
to ignore it.


Parameter summary
-----------------

.. math::

   \begin{aligned}
     m_p \qquad & \textrm{Total payload mass} \\
     \bar{\vec{r}}_{P/RM} \qquad & \textrm{Payload center of mass default position} \\
     \kappa_w \qquad & \textrm{Maximum weight shift distance} \\
     S_p \qquad & \textrm{Projected payload area} \\
     C_{d,p} \qquad & \textrm{Payload drag coefficient} \\
   \end{aligned}
