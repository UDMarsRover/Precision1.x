from flask import Flask, Response
import cv2

global app 
app = Flask(__name__)

class video:
   video = cv2.VideoCapture(0)

#@app.route('/')
#def index():
    #return "Default Message"

def gen(video):
    while True:
        
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)

       

        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#if __name__ == '__main__':
    #app.run()