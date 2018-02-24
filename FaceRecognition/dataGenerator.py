import cv2
import numpy as np
import sys

from picamera.array import PiRGBArray
from picamera import PiCamera
import time

face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
time.sleep(0.1)
count=0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
     
    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
    for (x,y,w,h) in faces:
        count+=1
        cv2.imwrite('user.6.'+str(count)+'.jpg',gray[y:y+h,x:x+w])
        print('Detect face')
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
    cv2.imshow("Frame", img)
    cv2.waitKey(100)
 
    rawCapture.truncate(0)
 
    #if key == ord("q"):
	   # break
