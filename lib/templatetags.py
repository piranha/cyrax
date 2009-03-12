from ConfigParser import ConfigParser
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jinja2 import nodes
from jinja2.ext import Extension

from cyrax.lib.conf import parse_config

class MetaInfoExtension(Extension):
    tags = set(['meta'])

    def __init__(self, environment):
        super(MetaInfoExtension, self).__init__(environment)

    def parse(self, parser):
        token = parser.stream.next()

        meta = parser.parse_statements(['name:endmeta'], drop_needle=True)
        config = meta[0].nodes[0].data

        args = [nodes.Name('entry', 'load'), nodes.Const(config)]
        output = [self.call_method('_update_entry', args=args),
                  nodes.Extends(nodes.Const('_base.html')),]
        return output

    def _update_entry(self, entry, config):
        entry.settings.read(config)
