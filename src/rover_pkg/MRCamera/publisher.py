#!/usr/bin/env python3

import cv2
import time
import queue
from threading import Thread

import numpy as np

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

w = 320
h = 240

# class CameraCaptureThread(Thread):
#    def __init__(self, camera=None, workQueue=None):
#        Thread.__init__(self)
#        self.camera = camera
#        self.workQueue = workQueue
#
#    def run(self):
#
#        while (self.camera.isAvailable() and not rospy.is_shutdown()):
#            #print("lol")
# 	    # rospy.loginfo("Capturing a frame.")
#            ret, frame = self.camera.captureFrame()
#            #if ret is not None:
#            self.workQueue.put(frame)
#
#        self.camera.release()


class Camera:
    def __init__(self, fps=30, width=320, height=240):
        self.camera = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.camera.set(cv2.CAP_PROP_FPS, fps)

    def captureFrame(self):
        return self.camera.read()

    def release(self):
        self.camera.release()

    def isAvailable(self):
        return self.camera is not None and self.camera.isOpened()


def createImageObject(frame):
    bridge = CvBridge()
    print(frame)
    if frame != None:
        return bridge.cv2_to_imgmsg(frame, encoding="passthrough")
    return bridge.cv2_to_imgmsg(np.zeros(w, h, 3), encoding="passthrough")


if __name__ == "__main__":
    rate = 5

    rospy.loginfo("Initiate the work queue and the camera.")
    #    workQueue = None
    #    workQueue = queue.Queue()
    camera = Camera(rate, w, h)

    # Start a separate thread to capture frames
    # cameraCaptureThread = CameraCaptureThread(camera = camera, workQueue = workQueue)
    # rospy.loginfo("Start the thread to capture image.")
    # cameraCaptureThread.start()

    # ROS setting
    rospy.loginfo("Initiate the camera_node.")
    rospy.init_node("camera_node")
    rate = rospy.Rate(5)

    rospy.loginfo("Create the camera_image publisher.")
    publisher = rospy.Publisher("CameraToBase", Image, queue_size=10)

    while not rospy.is_shutdown():
        #        if (not workQueue.empty()):
        # rospy.loginfo("Publish the captured frame.")
        print("hfdjsfghbsd")
        publisher.publish(createImageObject(camera.captureFrame()))

        rate.sleep()

#    cameraCaptureThread.join()
