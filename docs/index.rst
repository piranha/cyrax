.. _index:

=======
 Cyrax
=======

What's Cyrax?
-------------

Cyrax is a static site generator using Jinja2_ template engine.

It's inspired from Jekyll_ and Hyde_ site generators and started when I realized
that I'm dissatisfied with both of them by different reasons. When I tried to
come up with name I remembered my favourite character from Mortal Kombat 3 so
here we go.

.. _Jinja2: http://jinja.pocoo.org/2/
.. _Jekyll: http://github.com/mojombo/jekyll/
.. _Hyde: http://github.com/lakshmivyas/hyde/

Installation
------------

Cyrax depends on Jinja2 template library, you should either install it as your
distribution prefers (it's present in most of major distributions, particularly
in Debian and MacPorts), or use ``easy_install``::

   pip install jinja2

Get the cyrax by either cloning repository_ or downloading an archive_.

If you want to use built-in webserver, you could also install CherryPy 3, either
by your distribution tools or by ``easy_install``::

   pip install CherryPy

.. _repository: http://hg.piranha.org.ua/cyrax/
.. _archive: http://hg.piranha.org.ua/cyrax/archive/tip.tar.gz

Usage
-----

Run ``./cyrax``. Look at ``content`` subdirectory for example site.

Contents:

.. toctree::
   :maxdepth: 2

   formats
   usage

