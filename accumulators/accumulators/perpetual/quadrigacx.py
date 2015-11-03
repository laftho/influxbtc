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
    url = 'https://api.quadrigacx.com/v2/ticker?book=btc_cad'

    client = InfluxDBClient(context.host, context.port, context.user, context.password, context.dbname)

    response = urllib.urlopen(url)
    
	#{"high": "548.00", "last": "546.37", "timestamp": "1446576438", "volume":"652.39521487", "vwap":"485.48", "low":"472.00", "ask":"549.00", "bid":"547.00"}
    json_raw = json.loads(response.read())

    json_body = [
        {
            "measurement": "priceticker",
            "tags": {
                "host": "quadrigacx",
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
