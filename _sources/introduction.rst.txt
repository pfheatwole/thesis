************
Introduction
************


.. Introduce the topic. What am I discussing?

   [[One paragraph description of paragliders and paragliding.]]

   Paragliding is a recreational flying activity that uses a lightweight,
   flexible wing for non-powered flight. Pilots are strapped into a harness
   suspended from the wing by a network of flexible connecting lines, and
   control the glider by manipulating the lengths of the suspension lines and
   shifting their weight inside the harness. Because paragliders lack a motor,
   their motion is entirely dictated by interactions with gravity and wind. If
   the air is ascending a pilot can slow their descent, or even gain altitude;
   conversely, sinking air will cause the wing to descend more quickly. The
   horizontal component of the wind dictates the ground speed of the glider in
   a given direction, which determines what regions of the air the pilot can
   access, and what landing zones they can reach.


.. ---------------------------------------------------------------------------

   Context

   What am I modeling? (Describe the physical system; see Benedetti Ch. 2):


Overview
========

.. At this point I've explained why I would like to create one. What does that
   process look like?

.. What is *dynamic simulation*?

   Define modeling, parametric modeling, dynamics modeling, dynamic simulation,
   and the steps involved with creating a dynamic simulation. This lets me
   explain the "parametric" and "modeling" parts of the title.

The objective of this paper is to create a set of parametric models that can
estimate the flight dynamics of commercial paraglider wings using only limited
technical specifications.

In this paper, *modeling* refers to creating a mathematical representation of
a physical characteristic or behavior. A *dynamics model* is a mathematical
function that computes the acceleration of an object given the forces that act
on it, as described by Newton's 2nd law of motion :eq:`Newtons_2nd`:

.. Classical dynamics

.. math::
   :label: Newtons_2nd

   \begin{aligned}
   \textrm{Translational} \qquad F &= ma \\
   \textrm{Angular} \qquad M &= J \alpha
   \end{aligned}

These equations show that to compute the translational acceleration :math:`a`
and the rotational acceleration :math:`\alpha`, a dynamics model requires:

1. The mass :math:`m` and mass moment of inertia :math:`J`

2. The forces :math:`F` and moments :math:`M`

For a paraglider, the forces and moments that act on it are determined by its
current velocity, the relative wind flowing past the glider, air density,
gravity, and the pilot control inputs. The motion that is produced are the
*flight dynamics*, and the equations that represent how those inputs produce
the accelerations are called a *flight dynamics model*:

.. figure:: figures/block0.svg

   Flight dynamics model block diagram

The purpose of these *flight dynamics models* is to enable *dynamic
simulations*. A *dynamic simulation* is when acceleration is integrated over
time to produce a record of the object's velocity and position. The ability to
simulate a system's behavior provides opportunities such as studying that
behavior, developing control models, and running statistical filtering
pipelines. In fact, the inspiration for this project was a question whether
statistical flight reconstruction could be used to recreate the wind fields
present during a paraglider flight given only a record of its position, in much
the same way as researchers attempted to locate the lost Malaysia Airlines
Flight 370 :cite:`davey2016BayesianMethodsSearch`.

The steps to producing a dynamic simulation can be summarized as follows:

1. Understand the physical system

2. Model its inertial properties and forces

