#!/usr/bin/env python3

import PIL
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

class Camera:
    
    def __init__(self, camFile = -1, fps=20, width=320, height=240):
        # Setup camera
        self.fps = fps
        self.camera = cv2.VideoCapture(camFile, cv2.CAP_V4L)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.camera.set(cv2.CAP_PROP_FPS, fps)
        self.fps = fps
        rospy.init_node('camera_node')

    def compressImage(self, image, factor = 2):
        width, height = image.size
        newImage = PIL.Image.new("RGB", (width / factor, height / factor), color = 0)
        newWidth, newHeight = newImage.size
        pixelMap = newImage.load
        
        for i in range(newWidth):
            for j in range (newHeight):
                r, g, b = 0
                r, g, b += image.getPixel(i * 2, j * 2)
                r, g, b += image.getPixel(i * 2 + 1, j * 2)
                r, g, b += image.getPixel(i * 2, j * 2 + 1)
                r, g, b += image.getPixel(i * 2 + 1, j * 2 + 1)
                r, g, b /= 4
                pixelMap[i,j] = (r, g, b)
        return newImage
    
    def run(self): 
        rate = rospy.Rate(self.fps)
        bridge = CvBridge()
        publisher = rospy.Publisher('CameraToBase', Image, queue_size=10)
        while (self.camera is not None and self.camera.isOpened()):
            ret, frame = self.camera.read()
            if ret is not None:
                publisher.publish(bridge.cv2_to_compressed_imgmsg(frame, dst_format='jpg'))
                rate.sleep()

        self.camera.release()

if __name__ == '__main__':
    # New camera
    camera = Camera()
    # Run the camera
    camera.run()


