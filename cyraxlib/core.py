import os, shutil, logging
import os.path as op

from cyraxlib.conf import Settings
from cyraxlib.env import initialize_env
from cyraxlib.utils import new_base
from cyraxlib.models import TYPE_LIST

logger = logging.getLogger('core')


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


class Site(object):
    def __init__(self, root, dest):
        self.root = root
        self.dest = dest
        if op.exists(dest):
            shutil.rmtree(dest)

        self.settings = Settings(parent_tmpl='_base.html')
        conf = op.join(self.root, 'settings.cfg')
        if op.exists(conf):
            self.settings.read(file(conf).read())

        self.env = initialize_env(root)
        self.env.globals['site'] = self
        self.entries = []
        self._traverse()

    def __repr__(self):
        return '<Site: %r>' % self.root

    def __getitem__(self, name):
        return self.settings[name]

    def __getattr__(self, name):
        try:
            return self.settings[name]
        except KeyError:
            raise AttributeError

    def _traverse(self):
        for path, _, files in os.walk(self.root):
            relative = path[len(self.root):].lstrip(os.sep)
            if not relative.startswith('static'):
                for f in files:
                    if not f.startswith('_') and not f == 'settings.cfg':
                        self.add_page(op.join(relative, f))

    def add_page(self, path):
        self.entries.append(Entry(self, path))

    def render(self):
        for entry in self.entries:
            entry.render()
        self._copy_static()

    def _copy_static(self):
        logger.info('Copying static files')
        shutil.copytree(op.join(self.root, 'static'),
                        op.join(self.dest, 'static'))


class Entry(object):
    def __init__(self, site, path):
        self.site = site
        self.env = site.env
        self.path = path
        self.dest = self.site.dest

        self.settings = Settings(self.site.settings)
        self.template = self.env.get_template(path, globals={'entry': self})
        self.collect()

        # Determine type
        if 'type' in self.settings:
            try:
                type = self.settings.type.lower()
                Type = dict((x.__name__.lower(), x) for x in TYPE_LIST)[type]
            except KeyError:
                pass
        else:
            Type = None

        if not Type:
            for i in TYPE_LIST:
                if i.check(self):
                    Type = i
                    break

        if not Type:
            logger.info("Can't determine type for %s" % self)
            return

        self.__class__ = new_base(self, Type)
        self.settings.type = Type.__name__.lower()

        super(self.__class__, self).__init__()

        base = '_%s.html' % self.settings.type
        if op.exists(op.join(self.site.root, base)):
            self.settings.parent_tmpl = base

    def __repr__(self):
        return '<Entry: %r>' % self.path

    def __getitem__(self, name):
        return self.settings[name]

    def __getattr__(self, name):
        try:
            return self.settings[name]
        except KeyError:
            raise AttributeError

    def get_dest(self):
        return op.join(self.dest, self.get_url())

    def collect(self):
        # some parameters are determined at render time
        self.template.render()

    def render(self):
        logger.info('Rendering %s' % self)
        path = self.get_dest()
        makedirs(op.dirname(path))
        file(path, 'w').write(self.template.render())
