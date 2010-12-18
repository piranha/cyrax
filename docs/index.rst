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

Well, it's quite simple, as usually::

  pip install cyrax

If you've cloned `repository`_, then maybe you want to know that Cyrax depends
on Jinja2 template library and, if you want to use built-in server (for example
to look at your site when not deployed yet), on CherryPy (on their
``wsgiserver`` stuff).

.. _repository: http://hg.piranha.org.ua/cyrax/

Usage
-----

Run ``./cyrax``. Look at ``content`` `subdirectory`_ for example site.

.. _subdirectory: http://hg.piranha.org.ua/cyrax/file/tip/content/

Contents:

.. toctree::
   :maxdepth: 2

   formats
   usage

