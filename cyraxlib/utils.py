
import urlparse
import os.path as op
import posixpath


def new_base(obj, base):
    name = base.__name__ + obj.__class__.__name__
    return type(name, (base, ), dict(obj.__class__.__dict__))


def safe_url_join(base, path):
    """
    >>> safe_url_join('blog/x', 'foo/bar')
    'blog/x/foo/bar'
    >>> safe_url_join('/blog/x/', 'foo/bar')
    '/blog/x/foo/bar'
    >>> safe_url_join('http://blog/x', 'foo/bar')
    'http://blog/x/foo/bar'
    """
    scheme, netloc, basepath, params, query, fragment = urlparse.urlparse(base)
    newpath = posixpath.join(basepath, path)
    parts = (scheme, netloc, newpath, params, query, fragment)
    return urlparse.urlunparse(parts)


def get_base_path(url):
    """
    >>> get_base_path('http://google.com')
    '/'
    >>> get_base_path('http://piranha.org.ua/blog')
    '/blog'
    """
    basepath = urlparse.urlparse(url)[2]
    return basepath or '/'


def url2path(url):
    return op.sep.join(url.split('/'))


def path2url(path):
    return '/'.join(path.split(op.sep))
