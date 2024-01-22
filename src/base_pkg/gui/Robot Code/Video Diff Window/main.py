# Main Class
import random
import re
import sys
from flask import Flask, render_template, Response
from turbo_flask import Turbo

# import threading
# import time
import cv2
import Boxes_Only as box
import Video_Only as vid
import logging
import threading
import time


app = Flask(__name__)
turbo = Turbo(app)
global video


def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode(".jpg", image)

    frame = jpeg.tobytes()

    yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


def boxRunner():
    video = cv2.VideoCapture(0)


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()
    threading.Thread(target=video_feed).start()
    threading.Thread(target=index).start()


def update_load():
    with app.app_context():
        while True:
            time.sleep(0.5)
            # turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))
            turbo.push(turbo.replace(render_template("Speed.html"), "speed"))


@app.route("/")
def index1():
    return "Default Message"


@app.route("/video_feed")
def video_feed():
    return Response(gen(video), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/hi")
def index():
    return render_template("index.html")


@app.route("/page2")
def page2():
    return render_template("Tubro_Test.html")


@app.context_processor
def inject_load():
    # load = [int(random.random() * 100) / 100 for _ in range(3)]
    color = [int(random.random() * 200) for _ in range(23)]


@app.context_processor
def inject_load2():
    speeding = [int(random.random() * 200) for _ in range(1)]
    return {"speed1": speeding[0]}
    # v1 = vid.video();


b = threading.Thread(target=boxRunner, args=())
b.start()

# v = threading.Thread(target=vidRunner, args=())
# v.start()

# vF = threading.Thread(target=vidFeed, args=())
# vF.start()


if __name__ == "__main__":
    app.run()
