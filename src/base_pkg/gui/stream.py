from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

# Create a webcam object
video = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame as a multipart response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
