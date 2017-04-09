import cherrypy

from scraper import Scraper
from server import Server


class App(object):
    """
    App class encapsulates the background scraper and the web server for frontend.
    """
    def __init__(self):
        self.scraper = Scraper(interval=5*60)

    def start(self):
        # Start the background scraper.
        cherrypy.log('Starting background scraper..')
        self.scraper.start()

        # Start the server.
        cherrypy.quickstart(App(), '/')


if __name__ == '__main__':
    app = App()
    app.start()
