import redis


def GetRedisClient(config):
    """
    Creates a new redis connection and returns the client.
    """
    r = redis.StrictRedis(
        host=config.get('redis', 'host'),
        port=config.get('redis', 'port'),
        password=config.get('redis', 'pass')
    )
    return r
