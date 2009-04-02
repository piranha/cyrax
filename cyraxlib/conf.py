from ConfigParser import ConfigParser
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


def parse_config(inp):
    # ConfigParser doesn't like indent
    inp = '\n'.join(line.strip() for line in inp.strip().splitlines())
    # ...and tries to decode his input
    if isinstance(inp, unicode):
        inp = inp.encode('utf-8')
    config = ConfigParser()
    # ...and wants to have section header
    config.readfp(StringIO('[general]\n' + inp))
    return dict(config.items('general'))


class Settings(dict):
    def __init__(self, parent=None, **kwargs):
        self.parent = parent
        super(Settings, self).__init__(**kwargs)

    def read(self, inp):
        self.update(parse_config(inp))
        return self

    def __getitem__(self, name):
        try:
            return super(Settings, self).__getitem__(name)
        except KeyError:
            if self.parent:
                return self.parent[name]
            raise

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

