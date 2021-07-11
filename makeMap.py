import numpy as np
import geopandas as gpd
import random
import matplotlib.colors
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

import json
import textwrap
import datetime

import glob
import os

from os.path import dirname

def mkMap(jsonFileName):
    baseURLDir = dirname(__file__)
    filename = baseURLDir + "/data/jp.geojson"
    df = gpd.read_file(filename, encoding='SHIFT-JIS')

    print(df.length)

    df['target'] = "0"

    json_open = open(baseURLDir + '/tmp/json/' + jsonFileName + '.json', 'r')
    json_load = json.load(json_open)

    earthquakeId = json_load["Head"]["EventID"]

    #print(json_load["Body"]["Intensity"]["Observation"]["Pref"])
    #print(json_load["Body"]["Intensity"]["Observation"]["Pref"][0]["Area"])
    #print(json_load["Body"]["Intensity"]["Observation"]["Pref"][0]["Area"][0]["City"])
    print(json_load["Body"]["Intensity"]["Observation"]["Pref"][0]["Area"][0]["City"][0]["Code"])
    print(json_load["Body"]["Intensity"]["Observation"]["Pref"][0]["Area"][0]["City"][0]["MaxInt"])

    jsonPrefData = json_load["Body"]["Intensity"]["Observation"]["Pref"]


    print(df["N03_007"].str[:5])

    prefListArr = []

    for index, item in enumerate(jsonPrefData):
        prefListArr.append(item["Name"])
        print(item["Name"])

        for index2, item2 in enumerate(item["Area"]):
            for index3, item3 in enumerate(item2["City"]):
                print(item3["Name"],item3["Code"],item3["MaxInt"])
                print(item3["Code"][:5])
                print(df["N03_007"].str[:5] == item3["Code"][:5])
                df.loc[df["N03_007"].str[:5] == item3["Code"][:5], 'target'] = item3["MaxInt"]

    print(df)

    # https://qiita.com/kenmatsu4/items/fe8a2f1c34c8d5676df8
    def generate_cmap(colors):
        """自分で定義したカラーマップを返す"""
        values = range(len(colors))

        vmax = np.ceil(np.max(values))
        color_list = []
        for v, c in zip(values, colors):
            color_list.append( ( v/ vmax, c) )
        return LinearSegmentedColormap.from_list('custom_cmap', color_list)


    def mkMapImg(mkPrefName, outputPrefName):
        fig = plt.figure(figsize=(8,8),dpi=100)
        ax = fig.add_subplot(111)
        legend_kwds = dict(bbox_to_anchor=(1, 0.98), loc='upper left', borderaxespad=0, fontsize=8,frameon = False)
        
        # 描画設定
        if type(mkPrefName) is str:
            mini_df = df[df["N03_001"].isin([mkPrefName])]
            maxEarthquakeInt = mini_df['target'].max()
        else:
            mini_df = df[df["N03_001"].isin(mkPrefName)]
            maxEarthquakeInt = json_load["Body"]["Intensity"]["Observation"]["MaxInt"]


        # 震度による色
        if maxEarthquakeInt == "0":
            cm = generate_cmap(['#1f1f1f'])
        elif maxEarthquakeInt == "1":
            cm = generate_cmap(['#1f1f1f', '#60d5f6'])
        elif maxEarthquakeInt == "2":
            cm = generate_cmap(['#1f1f1f', '#60d5f6', '#007bc5',])
        elif maxEarthquakeInt == "3":
            cm = generate_cmap(['#1f1f1f', '#60d5f6', '#007bc5', '#36b27e',])
        elif maxEarthquakeInt == "4":
            cm = generate_cmap(['#1f1f1f', '#60d5f6', '#007bc5', '#36b27e', '#ff8d8d',])
        elif maxEarthquakeInt == "5":
            cm = generate_cmap(['#1f1f1f', '#60d5f6', '#007bc5', '#36b27e', '#ff8d8d', '#ffeb3d',])
        elif maxEarthquakeInt == "6":
            cm = generate_cmap(['#1f1f1f', '#60d5f6', '#007bc5', '#36b27e', '#ff8d8d', '#ffeb3d', '#ff9929'])
        elif maxEarthquakeInt == "7":
            cm = generate_cmap(['#1f1f1f', '#60d5f6', '#007bc5', '#36b27e', '#ff8d8d', '#ffeb3d', '#ff9929', '#ff602d'])
        elif maxEarthquakeInt == "8":
            cm = generate_cmap(['#1f1f1f', '#60d5f6', '#007bc5', '#36b27e', '#ff8d8d', '#ffeb3d', '#ff9929', '#ff602d', '#8d3b27'])
        elif maxEarthquakeInt == "9":
            cm = generate_cmap(['#1f1f1f', '#60d5f6', '#007bc5', '#36b27e', '#ff8d8d', '#ffeb3d', '#ff9929', '#ff602d', '#8d3b27', '#b5369c'])

        ax = mini_df.plot(
            figsize=(10,10),
            column="target",
            legend=False,       # 色の概要表示非表示
            legend_kwds=legend_kwds,
            ax=ax,
            cmap=cm,        # 震度の色
            edgecolor='#444',   # 市町のの境界線の色
            linewidth = 0.7     # 市町の境界線の太さ
        )

        #背景色の設定
        fig.patch.set_facecolor('xkcd:salmon')
        fig.patch.set_facecolor('#1f1f1f')

        if type(mkPrefName) is list:
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()

            ax = df.plot(
                figsize=(10,10),
                column="target",
                legend=False,       # 色の概要表示非表示
                legend_kwds=legend_kwds,
                ax=ax,
                cmap=cm,        # 震度の色
                edgecolor='#666',   # 市町のの境界線の色
                linewidth = 0.3     # 市町の境界線の太さ
            )

            #座標表示範囲
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)

            #背景色の設定
            fig.patch.set_facecolor('xkcd:salmon')
            fig.patch.set_facecolor('#1f1f1f')
        # 座標表示するか否か→背景色がonかoffか(白になる)
        plt.axis('off')

        plt.savefig(baseURLDir + "/tmp/img/" + earthquakeId + "/" + outputPrefName+ ".png", format="png", dpi=200, bbox_inches='tight', pad_inches=0)

    prefNameToEn = {
        "北海道":"Hokkaido",
        "青森県":"Aomori",
        "岩手県":"Iwate",
        "宮城県":"Miyagi",
        "秋田県":"Akita",
        "山形県":"Yamagata",
        "福島県":"Hukusima",
        "茨城県":"Ibaraki",
        "栃木県":"Totigi",
        "群馬県":"Gunma",
        "埼玉県":"Saitama",
        "千葉県":"Tiba",
        "東京都":"Tokyo",
        "神奈川県":"Kanagawa",
        "新潟県":"Niigata",
        "富山県":"Toyama",
        "石川県":"Isikawa",
        "福井県":"Hukui",
        "山梨県":"Yamanasi",
        "長野県":"Nagano",
        "岐阜県":"Gihu",
        "静岡県":"Sizuoka",
        "愛知県":"Aiti",
        "三重県":"Mie",
        "滋賀県":"Siga",
        "京都府":"Kyoto",
        "大阪府":"osaka",
        "兵庫県":"Hyogo",
        "奈良県":"Nara",
        "和歌山県":"Wakayama",
        "鳥取県":"Tottori",
        "島根県":"Simane",
        "岡山県":"Okayama",
        "広島県":"Hirosima",
        "山口県":"Yamaguti",
        "徳島県":"Tokusima",
        "香川県":"Kagawa",
        "愛媛県":"Ehime",
        "高知県":"Koti",
        "福岡県":"Hukuoka",
        "佐賀県":"Saga",
        "長崎県":"Nagasaki",
        "熊本県":"Kumamoto",
        "大分県":"oita",
        "宮崎県":"Miyazaki",
        "鹿児島県":"Kagosima",
        "沖縄県":"Okinawa"
    }


    if not os.path.exists(baseURLDir + "/tmp/img/" + earthquakeId + "/"):
        os.makedirs(baseURLDir + "/tmp/img/" + earthquakeId + "/")

    for prefName in prefListArr:
        mkMapImg(prefName, prefNameToEn[prefName])

    mkMapImg(prefListArr,"list")

    # 画像生成
    from PIL import Image, ImageDraw, ImageFont # pip install pillow

    if not os.path.exists(baseURLDir + "/img/old/" + earthquakeId + "/"):
        os.makedirs(baseURLDir + "/img/old/" + earthquakeId + "/")

    def mkOutputImg(prefName):
        print("hogehoge")

        im = Image.new("RGB", (1280, 720), (31, 31, 31))

        draw = ImageDraw.Draw(im)

        if type(prefName) is str:
            imgMap = Image.open(baseURLDir + "/tmp/img/" + earthquakeId + "/" + prefNameToEn[prefName]+ ".png")
        else:
            imgMap = Image.open(baseURLDir + "/tmp/img/" + earthquakeId + "/list.png")

        if int(680 / imgMap.size[1] * imgMap.size[0]) < 850:
            imgMap = imgMap.resize((int(680 / imgMap.size[1] * imgMap.size[0]), 680))
            im.paste(imgMap, (int((850 - (680 / imgMap.size[1] * imgMap.size[0])) / 2), 20))
        else:
            imgMap = imgMap.resize((850, int(850 * imgMap.size[1] / imgMap.size[0])))
            im.paste(imgMap, (0, int((850 - (850 * imgMap.size[1] / imgMap.size[0])) / 4)))

        trans_table = str.maketrans({
                "１":"1",
                "２":"2",
                "３":"3",
                "４":"4",
                "５":"5",
                "６":"6",
                "７":"7",
                "８":"8",
                "９":"9",
                "０":"0",
            }
        )

        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        timeTxt = json_load["Head"]["Headline"]["Text"].translate(trans_table)
        timeTxtOutPut = str(now.year) + "年" + str(now.month) + "月" + timeTxt.split('日')[0] + "日" + timeTxt.split('日')[1].split('時')[0] + ":" + timeTxt.split('日')[1].split('時')[1].split('分')[0] + "頃"

        maxPoint = [""]
        maxPointListCount = 0

        print(maxPoint[maxPointListCount])

        if 'Information' in json_load["Head"]["Headline"]:
            for maxPointIndex, maxPointItem in enumerate(json_load["Head"]["Headline"]["Information"][1]["Item"]["Areas"]["Area"]):
                if len(maxPoint[maxPointListCount]) + len(maxPointItem["Name"]) >= 11:
                    maxPointListCount += 1
                    maxPoint.append(maxPointItem["Name"])
                else:
                    maxPoint[maxPointListCount] = maxPointItem["Name"] + " " + maxPoint[maxPointListCount]
                print(maxPoint)

            

        fontTitle = ImageFont.truetype(baseURLDir + '/makeImage/GenShinGothic-Medium.ttf', 28)
        fontData = ImageFont.truetype(baseURLDir + '/makeImage/GenShinGothic-Medium.ttf', 38)

        if type(prefName) is str:
            draw.multiline_text((865, 20), prefName + "の震度マップ", fill=("#f3f3f3"), font=fontTitle)
        else:
            draw.multiline_text((865, 20), "震度マップ", fill=("#f3f3f3"), font=fontTitle)

        draw.multiline_text((865, 60), "発生時刻", fill=("#f3f3f3"), font=fontTitle)
        draw.multiline_text((865, 90), timeTxtOutPut, fill=("#f3f3f3"), font=fontData)

        draw.multiline_text((865, 155), "最大震度", fill=("#f3f3f3"), font=fontTitle)
        draw.multiline_text((990, 145), json_load["Body"]["Intensity"]["Observation"]["MaxInt"], fill=("#f3f3f3"), font=fontData)

        draw.multiline_text((865, 205), "マグニチュード", fill=("#f3f3f3"), font=fontTitle)
        draw.multiline_text((1080, 195), json_load["Body"]["Earthquake"]["Magnitude"], fill=("#f3f3f3"), font=fontData)

        draw.multiline_text((865, 255), "震源地", fill=("#f3f3f3"), font=fontTitle)
        draw.multiline_text((970, 245), json_load["Body"]["Earthquake"]["Hypocenter"]["Area"]["Name"], fill=("#f3f3f3"), font=fontData)

        draw.multiline_text((865, 295), "最大震度観測点", fill=("#f3f3f3"), font=fontTitle)

        TxtLinesNum = 0
        for maxPointDrawTxt in maxPoint:
            TxtLineHeight = 325 + (TxtLinesNum * 50)
            draw.multiline_text((865, TxtLineHeight), str(maxPointDrawTxt), fill=("#f3f3f3"), font=fontData)
            TxtLinesNum += 1

        imgLevel = Image.open(baseURLDir + "/img/level.png")

        if ((imgLevel.height / 4) + 335 + (TxtLinesNum * 50)) < 720:
            imgLevel = imgLevel.resize((imgLevel.width // 4, imgLevel.height // 4))
            im.paste(imgLevel, (865, 560))
        else:
            h = ((imgLevel.height / 4) + 335 + (TxtLinesNum * 50))
            imgLevel = imgLevel.resize((h / 558 * 921, h))
            im.paste(imgLevel, (865, 335 + (TxtLinesNum * 50)))

        if type(prefName) is str:
            im.save(baseURLDir + '/img/old/' + earthquakeId + '/' + prefNameToEn[prefName] + '.png', quality=95)
        else:
            im.save(baseURLDir + '/img/old/' + earthquakeId + '/all.png', quality=95)

    mkOutputImg(prefListArr)

    for prefName in prefListArr:
        print(prefName)
        mkOutputImg(prefName)
    
    return prefListArr

if __name__ == '__main__':#直接yobareru.pyを実行した時だけ、def test()を実行する
    mkMap("earthquake")