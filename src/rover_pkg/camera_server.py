#!/usr/bin/env python3
import cv2
import numpy as np
from flask import Flask, Response
import time
import rospy
from std_msgs.msg import Int8

app = Flask(__name__)

# Load the ArUco dictionary
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)   

# Initialize the ROS node
rospy.init_node('camera_publisher', anonymous=True)

# Create a ROS publisher
marker_pub = rospy.Publisher('/pi/camera/aruco', Int8, queue_size=10)

def webcam_feed():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()

        # Apply color correction for weird windows blue shift
        # Reduce the framerate by adding a delay
        # Uncomment the line below to reduce the framerate to 1 frame per second
        # frame = np.where(frame > 1, frame - 1, frame)
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers
        corners, ids, rejected = detector.detectMarkers(gray)
        if ids is not None:
            for i in range(len(ids)):
                # Draw outline of the marker on the current frame
                # Get the corners of the marker
                marker_corners = corners[i][0]
                marker_corners = marker_corners.astype(int)
                # Draw the outline of the marker
                cv2.polylines(frame, [marker_corners], True, (0, 255, 0), 2)
                # Put the text of the ID in the middle of the tag in the frame
                # Calculate the center of the marker
                center_x = int((marker_corners[0][0] + marker_corners[2][0]) / 2)
                center_y = int((marker_corners[0][1] + marker_corners[2][1]) / 2)

                # Draw the ID text on the frame
                cv2.putText(frame, str(ids[i]), (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                marker_id_msg = Int8(ids[i])
                marker_pub.publish(marker_id_msg)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        # Compress the frame for low latency
        _, compressed_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 20])
        frame_bytes = compressed_frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        # cv2.waitKey(100)
        time.sleep(0.03)

@app.route('/')
def index():
    return Response(webcam_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()