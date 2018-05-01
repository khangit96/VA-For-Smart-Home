import requests
import json
import apiai
from flask import Flask
from flask import request as requestFlask
import time
import config as con
import pyrebase

app = Flask(__name__)

# firebase
config = {
  "apiKey": "uTP6tlP930oA1s9zuwGIZvrz1ef8ZjVLegROgNN0",
  "authDomain": "smarthome-5d11a.firebaseapp.com",
  "databaseURL": "https://smarthome-5d11a.firebaseio.com",
  "storageBucket": "smarthome-5d11a.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def stream_handler(message):
     requestApiAI = ai.text_request()
     requestApiAI.lang = 'en'
     requestApiAI.query = message['data']
     requestApiAI.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

     response = requestApiAI.getresponse()
     json_res =json.loads(response.read().decode())

     result = json_res['result']
     action= result['action']
     textRespone= result['fulfillment']['speech']
     db.child("VA").update({"respone":textRespone})
     print(textRespone)

@app.route('/', methods=['GET'])
def index():
     my_stream = db.child("VA/message").stream(stream_handler)
     json_response = json.dumps({'result-assistance': True})
     return json_response

# #API AI
CLIENT_ACCESS_TOKEN = '873c83cbf665414a885eebbf5d5bd448'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

# get resquest
@app.route('/query',methods=['POST'])
def query():
     respone= requestFlask.json

     requestApiAI = ai.text_request()
     requestApiAI.lang = 'en'
     requestApiAI.query = respone['text']
     requestApiAI.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

     response = requestApiAI.getresponse()
     json_res =json.loads(response.read().decode())

     result = json_res['result']
     action= result['action']
     textRespone= result['fulfillment']['speech']
  
      # weather
     if action =='start-weather.start-weather-custom' or action== 'start-weather-true':
        try:
            entities=result['parameters']['weather']
        except:
            entities=''

        issueVoice('Ok chờ mình tí, để mình tra cứu thông tin thời tiết '+ entities)

    # temperature
     elif action== 'start-temperature-true':
         try:
            entities=result['parameters']['temperature']
            if entities!='':
                issueVoice('Chờ mình tí, để mình lấy thông tin nhiệt độ '+ entities)
         except:
            entities=''
            
     elif action== 'start-temperature-true.start-temperature-true-custom':
          issueVoice('Chờ mình tí, để mình lấy thông tin nhiệt độ hiện tại trong phòng')

    # control light
     elif action=='control-light-true':
          try:
            numberLight=result['parameters']['number-light']
            statusLight=result['parameters']['status-light']
            if statusLight== 'bật':
                 queryGPIO('turn-on-light',numberLight)
                 issueVoice('mình đã bật đèn '+numberLight+' rồi đó')
            elif statusLight== 'tắt':
                queryGPIO('turn-off-light',numberLight)
                issueVoice('mình đã tắt đèn '+numberLight+' rồi đó')
          except:
            numberLight=-3
            statusLight= ''
         

   
     elif action=='control-light-false.control-light-false-custom':
          context=result['contexts'][0]['parameters']

          try:
              if context['status-light']== 'bật':
                  queryGPIO('turn-on-light',context['number-light'])
                  issueVoice('mình đã bật đèn '+context['number-light']+' rồi đó')
              elif context['status-light']== 'tắt':
                  queryGPIO('turn-off-light',context['number-light'])
                  issueVoice('mình đã tắt đèn '+context['number-light']+' rồi đó')
          except:
              context= ''

     issueVoice(textRespone)
     json_response= json.dumps({'result-assistance':True})
     return json_response

# issueVoice
def issueVoice(voice):
    data={
         'voice':voice
     }
    API_ENDPOINT = 'http://'+con.GPIO_IP+':'+str(con.GPIO_PORT)+'/issue-voice'
    headers={
      'content-type': 'application/json; charset=utf-8'
     }
    r = requests.post(url = API_ENDPOINT,data=json.dumps(data),headers=headers)
    json_str = json.dumps(r.json())
    print(voice)

# query GPIO
def queryGPIO(url,light):
    data={
         'light':light
     }
    API_ENDPOINT = 'http://'+con.GPIO_IP+':'+str(con.GPIO_PORT)+'/'+url
    headers={
      'content-type': 'application/json; charset=utf-8'
     }
    r = requests.post(url = API_ENDPOINT,data=json.dumps(data),headers=headers)
    json_str = json.dumps(r.json())
    return json_str

# Start Server
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=con.ASSISTANCE_PORT)



