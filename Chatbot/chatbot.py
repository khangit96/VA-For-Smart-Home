import requests
import json
import os
import wget
import apiai
from flask import Flask,render_template, redirect, url_for
from flask import request as requestFlask
import time

app = Flask(__name__)

#home
@app.route('/',methods=['GET'])
def index():
     return render_template('index.html')

# #API AI
CLIENT_ACCESS_TOKEN = '873c83cbf665414a885eebbf5d5bd448'
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

#get resquest
@app.route('/query',methods=['POST'])
def query():
     respone= requestFlask.json

     ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

     requestApiAI = ai.text_request()
     requestApiAI.lang = 'en'  # optional, default value equal 'en'
     requestApiAI.query = respone['text']

     response = requestApiAI.getresponse()
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
     return 'ok'

#Test
thoiTietList=['long an','bình dương','hôm nay','ngày mai']

def queryApiAI(text):
     requestApiAI = ai.text_request()
     requestApiAI.lang = 'en'
     requestApiAI.query = text
     requestApiAI.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

     response = requestApiAI.getresponse()
     json_res =json.loads(response.read().decode())

     result = json_res['result']
     action= result['action']
     textRespone= result['fulfillment']['speech']

     if action =='start-weather.start-weather-custom' or action== 'start-weather-true':
        try:
            entities=result['parameters']['weather']
        except:
            entities=''

        print('Ok. Cho em ti, de em tra cuu thong tin thoi tiet '+ entities)
        time.sleep(3)

     elif action== 'start-temperature-true':
         try:
            entities=result['parameters']['temperature']
         except:
            entities=''

         print('Ok. Cho em ti, de em lay thong tin nhiet do '+ entities)
         time.sleep(3)
        

     print(textRespone)

#Start Server
# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0',port=3000)      
queryApiAI('không')




#  try:
    #     context=result['contexts'][0]['name']
    #  except:
    #     context=''

    #  try:
    #     entities=result['parameters']['ThoiTiet']
    #  except:
    #     entities=''

    # #ThoiTiet
    #  if context== 'thoi-tiet':  
    #     for s in thoiTietList:
    #         if  str(s) in text:
    #             print('ok')
    #             return
    #         #print (''+list.index(s))
    #     print('Thời tiết ở đâu ?')
    #  else:
    #    print(textRespone)

# os.system("mpg123 /home/khang/Downloads/demo.mp3")
# time.sleep(3)
# print('ok')
# os.system("pkill mpg123")