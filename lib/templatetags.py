from jinja2 import nodes
from jinja2.ext import Extension


class MetaInfoExtension(Extension):
    tags = set(['meta'])

    def __init__(self, environment):
        super(MetaInfoExtension, self).__init__(environment)

    def parse(self, parser):
        token = parser.stream.next()
        lineno = token.lineno

        meta = parser.parse_statements(['name:endmeta'], drop_needle=True)
        config = meta[0].nodes[0].data

        args = [nodes.Name('entry', 'load'), nodes.Const(config)]

        # Quick fix, till Jinja2 get's fixed
        # Should be:
        #output = [self.call_method('_update_entry', args=args),

        output = [
            nodes.CallBlock(self.call_method('_update_entry', args=args),
                            [], [], '').set_lineno(lineno),
            nodes.Extends(self.call_method('_determine_parent', args=args[:1]))
            ]
        return output

    def _update_entry(self, entry, config, caller):
        entry.settings.read(config)

        # TODO: Remove me after Jinja2 will be fixed
        return ''

    def _determine_parent(self, entry):
        return entry.settings.parent_tmpl
