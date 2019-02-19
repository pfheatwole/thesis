Example ReST Content
====================

Comments
--------

ReST allows inline comments that do no render to the document.

.. This is a single comment line.

The previous source line does not render.

.. This is a comment block. Block comments are created by maintaining the
   correct indentation. (This indentation can be obnoxious with vim
   autoformatting.) Once you have the second line indentation established,
   though, it should be okay.


Equations
---------

.. math::
    :label: wind_triangle

    w^2 = v^2 + t^2 - 2\cdot v\cdot t\cdot cos(\theta_x)

A numbered equation reference using its ``label``: :eq:`wind_triangle`


Tables
------

.. table:: Boolean AND
    :name: tbl-and

    =====  =====  =======
    A      B      A and B
    =====  =====  =======
    False  False  False
    True   False  False
    False  True   False
    True   True   True
    =====  =====  =======

A numbered table reference using it's ``name``: :numref:`tbl-and`


Figures
-------

Each builder (Latex, HTML, etc) support and prefer different types of image
formats. For example, Latex can't embed SVG directly, so those must be
embedded in a pdf, whereas HTML can use SVG directly.

As noted in the `Sphinx documentation
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#images>`_,
"Sphinx extends the standard docutils behavior by allowing an asterisk for the
extension."

For example, suppose the ``images`` folder has ``wind_triangle.svg`` and
``wind_triangle.pdf``. You can add that image to a document with:

.. code-block:: rst

  .. figure:: images/wind_triangle.*
      :alt: Wind Triangle (Alternate Text)
      :align: center

      Wind Triangle (Caption)

Each builder will select whichever format it "prefers".


Citations
---------

A link to an entry in the References using a bibtex citation key:
:cite:`barfoot_batch_2014`.
