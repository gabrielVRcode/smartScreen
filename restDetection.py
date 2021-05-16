import numpy as np
import cv2
import os
from flask import Flask
from flask import request
from flask_cors import CORS
import json
import sys

sys.stdout.flush()
flag = "False"
reload = "False"
fileName = ""
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello World !"

@app.route("/detected", methods=["POST"])
def faceDetected():
    global flag
    flag = "True"
    data = {"status": "success"}
    return json.dumps(data)

@app.route("/deactivate", methods=["POST"])
def returnStatus():
    global flag
    flag = "False"
    data = {"status" : "success"}
    return json.dumps(data)

@app.route("/getDetection", methods=["GET"])
def getDetection():
    global flag
    data={
        "detection": flag,
        "reload": reload
    }
    return json.dumps(data)

@app.route("/changeVideo", methods=["POST"])
def changeVideo():
    global reload
    if 'file' not in request.files:
        print("bad request")
    file = request.files['file']
    filename = "promo.mp4"
    file.save(os.path.join("/home/pi/Desktop/Spectre/", filename))
    reload = "True"
    data = {
        "status": "Done !"
    }
    return json.dumps(data)

@app.route("/doneVideo", methods=["POST"])
def doneVideo():
    global reload
    reload = "False"
    data = {
        "status": "Done !"
    }
    return json.dumps(data)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

