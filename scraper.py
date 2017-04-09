import threading
import time
import requests
import json

import cherrypy

from redis_client import GetRedisClient


class Scraper(object):
    def __init__(self, interval=1):
        self.interval = interval
        self.url = 'https://www.nseindia.com/homepage/Indices1.json'
        self.redisKey = 'nifty50data'

    def start(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        r = GetRedisClient()
        while True:
            try:
                page = requests.get(self.url)
                response = json.loads(page.content)
                for data in response['data']:
                    if data['name'] == 'NIFTY 50':
                        redisData = {
                            'lastPrice': data['lastPrice'],
                            'change': data['change'],
                            'pChange': data['pChange'],
                            'timestamp': int(time.time())
                        }
                        jsonData = json.dumps(redisData)
                        r.lpush(self.redisKey, jsonData)
            except Exception as e:
                cherrypy.log("Error occurred while pulling data from NSE", traceback=True)
                pass
            finally:
                time.sleep(self.interval)
