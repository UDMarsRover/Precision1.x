#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def callback(msg):
    # create bridge
    bridge = CvBridge()

    rospy.loginfo("recieved a video message/frame")

    # convert back to cv and display image
    cv_image = bridge.imgmsg_to_cv2(msg)
    cv_image = cv2.imdecode(cv_image, cv2.IMREAD_COLOR)
    cv2.imshow("camera", cv_image)

    cv2.waitKey(1)
    
def start_node():
    # create node and subscriber
    rospy.init_node('camera_sensor_subscriber', anonymous=True)
    rospy.Subscriber('CameraToBase', Image, callback)

    # keep node running until shut down
    rospy.spin()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass