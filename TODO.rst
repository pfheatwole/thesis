* Should I decompose the paraglider system in the Introduction? It'd explain
  the existence and order of the chapters.

  1. I want flight dynamics models of paragliders

  2. Those are hard to make, so I need a model that's parametrized by basic data

  3. Here's the kind of data I'm talking about

  4. Here's a logical decomposition of the paraglider system that allows each
     component to be relatively self-contained

     (this outlines the components and previews the chapter structure)


  The "foil" is the most complicated component and my foil model is independent
  of any paraglider-specific detail, so the foil geometry and foil aerodynamics
  get their own chapters. Given a general foil model you can define a specific
  canopy model.


UNFINISHED SECTIONS
===================

1. Introduction

2. Foil Geometry

   * [2.1.5] Orientation

   * [2.4.1] Section index

   * [2.5] Examples

   * [2.6] Case study

   * [2.7] Discussion


3. Foil aerodynamics

   * [3.1] Explain how I selected Phillips

   * [3.3] Case study

6. Demonstration

7. Conclusion


Topical
=======


Introduction
------------

* There are existing paraglider dynamics models in literature. I need to
  establish the needs of my application and observe the limitations of those
  existing models in order to motivate my paper.


Foil geometry
-------------

* Verify my use of *dihedral* and *anhedral*. At the least I think my use of
  "mean anhedral" is suspect; probably not even a helpful term.

* How do I argue that my definition of `r_LE/RP` decouples the parameters? You
  can see in the math that `r_LE/RP` and `r_P/LE` both involve `c` and `C_c/s`,
  but it won't be obvious that it counteracts the changes to keep the
  parameters decoupled.

* Where do I define *design parameters* (span, taper, etc)? Should be pretty
  early on on `Canopy Geometry` when I'm motivating parametric models.

* Finish the derivation of my parametrized wing geometry in `derivations`. The
  goal is to derive the version that uses `R` (configurable reference points),
  but keep the parafoil-related material in `Canopy Geometry`.


Foil aerodynamics
-----------------

* What is `CMT1` etc in Belloc's wind tunnel data? Why did I use it? Is it in
  the body axes? Why do I compute `Cla` for NLLT but not for AVL?


Paraglider components
---------------------

Suspension lines
^^^^^^^^^^^^^^^^

* I'll need to explain why I rejected using a *rigging angle* (essentially
  a built-in offset to the pitching angle) in favor of positioning `RM`
  explicitly. The primary reference on the topic is probably from the X-38
  project. See `iacomini1999InvestigationLargeScale`. Also used in
  `cumer2012SimulationGenericDynamics`.

  I didn't like the rigging angle because that suggested you could set the
  pitch angle of the wing, but in reality you only have partial control. The
  pitch angle is a function of many things, such as air density, airspeed,
  brake deflections, etc.

  Also, I wanted to use canopy frd as the body axes. The rigging angle is
  a built-in pitching offset. For me, `gamma = alpha + theta`, but for Iacomini
  it's `gamma = alpha + theta' + theta_R`, so his `theta' = theta - theta_R`.

  Wait, so is the rigging angle measured from a reference line through the
  central quarter-chord? Oof, if the definition of the rigging angle depends
  on `c4` then that's another complaint against rigging angles Yuck.

  Anyway, **how might I calculate them for my wings?** Would be cool to compute
  the "effective rigging angle" from wings defined using my parametrization.

  One big takeaway from `iacomini`: good parafoil performance requires keeping
  the angle of attack in what they call the *alpha corridor*: too steep and it
  stalls, too shallow and the leading edge can collapse.


Paraglider systems
------------------

* Barrows use the principal axes for `M_a` and `I_a`. I'm using the body axes.
  I forget why I'm neglecting that issue.

* Review the terms in the apparent mass derivation. "Apparent inertia matrix"
  etc, get pretty ambiguous. Try to clean it into a translational part,
  a rotational part, and a complete matrix.

* In my dynamics derivations, I don't appear to be consistent with specifying
  the coordinate systems; the derivatives in particular.


Demonstration
-------------

Simulation scenarios
^^^^^^^^^^^^^^^^^^^^

* In `iacomini1999InvestigationLargeScale` they talk a lot about the problems
  they had with parafoil *surge*, particularly during deployment. For their
  purposes, they defined surge as "the transition of the parafoil from
  a falling object to a flying object". I should create some scenarios that
  simulate wing surge, such as if you entered a sinking bubble (eg, instantly
  add +0.5ms vertical wind down so the wing has to rapidly equilibrate).

