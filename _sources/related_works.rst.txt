Related works
=============

.. This literature review should establish my work in the greater context. The
   goal is to create flight dynamics models using component models, so I need
   to discuss discuss existing methods/models for: paraglider system dynamics,
   foil geometries, foil aerodynamics, paraglider component models, etc.


Flight simulation
-----------------

.. 1. Foundational knowledge for building a flight simulator

   (This reflects the structure I defined in `introduction:Overview`)

This paper develops paraglider flight dynamics models that can be used for
flight simulation, which means that this paper is built on the foundations of
flight simulation. Flight simulation is simply the specific name of a dynamic
simulation that involves a flight dynamics model, and developing a flight
dynamics model follows the structure outlined in the
:ref:`introduction:Overview`: understand the system, model the inertia and
forces, develop the equations of motion, and integrate them over time.


.. 1a. Aircraft design (understand the system)

The first step to creating a model of an aircraft is a familiarity with the
physical system and how it behaves. Key concepts in the context of this paper
include characteristics of wing geometry; conventions for axes and relative
motion; flow angles (angle of attack and sideslip); aerodynamic coefficients;
and control inputs, actuators, and surfaces. An approachable starting point is
:cite:`gudmundsson2014GeneralAviationAircraft`, which provides a thorough
discussion of the terminology and significance of the major wing design
characteristics. Another ubiquitous resource is
:cite:`anderson1999AircraftPerformanceDesign`, which may be more suitable to
in-depth study.


.. 1b. Aerodynamics (the key physics of the system)

