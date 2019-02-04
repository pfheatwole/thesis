These are some scratch notes regarding the `memoir` LaTeX class.

* It can produce **glossaries** and **lists of symbols**

  Excellent for all the math I'll be doing

* It doesn't work with the standard **hyperref** package

   * You must use **memhfixc** after using *hyperref*
   * Recent versions of **hyperref** apply this automatically

* Provides its own flavor of some packages

   * **fancyhdr**, **geometry**, **crop**, etc
   * Probably want to disable **fancyhdr** in Sphinx?


Terminology
-----------

 * **recto** page: odd pages, front of the leaf
 * **verso** page: even pages, (back of the leaf
 * **folio**: page number
 * **pagination**: pages with *folios*
 * **preamble**: the region between the `\documentclass` and the start of the
   `document` environment
