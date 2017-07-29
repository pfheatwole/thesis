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

.. This is a nonprinting section for the PDF, but if you delete it then the
   first chapter won't include the chapter heading.

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

    introduction
    example
    citations_example
    appendix
    zreferences