* How should I discuss the sensations of angular accelerations? During a turn
  you have constant angular velocities, thus constant centrifugal forces. The
  angular **accelerations** are more akin to a falling sensation.

* Checkout the `lateral_gust` scenarios. With full accelerator the glider
  largely ignores the gust, but with symmetric brakes it really struggles.
  I was using a 10mph gust that ramps up over 1sec and lasts for 3sec for the
  accelerator, but the symmetric brake condition simply can't handle it: the
  aerodynamics fail to converge.

* Create a set of top-down figure-8s with 6a, 9a with M_R=0, and 9a with some
  yaw restoring force. Plot the xy coordinates on top of each other to show
  how the yaw force affects the track. Conceptually, you'd expect the actual
  track to be somewhere in between 6a (infinite yaw resistance) and 9a with
  M_R=0 (zero yaw resistance).

* Might be interesting to make a 2D side-view plot of the xz-coordinate lines
  connecting from `RM` to the wing and harness to compare `6a` versus `9a`. Do
  a symmetric brake pulse to show the "dolphin" effect, and compare the two
  models.


Conclusion
----------

Future work
^^^^^^^^^^^


Notation and symbols
--------------------

* Give examples of vectors (position, velocity, linear momentum, angular
  momentum, derivatives, etc)

* Add a description of a *direction cosine matrix* to `symbols`? Or maybe the
  `glossary`?


Belloc
------

* Record the software versions used to generate the SVG files

* Ask Belloc if I can publish the wind tunnel data in the public repo

* Add the pseudo-inviscid CL vs CD (builds confidence in the method and
  implementation)

* Eliminate the yucky resampling logic in `belloc.py:InterpolatedArc`
  Related: why do I use a `PchipInterpolator`?

* Document the coefficients I'm plotting in Belloc. I'm using `CZa` etc, which
  means I'm plotting coefficients with respect to the wind axes. I forget why
  I chose to do that, except (that appears) that's what XFLR5 computes? On the
  bright side, I'm already using the T1 (moments wrt the CG).

* The arc curvature isn't too extreme in `belloc`, but not zero. How much
  "excess" wing is there due to overlap/underlap on the lower/upper surfaces
  between the linear wing segments?

  Compare the chord area to the upper and lower areas. For the chord area, use
  the Phillips instance variables `dl * c_avg * curve_length`, where
  `curve_length` is the length of the upper or lower airfoil surface (which
  assume a chord length of 1)


Content Tasks
=============

* Record the momentum derivatives for Barrows in the derivation. It wasn't
  clear from the paper exactly how those worked.


Drafting
--------

#. **Define the concrete "key ideas" for the paper.** These will drive how
   I develop the entire paper, both in structure and content. (Possibly start
   with the non-technical development, then convert that into technical terms.
   It requires probabilistic methods, so satisfying the needs of that math
   should do a pretty good job establishing the core components of the paper.)

#. Develop a topic outline. (Topic ordering implicitly encodes dependencies.)

#. Write an informal overview of the goal, problems, resources, and solutions.
   This should be conversational: I can get through a description of my project
   when talking to the Mohlers, I should be able to put it down on paper. The
   key is to avoid getting hung up on the technical specifics. Those can be
   filled in later.

#. Write an "introduction to the introduction". **Don't make the reader wait
   a long time to understand my contribution.**

#. Draft a full abstract.

#. Draft a full introduction.

#. Review each section has adequately description assumptions. You need to
   establish the assumptions and constraints of your method to make sure you
   don't overpromise.

#. Annotate the informal draft with **text-only** descriptions of good
   supporting material (figure descriptions, equations, code references, etc.)
   Don't worry about actually producing those elements; this is about
   establishing a pathway to a cohesive structure: once you know what elements
   you really want, only then should you spend time creating them.


Feedback
^^^^^^^^

Summary of Bridget's comments from `2021w42`:

* The goal of the thesis is to:

  1. Put the project into plain terms

  2. Provide details for future work building a paragliding flight simulator

