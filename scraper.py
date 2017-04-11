import threading
import time
import requests
import json
import datetime
from pytz import timezone

import cherrypy

from config.config import Config
from utils.redis_client import GetRedisClient


class Scraper(object):
    """
    Scraper class scrapes the NSE URL for NIFTY values after `interval` number of seconds.
    """
    def __init__(self, interval=1):
        self.interval = interval
        self.url = 'https://www.nseindia.com/homepage/Indices1.json'

    def start(self):
        """
        start method starts the backgroud thread.
        """
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        """
        run method is the actual implementation of the scraper. The values are fetched and stored
        in a redis list.
        """
        config = Config().getConfig()
        r = GetRedisClient(config)
        while True:
            try:
                # Check if the market is open. This is done to avoid repeated pulling of the same
                # data once the market has closed.
                if self.isMarketOpen():
                    page = requests.get(self.url)
                    response = json.loads(page.content)
                    for data in response['data']:
                        if data['name'] == 'NIFTY 50':
                            redisData = {
                                'lastPrice': data['lastPrice'],
                                'change': float(data['change']),
                                'pChange': float(data['pChange']),
                                'timestamp': int(time.time())
                            }
                            # Store the json as a string in redis.
                            jsonData = json.dumps(redisData)
                            r.lpush(config.get('app', 'redis_key'), jsonData)
            except Exception as e:
                cherrypy.log("Error occurred while pulling data from NSE", traceback=True)
                pass
            finally:
                # Sleep for the interval.
                time.sleep(self.interval)

    def isMarketOpen(self):
        """
        isMarketOpen method checks if the stock market is open according to Indian Standard Time.
        """
        ist = timezone('Asia/Kolkata')
        istTime = datetime.datetime.now(ist).time()
        openTime = datetime.time(9, 15, 0)
        closeTime = datetime.time(15, 30, 0)
        return (istTime >= openTime and istTime <= closeTime)
