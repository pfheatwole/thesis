********
Contents
********

.. raw:: latex

    \frontmatter
    \thetitlepage
    \copyrightpage
    \committeepage

.. only:: html or singlehtml

   .. toctree::

      content/abstract
      content/acknowledgements

.. only:: latex

   .. The latex build must add these explicitly outside the toctree since the
      latex builder doesn't respect unnumbered sections

   .. include:: content/abstract.rst
   .. include:: content/acknowledgements.rst

   .. raw:: latex

      \tableofcontents*
      \listoffigures
      \mainmatter
      \pagestyle{asu}

.. toctree::
   :maxdepth: 3
   :numbered:

   content/introduction
   content/paraglider_model
   content/flight_simulation
   content/flight_reconstruction
   content/wind_regression
   content/wind_patterns
   content/wind_prediction
   content/examples

.. toctree::
   :maxdepth: 3

   content/glossary
   content/zreferences

.. All documents beyond this point are considered appendices

.. raw:: latex

   \appendix

.. toctree::
   :maxdepth: 3

   content/symbols
   content/appendix
