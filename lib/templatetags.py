from ConfigParser import ConfigParser
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jinja2 import nodes
from jinja2.ext import Extension

defaults = {
    'layout': '_base.html',
    'author': 'Alexander Solovyov',
    }

class MetaInfoExtension(Extension):
    tags = set(['meta'])

    def __init__(self, environment):
        super(MetaInfoExtension, self).__init__(environment)

    def parse(self, parser):
        parser.parse_expression()
        meta = parser.parse_statements(['name:endmeta'], drop_needle=True)
        # ConfigParser wants to have section header
        meta = u'[general]\n' + meta[0].nodes[0].data.strip()
        # ConfigParser thinks he's reading file and tries to decode
        meta = StringIO(meta.encode('utf-8'))
        config = ConfigParser()
        config.readfp(meta)

        settings = defaults.copy()
        settings.update(dict(config.items('general')))

        output = []
        for key, value in settings.items():
            output.append(nodes.Assign(nodes.Name(key, 'store'), nodes.Const(value)))
        # extend template
        output.append(nodes.Extends(nodes.Const(settings['layout'])))
        return output


# nice name
metainfo = MetaInfoExtension
