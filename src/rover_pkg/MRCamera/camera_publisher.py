#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def start_node():
    # create node and publisher
    rospy.init_node('camera_sensor_publisher', anonymous = True)
    publisher = rospy.Publisher('CameraToBase', Image, queue_size = 60)

    # establish rate in HZ 
    rate = rospy.Rate(60)

    # create video capture and bridge
    video_capture = cv2.VideoCapture(0)
    bridge = CvBridge()

    imout = Image()

    # main control loop
    while not rospy.is_shutdown():
        #capture frame by frame
        ret, frame = video_capture.read()
        if ret == True:
            rospy.loginfo('Frame captured and published')

            # compress image
            # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
            # _, frame = cv2.imencode('.jpg', frame, encode_param)

            # convert to imgmsg and publish to topic
            # imout.data = frame
            image_to_topic = bridge.cv2_to_imgmsg(frame)
            publisher.publish(image_to_topic)

        rate.sleep()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass