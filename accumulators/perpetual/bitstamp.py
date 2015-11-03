import schedule
import argparse
import urllib
import json
from influxdb import InfluxDBClient

def init(config):
    global context
    context = config
    
    schedule.every().hour.do(job)

def job():
    url = 'https://www.bitstamp.net/api/ticker_hour/'

    client = InfluxDBClient(context.host, context.port, context.user, context.password, context.dbname)

    response = urllib.urlopen(url)
    
    #{"high": "245.94", "last": "244.54", "timestamp": "1444226646", "bid": "244.55", "vwap": "245.07", "volume": "6708.63463811", "low": "243.69", "ask": "245.36"}
    json_raw = json.loads(response.read())

    json_body = [
        {
            "measurement": "priceticker",
            "tags": {
                "host": "bitstamp",
                "resolution": "hourly"
            }
        }
    ]

    json_body[0]['time'] = int(json_raw['timestamp'] + '000000000')
    del(json_raw['timestamp'])
    json_body[0]['fields'] = dict([(k, float(v)) for (k, v) in json_raw.iteritems()])
    
    print("Switch user: " + context.dbuser)
    client.switch_user(context.dbuser, context.dbuser_password)

    print("Write points: {0}".format(json_body))
    client.write_points(json_body)