* Regarding putting the project into "plain terms":

  * Motivation for the project - describe paragliding and what paragliders
    (and you in particular) need / desire

  * Existing technology - describe what paragliding models / simulators
    currently exist and what is lacking from these

  * Your contribution - describe what your contribution is and distinguish
    how it is different / similar to existing models/devices. It would also
    be helpful to include a top level system block diagram showing the main
    input and outputs of the system (I am currently unclear as to what the
    output is - positional data (i.e. a track)?)

  * An overview of the sections of your thesis so the reader will understand
    the organization of your chapters. My understanding is that you spend
    two whole chapters describing the model for the geometry (chapter 2) and
    aerodynamics (chapter 3) of the foil and then spend a chapter on the
    models of the 3 main components of the paraglider system (canopy,
    suspension lines and harness). What is unclear to me here is how does
    the canopy of chapter 4 differ from what you described in chapters 2 and
    3 (or is it just a particular instance of a foil). Then chapter 5 is
    about modeling the system as a whole, and chapter 6 is a case study that
    tests the performance/accuracy of the system model. It might also be
    useful to include somewhere in the intro (perhaps near the start as you
    are describing the motivation) how that even though you are a computer
    engineering student, the thesis delves into math, statistics, flight
    dynamics, etc. - all of which you had to learn before you could use your
    computer engineering skills to program your implementation

* **At the start of each chapter, provide a paragraph about why this chapter
  is important and how it fits into the whole thesis document.**

* "I kept wanting the document to tell me how your design differed / was the
  same as existing designs. For example, I know air foils have been modeled
  before (as well as paragliding wings) - so for your design choices, how
  much of it was based on an existing design and how much of it did you
  modify/create (some of your square bracket remarks seemed to hint at this,
  but I would like to see it more explicitly stated)."

* Chapter 6 (Demonstration)

  "What exactly is the output of the model?"

  "Just describe what it currently does and the limitations it has."

* "Focus on communicating your contributions in a way that someone like me,
  Lynne, and Marty (who don't have the background in flight dynamics and
  stats) can understand what you did." (ie, "more intro paragraphs to each
  section and subsection")


References
----------

* Create a list of topics relevant for "prior art" papers (paraglider dynamics,
  wind field estimation, thermal estimation, etc)

* Create a list of sources for each topic, including summary notes


Figures
-------

* In `generate_canopy_examples.py`, there's a function `_plot_foil` that
  appears to duplicate `gsim.plots.plot_foil`. Why does it exist?

* Factor out the canopy plotting function from the thesis script
  `generate_canopy_examples.py` (the one with the faux grid). I'd like to use
  it to to plot my Hook3ish

* I need a diagram for the 6 DoF model. I was going to just show the body
  centroid "B", but that makes it less obvious that the 6 DoF supports weight
  shift. Should all models include "P"? While I'm at it, is "B" still a good
  choice?

* Add author and license to my SVG metadata (Inkscape -> Document Properties)

* Figure labels must be globally unique, so standardized label prefixes would
  probably help. Could be based on the content of the figure (the specific
  object, or that object's domain) or the section that contains the figure.

  At the least, it seems like a reasonable that **labels should match the
  figure filename.** This will probably preclude using section names, since
  I want to avoid renaming figure filenames if the sections change.

  While I'm at it, **the figure sources should match the figure labels** as
  well. It should be obvious where a figure came from (within reason)

* Remove scratch/unused figures (eg, `elliptical_arc_dihedral.svg`)


Editorial Tasks
===============


Writing Style
-------------

* Choose a voice

  * Passive vs active (I strongly lean towards active, but be consistent)

  * "We will", "I will", "this paper will", etc?

* Eliminate crutch words like "simply", "just", etc

* Review page number references; standardize on `p123` style


Notation, math, etc
-------------------

* Although Steven's notation uses `F` and `M` for forces and moments, I want to
  be consistent that vectors are lowercase-bold. Instead, I'm using Hughes'
  style of lower `f` and `g` for forces and moments, relying on subscripts for
  disambiguation; naked `\vec{g}` is a well-established convention for gravity,
  moments are `\vec{g}_b2R` ("body with respect to reference point `R`")

  The exception is in Phillips' method, where I use `dF` to maintain
  consistency with the paper.

* When do you need to specify a reference frame in my mathematical notation?
  (Only when taking vector derivatives, I think; see `notes-202048:Math`)

* I'm getting sick of `\mathrm` for all the points (like
  `r_{\mathrm{P}/\mathrm{LE}}`). Can I write a latex macro that will wrap them
  for me?


Terminology
-----------

* There is a lot of confusion/ambiguity regarding *anhedral*. You might refer
  to the angle between the y-axis and the position of the section, or you might
  be referring to the section roll. I'm leaning towards reserving "anhedral"
  for "angle between y-axis and section position", since you talk about "arc
  anhedral" which clearly refers to the POSITION arc, not the roll angle. So,
  I guess `\Gamma` is that position angle, `\gamma` is the roll angle.

* Should I define a Sphinx role for terms/definitions? There's already
  a `:term:` role that requires they be in a glossary, but what about in-line
  definitions with no entry in the glossary? (They compile with a warning and
  render as normal text; no good.)


