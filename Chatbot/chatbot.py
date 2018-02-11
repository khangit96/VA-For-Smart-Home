import pyrebase
import requests
import json
import os
import wget

config = {
  "apiKey": "uTP6tlP930oA1s9zuwGIZvrz1ef8ZjVLegROgNN0",
  "authDomain": "smarthome-5d11a.firebaseapp.com",
  "databaseURL": "https://smarthome-5d11a.firebaseio.com",
  "storageBucket": "smarthome-5d11a.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def stream_handler(message):
     text=message['data']
     API_ENDPOINT = "http://api.openfpt.vn/text2speech/v4"

     headers={
            'api_key':'44c319aae94d40229d7cc09f1ce759f1',
            'speed':'0',
            'voice': 'hatieumai',
            'prosody':'1',
            'Cache-Control':'no-cache'
        }
     data = text.encode(encoding='utf-8')
     r = requests.post(url = API_ENDPOINT,data=data,headers=headers)

     url =r.json()['async']
     filename = wget.download(url)
     fileMp3='mpg321 '+filename
     os.system('mv '+filename+' voice.mp3')
     os.system("mpg123 voice.mp3")
     print(text)

#my_stream = db.child('chat').stream(stream_handler)

os.system("mpg123 voice.mp3")