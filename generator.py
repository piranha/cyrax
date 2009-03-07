import os.path as op
import os, shutil

from jinja2 import Environment
from jinja2 import BaseLoader, ChoiceLoader, FileSystemLoader, TemplateNotFound

ROOT = op.dirname(__file__)

class ThemeLoader(BaseLoader):
    '''
    A loader which loads template from selected theme.
    '''
    def __init__(self, theme):
        self.theme = theme

    def get_source(self, env, template):
        path = op.join(ROOT, 'themes', template)
        if not op.exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        source = file(path).read().decode('utf-8')
        return source, path, lambda: mtime == getmtime(path)

def generator(source, destination):
    shutil.rmtree(destination)
    os.mkdir(destination)

    loader = ChoiceLoader([
        FileSystemLoader(source),
        ThemeLoader('default')
        ])

    env = Environment(loader=loader)

    for path, dirs, files in os.walk(source):
        relative = path[len(source):]
        os.mkdir(op.join(destination, relative))
        for f in files:
            tmpl = env.get_template(op.join(relative, f))
            file(op.join(destination, relative, f), 'w').write(tmpl.render())