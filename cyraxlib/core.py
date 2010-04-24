import os, shutil, logging, datetime, time
import os.path as op
import sys

from cyraxlib.conf import Settings
from cyraxlib.env import initialize_env
from cyraxlib.utils import new_base, safe_url_join, url2path, get_base_path
from cyraxlib.models import TYPE_LIST
from cyraxlib.events import events

logger = logging.getLogger('core')


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass

def ishidden(name):
    return name.startswith('.') or name.startswith('_')

def impcallback(relpath, root):
    if not root in sys.path:
        sys.path.insert(0, root)
    modname, cbname = relpath.rsplit('.', 1)
    mod = __import__(modname, {}, {}, [1])
    return getattr(mod, cbname)

class Site(object):
    def __init__(self, root, dest):
        self.root = root
        if op.exists(dest):
            shutil.rmtree(dest)

        self.settings = Settings(parent_tmpl='_base.html')
        conf = op.join(self.root, 'settings.cfg')
        if op.exists(conf):
            self.settings.read(file(conf).read().decode('utf-8'))
        
        site_base_path = get_base_path(getattr(self.settings, 'url', '/'))
        self.dest = op.join(dest, url2path(site_base_path[1:]))

        self.env = initialize_env(root)
        self.env.globals['site'] = self
        self.entries = []
        self.tags = {}

        if self.settings.get('sitecallback'):
            callback = impcallback(self.settings.sitecallback, self.root)
            callback(self)

        self._traverse()

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
        for path, _, files in os.walk(self.root):
            relative = path[len(self.root):].lstrip(os.sep)
            if (not relative.startswith('static') and
                not any(map(ishidden, relative.split(op.sep)))):
                for f in files:
                    if (f != 'settings.cfg' and
                        not ishidden(f) and
                        op.join(relative, f) not in self.settings.get('exclude',
                                                                      [])):
                        self.add_page(op.join(relative, f).replace('\\', '/'))
        events.emit('site-traversed', site=self)

    def add_page(self, path):
        self.entries.append(Entry(self, path))

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


class BaseEntry(object):
    'Class, used in collection phase, when type is not determined yet'
    def get_relative_url(self):
        return ''

class Entry(BaseEntry):
    def __init__(self, site, path, source=None):
        '''Initialize an entry

        This involves change of base class by running static method Class.check
        of every member of models.TYPE_LIST.

        Arguments:

         - `site`: site this entry belongs to
         - `path`: relative path to source template and to result
         - `source`: ability to override source template, means that current
            entry is "virtual" (has no real equivalent in source directory).
            Hence `mtime` will be current time.
        '''
        self.site = site
        self.path = path

        if source:
            self.mtime = datetime.datetime.now()
        else:
            mtime = op.getmtime(op.join(site.root, path))
            self.mtime = datetime.datetime(*time.gmtime(mtime)[:6])

        self.settings = Settings(parent=self.site.settings)
        self.template = site.env.get_template(source or path,
                                              globals={'entry': self})
        self._type_determined = False
        self.collect()
        if not self._type_determined:
            self._determine_type()

    def _determine_type(self):
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
            logger.info("Can't determine type for %s" % self.get_relative_url())
            return

        self.__class__ = new_base(self, Type)
        self.settings.type = Type.__name__.lower()

        base = '_%s.html' % self.settings.type
        if op.exists(op.join(self.site.root, base)):
            self.settings.parent_tmpl = base

        super(self.__class__, self).__init__()

        self._type_determined = True

    def __repr__(self):
        type = self.settings.get('type', '').capitalize() or 'Entry'
        return '<%s: %r>' % (type, self.path)

    def __getitem__(self, name):
        return self.settings[name]

    def __getattr__(self, name):
        try:
            return self.settings[name]
        except KeyError:
            raise AttributeError

    def isdir(self):
        return self.settings.get('isdir', True)

    def get_dest(self):
        path = op.join(self.site.dest, url2path(self.get_relative_url()))
        if self.isdir():
            path = op.join(path, 'index.html')
        return path

    def collect(self):
        # some parameters are determined at render time
        self.template.render()

    def _get_url(self, absolute=False):
        if absolute:
            base = self.site.settings.url
        else:
            base = get_base_path(self.site.settings.url)
        return safe_url_join(base, self.get_relative_url())


    def get_url(self):
        return self._get_url(absolute=False)

    def get_absolute_url(self):
        return self._get_url(absolute=True)

    def render(self):
        logger.info('Rendering %s' % self.get_absolute_url())
        # workaround for a dumb bug
        # no ideas why but all tag templates contain same self inside
        self.template.globals['entry'] = self
        path = self.get_dest()
        makedirs(op.dirname(path))
        file(path, 'w').write(self.template.render().encode('utf-8'))
