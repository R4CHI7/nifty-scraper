import threading
import time
import requests
import json
import datetime
from pytz import timezone

import cherrypy

from config.config import Config
from redis_client import GetRedisClient


class Scraper(object):
    def __init__(self, interval=1):
        self.interval = interval
        self.url = 'https://www.nseindia.com/homepage/Indices1.json'

    def start(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        config = Config().getConfig()
        r = GetRedisClient(config)
        while True:
            try:
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
                            jsonData = json.dumps(redisData)
                            r.lpush(config.get('app', 'redis_key'), jsonData)
            except Exception as e:
                cherrypy.log("Error occurred while pulling data from NSE", traceback=True)
                pass
            finally:
                time.sleep(self.interval)

    def isMarketOpen():
        ist = timezone('Asia/Kolkata')
        istTime = datetime.datetime.now(ist).time()
        openTime = datetime.time(9, 15, 0)
        closeTime = datetime.time(15, 30, 0)
        return (istTime >= openTime and istTime <= closeTime)
