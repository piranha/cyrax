import yaml
from jinja2 import nodes
from jinja2.ext import Extension

defaults = {
    'layout': '_base.html',
    'author': 'Alexander Solovyov',
    }

class PageInfoExtension(Extension):
    tags = set(['meta'])

    def __init__(self, environment):
        super(PageInfoExtension, self).__init__(environment)

    def parse(self, parser):
        parser.parse_expression()
        conf = defaults.copy()
        meta = parser.parse_statements(['name:endmeta'], drop_needle=True)
        conf.update(yaml.load(meta[0].nodes[0].data))
        output = []
        for key, value in conf.items():
            output.append(nodes.Assign(nodes.Name(key, 'store'), nodes.Const(value)))
        # extend template
        output.append(nodes.Extends(nodes.Const(conf['layout'])))
        return output


# nice name
pageinfo = PageInfoExtension
