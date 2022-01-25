Parametric Paraglider Modeling
==============================

This repository contains the source material for my Master's thesis:
`Parametric Paraglider Modeling <https://pfheatwole.github.io/thesis/>`__

The project develops a parametric paraglider flight dynamics model suitable for
simulating flight trajectories under typical flight conditions. Its motivating
purpose is to approximate the flight dynamics of commercial paraglider wings
using only basic technical data.

To enable its use in common engineering applications (such as control modeling
and statistical filtering) the dynamics are encoded as differential equations
(``ẋ = f(x, u)``). An implementation of the dynamical system (including
a rudimentary flight simulator) is available as a Python library under
a permissive open source license: https://github.com/pfheatwole/glidersim/


Backstory
---------

The motivating goal was to learn wind patterns from sets of recorded paraglider
flights. The primary difficulty is that flight records are position-only time
series data, so extracting wind information requires a causal relationship
between paraglider motion and the underlying wind field. That causal link is
provided by the paraglider dynamics. If the dynamics of the paraglider that
created a flight are known, it may be possible to use statistical filtering to
perform probabilistic flight reconstruction; specifically, the problem requires
generating probability distributions over the paraglider state, control inputs,
and wind vectors.

Unfortunately, flight records do not include a dynamics model of the glider
that generated the data (in fact, they frequently omit any description of the
glider at all), so the dynamics model itself is uncertain. Thus, performing
flight reconstruction over a large number of flight tracks requires more than
single dynamics model: it needs an entire distribution of models. Developing
models is time consuming and requires extensive construction details that are
not readily available, so the new goal was to create a tool that can generate
paraglider models from publicly available information. Specifically, I wanted
a dynamics model that is parametrized by the most readily available wing data:
user manuals, pictures, and physical measurements. This paper develops such a
parametric model.


Building
--------

This document was produced using `Sphinx <https://www.sphinx-doc.org/>`__.

To rebuild the document from its source:

.. code-block:: bash

   $ git clone https://github.com/pfheatwole/thesis.git
   $ cd thesis
   $ python -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements/build.txt
   $ make html

Many of the figures were produced by scripts using the Python library. To run
any Python scripts that depend on `pfh.glidersim
<https://github.com/pfheatwole/glidersim>`__ :

.. code-block:: bash

   $ git clone https://github.com/pfheatwole/thesis.git
   $ cd thesis
   $ python -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements/develop.txt
   $ python source/figures/paraglider/belloc/belloc.py  # for example
