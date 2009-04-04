import sys, logging
import os.path as op

logger = logging.getLogger('server')


def start_server(address, port, path):
    try:
        import cherrypy
        from cherrypy.lib.static import serve_file
    except ImportError:
        logger.fatal('CherryPy is required to run webserver')
        sys.exit(1)

    class Root:
        @cherrypy.expose
        def default(self, *args):
            fn = op.join(path, *args)
            if op.exists(fn):
                if op.isdir(fn):
                    return serve_file(op.join(fn, 'index.html'))
                return serve_file(fn)
            raise cherrypy.NotFound

    cherrypy.config.update({'server.socket_host': address,
                            'server.socket_port': port,
                            'log.screen': True})
    conf = {'/static': {
            'tools.staticdir.dir': op.join(path, 'static'),
            'tools.staticdir.on': True,
            }}
    cherrypy.quickstart(Root(), '/', conf)
