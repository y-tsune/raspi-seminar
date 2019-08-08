#coding: UTF-8
import json
from requests_oauthlib import OAuth1Session
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

camera = PiCamera()

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

twitter = OAuth1Session(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
url_text = 'https://api.twitter.com/1.1/statuses/update.json'
url_media = "https://upload.twitter.com/1.1/media/upload.json"

while True:
    if GPIO.input(18):
        camera.start_preview()
        sleep(1)
        camera.capture('./image.jpg')
        camera.stop_preview()
        # 画像投稿
        files = {"media" : open('image.jpg', 'rb')}
        req_media = twitter.post(url_media, files = files)

        # レスポンスを確認
        if req_media.status_code != 200:
            print ("画像アップデート失敗: %s", req_media.text)
            GPIO.cleanup()
            exit()
        else:
            print ("uploading is success")

        # Media ID を取得
        media_id = json.loads(req_media.text)['media_id']
        print ("Media ID: %d" % media_id)

        # Media ID を付加してテキストを投稿
        params = {'status': '画像投稿テスト', "media_ids": [media_id]}
        req_media = twitter.post(url_text, params = params)

        # 再びレスポンスを確認
        if req_media.status_code != 200:
            print ("テキストアップデート失敗: %s", req_text.text)
            GPIO.cleanup()
            exit()

        print ("OK")

    sleep(1)

GPIO.cleanup()
