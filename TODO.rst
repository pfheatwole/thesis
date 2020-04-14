Sphinx
======

* Re-run ``sphinx-quickstart`` and see how the new ``conf.py`` defaults
  compare to my current version (from July 2017)


Content Tasks
=============

* Write a list of topics

  This is essentially an unordered outline whose purpose is to set the scope
  of the text. What are the topics I will need to cover? What is its impact?

* Write an outline

* Write an introduction

* Outline the atmospheric estimation process


References
----------

* Create a list of topics relevant for "prior art" papers (paraglider
  dynamics, wind field estimation, thermal estimation, etc)

* Create a list of sources for each topic, including summary notes

* The "REFERENCES" link in the PDF is one page too high.

* The REFERENCES in the PDF should come *before* the appendices?


Drafting
--------

#. Write an informal overview of the goal, problems, resources, and solutions.
   This should be conversational: I can get through a description of my
   project when talking to the Mohlers, I should be able to put it down on
   paper. The key is to avoid getting hung up on the technical specifics.
   Those can be filled in later.

#. Review each section has adequately description assumptions. You need to
   establish the assumptions and constraints of your method to make sure you
   don't overpromise.

#. Annotate the informal draft with **text-only** descriptions of good
   supporting material (figure descriptions, equations, code references, etc.)
   Don't worry about actually producing those elements; this is about
   establishing a pathway to a cohesive structure: once you know what elements
   you really want, only then should you spend time creating them.


Figures
=======

* Make a list of some useful figures for each section, where applicable

* For each type of figure, develop a single, standard plotting function. Those
  functions should adhere to the following rules: take a filename for saving
  SVG files; text in SVG files should be left as text using "TeX Gyre Heros";
  SVG outputs should not leave marginal whitespace.

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

  * Page numbering should start on page 1
   
  * Chapter titles and section headings are not styled correctly

* Code literals (surrounded by ``\`\```) are gray shaded in HTML, but have
  white backgrounds in the PDF. I tried setting ``'sphinxsetup':
  "VerbatimColor={rgb}{0.25,0.25,0.25}"`` in ``conf.py``, but that didn't seem
  to work. In the tex ouput it looks like code literals are inside
  ``\sphinxcode`` elements; might start there?


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


Miscellaneous
=============

* Create a project-local ``spellfile`` for vim (lots of project-specific
  words, like "kriging")
