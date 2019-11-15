.. ::

   This filename is prefixed with a `z` to ensure it is processed last, which
   is important for `sphinxcontrib-bibtex` to create the citation.

   See: https://sphinxcontrib-bibtex.readthedocs.io/en/latest/usage.html#issue-unresolved-citations

.. only:: html or singlehtml

    **********
    References
    **********

.. ::

   When Sphinx generates the `\bibsection` for the PDF it will use the
   redefined version from the Latex style. The style file redefines the
   `\bibname` to "REFERENCES" and adds it to the table of contents.

.. bibliography:: references.bib
   :style: unsrt
