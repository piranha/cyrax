import re
import time
import datetime
import posixpath
import os.path as op
import logging

from cyrax.conf import Settings
from cyrax.events import events
from cyrax.utils import (safe_url_join, url2path, path2url,
                         base_path, makedirs)


logger = logging.getLogger(__name__)
DATE_RE = re.compile(r'(.*?)(\d+)[/-](\d+)[/-](\d+)[/-](.*)$')


def postcmp(x, y):
    xd = x.settings.get('updated', x.settings.date)
    yd = y.settings.get('updated', y.settings.date)
    return -1 if xd < yd else 1 if xd > yd else 0


class Entry(object):
    def __init__(self, site, path, source=None):
        '''Initialize an entry

        This involves change of base class by running static method Class.check
        of every member of models.TYPE_LIST.

        Arguments:

         - `site`: site this entry belongs to
         - `path`: relative path to source template and to result
         - `source`: optional source template path. Can be used to trick
            system to have virtual entries (with no real equivalent in
            source directory)
        '''
        self.site = site
        self.path = path
        self.source = source
        self.mtime = self.get_mtime()

        self.settings = Settings(parent=self.site.settings)

        base = '_%s.html' % self.__class__.__name__.lower()
        if op.exists(op.join(self.site.root, base)):
            self.settings.parent_tmpl = base

        self.template = self.get_template()
        self.settings.base, self.settings.slug = op.split(self.path)
        self.collect()
        if hasattr(self, 'init'):
            self.init()

    def __repr__(self):
        return '<%s: %r>' % (self.__class__.__name__, self.path)

    def __getitem__(self, name):
        return self.settings[name]

    def __getattr__(self, name):
        try:
            return self.settings[name]
        except KeyError:
            raise AttributeError(name)

    def get_mtime(self):
        '''Determine modification time (with date)

        As in modification time vs creation time.

        If source is not null and path does not exist, then entry is virtual and
        returns current datetime.
        '''
        path = op.join(self.site.root, self.path)
        if self.source and not op.exists(path):
            return datetime.datetime.now()
        mtime = op.getmtime(path)
        return datetime.datetime(*time.gmtime(mtime)[:6])

    def get_template(self):
        '''Get Jinja2 template of entry to render
        '''
        return self.site.env.get_template(self.source or self.path,
                                          globals={'entry': self})

    def collect(self):
        '''Collect settings information from entry

        Renders Jinja2 template to get this information from {% meta %}
        '''
        self.template.render()

    def isdir(self):
        '''Determines if entry should be rendered as directory
        '''
        return self.settings.get('isdir', True)

    def get_dest(self):
        path = op.join(self.site.dest, url2path(self.get_relative_url()))
        if self.isdir():
            path = op.join(path, 'index.html')
        return path

    def get_relative_url(self):
        return self.path

    def get_url(self):
        return safe_url_join(base_path(self.site.url), self.get_relative_url())

    def get_absolute_url(self):
        return safe_url_join(self.site.url, self.get_relative_url())

    def render(self):
        logger.info('Rendering %r' % self)
        # workaround for a dumb bug
        # no ideas why but all tag templates contain same self inside
        self.template.globals['entry'] = self
        path = self.get_dest()
        makedirs(op.dirname(path))
        file(path, 'w').write(self.template.render().encode('utf-8'))


class NonHTML(Entry):
    @staticmethod
    def check(site, path):
        return not path.endswith('.html')

    def isdir(self):
        return self.settings.get('isdir', False)


class Post(Entry):
    @staticmethod
    def check(site, path):
        return bool(DATE_RE.search(path))

    def __init__(self, site, path, source=None):
        base, Y, M, D, slug = DATE_RE.search(path).groups()
        self.date = datetime.datetime(int(Y), int(M), int(D))
        super(Post, self).__init__(site, path, source)
        self.settings.base = base
        self.settings.slug = op.splitext(slug)[0]

    def init(self):
        # dumb hack
        self.settings.date = self.date
        self.site.posts.append(self)
        self.site.posts.sort(cmp=postcmp, reverse=True)
        self.site.latest_post = self.site.posts[0]

        self._process_tags()

    def _process_tags(self):
        for tag in self.settings.get('tags', []):
            tagentries = self.site.tags.setdefault(tag, [])
            if self not in tagentries:
                tagentries.append(self)
                self.site.tags[tag].sort(cmp=postcmp, reverse=True)

    def __str__(self):
        return self.slug

    def get_relative_url(self):
        date = self.date.strftime('%Y/%m/%d')
        return posixpath.join(self.base, date, self.slug) + '/'

    @staticmethod
    def register(site):
        site.posts = []

events.connect('traverse-started', Post.register)


class Page(Entry):
    @staticmethod
    def check(site, path):
        return path.endswith('.html')

    def init(self):
        if self.isdir():
            if self.path.endswith('index.html'):
                path = self.path[:-len('index.html')]
            else:
                path = op.splitext(self.path)[0]
        else:
            path = self.path
        base, slug = op.split(path)
        self.settings.base = base
        self.settings.slug = slug

        self.site.pages.append(self)

    def __str__(self):
        return self.slug

    def get_relative_url(self):
        url = posixpath.join(self.base, self.slug)
        if self.isdir() and url and not url.endswith('/'):
            url += '/'
        return url

    @staticmethod
    def register(site):
        site.pages = []

events.connect('traverse-started', Page.register)


class Tag(Entry):

    prefix = 'tag' + op.sep

    @classmethod
    def check(cls, site, path):
        res = path.startswith(cls.prefix)
        return res

    def init(self):
        self.slug = self.path[len(self.prefix):-len('.html')]
        self.site.tag_cache[self.slug] = self

    def __str__(self):
        return self.slug

    def get_relative_url(self):
        if self.path.endswith('.html'):
            url = path2url(self.path[:-len('.html')])
        else:
            url = path2url(self.path)
        if self.isdir():
            url += '/'
        return url

    @staticmethod
    def register(site):
        site.tags = {}

    @classmethod
    def process(cls, site):
        site.tag_cache = {}
        for tag in site.tags:
            path = '%s%s.html' % (cls.prefix, tag)
            site.entries.append(cls(site, path, '_taglist.html'))

events.connect('traverse-started', Tag.register)
events.connect('site-traversed', Tag.process)


TYPE_LIST = [Post, Tag, Page, NonHTML]
