***************
Example Content
***************

This section is a scratchpad that reminds me how to do things in Sphinx.

References
==========

Top-level documents are referenced using ``:doc:``. For example,
:doc:`introduction`. 

.. warning:: These are case sensitive.

Labels can either be explicit, like :ref:`common_notation` (which is using
a explicit, and thus global, reST label), or they can be auto-generated using
``sphinx.ext.autosectionlabel``. The catch is that for automatic labels, you
have to use the fully specified path from the index to the reST file. For
example, :ref:`content/introduction:Introduction`

Lastly, references can be numbered, using ``:numref:``, or labeled, using
``:ref:``. Beware, numbering starts with the top-level numbers, so if
a chapter or section is unnumbered it will look odd when reference outside
that context. For example, in HTML appendices aren't given alphabetical
sequences, so for the table in the appendix "Notation and Symbols" you'll get
something like :numref:`common_notation`.


Citations
=========


BibTex
------

Simple enough: :cite:`bencatel2013AtmosphericFlowField`


Internal References
-------------------

FIXME

Sections I think can use the name of the section directly? Like `Example
Content`_ or somesuch?


External URLs
-------------

These aren't too bad: `link text <http://www.google.com>`_.


Figures
=======

You can supply different formats for different builders and let them choose
the appropriate version (eg, SVG for HTML and PDF for latex). Or, instead of
converting SVG into PDF manually, use the Sphinx extension
``sphinx.ext.imgconverter``, which automatically converts SVG into PDF for the
latex builder.

.. _wind_triangle:
.. figure:: images/wind_triangle.*

   A Wind Triangle

Should see a :numref:`wind triangle in (Fig. %s) <wind_triangle>`.

Note that figure references are different from equations in that they use
standard reST labels ``.. _label_here`` instead of ``:label:`` options.


Math
====

Use the notation from :ref:`common_notation`.


Inline Equations
----------------

You use the ``:math:`` role for inline equations. For example, :math:`y
= \int_{a}^{b} f \left( x \right) dx`?


Numbered Equations
------------------

Sphinx allows numbered and unnumbered equations.

For example, the equation for marginal probability:

.. math::

   p(A) = \int_{B} p(A, B) p(B) dB

That equation is unlabeled (perhaps since it's not worth referencing
directly). But after applying the chain rule you get the more amenable:

.. math::
   :label: With_LR

   p\left( A \right) = \int_{B} p\left( A | B \right) p \left( B \right) dB


The ``:label:`` serves two purposes:

1. It allows you to reference it, like :eq:`With_LR`.

2. It instructs Sphinx to number the equation, if ``numfig = True`` in
   ``conf.py``.


Abbreviations
=============

You can use the ``:abbr:`` role for abbreviations and acronyms. For example,
:abbr:`FIFO (first-in, first-out)` will generate a acronym with the contents
of the parenthesis as a tool-tip (in HTML, in PDF it will output exactly).

Unfortunately, I'm not sure how useful this is to me. In the text I will
typically want to introduce the full definition first, like "first-in,
first-out (FIFO)". Tooltips would be mildly nice to have later on, but with
this format it'd repeat the full definition every time in the PDF (which
I don't want). Also, Sphinx doesn't offer "List of Acronyms" functionality.

However, I do like the idea of adding explicit "this is an acronym definition"
markup to make it easier to search for those terms. Maybe a dummy role?

.. todo::

   Could I define my own role for marking abbreviations? And how hard would it
   be to generate a list of those acronyms?


Glossaries
==========

You can add term definitions in a glossary using the ``:term:`` directive. For
example, :term:`term` or :term:`another term`.
