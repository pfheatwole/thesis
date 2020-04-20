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

      abstract
      acknowledgements

.. only:: latex

   .. The latex build must add these explicitly outside the toctree since the
      latex builder doesn't respect unnumbered sections

   .. include:: abstract.rst
   .. include:: acknowledgements.rst

   .. raw:: latex

      \tableofcontents*
      \listoffigures
      \mainmatter
      \pagestyle{asu}

.. toctree::
   :maxdepth: 3
   :numbered:

   introduction
   paraglider_model
   flight_simulation
   wind_prediction
   examples

.. toctree::
   :maxdepth: 3

   glossary
   zreferences

.. All documents beyond this point are considered appendices

.. raw:: latex

   \appendix

.. toctree::
   :maxdepth: 3

   symbols
   appendix
