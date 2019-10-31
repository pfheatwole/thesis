***************
Example Content
***************

This section is a scratchpad that reminds me how to do things in Sphinx.

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


Math
====


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
