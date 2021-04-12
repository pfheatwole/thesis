The task: estimate the aerodynamics from the shape.

The criteria: [[performance requirements]]

The options: [[LLT, NLLT, panel methods, CFD]]

The choice: [[NLLT]]

The implementation: [[none available, so I wrote one]]

The result: [[wind tunnel tests from Belloc]]


Outline
=======

* What are *aerodynamics*?

* Why does this project need the canopy aerodynamics?

* How do you estimate the aerodynamics of a wing from its shape?

* What are the performance criteria for an aerodynamics method suitable for
  paraglider flight reconstruction?

* [[Selecting an aerodynamics method]]

* [[Phillips' NLLT: concept, advantages and disadvantages, standard
  derivation, my improvements, implementation, etc]]

* Validation/demonstration (using Belloc's wind tunnel data)

* Discussion


BRAINDUMP
=========

* I need to estimate the aerodynamics **under normal flying conditons**. It
  must handle turning (longitudinal-only models are out), relatively high
  angles of attack (small angle models are out, which includes most linearized
  models), etc.

* To study the performance of a wing you can measure its aerodynamics
  *experimentally* or you can predict its performance *theoretically*.

* Theoretical methods that solve for the flow field can be categorized as
  *analytical* or *computational* methods. Both start by establishing a system
  of governing equations and solving for the target variables. *Analytical*
  methods allow for exact calculation of answers, whereas *computational*
  aerodynamics seek **numerical** solutions to the governing equations.
  Relying on computers to do the heavy lifting enable more complex models that
  would be infeasible to solve analytically.

* This chapter needs to choose an aerodynamics method.

  Models that allow analytical solutions, such as Prandtl's LLT, are
  convenient, but they rely on strong assumptions that do not hold for the
  complex wing geometries of paragliders.

  The non-linear shape of paraglider canopies together with the particular
  flight behaviors of paragliding flight make it unusually demanding. This
  chapter needs to select a suitable method, acquire an implementation of that
  method, and validate its performance.


* "To calculate the aerodynamic forces acting on an airplane, it is necessary
  to solve the equations governing the flow field about the vehicle."
  (Aerodynamics for Engineers, Sec:2.1, pg 44)

  The equations typically start with conserved quantities (mass, momentum, and
  energy) and adding boundary conditions (flow tangency along surfaces, Kutta
  condition). The result is a set of *boundary equations* that describe the
  flow along the outside of the boundary layer, and a set of *boundary
  conditions* that fix the precise value of the equations (**Note the two
  different uses of "boundary"**: there is the "boundary layer", which is the
  boundary around the surface, and the "boundary conditions" for solving the
  *boundary value problem*)


* From "Aerodynamics for Engineers", pg44:

     The fundamental physics laws used to solve for the fluid motion in
     a general problem are:

     1. Conservation of mass (or the continuity equation)

     2. Conservation of linear momentum (or Newton's 2nd law of motion)

     3. Conservation of energy (or the 1st law of thermodynamics)

* From "Aerodynamics for Engineers", Fig:7.15, pg377

  *stall pattern*: useful term when describing geometric twist for
  paragliders: the goal is to design the stall pattern to ensure that the wing
  tips stall first

* "The greatest compromise in using lifting-line theory into the stall
  angle-of-attack range and beyond is the use of data for the two-dimensional
  flow around an airfoil. The actual flow for this configuration is a complex,
  three-dimensional flow with separation."  (Aerodynamics for Engineers,
  pg:384, last paragraph)

* "Aerodynamics for Engineers", pg388, quoting Margason et al, 1985

  "The VLM predicts the experimental data very well, due to the fact that
  vortex lattice methods neglect both thickness and viscosity effects. **For
  most cases, the effect of viscosity offsets the effect of thickness,**
  fortuitously yielding good agreement between the VLM and experiment."

* "Aerodynamics for Engineers", pg390, discussing VLM:

  "In a rigorous theoretical analysis, the vortex lattice panels are located
  on the mean camber surface of the wing and, when the trailing vortices leave
  the wing, they follow a curved path. However, for many engineering
  applications, suitable accuracy can be obtained using linearized theory in
  which straight-line trailing vortices extend downstream to infinity."

  Similar issue with how I'm using Phillips? I'm assuming the trailing
  vortices are straight lines. I think I'm essentially using a linearized
  theory for the horseshoe vortices.

  He goes on to mention that the trailing vortices are typically aligned
  either parallel to the freestream or parallel to the body axes. I guess I'm
  using the former (freestream), which seems ambiguous if the wing is turning.

  This section also has a great discussion on placing the control points at
  the `0.75c` positions (the *Pistolesi boundary condition*). Has to do with
  the flow being parallel to the control point there?

* I can summarize a lot of the limitations of how I'm using Phillips method
  with the fact that it's a *steady* solution. A "rigorous" paraglider
  simulator would use an *unsteady* solver (accounting for the unsteady vortex
  shedding as the wing accelerates). See "Applications of the Unsteady
  Vortex-Lattice Method in Aircraft Aeroelasticity and Flight Dynamics" for
  some issues, such as: rotations, wing deformations, gusts, etc.

  Regarding rotations: see `model/notes/notes-2021w10.rst`

* "Aerodynamics for Engineers", pg393: excellent discussion that might be
  helpful for understanding Phillips derivation


* Seems like Katz and Plotkin introduced a numerical lifting-line method in
  "Lifting-line solution by horseshoe elements (Katz, Plotkin; 1991). Their
  method distributed horseshoe vortices along the quarter-chord line like
  Phillips did, but for its boundary condition it applied the *Neumann
  condition* at the three-quarter chord position. Phillips says that worked
  well for wings with planar (uncambered) wings with no flap deflections, but
  since they used a single chordwise panel they're effectively assuming the
  section can be approximated by flat plates (no camber).

  [[FIXME: need more discussion on the evolution from "Katz and Plotkin" to
  Phillips. Replacing the Neumann condition with the 3D vortex law?]]

  In "Aerodynamics for Engineers", pg396 they explain that typical VLMs solve
  for the circulations by using "the boundary condition that the surface is
  a streamline. That is, the resultant flow is tangent to the wing at each and
  every control point." Is it correct to say that everything up to this point
  was the same as Phillips, but Phillips using a different boundary condition?
  Namely, **instead of flow tangency, Phillips uses the viscous aerodynamic
  coefficients?** I'm trying to wrap my head around the idea that with
  a viscous boundary layer the flow might not be tangent to the surface;
  I mean, it can't flow through the wing, so it would have to be tangent,
  wouldn't it? Or can you have a component of the flow that's moving normal to
  the surface? Hrm, never thought of that. Then again, when you get VERY close
  to the wing then the normal flow goes to zero, which means the ONLY motion
  is normal to the surface. That makes a lot of sense, actually.


* Airfoil coefficients are non-dimensional *force coefficients*.

  "Aerodynamics for Engineers", Sec:3.14 calls them *flow-field parameters*?

* Airfoil thickness

  * "The boundary layer effectively thickens the airfoil, especially near the
    trailing edge. [...] This thickening effectively alleviates the adverse
    pressure gradients, which in turn permits somewhat thicker sections before
    separation occurs. To ensure that boundary layer transition occurs and
    delays or avoids separation altogether, you might use vortex generators or
    other forms of surface roughness." (Aerodynamics for Engineers, pg199)


* "Flight Vehicle Aerodynamics":

  * pg23: there are two basic vector field representations:

    1. Grid (defined at the nodes of a grid which fills the entire
       flow-field). Used by CFD methods to solve the *full-potential*,
       *Euler*, or Navier-Stokes equations

    2. Singularity (velocity fields of source and vortex sheet strengths;
       "defined in limited regions of the flow-field, typically at solid
       surfaces or other boundaries". **The basis of the vortex lattice and
       panel flow calculation methods**.

  * pg26: "Lumping [into sheets, lines, or points] is the basis of aerodynamic
    modeling."


  * pg126: *quasi-steady* flows for "an aircraft in **slow** maneuver"

    My dynamics models compute acceleration, but the aerodynamics (mostly)
    ignore acceleration. The apparent mass tries to account for some of it,
    but that only captures the **resulting** acceleration of the wing, not the
    calculation of the aerodynamics that produce the forces and moments.

    Also, from `avl_doc.txt`, "Vortex-Lattice Modeling Principles
    / Configurations":

      A vortex-lattice model like AVL is best suited for aerodynamic
      configurations which consist mainly of thin lifting surfaces at small
      angles of attack and sideslip.  These surfaces and their trailing wakes
      are represented as single-layer vortex sheets, discretized into
      horseshoe vortex filaments, whose trailing legs are assumed to be
      parallel to the x-axis. 

    Also, from `avl_doc.txt`, "Vortex-Lattice Modeling Principles / Unsteady
    Flow":

      AVL assumes quasi-steady flow, meaning that unsteady vorticity shedding
      is neglected.  More precisely, it assumes the limit of small reduced
      frequency, which means that any oscillatory motion (e.g. in pitch) must
      be slow enough so that the period of oscillation is much longer than the
      time it takes the flow to traverse an airfoil chord.  This is true for
      virtually any expected flight maneuver.  Also, the roll, pitch, and yaw
      rates used in the computations must be slow enough so that the resulting
      relative flow angles are small.  This can be judged by the dimensionless
      rotation rate parameters, which should fall within the following
      practical limits.

      -0.10 < pb/2V < 0.10
      -0.03 < qc/2V < 0.03
      -0.25 < rb/2V < 0.25

      These limits represent extremely violent aircraft motion, and are
      unlikely to exceeded in any typical flight situation, except possibly
      during low-airspeed aerobatic maneuvers.  In any case, if any of these
      parameters falls outside of these limits, the results should be
      interpreted with caution.

  * pg131: "Note also that each [horseshoe vortex] adds zero net circulation
    in the Trefftz plane, where its two trailing legs have equal and opposite
    circulations."

    Hrm. Consider how I'm using Phillips method during turns. Where are the
    trailing vortices oriented? Each segment share a leg, so the two trailing
    vortices of any segment cannot be aligned (during a turn). Doesn't that
    imply the horseshoe vortices of my model are producing forces in the
    trailing wake? (Since they don't cancel.)

    Earlier in the discussion on *lifting surface theory* (pg127) Drela wrote:
    "On the trailing wake portions of the sheets, the strengths are constant
    in x, and equal to their trailing-edge values." I think I'm already
    violating the conditions of the VLM since my horseshoe vortices are not
    aligned with `x` (although you can consider them a sheet, I guess).


* Review `Phillips._induced_velocities`. I'm computing the "induced velocity"
  vectors `v_ji` (the velocity that segment `j` induces on segment `i`) using
  a single, constant `u_inf` for all segments. It sure seems like this is
  saying that all segments have trailing vortices that align with `u_inf`.

  Hm. This comes from Eq:3 in Phillips. Can you replace the `u_inf` with
  `u_inf_1` and `u_inf_2` for the two vortices? The `V` is the velocity at
  some arbitrary point which was induced by the two vortices. Why do those two
  vortices have to be aligned? Does the math work if they point in different
  directions? (IIRC, that ends up producing forces in the trailing wake, which
  IIRC is bad for some reason; I forget why.)


* I think XFLR5 tries to add viscous drag by first computing the local section
  `Cl` using the VLM, then using `Cd(Cl)` to lookup the drag associated with
  particular lift coefficients.

  According to
  http://adl.stanford.edu/sandbox/groups/aa241x/wiki/e054d/attachments/12409/Aircraft%20Flight%20Dynamics%20%26%20VLM%20Codes.pdf?sessionID=62f441d3fcc6b4014c66ce9aa5d732f561008d30,
  page 27, I think this is called *strip theory*. For a discussion of strip
  theory, see :cite:`flandro2011BasicAerodynamicsIncompressible`, Sec:6.6,
  except in that case they use `Cd(alpha_eff)`, but it's the same idea: using
  a 3D method to determine the effective angle of attack, then looking up the
  pressure distribution or viscous drag terms using the airfoil polars.




* Permeability: :cite:`desabrais2015AerodynamicInvestigationsRamAir` mentions
  how L/D decreases with canopy use (since permeability increases)


What are some of the considerations regarding the canopy?

* Non-linear geometry

  The wings aren't straight; significant taper.

* Relatively high angles of attack are common

  Simulations must accept that paragliders commonly approach the stall angle
  of attack, so small angle assumptions become problematic.

* Relatively low Reynolds numbers

  Low airspeed means the paraglider is operating at relatively low Reynolds
  numbers. This is exacerbated by significant wing taper; going from the wing
  root to the wing tip often sees the Reynolds number vary from `1.5e6` down
  to `2e3`. The result is that the inviscid assumption used by many
  aerodynamic methods stops working well; viscous effects become significant.

  **Paragliders span the transitional band between laminar and turbulent
  Reynolds number regimes.** See "Aerodynamics for Engineers", Tbl:2.2 (pg72)


* Non-rigid surfaces (cell billowing, wrinkling, etc)


What are some considerations regarding the choice of aerodynamics method?

* Longitudinal models are not good enough; the method should support sideslip
  (from side gusts) and asymmetric wind (turns, thermal interactions, etc)

* Should not assume linear aerodynamics

  [[Anticipated sources of non-linearity include non-linear geometry,
  relatively large operating range for the angle of attack, asymmetric wind
  vectors, more?]]

  [Linearized dynamics models are most useful because they make stability and
  control problems tractable.]]

* Should provide graceful degradation near stall

  [[There are non-linear aerodynamics that do not predict stall at all
  (basically all inviscid methods, I think); I'd like a method that explicitly
  fails around the stall point. Not sure "graceful degradation" is good
  phrasing though.]]

* Should be computationally efficient

  (Support rapid design iterations; let a designer "play" with the design.)


Modeling concerns
=================

The classic method for estimating the aerodynamic performance of a wing is
Prandtl's *lifting-line theory* (LLT). This deceptively simple model allowed
analytical solutions to the lift distribution.

For wings with significant sweep and/or dihedral, the classic LLT breaks down.
These more complex geometries require adaptations to account for the
non-linear behaviors, resulting in *non-linear lifting line* (NLLT) theories.
These are often also known as "numerical" lifting-line theories, since they
require numerical solutions.

Related work:

* :cite:`gonzalez1993PrandtlTheoryApplied`

* One of my goals with this model is to provide a more detailed view of
  paraglider aerodynamics. Too many papers start by assuming a linear model,
  quadratic drag, etc. I think you should start with a more complete model,
  then use **that** to produce the simplified model. **Access to a complete,
  non-linear model enables you to quantify the error involved with simplified
  models.**

  In fact, I strongly suspect that a good solution to the computational
  performance problem is to replace the NLLT with polynomial CL and CD whose
  parameters (offset, slope, etc) are functions of sideslip. The problem there
  is you'd need to assume a uniform wind. You could account for asymmetric
  flow during turns by making the parameters functions of the angular rates,
  but you'd still need to assume the underlying wind field is uniform.

  Either way, the point is to start with a thorough model **before** applying
  simplifications, so you can check if the simplification is reasonable.


* Instead of solving the boundary layer conditions for the full 3D wing, it is
  common to treat the lifting surface as a collection of finite segments taken
  from theoretical infinite-length wings. The infinite length assumption
  eliminates 3D effects and allows the wing sections to be analyzed using 2D
  geometry. The 3D flow of the physical wing can then be approximated using
  the 2D aerodynamic coefficients.

Limitations of using "design by wing sections":

* This method represents the wing using straight, constant-profile wing
  segments. For a continuously curved wing, this approximation will never be
  correct, although the approximation improves as the number of segments
  increases.

* The "wing sections" modeling assumption: treats the wing as a composite of
  segments from infinitely long wings (ie, it assumes 2D coefficients are
  accurate representations of the 3D segments). This assumption implies steady
  state conditions, uniform boundary layers across the segments, no
  cross-flow, etc. The 2D coefficients also make an assumption about the
  center of pressure, so I'm guessing it'll affect the segment pitching
  moments.

* It is difficult to model cell distortions (due to billowing, etc) using
  predetermined 2D geometry. It is technically possibly to estimate the final
  cell shapes and measure the section profiles, but the "infinite wing"
  approximation is unlikely to remain valid. If the aerodynamic effects of
  cell distortions are of interest, they are best treated either
  approximately, using averaged coefficient effects, or using full
  computational fluid dynamics methods. This current work neglects the effects
  of cell distortions and assumes all wing segments match the idealized 2D
  airfoils.



Validation
----------

* Notice there are a variety of limitations to my chosen inviscid model: see
  https://www.xflr5.tech/docs/Part%20IV:%20Limitations.pdf. When I say "this
  is what inviscid methods produce", what I really mean is "this is the
  performance of the particular inviscid method I applied". In particular:

  * The lack of an *interactive boundary layer* means it doesn't account
    boundary layer thickness (viscous displacement effects should change the
    shape of the geometry). See pg6

  * The flat wake assumption (no wake rollup) tend to overestimate the vortex
    strengths (and thus lift). See pg29

