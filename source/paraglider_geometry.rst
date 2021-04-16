*******************
Paraglider Geometry
*******************

.. The discussions in this chapter should focus on the details that are
   important to the dynamics models.


.. Describe the system associated with the "paraglider dynamics".

A paraglider is a system of two components: a wing (canopy + lines), and
a payload (harness + pilot).

* [[This chapter is a bit squished since I need to to define both the wing
  geometry and the payload. They're both pretty simple though so it should be
  fine? The wing geometry just adds lines to a canopy and specifies the
  surface materials; I'm not trying to model individual risers, describe
  parafoil cells, etc. The harness I'm just going to say "here's the basic
  idea, I'm going to model it as a sphere.]]


.. Roadmap

This chapter will proceed as follows:

* Discuss the physical components (canopy, lines harness)

  [[ie, what are the individual components, their structural materials,
  notable aspects (and maybe their control inputs?]]

* Discuss the composite system (connections and interactions)

  [[ie, how the components combine to produce a paraglider.]]

  [[Discuss degrees-of-freedom here?]]

* [[Discuss existing paraglider models from literature?]]

* Present an complete definition of an example system, suitable for flight
  simulation, and discuss its performance

  [[ie, present my Hook3ish example: define the individual components and
  select a composite model that combines them into a complete system, and
  present some static analyses (wing polars).]]
