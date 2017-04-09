import cherrypy


class Server(object):
    """

    """
    @cherrypy.expose
    def index(self):
        return "<html><body>Hello</body></html>"
