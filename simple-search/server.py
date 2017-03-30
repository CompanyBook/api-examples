import cherrypy
from os import getcwd, path
from service import search


class Server:
    @cherrypy.expose
    def search(self, q='', country=''):
        return search(q, country)


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': path.abspath(getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    }
    cherrypy.config.update(
        {
            'server.socket_host': '0.0.0.0'
        })
    cherrypy.quickstart(Server(), '/', conf)
