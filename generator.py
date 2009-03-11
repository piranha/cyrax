import os.path as op
import os, shutil

from jinja2 import Environment
from jinja2 import BaseLoader, ChoiceLoader, FileSystemLoader, TemplateNotFound

from cyrax.lib import typogrify, templatefilters

ROOT = op.dirname(op.abspath(__file__))

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

    env = Environment(loader=loader, extensions=['cyrax.lib.templatetags.metainfo'])

    filters = dict((f.__name__, f) for f in typogrify.filters)
    env.filters.update(filters)
    filters = dict((f.__name__, f) for f in templatefilters.filters)
    env.filters.update(filters)

    return env


def generator(source, destination):
    '''
    Find all content files and render them into deploy location.
    '''
    if op.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    env = initialize_env(source)

    for path, dirs, files in os.walk(source):
        relative = path[len(source):]
        try:
            os.mkdir(op.join(destination, relative))
        except OSError:
            pass
        for f in files:
            if not f.startswith('_'):
                tmpl = env.get_template(op.join(relative, f))
                file(op.join(destination, relative, f), 'w').write(tmpl.render())
