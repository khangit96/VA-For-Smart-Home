import cv2
import urllib.request
import numpy as np

#Camera raspberry stream over MJPG Streamer server
#Read stream
stream= urllib.request.urlopen('http://192.168.43.164:8080/?action=stream')
bytes = bytes()
count=0

while True:
    #get byte from stream
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        
        #Decode byte to img
        count+=1
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        
        #showimg
        cv2.imshow('i', i)
        cv2.imwrite('captured'+str(count)+'.jpg',i)
        #Exit loop
        cv2.waitKey(2000)
        