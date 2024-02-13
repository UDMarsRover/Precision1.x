import random
import re
import sys
from flask import Flask, render_template, Response
from turbo_flask import Turbo
import threading
import time
import cv2



video = cv2.VideoCapture(0)
#face_cascade = cv2.CascadeClassifier()
#face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))





global frame
    




app = Flask(__name__)
    
def create_app():
    with app.app_context():
        cv2()
        Flask()
        Turbo()
        render_template()
        Response()

    return app

video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier()
face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))

turbo = Turbo(app)
@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(0.5)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'load'))



def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)

        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n' + render_template('index.html'))









@app.route('/')
def index():
    return render_template('index.html') + Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/page2')
def page2():
    global video

    return (Response(gen(video),
                     mimetype='multipart/x-mixed-replace; boundary=frame'))#,
            #render_template('Tubro_Test.html'))

#@app.context_processor
#def inject_load():
 #   load = [int(random.random() * 100) / 100 for _ in range(3)]
   # return {'load1': load[0], 'load5': load[1], 'load15': load[2]}

app.run()

