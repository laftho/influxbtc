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
    url = 'http://hn.algolia.com/api/v1/search_by_date?query=bitcoin'

    client = InfluxDBClient(context.host, context.port, context.user, context.password, context.dbname)

    response = urllib.urlopen(url)
    
    json_raw = json.loads(response.read())
    #print(json.dumps(json_raw, sort_keys=True, indent=4, separators=(',', ': ')))

    print("Switch user: " + context.dbuser)
    client.switch_user(context.dbuser, context.dbuser_password)
    
    #json_body[0]['time'] = int(json_raw['timestamp'] + '000000000')
    #del(json_raw['timestamp'])
    #print(json.dumps(json_raw['hits'], sort_keys=True, indent=4, separators=(',', ': ')))
    #json_hits = json.loads(json_raw['hits'][0])
    #print(json_hits)
    #json_body[0]['fields'] = dict([(k, v) for (k, v) in json_hits.iteritems()])
    for each in json_raw['hits']:
        json_body = [
            {
                "measurement": "hackernews_comments_total",
                "tags": {
                    "host": "hackernews",
                    "resolution": "five_minutely",
                    "type": "all_comments",
                    "query": "bitcoin"
                }
            }
        ]
        #print each['objectID']
        #print each['author']
        #print each['url']
        json_body[0]['fields'] = dict([('id', int(each['objectID']) )])
        comment_text = ''
        if(each['comment_text']):
            comment_text = each['comment_text'].encode('utf-8')
        else:
           comment_text = each['comment_text']
        #print each['story_text']
        json_body[0]['fields'] = dict([('id', int(each['objectID'])), ('author', each['author'].encode('utf-8')), ('comment_text', comment_text)])
        json_body[0]['time'] = each['created_at']
        #print each['title']
        #print each['_tags']
        #print each['parent_id']
        #print each['_highlightResult']
        #print each['points']
        #print each['story_id']
        #print each['created_at_i']
        #print each['story_url']
        #if(each['story_title']):
        #    print each['story_title'].encode('utf-8')
        print("Write points: {0}".format(json_body))
        client.write_points(json_body)

    
    
    '''

    print("Write points: {0}".format(json_body))
    client.write_points(json_body)
    '''
