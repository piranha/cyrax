try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from jinja2 import nodes
from jinja2.ext import Extension


class MetaInfoExtension(Extension):
    tags = set(['meta'])

    def __init__(self, environment):
        super(MetaInfoExtension, self).__init__(environment)

    def parse(self, parser):
        token = parser.stream.next()

        meta = parser.parse_statements(['name:endmeta'], drop_needle=True)
        config = meta[0].nodes[0].data

        args = [nodes.Name('entry', 'load'), nodes.Const(config)]

        # Quick fix, till Jinja2 get's fixed
        # Should be:
        #output = [self.call_method('_update_entry', args=args),
        output = [nodes.CallBlock(self.call_method('_update_entry', args=args), [], [], ''),
                  nodes.Extends(nodes.Const('_base.html')),]
        return output

    def _update_entry(self, entry, config, caller):
        entry.settings.read(config)

        # TODO: Remove me after Jinja2 will be fixed
        return ''
