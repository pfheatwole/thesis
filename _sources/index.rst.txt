.. only:: html or singlehtml

   .. include:: abstract.rst


********
Contents
********

.. raw:: latex

   \frontmatter
   \csutitle
   \csucopyright
   \csucommittee

.. only:: html or singlehtml

   .. toctree::

      acknowledgements

.. only:: latex

   .. The latex build must add these explicitly outside the toctree since the
      latex builder doesn't respect unnumbered sections

   .. include:: abstract.rst
   .. include:: acknowledgements.rst

   .. raw:: latex

      \tableofcontents*
      \listoffigures
      \listoftables
      \mainmatter

.. toctree::
   :maxdepth: 3
   :numbered:

   introduction
   related_works
   foil_geometry
   foil_aerodynamics
   paraglider_components
   system_dynamics
   state_dynamics
   demonstration
   validation
   conclusion

.. toctree::
   :maxdepth: 3

   glossary
   zreferences

.. All documents beyond this point are considered appendices

.. raw:: latex

   \appendix

.. toctree::
   :maxdepth: 3

   notation
   derivations
