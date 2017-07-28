.. Thesis documentation master file, created by
   sphinx-quickstart on Mon Jul 24 16:10:21 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. For CalPoly, they expect:
    • Title Page required (page i but not numbered)
    • Copyright Page required (page ii)
    • Committee Page required (page iii)
    • Abstract required (page iv)
    • Acknowledgments Page optional (cont. Roman numeral pagination)
    • Table of Contents required (cont. Roman numeral pagination)
    • List of Tables if applicable (cont. Roman numeral pagination)
    • List of Figures if applicable (cont. Roman numeral pagination)

This is a nonprinting section
=============================

.. Workaround for a (bug?) issue where the first section does not produce
   a chapter. Means the first chapter would have no chapter entry.
   FIXME: seems like I'm probably missing something, this should not be needed.

.. raw:: latex

    \frontmatter
    \thetitlepage
    \copyrightpage
    \committeepage

.. include:: abstract.rst

.. raw:: latex

    \tableofcontents*
    \listoffigures

.. raw:: latex

    \mainmatter
    \pagestyle{asu}

.. toctree::
   :maxdepth: 2

   intro
   citations_example
   appendix
   zbibliography
