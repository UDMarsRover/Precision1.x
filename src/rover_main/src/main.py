#!/usr/bin/env python3
import time
import rospy
from std_msgs.msg import String as rosstring



pushTopic = 'RoverToBase'
count = 0
pub = rospy.Publisher(pushTopic, rosstring, queue_size=10)
rospy.init_node('RoverMain')


if __name__ == '__main__':
    while True:
        pub.publish('Go step on a Lego!')
        time.sleep(2)
        count += 1
        print(count)
