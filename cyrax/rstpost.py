from os import path as op

from docutils import nodes, core
from docutils.writers import html4css1
from docutils.parsers.rst import directives, Directive

from cyrax import models
from cyrax.template.rstextensions import RST_SETTINGS


class CyraxWriter(html4css1.Writer):
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = CyraxTranslator
        self.visitor_attributes += ('cyraxmeta',)


class CyraxTranslator(html4css1.HTMLTranslator):
    def visit_cyraxmeta(self, node):
        self.cyraxmeta = '\n'.join(node.rawsource)

    def depart_cyraxmeta(self, node):
        pass


class CyraxMeta(Directive):
    '''Cyrax config catcher for reStructuredText

    Usage::

      .. meta::

        various: configuration
    '''
    class cyraxmeta(nodes.Special, nodes.PreBibliographic, nodes.Element):
        pass

    has_content = True

    def run(self):
        self.assert_has_content()
        return [self.cyraxmeta(self.content)]

        node = nodes.Element()
        node += nodes.raw(self.content)
        return [nodes.docinfo(self.content)]

directives.register_directive('meta', CyraxMeta)


class RstPost(models.Post):

    def __init__(self, *args, **kwargs):
        if not 'source' in kwargs:
            kwargs['source'] = '_post.html'
        super(RstPost, self).__init__(*args, **kwargs)

    @staticmethod
    def check(site, path):
        return models.Post.check(site, path) and path.endswith('.rst')

    def init(self):
        # dumb hack
        self.settings.date = self.date
        self.site.posts.append(self)
        self.site.posts.sort(cmp=models.postcmp, reverse=True)
        self.site.latest_post = self.site.posts[0]

        self._process_tags()

    def collect(self):
        # TODO: need the general solution for Jinja2 and rst to load sources 
        # with path prefixes
        
        source = file(op.join(self.site.env.loader.searchpath[0],
            self.path)).read()
        parts = core.publish_parts(source, writer=CyraxWriter(),
                                   settings_overrides=RST_SETTINGS)
        self.settings.read(parts['cyraxmeta'])
        self.settings.title = parts['title']
        self.settings.body = parts['body']


models.TYPE_LIST.insert(0, RstPost)
