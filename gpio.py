import requests
import json
from flask import Flask
from flask import request as requestFlask
import config as con
import time
import os
import urllib.request

app = Flask(__name__)

#home
@app.route('/',methods=['GET'])
def index():
     return 'Index'

#Turn on light
@app.route('/turn-on-light',methods=['POST'])
def turnOnLight():
     respone= requestFlask.json
     light=respone['light']
     print('turn on light '+str(light))
     json_response= json.dumps({'result-turn-on-light':True})
     return json_response

#Turn off light
@app.route('/turn-off-light',methods=['POST'])
def turnOffLight():
     respone= requestFlask.json
     light=respone['light']
     print('turn off light '+str(light))
     json_response= json.dumps({'result-turn-off-light':True})
     return json_response

#Issue voice
@app.route('/issue-voice',methods=['POST'])
def issueVoice():
     respone= requestFlask.json
     voice=respone['voice']
     
     API_ENDPOINT = "http://api.openfpt.vn/text2speech/v4"

     headers={
            'api_key':'44c319aae94d40229d7cc09f1ce759f1',
            'speed':'0',
            'voice': 'hatieumai',
            'prosody':'1',
            'Cache-Control':'no-cache'
        }
     data = voice.encode(encoding='utf-8')
     r = requests.post(url = API_ENDPOINT,data=data,headers=headers)

     try:
        url=r.json()['async']
        print(url)
        urllib.request.urlretrieve(url,'voice.mp3')
        os.system("mpg123 voice.mp3")
        json_response= json.dumps({'result-voice':True})
        return json_response

     except:
        json_response= json.dumps({'result-voice':False})
        return json_response
        

#Get temperature
@app.route('/get-temperature',methods=['GET'])
def getTemperature():
     time.sleep(5)
     return 'temperature'

#start server 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=con.GPIO_PORT)      
