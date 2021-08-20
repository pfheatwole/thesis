************
Introduction
************


This project develops a parametric model for composing paraglider system
dynamics. To make it easy to model existing paraglider wings, it is
parametrized by the most readily available specification data. It provides all
three primary control inputs (brakes, accelerator, and weight shift) and
a nonlinear aerodynamics model that balances accuracy and computation time.
The result is a dynamics model that can (approximately) simulate commercial
paraglider wings under typical flight conditions.


Complete backstory
------------------

The motivating goal was to learn wind patterns from recorded paraglider
flights. The primary difficulty is that the flight records are position-only
data, so extracting wind information requires a causal relationship between
paraglider motion and the underlying wind field. That causal link is provided
by the paraglider dynamics. If the dynamics of the paraglider that created
a flight are known, it may be possible to use statistical filtering to perform
probabilistic flight reconstruction; in this case, that would involve
generating probability distributions over the paraglider state, control
inputs, and wind vectors.

The first step is to obtain the dynamics model. To make things more difficult,
there are many different paraglider wings, and flight records do not
(typically) record what paraglider generated the data, so the dynamics model
itself is uncertain. Thus, performing flight reconstruction over a large
number of flight tracks needs needs not just a single dynamics model, it needs
an entire distribution of models. Generating individual models is hard, so the
new goal is to create a tool that can generate paraglider models from public
technical specs.

From a usability standpoint, a primary goal is to parametrize the model such
that it provides a direct mapping to the most easily/readily available wing
data. To encourage that, I decomposed the paraglider into three components
with minimal interfaces and assumptions, making it easy to swap component
models and include the variety of parafoil and paraglider knowledge from
literature.

In terms of the modeling process, I used my own wing as a test case to guide
development. The final chapter demonstrates the ability of this new tool to
produce a reasonably accurate model of my own wing using only public design
data, photos, and videos.

In terms of flight dynamics, a requirement was to support not only non-uniform
wind vectors across the wing, but non-uniform wind fields in general. The goal
was to simulate an indirect interaction with a thermal during a turn (since
pilots frequently disagree on wing behavior in that scenario, and I hoped to
shed light on the situation).

.. How does it compare to existing models, like Benedetti? What did I do
   differently to justify creating my model?

   Models that assume you already know the total wing aerodynamic coefficients
   are out since those are unknown (and those are typically linear models
   ayway). An explicit goal of my project was to NOT assume linearity.
