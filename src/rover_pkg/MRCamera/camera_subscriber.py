#!/usr/bin/env python3
import rospy
import cv2 as cv
import numpy as np
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

def image_callback(img_msg):
    rospy.loginfo(img_msg)
    # frame = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    # cv.imshow("video", frame)
    # cv.waitKey(1)

if __name__ == '__main__':
    # create node
    rospy.init_node("image_sub")
    rospy.loginfo("image_sub node started")

    # create bridge
    bridge = CvBridge()

    #create subscriber with image data type
    sub = rospy.Subscriber("camera", Image, callback=image_callback)

    rospy.spin()