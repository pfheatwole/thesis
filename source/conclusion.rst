**********
Conclusion
**********

.. What are the results of this project?

[[Assume an impatient reader will jump here. This is your last chance to
convince them the paper is worth reading.]]

* A parametric geometry and a dynamics model in Python. Includes several state
  models and simulator.

* Derivations available in appendices.

* Modular system design (doesn't simplify the equations by merging the
  components; each component is independent, as much as reasonable possible)

* Code available on Github using open source libraries

  * Why Python?

    * Approachable syntax

    * Good cross-domain language

    * Free (unlike matlab)

    * Numerical libraries (numpy, scipy)

    * Large library ecosystem (s2sphere, sklearn, databases, PyMC3, pandas, etc)

    * Easy integration into tools w/ native support (Blender, FreeCAD, QGIS)

      * Generate a simulation directly inside Blender

      * Design a wing and estimate it's polar curve inside FreeCAD

* Developed entirely using freely available tools (XFLR5, AVL, etc) and open
  source libraries (numpy, scipy, matplotlib, etc)

* The entire work is under permissive licensing: code is MIT, text and figures
  are CC-BY


Misc
----

* This paper does not solve the flight reconstruction problem; it only uses
  the simulator to generate test flights for validation. At first this is only
  helpful for superficial checks (do flights "look" correct?), but will
  eventually be necessary for physical flight validation.
