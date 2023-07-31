import random
import re
import sys
from flask import Flask, render_template
from turbo_flask import Turbo
import threading
import time
import cv2


#video = cv2.VideoCapture(0)
#face_cascade = cv2.CascadeClassifier()
#face_cascade.load(cv2.samples.findFile("static/haarcascade_frontalface_alt.xml"))




print(random.random())

    



app = Flask(__name__)

turbo = Turbo(app)

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()

def update_load():
    with app.app_context():
        while True:
            time.sleep(0.5)
            turbo.push(turbo.replace(render_template('loadavg.html'), 'color'))



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page2')
def page2():
    
    return render_template('Tubro_Test.html')

@app.context_processor
def inject_load():
    #load = [int(random.random() * 100) / 100 for _ in range(3)]
    color = [int(random.random() * 256)/266 for _ in range(3)]
    return {'load1': color[0], 'load5': color[1], 'load15': color[2]}



app.run()



#<tr><body bgcolor= "<td>{{ load1 }}</td>"></tr>
 # </body>

