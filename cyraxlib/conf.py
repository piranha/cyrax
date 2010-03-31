'''Parser of naive data format
Copyright 2009 Alexander Solovyov, under terms of Poetic License

Format:

  key: value
  key: [list, of, values]
  key: {key: value, key: value}
  key: date: yyyy-mm-dd HH:MM:SS
  key: True  # boolean value
  key: False # boolean value

Any line without a ":" is simply skipped.
'''

from datetime import datetime

def parse(data):
    result = {}
    for line in data.splitlines():
        try:
            key, value = parse_line(line)
            result[key] = value
        except ValueError:
            pass
    return result


def parse_line(line):
    key, value = strip(line.split(':', 1))
    s, e = value.startswith, value.endswith
    if s('[') and e(']'):
        value = strip(value[1:-1].split(','))
    elif s('{') and e('}'):
        value = dict(strip(x.split(':')) for x in value[1:-1].split(','))
    elif s('date:'):
        value = datetime.strptime(value[len('date:'):].strip(),
                                  '%Y-%m-%d %H:%M:%S')
    elif value == 'True':
        value = True
    elif value == 'False':
        value = False
    return key, value


def strip(lst):
    return [x.strip() for x in lst]


class Settings(dict):
    def __init__(self, parent=None, **kwargs):
        self.parent = parent
        super(Settings, self).__init__(**kwargs)

    def read(self, inp):
        self.update(parse(inp))
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

