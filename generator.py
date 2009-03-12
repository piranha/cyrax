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

    # env = initialize_env(source)


    # for path, dirs, files in os.walk(source):
    #     relative = path[len(source):]
    #     try:
    #         os.mkdir(op.join(destination, relative))
    #     except OSError:
    #         pass
    #     for f in files:
    #         if not f.startswith('_'):
    #             tmpl = env.get_template(op.join(relative, f))
    #             file(op.join(destination, relative, f), 'w').write(tmpl.render())
