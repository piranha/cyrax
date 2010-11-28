=============
 Cyrax usage
=============

Main executable is ``cyrax``. Run it in a directory with site sources to compile
your site. It expects file `settings.cfg` in a directory it's started in.

.. _config:

Configuration
-------------

``settings.cfg`` is a main site configuration file and has to be written in a
simple :ref:`configformat`. Possible configuration options used by Cyrax core:

- ``parent_tmpl`` - name of parent template for a ``Page`` object. Defaults to
  ``_base.html``.

- ``exclude`` - list of filenames to excluded from resulting site.

- ``sitecallback`` - Python path to function, which takes a ``Site`` object as
  an argument before traversing tree of files and can perform some
  modifications to behavior of Cyrax. Example_.

Any other options will be set on your ``Site`` object, which is available in any
template under name of ``site``.

.. _Example: http://hg.piranha.org.ua/piranha.org.ua/file/tip/_ext.py#l1