Structural
----------

* Make sure all the chapters follow the same structure
  (see `meta/editing:Content:Chapter structure`)

* For unnumbered chapters like "Glossary" and "Symbols", I'm using the ``..
  only::`` directive to specify the chapter titles. I have to do that because
  if I use regular section headings, the latex builder will set them as
  numbered.

  This current way works, but you can't have sections in those chapters: if
  you try, they'll all be marked as chapters, as if the original chapter
  heading doesn't exist. It confuses both the HTML and latex builders. I think
  `.. only::`` is "not meant for structural elements", so that makes sense,
  but I'm not sure how to fix this. For now, just don't use sections in
  unnumbered chapters.

* You can add ``:numbered:`` to the ``toctree`` to get section numbers in
  HTML, and it will automatically use ``<sec#>.<eq#>`` for equation
  cross-references, but I get some errors about "already assigned section
  numbers" when building HTML.

* The HTML builder doesn't label the appendices as appendices (it doesn't
  label them with an alphabetical sequence); might need to just handle them
  manually (explicit labels in HTML, explicit `\appendix` entry for the latex
  output).

  The (small) problem is that for the HTML builder (so no appendix chapter
  labels) ``:numref:`` has no chapter, so it references out-of-section tables
  as "Table 1" even though it should be "Table A.1", etc.


Formatting
----------

* I wish I could use tables without borders for aligning sets of items. Do
  I *ever* want tables with borders? If not, I might be able to just redefine
  the `tabulary` environment. I think I can specify my own template
  `tabulary.tex_t`. The one with Sphinx is in `sphinx/templates/latex` I'd also
  need some CSS to fix the HTML tables...

* Check headings for consistent capitalization (title case or sentence case).
  Leaning towards sentence case.

* Verify against Cal Poly formatting

  * ref: http://www.grad.calpoly.edu/masters-thesis/masters-thesis.html

* Code literals (``like this``) are gray shaded in HTML, but have white
  backgrounds in the PDF. I tried setting ``'sphinxsetup':
  "VerbatimColor={rgb}{0.25,0.25,0.25}"`` in ``conf.py``, but that didn't seem
  to work. In the TeX output it looks like code literals are inside
  ``\sphinxcode`` elements; might start there?

* The "REFERENCES" link in the PDF is one page too high.

* The REFERENCES in the PDF should come *before* the appendices?


Bibliography
^^^^^^^^^^^^

* What label does Sphinx use with ``:ref:`` to link between sections? Does
  CalPoly require me to cite section **numbers**? I think sphinx typically
  substitutes section labels.

* Can my bibliography link backwards to sections that reference them? (That
  functionality is available in latex, but I forget how.)

* I think I can use multiple bibliographies. This might be useful since my
  topics are so varied. Should I?

  See: `<https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html>`_.

* Should I use "Lastname, Firstname"? See `thesis/notes/Notes 2019-W45`

* Do I need to redefine ``\bibsection`` in the Latex style? Do the "Memoir"
  defaults meet the style guidelines?

* Why does latex reorder my bibliography chapter to the end, after the
  appendices?


Publishing
----------

* Publish to Zenodo, add *concept DOI* to README, add DOI to `pfh.glidersim`
  documentation

* Do I need `sphinx.ext.githubpages`? What does it do?

* Low priority: add `sphinx.ext.linkcode` once `glidersim` is up on Github?

  https://github.com/scikit-learn/scikit-learn/blob/main/doc/sphinxext/github_link.py


Development
===========

* Use `pip-compile --generate-hashes`? See
  https://pip.pypa.io/en/latest/cli/pip_install/#hash-checking-mode


Sphinx
------

* Eliminate `tex/pwasu.sty`? Don't think I need it anymore.

* Add `sphinx-sitemap`

* Add `sphinxext.opengraph`

* Furo in dark mode brakes SVGs with white backgrounds. Review pictures and add
  white backgrounds where necessary for dark mode.


HTML
^^^^

* Add a logo?

* The footer (copyright and license) doesn't show on mobile


Scripts
=======

* The figures will largely be generated by `matplotlib` scripts. They must all
  use consistent styling. How should I define and apply that configuration?
  A project-local `matplotlibrc`? A Python script that the figures import and
  execute?


Miscellaneous
=============

* Create a project-local ``spellfile`` for vim (lots of project-specific
  words, like "kriging")

* I should mention that my canopy geometry supports "open" parafoil designs;
  it's easy to use just the upper surface and ignore the lower.
