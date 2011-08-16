# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '..')
import cyrax

# -- General configuration -----------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo']
source_suffix = '.rst'
master_doc = 'index'
project = u'Cyrax'
copyright = u'2009-2011, Alexander Solovyov'
version = release = cyrax.__version__
exclude_trees = ['_build']

# -- Options for HTML output ---------------------------------------------------

html_title = "%s v%s" % (project, version)
