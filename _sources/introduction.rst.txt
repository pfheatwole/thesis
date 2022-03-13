************
Introduction
************

.. What does this paper do? It creates parametric paraglider flight dynamics
   models.

The objective of this paper is to create a set of parametric models that can
estimate the system dynamics of commercial paraglider wings using only limited
technical specifications. These *flight dynamics models* describe the behavior
of a paraglider by computing the translational and angular acceleration of the
aircraft in response to the pilot control inputs and its interactions with the
environment.

.. figure:: figures/block0.svg

The models are composed as systems of parametric components. Each component
model is responsible for calculating the inertial properties and resultant
forces that the system model will use to compute the glider acceleration. The
fact that only summary data is available for commercial wings means that each
component must encode a large amount of structural knowledge to augment the
data, and provide carefully chosen structural parameters that can be estimated
from that data.

.. In particular, the objective of this paper is to produce paraglider flight
   dynamics models as systems of differential equations :math:`\dot{\vec{x}}
   = f(\vec{x}, \vec{u})`.


.. Context

   "Provides the full context in a way that flows from the opening."

Motivation
==========

.. Why does this paper create parametric paraglider flight dynamics models?

.. Establishing a research territory (Context): wind patterns help pilots

Paragliding is a recreational flying activity that uses a lightweight, flexible
wing for non-powered flight. Pilots are strapped into a harness suspended from
the wing by a network of flexible connecting lines, and control the glider by
manipulating the lengths of the suspension lines and shifting their weight
inside the harness. Because paragliders lack a motor, their motion is entirely
dictated by interactions with gravity and wind. If the air is ascending a pilot
can slow their descent, or even gain altitude; conversely, sinking air will
cause the wing to descend more quickly. The horizontal component of the wind
dictates the ground speed of the glider in a given direction, which determines
what regions of the air the pilot can access, and what landing zones they can
reach.

As a result, a successful flight depends on the pilot's ability to recognize
the structure of the local air currents and navigate them in order to achieve
their flight goals, which may include optimizing for flight time, distance, or
a particular route. Because a glider is constantly spending energy to
counteract the force of gravity, the pilot must recognize the wind structure as
quickly as possible to minimize energy loss. Experienced pilots assess the
nearby air currents by observing vegetation, birds, or other pilots, but they
can also leverage knowledge gained from previous flights; although local wind
configurations are difficult to predict in detail, they can exhibit recurring
patterns. By learning those patterns a pilot can assess the current wind
conditions more quickly and more accurately, and can prioritize flying to areas
that are likely to support their flight goals.


.. Don't dwell on flight reconstruction, but it does establish the importance
   of the project and the performance criteria of the resulting models.

Traditionally, wind patterns are discovered by pilots with a lot of flight time
in a particular area, and are shared directly from one pilot to another. For
the pilot community to learn reliable patterns, individual pilots must first
recognize a pattern and then be able to communicate it with precision. An
appealing alternative would be to aggregate recorded flight data from many
pilots over many flights, detect any wind patterns automatically from those
flights, and build a graphical map to communicate the features of the wind
field visually instead of relying on verbal descriptions. In support of this
idea, there already exist large databases with millions of recorded flights
spanning several decades from pilots who share their flights for personal and
competitive purposes. The difficulty with using those records is that most
flight devices only record a tiny amount of the information available to
a pilot; in fact, the average flight record can only be expected to include
a time series of positions. There is typically no information regarding the
orientation, velocity, acceleration, pilot control inputs, or the weather
conditions. Even the details of the aircraft are unknown (in most cases). The
ability to learn wind patterns from a set of flight records hinges on the
ability to estimate the structure of the wind field that was present during
individual flights using position-only data.


.. Establishing a niche (Problem and Significance): paraglider flight dynamics

The key to success is to recognize that although position is the only available
data, it is not the only available information: we also know that each flight
record was produced by a paraglider. That information — knowledge of the
dynamics of the system that produced the data — establishes a causal
relationship between the sequence of glider positions and the underlying wind
field. This is vital information, because given a causal model it may be
possible to perform statistical *flight reconstruction*. [[FIXME: finish; add
reference to the MH370 paper.]]


.. Occupying the niche (Response): parametric modeling

The need for a flight dynamics model of the paraglider that produced the data
is a major stumbling block: not only are the dynamics unknown, but the glider
itself is unknown. Flight reconstruction would require not just a single model,
but an entire distribution over all dynamics models that could have produced
the data. It is laborious to create a single model for a commercial paraglider,
much less an entire set of models, then there's the killing blow that the only
available wing data is a sparse collection of summary measurements. The
response taken in this project is to encode large amounts of structural
knowledge in parametric functions that can augment the data and eliminate large
portions of the modeling process.


Roadmap
=======

.. "Brief indication of how the thesis will proceed."

The modeling process begins by developing a novel :doc:`foil_geometry` tailored
for nonlinear shapes, enabling simple, parametric representations of typical
paraglider canopies. It then chooses a :doc:`foil_aerodynamics` method suitable
for the nonlinear geometry and typical flight conditions of a parafoil canopy,
and compares its estimates to experimental wind tunnel data. Next,
:doc:`paraglider_components` decomposes a paraglider into a system of
components, and develops parametric models for each component. Finally,
:doc:`system_dynamics` combine the components into complete dynamics models,
and :doc:`state_dynamics` selects a suitable set of state variables and defines
their derivatives in terms of the system dynamics. The paper concludes with
a collection of :doc:`demonstrations <demonstration>` that show how to estimate
the parameters of the component models for a commercial paraglider wing, how to
validate the model, and how the model can be used to study paraglider behavior.

.. FIXME: would this be better in a "goals, steps, results" format?
