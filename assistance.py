import requests
import json
import apiai
from flask import Flask
from flask import request as requestFlask
import time
import config as con

app = Flask(__name__)

#home
@app.route('/',methods=['GET'])
def index():
     return 'Index'

# #API AI
CLIENT_ACCESS_TOKEN = '873c83cbf665414a885eebbf5d5bd448'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

#get resquest
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

      #weather
     if action =='start-weather.start-weather-custom' or action== 'start-weather-true':
        try:
            entities=result['parameters']['weather']
        except:
            entities=''

       # print('Ok. Cho em ti, de em tra cuu thong tin thoi tiet '+ entities)
        issueVoice('Ok chờ mình tí, để mình tra cứu thông tin thời tiết '+ entities)
        time.sleep(3)

    #temperature
     elif action== 'start-temperature-true':
         try:
            entities=result['parameters']['temperature']
         except:
            entities=''
         issueVoice('Ok. Chờ mình tí, để mình lấy thông tin nhiệt độ '+ entities)

         time.sleep(3)

    #control light
     elif action=='control-light-true':
          try:
            numberLight=result['parameters']['number-light']
            statusLight=result['parameters']['status-light']
          except:
            numberLight=-3
            statusLight= ''
          if statusLight== 'bật':
             queryGPIO('turn-on-light',numberLight)
          elif statusLight== 'tắt':
             queryGPIO('turn-off-light',numberLight)
   
     elif action=='control-light-false.control-light-false-custom':
          context=result['contexts'][0]['parameters']

          if context['status-light']== 'bật':
              queryGPIO('turn-on-light',context['number-light'])
              issueVoice('Em đã bật đèn '+context['number-light']+' rồi đó')
          elif context['status-light']== 'tắt':
              queryGPIO('turn-off-light',context['number-light'])
              issueVoice('Em đã tắt đèn '+context['number-light']+' rồi đó')

     issueVoice(textRespone)
     json_response= json.dumps({'result-assistance':True})
     return json_response

#issueVoice
def issueVoice(voice):
    data={
         'voice':voice
     }
    API_ENDPOINT = 'http://localhost:'+str(con.GPIO_PORT)+'/issue-voice'
    headers={
      'content-type': 'application/json; charset=utf-8'
     }
    r = requests.post(url = API_ENDPOINT,data=json.dumps(data),headers=headers)
    json_str = json.dumps(r.json())
    print(json_str)
  #  return json_str

#query GPIO
def queryGPIO(url,light):
    data={
         'light':light
     }
    API_ENDPOINT = 'http://localhost:'+str(con.GPIO_PORT)+'/'+url
    headers={
      'content-type': 'application/json; charset=utf-8'
     }
    r = requests.post(url = API_ENDPOINT,data=json.dumps(data),headers=headers)
    json_str = json.dumps(r.json())
    print(json_str)

#Start Server
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=con.ASSISTANCE_PORT)



