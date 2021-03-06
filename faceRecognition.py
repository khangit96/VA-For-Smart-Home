
import cv2
import dlib
import config as con
import requests
import json
import threading
import time

faceCascade = cv2.CascadeClassifier('./Model/haarcascade_frontface.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('./Model/trainner.yml')

OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600

# issueVoice


def issueVoice(arg, arg2):
    data = {
        'voice': arg
    }
    API_ENDPOINT = 'http://'+con.GPIO_IP+':'+str(con.GPIO_PORT)+'/issue-voice'
    headers = {
        'content-type': 'application/json; charset=utf-8'
    }
    r = requests.post(url=API_ENDPOINT, data=json.dumps(data), headers=headers)
    json_str = json.dumps(r.json())
    print(json_str)

# query assistance


def queryAssistance(arg, arg2):
    data = {
        'text': arg
    }
    API_ENDPOINT = 'http://localhost:'+str(con.ASSISTANCE_PORT)+'/query'
    headers = {
        'content-type': 'application/json; charset=utf-8'
    }
    r = requests.post(url=API_ENDPOINT, data=json.dumps(data), headers=headers)

    if r is None:
        print('error respones')
    else:
        json_str = json.dumps(r.json())
        print(json_str)

# start thread query assistance


def startThreadQueryAssistance(value):
    thread = threading.Thread(target=queryAssistance, args=(value, 'fkf'))
    thread.start()

# start thread issuse voice


def startThreadIssuseVoice(value):
    thread = threading.Thread(target=issueVoice, args=(value, 'fkf'))
    thread.start()

# predict face


def predictFace(gray, faces):
   for (x, y, w, h) in faces:
        Id, con = recognizer.predict(gray[y:y+h, x:x+w])

        if con < 100:
            if Id == 1:
                Id = "Huy"
            elif Id == 2:
                Id = "Khang"
            elif Id == 3:
                Id = 'Khang'
            elif Id == 4:
                Id = 'Khang'
            elif Id == 5:
                Id = 'Khang'
            elif Id == 6:
                Id = 'Khang'
            elif Id == 7:
                Id = 'Tuan'
        else:
            Id = "người lạ"

        if countPredict == 7:
              if Id == "người lạ":
                 startThreadIssuseVoice('xin chào, bạn tên gì')
              else:
                 startThreadIssuseVoice('xin chào ' + Id+'. ' + Id+'cần hỗ trợ gì')
              print(Id+'-'+str(con))
 
countPredict=0

# detect and tracking face
def detectAndTrackLargestFace():
    capture = cv2.VideoCapture(0)

    cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("base-image", 0, 100)
    cv2.moveWindow("result-image", 400, 100)

    # Start the window thread for the two windows we are using
    cv2.startWindowThread()

    # Create the tracker we will use
    tracker = dlib.correlation_tracker()

    # The variable we use to keep track of the fact whether we are
    # currently using the dlib tracker
    trackingFace = 0

    # The color of the rectangle we draw around the face
    rectangleColor = (0, 165, 255)

    try:
        while True:
            # Retrieve the latest image from the webcam
            rc, fullSizeBaseImage = capture.read()

            # Resize the image to 320x240
            baseImage = cv2.resize(fullSizeBaseImage, (320, 240))

            # Check if a key was pressed and if it was Q, then destroy all
            # opencv windows and exit the application
            pressedKey = cv2.waitKey(2)
            if pressedKey == ord('Q'):
                cv2.destroyAllWindows()
                exit(0)

            # Result image is the image we will show the user, which is a
            # combination of the original image from the webcam and the
            # overlayed rectangle for the largest face
            resultImage = baseImage.copy()

            # If we are not tracking a face, then try to detect one
            if not trackingFace:

                # For the face detection, we need to make use of a gray
                # colored image so we will convert the baseImage to a
                # gray-based image
                gray = cv2.cvtColor(baseImage, cv2.COLOR_BGR2GRAY)
                # Now use the haar cascade detector to find all faces
                # in the image
                faces = faceCascade.detectMultiScale(gray, 1.3, 5)

                # For now, we are only interested in the 'largest'
                # face, and we determine this based on the largest
                # area of the found rectangle. First initialize the
                # required variables to 0
                maxArea = 0
                x = 0
                y = 0
                w = 0
                h = 0

                # Loop over all faces and check if the area for this
                # face is the largest so far
                # We need to convert it to int here because of the
                # requirement of the dlib tracker. If we omit the cast to
                # int here, you will get cast errors since the detector
                # returns numpy.int32 and the tracker requires an int
                for (_x, _y, _w, _h) in faces:
                    if _w*_h > maxArea:
                        x = int(_x)
                        y = int(_y)
                        w = int(_w)
                        h = int(_h)
                        maxArea = w*h

                        predictFace(gray,faces)

                # If one or more faces are found, initialize the tracker
                # on the largest face in the picture
                if countPredict==7:
                    global countPredict
                    countPredict=0
                    if maxArea > 0:

                        # Initialize the tracker
                        tracker.start_track(baseImage, dlib.rectangle(
                            x-10, y-20, x+w+10, y+h+20))

                        # Set the indicator variable such that we know the
                        # tracker is tracking a region in the image
                        trackingFace = 1
                else:
                    countPredict+=1

            # Check if the tracker is actively tracking a region in the image
            if trackingFace:

                # Update the tracker and request information about the
                # quality of the tracking update
                trackingQuality = tracker.update(baseImage)

                # If the tracking quality is good enough, determine the
                # updated position of the tracked region and draw the
                # rectangle
                if trackingQuality >= 8.75:
                    tracked_position = tracker.get_position()

                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())
                    cv2.rectangle(resultImage, (t_x, t_y),
                                  (t_x + t_w, t_y + t_h), rectangleColor, 2)

                else:
                    # If the quality of the tracking update is not
                    # sufficient (e.g. the tracked region moved out of the
                    # screen) we stop the tracking of the face and in the
                    # next loop we will find the largest face in the image
                    # again
                    trackingFace = 0
                    print('stop tracking')
                    #startThreadIssuseVoice('mình không thấy mặt bạn, vui lòng quay lại đi')
                    

            # Since we want to show something larger on the screen than the
            # original 320x240, we resize the image again
            #
            # Note that it would also be possible to keep the large version
            # of the baseimage and make the result image a copy of this large
            # base image and use the scaling factor to draw the rectangle
            # at the right coordinates.
            largeResult = cv2.resize(
                resultImage, (OUTPUT_SIZE_WIDTH, OUTPUT_SIZE_HEIGHT))

            # Finally, we want to show the images on the screen
          
            cv2.imshow("result-image", largeResult)

    except KeyboardInterrupt as e:
        cv2.destroyAllWindows()
        exit(0)


if __name__ == '__main__':
    detectAndTrackLargestFace()
