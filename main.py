#!/usr/bin/env python

import os, sys, logging
import os.path as op

logging.basicConfig()

sys.path.insert(0, op.join(op.dirname(op.abspath(__file__)), '..'))

from cyrax.generator import generator

def main(argv):
    generator(os.path.abspath('content'), os.path.abspath('deploy'))

if __name__ == '__main__':
    main(sys.argv[1:])
