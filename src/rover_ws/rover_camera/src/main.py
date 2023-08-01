#!/usr/bin/env python3

import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

class Camera:
    
    def __init__(self, camFile = -1, fps=20, width=320, height=240):
        # Setup camera
        self.fps = fps
        self.camera = cv2.VideoCapture(camFile)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.camera.set(cv2.CAP_PROP_FPS, fps)
        self.fps = fps
        #rospy.init_node('camera_node')

    def compressImage(self, image, f = 3):
        
        newWidth = int(len(image[0]) / f)
        newHeight = int(len(image) / f)
        pixelMap = np.zeros((int(newHeight),int(newWidth),3), dtype = int)
        
        for i in range(newHeight):
            newI = i*f
            for j in range(newWidth):
                newJ = j*f
                subimage = image[newI:newI+f, newJ:newJ+f, :]
                outtemp = np.sum(subimage, axis=(0,1))
                p = np.asarray(outtemp/(f*f), dtype= 'int')
                pixelMap[i][j] = p

        return pixelMap
    
    def run(self): 
        rate = rospy.Rate(self.fps)
        bridge = CvBridge()
        publisher = rospy.Publisher('CameraToBase', Image, queue_size=10)
        while (self.camera is not None and self.camera.isOpened()):
            ret, frame = self.camera.read()
            if ret is not None:
                frame = self.compressImage(frame)
                publisher.publish(bridge.cv2_to_imgmsg(frame, encoding="bgr8"))
                rate.sleep()

        self.camera.release()

if __name__ == '__main__':
    # New camera
    camera = Camera()
    # Run the camera
    camera.run()
    camera.camera.release()


