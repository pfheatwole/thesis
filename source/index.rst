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
      \listoftables
      \mainmatter

.. toctree::
   :maxdepth: 3
   :numbered:

   introduction
   bayesian_filtering
   paraglider_canopies
   paraglider_dynamics
   data_considerations
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
