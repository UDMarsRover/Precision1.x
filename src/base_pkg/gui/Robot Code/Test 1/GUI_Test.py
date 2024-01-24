"""
Created on Oct 6, 2022

@author: jdunh
"""
from multiprocessing import Process
import time
from markupsafe import escape
from flask import Flask, render_template, request, Response
import cv2
from turbo_flask import Turbo

app = Flask(__name__)

video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier()
# face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))
"""
def gen(video):
    while True:
        success, image = video.read()
        frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)

        faces = face_cascade.detectMultiScale(frame_gray)

        for (x, y, w, h) in faces:
            center = (x + w//2, y + h//2)
            cv2.putText(image, "X: " + str(center[0]) + " Y: " + str(center[1]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            faceROI = frame_gray[y:y+h, x:x+w]
        ret, jpeg = cv2.imencode('.jpg', image)

        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
"""


@app.route("/")
def text():
    print("Hi2")
    return render_template("text.html")


@app.route("/item2")
def idk():
    looping()
    return render_template("file2.html")


@app.route("/input", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("action1") == "VALUE1":
            print(1)  # do something
        elif request.form.get("action2") == "VALUE2":
            print(2)  # do something else
        else:
            pass  # unknown
    elif request.method == "GET":
        return render_template("index.html")

    return render_template("index.html")


def looping():
    i = 1
    while i < 10:
        i += 1
        print(i)
        time.sleep(1)


@app.route("/video_feed")
def video_feed():
    # Set to global because we refer the video variable on global scope,
    # Or in other words outside the function
    global video

    # Return the result on the web
    return Response(video)

    mimetype = "multipart/x-mixed-replace; boundary=frame"


if __name__ == "__main__":
    Process(target=looping).start()


app.run()
