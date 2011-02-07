# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '..')
import cyrax

# -- General configuration -----------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Cyrax'
copyright = u'2009-2011, Alexander Solovyov'
version = release = cyrax.__version__
exclude_trees = ['_build']
pygments_style = 'sphinx'

# -- Options for HTML output ---------------------------------------------------

html_theme = 'cleanery'
html_theme_path = ['.']
html_title = "%s v%s" % (project, version)
