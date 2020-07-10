**********
Case Study
**********

[[This is where I plan to show (1) how to use the software to implement a real
wing, (2) generate some performance curves for that wing, (3) compare it to
expectations.]]


Design
======

* TODO: Use my Hook3ish to demonstrate how to approximate a real-world wing
  using the components I've defined.


Static Analysis
===============

* Show the polar curves. Consider if they are reasonable.

* Discuss limits, like unknown airfoil, unknown true line positions, lack of
  a proper `LineGeometry` (so brake deflections and arc changes when
  accelerator is applied are both unknown), no cell billowing, etc etc.

* TODO: Compare the real versus apparent mass matrices. Consider the relative
  magnitudes and the likely effects from accounting for apparent inertia.


Dynamic Analysis
================

* TODO: What are the sink rates during a hard turn? What are the sink rates
  during a hard turn? See the DHV ratings guide,
  :cite:`wild2009AirworthinessRequirementsHanggliders`

* TODO: Consider it's response to "exiting accelerated flight". In Sec:4.5.1
  of the DHV ratings guide "Airworthiness requirements for hanggliders and
  paragliders", they measure how the wing respond to "exiting accelerated
  flight". According to that, it sounds like wings dive **forward** when the
  accelerator is abruptly released. For my current Hook3ish, the wing
  experiences **backwards** pitch. Is this because I'm neglecting changes to
  the canopy geometry? Or is it symptomatic of the fact that I assume the
  lines stay taught? Conceptually, when you quickly release the speedbar, the
  A lines will quickly extend; it takes some time for the harness to drop (or
  the wing to rise) enough to regain tension, so the wing is certainly going
  to behave in ways not modeled by my equations. Good to point out.

