import sys, logging
import os.path as op
from optparse import OptionParser

__version__ = '2.7'
logger = logging.getLogger('cyrax')

def main():
    from cyrax.core import Site
    from cyrax.server import start_server

    usage = '%s [options] [source]' % sys.argv[0]
    parser = OptionParser(usage)

    parser.add_option('', '--log', default='-',
                      help='redirect log to this file (default: stdout)')
    parser.add_option('-q', '--quiet', default=False, action='store_true',
                      help='do not output information messages')
    parser.add_option('-v', '--verbose', default=False, action='store_true',
                      help='output more logs')

    parser.add_option('-w', '--webserve', default=False, action='store_true',
                      help='start local web server')
    parser.add_option('-a', '--address', default='127.0.0.1',
                      help='address to listen on (default: all interfaces)')
    parser.add_option('-p', '--port', default=8000, type='int',
                      help='port to listen on (default: 8000)')

    parser.add_option('-d', '--dest', default='',
        help='destination directory (default: _build in source dir)')
    parser.add_option('', '--version', default=False, action='store_true',
                      help='show cyrax version')

    opts, args = parser.parse_args()

    if opts.version:
        print 'Cyrax', __version__
        sys.exit(0)

    if opts.verbose:
        level = logging.DEBUG
    elif opts.quiet:
        level = logging.ERROR
    else:
        level = logging.INFO

    if opts.log == '-':
        logging.basicConfig(stream=sys.stdout, level=level)
    else:
        logging.basicConfig(filename=opts.log, level=level)

    source = op.abspath(args and args[0] or '.')
    if not op.exists(op.join(source, 'settings.cfg')):
        logger.error("Can't find settings.cfg in the current folder")
        sys.exit(1)

    dest = opts.dest or op.join(source, '_build')

    if opts.webserve:
        start_server(opts.address, opts.port, source, dest)
    else:
        site = Site(source, dest)
        site.render()
