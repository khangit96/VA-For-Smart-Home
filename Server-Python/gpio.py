import requests
import json
from flask import Flask
from flask import request as requestFlask
import config as con
import time
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
     print(str(light))
     return str(light)

#Turn off light
@app.route('/turn-off-light',methods=['POST'])
def turnOffLight():
     respone= requestFlask.json
     light=respone['light']
     print(str(light))
     return str(light)

#Get temperature
@app.route('/get-temperature',methods=['GET'])
def getTemperature():
     time.sleep(5)
     return 'temperature'

#start server 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=con.GPIO_PORT)      



