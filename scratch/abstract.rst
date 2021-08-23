Old abstract (2021-08-19)
=========================

It is trivial to produce an accurate estimate of the wind conditions that were
present during a paragliding flight: simply answering "somewhere between 0 and
5000 km/h" would suffice. However, although that answer is technically
correct, it is so imprecise that it is useless. The difficult task is to
improve the precision while maintaining the accuracy. If the flight is
in-progress then the estimate can be updated as the paraglider moves and
rotates in response to the wind, but what if the flight has finished and all
that remains is a record of its position over time? Is it possible to recover
usefully precise estimates of the wind from position-only flight data?
Developing that question is the motivation for this project. The ability to
recreate the wind conditions from individual flights would enable the
possibility of learning wind patterns from databases of recorded flights.

[[Originally I was using phrases like "demonstrate feasibility", but I never
did that. **Maybe I can use flight test cases to demonstrate different flight
scenarios that produce the same GPS track? Not the same as demonstrating
success, but might at least demonstrate feasibility.**]]

[[Elaborate: the purpose alone isn't good enough. **What were the outcomes?**
For example, the stages of the proposed processing pipeline; the paraglider
model; statistical learning methods for the model; simulated-based filtering
for the wind. How am I making clear advances towards immediate success, or
towards preparing future research for success?]]

[[Remember, the **motivation** of this paper is extracting wind patterns from
a set of flight records, but the **subject** of the paper is a parametric
paraglider dynamics model designed to approximate wings using only a minimal
amount of technical specification data.]]


Scratch abstract (2021-08-19)
=============================

Paraglider pilots rely on wind estimates to plan their flights. They improve
their estimates by learning from previous flights. At present, that learning
involves first-hand experience or word of mouth, but an enticing alternative
would be to discover wind patterns from recorded flight tracks. Unfortunately,
flight tracks only contain paraglider position data, so extracting information
about the wind would require a causal relationship between the wind and
paraglider motion.

The causal relationship between paraglider motion and the wind is given by the
paraglider aerodynamics. There are existing paraglider dynamics models in
literature, but they are insufficient for this task because they provide
incomplete control inputs, oversimplify the aerodynamics, and (in most cases)
are unable to predict the aerodynamics of paraglider canopies from basic
specification data.

This paper develops a parametric paraglider model with all three primary
control inputs (accelerator, brakes, and weight shift), a paraglider canopy
model that can rapidly approximate existing wings from minimal specification
data, and a nonlinear aerodynamics model suitable for typical flight
conditions. The resulting simulator should provide a basis for flight
reconstruction, as well as general simulation tasks.

.. ...such as adding info to heated internet forum debates about what happens
   when a paraglider has an indirect interaction with a thermal

Scratchwork
===========

Estimating wind vectors from a recorded flight track requires a causal
relationship between the wind vectors and paraglider position over time. That
causal relationship is provided by the paraglider dynamics, so flight
reconstruction requires a dynamics model of the paraglider that produced the
flight. [[**I've motivated the need for a single dynamics model.**]]

Unfortunately, in most cases the paraglider that produced the flight is
unknown, so performing flight reconstruction over arbitrary flight tracks
requires a distribution of dynamics models. Due to the computational costs of
a proper distribution over wing models, this is likely to be an empirical
distribution produced by a large set of models of paraglider wings that are
likely to have produced the flight tracks. [[**I've motivated the need for
MANY models.**]]

Creating paraglider models is time consuming, and is all the more difficult
because commercial wing manufacturers only provided summary specification
data. Relying on measurements to obtain complete geometries for many different
wings is infeasible; a more feasible goal is to produce a model that can
approximate the geometry using the summary specification data. The
specifications effectively *parametrize* the geometry, so creating wing models
using them requires a *parametric model*. [[**I've motivated the need for
a PARAMETRIC model to allow creating many individual models.**]]
