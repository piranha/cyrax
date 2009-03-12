from ConfigParser import ConfigParser
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jinja2 import nodes
from jinja2.ext import Extension

from cyrax.lib.conf import parse_config

defaults = {
    'layout': '_base.html',
    'author': 'Alexander Solovyov',
    }

class MetaInfoExtension(Extension):
    tags = set(['meta'])

    def __init__(self, environment):
        super(MetaInfoExtension, self).__init__(environment)

    def parse(self, parser):
        token = parser.stream.next()
        #parser.parse_expression()

        meta = parser.parse_statements(['name:endmeta'], drop_needle=True)
        config = parse_config(meta[0].nodes[0].data)
        settings = defaults.copy()
        settings.update(config)

        output = []
        for key, value in settings.items():
            output.append(nodes.Assign(nodes.Name(key, 'store'), nodes.Const(value)))
        # extend template
        output.append(nodes.Extends(nodes.Const(settings['layout'])))
        return output
