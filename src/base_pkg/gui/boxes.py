import random
import re
import sys
from flask import Flask, Response, render_template
from turbo_flask import Turbo
import threading
import time
import cv2




print(random.random())

app = Flask(__name__)
turbo = Turbo(app)

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()
    threading.Thread(target=inject_load).start()
    #threading.Thread(target=inject_load2).start()



def update_load():
    with app.app_context():
        while True:
            time.sleep(0.5)
            #turbo.push(turbo.replace(render_template('load_boxes.html'), 'error_boxes'))
            turbo.push(turbo.replace(render_template('box_object_test.html'), 'error_boxes'))
            

##############################################################################################################################
#All web addresses
#****************
#The main UDMRT UD page
@app.route('/')
def index():
    #return render_template('UDMRT_UI.html')
    return render_template('box_object_test.html')

#Displays all of the data from the main page in raw format.
@app.route('/raw')
def raw():
    return render_template('raw_data.html')

#Display the entire log from the rover.
@app.route('/log')
def log():
    return render_template('log.html')

#If someone goes to the wrong page.
@app.errorhandler(404)
def page_not_found(error):
    return render_template('Page_Not_Found.html'), 404
##############################################################################################################################
    
    
#@app.route('/errors')
#def errors():
    #app.logger.debug('A value for debugging')
    #app.logger.warning('A warning occurred (%d apples)', 42)
    #app.logger.error('An error occurred')
    #return render_template('index2.html')


    



@app.context_processor
def inject_load():
    #load = [int(random.random() * 100) / 100 for _ in range(3)]
    color = [int(random.random() * 200) for _ in range(23)]
    
    
    black = [0,0,0]
    red = [255,0,0]
    yellow = [255,255,0]
    green = [0,255,0]
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
        
    return {'speed': 1, 'RS': 2, 'FD': 3, 'Lat': 4, 'Roll': 5}


    #return {'speed': status1[0], 'RS': status1[1], 'FD': status1[2], 'Lat': status2[0], 'Roll': status2[1], 'Pitch': status2[2], 'Temp': status3[0], 'OHW': status3[1], 'Pi': status3[2], 'Emo': status4[0], 'load11': status4[1], 'load12': status4[2], 'load13': status5[0], 'load14': status5[1], 'load15': status5[2], 'load16': status6[0], 'load17': status6[1], 'load18': status6[2], 'load19': status7[0], 'load20': status7[1], 'load21': status7[2]}

    #print(str(len(dictOut)))
        
    


@app.context_processor
def inject_load2():
    speeding = [int(random.random() * 200) for _ in range(1)]
    return {'speed6': speeding[0]}



#def running():
    #app = Flask(__name__)
    #turbo = Turbo(app)
app.run()


