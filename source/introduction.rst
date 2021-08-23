************
Introduction
************

   *The following draft-only sections are summaries for Professor Slivovsky.*

Brief overview
--------------

This project develops a parametric model for composing paraglider system
dynamics models. To make it easy to model existing paraglider wings, it is
parametrized by the most readily available specification data. It provides all
three primary control inputs (brakes, accelerator, and weight shift) and
a nonlinear aerodynamics model that balances accuracy and computation time.
The output is a dynamics model that can (approximately) simulate commercial
paraglider wings under typical flight conditions.


Complete backstory
------------------

The motivating goal was to learn wind patterns from recorded paraglider
flights. The primary difficulty is that the flight records are position-only
time series data, so extracting wind information requires a causal
relationship between paraglider motion and the underlying wind field. That
causal link is provided by the paraglider dynamics. If the dynamics of the
paraglider that created a flight are known, it may be possible to use
statistical filtering to perform probabilistic flight reconstruction;
specifically, the problem requires generating probability distributions over
the paraglider state, control inputs, and wind vectors.

The first requirement is a dynamics model. Unfortunately, flight records do
not (typically) record what paraglider generated the data, so the dynamics
model itself is uncertain. Thus, performing flight reconstruction over a large
number of flight tracks needs needs not just a single dynamics model, it needs
an entire distribution of models. Generating models is hard, so the new goal
is to create a tool that can generate paraglider models from public technical
specs. Specifically, I wanted a parametrized model that provides a direct
mapping to the most easily/readily available wing data. To achieve that
I decomposed the paraglider into several components and developed a new foil
geometry model.

In terms of the modeling process, I used my own wing as a test case to guide
development; the final chapter will demonstrate the ability of this new tool
to produce a reasonably accurate model of my own wing using only public design
data, photos, and videos.

In terms of flight dynamics, I chose to require that the aerodynamics method
must support not only non-uniform wind vectors across the wing, but
non-uniform wind fields in general. The goal was to simulate an indirect
interaction with a thermal during a turn (since pilots frequently disagree on
wing behavior in that scenario, and I hoped to shed light on the situation).

.. How does it compare to existing models, like Benedetti? What did I do
   differently to justify creating my model?

   Models that assume you already know the total wing aerodynamic coefficients
   are out since those are unknown (and those are typically linear models
   ayway). An explicit goal of my project was to NOT assume linearity.
