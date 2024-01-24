#!/usr/bin/env python3
import sys
import cv2 as cv
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

# capture = cv.VideoCapture(0)
# if not capture.isOpened():
#     print("Cannot open camera")
#     exit(0)

# while True:
#     ret, frame = capture.read()
#     image_message = bridge.cv2_to_imgmsg(frame, encoding="passthrough")

#     if not ret:
#         print("Can't recieve frame")
#         break

def start_node():
    rospy.init_node('image_pub')
    rospy.loginfo('image_pub node started')

    # img = cv.imread(filename)
    # cv.imshow("image", img)
    # cv.waitKey(2000)

    bridge = CvBridge()
    capture = cv.VideoCapture(0) 

    if not capture.isOpened():
        print("cannot open camera")
        exit()

    pub = rospy.Publisher('image', Image, queue_size=10)

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

        imgMsg = bridge.cv2_to_imgmsg(frame, "bgr8")
        pub.publish(imgMsg)
        rospy.Rate(24.0).sleep()  # 1 Hz
    
    # release capture and destroy windows
    capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    try:
        # start_node(rospy.myargv(argv=sys.argv)[1])
        start_node()
    except rospy.ROSInterruptException:
        pass