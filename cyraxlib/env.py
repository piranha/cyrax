from jinja2 import Environment, FileSystemLoader

from cyraxlib import typogrify, templatefilters, templatetags


def initialize_env(source):
    '''
    Initialize environment.
    '''
    loader = FileSystemLoader(source)

    env = Environment(loader=loader, extensions=[templatetags.MetaInfoExtension,
                                                 templatetags.MarkExtension])

    filters = dict((f.__name__, f) for f in typogrify.filters)
    env.filters.update(filters)
    filters = dict((f.__name__, f) for f in templatefilters.filters)
    env.filters.update(filters)

    return env
