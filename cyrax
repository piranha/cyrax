#!/usr/bin/env python

import os, sys, logging
import os.path as op
from optparse import OptionParser

sys.path.insert(0, op.join(op.dirname(op.abspath(__file__)), '..'))

import cyrax
from cyrax.lib.core import Site
from cyrax.lib.server import start_server


def main():
    usage = '%s [options]' % sys.argv[0]
    parser = OptionParser(usage)

    parser.add_option('', '--log', default='-',
                      help='redirect log to this file (default: stdout)')
    parser.add_option('-q', '--quiet', default=False, action='store_true',
                      help='do not output information messages')

    parser.add_option('-w', '--webserve', default=False, action='store_true',
                      help='start server instead of site generation')
    parser.add_option('-a', '--address', default='0.0.0.0',
                      help='address to listen on (default: all interfaces)')
    parser.add_option('-p', '--port', default=8000,
                      help='port to listen on (default: 8000)')

    parser.add_option('-s', '--source', default='content',
                      help='directory with a source (default: content)')
    parser.add_option('-d', '--dest', default='deploy',
                      help='destination directory (default: deploy)')

    opts, args = parser.parse_args()

    if len(args):
        parser.print_help()
        sys.exit()

    level = opts.quiet and logging.ERROR or logging.INFO
    if opts.log == '-':
        logging.basicConfig(stream=sys.stdout, level=level)
    else:
        logging.basicConfig(filename=opts.log, level=level)

    if opts.webserve:
        start_server(opts.address, opts.port, op.abspath(opts.dest))
    else:
        site = Site(op.abspath(opts.source), op.abspath(opts.dest))
        site.render()

if __name__ == '__main__':
    main()
