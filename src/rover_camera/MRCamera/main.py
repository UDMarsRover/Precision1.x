#!/usr/bin/env python3

import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

class Camera:
    def __init__(self):
        self.fps = 20
        self.camera = cv2.VideoCapture(-1, cv2.CAP_V4L)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.camera.set(cv2.CAP_PROP_FPS, 20)
        print("camera created.")
        print(self.camera.isOpened())
    
    def run(self): 
        rate = rospy.Rate(80)
        bridge = CvBridge()
        publisher = rospy.Publisher('camera_image', Image, queue_size=10)
        while (self.camera is not None and self.camera.isOpened()):
            ret, frame = self.camera.read()
            if ret is not None:
                publisher.publish(bridge.cv2_to_imgmsg(frame, encoding="passthrough"))
                rate.sleep()
        print(self.camera.isOpened())
        self.camera.release()

if __name__ == '__main__':
    rospy.init_node('camera_node')
    print("running")
    camera = Camera()
    print("fps: ", camera.fps)
    camera.run()




