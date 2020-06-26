#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Thesis documentation build configuration file, created by
# sphinx-quickstart on Mon Jul 24 16:10:21 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # 'sphinx.ext.imgmath',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
    'sphinxcontrib.bibtex',
    'sphinxcontrib.rsvgconverter',
]

autosectionlabel_prefix_document = True

# zoom_factor = (10 / 72) / (16 / 96)  # PDF uses 11pt fonts, web uses 16px
zoom_factor = 0.6  # FIXME: this empirical solution works much better; why?
rsvg_converter_args = ["-z", str(round(zoom_factor, 2))]

# autosectionlabel will warn if a section label is reused inside a single
# document, regardless of section depth. Suppress those manually.
suppress_warnings = [
    # 'autosectionlabel.paraglider_model', # Outdated, but keeping it as an example
    'autosectionlabel.*',  # Assume I use fully-qualified section references
]

mathjax_config = {
    "TeX": {  # Define TeX macros for MathJax 2.7 (3.0 changed the spec)
        "extensions": ["cancel.js"],
        "Macros": {
            "given": r"\;\middle\vert\;",
            "vec": [r"\mathbf{#1}", 1],
            # "mat": [r"\left[#1\right]", 1],
            # "crossmat": [r"\mat{#1}^{\times}", 1],
            "mat": [r"\mathbf{#1}", 1],
            "crossmat": [r"\left[{#1}\right]^{\times}", 1],
        },
    },
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Paraglider Flight Reconstruction'
copyright = "2020, Peter Frank Heatwole"
author = 'Peter Frank Heatwole'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ''
# The full version, including alpha/beta/rc tags.
release = ''

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['build', 'scratch', 'TODO.rst', 'figures']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

numfig = True  # Enable numbered figure and table references in HTML

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
html_title = project  # Override "<project>'s documentation"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'logo': 'hook3_vectorized_opt.svg',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Thesisdoc'


# -- Options for LaTeX output ---------------------------------------------

EXTRA_PREAMBLE = r"""
\usepackage{csu}
\usepackage{cancel}
\newcommand{\given}{\;\middle\vert\;}
\renewcommand{\vec}{\mathbf}
\newcommand{\mat}[1]{\left[#1\right]}
\newcommand{\crossmat}[1]{\mat{#1}^{\times}}
\renewcommand{\arraystretch}{1.5}
"""

latex_engine = "xelatex"  # pdflatex has poor unicode support

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '11pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    'preamble': EXTRA_PREAMBLE,
    'fontpkg': r'''
        \PassOptionsToPackage{bookmarksnumbered}{hyperref}
        ''',

    # Configure memoir
    'extraclassoptions': 'openany,oneside',
    # 'maketitle': r'\thetitlepage',
    'maketitle': '',  # Disable so I can call \frontmatter first
    # 'tableofcontents': '\\tableofcontents',
    'tableofcontents': '',
    'fncychap': '',

    'makeindex': '',
    'printindex': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',

    'sphinxsetup':
        "TitleColor={named}{black}"
        + ",InnerLinkColor={rgb}{0.208,0.374,0.486}"
        + ",OuterLinkColor={rgb}{0.208,0.374,0.486}",
}

latex_additional_files = [
    'tex/csu.sty'
]


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ('index', 'Thesis.tex', project,
     'Peter Frank Heatwole', 'memoir'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'thesis', 'Thesis Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Thesis', 'Thesis Documentation',
     author, 'Thesis', 'One line description of project.',
     'Miscellaneous'),
]
