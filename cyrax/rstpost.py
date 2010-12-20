from docutils import nodes, core
from docutils.writers import html4css1
from docutils.parsers.rst import directives, Directive

from cyrax import models
import cyrax.template.rstextensions


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
        print self.content
        return [nodes.docinfo(self.content)]

directives.register_directive('meta', CyraxMeta)


class RstPost(models.Post):
    @staticmethod
    def check(site, path):
        return models.Post.check(site, path) and path.endswith('.rst')

    def init(self):
        # dumb hack
        self.settings.date = self.date
        self.site.posts.append(self)
        self.site.posts.sort(cmp=models.postcmp, reverse=True)
        self.site.latest_post = self.site.posts[0]

    def get_template(self):
        source = file(self.path).read()
        parts = core.publish_parts(source, writer=CyraxWriter())
        self.settings.read(parts['cyraxmeta'])
        return self.site.env.get_template(
            '_rstpost.html', globals={'entry': self, 'parts': parts})

    def __repr__(self):
        return '"%s"' % self.path


models.TYPE_LIST.insert(0, RstPost)