Next, to model a behavior you must be able to explain the behavior. The unique
characteristic of aircraft dynamics is that they experience aerodynamic forces
due to their motion relative to the air. The aerodynamic forces on the surfaces
of an aircraft are the results of the geometry, relative motion, and
characteristics of the fluid. Key concepts include the characteristics of the
flow (inviscid versus viscous, laminar versus turbulent, compressibility, etc)
and the modeling intuition of Prandtl's seminal work on boundary layers
:cite:`anderson2005LudwigPrandtlBoundary` (both 2D and 3D, which are vital to
understanding some of the aerodynamic difficulties in simulating flow around
a paraglider canopy). When selecting and working with aerodynamics models, it
is highly beneficial to have a general awareness of the complexity of
Navier-Stokes, and how the variety of aerodynamics models are the result of
attempts to produce tractable systems of equations by applying different
simplifying assumptions. An excellent introduction to these topics is
:cite:`bertin2014AerodynamicsEngineers`, which provides an approachable
introduction to the underlying physics, overviews of the core aerodynamic
models, and how they're derived. Another prevalent work is
:cite:`anderson2017FundamentalsAerodynamics` (or any of Anderson's works). For
more targeted discussions, :cite:`drela2014FlightVehicleAerodynamics` provides
clear insight into the theoretical details of common aerodynamics models, and
:cite:`cummings2015AppliedComputationalAerodynamics` provides a guide to their
computational aspects. For a less conventional approach,
:cite:`mclean2012UnderstandingAerodynamicsArguing` provides a unique
perspective of these aerodynamics models and the assumptions that underlie
them, including an excellent discussion of some issues with the NLLT that may
shed light on the difficulties that arise when using that approach.


.. 1c. System dynamics (equations of motion)

Once the inertial properties, forces, and moments can be determined, they must
be synthesized into a complete system dynamics model, which in this case are
known as the *equations of motion*. Unlike the simple equations in the
:ref:`introduction:Overview`, the equations describing the translational and
angular accelerations of an aircraft cannot always be decoupled; the equations
must be solved simultaneously. Producing the equations of motion when such
relationships exist involves writing equations for the translational and
angular momentum of the system and taking their derivatives with respect to
time (since acceleration is the time rate of change of momentum). For
a thorough explanation with a focus on aircraft dynamics see
:cite:`hughes2004SpacecraftAttitudeDynamics`; although the notation can be
opaque, it provides an excellent development for conservation of momentum of
multi-body systems, which is especially useful for understanding the
derivations of system models that include degrees of freedom between the
paraglider harness and the rest of the system.


.. 1d. Flight simulation

Once the equations of motion are known, they can be used to generate simulated
trajectories of the aircraft in response to different environmental and pilot
inputs. Key concepts include the choice of state variables, coordinate systems
and their relative advantages, encoding geometric orientation, representing the
environment, and applying numerical integration to the equations of motion to
produce the simulated result. For this work I found a complete reference in
:cite:`stevens2015AircraftControlSimulation`; the opening chapters provide
a masterful introduction to these key concepts, including a principled
mathematical notation (adopted by this paper, see :doc:`notation`) and
a thorough review of vector calculus (especially the counter-intuitive results
of taking the derivative of a vector with respect to an accelerating reference
frame, which is important when defining the :doc:`state_dynamics`).


Paraglider modeling
-------------------

.. 2. Paraglider specifics

In addition to the general knowledge of aircraft behavior, it is necessary to
understand the unique characteristics of paraglider flight. For practical
knowledge, recreational pilot materials make excellent resources. One thorough
introduction targeting beginner pilots :cite:`pagen2001ArtParagliding` provides
a tour of the components of a paraglider, their function, behavior, and an
admirable review of their aerodynamics; if any of the paraglider-specific
terminology in this paper is unclear, this book will likely clear up the
confusion.

Beyond recreational sources, academic literature relevant to paraglider
modeling is typically from one of two branches: parafoil-payload systems, and
paragliders. Parafoil-payload systems usually (but not always) refer to
large-scale ram-air gliding parachutes intended for heavy payload applications
such as cargo delivery and vehicle-recovery (such as landing the X-38
experimental space plane :cite:`madsen2003FlightPerformanceAerodynamics`, or
the more recent work by SpaceX to catch rocket fairings on a boat), while the
term "paraglider" usually (but not always) refers to the recreational aircraft.
Although the physical characteristics of parafoil-payload systems differ
significantly from paragliders due to their scale, carrying capacity, and
control schemes, their similarities make much of the research informative,
albeit not directly applicable. As a result this section will mix the two
groups, noting their differences when significant. Also, as this project has
chosen to neglect the effects of canopy deformations, research into modeling
those deformations will not be discussed.


.. 2b. Modeling: topical works

The first topic of research is on the aerodynamics of arched, inflatable wings.
Their nonlinear geometry made analyses difficult, so early studies were limited
to their longitudinal dynamics (fore-aft two-dimensional motion).
Alternatively, simple models of their 3D dynamics divide the wing into several
discrete segments that act independently (thus neglecting the 3D flow
interactions of a real 3D model) :cite:`slegers2003AspectsControlParafoil`.
Attempts to account for the full 3D aerodynamics typically involved either
measuring the longitudinal and lateral aerodynamic coefficients experimentally
:cite:`nicolaides1971ParafoilWindTunnel`, or estimating them using vortex
lattice and panel methods that can account for their nonlinear geometry by
neglecting viscous effects. The significance of the viscous effects led to
attempts to incorporate experimental aerodynamic coefficients via extended
lifting-line models; two important works regarding this approach were
:cite:`gonzalez1993PrandtlTheoryApplied` and
:cite:`iosilevskii1996LiftinglineTheoryArched`, which could estimate the 3D
aerodynamics of wings with circular arcs, but were unable to account for sweep.
As nonlinear lifting-line theory (NLLT) models continue to be developed, their
applicability to paraglider wings has greatly improved
:cite:`belloc2015WindTunnelInvestigation`; for example,
:cite:`kulhanek2019IdentificationDegradationAerodynamic` successfully applied
the method from :cite:`phillips2000ModernAdaptationPrandtl` to a reference
paraglider wing in a static flight test, confirming the merit of the of
a modern NLLT to this application.

Another significant characteristic of paraglider canopies is their low density,
which makes them sensitive to the effects of *apparent mass*
:cite:`lamb1945Hydrodynamics`. Early attempts to model the apparent mass of
a paraglider simplified the wing as an ellipsoid with a single center of
rotation :cite:`lissaman1993ApparentMassEffects`. Further developments
recognized the inadequacies the ellipsoid model, and adjusted the estimates to
account for two separate centers of rotation for rolling and pitching motions
:cite:`barrows2002ApparentMassParafoils`. Both models are limited by their
assumption of steady flow :cite:`thomasson2000EquationsMotionVehicle` so their
adequacy for simulations involving dynamic maneuvers is unclear; nevertheless,
the adapted model is assumed to be adequate for the purposes of this paper.

The last major topic of research is the system model. There are many system
models in literature, but their key differentiating factors in the context of
this project are whether they incorporate apparent mass and how they model the
attachment of the harness to the suspension lines. The inclusion of apparent
mass appears to be a modeling decision driven by whether the author expected
the effect to be significant; papers that exclude apparent mass do so without
explicit justification. For the harness connection, models are categorized by
their *degrees of freedom* (DoF) and the character of the connection points;
a 6-DoF model does not allow the payload to move at all, a 7-DoF allows the
payload to translate or rotate (relative to the suspension lines) in one
dimension, an 8-DoF adds two degrees of freedom, etc. For a general
understanding of the impact, :cite:`toglia2010ModelingMotionAnalysis` provides
a comparative analysis of a fixed (6-DoF) model versus a 9-DoF system model.
For a more thorough review of the many available system models,
:cite:`yakimenko2005DevelopmentScalable8DoF` has a seemingly exhaustive list of
the models through 2005, including a discussion of those models that account
for apparent mass. Two informative models that incorporate apparent mass are
:cite:`slegers2003AspectsControlParafoil` (which used the older method in
:cite:`lissaman1993ApparentMassEffects`) and
:cite:`cumer2012SimulationGenericDynamics` (which used the adapted apparent
mass model from :cite:`barrows2002ApparentMassParafoils`).


.. 2c. Modeling: comprehensive works

   Transition from specific topics to complete overviews. Finish with Benedetti
   to present my paper as an extension of his.

In addition to topical works, there have been several more comprehensive
studies. The best place to start is :cite:`lingard1995RamairParachuteDesign`:
although it has a parafoil-payload perspective, this approachable paper is
a thorough introduction to the terminology, geometric parameters, choice of
airfoil, and control schemes of parafoils (which it calls a "ram-air
parachute"); this paper also used geometric simplifications to study the canopy
aerodynamics and drag contributions, and developed linear models of the
longitudinal and lateral dynamics to study performance and stability. Next, for
a paraglider perspective, :cite:`babinsky1999AerodynamicPerformanceParagliders`
provides a compact survey on the sources of aerodynamic drag; it reviews the
impacts of arc, flexibility, air intakes, lines, and pilot. Worth reading
immediately after is :cite:`kulhanek2019IdentificationDegradationAerodynamic`,
as it is essentially an updated revision of
:cite:`babinsky1999AerodynamicPerformanceParagliders`.

The most comprehensive work on paraglider flight dynamics to date is the
dissertation :cite:`benedetti2012ParaglidersFlightDynamics` that inspired the
general structure of this paper. First, it provides an overview of paraglider
geometry, construction, and behavior. It then develops a foil geometry that
uses the locus of quarter-chord points to position the sections, as well as
intuitive parametric definitions of the underlying paraglider canopy structure.
For the paraglider components, it develops a model to position the harness as
a function of the accelerator control, a continuous brake deflection
distribution using both brakes, and the spherical harness model used by this
paper. Next, for the canopy aerodynamics it develops a pseudo-LLT (which it
acknowledges is an approximation in deference to the project's primary focus on
stability and control) using constant 2D aerodynamic coefficients. From the
complete aerodynamics model, it then estimates the 3D aerodynamic coefficients
and stability derivatives for a linearized model that is used for the remainder
of the work, which is focused on performance aspects (such as glide ratio
versus equilibrium pitch angle), stability analyses (such as longitudinal
stability versus riser position, and roll stability versus sideslip), and
controllability (takeoff, maneuvering, and landing).


This work
---------

.. List the improvements made by this paper

As mentioned in the previous paragraph, this project began with
:cite:`benedetti2012ParaglidersFlightDynamics` as its starting point. While
attempting to use those models to recreate commercial paraglider wings, this
work identified a collection of improvements that led to newly derived
models.

First, it improves the canopy geometry by developing a novel foil geometry
model inspired by a suggestion in :cite:`casellasParagliderDesignHandbook` that
allows independent reference points for the :math:`x`- and
:math:`yz`-positions. This increased flexibility allows accurate
representations of existing wings using simple parametric equations, which this
work uses to replace the parametric design curves in
:cite:`benedetti2012ParaglidersFlightDynamics` with new parametrizations that
are easier to estimate for an existing paraglider canopy. It also replaces the
approximate inertia calculations for the canopy surface and volume with
a mesh-based method that can account for different upper and lower surface
densities, and the extra solid mass from vertical ribs.


.. Also mention the different choice of section index? That has a big impact
   too, but I guess you could argue it's part of the new foil geometry.


For the canopy aerodynamics, it replaces his pseudo-LLT with a full NLLT
(:cite:`phillips2000ModernAdaptationPrandtl`,
:cite:`hunsaker2006LiftinglineApproachEstimating`) that supports arbitrary arc,
sweep, twist, specific (nonlinear model) aerodynamic coefficients for each
section as a function of Reynolds number and deflection distance, and
non-uniform wind vectors along the span. Also, instead of modeling trailing
edge deflections as section rotations (by adding the deflection angle to the
section angle of attack, effectively shifting the coefficient curves), this
model uses section coefficients generated from the actual deflected geometry,
and accounts for the effects of Reynolds number.

Next, it completely redesigns the suspension line model, keeping only the
intuition to replace the "rigging angle" with a displacement vector in the body
axes. The new model improves the representation of the brakes by first
calculating the deflection distance before calculating the true change in angle
of attack (which depends on the section chord), as well as improving the
accuracy of the deflection distribution itself. The new model improves the
representation of the accelerator by parametrizing the fore and aft connection
points instead of fixing them at the leading and trailing edge of the canopy,
thus allowing accurate models of commercial wings. Lastly, the new model moves
the line drag away from canopy centroid and distributes it into lumped points
that can model asymmetric forces between each semispan.

For the harness, the only minor change was to separate the weight shift
distance from an absolute distance to a proportional one controlled by
a harness parameter for the maximum displacement. Although functionality
equivalent, I personally felt that this change makes simulation scenarios
easier to write and understand.

For the system model, this paper derived 6-DoF and 9-DoF models (the 9-DoF is
a rederivation of the model used in
:cite:`slegers2010EffectsCanopypayloadRelative` and
:cite:`gorman2012EvaluationMultibodyParafoil`) that may optionally incorporate
the apparent mass estimates from :cite:`barrows2002ApparentMassParafoils`. The
9-DoF model is included for demonstration and testing purposes, and is not used
in any analyses.

The implementation of all models are available as an `open source library
<https://github.com/pfheatwole/glidersim>`__
:cite:`heatwolev2022.03.0aGlidersim`, including example wing models, and the
simulations used in this paper are available as part of the `open source
materials <https://github.com/pfheatwole/thesis>`__ used to produce this paper.


.. Bonus: discuss ongoing work related to the NLLT

   * MachUpX: https://machupx.readthedocs.io/en/latest/introduction.html

   * reid2020GeneralApproachLiftingLine

   * goates2021PracticalImplementationGeneral
