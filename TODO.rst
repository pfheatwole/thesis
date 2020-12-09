* Make sure every chapter introduction has a "Roadmap", and that the chapter
  follows that roadmap.

* Make sure all the chapters follow the same structure
  (`meta/editing:Content:Chapter structure`)

* Outline the content of an IGC file in the `Introduction`, since the absence
  of wind vector data is what motivates flight reconstruction.

* Review `introduction:SCRATCH`. Might have some useable stuff there.

* Merge `data_considerations` into `future_work`. I should frame my
  application of sequence alignment as a suggested starting points, which is
  fine since it's basically untested anyway.

* Review source for mentions of a "chord surface"

* Verify my use of *dihedral* and *anhedral*. At the least I think my use of
  "mean anhedral" is suspect; probably not even a helpful term.


* In `generate_canopy_examples.py`, there's a function `_plot_foil` that
  appears to duplicate `gsim.plots.plot_foil`. Why does it exist?

* Reconsider using `O` for the origin? Looks like a zero.

* If the HTML "Navigation" frame gets too long it goes off the screen, and you
  can't scroll it.

* Add a description of a *direction cosine matrix* to `symbols`? Or maybe the
  `glossary`?

* Write up an informal description of "this is how a pilot standing on the
  ground would estimate the wind by watching a glider in the air". That
  informal description is the stepping stone to understanding "flight
  reconstruction" and how it is possible even though the answers are only
  approximate.

* Create two parallel outlines, informal and formal, for the overall paper:
  work through developing the idea of "predicting points of the wind field by
  learning from the past". The informal development should be easy to read by
  a non-technical reader. It should function as a guide to show that the math
  isn't as scary as it might seem; the notation is intimidating, but
  ultimately it's based on logic that the reader already understands.


* Should my introduction chapter include a "Taxonomy of Tools" section that
  defines what I mean by *state estimation*, *parameter estimation*, *flight
  reconstruction*, *regression*, etc? It'd be interesting to define all the
  components, then finish the section by defining my project in terms of those
  components.


Topical
=======


Canopy geometry
---------------

* How do I argue that my definition of `r_LE/RP` decouples the parameters? You
  can see in the math that `r_LE/RP` and `r_P/LE` both involve `c` and
  `C_c/s`, but it won't be obvious that it counteracts the changes to keep the
  parameters decoupled.

* Where do I define *design parameters* (span, taper, etc)? Should be pretty
  early on on `Canopy Geometry` when I'm motivating parametric models.

* Finish the derivation of my parametrized wing geometry in `derivations`. The
  goal is to derive the version that uses `R` (configurable reference points),
  but keep the parafoil-related material in `Canopy Geometry`.

* Complete the parametric design choices for parafoils in `Canopy Geometry`.
  The choice to set `r_y = r_z`, how I define `C_c/s`, show some parametric
  curves (eg, elliptical chord), etc.


Content Tasks
=============

* Use the wing from Belloc as a case study. How to use my paraglider geometry
  to define/implement the wing from his description, then compare his wind
  tunnel performance to the estimate from Phillips method. Discuss likely
  sources of error. **They key notion is to show how his pointwise measurements
  can be converted into those six equations that define the paraglider
  canopy.** I'm not sure if I should define the entire wing plus analysis in
  a single section, or if this should be a recurring "Case Study" section that
  spans several chapters: "Paraglider Canopies", "Paraglider Wings", and
  "Paraglider Dynamics" (or whatever)

* Review the rambling "derivation" of the canopy geometry. In particular,
  eliminate that old version that used `\hat{x}_a`, it's a distraction.

  In fact, remove most of that content entirely. I'm moving the derivation of
  the general equation for points on the chord surface into the "Derivations"
  chapter. **The "Canopy Geometry" chapter should be specifically about (1)
  observing the important details of a canopy geometry, and (2) choosing
  a parametrization of the general equation that is most suitable for
  capturing those design details.**

* Record the momentum derivatives for Barrows in the derivation. It wasn't
  clear from the paper exactly how those worked.

* Sketch a directed graph of the processing pipeline for converting
  paragliding flight tracks into an in-flight predictive model. (This might be
  helpful for motivating the structure of the paper.)


Drafting
--------

#. **Define the concrete "key ideas" for the paper.** These will drive how
   I develop the entire paper, both in structure and content. (Possibly start
   with the non-technical development, then convert that into technical terms.
   It requires probabilistic methods, so satisfying the needs of that math
   should do a pretty good job establishing the core components of the paper.)

#. Develop a topic outline. (Topic ordering implicitly encodes dependencies.)

#. Write an informal overview of the goal, problems, resources, and solutions.
   This should be conversational: I can get through a description of my
   project when talking to the Mohlers, I should be able to put it down on
   paper. The key is to avoid getting hung up on the technical specifics.
   Those can be filled in later.

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


References
----------

* Create a list of topics relevant for "prior art" papers (paraglider
  dynamics, wind field estimation, thermal estimation, etc)

* Create a list of sources for each topic, including summary notes


Figures
-------

* I need a diagram for the 6 DoF model. I was going to just show the body
  centroid "B", but that makes it less obvious that the 6 DoF supports weight
  shift. Should all models include "P"? While I'm at it, is "B" still a good
  choice?

