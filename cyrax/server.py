import os
import posixpath
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import urllib
import logging

from cyrax import autoreload, core

logger = logging.getLogger(__name__)


class CyraxHTTPRequestHandler(SimpleHTTPRequestHandler):

    def translate_path(self, path):
        """
        The default behavior of SimpleHTTPRequestHandler.translate_path
        is to serve files from the current directory and all of the
        directories below it. This class overrides the method and
        looks for a `rootpath` attribute, which will be used instead
        of the current directory.
        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        try:
            path = self.rootpath
        except AttributeError:
            path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path


def run_server(address, port, source, dest):
    core.Site(source, dest).render()
    CyraxHTTPRequestHandler.rootpath = dest
    httpd = HTTPServer((address, port), CyraxHTTPRequestHandler)
    logger.info("Serving at http://%s:%s", address, port)
    httpd.serve_forever()


def start_server(address, port, source, dest):
    autoreload.main(run_server, (), {
        'address': address,
        'port': port,
        'source': source,
        'dest': dest,
    })
