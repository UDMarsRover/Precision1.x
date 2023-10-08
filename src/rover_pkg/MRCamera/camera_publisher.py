#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def start_node():
    # create node and publisher
    rospy.init_node('camera_sensor_publisher', anonymous = True)
    publisher = rospy.Publisher('video_topic', Image, queue_size = 60)

    # establish rate in HZ 
    rate = rospy.Rate(30)

    # create video capture and bridge
    video_capture = cv2.VideoCapture(0)
    bridge = CvBridge()

    # main control loop
    while not rospy.is_shutdown():
        #capture frame by frame
        ret, frame = video_capture.read()

        if ret == True:
            rospy.loginfo('Frame captured and published')

            # convert to imgmsg and publish to topic
            image_to_topic = bridge.cv2_to_imgmsg(frame)
            publisher.publish(image_to_topic)

        rate.sleep()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass