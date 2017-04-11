import json
import cherrypy
from jinja2 import Environment, PackageLoader

from utils.redis_client import GetRedisClient
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
            # Convert the JSON strings to objects.
            data = map(json.loads, data)
            for entry in data:
                # arrowClass and color are used for the frontend.
                arrowClass = ''
                color = ''
                if entry['change'] > 0.0:
                    arrowClass = 'fa-arrow-circle-up'
                    color = 'green'
                elif entry['change'] < 0.0:
                    arrowClass = 'fa-arrow-circle-down'
                    color = 'red'
                entry['arrowClass'] = arrowClass
                entry['color'] = color

            # Get the template and render using the data.
            template = env.get_template('index.html')
            return template.render(data=data)
        except Exception as e:
            cherrypy.log('Error occurred while handling request', traceback=True)
            template = env.get_template('500.html')
            return template.render()
