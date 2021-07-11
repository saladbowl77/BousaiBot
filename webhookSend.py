import requests

import json
import csv

from os.path import dirname


def sendMessage(jsonId):
    baseURLDir = dirname(__file__)

    json_open = open(baseURLDir + '/tmp/json/' + jsonId + '.json', 'r')
    json_load = json.load(json_open)

    with open(baseURLDir + '/data/webhookURL.csv') as f:
        reader = csv.reader(f)
        webhookUrlList = [row for row in reader]

    baseURLDir = dirname(__file__)

    with open(baseURLDir + '/data/webhookURL.csv') as f:
        reader = csv.reader(f)
        webhookUrlList = [row for row in reader]

    WEBHOOK_URL = "https://discord.com/api/webhooks/863427389962321920/hEXW6SnCkizEoLTni-D3Jwl8xg_dSHHkS_pTgeMvub_U-peGsCmMVzhjZ2aL71aWqCAW?wait=true"

    payload = {
            "payload_json" : {
                "username": "Webhook",
                "embeds": [
                    {
                    "image": {
                        "url": "attachment:img/old/20210710052352/all.png"
                    },
                    "author": {
                        "name": "地震情報 byBotName",
                    },
                    "title": "地震情報",
                    "url": "https://www.jma.go.jp/bosai/map.html?contents=earthquake_map",
                    "description": json_load["Head"]["Headline"]["Text"] + " [気象庁 地震MAP](https://www.jma.go.jp/bosai/map.html?contents=earthquake_map)",
                    "color": 15258703,
                    "image": {
                        "url" : "attachment://all.png"
                    },
                    "fields": [
                        {
                            "name": "震源地",
                            "value": json_load["Body"]["Earthquake"]["Hypocenter"]["Area"]["Name"]
                        },
                        {
                            "name": "マグニチュード",
                            "value": "M " + json_load["Body"]["Earthquake"]["Magnitude"],
                            "inline": True 
                        },
                        {
                            "name": "最大震度",
                            "value": json_load["Body"]["Intensity"]["Observation"]["MaxInt"],
                            "inline": True
                        },
                        {
                            "name": "地震ID",
                            "value": jsonId,
                            "inline": True
                        }
                    ],
                    "footer": {
                        "text": "made by saladbowl",
                        "icon_url": "https://pbs.twimg.com/profile_images/1284044313312329728/TAJzweRl_400x400.jpg"
                    }
                    }
                ]
            }
        }

    ### embed付き
    with open(baseURLDir + '/img/old/' + jsonId + "/all.png", 'rb') as f:
        all = f.read()
    files_qiita  = {
        "earthquakeMap" : ( "all.png", all ),
    }

    for webhookUrl in webhookUrlList:
        WEBHOOK_URL = webhookUrl[0]
        payload['payload_json'] = json.dumps( payload['payload_json'], ensure_ascii=False )
        res = requests.post(WEBHOOK_URL, data = payload, files = files_qiita )
        print( res.status_code )
        print( json.dumps( json.loads(res.content), indent=4, ensure_ascii=False ) )