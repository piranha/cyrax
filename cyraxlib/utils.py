def new_base(obj, base):
    name = base.__name__ + obj.__class__.__name__
    return type(name, (base, ), dict(obj.__class__.__dict__))