* My brake deflection plots are wrong. It assumes fixed hinges at 0.8c, which
  is very very wrong for the airfoil data I'm using with my Hook3ish

* Factor out the canopy plotting function from the thesis script
  `generate_canopy_examples.py` (the one with the faux grid). I'd like to use
  it to to plot my Hook3ish

* Add licenses to my SVG metadata (Inkscape -> Document Properties)

* Figure labels must be globally unique, so standardized label prefixes would
  probably help. Could be based on the content of the figure (the specific
  object, or that object's domain) or the section that contains the figure.

  At the least, it seems like a reasonable that **labels should match the
  figure filename.** This will probably preclude using section names, since
  I want to avoid renaming figure filenames if the sections change.

  While I'm at it, **the figure sources should match the figure labels** as
  well. It should be obvious where a figure came from (within reason)

* Remove scratch/unused figures (eg, `elliptical_arc_dihedral.svg`)


Extras
------

* Suppose you had the wind vectors. Assume you've identified some thermals.
  Any hope of identifying likely **causes**? Causal explanations seem like
  a lot of work, but things like topography (identifying orographic lift) or
  materials (identifying likely thermal triggers, like exposed dirt versus
  surrounding green areas, or identifying likely sinks, like water locations).

  If you think about this like a geostatistician you might think about
  relating the observations (wind vectors) to other data (topography, surface
  characteristics, etc).


Editorial Tasks
===============

* I'd like the ability to render sections to a PDF for markup. The PDF should
  be localized to a specific section to avoid a "too much to chew" situation.
  Each PDF should reference the git SHA hash; maybe
  "YYYYMMDD-HHMMSS_SECTION_SHA.pdf". It gets messy since you can't always fix
  all the issues at once, so you'll end up with a PDF with some fixes
  corrected and some not. **How do you track when a revision has been
  completed?**


Writing Style
-------------

* Choose a voice

  * Passive vs active (I strongly lean towards active, but be consistent)

  * "We will", "I will", "this paper will", etc?


Notation, Math, etc
-------------------

* Use `h_a/R` for "angular momentum of the apparent mass `a` about `R`"?
  I like the slash as "X with respect to Y", which makes sense here.

* Should I use :math:`\mathcal{F}_a` for "frame a" etc?

* I wish that Steven's notation for forces and moments wasn't capital letters
  "F" and "M". I would really like to reserve lowercase-bold for vectors and
  uppercase-bold for matrices. In Hughes he uses lowercase `f` and `g` for the
  force and moment, which is also a bit annoying since `g` is typically
  reserved for gravity. I could use `m` but that's typically reserved for
  masses. **Maybe it's time I put my foot down that I simply like using
  brackets for matrices; it enables visual scanning you can't do otherwise.
  Also, they help reveal mistakes, kind of like physical units in equations.**

* When do you need to specify a reference frame in my mathematical notation?
  (See `notes-202048:Math` for some thoughts.)

* I'm getting sick of `\mathrm` for all the points (like
  `r_{\mathrm{P}/\mathrm{LE}}`). Can I write a latex macro that will wrap them
  for me?


Terminology
-----------

* Everywhere I say "mean anhedral", what I really mean is "arc anhedral" (so
  "the anhedral of the arc" as opposed to "section anhedral").

* Should I define a Sphinx role for terms/definitions? There's already
  a `:term:` role that requires they be in a glossary, but using explicit
  asterisk wrappers is a bit fragile.


* Review the text for `Gamma` as a reference to section dihedral. I've
  abandoned Gamma in favor of traditional Euler angle parameters.


Structural
----------

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

* Introductions: I am using implicit introductions (chapter text preceding
  the first section). Should they be explicit? Some authors even use both
  (Frigola-Alcade's dissertation, for example). **This will probably depend on
  whether any of the introductions require subsections.**

* What sections should have PDF bookmarks?

   * Use `\currentpdfbookmark{label}{bookmarkname}`

   * Update (20191107): I don't know what this means?

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
  `tabulary.tex_t`. The one with Sphinx is in
  `~/.anaconda3/envs/science38/lib/python3.8/site-packages/sphinx/templates/latex`
  I'd also need some CSS to fix the HTML tables...

* Check headings for consistent capitalization (title case or sentence case).
  Leaning towards sentence case.

* Verify against CalPoly formatting

  * ref: http://www.grad.calpoly.edu/masters-thesis/masters-thesis.html

* Code literals (surrounded by ``\`\```) are gray shaded in HTML, but have
  white backgrounds in the PDF. I tried setting ``'sphinxsetup':
  "VerbatimColor={rgb}{0.25,0.25,0.25}"`` in ``conf.py``, but that didn't seem
  to work. In the tex ouput it looks like code literals are inside
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

* Should I use "Lastname, Firstname"? See "thesis/notes/Notes 2019-W45"

* Do I need to redefine ``\bibsection`` in the Latex style? Do the "Memoir"
  defaults meet the style guidelines?

* Why does latex reorder my bibliography chapter to the end, after the
  appendices?


Sphinx
======

* Re-run ``sphinx-quickstart`` and see how the new ``conf.py`` defaults
  compare to my current version (from July 2017)

* Update to Sphinx 4 (and thus MathJax 3)


HTML
----

* Add a document title below the sidebar logo?

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