3. Develop the equations of motion (Newton's 2nd law)

4. Integrate the equations of motion over time

The majority of the work for this project is in step 2 (estimating the inertial
properties and forces) because the estimation process requires accurate models
of the mass distribution and aerodynamics of each component of the glider.


.. attention:: The remainder of this chapter assumes a working familiarity with
   fundamental aerodynamics. For the necessary background to understand this
   work, the section of the "Related works" covering :ref:`related_works:Flight
   simulation` provides an overview and complete list of material that I found
   helpful.


Modeling challenges
===================

.. At this point I've explained the procedure in general.

.. What is unusual about paragliders compared to other wings?

The existence of this project suggests that existing (and freely available)
tools for aircraft simulations are inadequate for simulating paragliders. The
reason is that paragliders have a variety of unique characteristics that make
them difficult to model using tools built for conventional aircraft:

1. Highly curved shape

   Aerodynamics models must simplify the Navier-Stokes equations in order to
   produce a tractable system of equations. Those simplifications frequently
   make them incapable of representing the flow field around a nonlinear wing.

2. Low airspeed

   Paraglider airspeeds are typically in the range 24–72 [km/h]. They also have
   relatively short wing sections, with chord lengths ranging from 0.5–3 [m].
   These characteristics combined with the reduced airspeed at the inside
   wingtip during a turn means that the canopy (and the wing tips in
   particular) are frequently operating at Reynolds values in the 300k range,
   far below the :math:`Re = 10^6` range where where viscous effects start to
   become significant.

3. High angles of attack

   Compounding the issue of operating at low Reynolds values, paragliders
   frequently operate at high angles of attack, leading to flow separation and
   the dramatic nonlinear aerodynamic behavior that results. As they approach
   stall conditions, simple aircraft simulators that rely on linear
   aerodynamics can dramatically overestimate the true lift produced by the
   wing.

4. Flexible

   Paragliders are constructed from flexible nylon sheets and rely on air
   pressure and suspension lines to maintain their shape. Their internal cells
   billow and wrinkle while the canopy twists and bends in the wind. It can
   even collapse entirely. Systems that rely on a predetermined geometry are
   fundamentally incapable of modeling such behavior.

5. Air intakes

   To produce the internal pressure that forms the canopy, paragliders use air
   intakes at the leading edge which pressurize its volume. These air intakes
   violate the expected pressure gradients predicted by analyses that use the
   idealized airfoils used to define the section profiles. As a result,
   theoretical aerodynamic coefficients underestimate the section drag.

6. Lightweight

   A paraglider canopy is a large volume with a small amount of solid mass. Its
   low density means that a naive application of Newton's 2nd law will
   overestimate acceleration because it fails to account for the momentum of
   the fluid surrounding the glider, an effect known as *apparent mass*.

In addition to these characteristics, there is another issue that is relatively
unique to gliding aircraft:

7. Pilots care about the details of the wing behavior in non-uniform wind
   fields.

   The reason is that glider pilots rely on the ability to determine the
   structure of the wind field by sensing the imbalanced forces produced by
   differences in relative wind vectors across the wing.

Each of these characteristics introduce modeling challenges. The modeling
requirements will depend on which of these characteristics the dynamics model
attempts to capture.


Modeling requirements
=====================

.. What do I want?

The nuances of paraglider behavior are dominated by subtle interactions. The
design philosophy for this project was to avoid simplifying assumptions
whenever reasonable to avoid accidentally masking those subtle interactions.
This approach was driven by a desire to answer questions such as:

* How much drag comes from each individual component?

* How important are section-specific Reynolds values?

* How important is apparent mass?

* How does a paraglider react when one side of the wing is in a stronger
  thermal than the other side?


.. Which characteristics do I care about for this project? These establish the
   criteria that will be used to critique the related works, and for modeling
   decisions such as which aerodynamics model I choose.

The desire for accuracy must be balanced with practical limitations, choosing
which characteristics to include and which to simplify away. Having considered
the tradeoffs, this project chose the following set of modeling requirements,
beginning with the fundamental `challenges <Modeling challenges>`_ of the
previous section:

1. The aerodynamics method must use the true, nonlinear geometry. It must not
   flatten the canopy geometry in any dimension.

2. The aerodynamics method must support variable Reynolds values.

3. The aerodynamics method must provide graceful degradation as it approaches
   high angles of attack. (A decrease in accuracy is acceptable, but assuming
   linear aerodynamics up to high alpha is not. The goal is to fly the wing
   into strong thermals which will rapidly increase angle of attack, so the
   method must at least approximate those conditions.)

4. Canopy deformations due to flexibility will be neglected. This means that
   glider controls that use non-brake-line manipulations will also be neglected
   (since they rely on canopy deformations).

5. The aerodynamics method must support empirical viscous correction factors to
   mitigate the issues caused by a mismatch between the theoretical and actual
   section profiles.

6. The system model must support apparent mass (in order to verify its
   significance).

7. The aerodynamics method must support non-uniform vectors along the span.

In addition to those characteristic behaviors, this project had an additional
goal:

8. Computationally fast

   The fundamental goal of this project is to enable people to create models of
   commercial paraglider wings, and that process requires iteration, so the
   software should pursue simulation speed that would allow rapid iteration.


Roadmap
=======

.. "Brief indication of how the thesis will proceed."

The majority of this work is spent producing the models that estimate the
inertial properties and resultant forces for each component, but it also
develops the additional models necessary to generate flight simulations. For
reference, a complete flight simulation architecture is shown in
:numref:`block_simulator`. This paper will develop everything inside the "State
dynamics" block.

.. figure:: figures/diagram_block_simulator.svg
   :width: 50%
   :name: block_simulator

   Flight simulation block diagram

The modeling process begins by developing a novel :doc:`foil_geometry` with
increased flexibility compared to other open source wing modeling tools,
enabling simple, parametric representations of typical paraglider canopies. It
then chooses a :doc:`foil_aerodynamics` method that satisfies those `Modeling
requirements`_ that relate to the canopy aerodynamics. Next, it develops a set
of parametric :doc:`paraglider_components` using parametrizations that simplify
creating models of commercial paraglider systems. Finally,
:doc:`system_dynamics` models combine the components into complete flight
dynamics models, and :doc:`state_dynamics` shows how to define the derivatives
of a set of state variables in terms of those system dynamics. Having completed
the model derivations, the paper provides a complete :doc:`demonstration
<demonstration>` of how they can be used to model a commercial paraglider wing.
The penultimate chapter provides :doc:`validation` data of the aerodynamics
method by comparing wind tunnel measurements for a scale-model paraglider wing
against simulated results, as well as comparing simulated polar curves for the
:doc:`demonstration <demonstration>` model against basic flight test data.
Finally, the :doc:`conclusion` revisits the questions from the `Modeling
requirements`_ and proposes how this material may be used in future work.
