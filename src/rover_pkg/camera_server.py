#!/usr/bin/env python3
import cv2
import numpy as np
from flask import Flask, Response

app = Flask(__name__)

def webcam_feed():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Apply color correction for weird windows blue shift
        # Reduce the framerate by adding a delay
        # Uncomment the line below to reduce the framerate to 1 frame per second
        cv2.waitKey(100)
        # frame = np.where(frame > 1, frame - 1, frame)

        # Compress the frame for low latency
        _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 20])
        frame_bytes = compressed_frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return Response(webcam_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()2