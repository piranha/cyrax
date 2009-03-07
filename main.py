#!/usr/bin/env python

import os, sys

from generator import generator

def main(argv):
    generator(os.path.abspath('content'), os.path.abspath('deploy'))

if __name__ == '__main__':
    main(sys.argv[1:])
