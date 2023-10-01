#!/usr/bin/env python3
import cv2 as cv
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

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

        #display frame
        cv.imshow('video', frame)
        if cv.waitKey(1) == ord('q'):
            break

        # convert from opencv image to ros image
        imgMsg = bridge.cv2_to_imgmsg(frame, "bgr8")

        # publish to topic
        pub.publish(imgMsg)
        rospy.Rate(24.0).sleep()  # 1 Hz
    
    # release capture and destroy windows
    capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass