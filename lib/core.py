import os, shutil, logging
import os.path as op

from cyrax.lib.conf import Settings
from cyrax.lib.env import initialize_env
from cyrax.lib.utils import new_base
from cyrax.lib.models import TYPE_LIST

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

    def render(self):
        self._render()
        self._copy_static()

    def _traverse(self):
        for path, _, files in os.walk(self.root):
            relative = path[len(self.root):].lstrip(os.sep)
            for f in files:
                if not f.startswith('_') and f.endswith('.html'):
                    self.add_page(op.join(relative, f))

    def add_page(self, path):
        self.entries.append(Entry(self, path))

    def _render(self):
        for entry in self.entries:
            entry.render()

    def _copy_static(self):
        # static should be placed somewhere else
        shutil.copytree(op.join(self.root, 'static'),
                        op.join(self.dest, 'static'))


class Entry(object):
    def __init__(self, site, path):
        self.site = site
        self.env = site.env
        self.path = path
        self.dest = self.site.dest
        self.template = self.env.get_template(path, globals={'entry': self})
        self.settings = Settings(self.site.settings)

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

        self.__class__ = new_base(self, Type)
        self.settings.type = Type.__name__.lower()

        # initialize my new base class
        super(self.__class__, self).__init__()

    def __repr__(self):
        return '<Entry: %r>' % self.path
        #return '<%s: %r>' % (self.settings.type.capitalize(), str(self))

    def __getitem__(self, name):
        return self.settings[name]

    def __getattr__(self, name):
        try:
            return self.settings[name]
        except KeyError:
            raise AttributeError

    def get_url(self):
        url = super(self.__class__, self).get_url()

        # to always make directories with .index files
        if url.endswith('/index') or url == 'index':
            url += '.html'
        elif not url.endswith('/'):
            url += '/'
        return url

    def get_dest(self):
        dest = op.join(self.dest, self.get_url())
        if not dest.endswith('.html'):
            dest = op.join(dest, 'index.html')
        return dest

    def collect(self):
        # some parameters are determined at render time
        self.template.render()

    def render(self):
        logger.info('Rendering %s' % self)
        path = self.get_dest()
        makedirs(op.dirname(path))
        file(path, 'w').write(self.template.render())
        logger.info('Successfully rendered %s' % self)
