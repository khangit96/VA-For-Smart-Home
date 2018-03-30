import requests
import json
from flask import Flask
from flask import request as requestFlask
import config as con
import time
import os
import wget
import RPi.GPIO as GPIO
import time

app = Flask(__name__)


GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

#Relay1
GPIO.setup(20,GPIO.OUT)

#Relay2
GPIO.setup(21,GPIO.OUT)


#home
@app.route('/',methods=['GET'])
def index():
     return 'Index'

#Turn on light
@app.route('/turn-on-light',methods=['POST'])
def turnOnLight():
     respone= requestFlask.json
     light=respone['light']
     if light=="1":
         GPIO.output(20,GPIO.LOW)
     else:
         GPIO.output(21,GPIO.LOW)
         
     print('turn on light '+light)
     json_response= json.dumps({'result-turn-on-light':True})
     return json_response

#Turn off light
@app.route('/turn-off-light',methods=['POST'])
def turnOffLight():
     respone= requestFlask.json
     light=respone['light']
     if light=="2":
         GPIO.output(20,GPIO.LOW)
     else:
         GPIO.output(21,GPIO.LOW)
     print('turn off light '+light)
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

     url =r.json()['async']
     print(url)
     filename = wget.download(url)
     fileMp3='mpg321 '+filename
     os.system('mv '+filename+' voice.mp3')
     os.system("mpg123 voice.mp3")

     json_response= json.dumps({'result-voice':True})
     return json_response

#Get temperature
@app.route('/get-temperature',methods=['GET'])
def getTemperature():
     time.sleep(5)
     return 'temperature'

#start server 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=con.GPIO_PORT)      

def issueVoice(text):     
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
