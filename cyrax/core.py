import os, shutil, logging
import os.path as op
import sys
import glob

from cyrax.conf import Settings
from cyrax.template import initialize_env
from cyrax.utils import url2path, base_path
from cyrax.models import TYPE_LIST
from cyrax.events import events

try:
    import cyrax.rstpost
except ImportError:
    pass # no docutils :(


logger = logging.getLogger(__name__)
fnmatch = glob.fnmatch.fnmatch


def ishidden(name):
    return name.startswith('.') or name.startswith('_')


def impcallback(relpath, root):
    if not root in sys.path:
        sys.path.insert(0, root)
    modname, cbname = relpath.rsplit('.', 1)
    mod = __import__(modname, {}, {}, [1])
    return getattr(mod, cbname)


def get_entry(site, path):
    try:
        Type = (t for t in TYPE_LIST if t.check(site, path)).next()
    except StopIteration:
        logger.error("Can't determine type for %s" % path)
        return
    return Type(site, path)


class Site(object):
    def __init__(self, root, dest):
        self.root = root
        if op.exists(dest):
            shutil.rmtree(dest)

        self.settings = Settings(parent_tmpl='_base.html')
        conf = op.join(self.root, 'settings.cfg')
        if op.exists(conf):
            self.settings.read(file(conf).read().decode('utf-8'))

        site_base_path = base_path(self.url)
        self.dest = op.join(dest, url2path(site_base_path[1:]))

        self.env = initialize_env(root)
        self.env.globals['site'] = self
        self.entries = []

        if self.settings.get('sitecallback'):
            callback = impcallback(self.settings.sitecallback, self.root)
            callback(self)

        self._traverse()

    @property
    def url(self):
        return getattr(self.settings, 'url', '/')

    def __repr__(self):
        return '<Site: %r>' % self.root

    def __getitem__(self, name):
        return self.settings[name]

    def __getattr__(self, name):
        try:
            return self.settings[name]
        except KeyError, e:
            raise AttributeError(str(e))

    def _traverse(self):
        events.emit('traverse-started', site=self)
        exclude = self.settings.get('exclude', [])

        for path, _, files in os.walk(self.root):
            relative = path[len(self.root):].lstrip(os.sep)
            if (not relative.startswith('static') and
                not any(map(ishidden, relative.split(op.sep)))):
                for f in files:
                    full = op.join(relative, f)
                    if (f != 'settings.cfg' and
                        not ishidden(f) and
                        not any(map(lambda x: fnmatch(full, x), exclude))):
                        self.add_page(op.join(relative, f).replace('\\', '/'))

        events.emit('site-traversed', site=self)

    def add_page(self, path):
        self.entries.append(get_entry(self, path))

    def render(self):
        for entry in self.entries:
            entry.render()
        events.emit('site-rendered', site=self)
        self._copy_static()

    def _copy_static(self):
        if op.exists(op.join(self.root, 'static')):
            logger.info('Copying static files')
            shutil.copytree(op.join(self.root, 'static'),
                            op.join(self.dest, 'static'))
