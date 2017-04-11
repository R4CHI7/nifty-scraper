import ConfigParser


class Config(object):
    """
    Config class reads and parses the configuration file and makes it accessible to other parts
    of the app.
    """
    def __init__(self):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read('server.conf')

    def getConfig(self):
        return self.conf
