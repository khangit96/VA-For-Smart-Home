import pyrebase
import requests
import json
import os
import wget
import apiai

#Firebase
config = {
  "apiKey": "uTP6tlP930oA1s9zuwGIZvrz1ef8ZjVLegROgNN0",
  "authDomain": "smarthome-5d11a.firebaseapp.com",
  "databaseURL": "https://smarthome-5d11a.firebaseio.com",
  "storageBucket": "smarthome-5d11a.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#API AI
CLIENT_ACCESS_TOKEN = '6fb3bd7a729042bf9a656708f83bebd6'

def stream_handler(message):
     text=message['data']
     ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

     request = ai.text_request()
     request.lang = 'en'  # optional, default value equal 'en'
     request.query = text

     response = request.getresponse()
     json_res =json.loads(response.read().decode())

     result = json_res['result']
     action= result['action']
     text= result['fulfillment']['speech']
     print(text)
    
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
     print(url)
     filename = wget.download(url)
     fileMp3='mpg321 '+filename
     os.system('mv '+filename+' voice.mp3')
     os.system("mpg123 voice.mp3")
     print(text)

my_stream = db.child('chat').stream(stream_handler)

def queryAPIAI(text):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.query = text

    response = request.getresponse()
    json_res =json.loads(response.read().decode())

    result = json_res['result']
    action= result['action']
    text= result['fulfillment']['speech']
    
    #print(json.dumps(json_res, indent=4, sort_keys=True))
    print(text)