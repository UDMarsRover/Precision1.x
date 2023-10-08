#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def callback(msg):
    # create bridge
    bridge = CvBridge()

    rospy.loginfo("recieved a video message/frame")

    # convert back to cv and display image
    cv_image = bridge.imgmsg_to_cv2(msg)
    cv2.imshow("camera", cv_image)

    cv2.waitKey(1)

if __name__ == '__main__':
    # create node and subscriber
    rospy.init_node('camera_sensor_subscriber', anonymous=True)
    rospy.Subscriber('video_topic', Image, callback)

    # keep node running until shut down
    rospy.spin()

    cv2.destroyAllWindows()