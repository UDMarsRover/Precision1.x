from flask import Flask, Response, render_template
import cv2
from turbo_flask import Turbo
import threading
import time
import random
import re
import sys
import datetime


app = Flask(__name__)
video = cv2.VideoCapture(1)
turbo = Turbo(app)

"""
global clk 
global clk2
def clock():
    with app.app_context:
        while True:
            clk = round(time.time())
            clk2 = clk % 2
            time.sleep(0.5)
"""


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


"""
def clock():
    with app.app_context():
        while True:
            clk = 1
            time.sleep(0.5)
            clk = 0
            time.sleep(0.5)
"""


def update_load():
    with app.app_context():
        while True:
            time.sleep(0.5)
            turbo.push(turbo.replace(render_template("loadavg.html"), "load"))
            # turbo.push(turbo.replace(render_template('Speed.html'), 'speed'))
            print("Hey!")


@app.route("/")
def index():
    return render_template("index1.html")


def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode(".jpg", image)

        frame = jpeg.tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


@app.route("/video_feed")
def video_feed():
    global video
    return Response(gen(video), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.context_processor
def inject_load():
    # while (0 == clk2):
    # load = [int(random.random() * 100) / 100 for _ in range(3)]
    color = [int(random.random() * 200) for _ in range(23)]

    # time.sleep(1)
    black = [0, 0, 0]
    red = [255, 0, 0]
    yellow = [255, 255, 0]
    green = [0, 255, 0]
    status1 = black
    status2 = black

    if color[1] > 150:
        status1 = red

    elif color[1] >= 100:
        status1 = green

    else:
        status1 = yellow

    if color[2] > 100:
        status2 = red

    elif color[3] >= 50:
        status2 = green

    else:
        status2 = yellow

    if color[3] < 50:
        status3 = red

    elif color[3] <= 100:
        status3 = green

    else:
        status3 = yellow

    if color[4] > 135:
        status4 = green

    elif color[4] >= 70:
        status4 = red

    else:
        status4 = yellow

    if color[5] > 150:
        status5 = red

    elif color[5] >= 100:
        status5 = green

    else:
        status5 = yellow

    if color[6] > 150:
        status6 = red

    elif color[6] >= 100:
        status6 = green

    else:
        status6 = yellow

    if color[7] > 150:
        status7 = red

    elif color[7] >= 100:
        status7 = green

    else:
        status7 = yellow

    return {
        "load1": status1[0],
        "load2": status1[1],
        "load3": status1[2],
        "load4": status2[0],
        "load5": status2[1],
        "load6": status2[2],
        "load7": status3[0],
        "load8": status3[1],
        "load9": status3[2],
        "load10": status4[0],
        "load11": status4[1],
        "load12": status4[2],
        "load13": status5[0],
        "load14": status5[1],
        "load15": status5[2],
        "load16": status6[0],
        "load17": status6[1],
        "load18": status6[2],
        "load19": status7[0],
        "load20": status7[1],
        "load21": status7[2],
    }


if __name__ == "__main__":
    app.run()
