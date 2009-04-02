#!/usr/bin/env python

import os, sys, logging
import os.path as op
from optparse import OptionParser

sys.path.insert(0, op.join(op.dirname(op.abspath(__file__)), '..'))

from cyrax.generator import generator
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
        start_server(opts.address, opts.port, os.path.abspath('deploy'))
    else:
        generator(os.path.abspath('content'), os.path.abspath('deploy'))

if __name__ == '__main__':
    main()
