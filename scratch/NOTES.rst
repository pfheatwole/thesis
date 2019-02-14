Trouble Words
=============

* "paraglider wing" vs "paragliding wing"

* accelerator, speedbar/speed-bar/speed bar

* debias, de-bias (when to hyphenate)

* timestep, time-step, time step

* vario, variometer (allowable abbreviations)


Useful Reminders
================

* ReST allows comments (could be useful for structural peculiarities in my
  HTML versus LaTeX sources)

* Signposting is a useful way for the writer to layout their work. It's a way
  of telling yourself what you're going to work on next. Also, you can look
  back and see how your expected path has diverged.

* Just signposting *what* you're going to do isn't as helpful as first
  communicating *why* the *what* is necessary.

  Consider "I will discuss particle filtering." versus "Recreating the flight
  requires filling in missing pieces; this type of artificial data generation
  is known as simulation-based filtering. One such method is the particle
  filter."

* Each builder (Latex, HTML, etc) support and prefer different types of image
  formats. For example, Latex can't embed SVG directly, so those must be
  embedded in a pdf, whereas HTML can use SVG directly.
  
  As noted in the `Sphinx documentation
  <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#images>`_,
  "Sphinx extends the standard docutils behavior by allowing an asterisk for
  the extension."

  For example, suppose the `images` folder has ``wind_triangle.svg`` and
  ``wind_triangle.pdf``. You can add that image to a document with:

  .. code-block:: rst

     .. figure:: images/wind_triangle.*
         :alt: Wind Triangle
         :align: center

         Wind Triangle

   Each builder will select whichever format it "prefers".
