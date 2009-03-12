import os
import os.path as op

from cyrax.lib.conf import Settings
from cyrax.lib.env import initialize_env

def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


class Site(object):
    def __init__(self, root, dest):
        self.root = root
        self.dest = dest
        self.settings = Settings()
        if op.exists(op.join(self.root, 'settings.cfg')):
            self.settings.read(file(op.join(self.root, 'settings.cfg')).read())

        self.env = initialize_env(root)
        self.env.globals['site'] = self
        self.entries = []

    def render(self):
        self.traverse()
        self._render()

    def traverse(self):
        for path, _, files in os.walk(self.root):
            relative = path[len(self.root):].lstrip('/')
            for f in files:
                self.add_page(op.join(relative, f))

    def add_page(self, path):
        self.entries.append(Entry(self, path))

    def _render(self):
        for entry in self.entries:
            entry.render()


class Entry(object):
    def __init__(self, site, path):
        self.site = site
        self.env = site.env
        self._settings = Settings(self.site.settings)
        self.path = path
        self.dest = op.join(self.site.dest, path)
        self.template = self.env.get_template(path, globals={'self': self})

    def render(self):
        makedirs(op.dirname(self.dest))
        file(self.dest, 'w').write(self.template.render())

