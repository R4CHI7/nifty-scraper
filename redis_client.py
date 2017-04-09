import redis

from config.config import Config


def GetRedisClient():
    """
    Creates a new redis connection and returns the client.
    """
    config = Config().getConfig()
    r = redis.StrictRedis(
        host=config.get('redis', 'host'),
        port=config.get('redis', 'port'),
        password=config.get('redis', 'pass')
    )
    return r
