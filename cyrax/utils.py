import urlparse
import os
import os.path as op
import posixpath
from itertools import izip, takewhile


def makedirs(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


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


def base_path(url):
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


def removecommon(p1, p2):
    common = takewhile(lambda x: x[0] == x[1], izip(p1, p2))
    l = len(list(common))
    return p1[l:], p2[l:]


def relpath(cur, dest):
    p1, p2 = removecommon(cur.split(op.sep), dest.split(op.sep))
    # empty element because of / in the end of name
    if p1 and p1[-1] == '':
        p1 = p1[:-1]
    p = ['../'] * len(p1) + p2
    if not p:
        return ''
    return op.join(*p)
