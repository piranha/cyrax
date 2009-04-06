from jinja2 import Environment, FileSystemLoader, Undefined

from cyraxlib import typogrify, templatefilters, templatetags


class LoyalUnderfined(Undefined):
    def __getattr__(self, name):
        return

    __getitem__ = __getattr__


def initialize_env(source):
    '''
    Initialize environment.
    '''
    loader = FileSystemLoader(source)

    env = Environment(loader=loader, undefined=LoyalUnderfined,
                      extensions=[templatetags.MetaInfoExtension,
                                  templatetags.MarkExtension])

    filters = dict((f.__name__, f) for f in typogrify.filters)
    env.filters.update(filters)
    filters = dict((f.__name__, f) for f in templatefilters.filters)
    env.filters.update(filters)

    return env
