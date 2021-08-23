* When I plot my final wing, the arc doesn't seem to match the actual wing.
  Might want to comment on that.

* Where do I discuss the viscous drag corrections due to air intakes?

* Do I need to discuss the missing pieces like ``ParagliderWing``? My
  description of the component models is incomplete by necessity; the
  implementations have a LOT of detail.



Modeling workflow (2021-08-21)
==============================

I've already got the components organized in the chapters. I could mirror that
structure in this chapter, but it might be more helpful to take this
opportunity to present the material in a different way. In particular, I'm
leaning towards linear steps, like:

  To define the canopy using the component models, you need to define the
  idealized foil geometry, then specify several physical attributes that are
  use for inertia calculations and viscous drag corrections. For the foil
  geometry, define the chord distribution, fore-aft positioning, yz-curvature,
  and geometric twist. For the physical attributes, specify the surface and
  rib material densities, number of cells (to determine the number and
  placement of the internal ribs), spanwise extent of the air intakes, and the
  positions on the section profiles that delineate the air intake openings.
