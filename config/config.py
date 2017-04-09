import ConfigParser


class Config(object):
    def __init__(self):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read('server.conf')

    def getConfig(self):
        return self.conf
