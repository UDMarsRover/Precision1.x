#!/usr/bin/env python3

import cv2 as cv
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

def start_node():
    rospy.init_node('image_pub')
    rospy.loginfo('image_pub node started')

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptExcepetion:
        pass

# bridge = CvBridge()

# capture = cv.VideoCapture(0)

# if not capture.isOpened():
#     print("cannot open camera")
#     exit(0)

# while True:
#     ret, frame = capture.read()

#     if not ret:
#         print("Can't recieve frame")
#         break