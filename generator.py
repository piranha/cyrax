import os.path as op
import os, shutil

from cyrax.lib.models import Site

def generator(source, destination):
    '''
    Find all content files and render them into deploy location.
    '''
    if op.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    site = Site(source, destination)
    site.render()
