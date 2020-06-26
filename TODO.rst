* Should I use `h_a/R` for "angular momentum of the apparent mass `a` about
  `R`"?  I like the slash as "X with respect to Y", which makes sense here.

* I need a diagram for the 6 DoF model. I was going to just show the body
  centroid "B", but that makes it less obvious that the 6 DoF supports weight
  shift. Should all models include "P"? While I'm at it, is "B" still a good
  choice?

* Use the wing from Belloc as a case study. How to use my paraglider geometry
  to define/implement the wing from his description, then compare his wind
  tunnel performance to the estimate from Phillips method. Discuss likely
  sources of error. **They key notion is to show how his pointwise measurements
  can be converted into those six equations that define the paraglider
  canopy.** I'm not sure if I should define the entire wing plus analysis in
  a single section, or if this should be a recurring "Case Study" section that
  spans several chapters: "Paraglider Canopies", "Paraglider Wings", and
  "Paraglider Dynamics" (or whatever)

* Should my introduction chapter include a "Taxonomy of Tools" section that
  defines what I mean by *state estimation*, *parameter estimation*, *flight
  reconstruction*, *regression*, etc? It'd be interesting to define all the
  components, then finish the section by defining my project in terms of those
  components.

* I should mention that my canopy geometry supports "open" parafoil designs;
  it's easy to use just the upper surface and ignore the lower.

* I should probably use bold face for vectors and matrices; the over arrows
  are too messy

* I wish I could use tables without borders for aligning sets of items. Do
  I *ever* want tables with borders? If not, I might be able to just redefine
  the `tabulary` environment. I think I can specify my own template
  `tabulary.tex_t`. The one with Sphinx is in
  `~/.anaconda3/envs/science38/lib/python3.8/site-packages/sphinx/templates/latex`
  I'd also need some CSS to fix the HTML tables...

* Does "Bayesian filtering" deserve it's own chapter, or should it be part of
  the "Introduction" chapter?


Content Tasks
=============

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

* Should I choose standardize figure sizes? I'm not clear on how you choose
  scales with SVG, but I'm guessing if you start mixing up units it gets
  awkward (eg, mixing matplotlib or graphviz output with inkscape). At the
  least I should choose standard unit sizes (eg, coordinate axes are 1.5px
  thickness).

* Should I add a license to my SVG metadata? (Inkscape -> Document Properties)

* Make a list of some useful figures for each section, where applicable

* For each type of **script-generated** figure, develop a single, standard
  plotting function. Those functions should adhere to the following rules:
  take a filename for saving SVG files; text in SVG files should be left as
  text using "TeX Gyre Heros"; SVG outputs should not leave marginal
  whitespace.

* Figure labels must be globally unique. Should prototype some standard label
  prefixes. Might be based on the content of the figure (the specific object,
  or that object's domain) or the section that contains the figure

  At the least, it seems like a reasonable that **labels should match the
  figure filename.** This will probably preclude using section names, since
  I want to avoid renaming figure filenames if the sections change.

  While I'm at it, **the figure sources should match the figure labels** as
  well. It should be obvious where a figure came from.


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

* Should I use :math:`\mathcal{F}_a` for "frame a" etc?

* I wish that Steven's notation for forces and moments wasn't capital letters
  "F" and "M". I would really like to reserve lowercase-bold for vectors and
  uppercase-bold for matrices. In Hughes he uses lowercase `f` and `g` for the
  force and moment, which is also a bit annoying since `g` is typically
  reserved for gravity. I could use `m` but that's typically reserved for
  masses. **Maybe it's time I put my foot down that I simply like using
  brackets for matrices; it enables visual scanning you can't do otherwise.
  Also, they help reveal mistakes, kind of like physical units in equations.**

* I need to standardize `r_xy` instead of simply `r_x`. It improves symmetry.
  (You're designing in either the xy plane or the yz plane.)

  And do I like name `r` for the reference positions? I'm using that for
  vectors, these are scalars.


Terminology
-----------

* What markup style should I use for terms/definitions? (bold?)


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

* Verify against CalPoly formatting

  * ref: http://www.grad.calpoly.edu/masters-thesis/masters-thesis.html

* Chapter pages don't have page numbers

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


HTML
----

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
