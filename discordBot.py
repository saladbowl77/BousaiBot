# インストールした discord.py を読み込む
from discord.ext import tasks
import discord
import json
import csv
from os.path import dirname

import getNewest

baseURLDir = dirname(__file__)
addImgNewsList = []

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzA2NDEyMjkxNzUwMzYzMTU4.Xq53tg.RGBZW9xSUooywhdfw6_lRcNuHW4'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == 'test':
        print("test")
        fileImg = discord.File(baseURLDir + "/img/old/20210710052352/all.png", filename="ファイル名.png")
        await message.channel.send(file=fileImg)
    elif message.content[:13] == '/EQ -webhook ':
        with open('data/webhookURL.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([message.content[13:]])
        await message.channel.send("地震通知を登録しました!")
    elif message.content[:3] == '/EQ' or message.content[:3] == '/EQ help':
        await message.channel.send("Help\n地震通知Webhook追加 ``/EQ -webhook https://discord.com/api/webhooks/XXXXXXX``")


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)