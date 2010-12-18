============
File formats
============

.. _configformat:

Configuration format
--------------------

Basically configuration format is a list of key-value pairs, where each pair
should be located on a separate line, like this::

  title: Some title
  author: Some author

It can contain different data formats, namely:

- list
  ::

    key: [list, of, values]

- dictionary
  ::

    key: {key: value, key: value}

- date
  ::
   
    key: date: yyyy-mm-dd HH:MM:SS

  This format is currently the only one which is supported.

- boolean value
  ::

    key: true
    key: false

   Case insensitive, with possible values for ``True``: `true`, `yes`,
   `on`. For ``False``: `false`, `no`, `off`.

Everything else is a string, with an exception for fields with name ``date`` -
value of those are checked to be a date value. In other case, string is
returned.

Template formats
----------------

Jinja2 is used as a template engine, so basic template (leading to
identification of page as ``Page`` object) is a Jinja2 template, which extends
parent template.

Every Jinja2 template in Cyrax can use ``{% meta %} ... {% endmeta %}`` tag,
which should contain text in :ref:`configformat`, setting up and overrding options for
current page.

Parent template
~~~~~~~~~~~~~~~

Each entry has a ``parent_html``, from which it will be inherited. It is
determined by model name, as ``_<lowered model name>.html``. In case it does not
exist, ``_base.html`` is used (can be overridden, see ``parent_tmpl`` in
:ref:`config`).

Models
------

There are few models for different templates coming with Cyrax predefined, and
you can define your own using a ``sitecallback`` :ref:`config` variable
by adding new models to ``cyraxlib.models.TYPE_LIST``.

Models are just descendants of an ``object``, defining
py:classmethod:`check(entry)` which should determine if passed entry is an
instance of a given model. Another requirement is
py:method:`get_relative_url()`, which should return URL where rendered entry
will be located, relative to site root.

Common configuration variables:

- ``isdir`` (default: ``True``) - should current entry be rendered as a
  directory with ``index.html`` inside or a simple file.

- ``type`` (default: ``None``) - predefine type of current entry, without
  running ``check()`` from every model.

NonHTML
~~~~~~~

Model for entries whose extension doesn't end with ``.html``, usually last of
models in ``TYPE_LIST``. ``isdir`` returns ``False`` by default.
  
Page
~~~~

Page is a model for single html pages and it's ``check()`` returns ``True`` if
path ends with ``.html``. Does nothing special.

Post
~~~~

Model for a blog post, determined by checking if it's name is prepended with a
date (either separated by dashes or by slashes,
f.e. 'blog/2010/03-14-some-post.html').

Special behavior contains adding itself to a sorted collection of posts on a
``Site`` object (``site.posts``) and by adding tag from ``tags`` to a sorted
collection of tags on ``Site`` object (``site.tags``).

Configuration variables:

- ``tags`` (default: ``[]``) - list of tag names.

Tag
~~~

Entry for a tag. Most of the special behavior is done by adding an event handler
to ``site-travered`` signal, which adds virtual pages for tags.
