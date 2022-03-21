.. only:: html or singlehtml

   ********
   Abstract
   ********

.. raw:: latex

   \csuabstract


.. Remember: "Tell a complete story in the abstract."

Dynamic simulations are invaluable for studying system behavior, developing
control models, and running statistical analyses. For example, paraglider
flight simulations could be used to analyze how a wing behaves when it
encounters wind shear, or to reconstruct the wind field that was present during
a flight. Unfortunately, creating dynamics models for commercial paraglider
wings is difficult: not only are detailed specifications unavailable, but even
if they were, a detailed model would be laborious to create. To address that
difficulty, this project develops a paraglider flight dynamics model that uses
parametric components to model commercial paraglider wings given only limited
technical specifications and knowledge of typical wing design. To validate the
model design and implementation, an aerodynamic simulation of a reference
paraglider canopy is compared to wind tunnel measurements, and a dynamic
simulation of a commercial paraglider system is compared to basic flight test
data. The entirety of the models and example wings are available as an `open
source library <https://github.com/pfheatwole/glidersim>`__ built on the Python
scientific computing stack.
