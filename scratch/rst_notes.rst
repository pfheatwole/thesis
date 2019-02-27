Headings
========

From `Python's Style Guide for Formatting`_, a suggested set of heading labels
for RST documents are:

   # with overline, for parts
   * with overline, for chapters
   =, for sections
   -, for subsections
   ^, for subsubsections
   ", for paragraphs

The style guide is a part of the `Python Developer's Guide`_, which is itself
a great example set of RST documents:

.. _Python's Style Guide for Formatting:
   https://devguide.python.org/documenting/#style-guide

.. _Python Developer's Guide: https://github.com/python/devguide


Autoformatting
==============

TODO: Figure out how to disable autoformatting inside code RST blocks

* Need to blacklist `rstLiteralBlock` and `rstCodeBlock`

  https://github.com/reedes/vim-pencil#autoformat-blacklisting-and-whitelisting

  Depends on https://github.com/marshallward/vim-restructuredtext/issues/28
