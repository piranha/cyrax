============
File formats
============

.. _config:

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

Template format
---------------

Jinja2 is used as a template engine, so basic template (leading to
identification of page as ``Page`` object) is a Jinja2 template, which extends
parent template (by default ``_base.html``, see ``parent_tmpl`` in
:ref:`configuration`).

Every Jinja2 template in Cyrax can use ``{% meta %} ... {% endmeta %}`` tag,
which should contain text in :ref:`config`, setting up and overrding options for
current page.

