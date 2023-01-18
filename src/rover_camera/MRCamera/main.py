#!/usr/bin/env python3

import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

class Camera:
    def __init__(self, fps=20, width=320, height=240):
<<<<<<< HEAD
=======
        # Setup camera
>>>>>>> 3e6fed363ee962b718c2be4c1aea6baaca7d1e02
        self.fps = fps
        self.camera = cv2.VideoCapture(-1, cv2.CAP_V4L)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.camera.set(cv2.CAP_PROP_FPS, fps)
        self.fps = fps
<<<<<<< HEAD
        rospy.init_node('camera_node')

    def run(self): 
        rate = rospy.Rate(self.fps)
        bridge = CvBridge()
        publisher = rospy.Publisher('camera_image', Image, queue_size=10)
        while (self.camera is not None and self.camera.isOpened()):
            ret, frame = self.camera.read()
            if ret is not None:
                publisher.publish(bridge.cv2_to_imgmsg(frame, encoding="bgr8"))
                rate.sleep()

        self.camera.release()

if __name__ == '__main__':
    camera = Camera()
    camera.run()
=======
        # Set the ros node
        rospy.init_node('camera_node')
    
    def run(self): 
        # Set ros rate to match camera rate
        rate = rospy.Rate(self.fps)
        bridge = CvBridge()
        # Instantiate publisher
        publisher = rospy.Publisher('CameraToBridge', Image, queue_size=10)
        # Loop to publish images
        while (self.camera is not None and self.camera.isOpened()):
            # Get single frame from camera
            ret, frame = self.camera.read()
            if ret is not None:
                # Publish that camera as 
                publisher.publish(bridge.cv2_to_imgmsg(frame, encoding="bgr8"))
                # Wait amount of time set by ros rate
                rate.sleep()
        # Release camera when finished
        self.camera.release()

if __name__ == '__main__':
    # New camera
    camera = Camera()
    # Run the camera
    camera.run()

    
>>>>>>> 3e6fed363ee962b718c2be4c1aea6baaca7d1e02
