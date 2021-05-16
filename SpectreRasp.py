# import the necessary packages
from tkinter import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import requests
import cv2
import PIL.Image, PIL.ImageTk
import threading
import time
import RPi.GPIO as GPIO
import json

PIN_OUT = 18  # VIDEO IN ACTION
PIN_OUT2 = 25  # FACE DETECTION
faceCascade = 0
camara = 0
rawCapture = 0
def initCamera():
    global PIN_OUT, PIN_OUT2, faceCascade, camera, rawCapture
    # initiate algorhitms detection
    faceCascade = cv2.CascadeClassifier('/home/pi/Desktop/Spectre/haarcascade_frontalface_alt2.xml')
    # eyeCascade = cv2.CascadeClassifier('/home/pi/Desktop/Spectrehaarcascade_eye.xml')

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 90
    rawCapture = PiRGBArray(camera, size=(640, 480))

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_OUT, GPIO.OUT)
    GPIO.setup(PIN_OUT2, GPIO.OUT)
    GPIO.output(PIN_OUT, GPIO.LOW)
    GPIO.output(PIN_OUT2, GPIO.LOW)
    # allow the camera to warmup
    time.sleep(0.5)
    FaceDetection()

def endedVideo():
    global PIN_OUT, PIN_OUT2, faceCascade, camera, rawCapture
    while(True):
        r = requests.get("http://127.0.0.1:8080/getDetection")
        json_data = json.loads(r.text)
        #print(json_data['detection'])
        if(json_data['detection'] == "False"):
            GPIO.output(PIN_OUT, GPIO.LOW)
            FaceDetection()
            break
        time.sleep(10)

def FaceDetection():
    global PIN_OUT, PIN_OUT2, faceCascade, camera, rawCapture
    try:
        GPIO.output(PIN_OUT2, GPIO.HIGH)
        rawCapture.truncate(0)
        # capture frames from the camera
        try:
            for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                frame = image.array
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,minSize=(30, 30))  # flags = cv2.CV_HAAR_SCALE_IMAGE
                if (len(faces) > 0):
                    print("Detected")
                    #rawCapture.truncate(0)
                    GPIO.output(PIN_OUT2, GPIO.LOW)
                    GPIO.output(PIN_OUT, GPIO.HIGH)
                    r = requests.post("http://127.0.0.1:8080/detected")
                    t1 = threading.Thread(target = endedVideo)
                    t1.start()
                    break
                # # for (x, y, w, h) in faces:
                # #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #
                # # show the frame
               # cv2.imshow("Frame", frame)
                #key = cv2.waitKey(1) & 0xFF
                rawCapture.truncate(0)
        except:
            print("FALLE COMO CAMARA")
            camera.close()
            GPIO.output(PIN_OUT, GPIO.LOW)
            GPIO.output(PIN_OUT2, GPIO.LOW)
            initCamera()
    except KeyboardInterrupt:
        camera.close()
        GPIO.output(PIN_OUT, GPIO.LOW)
        GPIO.output(PIN_OUT2, GPIO.LOW)

initCamera()
