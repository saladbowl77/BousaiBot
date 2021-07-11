import requests
import json

import makeMap

from datetime import datetime

from os.path import dirname

def getEarthquakeData():
    baseURLDir = dirname(__file__)

    # 地震API アクセス常時
    urlP2p = "https://api.p2pquake.net/v2/jma/quake"
    responseP2p = requests.get(urlP2p)
    jsonDataP2p = responseP2p.json()

    if 'issue' in jsonDataP2p[0] and 'time' in jsonDataP2p[0]["issue"]:
        lastEarthquakeDatetime = jsonDataP2p[0]["issue"]["time"]
        lastEarthquakeDatetime = datetime.strptime(lastEarthquakeDatetime, '%Y/%m/%d %H:%M:%S')

        with open(baseURLDir + "/tmp/lastDatetimeP2P.txt") as f:
            lastDatetimeP2P = f.read()

        print(lastDatetimeP2P)

        lastDatetimeP2P = datetime.strptime(lastDatetimeP2P, '%Y-%m-%d %H:%M:%S')
        if lastEarthquakeDatetime > lastDatetimeP2P:
            print("ok")
            with open(baseURLDir + "/tmp/lastDatetimeJMA.txt") as f:
                lastDatetimeJMA = f.read()

            lastDatetimeJMA = datetime.strptime(lastDatetimeJMA, '%Y-%m-%d %H:%M:%S')

            urlJMAList = "https://www.jma.go.jp/bosai/quake/data/list.json"
            responseJMAList = requests.get(urlJMAList)
            jsonDataJMAList = responseJMAList.json()

            jsonDataJMALastDatetime = jsonDataJMAList[0]["rdt"]
            jsonDataJMALastDatetime = datetime.strptime(jsonDataJMALastDatetime, '%Y-%m-%dT%H:%M:%S+09:00')

            if jsonDataJMALastDatetime > lastDatetimeJMA:
                urlJMAEarthquakeData = "https://www.jma.go.jp/bosai/quake/data/" + jsonDataJMAList[0]["json"]
                responseJMAEarthquakeData = requests.get(urlJMAEarthquakeData)
                jsonDataJMAEarthquakeData = responseJMAEarthquakeData.json()

                with open('tmp/json/' + jsonDataJMAList[0]["eid"] + '.json', 'w') as f:
                    json.dump(jsonDataJMAEarthquakeData, f, indent=4)

                returnList = makeMap.mkMap(jsonDataJMAList[0]["eid"])
                print(returnList)

                with open(baseURLDir + "/tmp/lastDatetimeP2P.txt", mode='w') as f:
                    f.write(str(lastEarthquakeDatetime))
                with open(baseURLDir + "/tmp/lastDatetimeJMA.txt", mode='w') as f:
                    f.write(str(jsonDataJMALastDatetime))
                
                import webhookSend
                webhookSend.sendMessage(jsonDataJMAList[0]["eid"])

                return jsonDataJMAList[0]["eid"], returnList


if __name__ == '__main__':#直接yobareru.pyを実行した時だけ、def test()を実行する
    getEarthquakeData()