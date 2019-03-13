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


Drafting Tasks
==============

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

* What sections should have PDF bookmarks?

   * Use `\currentpdfbookmark{label}{bookmarkname}`

* Appendices only need a single `\appendix` call; how to organize the TOC?


Formatting
----------

* Verify against CalPoly formatting
  
  * ref: http://www.grad.calpoly.edu/masters-thesis/masters-thesis.html

  * Page numbering should start on page 1
   
  * Chapter titles and section headings are not styled correctly


Bibliography
^^^^^^^^^^^^

* `sphinxcontrib-bibtex` provides the `unsrt` style, but I'd rather it use
  `Lastname, Firstname` ordering. How difficult is that?

  See: https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html#custom-formatting-sorting-and-labelling
