.. -*- mode: rst -*-

=======
 Cyrax
=======

Cyrax is a static site generator using Jinja2_ template engine.

It's inspired by Jekyll_ and Hyde_ site generators and started when I realized
that I'm dissatisfied with both of them for different reasons. When I tried to
come up with name I remembered my favourite character from Mortal Kombat 3 so
here we go.

Installation
------------

Well, it's quite simple, as usually::

  pip install cyrax

Cyrax depends on the Jinja2 template library, so you can install it through your OS
package system (in other case pip will install it automatically).

Note, please, that in order to use parsers like markdown, or reST, or textile,
corresponding libraries should be installed (either python-markdown or
python-markdown2 are good enough for markdown).

Usage
-----

Read some docs_, run ``cyrax --help`` to read about command line options, look
at `example site`_.

Also it's really easy to extend Cyrax, see `an example`_.

.. _an example: https://github.com/piranha/osgameclones/blob/master/_ext.py

News
----

Indeed something happens with each release and you are probably interested what
(and too lazy to read `changelog`_).

.. _changelog: http://github.com/piranha/cyrax/

2.7 (11.10.2016)
~~~~~~~~~~~~~~~~

- support for globs in `exclude` in `settings.cfg`

2.6 (10.10.2016)
~~~~~~~~~~~~~~~~

- make Jinja2 `do` extension available in templates

2.4-2.5 (16.08.2011)
~~~~~~~~~~~~~~~~~~~~

- drop unused dependency on cherrypy
- make rst render start with h2 in inner sections

2.3 (28.12.2010)
~~~~~~~~~~~~~~~~

- rework RstPost a bit, removing nasty bugs with template caching

2.1-2.2 (21.12.2010)
~~~~~~~~~~~~~~~~~~~~

- nasty bug with circular dependecies
- forget to process tags in RstPost

2.0 (18.12.2010)
~~~~~~~~~~~~~~~~

- refactored module system, no more ``cyraxlib``, only ``cyrax`` now exists
- completely refactored internal models system, now it uses usual inheritance
  instead of some strange composition (which means it's easier to understand
  and to extend now)
- ability to write posts in reStructuredText (which as well could serve as an
  `example`_ to writing your own models).

.. _example: http://github.com/piranha/cyrax/blob/master/cyrax/rstpost.py

1.0-1.1 (28.11.2010)
~~~~~~~~~~~~~~~~~~~~

- now most of urls generated on page (by function ``url_for``) are relative to
  current page, which means that you mostly can view your site without using
  web-server (though you'll need to click on ``index.html`` yourself :)
- some docs, heh. This part needs attention anyway

.. _Jinja2: http://jinja.pocoo.org/2/
.. _Jekyll: http://github.com/mojombo/jekyll/
.. _Hyde: http://github.com/lakshmivyas/hyde/
.. _repository: http://github.com/piranha/cyrax/
.. _docs: http://cyrax.readthedocs.org/
.. _example site: http://github.com/piranha/cyrax/tree/master/content/
