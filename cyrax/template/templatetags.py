from jinja2 import nodes
from jinja2.ext import Extension


class MetaInfoExtension(Extension):
    tags = set(['meta'])

    def parse(self, parser):
        token = parser.stream.next()
        lineno = token.lineno

        meta = parser.parse_statements(['name:endmeta'], drop_needle=True)
        try:
            config = meta[0].nodes[0].data
        except IndexError:
            config = '' # there was no data

        args = [nodes.Name('entry', 'load'), nodes.Const(config)]

        output = [
            nodes.CallBlock(self.call_method('_update_entry', args=args),
                            [], [], '').set_lineno(lineno),
            nodes.Extends(self.call_method('_determine_parent', args=args[:1]))
            ]
        return output

    def _update_entry(self, entry, config, caller):
        entry.settings.read(config)
        return ''

    def _determine_parent(self, entry):
        return entry.settings.parent_tmpl


class MarkExtension(Extension):
    tags = set(['mark'])

    def parse(self, parser):
        token = parser.stream.next()
        lineno = token.lineno

        name = parser.stream.next().value
        args = [nodes.Name('entry', 'load'), nodes.Const(name)]
        body = parser.parse_statements(['name:endmark'], drop_needle=True)

        return nodes.CallBlock(self.call_method('_set_attr', args=args),
                               [], [], body).set_lineno(lineno)

    def _set_attr(self, entry, name, caller):
        if entry:
            setattr(entry, name, caller())
        return ''
