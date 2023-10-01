#!/usr/bin/env python3
import rospy
import cv2 as cv
import numpy as np
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

# def compress_image(image, f = 3):
#     new_width = int(len(image[0]) / f)
#     new_height = int(len(image) / f)
#     pixel_map = np.zeros((int(new_height),int(new_width),3), dtype = int)
        
#     for i in range(new_height):
#         newI = i*f
#         for j in range(new_width):
#             newJ = j*f
#             subimage = image[newI:newI+f, newJ:newJ+f, :]
#             outtemp = np.sum(subimage, axis=(0,1))
#             p = np.asarray(outtemp/(f*f), dtype= 'int')
#             pixel_map[i][j] = p

#     return pixel_map

def start_node():
    # create node
    rospy.init_node('image_pub')
    rospy.loginfo('image_pub node started')

    # create bridge and video capture
    bridge = CvBridge()
    capture = cv.VideoCapture(0) 

    if not capture.isOpened():
        print("cannot open camera")
        exit()

    # create publisher with image data type
    pub = rospy.Publisher('image', Image, queue_size=10)

    # main control loop
    while not rospy.is_shutdown():
        #capture frame by frame
        ret, frame = capture.read()

        if not ret:
            print("Can't recieve frame")
            break

        #compress frame
        #compressed_frame = compress_image(frame)

        #display frame
        cv.imshow('video', compressed_frame)
        if cv.waitKey(1) == ord('q'):
            break

        # convert from opencv image to ros image
        img_msg = bridge.cv2_to_imgmsg(compressed_frame, "bgr8")

        # publish to topic
        pub.publish(img_msg)
        rospy.Rate(24.0).sleep()  # 1 Hz
    
    # release capture and destroy windows
    capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass