import json
import cherrypy
from jinja2 import Environment, PackageLoader

from redis_client import GetRedisClient
from config.config import Config


class Server(object):
    """
    Server class handles the requests to the web server.
    """
    @cherrypy.expose
    def index(self):
        """
        index handles requests to '/'.
        """
        env = Environment(loader=PackageLoader('server', 'templates'))
        try:
            config = Config().getConfig()
            r = GetRedisClient(config)
            data = r.lrange(config.get('app', 'redis_key'), 0, -1)
            data = map(json.loads, data)
            print data
            template = env.get_template('index.html')
            return template.render()
        except Exception as e:
            cherrypy.log('Error occurred while handling request', traceback=True)
            template = env.get_template('500.html')
            return template.render()
