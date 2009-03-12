import os.path as op

from jinja2 import Environment
from jinja2 import BaseLoader, ChoiceLoader, FileSystemLoader, TemplateNotFound

from cyrax.lib import typogrify, templatefilters, templatetags

import cyrax
ROOT = op.dirname(op.abspath(cyrax.__file__))


class ThemeLoader(BaseLoader):
    '''
    A loader which loads template from selected theme.
    '''
    def __init__(self, theme):
        self.theme = theme

    def get_source(self, env, template):
        path = op.join(ROOT, 'themes', self.theme, template)
        if not op.exists(path):
            raise TemplateNotFound(template)
        mtime = op.getmtime(path)
        source = file(path).read().decode('utf-8')
        return source, path, lambda: mtime == op.getmtime(path)


def initialize_env(source):
    '''
    Initialize environment.
    '''
    loader = ChoiceLoader([
        FileSystemLoader(source),
        ThemeLoader('default')
        ])

    env = Environment(loader=loader, extensions=[templatetags.MetaInfoExtension])

    filters = dict((f.__name__, f) for f in typogrify.filters)
    env.filters.update(filters)
    filters = dict((f.__name__, f) for f in templatefilters.filters)
    env.filters.update(filters)

    return env
